# WhatsApp Cloud API — Review Checklist

Checklist de validação obrigatória para auditoria de código WhatsApp.
Referência principal em [SKILL.md](SKILL.md).

---

## 1. Token de Acesso

| Regra | Validar |
|---|---|
| Tipo | System User Token permanente (nunca expira) |
| Proibido | User Access Token temporário / token do dashboard de testes |
| Permissões mínimas | `whatsapp_business_messaging` + `whatsapp_business_management` + `business_management` |
| Armazenamento | Variável de ambiente ou vault — nunca hardcoded |
| Verificação no código | Validar presença antes de chamar API, erro claro se ausente |

Tokens temporários expiram em ~1h → erro `190` em produção.

---

## 2. Endpoint e Payload

| Regra | Validar |
|---|---|
| Endpoint envio | `POST /{phoneNumberId}/messages` — nunca `wabaId` |
| Versão API | v21.0+ mínimo, v23.0+ preferível. Não misturar |
| Campo obrigatório | `"messaging_product": "whatsapp"` em TODO payload |
| `wabaId` | Somente para templates, Flows, analytics |
| Base URL | `https://graph.facebook.com/v{VERSION}` |

---

## 3. Coexistence

| Regra | Validar |
|---|---|
| Suporte | Mesmo número em WhatsApp Business App + Cloud API simultaneamente |
| Webhook obrigatório | Assinar `smb_message_echoes` no dashboard |
| No código | Tratar `smb_message_echoes` para espelhar mensagens do app no sistema |
| Cobrança | API cobrada / App gratuita (nos limites) |
| Sync | Histórico sincronizado em tempo real |

---

## 4. Webhooks

| Regra | Validar |
|---|---|
| Assinatura | Verificar `X-Hub-Signature-256` com HMAC SHA256 do App Secret |
| Verify Token | GET retorna `hub.challenge` quando `hub.verify_token` confere |
| Resposta | HTTP 200 em < 5 segundos, processar async |
| Idempotência | Guardar `message_id`, ignorar duplicados |
| Status tracking | Processar `sent`, `delivered`, `read`, `failed`, `deleted` |
| Campos assinados | `messages`, `message_statuses`, `smb_message_echoes` (mínimo) |

---

## 5. Error Handling e Retry

### Padrão obrigatório
```
1. Verificar HTTP status antes de parsear JSON
2. Extrair error.code e error.error_subcode da resposta
3. Logar fbtrace_id para suporte Meta
4. Retry com exponential backoff SOMENTE para erros transitórios
5. Nunca retry em erros permanentes
```

### Classificação de erros

| Tipo | Códigos | Ação |
|---|---|---|
| Transitório (retry) | HTTP 429, 5xx, code 131053 | Backoff exponencial, respeitar `Retry-After` |
| Permanente (sem retry) | 100, 131026, 132000, 190, 200 | Log + notificar + abortar |
| Janela expirada | 131047 | Usar template HSM |

### Implementação de retry
```typescript
async function callWithRetry<T>(fn: () => Promise<T>, maxRetries = 3): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn()
    } catch (error) {
      if (!error.isRetryable || attempt === maxRetries) throw error
      const delay = Math.min(1000 * 2 ** attempt, 30000)
      await new Promise(r => setTimeout(r, delay))
    }
  }
  throw new Error('Max retries exceeded')
}
```

---

## 6. Templates HSM

| Regra | Validar |
|---|---|
| Gerenciamento | Via `wabaId`: `/{wabaId}/message_templates` |
| Envio | Via `phoneNumberId` com type `template` |
| Categorias válidas | `MARKETING`, `UTILITY`, `AUTHENTICATION` |
| Parâmetros | Mapear `{{1}}`, `{{2}}` para `components[].parameters[]` |
| Janela 24h | Fora da janela, SÓ templates aprovados |
| Status webhook | Tratar `message_template_status_update` |

---

## 7. Mídia

| Regra | Validar |
|---|---|
| Download | URL temporária expira ~5 min — baixar imediatamente no webhook |
| Fluxo | `GET /{mediaId}` → URL → `GET {url}` com Bearer → salvar permanente |
| Upload | `POST /{phoneNumberId}/media` com multipart/form-data |
| Limites | Imagem 5MB, Vídeo 16MB, Áudio 16MB, Documento 100MB |

---

## 8. Segurança e Compliance

| Regra | Validar |
|---|---|
| Tokens em logs | Nunca expor access tokens em logs ou respostas HTTP |
| HMAC | Nunca confiar em dados do webhook sem validar assinatura |
| Sanitização | Sanitizar dados do webhook antes de persistir |
| Rate limiting | Rate limiting próprio no endpoint webhook |
| Validação | Verificar que `phoneNumberId` no webhook corresponde ao configurado |
| LGPD/GDPR | Opt-in explícito antes de enviar mensagens, respeitar opt-out |
| Dados sensíveis | Não persistir mídia sem necessidade, cleanup periódico |

---

## 9. Red Flags — Reprovar Imediatamente

Qualquer um destes itens resulta em **Problema encontrado**:

1. Token hardcoded no código fonte
2. Ausência de `messaging_product: "whatsapp"` no payload
3. Usar `wabaId` no endpoint de envio de mensagens
4. Webhook sem validação de assinatura HMAC
5. Webhook que não retorna 200 antes de processar
6. Retry em erros permanentes (190, 100, 200)
7. Download de mídia sem tratamento de expiração da URL
8. Token temporário do dashboard usado em produção
9. Logs expondo access tokens
10. Ausência de tratamento de `smb_message_echoes` quando Coexistence está ativo
11. Envio de mensagem free-form fora da janela de 24h sem template
12. Ausência de `fbtrace_id` no log de erros

---

## 10. Padrão de Código — Mínimo Aceitável

### Envio de mensagem
```typescript
async function sendWhatsAppMessage(
  phoneNumberId: string, to: string, text: string, accessToken: string
) {
  const response = await fetch(
    `https://graph.facebook.com/v25.0/${phoneNumberId}/messages`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messaging_product: 'whatsapp',
        to,
        type: 'text',
        text: { body: text },
      }),
    }
  )

  const data = await response.json()

  if (!response.ok) {
    const errorCode = data?.error?.code
    const fbtrace = data?.error?.fbtrace_id
    const isRetryable = response.status === 429 || response.status >= 500 || errorCode === 131053
    logger.error({ errorCode, fbtrace, status: response.status }, 'WhatsApp API error')
    throw new WhatsAppApiError(data.error, isRetryable)
  }

  return data
}
```

### Webhook handler
```typescript
async function handleWebhook(req: FastifyRequest, reply: FastifyReply) {
  const signature = req.headers['x-hub-signature-256'] as string
  if (!verifyHmacSignature(req.rawBody, signature, APP_SECRET)) {
    return reply.code(401).send()
  }

  reply.code(200).send()

  const { entry } = req.body as WebhookPayload
  for (const e of entry) {
    for (const change of e.changes) {
      switch (change.field) {
        case 'messages':
          await processMessages(change.value)
          break
        case 'smb_message_echoes':
          await processAppEchoes(change.value)
          break
      }
    }
  }
}
```

---

## 11. Checklist Rápida (copiar e acompanhar)

```
Validação WhatsApp Cloud API:
- [ ] Token: System User permanente (não temporário)
- [ ] Permissões: messaging + management + business_management
- [ ] Endpoint: /{phoneNumberId}/messages (não wabaId)
- [ ] messaging_product: "whatsapp" presente
- [ ] Webhook: HMAC validado
- [ ] Webhook: responde 200 antes de processar
- [ ] Webhook: idempotente (message_id tracking)
- [ ] Webhook: smb_message_echoes tratado (Coexistence)
- [ ] Erros: retry apenas em transitórios
- [ ] Erros: fbtrace_id logado
- [ ] Mídia: download imediato (URL expira)
- [ ] Templates: via wabaId, envio via phoneNumberId
- [ ] Janela 24h: template obrigatório fora da janela
- [ ] Segurança: tokens em env vars, nunca hardcoded
- [ ] LGPD: opt-in/opt-out respeitados
```
