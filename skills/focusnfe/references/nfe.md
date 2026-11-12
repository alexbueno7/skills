# NFe, CTe, MDFe (Focus NFe)

NFCe (nuvem `/nfce` + Comunicador) está em [nfce.md](nfce.md). Não misturar path `/nfe` com `/nfce`.

Servidores OpenAPI: `https://api.focusnfe.com.br/v2` e `https://homologacao.focusnfe.com.br/v2`.

## NFe (`/nfe`)

Campos do JSON ↔ XML 4.00: https://campos.focusnfe.com.br/nfe/NotaFiscalXML.html

| Método | Path | HTTP | Notas |
|---|---|---|---|
| POST | `/nfe?ref=` | 201 autorizado síncrono, 202 processando | Padrão assíncrono |
| GET | `/nfe/{ref}` | 200 | `completa=0\|1` |
| DELETE | `/nfe/{ref}` | 200 | Body `{ "justificativa": "15..255" }`. ~24h. Só `autorizado` |
| POST | `/nfe/{ref}/carta_correcao` | 200 | Até 20 CCe; vale a última. Não corrige imposto, remetente/destinatário, datas |
| POST | `/nfe/{ref}/email` | 200 | Envio async; confirmação síncrona |
| POST | `/nfe/inutilizacao` | 200 | Síncrono. Numeração costuma ser automática |
| GET | `/nfe/inutilizacoes` | 200 | Filtros cnpj/cpf/datas/faixa |
| POST | `/nfe/importacao` | 200 | XML; emitente precisa existir; certificado não obrigatório para importar |
| POST | `/nfe/danfe` | 200 | Preview **sem** valor fiscal |
| POST | `/nfe/{ref}/danfe_etiqueta` | 200 | |
| POST | `/nfe/{ref}/ator_interessado` | 200 | Até 6 meses após autorização |
| POST/DELETE | `/nfe/{ref}/insucesso_entrega` | 200 | |
| POST/GET/DELETE | `/nfe/{ref}/econf` (+ `/{protocolo}`) | 200 | Cancelar ECONF na ordem de envio |
| POST/DELETE | `/nfe/{ref}/evento` | 200 | |
| POST | `/nfe/{ref}/hook` | 200 | Reenvia webhook |

### GET 200 — oneOf

**processando**

```json
{ "cnpj_emitente": "...", "ref": "...", "status": "processando_autorizacao" }
```

**autorizado**

```json
{
  "cnpj_emitente": "12345678000123",
  "ref": "referencia_000899_nfe",
  "status": "autorizado",
  "status_sefaz": "100",
  "mensagem_sefaz": "Autorizado o uso da NF-e",
  "chave_nfe": "NFe4119...",
  "numero": "22",
  "serie": "1",
  "caminho_xml_nota_fiscal": "/arquivos/.../nfe.xml",
  "caminho_danfe": "/arquivos/.../danfe.pdf"
}
```

`completa=1` adiciona `protocolo` e `requisicao_nota_fiscal` (espelho do XML).

**cancelado**: `status=cancelado` + `caminho_xml_cancelamento`.

**erro_autorizacao**: `status=erro_autorizacao` + `status_sefaz` + `mensagem_sefaz` + `erros[]`.

### POST emitir — erros 422

- `permissao_negada`
- `pending_operation` — ainda processando
- `already_processed` — já autorizada
- `erro_validacao_schema` + `erros[].campo`

DELETE 422: `nfe_nao_autorizada`. 400: justificativa fora do tamanho.

Carta de correção / eventos: `status` `autorizado` | `erro_autorizacao`.

## CTe (`/cte`, `/cte_os`, `/cte_simp`)

CTe comum: pré-validação síncrona; autorização **assíncrona** (`202`). OS e Simplificado: processamento **síncrono** na doc.

Consulta/cancelamento/CCe/hook: `/cte/{ref}` (Simplificado reusa esses paths).

CCe: não corrige imposto, remetente/destinatário, datas. Até 20; vale a última. Informar o **nome do campo** da API a corrigir.

Modais: rodoviário, aéreo, aquaviário, ferroviário, dutoviário, multimodal — ver https://campos.focusnfe.com.br/cte_cteos/

HTTP emitir: 202, 400, 401, 409, 422.

## MDFe (`/mdfe`)

Emissão 202 (há modo síncrono configurável na empresa). Depois: cancelar, encerrar (obrigatório ao fim da viagem), `inclusao_condutor`, `inclusao_dfe` (carregamento posterior). Encerrar ≠ cancelar.

422 típico: `mdfe_em_processamento`, `mdfe_ja_autorizado`, `mdfe_ja_encerrado`.

## NFCom, DCe, NFGás

Mesmo padrão: POST `?ref=` → 202; GET; DELETE; POST `.../hook`. NFGás está em beta.
