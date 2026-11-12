---
name: mailcheap-api
description: "Integration with the Mailcheap REST API v1 (NMS) for managing email hosting: accounts, domains, aliases, DKIM, antispam, Sieve filters and autoresponder. Use when working with Mailcheap, an email hosting API, a mail server API, the NMS API or hosted email management. PT-BR: Integração com a API REST v1 (NMS) do Mailcheap para gerenciar email hosting: contas, domínios, aliases, DKIM, antispam, filtros Sieve e autoresponder. Use ao trabalhar com Mailcheap, API de email hosting ou gerenciamento de email hospedado."
disable-model-invocation: true
---

# Mailcheap API (NMS v1)

Documentação oficial: https://www.mailcheap.co/help/hosted-email/api/v1/

## Visão geral

API REST JSON para o **New Mail System (NMS)** do Mailcheap. Substitua `example.domain.tld` pelo hostname do seu mailserver.

| Item | Valor |
|------|-------|
| Base URL | `https://{MAILCHEAP_HOST}/api/v1/` |
| Content-Type | `application/json` (UTF-8) |
| Rate limit | 15–20 req/s por IP (ban temporário se exceder repetidamente) |
| DELETE bem-sucedido | HTTP `204` — corpo vazio (`text/html`) |
| DELETE com body | Vários endpoints enviam JSON no body em `DELETE` (aliases, domains, sieve, etc.) |

## Variáveis de ambiente

```bash
MAILCHEAP_HOST=mail.seudominio.com      # hostname do mailserver (sem /api/v1)
MAILCHEAP_USERNAME=admin                # usuário API
MAILCHEAP_PASSWORD=senha-segura         # senha (não o token)
MAILCHEAP_AUTH_TOKEN=                   # opcional: token pré-obtido
```

## Níveis de permissão

| Nível | Escopo |
|-------|--------|
| `MasterAdmin` | Servidor inteiro — domínios, admins, configurações globais |
| `DomainAdmin` | Domínios atribuídos — mailboxes e aliases do domínio |
| `MailUser` | Conta individual — filtros Sieve, autoresponder, webmail |

Hierarquia: `MasterAdmin` > `DomainAdmin` > `MailUser`

## Autenticação

### 1. Obter token

```http
POST https://{MAILCHEAP_HOST}/api/v1/auth/
Content-Type: application/json

{"username": "admin", "password": "senha", "otp": "123456"}
```

`otp` é opcional (2FA). Resposta:

```json
{
  "auth": {
    "auth_token": "EXAMPLE_AUTH_TOKEN",
    "perm_level": "MasterAdmin",
    "status": "success",
    "valid_from": 1582536047,
    "valid_to": 1582622447
  }
}
```

### 2. Usar token nas requisições

**Basic Auth**: `Authorization: Basic base64(username:auth_token)`

O token expira (~24h). Renovar com `valid_to` (UNIX timestamp em segundos).

### 3. Revogar token

```http
DELETE https://{MAILCHEAP_HOST}/api/v1/auth/
Authorization: Basic ...
```

## Cliente TypeScript (padrão recomendado)

```typescript
type MailcheapAuth = {
  username: string
  authToken: string
  permLevel: string
  validTo: number
}

type MailcheapConfig = {
  host: string
  username: string
  password: string
}

let cachedAuth: MailcheapAuth | null = null

function getBaseUrl(host: string): string {
  return `https://${host.replace(/\/$/, '')}/api/v1`
}

function basicAuthHeader(username: string, token: string): string {
  const encoded = Buffer.from(`${username}:${token}`).toString('base64')
  return `Basic ${encoded}`
}

async function obtainToken(config: MailcheapConfig, otp?: string): Promise<MailcheapAuth> {
  const res = await fetch(`${getBaseUrl(config.host)}/auth/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: config.username, password: config.password, ...(otp && { otp }) }),
  })
  const body = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(`Mailcheap auth ${res.status}: ${JSON.stringify(body)}`)

  const auth = body.auth
  return {
    username: auth.username,
    authToken: auth.auth_token,
    permLevel: auth.perm_level,
    validTo: auth.valid_to,
  }
}

async function getAuth(config: MailcheapConfig): Promise<MailcheapAuth> {
  const now = Math.floor(Date.now() / 1000)
  if (cachedAuth && cachedAuth.validTo > now + 60) return cachedAuth

  if (process.env.MAILCHEAP_AUTH_TOKEN) {
    cachedAuth = {
      username: config.username,
      authToken: process.env.MAILCHEAP_AUTH_TOKEN,
      permLevel: 'unknown',
      validTo: now + 86400,
    }
    return cachedAuth
  }

  cachedAuth = await obtainToken(config)
  return cachedAuth
}

async function mailcheapRequest<T>(
  config: MailcheapConfig,
  method: string,
  path: string,
  body?: unknown,
): Promise<T> {
  const auth = await getAuth(config)
  const url = `${getBaseUrl(config.host)}${path.startsWith('/') ? path : `/${path}`}`

  const hasBody = body !== undefined
  const res = await fetch(url, {
    method,
    headers: {
      Authorization: basicAuthHeader(auth.username, auth.authToken),
      ...(hasBody && { 'Content-Type': 'application/json' }),
    },
    body: hasBody ? JSON.stringify(body) : undefined,
  })

  if (res.status === 204) return undefined as T

  const responseBody = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(`Mailcheap ${method} ${path} → ${res.status}: ${JSON.stringify(responseBody)}`)
  return responseBody as T
}
```

## Regras de senha (contas)

- Mínimo 12 caracteres
- Pelo menos 1 maiúscula e 1 minúscula
- Pelo menos 1 dígito
- Aceita hash `{SHA512-CRYPT}$6$...` no lugar de plain-text

## Operações comuns

### Criar domínio

```typescript
const result = await mailcheapRequest(config, 'POST', '/domains/', { domain: 'cliente.com.br' })
// status: pending_verification — configurar DNS TXT com verification_code
```

### Criar mailbox (MailUser)

```typescript
await mailcheapRequest(config, 'POST', '/accounts/', {
  username: 'contato@cliente.com.br',
  password: 'SenhaSegura123',
  perm_level: 'MailUser',
  api_access: 0,
  enabled: 1,
  recovery_email: 'admin@empresa.com',
  language: 'pt',
  domain: 'cliente.com.br',
  storagequota_total: 500, // MiB
})
```

### Criar alias

```typescript
await mailcheapRequest(config, 'POST', '/aliases/', {
  alias: 'vendas@cliente.com.br',
  recipients: 'contato@cliente.com.br, gerente@cliente.com.br',
})
```

### Habilitar DKIM

```typescript
// A doc oficial pede body placeholder (Python: {None: None}); {} costuma bastar
await mailcheapRequest(config, 'POST', `/domains/dkim/cliente.com.br/`, {})
// Publicar registro DNS retornado após key generation
```

### Listar contas (paginado)

```typescript
const data = await mailcheapRequest<{ accounts: unknown[] }>(
  config,
  'GET',
  '/accounts/?limit=50&start=0&perm_level=MailUser',
)
```

## Verificação de domínio

Ao criar domínio ou domain alias, a API retorna:

| Campo | Descrição |
|-------|-----------|
| `status` | `pending_verification` até DNS confirmado |
| `verification_type` | Geralmente `DNS TXT` |
| `verification_code` | Valor do registro TXT |
| `expire_time` | Prazo UNIX (segundos) |

## Tratamento de erros

| Status | Significado |
|--------|-------------|
| `204` | Sucesso sem corpo (DELETE comum) |
| `401` | Token inválido/expirado — renovar via POST `/auth/` |
| `403` | Permissão insuficiente para o endpoint |
| `429` | Rate limit — backoff exponencial |
| `5xx` | Erro servidor — retry com jitter |

## Checklist de implementação

```
- [ ] MAILCHEAP_HOST aponta para o mailserver correto
- [ ] Conta API tem api_access=1 e perm_level adequado
- [ ] Token cacheado com margem de 60s antes de valid_to
- [ ] Senhas respeitam requisitos mínimos
- [ ] Domínio verificado via DNS antes de criar mailboxes
- [ ] DKIM habilitado e DNS publicado
- [ ] Rate limit respeitado (< 15 req/s)
```

## Armadilhas comuns

- **Catch-all alias** (`@domain.tld`): desencorajado — aceita spam para endereços inexistentes
- **Username MailUser**: deve ser email completo (`user@domain.tld`)
- **Quota**: `storagequota_total` em **MiB**, não bytes
- **Trailing slash**: URLs da API terminam com `/` — manter consistência
- **2FA ativo**: incluir `otp` no POST `/auth/`
- **DELETE com JSON**: `aliases`, `domains`, `sender_addresses`, `sieve_filters`, `contacts`, `calendars` e outros usam identificador no body, não na URL
- **Sieve update/delete**: `PUT`/`DELETE` em `/sieve_filters/` com `filter_position` no body
- **Sender addresses**: path é `/sender_addresses/` (com underscore), não `/senderaddresses/`
- **Antispam**: thresholds em `/antispam/thresholds/global/` e `/antispam/thresholds/domain/{domain}/`; wlbl em `/antispam/wlbl/...`
- **Automigration user**: `POST /automigration/users/` não exige autenticação
- **WebAuthn**: paths em `/webauthn/...`, não `/auth/passwordless/...`
- **Cascade DomainAdmin**: `PATCH /accounts/cascade/domainadmin/{user}/enable|disable/` — não confundir com PATCH simples em `/accounts/`

## Referência completa

Endpoints validados contra a [documentação oficial](https://www.mailcheap.co/help/hosted-email/api/v1/). Ver [reference.md](reference.md).
