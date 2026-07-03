# Ficha técnica de achado

**Pilar:** entregar
**Fase:** 5
**Categoria:** reporting
**OWASP:** —
**Ferramentas sugeridas:** —
**Intenção:** Documentar um achado com todos os campos necessários para um relatório profissional de pentest.

## Como usar
Descreva o achado com o máximo de detalhes técnicos que você coletou: onde encontrou, como confirmou e qual foi a resposta do servidor ou comportamento do sistema.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DO_ACHADO}} | Descrição detalhada: localização, comportamento observado, requisição e resposta de confirmação |

## Prompt
```
Documente o seguinte achado de segurança: {{DESCRICAO_DO_ACHADO}}. Produza uma ficha técnica completa com:

(1) Título: descritivo e específico, ex: IDOR em /api/v1/users/{id} permite acesso a dados de qualquer usuário;
(2) Severidade: CVSS 4.0 (vetor `CVSS:4.0/...`), com CVSS 3.1 opcional para compat com scanners legados; classificação OWASP Top 10 (para achados de IA, use a numeração OWASP LLM Top 10 2025 — LLM01–LLM10:2025 — no campo OWASP);
(3) Descrição técnica: como a vulnerabilidade funciona e qual é a causa raiz;
(4) Prova de conceito: requisição HTTP completa em curl ou passos de reprodução numerados;
(5) Impacto: o que um atacante consegue fazer se explorar com sucesso;
(6) Recomendação de correção: solução técnica específica com exemplo de código corrigido se aplicável;
(7) Referências: CWE, OWASP e CVE se aplicável;
(8) Evidências: referência ao arquivo de prova em `evidencias/AUD-XXX/` (screenshot, log ou request);
(9) Instâncias/ativos afetados: contagem e lista dos endpoints/arquivos afetados.
```

## Saída esperada
Ficha técnica completa do achado com todos os campos para relatório profissional.

## Onde usar no fluxo
Fase 5 - Relatório. Use para cada achado individualmente antes de consolidar no relatório. Transfira o resultado para `templates/registro-de-achado.yaml` e `templates/relatorio-final.md`. Consulte `AUDITORIA.md` para o checklist completo.
