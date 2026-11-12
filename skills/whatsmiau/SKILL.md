---
name: whatsmiau
description: "Integrates and operates the Whatsmiau Cloud API v2 (WhatsApp): instances, messages, chat, webhooks, groups, communities and MCP. Use when integrating WhatsApp through Whatsmiau or an Evolution-compatible API, sending messages, managing instances or QR codes, webhooks or groups, or when the user mentions Whatsmiau, api.whatsmiau.dev or mcp.whatsmiau.dev. For Meta's official API use whatsapp-meta-api. PT-BR: Integra e opera a Whatsmiau Cloud API v2 (WhatsApp): instâncias, mensagens, chat, webhooks, grupos, comunidades e MCP. Use ao integrar WhatsApp via Whatsmiau ou API compatível com Evolution, enviar mensagens, gerenciar instâncias/QR, webhooks ou grupos."
---

# Whatsmiau Cloud API v2

Fonte oficial: [docs](https://whatsmiau.dev/docs/getting-started) · Base REST: `https://api.whatsmiau.dev/v2` · MCP: `https://mcp.whatsmiau.dev`

Compatível com Evolution API: código Evolution existente funciona trocando a base URL.

## Quando usar o quê

| Cenário | Preferir |
|---------|----------|
| Agente no Codex já autenticado no MCP `user-whatsmiau` | Tools MCP (`list_instances`, `send_text_message`, …) |
| Código de produção / backend do app | REST + header `apikey` |
| Operação pontual sem MCP | `curl` REST |

Antes de enviar mensagem via MCP: `list_instances` → confirmar `CONNECTED` → `check_whatsapp_number` se o número for incerto.

## Autenticação REST

Todas as rotas: header `apikey: <CHAVE>` (Dashboard → Chave API). Escopo por conta.

```bash
curl -X GET https://api.whatsmiau.dev/v2/instance/fetchInstances \
  -H "apikey: $WHATSMIAU_API_KEY"
```

Variável sugerida: `WHATSMIAU_API_KEY` (nunca commitar).

## Convenções críticas

1. **Identificador = `instanceName`** escolhido na criação. Path `:name` / `:instance` usa esse nome — sem ObjectID separado.
2. **Números**: DDI+DDD+número, só dígitos. BR: `5511999887766`. Sem `+`, espaços ou hífen.
3. **JIDs**: DM `5511...@s.whatsapp.net` · grupo `120363...@g.us`.
4. **Estados**: `open` / `CONNECTED` · `closed` / `DISCONNECTED` · `connecting` · `qr-code`. Suspensa por plano: `closed` + `suspended: true`.
5. **Mídia**: URL HTTPS pública. Webhook URL: HTTPS público; localhost/IPs privados bloqueados (SSRF).
6. **Formatação texto**: `*negrito*` `_itálico_` `~riscado~` ` ```mono``` `.

## Fluxo mínimo (conectar + enviar)

```
1. POST /instance/create  { "instanceName": "Marketing01", "qrcode": true }
2. GET  /instance/connect/Marketing01          → QR base64 / pairing code
   ou GET /instance/connect/Marketing01/image  → PNG
3. GET  /instance/connectionState/Marketing01  → state == "open"
4. POST /chat/whatsappNumbers/Marketing01      { "numbers": ["5511..."] }
5. POST /message/sendText/Marketing01          { "number": "5511...", "text": "Olá" }
```

Logout (mantém slot): `DELETE /instance/logout/:name`  
Delete permanente: `DELETE /instance/delete/:name`

## Mapa rápido de endpoints

### Instâncias — [docs/instances](https://whatsmiau.dev/docs/instances)

| Método | Path |
|--------|------|
| POST | `/instance/create` |
| GET | `/instance/fetchInstances` |
| GET | `/instance/connect/:name` |
| GET | `/instance/connect/:name/image` |
| GET | `/instance/connectionState/:name` |
| PUT | `/instance/update/:name` |
| DELETE | `/instance/logout/:name` |
| DELETE | `/instance/delete/:name` |

Create body essencial: `instanceName` (obrigatório). Opcionais: `qrcode`, `rejectCall`, `msgCall`, `groupsIgnore`, `alwaysOnline`, `readMessages`, `readStatus`, `syncFullHistory`, `webhook.{enabled,url,events,base64}`, proxy\* (Enterprise), `migration` (Enterprise).

### Mensagens — [docs/messages](https://whatsmiau.dev/docs/messages)

| Método | Path | Notas |
|--------|------|-------|
| POST | `/message/sendText/:instance` | `number`, `text`; opcional `delay` (máx 300000), `quoted`, mentions |
| POST | `/message/sendMedia/:instance` | `number`, `media` URL, `mediatype`: image/video/document |
| POST | `/message/sendWhatsAppAudio/:instance` | PTT; `audio` URL |
| POST | `/message/sendList/:instance` | sections/rows; resposta via webhook `listResponseMessage` |
| POST | `/message/sendButtons/:instance` | até 3 reply (limite WA); type `reply` |
| POST | `/message/sendSticker/:instance` | WebP preferencial |
| POST | `/message/sendLocation/:instance` | `latitude`, `longitude` |
| POST | `/message/sendContact/:instance` | array de vCards |
| POST | `/message/sendPoll/:instance` | `values` 2–10; `selectableCount` |
| POST | `/message/sendPtv/:instance` | vídeo redondo ≤60s MP4 |
| POST | `/message/sendStatus/:instance` | status próprio; **sem** `number` |

### Chat — [docs/chat](https://whatsmiau.dev/docs/chat)

| Método | Path |
|--------|------|
| POST | `/message/sendReaction/:instance` |
| POST | `/chat/sendPresence/:instance` | `composing` / presence + `type` text\|audio |
| POST | `/chat/markMessageAsRead/:instance` |
| POST | `/chat/whatsappNumbers/:instance` |
| DELETE | `/chat/deleteMessageForEveryone/:instance` |

### Webhooks — [docs/webhooks](https://whatsmiau.dev/docs/webhooks)

| Método | Path |
|--------|------|
| POST | `/webhook/set/:instance` |
| GET | `/webhook/find/:instance` |

Eventos: `messages.upsert`, `messages.update`, `messages.delete`, `messages.set` (exige `syncFullHistory: true` na create), `connection.update`, `contacts.upsert`, `group-participants.update`.

Detalhes de payload: [reference-webhooks.md](reference-webhooks.md)

### Grupos / Comunidades

Catálogo completo + params: [reference-api.md](reference-api.md)  
Docs: [groups](https://whatsmiau.dev/docs/groups) · [communities](https://whatsmiau.dev/docs/communities)

## MCP (Codex)

Endpoint: `https://mcp.whatsmiau.dev` (OAuth; não precisa colar API key no mcp.json).

```json
{ "mcpServers": { "whatsmiau": { "url": "https://mcp.whatsmiau.dev" } } }
```

23 tools — mapa MCP↔REST em [reference-mcp.md](reference-mcp.md).

**Lacunas MCP vs REST:** grupos/comunidades e delete-message-for-everyone existem só na REST. Para esses, usar `curl`/código.

## Regras ao implementar no código

- Não inventar paths fora da tabela / [endpoints.json](endpoints.json).
- Sempre tratar `connectionState` antes de send.
- Webhook: responder 2xx rápido; processar async.
- `messages.set` só com `syncFullHistory: true` + evento inscrito.
- Proxy/migration: Enterprise only — não assumir em planos menores.
- Botões: máx 3. Cada item: `{ "type": "reply", "displayText": "...", "id": "..." }` (também há botões PIX na docs). Lista: até 10 sections × 10 rows (máx 30 rows).
- `sendMedia`: enviar `mediatype` (`image`|`video`|`document`) + `media` (URL) — campo `mediatype` aparece nos exemplos oficiais.

## Checklist de verificação

```
- [ ] apikey válida (fetchInstances 200)
- [ ] instanceName estável e único na conta
- [ ] state open antes de enviar
- [ ] número validado (whatsappNumbers) quando aplicável
- [ ] webhook HTTPS público se precisa receber eventos
- [ ] eventos inscritos batem com o handler
```

## Referências

- [reference-api.md](reference-api.md) — todos os endpoints + params
- [reference-webhooks.md](reference-webhooks.md) — envelope e eventos
- [reference-mcp.md](reference-mcp.md) — tools MCP
- [endpoints.json](endpoints.json) — extrato estruturado da docs
