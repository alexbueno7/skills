---
name: audaks-cloud
description: "Operates the Audaks Cloud REST API (api.audaks.com.br), a Brazilian cloud provider: VMs (create, start/stop/reset, change plan), block storage, snapshots and backups, networks, IPs, security groups, load balancers, DNS, monitoring, billing, projects and tickets. Use when the user mentions Audaks, audaks.com.br, a server or VM on Audaks, or asks to list or manage Audaks cloud infrastructure. PT-BR: Opera a API REST da Audaks Cloud: VMs, block storage, snapshots/backups, redes, IPs, security groups, load balancers, DNS, monitoramento, billing, projetos e tickets. Use quando citarem Audaks, servidor/VM na Audaks, ou pedirem para listar/gerenciar infra cloud da Audaks."
disable-model-invocation: true
---

# Audaks Cloud API

Docs: https://api.audaks.com.br/api/docs/alto (compute) · https://api.audaks.com.br/api/docs/ceph (object storage)
Painel Laravel/OpenStack. Token Sanctum, `Authorization: Bearer <token>`. Base `https://api.audaks.com.br/api`.

## Env

```bash
AUDAKS_API_TOKEN=...                               # obrigatório
AUDAKS_API_URL=https://api.audaks.com.br/api        # opcional
```

Token: painel → Profile → API → Enable API (`POST /profile/api/enable`, `token_name`, `expires_at` vazio = sem expiração). Nunca imprimir o token nem gravar em arquivos do projeto.

## Uso

```bash
../audaks-cloud/audaks.sh GET /virtual-machines
../audaks-cloud/audaks.sh GET "/virtual-machines?include=plan,template"
../audaks-cloud/audaks.sh GET /virtual-machines/{VM_SLUG}
../audaks-cloud/audaks.sh POST /virtual-machines/{VM_SLUG}/stop
../audaks-cloud/audaks.sh GET /monitoring/{VM_SLUG}/disk-io-read-write
../audaks-cloud/audaks.sh GET /account/balance
```

Script faz `curl`, pretty-print JSON, sai com 1 e `HTTP <code>` em stderr se ≥400. Sem token: erro explícito.

## Convenções da API

- Resposta: `{ "data": ..., "message": "Ok", "status": "Success", "timezone": "..." }`.
- Identificadores são slugs (`vm-xxxx`, `sg-xxxx`, `bs-xxxx`), não IDs numéricos.
- `GET /virtual-machines` lista resumida (sem IP/plano); `?include=` retorna HTTP 500 — não usar. Para plano, storage e IPs use `GET /virtual-machines/{slug}`: `offering.plan.attribute` (cpu/memory), `storage_setting.name` (ex. `Ultra NVMe`), `compute_category.name`, `ipaddresses[].ipaddress`.
- `GET /profile` retorna `data` sem `name/email` no topo; ignorar para identificação.
- Create/update: `application/json`. Login/profile/api enable: `multipart/form-data` (usar `-F`, não o wrapper).
- Ações de VM: `POST .../start|stop|reset`. Resize: `POST .../change-plan`. Rede: `attach-network`/`detach-network`, `attach-public-network`.
- Security groups: regras em `meta.securityGroupRules[]` de `GET /security-groups` (campos `direction`, `ethertype`, `protocol`, `portRangeMin/Max`, `remoteIpPrefix`, `id`). Remover regra: `POST /security-groups/{slug}/delete-rule/{RULE_ID}` body `{"provider":"alto"}` (DELETE retorna 500). Adicionar (testado): `POST .../add-rule` body `{"provider":"alto","cloud_provider":"alto","region":"br-1","project":"<project-slug do SG>","rules":[...regras existentes de meta.securityGroupRules..., {"direction":"ingress","protocol":"TCP","ethertype":"IPv4","remote":"cidr","cidr":"0.0.0.0/0","network_id":"","port_range":"3000","port_range_type":"PORT","portRangeMin":3000,"portRangeMax":3000,"description":"..."}]}` — enviar lista completa; sem `portRangeMin/Max` a regra vira **todas as portas TCP** (`port_range` sozinho é ignorado). Sem `cloud_provider/region/project` retorna 422.
- Billing cycle `hourly|monthly`; `storage_category` `ssd-storage`; `cloud_provider` `alto`; `server` `cloud-compute`.

## Segurança

- Ações destrutivas (`DELETE /virtual-machines/{slug}`, `DELETE /blockstorages/...`, `restore` de backup, `detach`, `reset`) exigem confirmação explícita do usuário com o slug alvo.
- Billing/cancel-requests: só leitura sem pedido explícito.

## Referência completa

`reference.md` — todos os endpoints (155 alto + exclusivos ceph) com params e exemplo de body. Grep por path ou tag antes de chamar.
