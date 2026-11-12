---
name: notas-fiscais-brasil
description: "Reviews and guides the implementation of Brazilian tax invoice issuing and management (NFS-e, NF-e, NFC-e): tax classification, withholdings, calculations, payloads, integration with providers and tax authorities, states, cancellation, tests and reconciliation. Use to audit invoice issuers or to fix and implement fiscal flows for any company, tax regime or municipality. Brazil only. For the payer's withholdings see retencoes-tributarias-tomador; for the Focus NFe integration see focusnfe. PT-BR: Revisa e orienta implementação de emissão e gestão de notas fiscais brasileiras (NFS-e, NF-e e NFC-e): enquadramento tributário, retenções, cálculos, payloads, integração com provedores e autoridades fiscais, estados, cancelamento, testes e conciliação. Use para auditar emissores ou corrigir e implementar fluxos fiscais."
---

# Revisão e implementação de notas fiscais brasileiras

## Objetivo e modos

Verificar se regras fiscais e fluxo técnico correspondem à operação real e implementar apenas o escopo solicitado. Skill genérica: nenhuma empresa, cidade, regime, alíquota ou provedor é padrão.

- **Revisão:** analisar legislação, contratos de integração e código; entregar achados com evidências, impacto e teste sugerido. Não editar nem emitir documentos.
- **Implementação/correção:** identificar causa, aplicar menor alteração coerente com arquitetura e deixar testes executáveis.
- Pedido ambíguo: fazer diagnóstico somente leitura e esclarecer antes de alterar. Pedido de implementação não autoriza emissão real, cancelamento, substituição ou recolhimento em produção.

## 1. Delimitar operação e fontes

Identificar documento (NFS-e, NF-e ou NFC-e), finalidade, competência, regime do emitente e destinatário/tomador, estabelecimentos, município/UF, serviço ou mercadoria efetivos, operação interna/interestadual/exterior e eventos envolvidos. Identificar provedor, versão da API/layout e ambiente.

Não inferir documento ou tributação apenas por CNAE, nome da empresa ou regime. Não aplicar regras de NFS-e a NF-e/NFC-e. Dados ausentes permanecem desconhecidos; não assumir Lucro Presumido, alíquota zero, ausência de retenção ou município da sede.

Fontes, com responsabilidades distintas:
- **Legislação oficial vigente na competência:** define obrigação fiscal, incidência, dispensa e responsável. Consultar normas federais, estaduais e municipais pertinentes, incluindo regras transitórias de IBS/CBS quando aplicáveis.
- **Manuais oficiais e documentação do provedor:** definem layout, códigos, endpoints, validações e estados; não substituem fundamento tributário.
- **Contabilidade e documentos do cliente:** informam enquadramento e operação. Registrar data e fundamento informado; divergência não vira regra automática.
- **Código e documentos fiscais autorizados:** evidenciam comportamento implementado, não comprovam por si só correção legal.

Registrar fonte, dispositivo/versão, vigência e data de consulta. Sem acesso à fonte, declarar validação pendente e não inventar códigos, percentuais ou endpoints. Bloquear conclusão fiscal e emissão afetadas pela dúvida, sem impedir diagnóstico ou correções técnicas independentes.

## 2. Montar matriz fiscal verificável

Para cada tributo relevante: incidência, base, deduções permitidas, alíquota, responsável, retenção, dispensa, limite, arredondamento, fato gerador, vigência e campo correspondente no layout. Resultado: aplicável, não aplicável ou pendente, sempre com evidência.

### NFS-e e retenções

- Separar município competente pelo ISS (LC 116/2003, arts. 3º e 4º) da responsabilidade pela retenção (art. 6º e lei aplicável). Local de incidência não implica retenção automática.
- Conferir item da lista, código municipal/nacional e estabelecimento prestador. Serviço efetivo prevalece sobre associação genérica ao CNAE.
- Não presumir substituição tributária pelo porte ou categoria do tomador. Indústrias, bancos, concessionárias e órgãos públicos dependem do enquadramento legal aplicável.
- Separar regime do prestador do regime do pagador. Pagador Simples não dispensa automaticamente IRRF; avaliar CSRF separadamente, inclusive Lei 10.833/2003, art. 30, §2º.
- Serviços profissionais: consultar Decreto 9.580/2018, art. 714, e exceções para IRRF; Lei 10.833/2003, arts. 30 e 31, para CSRF. Verificar INSS e outros tributos quando a operação exigir, sem presumir incidência.
- Órgãos públicos: distinguir esfera e natureza do ente e consultar IN RFB 1.234/2012 e alterações quando aplicáveis. Não copiar alíquota privada nem enquadrar serviço hospitalar apenas pelo nome da clínica.
- Limites: verificar alcance do art. 67 da Lei 9.430/1996 e do art. 31, §3º, da Lei 10.833/2003, inclusive exceções. Calcular sobre imposto e evento corretos; não substituir por valor bruto fixo da nota nem agregar pagamentos por regra histórica sem confirmar vigência.
- Distinguir emissão, pagamento/crédito, destaque, retenção efetiva e recolhimento. Mensalidade/disponibilidade contratual não é dispensa automática.

### NF-e e NFC-e

- Conferir natureza da operação, CFOP, NCM, CST/CSOSN, origem, destinatário, finalidade, presença e demais classificações exigidas pelo layout vigente.
- Avaliar ICMS próprio/ST, DIFAL/FCP, IPI, PIS/COFINS e IBS/CBS conforme operação, regime e vigência. Não aplicar todos por padrão nem equiparar tributo destacado a valor retido.
- Validar regras de itens, totais, frete, descontos, pagamentos/troco e contingência no manual correspondente. Usar códigos e campos documentados, não exemplos de outro documento fiscal.

## 3. Confrontar regra, código e payload

Rastrear entrada, cadastro, cálculo, persistência, serialização, envio e retorno. Em revisão, cada achado precisa de regra esperada, trecho/caminho que diverge, cenário reproduzível e impacto real; dúvida fiscal é pendência, não bug comprovado.

Em implementação:
- Manter regra fiscal no backend/fonte de verdade existente; frontend exibe e valida interação, sem cálculo concorrente independente.
- Reutilizar módulos e tipos do projeto. Não criar motor tributário genérico, dependência ou configuração sem necessidade concreta.
- Valores monetários com decimal apropriado ou unidades inteiras, preservando precisão exigida para quantidades e alíquotas; arredondar no estágio definido pelo layout/regra. Não usar tolerância para ocultar divergências.
- Separar base, imposto calculado, imposto retido, total fiscal e recebível. Não subtrair ISS não retido nem todos os tributos destacados do líquido.
- Validar identidade/tenant, permissões, documentos, códigos, competência, valores e campos obrigatórios antes do envio. Impedir emissão entre empresas diferentes.
- Preservar ausência, zero, isenção, não incidência e não retenção como conceitos distintos quando o contrato exigir. Não converter erro ou dado desconhecido em zero.
- Guardar evidências e versão dos parâmetros usados na emissão conforme estrutura existente, sem recalcular documento autorizado com regra atual. Novas regras precisam respeitar vigência e documentos históricos.

## 4. Validar ciclo de vida da integração

- Separar homologação/produção, credenciais e certificados; não expor segredos nem documentos pessoais em logs.
- Distinguir pedido recebido, processamento, autorização, rejeição, falha de transporte e cancelamento confirmado. HTTP 200, PDF ou protocolo de fila não comprovam autorização fiscal.
- Em timeout após envio, consultar pela referência/chave documentada antes de reenviar. Usar idempotência oferecida pelo provedor e controles existentes contra concorrência; evitar duplicidade por retry.
- Validar webhooks conforme mecanismo documentado (assinatura/autenticação quando disponível), tratar duplicados e eventos fora de ordem, correlacionar empresa e documento e não permitir regressão indevida de estado. Se origem não for verificável, confirmar no provedor antes de mudança fiscal sensível.
- Conciliar status local com autoridade/provedor; persistir chave, protocolo, XML e eventos conforme contrato e requisitos de acesso/guarda. PDF não substitui documento eletrônico autorizado.
- Cancelamento, substituição, correção e inutilização têm regras próprias por documento e jurisdição. Não confundir exclusão local com evento fiscal; exigir autorização e confirmar resultado remoto.
- Documento anterior incorreto: identificar alcance e propor tratamento com contabilidade. Não cancelar em massa, sobrescrever XML autorizado ou declarar passivo regularizado sem evidência.

## 5. Testar proporcionalmente à mudança

Usar scripts e infraestrutura existentes; cada lógica não trivial precisa de teste executável. Selecionar cenários afetados:

- Regimes distintos de emitente e tomador; privado/público e municípios/UFs diferentes.
- Retenção presente/ausente, isenção/não incidência, dado obrigatório ausente e enquadramento pendente.
- Limite imediatamente abaixo, igual e acima; arredondamento, múltiplos itens, descontos e divergência entre base da nota e pagamento.
- Campos e totais do payload, vigência antiga/nova e preservação de documento autorizado.
- Autorização, rejeição, processamento assíncrono, timeout após aceite, retry, webhook duplicado/fora de ordem e tentativa entre tenants.
- Cancelamento/substituição apenas se alterados, com permissões e estados válidos.

Mocks cobrem contratos isolados, não comprovam autorização fiscal. Validar integração em homologação quando disponível e autorizada; documentar limitações. Não emitir nota real para testar. Validação técnica não substitui validação tributária.

## Entrega

Informar escopo/documento, regras confirmadas e fontes, pendências fiscais, achados ou arquivos alterados, comportamento, checks executados e limites de verificação. Separar implementado, testado em homologação e confirmado em produção. Não declarar correto o enquadramento não validado.

## Referência histórica opcional

