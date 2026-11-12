# Whatsmiau — MCP

Docs: [https://whatsmiau.dev/docs/mcp](https://whatsmiau.dev/docs/mcp)  
Endpoint: `https://mcp.whatsmiau.dev`  
Auth: OAuth 2.0 (Dynamic Client Registration). Token local renovado pelo cliente.

## Config Cursor

`~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "whatsmiau": {
      "url": "https://mcp.whatsmiau.dev"
    }
  }
}
```

Claude Desktop (via mcp-remote):

```json
{
  "mcpServers": {
    "whatsmiau": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.whatsmiau.dev"]
    }
  }
}
```

Teste: “liste minhas instâncias do WhatsApp” → tool `list_instances`.

## Tools (23) ↔ REST

### Instâncias (7)

| MCP | REST aproximado |
|-----|-----------------|
| `list_instances` | `GET /instance/fetchInstances` |
| `create_instance` | `POST /instance/create` |
| `get_instance_details` | estado + config da instância |
| `connect_instance` | `GET /instance/connect/:name` (QR base64) |
| `logout_instance` | `DELETE /instance/logout/:name` |
| `delete_instance` | `DELETE /instance/delete/:name` |
| `update_instance` | `PUT /instance/update/:name` |

### Mensagens (12)

| MCP | REST |
|-----|------|
| `send_text_message` | `POST /message/sendText/:instance` |
| `send_media_message` | `POST /message/sendMedia/:instance` |
| `send_audio_message` | `POST /message/sendWhatsAppAudio/:instance` |
| `send_list_message` | `POST /message/sendList/:instance` |
| `send_button_message` | `POST /message/sendButtons/:instance` |
| `send_sticker_message` | `POST /message/sendSticker/:instance` |
| `send_location_message` | `POST /message/sendLocation/:instance` |
| `send_contact_message` | `POST /message/sendContact/:instance` |
| `send_poll_message` | `POST /message/sendPoll/:instance` |
| `send_ptv_message` | `POST /message/sendPtv/:instance` |
| `send_status_message` | `POST /message/sendStatus/:instance` |
| `send_reaction` | `POST /message/sendReaction/:instance` |

### Chat & webhook (4)

| MCP | REST |
|-----|------|
| `mark_message_as_read` | `POST /chat/markMessageAsRead/:instance` |
| `send_typing_indicator` | `POST /chat/sendPresence/:instance` |
| `check_whatsapp_number` | `POST /chat/whatsappNumbers/:instance` |
| `get_webhook` | `GET /webhook/find/:instance` |

## Só via REST (sem tool MCP)

- Grupos (`/group/*`)
- Comunidades (`/community/*`)
- `DELETE /chat/deleteMessageForEveryone/:instance`
- `GET /instance/connect/:name/image` (PNG)
- `POST /webhook/set/:instance` (set completo — MCP atualiza webhook via `update_instance`)

## Workflow agente

```
1. list_instances
2. Se DISCONNECTED → connect_instance → mostrar QR ao usuário → poll status
3. check_whatsapp_number antes do primeiro contato
4. send_*_message
5. mark_message_as_read / send_reaction conforme UX
```

Params MCP usam snake_case (`instance`, `media_url`, `audio_url`). REST usa camelCase Evolution (`instanceName`, `mediatype`, `media`).
