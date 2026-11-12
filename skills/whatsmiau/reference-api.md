# Whatsmiau API — referência de endpoints

Base: `https://api.whatsmiau.dev/v2`

Auth: header `apikey`.

Gerado a partir da documentação oficial (+ patches dos exemplos oficiais para campos omitidos no schema da UI).

## Instâncias

### `POST /instance/create`

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `instanceName` | string | sim | Identificador único da instância dentro da sua conta. Será usado como :name em todos os outros endpoints. |
| `qrcode` | boolean | não | Retorna o QR Code na resposta de criação (se suportado pelo core). |
| `token` | string | não | Token personalizado. |
| `rejectCall` | boolean | não | Rejeita automaticamente chamadas recebidas. |
| `msgCall` | string | não | Mensagem enviada automaticamente ao rejeitar uma chamada. |
| `groupsIgnore` | boolean | não | Ignora eventos de grupos no webhook. |
| `alwaysOnline` | boolean | não | Mantém a conta sempre online no WhatsApp. |
| `readMessages` | boolean | não | Marca automaticamente as mensagens como lidas. |
| `readStatus` | boolean | não | Marca automaticamente status como visto. |
| `syncFullHistory` | boolean | não | Sincroniza o histórico completo do WhatsApp ao conectar. |
| `webhook.enabled` | boolean | não | Ativa o webhook já na criação. |
| `webhook.url` | string | não | URL HTTPS pública que receberá os eventos. Bloqueado: localhost, IPs privados e redes internas (proteção SSRF). |
| `webhook.events` | string[] | não | Lista de eventos para filtrar. Se omitida, todos os eventos são enviados. |
| `webhook.base64` | boolean | não | Se true, mídias nos eventos vêm codificadas em base64. |
| `proxyHost` | string | não | Proxy: host público (Enterprise). |
| `proxyPort` | string | não | Proxy: porta (Enterprise). |
| `proxyUsername` | string | não | Proxy: usuário (Enterprise). |
| `proxyPassword` | string | não | Proxy: senha (Enterprise). |
| `migration` | object | não | Migração de sessão Baileys já autenticada. Restrito ao plano Enterprise. Estrutura: { creds: object, preKeys: array }. Resposta inclui migration: { jid, preKeysImported, connected }. |
| `proxyProtocol` | string | não | http \| https \| socks5 (Enterprise). |


### `GET /instance/connect/:name`
_Conectar Instância_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | não | Número de telefone com DDI para receber pairing code em vez de QR Code (ex: 5511999998888). |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/instance/connect/Marketing01" -H "apikey: $WHATSMIAU_API_KEY"
```

### `GET /instance/connect/:name/image`
_QR Code como PNG_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `name` | string | sim | Nome da instância. |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/instance/connect/Marketing01/image" -H "apikey: $WHATSMIAU_API_KEY"
```

### `GET /instance/connectionState/:name`
_Estado da Conexão_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `name` | string | sim | Nome da instância. |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/instance/connectionState/Marketing01" -H "apikey: $WHATSMIAU_API_KEY"
```

### `PUT /instance/update/:name`
_Atualizar Instância_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `name` | string | sim | Nome da instância (path param). |
| `webhook.enabled` | boolean | não | Ativa/desativa o webhook. |
| `webhook.url` | string | não | URL HTTPS que receberá os eventos. Bloqueado: localhost, IPs privados e redes internas. |
| `webhook.events` | string[] | não | Filtro de eventos (ex: messages.upsert, connection.update). |
| `webhook.base64` | boolean | não | Se true, mídias nos eventos vêm codificadas em base64. |
| `proxyHost` | string | não | Host público do proxy (Enterprise). |
| `proxyPort` | string | não | Porta do proxy (Enterprise). |
| `proxyUsername` | string | não | Usuário do proxy (Enterprise). |
| `proxyPassword` | string | não | Senha do proxy (Enterprise). |


### `DELETE /instance/logout/:name`
_Desconectar (Logout)_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `name` | string | sim | Nome da instância. |


### `DELETE /instance/delete/:name`
_Deletar Instância_

_Sem body/query documentados (path param `:name`/`:instance` implícito)._

```bash
curl -X DELETE "https://api.whatsmiau.dev/v2/instance/delete/Marketing01" -H "apikey: $WHATSMIAU_API_KEY"
```

### `GET /instance/fetchInstances`
_Listar Instâncias_

_Sem body/query documentados (path param `:name`/`:instance` implícito)._

```bash
curl -X GET "https://api.whatsmiau.dev/v2/instance/fetchInstances" -H "apikey: $WHATSMIAU_API_KEY"
```

## Mensagens

### `POST /message/sendText/:instance`
_Enviar Texto_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário com DDI e DDD (ex: 5511999998888). |
| `text` | string | sim | O texto a ser enviado. |
| `delay` | number | não | Atraso em milissegundos antes de enviar (máx: 300000). |
| `linkPreview` | boolean | não | Exibir preview de links. |
| `mentionsEveryOne` | boolean | não | Mencionar todos em grupos. |
| `mentioned` | string[] | não | Lista de JIDs a mencionar. |
| `quoted` | object | não | Mensagem a ser respondida (key.id obrigatório). |


### `POST /message/sendMedia/:instance`
_Enviar Mídia_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário. |
| `media` | string | sim | URL pública do arquivo. |
| `caption` | string | não | Legenda da mídia. |
| `fileName` | string | não | Nome do arquivo (para documentos). |
| `mimetype` | string | não | MIME type do arquivo. |
| `delay` | number | não | Atraso em milissegundos (máx: 300000). |
| `quoted` | object | não | Mensagem a ser respondida (key.id obrigatório). |
| `mentionsEveryOne` | boolean | não | Mencionar todos em grupos. |
| `mentioned` | string[] | não | Lista de JIDs a mencionar. |
| `mediatype` | string | sim | Tipo: image \| video \| document (obrigatório na prática; presente nos exemplos oficiais). |


### `POST /message/sendWhatsAppAudio/:instance`
_Enviar Áudio (PTT)_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário. |
| `audio` | string | sim | URL pública do arquivo MP3/OGG. |
| `delay` | number | não | Atraso em milissegundos (máx: 300000). |
| `encoding` | boolean | não | Re-encodar o áudio antes de enviar. |
| `quoted` | object | não | Mensagem a ser respondida (key.id obrigatório). |
| `mentionsEveryOne` | boolean | não | Mencionar todos em grupos. |
| `mentioned` | string[] | não | Lista de JIDs a mencionar. |


### `POST /message/sendList/:instance`
_Enviar Lista_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário (ex: 5511999998888). |
| `title` | string | não | Título da mensagem. |
| `description` | string | sim | Descrição/corpo da mensagem. |
| `buttonText` | string | não | Texto do botão que abre a lista. |
| `footerText` | string | não | Texto do rodapé. |
| `sections` | array | sim | Seções da lista, cada uma com title e rows[]. |
| `sections[].title` | string | não | Título da seção. |
| `sections[].rows[].title` | string | sim | Título da opção. |
| `sections[].rows[].description` | string | não | Descrição da opção. |
| `sections[].rows[].rowId` | string | sim | ID único da opção (retornado no webhook). |


### `POST /message/sendButtons/:instance`
_Enviar Botões_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário (ex: 5511999998888). |
| `title` | string | não | Título da mensagem. |
| `description` | string | sim | Corpo da mensagem. |
| `footer` | string | não | Texto do rodapé. |
| `buttons` | array | sim | Lista de botões (máximo 3). |
| `buttons[].displayText` | string | sim | Texto exibido no botão. |


### `POST /message/sendSticker/:instance`
_Enviar Figurinha_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário (ex: 5511999998888). |
| `sticker` | string | sim | URL pública do arquivo WebP. |
| `delay` | number | não | Atraso em milissegundos antes de enviar (máx: 300000). |
| `notConvertSticker` | boolean | não | Se true, não tenta converter o arquivo antes de enviar. |
| `quoted` | object | não | Mensagem a ser respondida (key.id obrigatório). |
| `mentionsEveryOne` | boolean | não | Mencionar todos em grupos. |
| `mentioned` | string[] | não | Lista de JIDs a mencionar. |


### `POST /message/sendLocation/:instance`
_Enviar Localização_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário (ex: 5511999998888). |
| `latitude` | number | sim | Latitude em graus decimais (ex: -23.55052). |
| `longitude` | number | sim | Longitude em graus decimais (ex: -46.633308). |
| `address` | string | não | Endereço textual complementar. |
| `delay` | number | não | Atraso em milissegundos (máx: 300000). |
| `quoted` | object | não | Mensagem a ser respondida (key.id obrigatório). |


### `POST /message/sendContact/:instance`
_Enviar Contato_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário (ex: 5511999998888). |
| `contact` | array | sim | Lista de contatos a enviar. |
| `contact[].fullName` | string | sim | Nome completo do contato. |
| `contact[].phoneNumber` | string | sim | Número de telefone do contato. |
| `contact[].wuid` | string | não | WhatsApp UID do contato (se souber). |
| `contact[].organization` | string | não | Organização/empresa. |
| `contact[].email` | string | não | E-mail do contato. |
| `contact[].url` | string | não | Website do contato. |
| `delay` | number | não | Atraso em milissegundos (máx: 300000). |
| `quoted` | object | não | Mensagem a ser respondida (key.id obrigatório). |


### `POST /message/sendPoll/:instance`
_Enviar Enquete_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário (ex: 5511999998888). |
| `name` | string | sim | Pergunta da enquete. |
| `values` | string[] | sim | Opções de resposta (mínimo 2, máximo 12). |
| `selectableCount` | number | não | Quantas opções o usuário pode escolher. 0 = apenas 1 voto (padrão). Use 1..N para múltipla escolha. |
| `delay` | number | não | Atraso em milissegundos (máx: 300000). |
| `quoted` | object | não | Mensagem a ser respondida (key.id obrigatório). |


### `POST /message/sendPtv/:instance`
_Enviar Vídeo Redondo (PTV)_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do destinatário (ex: 5511999998888). |
| `video` | string | sim | URL pública do arquivo MP4. |
| `delay` | number | não | Atraso em milissegundos (máx: 300000). |
| `quoted` | object | não | Mensagem a ser respondida (key.id obrigatório). |
| `mentionsEveryOne` | boolean | não | Mencionar todos em grupos. |
| `mentioned` | string[] | não | Lista de JIDs a mencionar. |


### `POST /message/sendStatus/:instance`
_Enviar Status_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `content` | string | sim | Texto do status OU URL pública do arquivo de mídia. |
| `caption` | string | não | Legenda (apenas para imagem/vídeo). |
| `font` | number | não | Índice da fonte para texto (0-5). |
| `allContacts` | boolean | não | Se true, envia para todos os contatos. |
| `statusJidList` | string[] | não | Lista de JIDs específicos que vão ver o status (ignorado se allContacts=true). |


### `POST /message/sendReaction/:instance`
_Enviar Reação_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `remoteJid` | string | sim | JID do chat (ex: 5511...@s.whatsapp.net). |
| `id` | string | sim | ID da mensagem alvo. |
| `fromMe` | boolean | sim | Se a mensagem foi enviada por você. |


## Chat & Presença

### `POST /chat/sendPresence/:instance`
_Enviar Presença_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `number` | string | sim | Número do chat alvo (ex: 5511999998888). |
| `delay` | number | não | Duração em milissegundos (máx: 300000). |


### `POST /chat/markMessageAsRead/:instance`
_Marcar como Lido_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `remoteJid` | string | sim | JID do chat (ex: 5511...@s.whatsapp.net). |
| `id` | string | sim | ID da mensagem. |
| `sender` | string | não | JID do remetente (obrigatório em grupos). |


### `POST /chat/whatsappNumbers/:instance`
_Verificar Número_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `numbers` | string[] | sim | Lista de números para verificar. |


### `DELETE /chat/deleteMessageForEveryone/:instance`
_Deletar Mensagem_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `id` | string | sim | ID da mensagem a ser deletada. |
| `remoteJid` | string | sim | JID do chat (ex: 5511999998888@s.whatsapp.net ou grupo@g.us). |
| `fromMe` | boolean | sim | Se a mensagem foi enviada por você (true) ou recebida (false). |
| `participant` | string | não | JID do remetente original. Obrigatório ao deletar mensagem de outro participante em grupos. |


## Webhooks

### `POST /webhook/set/:instance`
_Configurar Webhook_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `webhook.enabled` | boolean | não | Ativa ou desativa o webhook. |
| `webhook.url` | string | não | URL que receberá os eventos via POST. |
| `webhook.events` | string[] | não | Lista de eventos para filtrar (ex: messages.upsert, connection.update). |
| `webhook.headers` | object | não | Headers HTTP customizados enviados junto com cada evento. |
| `webhook.byEvents` | boolean | não | Se true, envia um POST por evento. Se false, agrupa. |
| `webhook.base64` | boolean | não | Se true, codifica o payload em base64. |


### `GET /webhook/find/:instance`
_Consultar Webhook_

_Sem body/query documentados (path param `:name`/`:instance` implícito)._

```bash
curl -X GET "https://api.whatsmiau.dev/v2/webhook/find/Marketing01" -H "apikey: $WHATSMIAU_API_KEY"
```

## Grupos

### `POST /group/create/:instance`
_Criar Grupo_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `subject` | string | sim | Nome do grupo (1 a 25 caracteres). |
| `description` | string | não | Descrição/tópico inicial do grupo. |
| `participants` | string[] | não | Lista de números a adicionar (com DDI, sem caracteres especiais). |
| `promoteParticipants` | boolean | não | Promover todos os participantes adicionados a admin. |


### `POST /group/updateGroupSubject/:instance`
_Atualizar Nome do Grupo_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string | sim | JID do grupo (ex: 120363xxxxxxx@g.us). |
| `subject` | string | sim | Novo nome do grupo (1 a 25 caracteres). |


### `POST /group/updateGroupPicture/:instance`
_Atualizar Foto do Grupo_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string | sim | JID do grupo (ex: 120363xxxxxxx@g.us). |
| `image` | string | sim | URL pública de uma imagem JPEG ou imagem em base64 (data URI ou puro base64). |


### `POST /group/updateGroupDescription/:instance`
_Atualizar Descrição do Grupo_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string | sim | JID do grupo. |
| `description` | string | sim | Nova descrição (string vazia remove). |


### `GET /group/findGroupInfos/:instance?groupJid={jid}`
_Buscar Informações do Grupo_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string (query) | sim | JID do grupo. |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/group/findGroupInfos/Marketing01?groupJid=120363xxxxxxx@g.us" -H "apikey: $WHATSMIAU_API_KEY"
```

### `GET /group/fetchAllGroups/:instance?getParticipants={bool}`
_Listar Todos os Grupos_

_Sem body/query documentados (path param `:name`/`:instance` implícito)._

```bash
curl -X GET "https://api.whatsmiau.dev/v2/group/fetchAllGroups/Marketing01?getParticipants=false" -H "apikey: $WHATSMIAU_API_KEY"
```

### `GET /group/participants/:instance?groupJid={jid}`
_Listar Participantes do Grupo_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string (query) | sim | JID do grupo. |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/group/participants/Marketing01?groupJid=120363xxxxxxx@g.us" -H "apikey: $WHATSMIAU_API_KEY"
```

### `GET /group/inviteCode/:instance?groupJid={jid}`
_Obter Link de Convite_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string (query) | sim | JID do grupo. |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/group/inviteCode/Marketing01?groupJid=120363xxxxxxx@g.us" -H "apikey: $WHATSMIAU_API_KEY"
```

### `GET /group/inviteInfo/:instance?inviteCode={code}`
_Informações de um Convite_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `inviteCode` | string (query) | sim | Código de convite (a parte após /chat.whatsapp.com/). |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/group/inviteInfo/Marketing01?inviteCode=INVITECODE" -H "apikey: $WHATSMIAU_API_KEY"
```

### `GET /group/acceptInviteCode/:instance?inviteCode={code}`
_Aceitar Convite_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `inviteCode` | string (query) | sim | Código de convite do grupo. |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/group/acceptInviteCode/Marketing01?inviteCode=INVITECODE" -H "apikey: $WHATSMIAU_API_KEY"
```

### `POST /group/sendInvite/:instance`
_Enviar Convite via DM_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string | sim | JID do grupo. |
| `description` | string | não | Texto opcional enviado junto com o link. |
| `numbers` | string[] | sim | Lista de números (com DDI) que receberão o convite. |


### `POST /group/revokeInviteCode/:instance`
_Revogar Link de Convite_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string | sim | JID do grupo. |


### `POST /group/updateParticipant/:instance`
_Gerenciar Participantes_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string | sim | JID do grupo. |
| `participants` | string[] | sim | Lista de JIDs ou números (com DDI) afetados pela operação. |
| `action` | string | sim | add \| remove \| promote \| demote |


### `POST /group/updateSetting/:instance`
_Configurações do Grupo_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string | sim | JID do grupo. |
| `action` | string | sim | announcement \| not_announcement \| locked \| unlocked |


### `POST /group/toggleEphemeral/:instance`
_Mensagens Efêmeras_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string | sim | JID do grupo. |
| `expiration` | number | não | Duração em segundos. Apenas um destes valores é aceito: 0 (desativado), 86400 (24h), 604800 (7 dias), 7776000 (90 dias). Omitir equivale a 0. |


### `DELETE /group/leaveGroup/:instance?groupJid={jid}`
_Sair do Grupo_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `groupJid` | string (query) | sim | JID do grupo do qual sair. |


## Comunidades

### `POST /community/create/:instance`
_Criar Comunidade_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `subject` | string | sim | Nome da comunidade (1 a 25 caracteres). |
| `description` | string | não | Descrição da comunidade. |


### `POST /community/createSubGroup/:instance`
_Criar Sub-grupo na Comunidade_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `subject` | string | sim | Nome do sub-grupo (1 a 25 caracteres). |
| `parentJid` | string | sim | JID da comunidade pai. |
| `participants` | string[] | não | Números a adicionar ao novo sub-grupo. |


### `POST /community/linkGroup/:instance`
_Vincular Grupo Existente_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `parentJid` | string | sim | JID da comunidade. |
| `childJid` | string | sim | JID do grupo a vincular. |


### `POST /community/unlinkGroup/:instance`
_Desvincular Grupo_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `parentJid` | string | sim | JID da comunidade. |
| `childJid` | string | sim | JID do sub-grupo a desvincular. |


### `GET /community/subGroups/:instance?communityJid={jid}`
_Listar Sub-grupos_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `communityJid` | string (query) | sim | JID da comunidade pai. |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/community/subGroups/Marketing01?communityJid=120363xxxxxxx@g.us" -H "apikey: $WHATSMIAU_API_KEY"
```

### `GET /community/linkedGroupsParticipants/:instance?communityJid={jid}`
_Membros dos Grupos Vinculados_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `communityJid` | string (query) | sim | JID da comunidade. |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/community/linkedGroupsParticipants/Marketing01?communityJid=120363xxxxxxx@g.us" -H "apikey: $WHATSMIAU_API_KEY"
```

### `POST /community/setJoinApprovalMode/:instance`
_Aprovação de Entrada_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `communityJid` | string | sim | JID da comunidade. |
| `mode` | boolean | não | true para exigir aprovação de novos membros; false (padrão) para entrada livre via link de convite. |


### `POST /community/setMemberAddMode/:instance`
_Modo de Adição de Membros_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `communityJid` | string | sim | JID da comunidade. |
| `mode` | string | sim | admin_add \| all_member_add |


### `GET /community/requestParticipants/:instance?communityJid={jid}`
_Solicitações Pendentes_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `communityJid` | string (query) | sim | JID da comunidade. |

```bash
curl -X GET "https://api.whatsmiau.dev/v2/community/requestParticipants/Marketing01?communityJid=120363xxxxxxx@g.us" -H "apikey: $WHATSMIAU_API_KEY"
```

### `POST /community/requestParticipants/update/:instance`
_Aprovar ou Rejeitar Solicitações_

| Param | Tipo | Req | Descrição |
|-------|------|-----|-----------|
| `communityJid` | string | sim | JID da comunidade. |
| `participants` | string[] | não | Lista de JIDs a aprovar/rejeitar. Use a resposta de requestParticipants para obter os JIDs pendentes. |
| `action` | string | sim | approve \| reject |

