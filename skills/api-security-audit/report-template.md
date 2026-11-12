# Template de Relatório de Segurança

## 🚨 Relatório de Vulnerabilidades Encontradas

| # | Endpoint | Ataque Simulado | Severidade | Impacto |
|---|----------|-----------------|------------|---------|
| 1 | `GET /api/users/{id}` | BOLA - Manipulação de ID | 🔴 Crítica | Acesso a dados de outros usuários |
| 2 | `POST /api/login` | Brute Force | 🟠 Alta | Takeover de contas |
| 3 | `PATCH /api/users/me` | Mass Assignment | 🟡 Média | Escalação de privilégios |

---

## 📋 Detalhamento das Vulnerabilidades

### V001: [Nome da Vulnerabilidade]

**Categoria OWASP:** API1 - Broken Object Level Authorization  
**Severidade:** 🔴 Crítica  
**CVSS:** 9.1 (Critical)

**Descrição:**
[Explicação técnica do problema]

**Prova de Conceito:**
```bash
curl -H "Authorization: Bearer $TOKEN_USER_A" \
     "https://api.example.com/users/$USER_B_ID"
```

**Resposta:**
```json
{
  "id": "user-b-id",
  "email": "userb@example.com",
  "passwordHash": "...",  // ← Dados sensíveis expostos
  "role": "ADMIN"
}
```

**Impacto:**
- Vazamento de dados pessoais (LGPD)
- Exposição de credenciais
- Possível takeover de contas

---

## 🛠️ Plano de Ação e Correções

### V001: BOLA em /api/users/{id}

**Problema:** Endpoint não verifica ownership do recurso.

**Correção:**
```typescript
app.get('/api/users/:id', async (request, reply) => {
  const { id } = request.params as { id: string }
  
  // 1. Validar formato do ID
  const parseResult = uuidSchema.safeParse(id)
  if (!parseResult.success) {
    return reply.status(400).send({ error: 'invalid-uuid' })
  }
  
  // 2. Buscar recurso
  const user = await prisma.user.findUnique({ 
    where: { id },
    select: { id: true, name: true, email: true } // Projeção explícita
  })
  
  if (!user) {
    return reply.status(404).send({ error: 'not-found' })
  }
  
  // 3. Verificar ownership (se não for admin)
  if (request.user.role !== 'ADMIN' && user.id !== request.user.id) {
    return reply.status(403).send({ error: 'forbidden' })
  }
  
  return { user }
})
```

**Arquivos afetados:**
- `api/src/routes/users.routes.ts`
- `api/src/middlewares/authorization.ts`

---

## ✅ Backlog de Correção Priorizado

### P0 - IMEDIATO (deploy hoje)
- [ ] **V001** - Implementar verificação de ownership em `/api/users/{id}`
- [ ] **V002** - Adicionar validação de UUID em todas as rotas com `:id`

### P1 - ALTA (próximas 24h)
- [ ] **V003** - Configurar rate limiting global (100 req/min por IP)
- [ ] **V004** - Remover campos sensíveis das respostas (passwordHash, tokens)

### P2 - MÉDIA (próxima sprint)
- [ ] **V005** - Implementar projeção explícita em todos os endpoints
- [ ] **V006** - Adicionar logging de tentativas de acesso não autorizado

### P3 - BAIXA (backlog)
- [ ] **V007** - Adicionar headers de segurança (X-Content-Type-Options, etc)
- [ ] **V008** - Configurar CORS mais restritivo

---

## 📊 Resumo Executivo

| Severidade | Quantidade | Status |
|------------|------------|--------|
| 🔴 Crítica | 2 | ⏳ Pendente |
| 🟠 Alta | 3 | ⏳ Pendente |
| 🟡 Média | 4 | ⏳ Pendente |
| 🟢 Baixa | 2 | ⏳ Pendente |

**Risco Geral:** 🔴 ALTO  
**Recomendação:** Bloquear deploy até correção das vulnerabilidades P0.

---

## 🔍 Metodologia

- **Framework:** OWASP API Security Top 10 2023
- **Ferramentas:** curl, Burp Suite, scripts customizados
- **Período:** [DATA]
- **Auditor:** [NOME]
