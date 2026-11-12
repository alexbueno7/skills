# Agent Skills

Skills for coding agents (Claude Code, Codex, Cursor, Pi and others), installable with [`npx skills`](https://skills.sh/). Each one below says what it does, what you get and what it is based on.

Português: [README.pt-BR.md](README.pt-BR.md)

Skill names and descriptions are in English and Portuguese. The instructions inside each skill are written in Brazilian Portuguese; agents follow them whatever language you write in.

## Install

Requires Node.js. Run inside your project, or add `-g` to install for every project.

```bash
# Install everything
npx skills add alexbueno7/skills

# One skill
npx skills add alexbueno7/skills --skill simplify-ui

# Global, for every project
npx skills add alexbueno7/skills --skill simplify-ui -g

# For one agent only
npx skills add alexbueno7/skills --skill simplify-ui --agent claude-code

# Update
npx skills update

# Remove
npx skills remove simplify-ui
```

Without the CLI: copy the folder `skills/<name>` into `.claude/skills/` (project) or `~/.claude/skills/` (global), or the equivalent folder of your agent, then start a new session.

## Skills

**UI and product**: [`simplify-ui`](#simplify-ui), [`8pt-grid`](#8pt-grid), [`layout-audit`](#layout-audit)

**Workflow**: [`prompt-brief`](#prompt-brief), [`api-security-audit`](#api-security-audit), [`seo-optimization-suite`](#seo-optimization-suite)

**Integrations**: [`whatsapp-meta-api`](#whatsapp-meta-api), [`whatsmiau`](#whatsmiau), [`mailcheap-api`](#mailcheap-api), [`audaks-cloud`](#audaks-cloud)

**Brazil only**: [`focusnfe`](#focusnfe), [`notas-fiscais-brasil`](#notas-fiscais-brasil)

### simplify-ui

**What it does.** Reviews a screen, page, component or flow and removes what does not help the visitor decide: taglines, supporting text and secondary labels. When a screen stops making sense without that text, the skill fixes the layout instead of putting the text back. It works in seven steps: name the purpose, separate content from noise, simplify the architecture, simplify the design, check user, developer and agent experience together, confirm nothing broke, deliver.

**What you get.** The change applied in your repository, with a short report: what changed, where to see it, what was verified and what depends on a business decision.

**What it is based on.** The style and layouts Apple uses in its marketing pages, which the author took as the model, condensed into one design brief quoted in full inside the skill: "as perfect as Linear's website or Apple Notes: simple purpose, simple architecture, simple design, simple implementation". In practice that means a title in a few lines, one main action and at most one secondary, the same type scale and spacing across pages, and no decorative bands, arbitrary color highlights or motion without a function. What is copied from Apple and Linear is the discipline of cutting, not the appearance. It cites no study; it is an opinionated working rule.

**Limits.** Keeps facts, prices, deadlines, URLs, tracking, contracts and legal text. Does not commit, push or deploy without permission.

**Install.** `npx skills add alexbueno7/skills --skill simplify-ui` · [SKILL.md](skills/simplify-ui/SKILL.md)

### 8pt-grid

**What it does.** Gives the agent one spacing rule for any interface: every margin, padding, gap and component size is a multiple of 8, with 4 for finer control. It defines a scale by role (inside a component, between related items, between groups, between sections), starting values for common components and a quick review checklist.

**What you get.** Layouts whose spacing follows one scale, and a list of the values that broke it when reviewing existing UI.

**What it is based on.** Two sources named in the skill: the article "Everything you should know about 8 point grid system in UX design" (Ashphiar Raihan Rumman, UX Planet, 2022) and a 2026 thread by Magdiel Silva on scale by role, proximity and tokens. Grouping follows the Gestalt principle of proximity: items that belong together sit closer than items that do not.

**Limits.** A consistency tool, not dogma: font size, 1px borders, optical alignment and very small elements may leave the scale.

**Install.** `npx skills add alexbueno7/skills --skill 8pt-grid` · [SKILL.md](skills/8pt-grid/SKILL.md)

### layout-audit

**What it does.** Audits a website page by page before a redesign. It first learns the business and the offer, then searches recent UX and marketing literature for the real problem found, then inspects the live pages at phone, tablet and desktop widths, and finally writes a plan for each page or page family.

**What you get.** An illustrated PDF (and portable HTML) with evidence, screenshots, dated sources and a phased plan. It never edits the site.

**What it is based on.** The same simplicity brief as simplify-ui, plus a research method instead of a fixed reading list: each run searches sources published in the last three years and records author, date, method, population and limits for every one. It separates empirical research from professional guidance and from opinion, and does not transfer a result to a context it was not measured in (a checkout study does not prove an effect on a B2B landing page). Pages are measured at 375/390, 768/1024 and 1440 px.

**Limits.** Calls the skills unslop, ui-ux-pro-max and seo-optimization-suite; install them for the full audit. Needs a browser tool for screenshots; without one it reports a partial analysis. Skips logged-in areas, checkout and admin panels unless asked.

**Install.** `npx skills add alexbueno7/skills --skill layout-audit` · [SKILL.md](skills/layout-audit/SKILL.md)

### prompt-brief

**What it does.** Takes a short, informal task description and returns a complete prompt ready to paste into a coding agent that has no context. It first checks three things (what to change, the expected result, how to verify it is done) and asks up to three short questions only about what is missing.

**What you get.** One code block with the brief in eight XML sections: context, goal, done_when, boundaries, autonomy, proof, report, memory.

**What it is based on.** Written to get the most out of Claude Fable 5.2, following Anthropic's official guide [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices): be clear and direct, add context so the model knows the goal behind an instruction, and structure the prompt with XML tags, which the guide says help Claude parse prompts that mix instructions, context and inputs. See also [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2). Each section answers a question an agent otherwise has to guess: what is true now, what done means, what it must not touch, how far it may go alone, and what evidence to bring back. The same guide applies to the other current Claude models.

**Limits.** It writes the prompt and does not execute the task. It does not invent facts, file paths or causes; guesses are marked as hypotheses.

**Install.** `npx skills add alexbueno7/skills --skill prompt-brief` · [SKILL.md](skills/prompt-brief/SKILL.md)

### api-security-audit

**What it does.** Runs a security audit of a REST API in three phases: reconnaissance, vulnerability analysis by category, and report. For each category it gives the test to run with curl, what a vulnerable response looks like, and the fix.

**What you get.** A findings report from the included template, with severity, reproduction steps and fix for each issue, plus three helper scripts: endpoint scan, object-level authorization test and rate-limit test.

**What it is based on.** The OWASP API Security Top 10, 2023 edition (https://owasp.org/API-Security/). Categories covered with tests: API1 BOLA, API2 Broken Authentication, API3 Broken Object Property Level Authorization, API4 Unrestricted Resource Consumption, API5 BFLA and API8 Injection.

**Limits.** For APIs you own or are authorized to test. Code examples use Prisma and TypeScript.

**Install.** `npx skills add alexbueno7/skills --skill api-security-audit` · [SKILL.md](skills/api-security-audit/SKILL.md)

### seo-optimization-suite

**What it does.** Coordinates a full SEO and performance pass on a site in fixed phases: context, diagnosis, indexing and DNS/SSL, performance and Core Web Vitals, images, on-page metadata, site architecture, AI search readiness, then verification. It has quick modes for performance only, on-page only, AI search only and pre-deploy.

**What you get.** A report with scores before and after, the 16-item checklist, issues fixed and issues left out of scope. Includes two scripts: a standard Lighthouse run and an HTTP check of robots, sitemap, redirects, HTTPS and llms.txt.

**What it is based on.** Measurement, not opinion: Google Lighthouse CLI runs before any fix and again after, mobile first, and the report shows both. The rules for each area come from specialized skills it reads at run time (Core Web Vitals, PageSpeed, image optimization, SEO audit, schema markup), listed in `skills-registry.md`.

**Limits.** Needs Node.js and Chrome or Chromium for Lighthouse. The specialized skills in the registry are installed separately; without them it covers less. Default is apex domain as canonical with www redirecting to it.

**Install.** `npx skills add alexbueno7/skills --skill seo-optimization-suite` · [SKILL.md](skills/seo-optimization-suite/SKILL.md)

### whatsapp-meta-api

**What it does.** Two jobs for Meta's official WhatsApp Business Cloud API. As a reference, it gives the endpoints and payloads for text, templates, media, interactive buttons and lists, reactions, webhooks, business profile, number management, groups, Flows, calling and analytics. As a reviewer, it audits existing integration code against a checklist and answers in a fixed findings format.

**What you get.** Working request examples, the webhook structure with the events to subscribe to, a table of common Meta error codes with whether to retry, and a review checklist.

**What it is based on.** Meta's official developer documentation, linked section by section at the end of the skill (overview, permissions, messages, templates, media, phone numbers, groups, Flows, webhooks, Coexistence, error codes, business profile). Examples target Graph API v25.0.

**Limits.** Code examples assume Fastify, Prisma, TypeScript and Bun. Meta changes this API often; check the linked docs for the current version.

**Install.** `npx skills add alexbueno7/skills --skill whatsapp-meta-api` · [SKILL.md](skills/whatsapp-meta-api/SKILL.md)

### whatsmiau

**What it does.** Integrates WhatsApp through Whatsmiau, an Evolution-compatible provider: creating and connecting instances by QR code, sending messages, reading chats, configuring webhooks, managing groups and communities, and using the provider's MCP server.

**What you get.** The minimal flow to connect and send, a quick endpoint map, full reference files for the API, webhooks and MCP, and a verification checklist.

**What it is based on.** The provider's official documentation at https://whatsmiau.dev/docs, with each section of the skill linked to its page, plus a machine-readable endpoint list in `endpoints.json`.

**Limits.** Needs a Whatsmiau account and API key. This is an unofficial WhatsApp route; for Meta's official API use whatsapp-meta-api.

**Install.** `npx skills add alexbueno7/skills --skill whatsmiau` · [SKILL.md](skills/whatsmiau/SKILL.md)

### mailcheap-api

**What it does.** Manages email hosting on Mailcheap through its REST API: domains, mailboxes, aliases, DKIM, antispam, Sieve filters and autoresponders. It covers getting, using and revoking the token, password rules and domain verification.

**What you get.** A TypeScript client pattern, the common operations with payloads, error handling, an implementation checklist and a list of common pitfalls.

**What it is based on.** Mailcheap's official API v1 documentation (https://www.mailcheap.co/help/hosted-email/api/v1/). The reference file states it was validated against that documentation in June 2026 and lists the page of each endpoint.

**Limits.** Only runs when you call it by name. Needs your Mailcheap host and credentials in environment variables.

**Install.** `npx skills add alexbueno7/skills --skill mailcheap-api` · [SKILL.md](skills/mailcheap-api/SKILL.md)

### audaks-cloud

**What it does.** Operates infrastructure on Audaks Cloud, a Brazilian provider: virtual machines (create, start, stop, reset, change plan), block storage, snapshots and backups, networks, IPs, security groups, load balancers, DNS, monitoring, billing, projects and support tickets.

**What you get.** A small shell helper (`audaks.sh`) for authenticated calls and a full endpoint reference.

**What it is based on.** The provider's own API definitions: the reference was generated from Audaks' Swagger files for compute and object storage, published at https://api.audaks.com.br/api/docs/alto and /ceph.

**Limits.** Only runs when you call it by name. Needs an Audaks API token. Actions on servers are real; confirm the target before stopping, resetting or deleting.

**Install.** `npx skills add alexbueno7/skills --skill audaks-cloud` · [SKILL.md](skills/audaks-cloud/SKILL.md)

### focusnfe

**What it does.** Integrates Focus NFe, a Brazilian provider for issuing electronic tax documents: NFe, NFCe, municipal and national NFSe, CTe and MDFe, plus received documents, company registration and webhooks. It explains test versus production, authentication, the unique reference per document, which operations answer immediately and which are queued, and document status.

**What you get.** An implementation flow, a list of known pitfalls, and reference files by document type with payloads and an endpoint catalog.

**What it is based on.** Focus NFe's official documentation (https://doc.focusnfe.com.br/reference/introducao). The endpoint catalog was extracted from the OpenAPI definitions embedded in those pages on 2026-09-17, and the skill tells the agent to read the catalog before assuming any path or field.

**Limits.** Brazil only. Needs a Focus NFe token. Production issues real tax documents; test in the homologation environment first.

**Install.** `npx skills add alexbueno7/skills --skill focusnfe` · [SKILL.md](skills/focusnfe/SKILL.md)

### notas-fiscais-brasil

**What it does.** Reviews or implements the issuing of Brazilian invoices (NFS-e, NF-e, NFC-e) in a system. It defines the operation and its sources, builds a tax matrix that can be checked, compares rule, code and payload, validates the integration life cycle (sending, timeout, retry, cancellation) and tests in proportion to the change.

**What you get.** A report with the rules confirmed and their sources, pending tax questions, findings or files changed, and checks run.

**What it is based on.** Brazilian legislation cited by article: LC 116/2003 (arts. 3, 4 and 6) for ISS, Lei 10.833/2003 (arts. 30 and 31) for CSRF, Decreto 9.580/2018 (art. 714) for IRRF on professional services, IN RFB 1.234/2012 for public bodies, and Lei 9.430/1996 (art. 67) for limits. The skill requires recording source, version, validity and date of each rule, and blocks conclusions when a source could not be read.

**Limits.** Brazil only. Not tax or legal advice: an accountant confirms classification and rates. It points to a companion skill, retencoes-tributarias-tomador, which is not in this repository (it derives from asv-digital/skills-contadores).

**Install.** `npx skills add alexbueno7/skills --skill notas-fiscais-brasil` · [SKILL.md](skills/notas-fiscais-brasil/SKILL.md)

## License

[MIT](LICENSE). Free to use, change and share.
