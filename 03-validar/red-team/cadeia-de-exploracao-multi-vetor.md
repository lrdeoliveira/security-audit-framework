# Cadeia de exploração multi-vetor

**Pilar:** validar
**Fase:** 3-4
**Categoria:** red-team
**OWASP:** —
**Ferramentas sugeridas:** Manual
**Intenção:** Combinar vulnerabilidades individuais em uma cadeia de ataque com impacto máximo.

## Como usar
Liste as vulnerabilidades já confirmadas no alvo. O prompt analisa como combiná-las para maximizar o impacto.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{NOME_DO_ALVO}} | Nome do sistema ou aplicação sendo avaliado |
| {{LISTA_DE_VULNERABILIDADES}} | Lista de vulnerabilidades confirmadas com tipo, localização e severidade individual |

## Prompt
```
Você é um red teamer especializado em chains de exploração. Dado o conjunto de vulnerabilidades confirmadas em {{NOME_DO_ALVO}}: {{LISTA_DE_VULNERABILIDADES}}, elabore:

(1) Todas as cadeias possíveis que combinam 2 ou mais vulnerabilidades;
(2) Para cada cadeia: pré-condições necessárias, passos de exploração em ordem, dificuldade e impacto final;
(3) A cadeia de maior impacto com detalhamento técnico completo de cada passo;
(4) Cadeias que escalam privilégio: baixo para médio para alto para RCE ou exfiltração total;
(5) Cadeias que combinam vulnerabilidades de IA com vulnerabilidades web tradicionais;
(6) Recomendação de qual vulnerabilidade corrigir primeiro para quebrar o maior número de cadeias.

Exemplos-âncora de cadeia: (a) IDOR de leitura → vazamento de token de reset → account takeover → escalada a admin; (b) prompt injection indireta via RAG → tool call de exfiltração → SSRF ao endpoint de metadata da cloud. Materialize cada cadeia no YAML usando o campo `deriva_de` para ligar os achados individuais que a compõem.

Formate as cadeias como: A -> B -> C = impacto X.
```

## Saída esperada
Mapa de cadeias de exploração com passos, pré-condições, impacto e recomendação de prioridade de correção.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3/4 - Validação de impacto. Execute após confirmar vulnerabilidades individuais para escalar o impacto da operação. Consulte `AUDITORIA.md` para o checklist completo.
