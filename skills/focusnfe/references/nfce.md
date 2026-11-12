# NFCe — nuvem `/nfce` e Comunicador Offline

Doc: [NFCe](https://doc.focusnfe.com.br/reference/nfce). **Todos os processos da API cloud são síncronos.** Não existe `202` na emissão NFCe.

Webhook cloud: não há `event=nfce` no OpenAPI de hooks. Eventos ligados: `nfce_contingencia`, `nfce_consulta_automatica`. Reenvio pontual **não** aparece no OpenAPI de `/nfce` (diferente de NFe).

DANFCe (`caminho_danfe`) é **HTML**, não PDF.

Empresa precisa `habilita_nfce` + **CSC** (token QR Code). Sem CSC: 422 `erro_validacao` “Código CSC não configurado”.

## Cloud — métodos

| Método | Path | HTTP | Body / query |
|---|---|---|---|
| POST | `/nfce` | 201, 400, 401, 403, 415, 422 | Query `ref*` , `completa=0\|1`, `forma_emissao=offline`. JSON `NFCeRequest` |
| GET | `/nfce/{ref}` | 200, 401, 403, 404 | Query `completa` |
| DELETE | `/nfce/{ref}` | 200, 400, 401, 403, 404, 415, 422 | `{ "justificativa": "15..255" }`. Prazo **30 min** |
| POST | `/nfce/{ref}/email` | 200, 400, 401, 403, 404, 415 | `{ "emails": ["a@b.c"] }` máx. 10. Envio em background |
| POST | `/nfce/inutilizacao` | 200, 400, 401, 403, 415, 422 | Síncrono |
| GET | `/nfce/inutilizacoes` | 200, 400, 401 | `cnpj` **ou** `cpf` + datas/faixa |
| POST | `/nfce/{ref}/econf` | 200 … 422 | `{ "detalhes_pagamento": [...] }` |
| GET | `/nfce/{ref}/econf/{protocolo}` | 200, 401, 403, 404 | |
| DELETE | `/nfce/{ref}/econf/{protocolo}` | 200, 401, 403, 404, 422 | Cancelar na ordem dos envios |

## POST `/nfce?ref=` — payload

Obrigatórios: `cnpj_emitente`, `data_emissao` (ISO + timezone; atraso máx. **5 min** → SEFAZ `704`), `presenca_comprador`, `modalidade_frete`, `local_destino`, `natureza_operacao`, `items[]`, `formas_pagamento[]`.

```json
{
  "cnpj_emitente": "12345678000123",
  "data_emissao": "2026-09-17T12:00:00-03:00",
  "natureza_operacao": "VENDA AO CONSUMIDOR",
  "presenca_comprador": "1",
  "modalidade_frete": "9",
  "local_destino": "1",
  "nome_destinatario": "Consumidor",
  "cpf_destinatario": "00000000191",
  "items": [
    {
      "numero_item": "1",
      "codigo_produto": "SKU1",
      "descricao": "Produto",
      "codigo_ncm": "21069090",
      "cfop": "5102",
      "unidade_comercial": "UN",
      "unidade_tributavel": "UN",
      "quantidade_comercial": 1,
      "quantidade_tributavel": 1,
      "valor_unitario_comercial": 10.0,
      "valor_unitario_tributavel": 10.0,
      "valor_bruto": 10.0,
      "icms_origem": "0",
      "icms_situacao_tributaria": "102"
    }
  ],
  "formas_pagamento": [{ "forma_pagamento": "01", "valor_pagamento": 10.0 }]
}
```

| Campo | Valores |
|---|---|
| `presenca_comprador` | `1` presencial, `4` entrega domicílio |
| `modalidade_frete` | `0` emitente, `1` dest, `2` terceiros, `9` sem frete |
| `local_destino` | `1` interna, `2` interestadual, `3` exterior |
| `indicador_inscricao_estadual_destinatario` | `1` ICMS, `2` isento, `9` não contribuinte |
| `forma_pagamento` | `01` dinheiro, `02` cheque, `03` crédito, `04` débito, `05` crédito loja, `10–13` vales, `99` outros |
| `tipo_integracao` (card) | `1` integrado (+ autorização), `2` não integrado |
| `bandeira_operadora` | `01` Visa, `02` Master, `03` Amex, `99` outros |

Destinatário: `cpf_destinatario` **ou** `cnpj_destinatario`. Numeração: omitir `numero`/`serie` deixa a API controlar. Contingência manual: query `forma_emissao=offline` **e** body `numero`, `serie`, `codigo_unico` (tag `cNF`).

Item: `valor_desconto`, `valor_total_tributos` opcionais. Lei da Transparência no Comunicador Offline exige `valor_total_tributos` no item se quiser o cálculo — a API local **não** calcula sozinha.

## POST 201 — emissão

`status` só `autorizado` | `erro_autorizacao` (síncrono: o 201 também carrega rejeição SEFAZ).

**autorizado**

```json
{
  "cnpj_emitente": "12345678000123",
  "ref": "referencia_000899",
  "status": "autorizado",
  "status_sefaz": "100",
  "mensagem_sefaz": "Autorizado o uso da NF-e",
  "chave_nfe": "NFe4119...",
  "numero": "12",
  "serie": "1",
  "caminho_xml_nota_fiscal": "/arquivos/.../nfe.xml",
  "caminho_danfe": "/notas_fiscais_consumidor/NFe....html",
  "qrcode_url": "http://www.fazenda.pr.gov.br/nfce/qrcode/?p=...",
  "url_consulta_nf": "http://www.fazenda.pr.gov.br/nfce/consulta"
}
```

Contingência: + `contingencia_offline: true`, `contingencia_offline_efetivada: false`.

**erro_autorizacao** (ainda HTTP 201 no OpenAPI de emitir):

```json
{
  "cnpj_emitente": "12345678000123",
  "ref": "referencia_000899",
  "status": "erro_autorizacao",
  "status_sefaz": "704",
  "mensagem_sefaz": "Rejeição: NFC-e com Data-Hora de emissão atrasada"
}
```

GET `?completa=1` autorizado: + `protocolo`, `requisicao_nota_fiscal`, `protocolo_nota_fiscal`.

GET oneOf extra: `denegado`; cancelada traz `caminho_xml_cancelamento` e `numero_protocolo`.

## Erros emitir

| HTTP | `codigo` | Quando |
|---|---|---|
| 400 | `requisicao_invalida` | `ref` ausente |
| 400 | `forma_emissao_nao_informada` | `forma_emissao` inválido |
| 422 | `permissao_negada` | CNPJ emitente não autorizado |
| 422 | `pending_operation` | ref ainda processando |
| 422 | `already_processed` | ref já autorizada |
| 422 | `erro_validacao_schema` | campo vazio (ex. `data_emissao`) |
| 422 | `ambiente_nao_configurado` | ambiente NFCe |
| 422 | `empresa_nao_configurada` | empresa sem NFCe |
| 422 | `erro_validacao` | CSC ausente |

## DELETE cancelar — 200

```json
{
  "status": "cancelado",
  "status_sefaz": "135",
  "mensagem_sefaz": "...",
  "caminho_xml_cancelamento": "/arquivos/...",
  "numero_protocolo": "..."
}
```

`status`: `cancelado` | `erro_cancelamento`.

400: justificativa tamanho/ausente. 422: `nfe_nao_autorizada`; `already_processed` “A nota fiscal foi cancelada”.

## Inutilização

```json
{
  "cnpj": "12345678000123",
  "serie": "1",
  "numero_inicial": "7730",
  "numero_final": "7732",
  "justificativa": "15 caracteres min"
}
```

Resposta: `status` `autorizado` | `erro_autorizacao` + `caminho_xml`, `protocolo_sefaz`, faixa, `modelo`.

## ECONF

`detalhes_pagamento[]` obrigatório: `forma_pagamento`, `valor_pagamento`, `data_pagamento`. Opcionais: indicador, descrição, CNPJs transacional/IF/beneficiário, UF, bandeira, autorização.

Resposta registro: `status` `autorizado` | `erro_autorizacao`, `caminho_xml_conciliacao_financeira`, `numero_conciliacao_financeira`, `numero_protocolo`.

Cancelamento: `caminho_xml_cancelamento_conciliacao_financeira`, `numero_cancelamento_conciliacao_financeira`.

## Comunicador Offline (API local)

Não é `api.focusnfe.com.br`. Host do app. Paths OpenAPI já incluem `/v2/fiscal/nfce` — **não** prefixar de novo o `/v2` da nuvem.

`ref` única por emitente. Duplicata = erro “referência já utilizada”. Extensão cancelamento: `.canc`. Justificativa 15–200 no fluxo arquivo; OpenAPI local pede `justificativa` no DELETE.

| Método | Path |
|---|---|
| POST | `/v2/fiscal/nfce?ref=` (+ `tipo_contingencia=offline` e/ou `forma_emissao=offline`) |
| GET | `/v2/fiscal/nfce/{ref}` |
| DELETE | `/v2/fiscal/nfce/{ref}` `{ "justificativa": "..." }` |
| GET | `/v2/fiscal/nfce/{chave}.pdf` espelho |
| GET | `/v2/fiscal/nfce/{chave}.xml` autorizado |
| GET | `/v2/fiscal/nfce/{chave}-canc.xml` cancelado |
| GET | `/v2/fiscal/nfce/pendentes` |
| PUT | `/v2/fiscal/nfce/{ref}/efetivar` contingência → SEFAZ |

Body local exige dados do **emitente** no JSON (`nome_emitente`, endereço, `valor_total`, items, pagamentos) — diferente da nuvem, que puxa cadastro da empresa.

Resposta local: `{ ref, status, mensagem, cpf_cnpj_emitente, chave_nfe, chave_nfe_cancelamento, numero }`.
