---
name: focusnfe
description: "Integrates the Focus NFe v2 REST API for Brazilian electronic tax documents (NFe, NFCe, municipal and national NFSe, CTe, MDFe, received documents, companies, webhooks, Offline Communicator). Use when issuing, querying or cancelling invoices, handling DANFCe, QR Code, CSC, offline contingency, NFCe number invalidation or ECONF, or when the user mentions Focus NFe, NFCe or doc.focusnfe.com.br. Brazil only. PT-BR: Integra a API REST Focus NFe v2 (NFe, NFCe/NFC-e, NFSe municipal e nacional, CTe, MDFe, documentos recebidos, empresas, webhooks, Comunicador Offline). Use ao emitir, consultar ou cancelar notas, DANFCe, QR Code, CSC, contingência offline, inutilização NFCe, ECONF, ou quando citarem Focus NFe, FocusNFe, NFC-e."
---

# Focus NFe API v2

Fonte canônica: [documentação](https://doc.focusnfe.com.br/reference/introducao). Índice: [llms.txt](https://doc.focusnfe.com.br/llms.txt). Páginas `.md` trazem OpenAPI 3.0.3.

Antes de inventar path, método ou campo: ler [catalog.md](references/catalog.md). Payloads: [nfe.md](references/nfe.md), [nfce.md](references/nfce.md), [nfse.md](references/nfse.md), [recebidas.md](references/recebidas.md), [gestao.md](references/gestao.md). Campos XML NFe 4.00: https://campos.focusnfe.com.br/nfe/NotaFiscalXML.html

Não confundir com Nuvem Fiscal (`api.nuvemfiscal.com.br`, OAuth2). Focus usa **HTTP Basic + token**, paths `/v2/{recurso}`.

## 1. Detectar runtime

1. Token da empresa (painel Focus). Sem token: parar e pedir. Não inventar.
2. Ambiente: `FOCUSNFE_TOKEN`, `FOCUSNFE_ENV` (`homologacao`|`producao`) ou equivalente no projeto.
3. Homologação não tem validade fiscal. Produção emite documento real.

```bash
# smoke
curl -u "$FOCUSNFE_TOKEN:" https://homologacao.focusnfe.com.br/v2/empresas
```

401 HTML `HTTP Basic: Access denied` = token ausente, senha não vazia, ou `Authorization` malformado. Não é JSON.

## 2. Ambiente e auth

| Ambiente | Base |
|---|---|
| Homologação | `https://homologacao.focusnfe.com.br/v2` |
| Produção | `https://api.focusnfe.com.br/v2` |

Auth: RFC 7617 Basic. Usuário = token. Senha = string vazia.

```http
Authorization: Basic BASE64(token + ":")
```

```bash
curl -u 'TOKEN:' https://api.focusnfe.com.br/v2/nfe/REF
```

Sem header de API key separado. Mesmo esquema nos dois ambientes; muda URL e token.

TLS: Java costuma exigir cadeia completa no truststore. `openssl s_client -showcerts -connect api.focusnfe.com.br:443`

## 3. Referência (`ref`)

Identificador da emissão, único **por token/empresa**. Alfanumérico. Sem acento, espaço, `@`, `/`.

- Rejeitada / erro antes de autorizar: pode reenviar a **mesma** `ref` depois de corrigir o JSON.
- Autorizada (mesmo se depois cancelada): `ref` **queimada**. Nova emissão precisa de `ref` nova.

Emissão: query `?ref=`. Consulta/cancelamento/eventos: path `/{referencia}`.

## 4. Síncrono vs assíncrono

| Documento | Emissão | Acompanhar |
|---|---|---|
| NFe | Assíncrono padrão (`202`). Alguns estados/contas: síncrono (`201`) | GET ou webhook `nfe` |
| NFCe | Sempre síncrono (`201`, inclusive rejeição SEFAZ) | GET. Contingência: `forma_emissao=offline`. Hook: `nfce_contingencia` / `nfce_consulta_automatica` (não existe `event=nfce`) |
| NFSe municipal | Aceite síncrono (`201` processando) + fila na prefeitura | GET ou webhook `nfse` |
| NFSe nacional (`/nfsen`) | Assíncrono (`202`) | GET ou webhook `nfsen` |
| CTe | Assíncrono (`202`). CTe OS / Simplificado: síncrono na prática da doc | GET ou webhook `cte` |
| MDFe, NFCom, DCe, NFGás | Assíncrono (`202`) | GET + hook |

Não polar GET em loop se der para cadastrar webhook.

## 5. HTTP comum

Erro de aplicação (JSON):

```json
{ "codigo": "requisicao_invalida", "mensagem": "...", "erros": [{ "mensagem": "...", "campo": "tipo_documento" }] }
```

NFSe de prefeitura ainda pode devolver `erros[].codigo` / `correcao` (ex. `L99`).

| HTTP | Significado típico |
|---|---|
| 200 | Consulta, cancelamento, evento, listagem |
| 201 | NFe síncrona autorizada / NFSe aceita / NFCe síncrona — **ler `status`**: NFCe 201 ainda pode ser `erro_autorizacao` |
| 202 | Aceito, processando (NFe/CTe/MDFe/NFSen) |
| 302 | PDF de documento recebido: URL em `Location`. **Não** reenviar Basic Auth no GET do arquivo |
| 400 | `ref` faltando, JSON inválido, `justificativa` fora de 15–255 |
| 401 | Token. Corpo HTML |
| 403 | Sem permissão / backup |
| 404 | `nao_encontrado` |
| 409 | Conflito (CTe/MDFe já em fila) |
| 415 | `formato_invalido` — `Content-Type` ou body vazio |
| 422 | Negócio: `erro_validacao_schema`, `already_processed`, `pending_operation`, `nfe_nao_autorizada`, `permissao_negada` |

Códigos `codigo` extraídos do OpenAPI: [catalog.md](references/catalog.md).

Arquivos (`caminho_xml_*`, `caminho_danfe`): path relativo. GET `{BASE_SEM_V2}{caminho}` com o mesmo Basic, salvo URL pré-assinada / S3 (`url_danfse`). NFCe: `caminho_danfe` é **HTML**; consumidor usa `qrcode_url` / `url_consulta_nf`.

## 6. `status` do documento

Normalizar sempre a string. Não assumir gênero (`autorizado` vs `autorizada`) — OpenAPI desta API usa **masculino**.

| Valor | Onde |
|---|---|
| `processando_autorizacao` | NFe, NFSe, NFSen, CTe, MDFe |
| `autorizado` | Autorização SEFAZ/prefeitura/ADN |
| `cancelado` | Cancelamento ok |
| `erro_autorizacao` | Rejeição |
| `erro_cancelamento` | Cancelamento falhou |
| `denegado` | NFCe (e NFe) na consulta |
| `contingencia_offline` | Flag boolean na NFCe, não é `status` |
| `incluido` / `erro_inclusao` | Evento MDFe (condutor/DFe) |

Consulta NFe/NFCe `?completa=1` acrescenta `requisicao_nota_fiscal` e protocolo. Sem isso o payload é resumo (`chave_nfe`, `numero`, `serie`, caminhos; NFCe + QR).

## 7. Fluxo de implementação

1. Definir documento (NFe / NFCe / NFSe / nfsen / recebido).
2. Cadastrar empresa se SaaS multi-CNPJ (`POST /empresas`). Certificado e habilitação no painel/campos `habilita_*`.
3. `POST /hooks` com `event` + `url` **antes** de emitir em massa.
4. `POST /{recurso}?ref=` com JSON. Tratar 201/202 vs 4xx.
5. Persistir `ref`. Se 202: esperar webhook ou GET.
6. Autorizado: guardar `chave_*`, `numero`, caminhos XML/PDF.
7. Cancelar só se `status=autorizado`. `justificativa` 15–255. Prazos: NFe ~24h (UF pode alongar); NFCe **30 minutos**.
8. `ref` autorizada não reutiliza.

## 8. Armadilhas

- Basic com senha preenchida = 401.
- Polling sem webhook estoura limite e atrasa autorização.
- `already_processed` / `nfe_autorizada`: a `ref` já autorizou. Consultar, não reemitir.
- `pending_operation`: ainda na fila. GET/hook, não POST de novo.
- Manifestação `nao_realizada` exige justificativa 15–255.
- NFe recebida: lista devolve **resumo** até manifestar (`ciencia` libera XML completo).
- Lista recebidas: 100 itens; paginar com `versao` + headers `X-Total-Count`, `X-Max-Version`.
- PDF recebido: 302 + `Location` pré-assinada; cliente HTTP não deve colar `Authorization` no host do arquivo.
- NFSe municipal: município manda na prática. Conferir [municípios integrados](https://focusnfe.com.br/cidades-integradas-nfse/) e `GET /municipios/{ibge}/json`. Campos (RT) da reforma podem ser ignorados/rejeitados.
- OpenAPI de `Tomador` marca `cpf` e `cnpj` como required ao mesmo tempo — na emissão real é um **ou** outro.
- Comunicador Offline não é a API cloud. Paths `/v2/fiscal/nfce` no OpenAPI local; não prefixar de novo com `/v2` da nuvem.
- Backup cobre NFe, NFCe, NFCom, CTe, MDFe — **não** NFSe.
- NFCe: DANFCe é HTML (`caminho_danfe`). `data_emissao` >5 min → SEFAZ `704`. Sem CSC → 422. Cancelar em **30 min**. POST 201 com `status=erro_autorizacao` ainda é rejeição, não sucesso fiscal.

## 9. Router

| Tarefa | Arquivo |
|---|---|
| Qualquer método/HTTP | [catalog.md](references/catalog.md) |
| NFe / CTe / MDFe | [nfe.md](references/nfe.md) |
| NFCe nuvem + Comunicador Offline | [nfce.md](references/nfce.md) |
| NFSe municipal / nacional | [nfse.md](references/nfse.md) |
| Recebidas + manifestação | [recebidas.md](references/recebidas.md) |
| Empresas, hooks, backups, CEP/NCM/CNPJ | [gestao.md](references/gestao.md) |

Docs oficiais: [introdução](https://doc.focusnfe.com.br/reference/introducao) · [auth](https://doc.focusnfe.com.br/reference/autenticacao) · [ambiente](https://doc.focusnfe.com.br/reference/ambiente) · [ref](https://doc.focusnfe.com.br/reference/referencia) · suporte `suporte@focusnfe.com.br`
