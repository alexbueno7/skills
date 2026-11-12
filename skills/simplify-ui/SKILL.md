---
name: simplify-ui
description: "Simplifies interfaces to the bar of Linear's website or Apple Notes: simple purpose, architecture, design and implementation; cuts taglines, supporting text and secondary labels, and fixes the layout when the screen depended on them. Use when creating, reviewing, simplifying or standardizing UI, pages, components, copy, navigation or flows, even if the user only says \"simplify\", \"clean this up\" or \"make it like the home page\". For a full audit with PDF use layout-audit; for code-only simplification use simplify. PT-BR: Simplifica interfaces no padrão do site da Linear ou do Apple Notes: corta taglines, texto de apoio e rótulos secundários e corrige o layout quando a tela dependia deles. Use ao criar, revisar, simplificar ou padronizar telas, páginas, componentes, copy, navegação ou fluxos, mesmo que o pedido seja só \"simplifica\", \"limpa isso\" ou \"deixa como a home\"."
---

# Simples perfeito

## Briefing

Aplicar integralmente, como critério de decisão:

> I want this to be as perfect as Linear's website or Apple Notes: simple purpose,
> simple architecture, simple design, simple implementation. Cut taglines, helper
> text and secondary labels. If a screen needs them to make sense, fix the layout.
> Every decision should elevate the user experience (UX), developer experience (DX)
> and agent experience (AX) at once, without breaking anything.

Origem: o estilo e os layouts das páginas de marketing da Apple. Simplicidade aqui é
clareza de propósito, não minimalismo decorativo. O que se copia de Apple e Linear é a
disciplina de corte, não a aparência.

## Defaults

| Entrada | Padrão quando omitida |
|---|---|
| Escopo | Tela, componente ou fluxo citado; sem ampliar para redesign geral |
| Referência | Página ou componente já aprovado no projeto; sem referência, derivar do propósito |
| Conteúdo | Preservar fatos, preços, prazos, limites, URLs, rastreio, contratos e texto legal |
| Verificação | Checks proporcionais: tipos, testes afetados, build e navegação real quando houver UI |
| Entrega | Mudanças aplicadas no repositório atual; sem commit, push ou deploy sem autorização |
| Idioma | pt-BR, salvo instrução superior do ambiente |

## 1. Nomear o propósito

Escrever em uma frase o que a tela permite fazer ou entender. Se não couber em uma
frase, a tela tem mais de um propósito; dividir, agrupar ou remover antes de
estilizar. O título principal nomeia esse propósito em linguagem do usuário, não
slogan, não nome de mecanismo interno, não explicação sobre como a página foi gerada.

## 2. Separar corte de conteúdo de corte de ruído

Cortar quando repete, decora ou explica o óbvio:
- taglines, frases de efeito, rótulos acima do título, badges sem comprovação;
- texto de apoio que repete o título, ícones que não distinguem itens;
- seções que existem apenas porque o modelo da página tinha o espaço;
- promessas de resultado não verificáveis e comparações vagas.

Preservar quando a decisão depende disso:
- rótulos de campos, validações, erros, consentimentos e instruções críticas;
- preços, custos iniciais, limites, prazos, taxas de terceiros e condições;
- diferenças reais entre planos, opções ou caminhos;
- conteúdo que responde à intenção de busca de páginas públicas.

Se uma tela só faz sentido com texto auxiliar, o problema é o layout: reorganizar
hierarquia, ordem, agrupamento ou nome das ações até o texto ficar dispensável.

## 3. Arquitetura simples

Reusar fonte de dados, componentes, tokens e padrões existentes antes de criar
qualquer coisa. Uma verdade por fato: preço, FAQ, nome e condições vêm da mesma fonte
que alimenta as outras páginas e o schema. Sem abstração nova para um único uso, sem
duplicar classes de botão, sem página paralela quando a existente pode ganhar a
opção. Mudança em componente compartilhado precisa listar quem a herda.

## 4. Design simples

Mesma escala tipográfica, largura, espaçamento e botões da referência aprovada.
Título em poucas linhas; texto de apoio abaixo dele, não deslocado para um canto;
uma ação principal e no máximo uma secundária; listas com a mesma largura das
perguntas ou cabeçalhos que acompanham. Sem faixas decorativas, destaques de cor
arbitrários, sombras coloridas, movimento sem função ou grades de cartões iguais
para conteúdos diferentes. Mobile e desktop são a mesma decisão vista em dois tamanhos.

## 5. UX, DX e AX ao mesmo tempo

Antes de aplicar, responder para cada mudança:
- **UX:** a pessoa entende mais rápido o que é, quanto custa e o que fazer?
- **DX:** há menos código, menos duplicação, menos casos especiais e testes claros?
- **AX:** HTML semântico, nomes acessíveis, títulos únicos, links previsíveis,
  metadados e dados estruturados coerentes com o visível, sem texto oculto?

Se uma dimensão piora, não é simplificação; procurar outra solução ou explicar o
trade-off ao usuário antes de seguir.

## 6. Sem quebrar nada

Preservar URLs, redirecionamentos, canonical, rastreio, eventos, formulários,
destinos de contratação e contratos de componentes. Props removidas exigem conferir
todos os chamadores e testes que as simulam. Confirmar no navegador o fluxo real
quando a mudança for de UI: títulos, menus, foco, Escape, formulários sem envio real,
estados vazio/erro, desktop e mobile. Não declarar testado o que não foi executado.

## 7. Entregar

Começar pelo resultado: o que mudou, onde ver, o que foi verificado e o que ficou
pendente ou depende de decisão comercial. Separar fato de hipótese. Não transformar
estratégia interna (SEO, geração dinâmica, arquitetura) em texto para o visitante.
