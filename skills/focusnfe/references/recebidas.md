# Documentos recebidos (Focus NFe)

Distribuição de documentos emitidos **contra** o CNPJ. Campo `versao` é monotônico por CNPJ: guardar o máximo local e pedir só `versao` maior.

Toda lista: **100** registros. Headers:

- `X-Total-Count` — total da busca
- `X-Max-Version` — usar na próxima query `versao`

## NFe recebidas — `/nfes_recebidas`

Receita manda **resumo** primeiro. XML completo depois da manifestação.

| Método | Path | HTTP |
|---|---|---|
| GET | `/nfes_recebidas?cnpj=&versao=&pendente=&pendente_ciencia=` | 200, 400, 401, 403 |
| GET | `/nfes_recebidas/{chave}` | 200. Query `cnpj`, `completa` |
| GET | `/nfes_recebidas/{chave}.json` | JSON completo |
| GET | `/nfes_recebidas/{chave}.xml` | XML |
| GET | `/nfes_recebidas/{chave}.pdf` | **302** + `Location` pré-assinada. Sem Basic no GET do arquivo |
| GET | `/nfes_recebidas/{chave}/cancelamento.xml` | |
| GET | `/nfes_recebidas/{chave}/carta_correcao.xml` | última CCe |
| POST | `/nfes_recebidas/{chave}/manifesto` | síncrono |
| POST | `/nfes_recebidas/{chave}/evento` | |
| DELETE | `/nfes_recebidas/{chave}/evento` | |
| POST | `/nfes_recebidas/{chave}/hook` | |

`pendente=1`: sem manifesto final. `pendente_ciencia=1`: sem ciência.

### Manifestar

```json
{ "tipo": "ciencia" }
```

`tipo`: `ciencia` | `confirmacao` | `desconhecimento` | `nao_realizada`

`nao_realizada` exige `justificativa` 15–255.

Resposta:

```json
{
  "status": "aceita",
  "status_sefaz": "135",
  "mensagem_sefaz": "Evento registrado e vinculado a NF-e",
  "protocolo": "...",
  "data_manifesto": "2024-01-15T10:10:00-03:00"
}
```

Webhook: `nfe_recebida` (e `nfe_recebida_falha_consulta`).

## CTe recebidas — `/ctes_recebidas`

XML completo já na distribuição. Mesmo esquema `versao` / 100 itens / headers.

GET `{chave}`, `.json`, `.xml`, `.pdf` (DACTe, redirect), `cancelamento.xml`, `carta_correcao.xml`.

Desacordo: `POST /ctes_recebidas/{chave}/desacordo` síncrono. CPF tomador **não** registra desacordo via WS (NT 2022.001) — só gov.br.

Webhook: `cte_recebida`.

## NFSe nacional recebidas — `/nfsens_recebidas`

XML completo. Lista `cnpj` + `versao` + `completa`. Item: `.json`, `.xml`, `.pdf` (redirect), `.html` (DANFSe nacional).

Webhook: `nfsen_recebida`.
