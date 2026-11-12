# Whatsmiau — Webhooks e eventos

Docs: [https://whatsmiau.dev/docs/webhooks](https://whatsmiau.dev/docs/webhooks)

## Configuração

```bash
# Set
curl -X POST https://api.whatsmiau.dev/v2/webhook/set/Marketing01 \
  -H "Content-Type: application/json" \
  -H "apikey: $WHATSMIAU_API_KEY" \
  -d '{
    "webhook": {
      "enabled": true,
      "url": "https://meusite.com/webhook",
      "events": ["messages.upsert", "connection.update"],
      "headers": { "Authorization": "Bearer meu_token" }
    }
  }'

# Find
curl -X GET https://api.whatsmiau.dev/v2/webhook/find/Marketing01 \
  -H "apikey: $WHATSMIAU_API_KEY"
```

Também configurável em `POST /instance/create` e `PUT /instance/update/:name` via objeto `webhook`.

Regras:
- URL deve ser HTTPS pública (localhost / IPs privados bloqueados — SSRF).
- Sem `events` → todos os eventos.
- `base64: true` → mídia no payload em base64.

## Envelope padrão

```ts
{
  event: string        // ex: "messages.upsert"
  instance: string     // id/nome da instância
  data: T              // payload do evento
  date_time: string    // ISO 8601
  sender?: string
  server_url?: string
}
```

## Eventos

### `messages.upsert`

Nova mensagem recebida ou enviada (texto, mídia, reação, contato, lista, botões, …).

`data` principal:
- `key.{remoteJid, fromMe, id, participant?}`
- `pushName`, `status` (`sent`|`received`)
- `message` — um dos: `conversation`, `imageMessage`, `videoMessage`, `audioMessage`, `documentMessage`, `reactionMessage`, `contactMessage`, `listResponseMessage`, …
- `mediaUrl?` — URL pública após upload no storage
- `messageType`, `messageTimestamp`, `instanceId`
- `contextInfo?` — reply/menção/efêmera (`stanzaId`, `quotedMessage`, `mentionedJid`, `expiration`)

### `messages.update`

Status de entrega/leitura.

- `status`: `DELIVERY_ACK` | `READ`
- `keyId` / `messageId`, `remoteJid`, `fromMe`, `participant`, `instanceId`

### `messages.set`

Histórico em lotes ao conectar. Requer `syncFullHistory: true` na create **e** evento inscrito.

Envelope extra: `isLatest` (bool), `progress` (0–100).  
`data` = array no formato de `messages.upsert`.

### `connection.update`

- `state`: `open` | `close`
- `statusReason`: 200 = sucesso
- Com `open`: `wuid`, `profileName`, `profilePictureUrl?`

### `contacts.upsert`

Array de contatos/grupos: `remoteJid`, `remoteLid`, `pushName`, `profilePicUrl`, `instanceId`.

### `messages.delete`

Revogação (apagar para todos): `id`, `remoteJid`, `fromMe`, `participant`, `status: "DELETED"`.

### `group-participants.update`

- `action`: `add` | `remove` | `promote` | `demote`
- `id` = JID do grupo
- `author`, `participants[]` (`id`, `phoneNumber`, `admin`)
- `participantsData` (compat Evolution)

## Handler (padrão)

1. Validar headers customizados se configurados.
2. Responder 200 imediatamente.
3. Filtrar por `event` + `instance`.
4. Idempotência por `data.key.id` / `keyId` quando possível.
5. Não processar `fromMe: true` em bots de atendimento, salvo se necessário.
