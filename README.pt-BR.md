# Agent Skills

Skills para agentes de código (Claude Code, Codex, Cursor, Pi e outros), instaláveis com [`npx skills`](https://skills.sh/). Cada uma abaixo diz o que faz, o que entrega e em que se baseia.

English: [README.md](README.md)

Nomes e descrições estão em inglês e português. As instruções dentro de cada skill estão em português.

## Instalar

Requer Node.js. Rode dentro do projeto, ou use `-g` para instalar em todos os projetos.

```bash
# Instalar todas
npx skills add alexbueno7/skills

# Uma skill só
npx skills add alexbueno7/skills --skill simplify-ui

# Global, para todos os projetos
npx skills add alexbueno7/skills --skill simplify-ui -g

# Só para um agente
npx skills add alexbueno7/skills --skill simplify-ui --agent claude-code

# Atualizar
npx skills update

# Remover
npx skills remove simplify-ui
```

Sem a CLI: copie a pasta `skills/<nome>` para `.claude/skills/` (projeto) ou `~/.claude/skills/` (global), ou a pasta equivalente do seu agente, e abra uma sessão nova.

## Skills

**UI e produto**: [`simplify-ui`](#simplify-ui), [`8pt-grid`](#8pt-grid), [`layout-audit`](#layout-audit)

**Workflow**: [`prompt-brief`](#prompt-brief), [`api-security-audit`](#api-security-audit), [`seo-optimization-suite`](#seo-optimization-suite)

**Integrações**: [`whatsapp-meta-api`](#whatsapp-meta-api), [`whatsmiau`](#whatsmiau), [`mailcheap-api`](#mailcheap-api), [`audaks-cloud`](#audaks-cloud)

**Só Brasil**: [`focusnfe`](#focusnfe), [`notas-fiscais-brasil`](#notas-fiscais-brasil)

### simplify-ui

**O que faz.** Revisa uma tela, página, componente ou fluxo e remove o que não ajuda o visitante a decidir: taglines, texto de apoio e rótulos secundários. Quando a tela deixa de fazer sentido sem esse texto, a skill corrige o layout em vez de devolver o texto. Trabalha em sete passos: nomear o propósito, separar conteúdo de ruído, simplificar a arquitetura, simplificar o design, conferir a experiência de usuário, desenvolvedor e agente juntas, confirmar que nada quebrou, entregar.

**O que entrega.** A mudança aplicada no seu repositório, com relatório curto: o que mudou, onde ver, o que foi verificado e o que depende de decisão comercial.

**Em que se baseia.** O estilo e os layouts que a Apple usa nas páginas de marketing, que o autor tomou como modelo, condensados em um briefing de design citado por inteiro dentro da skill: "as perfect as Linear's website or Apple Notes: simple purpose, simple architecture, simple design, simple implementation". Na prática: título em poucas linhas, uma ação principal e no máximo uma secundária, a mesma escala tipográfica e de espaçamento entre páginas, e nada de faixas decorativas, destaques de cor arbitrários ou movimento sem função. O que se copia de Apple e Linear é a disciplina de corte, não a aparência. Não cita estudo; é uma regra de trabalho com opinião.

**Limites.** Preserva fatos, preços, prazos, URLs, rastreio, contratos e texto legal. Não faz commit, push nem deploy sem autorização.

**Instalar.** `npx skills add alexbueno7/skills --skill simplify-ui` · [SKILL.md](skills/simplify-ui/SKILL.md)

### 8pt-grid

**O que faz.** Dá ao agente uma regra única de espaçamento para qualquer interface: toda margem, padding, gap e tamanho de componente é múltiplo de 8, com 4 para controle mais fino. Define uma escala por papel (dentro do componente, entre itens relacionados, entre grupos, entre seções), valores de partida para componentes comuns e uma lista de revisão rápida.

**O que entrega.** Layouts com espaçamento em uma escala só e, ao revisar UI existente, a lista dos valores que quebravam a escala.

**Em que se baseia.** Duas fontes citadas na skill: o artigo "Everything you should know about 8 point grid system in UX design" (Ashphiar Raihan Rumman, UX Planet, 2022) e uma thread de 2026 de Magdiel Silva sobre escala por papel, proximidade e tokens. O agrupamento segue o princípio de proximidade da Gestalt: o que pertence junto fica mais perto do que o que não pertence.

**Limites.** Ferramenta de consistência, não dogma: tamanho de fonte, bordas de 1px, alinhamento óptico e elementos muito pequenos podem sair da escala.

**Instalar.** `npx skills add alexbueno7/skills --skill 8pt-grid` · [SKILL.md](skills/8pt-grid/SKILL.md)

### layout-audit

**O que faz.** Audita um site página a página antes de um redesign. Primeiro entende o negócio e a oferta, depois pesquisa literatura recente de UX e marketing sobre o problema real encontrado, depois inspeciona as páginas publicadas em larguras de celular, tablet e desktop, e por fim escreve um plano por página ou família de páginas.

**O que entrega.** Um PDF ilustrado (e HTML portável) com evidências, capturas, fontes datadas e plano por fases. Nunca edita o site.

**Em que se baseia.** O mesmo briefing de simplicidade da simplify-ui, mais um método de pesquisa em vez de uma lista fixa de leitura: cada execução busca fontes dos últimos três anos e registra autor, data, método, população e limites de cada uma. Separa pesquisa empírica de orientação profissional e de opinião, e não transfere resultado para contexto onde não foi medido (estudo de checkout não prova efeito em landing B2B). As páginas são medidas em 375/390, 768/1024 e 1440 px.

**Limites.** Chama as skills unslop, ui-ux-pro-max e seo-optimization-suite; instale-as para a auditoria completa. Precisa de ferramenta de navegador para as capturas; sem ela, declara análise parcial. Não cobre área logada, checkout e painéis, salvo pedido.

**Instalar.** `npx skills add alexbueno7/skills --skill layout-audit` · [SKILL.md](skills/layout-audit/SKILL.md)

### prompt-brief

**O que faz.** Recebe uma descrição curta e informal de tarefa e devolve um prompt completo, pronto para colar em um agente de código que não tem contexto. Antes confere três coisas (o que mudar, o resultado esperado, como conferir que ficou pronto) e faz até três perguntas curtas só sobre o que falta.

**O que entrega.** Um bloco de código com o brief em oito seções XML: context, goal, done_when, boundaries, autonomy, proof, report, memory.

**Em que se baseia.** Escrita para tirar o máximo do Claude Fable 5.2, seguindo o guia oficial da Anthropic [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices): ser claro e direto, dar contexto para o modelo saber o objetivo por trás da instrução, e estruturar o prompt com tags XML, que segundo o guia ajudam o Claude a ler prompts que misturam instruções, contexto e entradas. Veja também [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2). Cada seção responde uma pergunta que o agente teria de adivinhar: o que é verdade hoje, o que significa pronto, o que não pode tocar, até onde pode ir sozinho e que evidência trazer. O mesmo guia vale para os outros modelos Claude atuais.

**Limites.** Escreve o prompt e não executa a tarefa. Não inventa fatos, caminhos de arquivo nem causas; suposição entra marcada como hipótese.

**Instalar.** `npx skills add alexbueno7/skills --skill prompt-brief` · [SKILL.md](skills/prompt-brief/SKILL.md)

### api-security-audit

**O que faz.** Faz auditoria de segurança de uma API REST em três fases: reconhecimento, análise de vulnerabilidades por categoria e relatório. Para cada categoria traz o teste a rodar com curl, como é uma resposta vulnerável e a correção.

**O que entrega.** Um relatório de achados a partir do modelo incluído, com severidade, passos de reprodução e correção de cada problema, mais três scripts de apoio: varredura de endpoints, teste de autorização por objeto e teste de rate limit.

**Em que se baseia.** O OWASP API Security Top 10, edição 2023 (https://owasp.org/API-Security/). Categorias cobertas com testes: API1 BOLA, API2 Broken Authentication, API3 Broken Object Property Level Authorization, API4 Unrestricted Resource Consumption, API5 BFLA e API8 Injection.

**Limites.** Para APIs suas ou que você tem autorização de testar. Os exemplos de código usam Prisma e TypeScript.

**Instalar.** `npx skills add alexbueno7/skills --skill api-security-audit` · [SKILL.md](skills/api-security-audit/SKILL.md)

### seo-optimization-suite

**O que faz.** Coordena uma passada completa de SEO e performance em um site em fases fixas: contexto, diagnóstico, indexação e DNS/SSL, performance e Core Web Vitals, imagens, metadata on-page, arquitetura do site, prontidão para busca por IA e verificação. Tem modos rápidos para só performance, só on-page, só busca por IA e pré-deploy.

**O que entrega.** Um relatório com notas antes e depois, a checklist de 16 itens, problemas corrigidos e problemas fora do escopo. Inclui dois scripts: execução padrão do Lighthouse e checagem HTTP de robots, sitemap, redirects, HTTPS e llms.txt.

**Em que se baseia.** Medição, não opinião: o Google Lighthouse CLI roda antes de qualquer correção e de novo depois, mobile primeiro, e o relatório mostra os dois. As regras de cada área vêm de skills especializadas que ela lê na hora (Core Web Vitals, PageSpeed, otimização de imagem, auditoria SEO, schema), listadas em `skills-registry.md`.

**Limites.** Precisa de Node.js e Chrome ou Chromium para o Lighthouse. As skills especializadas do registro são instaladas à parte; sem elas a cobertura é menor. O padrão é domínio apex como canônico, com www redirecionando para ele.

**Instalar.** `npx skills add alexbueno7/skills --skill seo-optimization-suite` · [SKILL.md](skills/seo-optimization-suite/SKILL.md)

### whatsapp-meta-api

**O que faz.** Dois papéis para a API oficial WhatsApp Business Cloud da Meta. Como referência, traz endpoints e payloads de texto, templates, mídia, botões e listas interativas, reações, webhooks, perfil comercial, gestão de número, grupos, Flows, chamadas e analytics. Como revisor, audita código de integração existente contra uma checklist e responde em formato fixo de achados.

**O que entrega.** Exemplos de requisição que funcionam, a estrutura de webhook com os eventos a assinar, tabela dos erros comuns da Meta com indicação de quando repetir, e a checklist de revisão.

**Em que se baseia.** A documentação oficial de desenvolvedores da Meta, com link por seção no fim da skill (visão geral, permissões, mensagens, templates, mídia, números, grupos, Flows, webhooks, Coexistence, códigos de erro, perfil comercial). Os exemplos usam a Graph API v25.0.

**Limites.** Os exemplos de código assumem Fastify, Prisma, TypeScript e Bun. A Meta muda essa API com frequência; confira a versão atual nos links.

**Instalar.** `npx skills add alexbueno7/skills --skill whatsapp-meta-api` · [SKILL.md](skills/whatsapp-meta-api/SKILL.md)

### whatsmiau

**O que faz.** Integra WhatsApp pela Whatsmiau, provedor compatível com Evolution: criar e conectar instâncias por QR code, enviar mensagens, ler conversas, configurar webhooks, gerenciar grupos e comunidades, e usar o servidor MCP do provedor.

**O que entrega.** O fluxo mínimo para conectar e enviar, um mapa rápido de endpoints, arquivos de referência completos de API, webhooks e MCP, e uma checklist de verificação.

**Em que se baseia.** A documentação oficial do provedor em https://whatsmiau.dev/docs, com cada seção da skill ligada à sua página, mais a lista de endpoints em `endpoints.json`.

**Limites.** Precisa de conta e chave de API da Whatsmiau. É uma rota não oficial do WhatsApp; para a API oficial da Meta use whatsapp-meta-api.

**Instalar.** `npx skills add alexbueno7/skills --skill whatsmiau` · [SKILL.md](skills/whatsmiau/SKILL.md)

### mailcheap-api

**O que faz.** Gerencia hospedagem de e-mail na Mailcheap pela API REST: domínios, caixas, aliases, DKIM, antispam, filtros Sieve e autoresponder. Cobre obter, usar e revogar o token, regras de senha e verificação de domínio.

**O que entrega.** Um padrão de cliente em TypeScript, as operações comuns com payloads, tratamento de erros, checklist de implementação e lista de armadilhas comuns.

**Em que se baseia.** A documentação oficial da API v1 da Mailcheap (https://www.mailcheap.co/help/hosted-email/api/v1/). O arquivo de referência informa que foi validado contra essa documentação em junho de 2026 e lista a página de cada endpoint.

**Limites.** Só roda quando você a chama pelo nome. Precisa do host e das credenciais da Mailcheap em variáveis de ambiente.

**Instalar.** `npx skills add alexbueno7/skills --skill mailcheap-api` · [SKILL.md](skills/mailcheap-api/SKILL.md)

### audaks-cloud

**O que faz.** Opera infraestrutura na Audaks Cloud, provedor brasileiro: máquinas virtuais (criar, ligar, desligar, resetar, trocar plano), block storage, snapshots e backups, redes, IPs, security groups, load balancers, DNS, monitoramento, billing, projetos e tickets de suporte.

**O que entrega.** Um pequeno script de shell (`audaks.sh`) para chamadas autenticadas e a referência completa de endpoints.

**Em que se baseia.** As definições de API do próprio provedor: a referência foi gerada dos arquivos Swagger da Audaks para compute e object storage, publicados em https://api.audaks.com.br/api/docs/alto e /ceph.

**Limites.** Só roda quando você a chama pelo nome. Precisa de token de API da Audaks. As ações nos servidores são reais; confirme o alvo antes de parar, resetar ou apagar.

**Instalar.** `npx skills add alexbueno7/skills --skill audaks-cloud` · [SKILL.md](skills/audaks-cloud/SKILL.md)

### focusnfe

**O que faz.** Integra a Focus NFe, provedor brasileiro de emissão de documentos fiscais eletrônicos: NFe, NFCe, NFSe municipal e nacional, CTe e MDFe, além de documentos recebidos, cadastro de empresas e webhooks. Explica homologação e produção, autenticação, a referência única por documento, quais operações respondem na hora e quais entram em fila, e o status do documento.

**O que entrega.** Um fluxo de implementação, lista de armadilhas conhecidas e arquivos de referência por tipo de documento, com payloads e catálogo de endpoints.

**Em que se baseia.** A documentação oficial da Focus NFe (https://doc.focusnfe.com.br/reference/introducao). O catálogo de endpoints foi extraído das definições OpenAPI embutidas nessas páginas em 17/09/2026, e a skill manda o agente ler o catálogo antes de supor qualquer caminho ou campo.

**Limites.** Só Brasil. Precisa de token da Focus NFe. Produção emite documento fiscal real; teste antes em homologação.

**Instalar.** `npx skills add alexbueno7/skills --skill focusnfe` · [SKILL.md](skills/focusnfe/SKILL.md)

### notas-fiscais-brasil

**O que faz.** Revisa ou implementa a emissão de notas fiscais brasileiras (NFS-e, NF-e, NFC-e) em um sistema. Delimita a operação e suas fontes, monta uma matriz fiscal verificável, confronta regra, código e payload, valida o ciclo de vida da integração (envio, timeout, repetição, cancelamento) e testa em proporção à mudança.

**O que entrega.** Um relatório com as regras confirmadas e suas fontes, pendências fiscais, achados ou arquivos alterados e checks executados.

**Em que se baseia.** Legislação brasileira citada por artigo: LC 116/2003 (arts. 3º, 4º e 6º) para ISS, Lei 10.833/2003 (arts. 30 e 31) para CSRF, Decreto 9.580/2018 (art. 714) para IRRF em serviços profissionais, IN RFB 1.234/2012 para órgãos públicos e Lei 9.430/1996 (art. 67) para limites. A skill exige registrar fonte, versão, vigência e data de cada regra, e bloqueia conclusão quando a fonte não pôde ser lida.

**Limites.** Só Brasil. Não é consultoria fiscal nem jurídica: o contador confirma enquadramento e alíquotas. Aponta para uma skill complementar, retencoes-tributarias-tomador, que não está neste repositório (deriva de asv-digital/skills-contadores).

**Instalar.** `npx skills add alexbueno7/skills --skill notas-fiscais-brasil` · [SKILL.md](skills/notas-fiscais-brasil/SKILL.md)

## Licença

[MIT](LICENSE). Livre para usar, alterar e compartilhar.
