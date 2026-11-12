# Skills Registry — SEO Optimization Suite

Referência de todas as skills disponíveis para orquestração. Paths absolutos para Read tool.

## Ferramenta CLI (Tier 0 — sempre usar)

| Ferramenta | Path | Uso |
|------------|------|-----|
| Lighthouse audit | `scripts/lighthouse-audit.sh` | Baseline Fase 1 + verificação Fase 6 |
| Ensure install | `scripts/ensure-lighthouse.sh` | `npm install -g lighthouse` se ausente |
| Technical SEO HTTP | `scripts/technical-seo-check.sh` | robots, sitemap, www→apex, https, llms.txt, openapi |
| Checklist full-audit | `references/full-audit-checklist.md` | 16 itens + Agente vs Humano |

Instalação global: `npm install -g lighthouse@latest` (requer Chrome/Chromium).

## Tier 1 — Performance & PageSpeed (novas)

| Skill | Path | Installs | Trigger terms |
|-------|------|----------|---------------|
| pagespeed-insights | `../pagespeed-insights/SKILL.md` | 533 | PageSpeed, Lighthouse, PSI scores |
| core-web-vitals | `../core-web-vitals/SKILL.md` | 7.7K | LCP, INP, CLS, CWV |
| performance | `../performance/SKILL.md` | 13.7K | load time, TTFB, budget |
| image-optimization | `../image-optimization/SKILL.md` | 798 | WebP, hero, lazy load, alt |

## Tier 2 — SEO tradicional

| Skill | Path | Trigger terms |
|-------|------|---------------|
| seo-audit | `../seo-audit/SKILL.md` | audit, ranking, indexação |
| schema-markup | `../schema-markup/SKILL.md` | JSON-LD, rich snippets |
| fixing-metadata | `../fixing-metadata/SKILL.md` | title, OG, canonical |
| site-architecture | `../site-architecture/SKILL.md` | IA, URLs, nav, pilares, profundidade |
| programmatic-seo | `../programmatic-seo/SKILL.md` | páginas em escala |
| cloudflare-manager | `~/.claude/skills/cloudflare-manager/SKILL.md` | DNS, SSL, redirect www/apex |

## Tier 3 — GEO / AI Search

| Skill | Path | Trigger terms |
|-------|------|---------------|
| geo | `~/.claude/skills/geo/SKILL.md` | GEO audit completo |
| geo-technical | `~/.claude/skills/geo-technical/SKILL.md` | crawl, SSR, security |
| ai-seo | `../ai-seo/SKILL.md` | AEO, LLM citations |
| geo-crawlers | `~/.claude/skills/geo-crawlers/SKILL.md` | robots.txt AI bots |
| geo-schema | `~/.claude/skills/geo-schema/SKILL.md` | schema para AI |
| geo-content | `~/.claude/skills/geo-content/SKILL.md` | E-E-A-T, citability |
| geo-citability | `~/.claude/skills/geo-citability/SKILL.md` | score citabilidade |
| geo-llmstxt | `~/.claude/skills/geo-llmstxt/SKILL.md` | llms.txt, openapi.json |

## Tier 4 — Qualidade complementar

| Skill | Path | Trigger terms |
|-------|------|---------------|
| fixing-accessibility | `../fixing-accessibility/SKILL.md` | a11y, PSI Accessibility |
| fixing-motion-performance | `../fixing-motion-performance/SKILL.md` | animações, jank |
| analytics-tracking | `../analytics-tracking/SKILL.md` | GA4, conversão |

## Tier 5 — Meta / utilitários

| Skill | Path | Trigger terms |
|-------|------|---------------|
| find-skills | `../find-skills/SKILL.md` | buscar skill nova |
| karpathy-guidelines | `../karpathy-guidelines/SKILL.md` | simplicidade, diffs |

## Ordem de leitura por cenário

### PageSpeed 64, LCP 9.9s (caso REFORMAX)
1. pagespeed-insights → core-web-vitals → performance → image-optimization → fixing-metadata

### SEO audit completo (full-audit)
1. technical-seo-check.sh + checklist → seo-audit → site-architecture → cloudflare-manager (se token) → geo-technical → performance → fixing-metadata → schema-markup → geo-llmstxt → ai-seo
2. Relatório: tabela PASS/FAIL/HUMAN/N/A dos 16 itens. GSC/Bing/backlinks sem evidência = HUMAN.

### Deploy produção
1. performance → image-optimization → fixing-metadata → schema-markup
