---
name: prompt-brief
description: "Turns a loose task description into a prompt in the XML-section brief format (context, goal, done_when, boundaries, autonomy, proof, report, memory), asking what is missing before writing. Use when the user runs /prompt-brief or asks to fix, improve or standardize a prompt, turn a text into a brief, or write a prompt for an agent. Not for auditing prompts that already exist in a project, nor for executing the task described. PT-BR: Transforma uma descrição solta de tarefa em um prompt no padrão de brief em seções XML, perguntando o que falta antes de escrever. Use quando o usuário chamar /prompt-brief ou pedir para \"ajustar o prompt\", \"melhorar esse prompt\", \"virar brief\" ou \"prompt para o agente\". Não use para auditar prompts existentes nem para executar a tarefa."
---

# Prompt no padrão de brief

O usuário entrega uma descrição de tarefa, em geral curta e informal, e quer de volta um prompt pronto para colar em um agente de desenvolvimento. O texto vem nos argumentos do comando ou na mensagem que o chamou. Quem vai ler o resultado é outro agente, sem nenhum contexto desta conversa: tudo o que ele precisa saber tem de estar escrito no brief.

O trabalho aqui é escrever o prompt, não fazer a tarefa. Não edite arquivos, não rode comandos da tarefa e não comece a implementação, mesmo que a descrição pareça um pedido direto. Se o usuário quiser a execução, ele pede depois.

Base: guia oficial de prompts da Anthropic, [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (ser claro e direto, dar contexto, estruturar com tags XML) e [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2).

## Antes de escrever

Confira se a descrição responde a três coisas:

1. O que mudar ou corrigir: qual sistema, página, tela, função ou conteúdo.
2. Qual é o resultado esperado.
3. Como conferir que ficou pronto.

Se faltar algo que muda o resultado, faça até três perguntas curtas, só sobre o que falta, e espere a resposta. Não pergunte o que já está na descrição, na conversa ou no `AGENTS.md` do projeto atual; leia-o quando existir, porque ele costuma responder qual é o sistema e quais são os limites. Se o usuário disser para gerar mesmo assim, escreva com o que há e registre em `context` o que ficou em aberto.

Não invente fatos, causas, caminhos de arquivo, URLs ou nomes de função. O que for hipótese entra marcado como hipótese.

## Formato

Tags em inglês, texto em pt-BR, as oito seções nesta ordem, separadas por linha em branco. As quatro primeiras você escreve a partir da descrição. As quatro últimas são fixas: copie como estão abaixo, trocando só o destino das notas em `memory` quando o usuário indicar outro arquivo.

```
<context>
Projeto ou sistema, para quem é e o que acontece hoje. O que o resultado permite a essa pessoa fazer.
</context>

<goal>
O resultado esperado, em uma ou duas frases.
</goal>

<done_when>
- Verificação que dá para executar ou medir.
- Segunda verificação.
</done_when>

<boundaries>
Altere apenas [escopo]. Não mexa em [fora do escopo].
Sem funcionalidades, refatorações ou arquivos que não foram pedidos.
Se for apenas uma pergunta, responda e pare.
</boundaries>

<autonomy>
Aja assim que souber o suficiente.
Não reabra decisões já tomadas.
Pare e pergunte somente antes de algo irreversível, de uma mudança real de escopo ou quando só o solicitante tiver a resposta.
Execute partes independentes em subagentes em paralelo.
</autonomy>

<proof>
Confira o trabalho contra done_when antes de relatar.
Toda afirmação aponta para um resultado desta sessão.
Etapas que falharam ou foram puladas são relatadas como falhas ou puladas.
</proof>

<report>
Primeira frase: o que aconteceu.
Depois, só os detalhes que mudam o que será feito em seguida.
Frases completas, sem abreviações.
</report>

<memory>
Registre lições desta execução no AGENTS.md do projeto:
uma lição por nota, com uma linha sobre por que importou.
Atualize uma nota antiga antes de criar outra.
</memory>
```

## Como preencher cada seção

- `context`: escreva para alguém que nunca viu o projeto. Diga o que é o sistema, quem usa e o que acontece hoje. Causa provável e decisões já tomadas pelo usuário entram aqui.
- `goal`: o resultado, não os passos. Uma ou duas frases.
- `done_when`: cada item é algo que o agente consegue executar ou medir, como um comando que passa, uma tela que mostra certo valor ou uma resposta de API. "Funciona bem" não serve.
- `boundaries`: o escopo que o usuário deu e o que fica de fora. Se ele não disse o que fica de fora, não invente uma lista: mantenha as duas linhas genéricas.

## Entrega

Devolva o brief inteiro em um único bloco de código, pronto para copiar, sem resumo antes nem comentário depois. Se você assumiu algo que o usuário não disse, liste em uma linha abaixo do bloco.

