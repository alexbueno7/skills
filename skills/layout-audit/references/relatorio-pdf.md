# Relatório e PDF portável

## Conteúdo obrigatório

1. Capa: site, URL, ambiente, versão quando conhecida e data de coleta.
2. Resumo executivo: diagnóstico, tarefas prioritárias e o que preservar.
3. Escopo: URLs únicas, modelos/amostras, exclusões e bloqueios.
4. Negócio: oferta, jornada, custos, limites e evidências de clientes com origem/data.
5. Pesquisa: fontes recentes, método/população, achado, aplicação e limites.
6. Direção: produto, caráter, mundo visual, momentos e assinatura da marca.
7. Padrões comuns: tipografia, cor, espaçamento, imagens, navegação e estados.
8. Ficha por página/modelo: como está, problema, proposta, risco e aceite.
9. Plano: prioridades, dependências, fontes/componentes e ordem de execução.
10. QA: UX/DX/AX, SEO, desempenho e regressão funcional.
11. Limitações e bibliografia com URLs clicáveis.

## Ficha de página

Usar URL e propósito como título, não nome genérico como “página 3”.
Captura deve mostrar o trecho que sustenta o achado, com viewport e data.
Para página longa, usar recortes legíveis; evitar reduzir 10 telas a uma miniatura.

Separar explicitamente:
- **Observado:** texto, layout ou comportamento visto, com evidência.
- **Problema:** consequência demonstrada ou risco identificado.
- **Hipótese:** benefício esperado, ainda não medido.
- **Proposta:** estrutura e copy sugeridas; fatos comerciais continuam sujeitos à fonte.
- **Aceite:** cenário reproduzível que confirma a correção sem regressão.

Representação do “como ficaria” pode ser ordem de blocos, copy exemplificada ou
wireframe rotulado. Não gerar antes/depois enganoso. Sem mockup, escrever
“proposta textual, não renderizada”. Ilustrações não substituem capturas atuais.

## Geração adaptável

Detectar motor já disponível: impressão PDF do navegador, Playwright + Chromium,
Chrome headless ou ferramenta de documentos do host. Não fixar caminhos de uma
máquina nem depender de servidor permanente. Resolver imagens antes de imprimir.

Com Playwright disponível no runtime, adaptar este trecho ao módulo instalado:

```js
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const missing = await page.evaluate(() =>
    [...document.images].filter(i => !i.complete || !i.naturalWidth).length);
  if (missing) throw new Error(`${missing} imagens ausentes`);
  await page.pdf({ path: pdfPath, format: 'A4', printBackground: true,
    preferCSSPageSize: true });
} finally {
  await browser.close();
}
```

`htmlPath` e `pdfPath` são caminhos absolutos escolhidos para esta execução.
Se Chromium instalado pelo sistema, informar seu `executablePath` detectado.
Não desativar sandbox automaticamente; respeitar ambiente e permissões.

## HTML e impressão

- Documento UTF-8, `lang="pt-BR"`, título informativo e texto selecionável.
- Incorporar capturas como data URIs ou fornecer pasta de assets permanente junto.
- Escapar HTML de títulos, textos e URLs recuperados. Não executar scripts do site
  auditado dentro do relatório. Validar protocolos dos links (http/https).
- CSS de impressão A4 com margens, fonte legível, cabeçalhos e paginação quando suportados.
- Evitar quebra dentro de pequenos cards/tabelas; permitir parágrafos longos paginarem.
- `max-width:100%` nas imagens; proporção preservada; legenda fora da imagem.
- Cores com contraste e sem fundos pesados que dificultem impressão.
- Salvar PDF e HTML em pasta com slug/data; não sobrescrever auditoria anterior.

## Inspeção final

Se disponíveis, `pdfinfo` verifica tamanho/páginas; `pdftotext` verifica texto e acentos;
`pdftoppm` permite inspecionar páginas reais renderizadas. Contagem de imagens no HTML
não comprova paginação correta no PDF.

Validar amostras do começo, meio e fim, incluindo a página de maior densidade.
Procurar cortes, folhas vazias acidentais, capturas ilegíveis e fontes ausentes.
Confirmar que a contagem de fichas corresponde ao inventário deduplicado.

## Ausências e falhas

Sem pesquisa: não apresentar conhecimento de memória como literatura recente.
Sem browser: screenshots do usuário podem sustentar análise estática, não interação.
Sem dados de clientes: completar avaliação visual e deixar hipóteses explícitas.
Sem PDF: entregar HTML imprimível, indicar bloqueio e não chamar HTML de PDF.
Uma página inacessível não invalida as outras; registrar motivo e continuar cobertura.
