# Geração de script de scan automatizado

**Pilar:** entregar
**Fase:** automação
**Categoria:** automation
**OWASP:** —
**Ferramentas sugeridas:** Python, Bash, CI/CD
**Intenção:** Criar script Python ou Bash que automatiza uma sequência de testes recorrentes.

## Como usar
Descreva o que você quer automatizar: quais ferramentas usar, em qual sequência, quais outputs coletar e qual formato de resultado você precisa.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{LINGUAGEM_DO_SCRIPT}} | Python, Bash ou outra linguagem preferida |
| {{DESCRICAO_DO_FLUXO}} | Sequência de ferramentas a executar, parâmetros e formato de saída consolidada |

## Prompt
```
Crie um script {{LINGUAGEM_DO_SCRIPT}} que automatiza o seguinte fluxo de scan: {{DESCRICAO_DO_FLUXO}}. O script deve:

(1) Aceitar o alvo como argumento (domínio ou URL base);
(2) Executar as ferramentas na sequência correta, aguardando a saída de cada uma;
(3) Parsear os resultados relevantes de cada ferramenta (JSON, texto ou XML);
(4) Consolidar os achados em relatório único com deduplicação;
(5) Ter tratamento de erros: timeout, falha de ferramenta, alvo inacessível;
(6) Gerar log de execução com timestamps e status de cada etapa.

Requisitos de segurança da própria automação:
(a) Não embutir segredos/tokens no script — ler de variável de ambiente ou secret manager;
(b) Exigir flag explícita de autorização/escopo do alvo antes de disparar qualquer teste contra ele;
(c) Retornar exit codes distintos (0 = ok, ≠0 conforme severidade/erro) para gating em CI/CD;
(d) Respeitar rate limit e evitar hammering: throttle/concorrência limitada entre requisições e ferramentas.

Inclua comentários explicando cada seção e instruções de uso.
```

## Saída esperada
Script completo com tratamento de erros, parsing de resultados e saída consolidada.

## Onde usar no fluxo
Automação. Use para codificar fluxos recorrentes e criar gates de CI/CD de segurança. Consulte `AUDITORIA.md` para o checklist completo.
