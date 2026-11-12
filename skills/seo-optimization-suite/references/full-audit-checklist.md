# Checklist full-audit — o que o agente deve validar

Lista canônica. No modo `full-audit`, **cada item** sai PASS / FAIL / HUMAN no relatório. Não pular item.

Legenda:
- **Agente**: dá para checar ou corrigir no código/HTTP nesta sessão
- **Humano**: exige conta, painel ou ferramenta paga; o agente pergunta e registra, não inventa PASS

---

## 1. sitemap.xml submitted and cleaned up

**Agente**
- GET `/sitemap.xml` e `/sitemap_index.xml` — 200, XML válido, só URLs canônicas 200/indexáveis
- `robots.txt` contém `Sitemap: https://...`
- Remover do sitemap: noindex, 404, redirect, parâmetros lixo, rascunho
- Rodar: `scripts/technical-seo-check.sh <URL>`

**Humano**
- Search Console → Sitemaps → submetido, 0 erros, última leitura recente
- Sem PASS de "submitted" sem o usuário confirmar (ou API GSC autenticada)

## 2. robots.txt configured

**Agente**
- GET `/robots.txt` 200
- Não bloquear `/`, CSS, JS, imagens do LCP
- Permitir Googlebot, Bingbot e bots de IA conforme `geo-crawlers`
- Sitemap apontado

Skill: `seo-audit`, `geo-crawlers`

## 3. Google Search Console + Bing Webmaster connected

**Humano (obrigatório registrar)**
- GSC: propriedade no host canônico (apex ou www, o que o 301 escolheu), verificação OK
- Bing Webmaster: site adicionado (Copilot/ChatGPT usam índice Bing)
- Sitemap submetido nos dois

O agente **não** conecta OAuth. Perguntar. Se não tiver acesso: FAIL + instrução, não omitir.

## 4. Meta titles and descriptions

**Agente** — skill `fixing-metadata`
- Title único, ~50–60 caracteres
- Description única, ~150–160
- Home + páginas críticas (não só a URL do Lighthouse)

## 5. Canonical issues fixed

**Agente** — `fixing-metadata`
- Cada página indexável: canonical absoluta, self-ref
- Canonical = host canônico (mesmo do 301)
- Sem canonical cruzado para home em páginas profundas

## 6. Duplicate/redirect issues cleaned up

**Agente**
- Cadeias: A→B→C vira A→C
- Loops: FAIL
- HTTP→HTTPS 301
- Trailing slash consistente
- Conteúdo duplicado: canonical ou 301, não dois 200

Crawler completo (Screaming Frog) se o usuário fornecer export; senão amostrar home, 5 internas, www/apex, http.

## 7. www → non-www 301 redirect fixed

Padrão desta skill: **apex canônico** (`https://dominio.com.br`), www 301 para apex — a menos que o projeto já tenha apex→www documentado.

**Agente**
```bash
curl -sI https://www.dominio.com.br | grep -iE 'HTTP/|location:'
curl -sI https://dominio.com.br | grep -iE 'HTTP/|location:'
```
- Host não-canônico: 301 para o canônico (um hop)
- Canônico: 200, não 301 para si mesmo

Correção: Cloudflare Page Rule / Redirect Rule, ou nginx `return 301`. Ver item 8.

## 8. Cloudflare DNS / SSL issue resolved

**Agente**
- HTTPS 200 no canônico, certificado válido (não interstitial Lighthouse)
- Sem mixed content nas páginas críticas
- DNS: A/AAAA ou CNAME corretos; www e apex resolvem
- SSL/TLS Cloudflare: Full (strict) se origem tem cert válido

Skill: `cloudflare-manager` se `CLOUDFLARE_API_KEY` existir.

**Humano** se não houver token: capturar no dashboard (DNS, SSL/TLS, Redirects) e colar evidência.

## 9. Internal links cleaned up

**Agente** — `site-architecture`, `seo-audit`
- Âncora descritiva, sem "clique aqui"
- Sem órfãs nas páginas-pilar
- Sem 404 internos nas páginas críticas
- Footer/sidebar não substituem links no corpo

## 10. Structured data / JSON-LD added

**Agente** — `schema-markup` (SSR/Blade, não só JS)
- Home: `Organization` + `WebSite`
- Demais: tipo da página (Product, Article, LocalBusiness, FAQ, BreadcrumbList)
- Validar no browser: `document.querySelectorAll('script[type="application/ld+json"]')`
- Rich Results Test — não usar só curl

## 11. Page speed + Core Web Vitals optimized

**Agente** — Lighthouse CLI Fase 1 e 6 + `core-web-vitals` + `performance` + `image-optimization`
- LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 (alvo "Good")
- Performance mobile < 50: bloquear deploy

## 12. llms.txt + openapi.json added

**Agente**
- GET `/llms.txt` 200, markdown curto: o que é, para quem, links das páginas-pilar + pricing
- GET `/openapi.json` **ou** `/openapi.yaml` 200 se o produto tem API pública; se não tem API, marcar N/A (não FAIL)
- Referenciar `llms.txt` no `robots.txt` (comentário) e, se existir, no sitemap

Skills: `ai-seo`, `geo-llmstxt`

`openapi.json` descreve a API para agentes. Não confundir com JSON-LD.

## 13. Pillar pages + content clusters

**Agente** — `site-architecture`
- Cada tema de negócio: 1 pilar (guia amplo) + 3+ satélites que linkam o pilar e recebem link do pilar
- Sem canibalização (dois URLs para a mesma intenção)
- Mapear no relatório: pilar → slugs do cluster

Não é "ter um blog". É grafo de tópicos.

## 14. Crawl depth under 4 + thin content check

**Agente**
- Página importante a no máximo **3 cliques** da home (profundidade de crawl < 4)
- Thin: tag/arquivo/paginação sem conteúdo único, doorway, duplicata near-duplicate
- Locale só com chrome traduzido = thin

## 15. Entity optimization

**Agente**
- Nome da marca/empresa consistente (title, H1, schema `name`, footer)
- `Organization.sameAs` = perfis oficiais reais
- NAP local se LocalBusiness (mesmo texto do GBP)
- Entidade ≠ keyword stuffing. Uma entidade principal por site.

## 16. Quality backlinks

**Humano + ferramenta** (Ahrefs/Semrush/GSC Links)
- O agente **não** compra link e **não** inventa DR/DA
- Se houver export: spam, PBN, irrelevante = desavow candidato
- Se não houver ferramenta: GSC → Links (top sites) + pedir ao usuário; senão FAIL/HUMAN

Qualidade > volume. 3 links editoriais no nicho valem mais que 300 diretórios.

---

## Script de checagem HTTP

```bash
scripts/technical-seo-check.sh https://dominio.com.br
```

Cobre itens 1–2, 7 (host), 12 (arquivos). Não substitui GSC, Bing, backlinks nem Lighthouse.
