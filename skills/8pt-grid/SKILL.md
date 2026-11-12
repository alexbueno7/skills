---
name: 8pt-grid
description: "8-point grid system for UI. Use when creating, adjusting or reviewing layout, spacing, padding, margin, gap, component or icon size, or line-height in any interface (web, app, dashboard), or when the user mentions 8pt grid, 8 point grid, consistent spacing, vertical rhythm, spacing scale, spacing tokens, a cluttered interface or grouping elements. PT-BR: Sistema de grid de 8 pontos para UI. Use ao criar, ajustar ou revisar layout, espaçamento, padding, margin, gap, tamanho de componente ou ícone e line-height, ou quando o usuário citar \"grid de 8\", \"espaçamento consistente\", \"ritmo vertical\", \"tokens de espaçamento\", \"interface poluída\" ou \"agrupar elementos\"."
---

# Grid de 8 pontos

Fontes:
- https://uxplanet.org/everything-you-should-know-about-8-point-grid-system-in-ux-design-b69cb945b18d (Ashphiar Raihan Rumman, UX Planet, 2022).
- https://x.com/magdiel_rb/status/2120589656215495103 (Magdiel Silva, thread, 2026): escala por papel, proximidade, tokens.

## Regra central

Dimensões, padding, margin e gap em múltiplos de 8: 8, 16, 24, 32, 40, 48, 56, 64...
Meio passo de 4 só quando precisar apertar (ícone + texto, chips, densidade alta).

Motivo: a maioria das telas é divisível por 8, escala limpo em @1x/@2x/@3x (projete em @1x), menos decisões, ritmo consistente, e o desenvolvedor reconhece o incremento sem medir.

## Escala por papel

Cada passo tem uma função; escolha pelo papel, não pelo olho.

| Valor | Papel |
|---|---|
| 4 | ajuste fino (ícone + texto) |
| 8 | pequeno: label e seu input, título e descrição |
| 16 | entre elementos relacionados |
| 24 | entre grupos |
| 32 | entre blocos maiores |
| 48 | entre seções |
| 64 | respiro entre áreas importantes |

O objetivo não é 8px em tudo: é criar relações proporcionais entre os elementos.

## Proximidade (Gestalt)

Distância é informação: perto = relacionado, longe = outro grupo.

- Dentro do grupo, passo pequeno; entre grupos, passo claramente maior. Formulário: 8 entre label e input, 24 entre conjuntos de campos. Card: 8 entre título e descrição, 24 até o botão, 24 de padding.
- O que comunica é o **contraste** entre as distâncias, não o valor absoluto. Quanto maior a razão entre/dentro, mais claro o grupo: mire em 2x ou mais (8 e 16, 8 e 24, 16 e 32). Passos vizinhos no alto da escala (24 e 32 = 1,33x) quase não separam.
- Agrupe pela distância antes de recorrer a borda ou divisória.
- Tela poluída com poucos elementos: confira primeiro se as distâncias são uniformes ou ambíguas (espaço dentro do grupo igual ou maior que o de fora). Sem diferença, nada agrupa.

## Valores de partida por componente

- **Cards e containers**: padding 16, 24 ou 32, conforme a densidade do conteúdo.
- **Layout**: gap de 16 ou 24 entre cards; margem externa de 32 ou 48 no desktop.
- **Botões e inputs**: altura 32, 40 ou 48.
- **Modais e painéis**: padding 24 ou 32; distâncias previsíveis entre cabeçalho, conteúdo e ações.
- **Responsivo**: mesma escala no mobile e no desktop; muda o token usado, não a escala.

## Como aplicar

- **Soft grid, não hard grid**: meça o espaço *entre* elementos em múltiplos de 8; não encaixe tudo numa grade fixa do documento. É o que o código faz (padding/margin/gap).
- **Espaçamento como variáveis/tokens**, nunca valor solto. Use a escala do projeto se já existir; se não existir, crie antes de espaçar componentes:

  ```css
  :root {
    --space-1: 4px;
    --space-2: 8px;
    --space-3: 16px;
    --space-4: 24px;
    --space-5: 32px;
    --space-6: 48px;
    --space-7: 64px;
  }
  ```

  Ao gerar código, não invente valor (`margin: 13px`, `gap: 19px`, `padding: 27px`): todo espaçamento sai de um token.
- **Horizontal**: 12 colunas, gutter 24px (1.5rem). Em artboard de 1440px, margem de 60px por lado no container.
- **Vertical**: ritmo de 8px; alturas de botão, input, card e linha de tabela em múltiplos de 8.
- **Ícones**: SVG, em 16, 24, 32, 40.
- **Tipografia**: o tamanho da fonte pode variar (14, 15, 21...); o **line-height não**: múltiplo de 8, ou de 4 para controle mais fino (4, 8, 12, 16, 20, 24...).
- **Exceção**: não é dogma, é ferramenta de consistência. Tamanho de fonte, bordas (1px), alinhamento óptico e elementos muito pequenos podem sair da escala. Se o componente fora do múltiplo de 8 fica melhor, quebre a regra de propósito, não por descuido.

## Tailwind (nota prática, fora do artigo)

Unidade padrão = 4px, então passos pares estão no grid: `2`=8, `4`=16, `6`=24, `8`=32, `10`=40, `12`=48. Ímpares (`1`, `3`, `5`) são o meio passo de 4. Evite valores arbitrários (`p-[13px]`).

## Revisão rápida

1. Algum padding/margin/gap fora de múltiplo de 4? Corrija ou justifique.
2. Line-height em múltiplo de 4?
3. Ícones em 16/24/32/40?
4. Espaçamento vem de token/escala, não de número mágico?
5. Distância dentro do grupo é visivelmente menor que entre grupos?
6. Alguma borda ou divisória que só a distância já resolveria?
