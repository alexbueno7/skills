# Empresas, webhooks, backups, APIs acessórias

## Empresas — `/empresas`

SaaS multi-CNPJ. `dry_run=1` simula POST/PUT sem gravar.

| Método | Path | HTTP |
|---|---|---|
| POST | `/empresas?dry_run=` | 200, 400, 401, 422 |
| GET | `/empresas?cnpj=&cpf=&offset=` | 200. Até 50 por página |
| GET | `/empresas/{id}` | 200, 401, 404, 422 |
| PUT | `/empresas/{id}?dry_run=` | 200 |
| DELETE | `/empresas/{id}` | 200 irreversível |

Campos frequentes do create: `nome`, `nome_fantasia`, `cnpj` ou `cpf`, `inscricao_estadual`, `inscricao_municipal`, `regime_tributario`, endereço (`logradouro`, `numero`, `bairro`, `municipio`, `cep`, `uf`), `email`, `telefone`, flags `habilita_nfe`, `habilita_nfce`, `habilita_nfse`, `habilita_nfsen_producao`, `habilita_cte`, `habilita_mdfe`, `habilita_manifestacao`, etc.

Certificado digital: painel / fluxo da empresa (não está neste recorte de `/empresas` OpenAPI). Sem certificado habilitado a SEFAZ rejeita emissão.

## Webhooks — `/hooks`

POST JSON para a `url` a cada mudança. Um documento por chamada.

Retry se a URL falhar ou HTTP ∉ 2xx: 1 min, 30 min, 1 h, 3 h, 24 h. Depois **para**.

```json
{ "cnpj": "12345678000123", "event": "nfe", "url": "https://seu.sistema/hooks/nfe" }
```

Obrigatórios: `event`, `url`. Opcional: `cpf`, `authorization`, `authorization_header`.

`event`: `nfe`, `nfse`, `nfsen`, `nfce_contingencia`, `nfce_consulta_automatica`, `nfe_recebida`, `nfe_recebida_falha_consulta`, `nfsen_recebida`, `cte_recebida`, `inutilizacao`, `cte`, `mdfe`, `nfcom`, `dce`.

Não existe `event=nfce` para autorização online. Contingência/consulta automática usam os dois eventos `nfce_*`. Detalhe de emissão: [nfce.md](nfce.md).

CRUD: POST `/hooks`, GET `/hooks`, GET `/hooks/{id}`, DELETE `/hooks/{id}`.

Reenvio pontual: `POST /{recurso}/{ref}/hook`.

## Backups — `/backups/{cnpj}.json`

GET lista ZIPs mensais (DANFE NFe + XML NFe/NFCe/CTe/MDFe). HTTP 200, 401, 403. **Não** inclui NFSe.

## Emails bloqueados

GET/DELETE `/blocked_emails/{email}`. Spam/reclamação pode ser indeletável (422).

## Acessórias (beta onde a doc marca)

Todas paginam ~50 + `offset` + `X-Total-Count`, salvo item único.

| Recurso | Paths |
|---|---|
| CEP | `GET /ceps`, `GET /ceps/{cep}` |
| CFOP | `GET /cfops`, `GET /cfops/{codigo}` |
| CNAE | `GET /codigos_cnae`, `GET /codigos_cnae/{codigo}` |
| CNPJ | `GET /cnpjs/{cnpj}` — 14 dígitos, só números |
| NCM | `GET /ncms`, `GET /ncms/{codigo}` |
| Municípios | `GET /municipios`, `GET /municipios/{ibge}` |
| Lista serviço | `GET /municipios/{ibge}/itens_lista_servico` |
| Código trib. municipal | `GET /municipios/{ibge}/codigos_tributarios_municipio` |
| JSON exemplo NFSe | `GET /municipios/{ibge}/json` |

CEP: no mínimo 2 filtros, exceto município de CEP único (`codigo_ibge` só).

## Comunicador Offline

API **local** do aplicativo Focus, arquivos `.nfce` / `.canc`. Não misturar com `api.focusnfe.com.br`. Paths OpenAPI `/v2/fiscal/nfce` — host do comunicador, não a nuvem. Contratos: [nfce.md](nfce.md).
