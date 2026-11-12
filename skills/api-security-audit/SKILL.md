---
name: api-security-audit
description: "Vulnerability analysis and penetration testing for REST APIs following the OWASP API Security Top 10. Use when reviewing endpoint security, auditing authentication or authorization, hunting API vulnerabilities, or when the user mentions BOLA, BFLA, injection, rate limiting, JWT or API security. PT-BR: Análise de vulnerabilidades e testes de penetração em APIs REST seguindo o OWASP API Security Top 10. Use ao revisar segurança de endpoints, auditar autenticação/autorização, buscar vulnerabilidades em APIs, ou quando o usuário citar BOLA, BFLA, injection, rate limiting, JWT ou segurança de API."
---

# API Security Audit

Especialista em Segurança Ofensiva focado em APIs REST. Análise baseada no **OWASP API Security Top 10 2023**.

## Metodologia de Auditoria

### Fase 1: Reconhecimento

1. Mapear todos os endpoints da API
2. Identificar parâmetros de entrada (path, query, body, headers)
3. Analisar esquemas de autenticação (JWT, OAuth, API Key)
4. Documentar roles e níveis de acesso

### Fase 2: Análise de Vulnerabilidades

Testar cada categoria OWASP:

| ID | Categoria | Teste |
|----|-----------|-------|
| API1 | **BOLA** | Manipular IDs para acessar recursos de outros usuários |
| API2 | **Broken Auth** | Validar tokens, expiração, refresh flow |
| API3 | **Object Property** | Verificar mass assignment e campos expostos |
| API4 | **Resource Consumption** | Testar rate limiting e DoS |
| API5 | **BFLA** | Acessar rotas admin com user comum |
| API6 | **SSRF** | URLs em parâmetros que fazem requests |
| API7 | **Security Misconfig** | Headers, CORS, verbose errors |
| API8 | **Injection** | SQLi, NoSQLi, Command Injection |
| API9 | **Asset Management** | Endpoints não documentados, versões antigas |
| API10 | **Server-Side Request** | Validação insuficiente de inputs |

### Fase 3: Relatório

Gerar relatório seguindo o formato em [report-template.md](report-template.md).

## Checklist de Testes

```
Progresso da Auditoria:

[ ] Fase 1 - Reconhecimento
    [ ] Endpoints mapeados
    [ ] Parâmetros identificados
    [ ] Auth scheme documentado

[ ] Fase 2 - OWASP Top 10
    [ ] API1 - BOLA testado
    [ ] API2 - Auth testado
    [ ] API3 - Object Property testado
    [ ] API4 - Rate Limiting testado
    [ ] API5 - BFLA testado
    [ ] API6 - SSRF testado
    [ ] API7 - Misconfig testado
    [ ] API8 - Injection testado
    [ ] API9 - Assets testado
    [ ] API10 - Unsafe API testado

[ ] Fase 3 - Relatório
    [ ] Vulnerabilidades documentadas
    [ ] Severidades classificadas
    [ ] Remediações propostas
    [ ] Backlog priorizado
```

## Testes por Categoria

### API1: BOLA (Broken Object Level Authorization)

**O que testar:**
- Trocar IDs em URLs: `/users/123` → `/users/124`
- Manipular UUIDs em requisições
- Testar referências em relacionamentos

**Payloads:**
```bash
# Testar acesso a recurso de outro usuário
curl -H "Authorization: Bearer $TOKEN_USER_A" \
     "https://api.example.com/users/$USER_B_ID"

# Testar IDOR em nested resources
curl -H "Authorization: Bearer $TOKEN" \
     "https://api.example.com/orgs/$OTHER_ORG/members"
```

**Correção:**
```typescript
// Verificar ownership antes de retornar
const resource = await prisma.resource.findUnique({ where: { id } })
if (resource.ownerId !== request.user.id) {
  return reply.status(403).send({ error: 'forbidden' })
}
```

### API2: Broken Authentication

**O que testar:**
- Tokens expirados ainda funcionando
- JWT sem validação de assinatura
- Refresh token reutilizável após logout
- Brute force em login

**Payloads:**
```bash
# Token expirado
curl -H "Authorization: Bearer $EXPIRED_TOKEN" \
     "https://api.example.com/me"

# JWT com assinatura inválida
curl -H "Authorization: Bearer eyJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ." \
     "https://api.example.com/admin"

# Brute force em login: medir se há bloqueio após tentativas repetidas
python scripts/rate_limit_test.py --url https://api.example.com/login --method POST
```

### API3: Broken Object Property Level Authorization

**O que testar:**
- Mass assignment (enviar campos extras)
- Resposta expõe campos sensíveis

**Payloads:**
```bash
# Mass assignment - tentar virar admin
curl -X PATCH "https://api.example.com/users/me" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"name":"test","role":"ADMIN","isVerified":true}'

# Verificar campos expostos na resposta
curl "https://api.example.com/users/123" | jq 'keys'
```

**Correção:**
```typescript
// Whitelist de campos atualizáveis
const allowedFields = ['name', 'email', 'avatar']
const data = pick(request.body, allowedFields)

// Projeção explícita na resposta
const user = await prisma.user.findUnique({
  where: { id },
  select: { id: true, name: true, email: true } // SEM passwordHash, role
})
```

### API4: Unrestricted Resource Consumption

**O que testar:**
- Rate limiting ausente
- Paginação sem limite máximo
- Upload sem limite de tamanho
- Queries complexas (GraphQL batching)

**Payloads:**
```bash
# Testar rate limiting
for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
       "https://api.example.com/login" \
       -d '{"email":"test@test.com","password":"wrong"}'
done | sort | uniq -c

# Paginação abusiva
curl "https://api.example.com/users?limit=999999"
```

### API5: BFLA (Broken Function Level Authorization)

**O que testar:**
- Acessar rotas `/admin/*` com token de user comum
- Mudar método HTTP (GET → DELETE)
- Acessar endpoints de outras roles

**Payloads:**
```bash
# User comum tentando rota admin
curl -H "Authorization: Bearer $USER_TOKEN" \
     "https://api.example.com/admin/users"

# Tentar deletar como user comum
curl -X DELETE -H "Authorization: Bearer $USER_TOKEN" \
     "https://api.example.com/posts/123"
```

### API8: Injection

**O que testar:**
- SQL Injection em parâmetros
- NoSQL Injection em filtros
- Command Injection em uploads/processamento

**Payloads:**
```bash
# SQL Injection
curl "https://api.example.com/users?search=admin'--"
curl "https://api.example.com/users?id=1 OR 1=1"

# NoSQL Injection (MongoDB)
curl "https://api.example.com/users" \
     -d '{"email":{"$gt":""},"password":{"$gt":""}}'

# UUID Injection (validação fraca)
curl "https://api.example.com/users/*"
curl "https://api.example.com/users/../admin"
```

**Correção:**
```typescript
// Validar UUID antes de usar
import { z } from 'zod'
const uuidSchema = z.string().uuid()

const parseResult = uuidSchema.safeParse(id)
if (!parseResult.success) {
  return reply.status(400).send({ error: 'invalid-uuid' })
}
```

## Severidade

| Nível | Critério | SLA |
|-------|----------|-----|
| 🔴 **Crítica** | RCE, SQLi com dump, bypass auth total | Imediato |
| 🟠 **Alta** | BOLA, BFLA, dados sensíveis expostos | 24h |
| 🟡 **Média** | Rate limiting ausente, mass assignment | 7 dias |
| 🟢 **Baixa** | Headers faltando, verbose errors | 30 dias |

## Scripts de Automação

Execute os scripts em `scripts/` para testes automatizados:

```bash
# Scan de endpoints
python scripts/endpoint_scan.py --base-url https://api.example.com

# Teste de BOLA
python scripts/bola_test.py --url https://api.example.com/users/{id}

# Rate limiting
python scripts/rate_limit_test.py --url https://api.example.com/login --method POST
```

## Recursos Adicionais

- Template de relatório: [report-template.md](report-template.md)
- OWASP API Top 10: https://owasp.org/API-Security/
