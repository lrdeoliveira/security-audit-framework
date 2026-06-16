# Geração de casos de teste por endpoint

**Pilar:** validar
**Fase:** 3
**Categoria:** dast
**OWASP:** —
**Ferramentas sugeridas:** Burp Suite
**Intenção:** Criar payloads de ataque e roteiro de teste manual para um endpoint específico.

## Como usar
Descreva o endpoint com metodo HTTP, URL, headers de autenticação, schema do body e o que ele faz. Quanto mais contexto sobre lógica de negócio, mais relevantes os casos.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DO_ENDPOINT}} | Metodo HTTP, URL, headers necessarios, schema do body e descrição da funcionalidade |

## Prompt
```
Atue como pentester web senior. Dado o endpoint {{DESCRICAO_DO_ENDPOINT}}, gere casos de teste para:

(1) Auth bypass: acesso sem token, com token expirado, com token de outro usuário;
(2) IDOR: substituicao de IDs por IDs de outros usuários, IDs negativos, UUIDs de outros contextos;
(3) Injection: SQLi (erro e blind), NoSQL, SSTI, command injection nos campos relevantes;
(4) Validação de entrada: campos ausentes, tipos errados, strings longas, caracteres especiais;
(5) Rate limiting: requisicoes em volume e padrões de enumeração;
(6) Business logic: estados invalidos, sequências fora de ordem, operações em recursos de outro usuário.

Formate como tabela: vetor, payload de exemplo, resposta esperada se vulneravel.
```

## Saída esperada
Tabela de casos de teste com vetor, payload e resposta esperada em caso vulneravel.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3 - Análise dinâmica. Use antes da sessão no Burp para não improvisar os casos de teste. Consulte `AUDITORIA.md` para o checklist completo.
