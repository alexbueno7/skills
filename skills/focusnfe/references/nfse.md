# NFSe municipal e NFSe nacional (Focus NFe)

## Municipal — `/nfse`

Prefeitura via provedor integrado. Especificidade por cidade: https://focusnfe.com.br/cidades-integradas-nfse/

Reforma tributária: campos novos marcados (RT) no OpenAPI. Município pode ignorar ou rejeitar. Muitos migram para o padrão nacional (`/nfsen`).

JSON de exemplo por IBGE: `GET /municipios/{codigo_ibge}/json`

### Métodos

| Método | Path | HTTP |
|---|---|---|
| POST | `/nfse?ref=` | 201 processando, 400, 401, 422 |
| GET | `/nfse/{ref}` | 200 oneOf, 404 |
| DELETE | `/nfse/{ref}` | 200, 400, 404. Body opcional `{ "justificativa": "15..255" }` |
| POST | `/nfse/{ref}/email` | 200. Envio em background |
| POST | `/nfse/{ref}/hook` | 200 |

Algumas prefeituras **não** cancelam por webservice. Confirmar no guia de municípios.

### POST body — obrigatórios

```json
{
  "data_emissao": "2016-12-25T12:00:00-03:00",
  "natureza_operacao": "1",
  "optante_simples_nacional": true,
  "prestador": {
    "cnpj": "12345678000123",
    "inscricao_municipal": "...",
    "codigo_municipio": "4106902"
  },
  "tomador": {
    "cnpj": "99887766000155",
    "razao_social": "...",
    "endereco": {}
  },
  "servico": {
    "valor_servicos": 1500.0,
    "iss_retido": false,
    "item_lista_servico": "0402",
    "discriminacao": "Serviço prestado",
    "codigo_municipio": "4106902"
  }
}
```

`natureza_operacao`: `1` município, `2` fora, `3` isenção, `4` imune, `5` suspensa judicial, `6` suspensa administrativa.

`regime_especial_tributacao`: `1` ME municipal … `5` MEI … `6` ME/EPP SN. Ignorado em alguns municípios.

`prestador.codigo_municipio`: IBGE 7 dígitos. 400 exemplo: parâmetro `prestador.codigo_municipio` não informado.

OpenAPI lista `tomador.cpf` e `tomador.cnpj` ambos required — tratar como **um dos dois**.

Serviço opcionais frequentes: `aliquota`, `valor_iss`, `codigo_cnae` (7 dígitos), `codigo_tributario_municipio`, retenções PIS/COFINS/INSS/IR/CSLL, campos (RT) IBS/CBS/`codigo_nbs`.

### GET 200

| status | Campos extras |
|---|---|
| `processando_autorizacao` | `cnpj_prestador`, `ref`, `numero_rps`, `serie_rps`, `tipo_rps` |
| `autorizado` | `numero`, `codigo_verificacao`, `data_emissao`, `url` (HTML), `caminho_xml_nota_fiscal`, `url_danfse` (S3) |
| `cancelado` | + `caminho_xml_cancelamento` |
| `erro_autorizacao` | `erros[]` com `codigo`, `mensagem`, `correcao` (ex. `L99` regime especial) |

POST 201 devolve o objeto **processando**, não a nota autorizada.

422 emitir: `erro_validacao` (emitente diferente do primeiro envio), `nfe_autorizada` (ref já autorizada — nome do código é esse mesmo na NFSe).

DELETE 200: `{ "status": "cancelado" }` ou `{ "status": "erro_cancelamento", "erros": [...] }`.

## Nacional — `/nfsen`

ADN. Campos completos: https://campos.focusnfe.com.br/nfse_nacional/EmissaoDPSXml.html

| Método | Path | HTTP |
|---|---|---|
| POST | `/nfsen?ref=` | **202**, 400, 401, 422 |
| GET | `/nfsen/{ref}` | 200 same status family |
| DELETE | `/nfsen/{ref}` | 200, 404 |
| POST | `/nfsen/{ref}/email` | 200 |
| POST | `/nfsen/{ref}/hook` | 200 |

GET autorizado: mesmos campos de URL/XML/DANFSe da municipal. Processando nacional às vezes só `cnpj_prestador`, `ref`, `status` (sem RPS no exemplo).

Webhook event: `nfsen`. Recebidas contra o CNPJ: `/nfsens_recebidas` + event `nfsen_recebida`.
