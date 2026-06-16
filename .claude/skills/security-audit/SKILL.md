---
name: security-audit
description: Conduz uma auditoria de segurança completa (pentest assistido) de um repositório, aplicação web, infra ou sistema com IA/LLM/MCP, seguindo o Security Audit Framework (5 fases). Use quando o usuário pedir para auditar a segurança de um alvo, rodar um pentest, fazer um security assessment, revisão de segurança a fundo, ou caçar vulnerabilidades de forma estruturada — indo além de um simples review de diff. Para revisar apenas o diff atual, prefira /security-review.
---

# Security Audit — condutor do framework

Esta skill executa o **Security Audit Framework** de ponta a ponta. O framework é
prompt-driven: o conhecimento vive em arquivos Markdown por pilar; esta skill é o
maestro que decide a ordem, mantém o estado e consolida os achados.

## 0. Pré-requisitos (faça SEMPRE antes de começar)

1. **Autorização.** Confirme com o usuário que ele tem permissão para auditar o alvo
   (sistema próprio, engajamento com autorização escrita, CTF, ou pesquisa autorizada).
   Sem autorização clara, **pare e pergunte**. Não audite alvos de terceiros sem permissão.
2. **Localize o framework.** Encontre o `AUDITORIA.md` (ponto de entrada):
   - Se você está dentro do repositório do framework, está na raiz.
   - Caso contrário, procure por `AUDITORIA.md` no projeto atual, ou peça o caminho ao
     usuário, ou aponte para `github.com/lrdeoliveira/security-audit-framework`.
   - **Leia o `AUDITORIA.md`** — ele tem o índice de todos os prompts, as tabelas de
     severidade/CVSS e o schema de achados. É a fonte de verdade; siga-o.
3. **Defina o escopo.** URLs, repositórios, ambientes (dev/staging/prod), e o que está
   fora do escopo. Anote os placeholders do framework (ex.: `{{DESCRICAO_DO_ALVO}}`,
   `{{DESCRICAO_DO_RAG}}`).
4. **Crie o registro.** `auditorias/{produto}-{data}/achados.yaml`, seguindo
   `templates/registro-de-achado.yaml`. ⚠️ Esta pasta contém dados sensíveis reais —
   nunca a publique.

## 1. Fluxo (siga a ordem; é um pipeline com loop de reteste)

```
bootstrap-scan → 01 descobrir → 02 analisar → 03 validar → 04 entregar
                                                     ↑_____ reteste _____|
```

- **Orquestrador (`00-orquestrador/`)** — rode `plano-de-ataque-em-5-fases.md` para
  montar o plano, depois `bootstrap-scan.sh` (Semgrep, Gitleaks, TruffleHog, Trivy,
  osv-scanner, Checkov, mcp-scan) para a ingestão automatizada inicial. Use o resultado
  para priorizar onde olhar.
- **Pilar 1 — Descobrir (`01-descobrir/`)** — fingerprint de stack, superfície de
  ataque, rotas/SPA, integrações, dependências, componentes de IA, supply-chain de LLM.
- **Pilar 2 — Analisar (`02-analisar/`)** — SAST/config/IaC: auth, injection,
  path-traversal/SSRF, segredos, cripto, XSS/client-side, CORS/CSRF/headers, logging
  (A09), desserialização/race-conditions (A08), IaC, MCP. Registre rascunhos de achado.
- **Pilar 3 — Validar (`03-validar/`)** — confirme explorabilidade:
  - `dast/` — IDOR, auth/account-takeover, XSS ativo, rate-limiting/brute-force/DoS,
    lógica de negócio, upload, vazamento de informação.
  - `ia/` — prompt-injection, guardrails, RAG, tool-use/excessive-agency, output
    handling inseguro (LLM05), denial-of-wallet/consumo ilimitado (LLM10).
  - `red-team/` — cadeia de exploração multi-vetor.
  - Pule o sub-pilar de IA se o alvo não tiver IA/LLM/MCP.
- **Pilar 4 — Entregar (`04-entregar/`)** — sumário executivo, roadmap de remediação
  por sprint, mapeamento de conformidade (LGPD/SOC2/ISO/ASVS), plano de reteste por
  achado, e (opcional) o template de CI/CD em `ci-cd/security-audit.yml`.

## 2. Como executar cada prompt

Para cada arquivo de prompt do pilar: leia-o, substitua os placeholders pelo contexto
real do alvo, execute a análise contra o código/sistema, e **registre todo achado
confirmado** no `achados.yaml` usando o schema do `AUDITORIA.md` (id `AUD-NNN`,
severidade, CVSS 3.1, OWASP, CWE, pilar/subpilar, `prompt_origem`, `deriva_de` quando
um rascunho do Pilar 2 vira confirmado no Pilar 3, `conformidade`, localização, PoC,
impacto, remediação, reteste). Preencha o bloco `cobertura` (endpoints testados/total).

## 3. Boas práticas de execução

- **Correlacione SAST→DAST.** Um achado estático só vira "confirmado" quando você
  demonstra explorabilidade no Pilar 3; use `deriva_de` para ligar os dois.
- **Severidade honesta.** Use as tabelas do `AUDITORIA.md`; não infle nem minimize.
  Marque suposições não verificadas como tal.
- **Sem dano.** Em DAST, prefira PoCs não destrutivos. Nunca exfiltre dados reais,
  derrube serviços, nem teste em produção sem autorização explícita.
- **Reteste.** Após a remediação, re-rode os prompts dos achados afetados e atualize o
  campo `reteste`. O loop só fecha quando os achados estão resolvidos ou aceitos.
- **Paralelize a descoberta** quando fizer sentido (vários pilares de leitura são
  independentes), mas mantenha um único `achados.yaml` consolidado.

## 4. Entregável final

Um relatório (`templates/relatorio-final.md`) com: resumo executivo, placar de achados
por severidade, detalhe de cada `AUD-NNN` com PoC e remediação, roadmap por sprint e
mapeamento de conformidade. Mais a opção de instalar `ci-cd/security-audit.yml` no
repositório alvo para auditoria contínua (quebra o build em CRITICAL).
