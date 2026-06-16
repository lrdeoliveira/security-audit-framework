# Ficha técnica de achado

**Pilar:** entregar
**Fase:** 5
**Categoria:** reporting
**OWASP:** —
**Ferramentas sugeridas:** —
**Intenção:** Documentar um achado com todos os campos necessarios para um relatório profissional de pentest.

## Como usar
Descreva o achado com o máximo de detalhes técnicos que você coletou: onde encontrou, como confirmou e qual foi a resposta do servidor ou comportamento do sistema.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DO_ACHADO}} | Descricao detalhada: localização, comportamento observado, requisicao e resposta de confirmação |

## Prompt
```
Documente o seguinte achado de segurança: {{DESCRICAO_DO_ACHADO}}. Produza uma ficha técnica completa com:

(1) Titulo: descritivo e específico, ex: IDOR em /api/v1/users/{id} permite acesso a dados de qualquer usuário;
(2) Severidade: CVSS 3.1 score e vetor, classificação OWASP Top 10;
(3) Descricao técnica: como a vulnerabilidade funciona e qual e a causa raiz;
(4) Prova de conceito: requisicao HTTP completa em curl ou passos de reprodução numerados;
(5) Impacto: o que um atacante consegue fazer se explorar com sucesso;
(6) Recomendação de correção: solucao técnica específica com exemplo de código corrigido se aplicavel;
(7) Referencias: CWE, OWASP e CVE se aplicavel.
```

## Saída esperada
Ficha técnica completa do achado com todos os campos para relatório profissional.

## Onde usar no fluxo
Fase 5 - Relatório. Use para cada achado individualmente antes de consolidar no relatório. Transfira o resultado para `templates/registro-de-achado.yaml` e `templates/relatorio-final.md`. Consulte `AUDITORIA.md` para o checklist completo. Consulte `AUDITORIA.md` para o checklist completo.
