---
name: whatsapp-meta-api
description: "Senior specialist in the WhatsApp Business Cloud API (Meta Graph API v23.0+). Two roles: (1) implementation reference with endpoints, payloads and patterns; (2) strict code validator that audits compliance, security and Meta best practices. Use when implementing, reviewing or fixing any WhatsApp integration: sending messages, HSM templates, webhooks, media, Coexistence, Flows, groups, automations, or when the user mentions WhatsApp, WABA, Graph API or Cloud API. For the Whatsmiau provider use whatsmiau. PT-BR: Especialista em WhatsApp Business Cloud API (Graph API Meta v23.0+): referência de implementação e validador de código para conformidade, segurança e boas práticas da Meta. Use ao implementar, revisar ou corrigir integração WhatsApp: envio de mensagens, templates HSM, webhooks, mídia, Coexistence, Flows, grupos, automações, \"revisar WhatsApp\", \"validar integração WhatsApp\"."
---

# WhatsApp Business Cloud API

Skill unificada: referência técnica + validador/reviewer de código.
Para regras detalhadas de validação, ver [review-checklist.md](review-checklist.md).

---

## Modo Reviewer — Formato de Resposta

Ao revisar código WhatsApp, iniciar **sempre** com:

- **Aprovado** — Código correto, conforme melhores práticas Meta 2026.
- **Parcialmente correto** — Funciona mas tem pontos a melhorar.
- **Problema encontrado** — Erros que impedem funcionamento ou violam regras da Meta.

Listar pontos específicos, sugerir código corrigido, e mencionar compatibilidade com **Coexistence** quando envolver envio/recebimento.

---

## Contexto do Projeto

**Stack:** Fastify + Prisma + TypeScript + Bun
**API version:** `v25.0` (manter consistente — não misturar versões)
**Base URL:** `https://graph.facebook.com/v25.0`

### Credenciais (formato correto)
```typescript
// CORRETO — usado em official.provider.ts e client.whatsapp.ts
{ phoneNumberId: string, wabaId: string, accessToken: string }

// ERRADO — formato legado em whatsapp.service.ts (não usar)
{ apiUrl: string, token: string, phoneId?: string }
```

### Autenticação
```typescript
headers: {
  Authorization: `Bearer ${creds.accessToken}`,
  'Content-Type': 'application/json',
}
```

### `wabaId` vs `phoneNumberId`
- `phoneNumberId` → envio de mensagens (`POST /{phoneNumberId}/messages`)
- `wabaId` → templates, Flows, analytics (`GET /{wabaId}/message_templates`)
- Ambos obrigatórios em `IntegrationConfig.credentials`

---

## Permissões OAuth

| Permissão | Habilita | Obrigatória |
|---|---|---|
| `whatsapp_business_messaging` | Enviar mensagens, webhooks de mensagem/status, grupos | Sim |
| `whatsapp_business_management` | Templates HSM, gerenciar número, Flows, analytics, webhooks de conta | Sim |
| `business_management` | Acesso ao portfólio WABA (account info, analytics agregado) | Sim |
| `whatsapp_business_manage_events` | Marketing Messages Lite API (otimizações automáticas) | Opcional |

---

## Coexistence (WhatsApp Business App + Cloud API)

Desde março/2025, mesmo número pode usar simultaneamente WhatsApp Business App + Cloud API.

| Aspecto | Detalhe |
|---|---|
| Sincronização | Mensagens API aparecem no app e vice-versa, tempo real |
| Webhook | Mensagens do app: evento `smb_message_echoes` |
| Cobrança | Via API: cobrada. Via app: gratuita (dentro dos limites) |
| Campo obrigatório no webhook | Assinar `smb_message_echoes` no dashboard Meta |
| No código | Tratar `smb_message_echoes` para espelhar mensagens do app no sistema |

---

## Envio de Mensagens — `POST /{phoneNumberId}/messages`

### Texto
```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "text",
  "text": { "body": "Mensagem aqui" }
}
```

### Template HSM
```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "nome_do_template",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "body",
        "parameters": [
          { "type": "text", "text": "valor_variavel_1" }
        ]
      }
    ]
  }
}
```

### Mídia (image/video/audio/document/sticker)
```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "image",
  "image": { "link": "https://url-da-imagem.jpg", "caption": "Legenda" }
}
```
`document`: adicionar `"filename"`. `audio`/`sticker`: sem `caption`.

### Interactive — Reply Buttons
```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "body": { "text": "Escolha:" },
    "action": {
      "buttons": [
        { "type": "reply", "reply": { "id": "btn_1", "title": "Sim" } },
        { "type": "reply", "reply": { "id": "btn_2", "title": "Não" } }
      ]
    }
  }
}
```

### Interactive — Lista
```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "body": { "text": "Selecione:" },
    "action": {
      "button": "Ver opções",
      "sections": [{
        "title": "Seção 1",
        "rows": [{ "id": "row_1", "title": "Opção 1", "description": "Descrição" }]
      }]
    }
  }
}
```

### Reaction / Marcar como lida
```json
// Reaction
{ "messaging_product": "whatsapp", "to": "...", "type": "reaction",
  "reaction": { "message_id": "wamid.xxx", "emoji": "👍" } }

// Mark as read
{ "messaging_product": "whatsapp", "status": "read", "message_id": "wamid.xxx" }

// Mark as read + typing indicator (some ao enviar resposta ou após 25s)
{ "messaging_product": "whatsapp", "status": "read", "message_id": "wamid.xxx",
  "typing_indicator": { "type": "text" } }
```

### Location / Contacts
```json
// Location
{ "messaging_product": "whatsapp", "to": "...", "type": "location",
  "location": { "latitude": -23.55, "longitude": -46.63, "name": "Local", "address": "Endereço" } }

// Contacts
{ "messaging_product": "whatsapp", "to": "...", "type": "contacts",
  "contacts": [{ "name": { "formatted_name": "Nome" }, "phones": [{ "phone": "5511..." }] }] }
```

---

## Marketing Messages Lite API

**Permissão:** `whatsapp_business_manage_events`

Mesmo endpoint de mensagens, com campo adicional `biz_opaque_callback_data` para rastreamento de conversão. Pacing automático e per-user limits.

Webhook `user_preferences`: indica opt-out de marketing — **deve ser respeitado**.

---

## Templates HSM — via `wabaId`

**Permissão:** `whatsapp_business_management`

| Operação | Endpoint |
|---|---|
| Listar | `GET /{wabaId}/message_templates?fields=id,name,status,category,language,components` |
| Criar | `POST /{wabaId}/message_templates` |
| Deletar | `DELETE /{wabaId}/message_templates?name=nome` |

Categorias: `MARKETING`, `UTILITY`, `AUTHENTICATION`
Status: `APPROVED`, `REJECTED`, `PENDING`, `PAUSED`, `DISABLED`
Webhook: `message_template_status_update`

---

## Download de Mídia — Fluxo Obrigatório

URL temporária expira em ~5 min. Baixar **imediatamente** no webhook.

```
1. GET /{mediaId} → obtém { url, mime_type, file_size }
2. GET {url} com Bearer token → baixa o arquivo
3. Upload MinIO/R2 → persiste URL permanente
```

Limites: Imagem 5MB, Vídeo 16MB, Áudio 16MB, Documento 100MB.

---

## Business Profile

```
GET /{phoneNumberId}/whatsapp_business_profile?fields=about,address,description,email,websites,profile_picture_url,vertical
POST /{phoneNumberId}/whatsapp_business_profile
{ "messaging_product": "whatsapp", "about": "...", "address": "...", "description": "...",
  "email": "...", "websites": ["https://..."], "vertical": "OTHER" }
```

Foto de perfil: enviar como mídia primeiro, depois referenciar pelo media ID.

---

## Webhooks — Estrutura e Eventos

### Payload base
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "{WABA_ID}",
    "changes": [{
      "field": "messages",
      "value": {
        "metadata": { "phone_number_id": "...", "display_phone_number": "..." },
        "messages": [...],
        "statuses": [...],
        "contacts": [...]
      }
    }]
  }]
}
```

### Eventos a assinar

| Campo | Permissão | Ação |
|---|---|---|
| `messages` | `whatsapp_business_messaging` | Processar mensagens recebidas |
| `message_statuses` | `whatsapp_business_messaging` | sent/delivered/read/failed/deleted |
| `smb_message_echoes` | `whatsapp_business_messaging` | Coexistence — mensagens do app |
| `message_template_status_update` | `whatsapp_business_management` | Atualizar status template no DB |
| `message_template_quality_update` | `whatsapp_business_management` | Notificar admin |
| `phone_number_quality_update` | `whatsapp_business_management` | Alertar — risco de suspensão |
| `phone_number_name_update` | `whatsapp_business_management` | Atualizar display name |
| `account_alerts` | `whatsapp_business_management` | Registrar alertas críticos |
| `user_preferences` | `whatsapp_business_manage_events` | Respeitar opt-out marketing |

### Validação obrigatória
- Verificar `X-Hub-Signature-256` com HMAC SHA256 do App Secret
- Endpoint GET retorna `hub.challenge` quando `hub.verify_token` confere
- Retornar HTTP 200 em < 5 segundos, processar async depois
- Idempotência: guardar `message_id`, ignorar duplicados

---

## Gerenciamento de Número

```
GET /{phoneNumberId}?fields=display_phone_number,verified_name,quality_rating,status,name_status
POST /{phoneNumberId}/request_code  → { "code_method": "SMS", "language": "pt_BR" }
POST /{phoneNumberId}/verify_code   → { "code": "123456" }
POST /{phoneNumberId}/deregister
POST /{phoneNumberId}               → { "display_name": "Novo Nome" } (requer aprovação)
```

---

## Grupos

**Permissão:** `whatsapp_business_messaging` + feature habilitada

```
POST /{phoneNumberId}/groups          → { "subject": "Nome", "description": "..." }
POST /{groupId}/participants          → { "participants": [{ "wa_id": "5511..." }] }
DELETE /{groupId}/participants        → { "participants": [{ "wa_id": "5511..." }] }
Enviar mensagem: to = "{groupId}@g.us"
```

---

## Flows API (Interactive Flows)

**Permissão:** `whatsapp_business_management`

```
POST /{wabaId}/flows                → criar flow
GET /{wabaId}/flows                 → listar flows
POST /{flowId}/publish              → publicar flow
```

Envio via mensagem interativa com `type: "flow"` no campo `interactive.action`.

---

## Calling (Voice/Video — 2026)

Recurso novo. Requer habilitação específica na conta WABA.
Endpoint: `POST /{phoneNumberId}/calls`
Webhooks: `call_events` (ringing, answered, ended, failed)

---

## Analytics

```
GET /{wabaId}/analytics?start=YYYY-MM-DD&end=YYYY-MM-DD&granularity=DAY&phone_numbers=["{phoneNumberId}"]&product_types=[0]
```
Retorna: `sent`, `delivered`, `read` por dia.

---


## Erros Comuns da API Meta

| Código | Significado | Retry? |
|---|---|---|
| 100 | Parâmetro inválido | Não |
| 131026 | Número não existe no WhatsApp | Não |
| 131047 | Janela de 24h expirada — usar template | Não |
| 131053 | Servidor indisponível | Sim (backoff) |
| 132000 | Template não aprovado | Não |
| 190 | Token expirado/inválido | Não |
| 200 | Permissão insuficiente | Não |
| HTTP 429 | Rate limiting | Sim (respeitar Retry-After) |
| HTTP 5xx | Erro temporário Meta | Sim (backoff) |

**Sempre logar `fbtrace_id`** da resposta de erro para suporte Meta.

---

## Variáveis de Ambiente

```bash
WHATSAPP_APP_ID=              # ID do App Meta
WHATSAPP_APP_SECRET=          # Secret para HMAC do webhook
WHATSAPP_WEBHOOK_VERIFY_TOKEN=
WHATSAPP_EMBEDDED_SIGNUP_CONFIG_ID=
# Testes:
WHATSAPP_TEST_PHONE_NUMBER_ID=
WHATSAPP_TEST_ACCESS_TOKEN=
WHATSAPP_TEST_RECIPIENT=
```

Nunca hardcodar tokens. Nunca commitar `.env` ou arquivos com tokens em texto puro.

---

## Referências

- [Visão geral](https://developers.facebook.com/documentation/business-messaging/whatsapp/overview/)
- [Permissões](https://developers.facebook.com/documentation/business-messaging/whatsapp/permissions/)
- [Envio de mensagens](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages/)
- [Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-management/)
- [MM Lite API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/marketing-messages-lite-api)
- [Media API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/media/media-api)
- [Phone Number API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/phone-number-management-api)
- [Groups API](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/)
- [Flows API](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/)
- [Webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview/)
- [Coexistence](https://developers.facebook.com/documentation/business-messaging/whatsapp/coexistence/)
- [Error Codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)
- [Business Profile](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/business/business-profile-api)
