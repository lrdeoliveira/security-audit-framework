# CI/CD de segurança contínua

Pipeline que roda os scanners do framework automaticamente em cada PR/push do repositório **alvo** (o app que você audita), fechando o loop entre a auditoria manual e a vigilância contínua.

## Instalação (1 minuto)

1. Copie `security-audit.yml` para o repositório alvo em:
   ```
   .github/workflows/security-audit.yml
   ```
2. Faça commit e push. O pipeline roda sozinho no próximo PR/push.
3. (Opcional) Para regras premium do Semgrep, adicione o secret `SEMGREP_APP_TOKEN` em *Settings → Secrets → Actions*.
4. **Repo de organização:** adicione o secret `GITLEAKS_LICENSE`. Desde a v2, o `gitleaks-action` é grátis apenas para contas pessoais; em repos de org, o job falha sem a licença.

> O arquivo fica em `ci-cd/` aqui no framework como **template**. Ele não roda no repo do framework — roda no código-alvo.

## O que o pipeline faz

| Job | Ferramenta | Saída | Quebra o build? |
|-----|-----------|-------|-----------------|
| `semgrep` | Semgrep (SAST) | SARIF → aba Security | **Sim, em regras ERROR** (o scan informativo sobe todo o SARIF) |
| `trivy` | Trivy (SCA + IaC + secret) | SARIF → aba Security | **Sim, se CRITICAL** (vuln, secret e IaC/misconfig) |
| `gitleaks` | Gitleaks (segredos no histórico) | log + anotações | Sim, se vazar segredo |
| `dependency-review` | Dependency Review (só em PR) | anotações no PR | **Sim, se PR introduz dependência CRITICAL** |
| `osv-scanner` | OSV (vulns de dependências) | SARIF → aba Security | Não (informativo) |

Gatilhos: todo `push` em main/master/develop, todo `pull_request`, varredura semanal (segunda 06:00 UTC) e execução manual (`workflow_dispatch`).

As permissões seguem *least privilege*: o topo do workflow tem só `contents: read` e cada job eleva apenas o que precisa (ex.: `security-events: write` só em `semgrep`/`trivy`/`osv-scanner`). Em PRs vindos de **fork**, o `GITHUB_TOKEN` é read-only e o upload de SARIF é ignorado silenciosamente — rode a varredura completa no push para `main`.

## Onde ver os resultados

- **Security → Code scanning alerts**: findings de Semgrep, Trivy e OSV consolidados, com linha de código e severidade.
- **Actions → security-audit**: log de cada job; o gate de CRITICAL aparece aqui como falha vermelha.
- **PR checks**: o desenvolvedor vê o status antes do merge.

## Política recomendada (branch protection)

Em *Settings → Branches → Branch protection rules* para `main`:

- Exija o check `security-audit / SCA / IaC (Trivy)` como obrigatório.
- Bloqueie merge com alertas de Code Scanning de severidade alta/crítica.

Assim nenhuma dependência com CVE crítico ou segredo vazado entra em produção.

## Como isso se conecta ao framework

- **`bootstrap-scan.sh`** (em `00-orquestrador/`) = varredura **local e profunda** no início de uma auditoria (inclui mcp-scan, checkov, trufflehog e consolida em `pre-scan.md`). Use ao auditar manualmente.
- **`security-audit.yml`** (este) = varredura **contínua e automática** em cada mudança, para não regredir entre auditorias.

Os dois usam os mesmos motores (Semgrep, Trivy, Gitleaks, OSV); o reteste de achados corrigidos (ver `04-entregar/plano-de-reteste-por-achado.md`) pode ser amarrado a este pipeline.

## Ajustes comuns

- **Reduzir ruído inicial**: troque `severity: CRITICAL,HIGH,MEDIUM` do Trivy para `CRITICAL,HIGH` enquanto trata o backlog.
- **Monorepo**: ajuste `scan-args` do osv-scanner e o working-directory dos jobs por subprojeto.
- **Falhar também em HIGH**: no job `trivy`, gate adicional com `severity: CRITICAL,HIGH` e `exit-code: "1"`.
- **Afrouxar o gate do Semgrep**: o passo *Semgrep gate* falha em regras `ERROR`. Para tornar o SAST puramente informativo enquanto trata o backlog, remova esse passo (o upload de SARIF continua).
- **Pin de versões**: as actions **já são fixadas por SHA de commit** (mais a imagem do Semgrep por digest). Ao atualizar, regenere o SHA a partir da tag e valide — ex.: `gh api repos/actions/checkout/commits/v5.0.0 --jq .sha` — em vez de digitar o SHA à mão.
