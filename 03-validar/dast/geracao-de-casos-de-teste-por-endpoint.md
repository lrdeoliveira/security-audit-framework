# Geração de casos de teste por endpoint

**Pilar:** validar
**Fase:** 3
**Categoria:** dast
**OWASP:** —
**Ferramentas sugeridas:** Burp Suite
**Intenção:** Criar payloads de ataque e roteiro de teste manual para um endpoint específico.

## Como usar
Descreva o endpoint com método HTTP, URL, headers de autenticação, schema do body e o que ele faz. Quanto mais contexto sobre lógica de negócio, mais relevantes os casos.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DO_ENDPOINT}} | Método HTTP, URL, headers necessários, schema do body e descrição da funcionalidade |

## Prompt
```
Atue como pentester web senior. Dado o endpoint {{DESCRICAO_DO_ENDPOINT}}, gere casos de teste para:

(1) Auth bypass: acesso sem token, com token expirado, com token de outro usuário;
(2) IDOR: substituição de IDs por IDs de outros usuários, IDs negativos, UUIDs de outros contextos;
(3) Injection: SQLi (erro e blind), NoSQL, SSTI, command injection nos campos relevantes;
(4) Validação de entrada: campos ausentes, tipos errados, strings longas, caracteres especiais;
(5) Rate limiting: requisições em volume e padrões de enumeração;
(6) Business logic: estados inválidos, sequências fora de ordem, operações em recursos de outro usuário;
(7) Mass assignment: injetar campos privilegiados (role, isAdmin, ownerId, status) no body;
(8) HTTP verb tampering: trocar o método (GET/POST/PUT/PATCH/DELETE) para contornar checagem por verbo;
(9) Confusão de content-type: enviar JSON como form-urlencoded e vice-versa, alternar Content-Type para burlar validação;
(10) Parameter pollution: duplicar parâmetros (query e body) para confundir o parser.

Para cada vetor, forneça a string exata do payload, não só o nome da técnica. Formate como tabela: vetor, string exata do payload, resposta esperada se vulnerável.

Segurança operacional: use contas de teste próprias; marque os casos destrutivos (escrita/exclusão) para execução controlada.
```

## Saída esperada
Tabela de casos de teste com vetor, payload e resposta esperada em caso vulnerável.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3 - Análise dinâmica. Use antes da sessão no Burp para não improvisar os casos de teste. Consulte `AUDITORIA.md` para o checklist completo.
