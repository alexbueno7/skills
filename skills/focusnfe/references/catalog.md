# Catálogo de endpoints Focus NFe v2

Fonte: OpenAPI embutido em https://doc.focusnfe.com.br (páginas `.md`, 2026-09-17).
Base: `https://homologacao.focusnfe.com.br/v2` ou `https://api.focusnfe.com.br/v2`.
Auth: HTTP Basic, usuário = token, senha vazia.

Total extraído: **127** operations.

Comunicador Offline (`/v2/fiscal/nfce/*`) é API **local**, não cloud. Não concatenar com o prefixo `/v2` da nuvem.

## Backups (NFe, NFCe, CTe e MDFe)

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/backups/{cnpj}.json` | Consultar por CNPJ | 200, 401, 403 | path:cnpj* |

## CEPs - Código de Endereçamento Postal (beta)

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/ceps` | Consultar | 200, 400, 401 | query:codigo_ibge, query:uf, query:logradouro, query:localidade, query:offset |
| `GET` | `/ceps/{cep}` | Consultar por número | 200, 401, 404 | path:cep* |

## CFOP - Código Fiscal de Operações e Prestações

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/cfops` | Consultar | 200, 401 | query:codigo, query:descricao, query:offset |
| `GET` | `/cfops/{codigo}` | Consultar por código | 200, 401, 404 | path:codigo* |

## CNAE - Classificação Nacional de Atividades Econômicas

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/codigos_cnae` | Consultar | 200, 401 | query:codigo, query:descricao, query:secao, query:descricao_secao, query:divisao, query:descricao_divisao, query:grupo, query:descricao_grupo, query:classe, query:descricao_classe, query:subclasse, query:descricao_subclasse, query:offset |
| `GET` | `/codigos_cnae/{codigo}` | Consultar por código | 200, 401, 404 | path:codigo* |

## CNPJ - Cadastro Nacional da Pessoa Jurídica

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/cnpjs/{cnpj}` | Consultar | 200, 400, 401, 404 | path:cnpj* |

## CTe Recebidas - Conhecimento de Transporte Eletrônico

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/ctes_recebidas` | Consultar | 200, 400, 401, 404 | query:cnpj*, query:versao |
| `GET` | `/ctes_recebidas/{chave}` | Consultar por chave | 200, 401, 404 | path:chave*, query:cnpj, query:completa |
| `GET` | `/ctes_recebidas/{chave}.json` | Consulta em formato JSON | 200, 401, 404 | path:chave*, query:completa |
| `GET` | `/ctes_recebidas/{chave}.pdf` | Baixar o DACTe | 200, 401, 404 | path:chave* |
| `GET` | `/ctes_recebidas/{chave}.xml` | Baixar o XML | 200, 401, 404 | path:chave* |
| `GET` | `/ctes_recebidas/{chave}/cancelamento.xml` | Baixar o XML de cancelamento | 200, 401, 404 | path:chave* |
| `GET` | `/ctes_recebidas/{chave}/carta_correcao.xml` | Baixar o XML de carta de correção | 200, 401, 404 | path:chave* |
| `GET` | `/ctes_recebidas/{chave}/desacordo` | Consultar desacordo | 200, 401, 404 | path:chave* |
| `POST` | `/ctes_recebidas/{chave}/desacordo` | Informar desacordo | 200, 400, 401, 403, 404, 415 | path:chave* |
| `POST` | `/ctes_recebidas/{chave}/hook` | Solicitar reenvio de notificação | 200 | path:chave* |

## CTe, CTe OS e CTe Simplificado - Conhecimento de Transporte Eletrônico

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/cte` | Emitir CTe | 202, 400, 401, 409, 422 | query:ref* |
| `DELETE` | `/cte/{referencia}` | Cancelar | 200, 400, 401, 404, 415 | path:referencia* |
| `GET` | `/cte/{referencia}` | Consultar | 200, 401, 404 | path:referencia*, query:completa |
| `POST` | `/cte/{referencia}/carta_correcao` | Carta de correção | 200, 400, 401, 404 | path:referencia* |
| `POST` | `/cte/{referencia}/hook` | Solicitar reenvio de notificação | 200 | path:referencia* |
| `POST` | `/cte_os` | Emitir CT-e OS | 202, 400, 401, 409, 422 | query:ref* |
| `POST` | `/cte_simp` | Emitir CT-e Simplificado | 202, 400, 401, 409, 422 | query:ref* |

## Comunicador Offline Focus NFe

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/v2/fiscal/nfce` | Emitir NFCe | 200 | query:ref*, query:tipo_contingencia, query:forma_emissao |
| `GET` | `/v2/fiscal/nfce/pendentes` | Listar NFCes pendentes de efetivação | 200 | — |
| `GET` | `/v2/fiscal/nfce/{chave_nfe}-canc.xml` | Gerar XML cancelado da NFCe | 200 | path:chave_nfe* |
| `GET` | `/v2/fiscal/nfce/{chave_nfe}.pdf` | Gerar espelho PDF da NFCe | 200 | path:chave_nfe* |
| `GET` | `/v2/fiscal/nfce/{chave_nfe}.xml` | Gerar XML autorizado da NFCe | 200 | path:chave_nfe* |
| `DELETE` | `/v2/fiscal/nfce/{referencia}` | Cancelar NFCe | 200 | path:referencia* |
| `GET` | `/v2/fiscal/nfce/{referencia}` | Consultar NFCe | 200 | path:referencia* |
| `PUT` | `/v2/fiscal/nfce/{referencia}/efetivar` | Efetivar NFCe em contingência | 200 | path:referencia* |

## DCe - Declaração de Conteúdo Eletrônica

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/dce` | Emitir | 202, 401, 403 | query:ref* |
| `DELETE` | `/dce/{referencia}` | Cancelar | 200, 400, 401, 404, 415 | path:referencia* |
| `GET` | `/dce/{referencia}` | Consultar | 200, 401, 404 | path:referencia* |
| `POST` | `/dce/{referencia}/hook` | Solicitar reenvio de notificação | 200 | path:referencia* |

## Emails bloqueados

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `DELETE` | `/blocked_emails/{email}` | Solicitar exclusão | 200, 401, 404, 422 | path:email* |
| `GET` | `/blocked_emails/{email}` | Consultar | 200, 401, 404 | path:email* |

## Empresas

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/empresas` | Listar | 200, 401 | query:cnpj, query:cpf, query:offset |
| `POST` | `/empresas` | Criar | 200, 400, 401, 422 | query:dry_run |
| `DELETE` | `/empresas/{id}` | Excluir | 200, 401, 404, 422 | path:id* |
| `GET` | `/empresas/{id}` | Consultar por ID | 200, 401, 404, 422 | path:id* |
| `PUT` | `/empresas/{id}` | Atualizar | 200, 400, 401, 404, 422 | path:id*, query:dry_run |

## MDFe - Manifesto Eletrônico de Documentos Fiscais

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/mdfe` | Emitir | 202, 400, 401, 409, 422 | query:ref* |
| `DELETE` | `/mdfe/{referencia}` | Cancelar | 200, 400, 401, 404, 415 | path:referencia* |
| `GET` | `/mdfe/{referencia}` | Consultar | 200, 401, 404 | path:referencia* |
| `POST` | `/mdfe/{referencia}/encerrar` | Encerrar | 200, 400, 401, 404, 422 | path:referencia* |
| `POST` | `/mdfe/{referencia}/hook` | Solicitar reenvio de notificação | 200 | path:referencia* |
| `POST` | `/mdfe/{referencia}/inclusao_condutor` | Incluir um condutor | 200, 400, 401, 404 | path:referencia* |
| `POST` | `/mdfe/{referencia}/inclusao_dfe` | Incluir um DFe | 200, 400, 401, 404 | path:referencia* |

## Municípios (beta)

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/municipios` | Listar ou filtrar municípios | 200, 401 | query:sigla_uf, query:nome_municipio, query:nome, query:status_nfse, query:limit |
| `GET` | `/municipios/{codigo_municipio}` | Consultar município por código IBGE | 200, 401, 404 | — |
| `GET` | `/municipios/{codigo_municipio}/codigos_tributarios_municipio` | Listar códigos tributários municipais | 200, 401, 404 | query:codigo, query:descricao, query:limit |
| `GET` | `/municipios/{codigo_municipio}/codigos_tributarios_municipio/{codigo}` | Consultar código tributário municipal por código | 200, 401, 404 | path:codigo* |
| `GET` | `/municipios/{codigo_municipio}/itens_lista_servico` | Listar itens da lista de serviço do município | 200, 401, 404 | query:codigo, query:descricao, query:limit |
| `GET` | `/municipios/{codigo_municipio}/itens_lista_servico/{codigo}` | Consultar item da lista de serviço por código | 200, 401, 404 | path:codigo* |
| `GET` | `/municipios/{codigo_municipio}/json` | Consultar o JSON de exemplo do município pelo código IBGE | 200, 401, 404 | — |

## NCM - Nomenclatura Comum do Mercosul

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/ncms` | Consultar | 200, 401 | query:codigo, query:descricao, query:capitulo, query:posicao, query:subposicao1, query:subposicao2, query:item1, query:item2, query:offset |
| `GET` | `/ncms/{codigo}` | Consultar por código | 200, 401, 404 | path:codigo* |

## NFC-e - Nota Fiscal de Consumidor Eletrônica

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/nfce` | Emitir | 201, 400, 401, 403, 415, 422 | query:ref*, query:completa, query:forma_emissao |
| `POST` | `/nfce/inutilizacao` | Inutilizar numeração | 200, 400, 401, 403, 415, 422 | — |
| `GET` | `/nfce/inutilizacoes` | Consultar inutilizações | 200, 400, 401 | query:cnpj, query:cpf, query:data_recebimento_inicial, query:data_recebimento_final, query:numero_inicial, query:numero_final |
| `DELETE` | `/nfce/{referencia}` | Cancelar | 200, 400, 401, 403, 404, 415, 422 | path:referencia* |
| `GET` | `/nfce/{referencia}` | Consultar | 200, 401, 403, 404 | path:referencia*, query:completa |
| `POST` | `/nfce/{referencia}/econf` | Registrar Conciliação Financeira (ECONF) | 200, 400, 401, 403, 404, 415, 422 | path:referencia* |
| `DELETE` | `/nfce/{referencia}/econf/{numero_protocolo}` | Cancelar ECONF | 200, 401, 403, 404, 422 | path:referencia*, path:numero_protocolo* |
| `GET` | `/nfce/{referencia}/econf/{numero_protocolo}` | Consultar ECONF | 200, 401, 403, 404 | path:referencia*, path:numero_protocolo* |
| `POST` | `/nfce/{referencia}/email` | Enviar NFC-e por email | 200, 400, 401, 403, 404, 415 | path:referencia* |

## NFCom - Nota Fiscal de Comunicação

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/nfcom` | Emitir | 202, 401, 403 | query:ref* |
| `DELETE` | `/nfcom/{referencia}` | Cancelar | 200, 400, 401, 404, 415 | path:referencia* |
| `GET` | `/nfcom/{referencia}` | Consultar | 200, 401, 404 | path:referencia* |
| `POST` | `/nfcom/{referencia}/hook` | Solicitar reenvio de notificação | 200 | path:referencia* |

## NFGás - Nota Fiscal Eletrônica do Gás

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/nfgas` | Emitir | 202, 401, 403 | query:ref* |
| `DELETE` | `/nfgas/{referencia}` | Cancelar | 200, 400, 401, 404, 415 | path:referencia* |
| `GET` | `/nfgas/{referencia}` | Consultar | 200, 401, 404 | path:referencia* |
| `POST` | `/nfgas/{referencia}/hook` | Solicitar reenvio de notificação | 200 | path:referencia* |

## NFSe - Nota Fiscal de Serviço

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/nfse` | Emitir | 201, 400, 401, 422 | query:ref* |
| `DELETE` | `/nfse/{referencia}` | Cancelar | 200, 400, 404 | path:referencia* |
| `GET` | `/nfse/{referencia}` | Consultar | 200, 404 | path:referencia* |
| `POST` | `/nfse/{referencia}/email` | Reenviar email | 200, 404 | path:referencia* |
| `POST` | `/nfse/{referencia}/hook` | Solicitar reenvio de notificação | 200 | path:referencia* |

## NFSe Nacional - Nota Fiscal de Serviço Padrão Nacional

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/nfsen` | Emitir | 202, 400, 401, 422 | query:ref* |
| `DELETE` | `/nfsen/{referencia}` | Cancelar | 200, 404 | path:referencia* |
| `GET` | `/nfsen/{referencia}` | Consultar | 200, 404 | path:referencia* |
| `POST` | `/nfsen/{referencia}/email` | Reenviar email | 200, 404 | path:referencia* |
| `POST` | `/nfsen/{referencia}/hook` | Solicitar reenvio de notificação | 200 | path:referencia* |

## NFSe Nacional Recebidas

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/nfsens_recebidas` | Consultar | 200, 400, 401 | query:cnpj*, query:completa, query:versao |
| `GET` | `/nfsens_recebidas/{chave}.html` | DANFSe HTML | 200, 401, 404 | path:chave* |
| `GET` | `/nfsens_recebidas/{chave}.json` | Consulta em formato JSON | 200, 401, 404 | path:chave* |
| `GET` | `/nfsens_recebidas/{chave}.pdf` | Visualizar/Baixar o PDF da DANFSe | 200, 401, 404 | path:chave* |
| `GET` | `/nfsens_recebidas/{chave}.xml` | Consultar em formato XML | 200, 401, 404 | path:chave* |
| `POST` | `/nfsens_recebidas/{chave}/hook` | Solicitar reenvio de notificação | 200, 401, 404 | path:chave* |

## NFe - Nota Fiscal Eletrônica

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `POST` | `/nfe` | Emitir | 201, 202, 400, 401, 415, 422 | query:ref* |
| `POST` | `/nfe/danfe` | Pré-visualização de DANFe | 200, 401 | — |
| `POST` | `/nfe/importacao` | Importar NFe | 200, 400, 401, 415 | query:ref |
| `POST` | `/nfe/inutilizacao` | Inutilizar Numeração | 200, 400, 401, 404, 415, 422 | — |
| `GET` | `/nfe/inutilizacoes` | Consultar Inutilizações | 200, 400, 401 | query:cnpj, query:cpf, query:data_recebimento_inicial, query:data_recebimento_final, query:numero_inicial, query:numero_final |
| `DELETE` | `/nfe/{referencia}` | Cancelar | 200, 400, 401, 404, 415, 422 | path:referencia* |
| `GET` | `/nfe/{referencia}` | Consultar | 200, 401, 404 | path:referencia*, query:completa |
| `POST` | `/nfe/{referencia}/ator_interessado` | Registrar Ator Interessado | 200, 400, 401, 404, 415 | path:referencia* |
| `POST` | `/nfe/{referencia}/carta_correcao` | Emitir Carta de Correção | 200, 400, 401, 404, 415 | path:referencia* |
| `POST` | `/nfe/{referencia}/danfe_etiqueta` | Criação DANFe Etiqueta | 200, 401, 404 | path:referencia* |
| `POST` | `/nfe/{referencia}/econf` | Registrar Conciliação Financeira (ECONF) | 200, 400, 401, 404, 415, 422 | path:referencia* |
| `DELETE` | `/nfe/{referencia}/econf/{numero_protocolo}` | Cancelar Conciliação Financeira (ECONF) | 200, 400, 401, 404, 422 | path:referencia*, path:numero_protocolo* |
| `GET` | `/nfe/{referencia}/econf/{numero_protocolo}` | Consultar Conciliação Financeira (ECONF) | 200, 401, 404 | path:referencia*, path:numero_protocolo* |
| `POST` | `/nfe/{referencia}/email` | Enviar NFe por Email | 200, 400, 401, 404, 415 | path:referencia* |
| `DELETE` | `/nfe/{referencia}/evento` | Cancelar evento | 200, 400, 422 | path:referencia* |
| `POST` | `/nfe/{referencia}/evento` | Emitir Evento | 200, 400, 422 | path:referencia* |
| `POST` | `/nfe/{referencia}/hook` | Solicitar reenvio de notificação de NFe | 200 | path:referencia* |
| `DELETE` | `/nfe/{referencia}/insucesso_entrega` | Cancelar Insucesso na Entrega | 200, 400, 401, 404, 415, 422 | path:referencia* |
| `POST` | `/nfe/{referencia}/insucesso_entrega` | Registrar Insucesso na Entrega | 200, 400, 401, 404, 415 | path:referencia* |

## NFe Recebidas - Manifestação do Destinatário

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/nfes_recebidas` | Consultar | 200, 400, 401, 403 | query:cnpj*, query:versao, query:pendente, query:pendente_ciencia |
| `GET` | `/nfes_recebidas/{chave}` | Consultar por chave | 200, 401, 404 | path:chave*, query:cnpj, query:completa |
| `GET` | `/nfes_recebidas/{chave}.json` | Consulta em formato JSON | 200, 401, 404 | path:chave*, query:completa |
| `GET` | `/nfes_recebidas/{chave}.pdf` | Baixar o DANFe | 200, 302, 401, 404 | path:chave* |
| `GET` | `/nfes_recebidas/{chave}.xml` | Baixar o XML | 200, 401, 404 | path:chave* |
| `GET` | `/nfes_recebidas/{chave}/cancelamento.xml` | Baixar o XML de cancelamento | 200, 401, 404 | path:chave* |
| `GET` | `/nfes_recebidas/{chave}/carta_correcao.xml` | Baixar o XML de carta de correção | 200, 401, 404 | path:chave* |
| `DELETE` | `/nfes_recebidas/{chave}/evento` | Cancelar evento | 200, 400, 422 | path:chave* |
| `POST` | `/nfes_recebidas/{chave}/evento` | Evento | 200, 400 | path:chave* |
| `POST` | `/nfes_recebidas/{chave}/hook` | Solicitar reenvio de notificação | 200 | path:chave* |
| `POST` | `/nfes_recebidas/{chave}/manifesto` | Manifestar | 200, 400, 401, 404, 415 | path:chave* |

## Webhooks (Gatilhos)

| Método | Path | Operação | HTTP | Params |
|---|---|---|---|---|
| `GET` | `/hooks` | Listar | 200, 400 | — |
| `POST` | `/hooks` | Criar | 200, 400, 404 | — |
| `DELETE` | `/hooks/{id}` | Excluir | 200 | path:id* |
| `GET` | `/hooks/{id}` | Consultar por ID | 200 | path:id* |

## Códigos de erro (`codigo`) vistos nos OpenAPI

- `1.06`
- `8599603`
- `90049090`
- `already_processed`
- `ambiente_nao_configurado`
- `bad_request`
- `cte_em_processamento`
- `cte_ja_autorizado`
- `empresa_nao_configurada`
- `empresa_nao_habilitada`
- `erro_validacao`
- `erro_validacao_schema`
- `event_not_found`
- `forma_emissao_nao_informada`
- `formato_invalido`
- `mdfe_em_processamento`
- `mdfe_ja_autorizado`
- `mdfe_ja_encerrado`
- `modelo_invalido`
- `nao_autorizado`
- `nao_encontrado`
- `nfe_autorizada`
- `nfe_nao_autorizada`
- `nota_ja_existente`
- `object_not_found`
- `parametros_modal_nao_informados`
- `pending_operation`
- `permissao_negada`
- `requisicao_invalida`

## Enums `status` por schema

- `AtorInteressadoResponse`: `autorizado`, `erro_autorizacao`
- `AutorizadaCompletoResponse`: `autorizado`
- `AutorizadaResponse`: `autorizado`, `cancelado`, `erro_autorizacao`, `negado`
- `CanceladaResponse`: `cancelada`, `cancelado`
- `CancelamentoInsucessoEntregaResponse`: `autorizado`, `erro_autorizacao`
- `CancelamentoNFCeResponse`: `cancelado`, `erro_cancelamento`
- `CancelamentoNFeResponse`: `cancelado`, `erro_cancelamento`
- `CancelamentoResponse`: `cancelado`
- `CartaCorrecaoResponse`: `autorizado`, `erro_autorizacao`
- `DceCanceladaResponse`: `cancelado`
- `DceErroAutorizacaoResponse`: `erro_autorizacao`
- `EconfCancelamentoResponse`: `autorizado`, `erro_autorizacao`
- `EconfResponse`: `autorizado`, `erro_autorizacao`
- `ErroAutorizacaoResponse`: `erro_autorizacao`
- `ErroCancelamentoResponse`: `erro_cancelamento`
- `EventoAutorizadoResponse`: `erro_inclusao`, `incluido`
- `EventoResponse`: `autorizado`, `erro_autorizacao`
- `InsucessoEntregaResponse`: `autorizado`, `erro_autorizacao`
- `InutilizacaoNFCeResponse`: `autorizado`, `erro_autorizacao`
- `InutilizacaoResponse`: `autorizado`, `erro_autorizacao`
- `NFCeAutorizadaResponse`: `autorizado`, `erro_autorizacao`
- `NFCeConsultaResponse`: `autorizado`, `denegado`, `erro_autorizacao`
- `NFeAutorizadaResponse`: `autorizado`
- `NFeConsultaResponse`: `autorizado`, `cancelado`, `denegado`, `erro_autorizacao`, `processando_autorizacao`
- `NFeProcessandoResponse`: `processando_autorizacao`

