# Revisão de autenticação e controle de acesso

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A01:2021 - Broken Access Control
**Ferramentas sugeridas:** Semgrep, CodeQL
**Intenção:** Auditar implementação de auth, JWT, sessão e autorização por recurso.

## Como usar
Cole o código de autenticação, middleware de autorização e rotas protegidas. Inclua a definição de roles/permissões se existir.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_DE_AUTH}} | Código de autenticação, middleware de autorização, rotas protegidas e modelo de permissões |

## Prompt
```
Atue como especialista em segurança de identidade e acesso. Análise {{CODIGO_DE_AUTH}} e identifique:

(1) Broken authentication: senhas sem hash adequado, tokens fracos, sessões sem expiração;
(2) JWT: algoritmo none, chave fraca, ausência de validação de audience/issuer, tokens sem rotação;
(3) IDOR: acesso a recursos por ID sem verificação de propriedade;
(4) Privilege escalation: paths para elevar permissões ou acessar funcionalidades restritas;
(5) RBAC incompleto: endpoints sem middleware de autorização, roles inferidas pelo cliente;
(6) Mass assignment: binding de campos não permitidos em criação/atualização.

Para cada achado: localização, cenário de exploração e correção.
```

## Saída esperada
Auditoria de auth com achados por categoria, cenários de exploração e patches recomendados.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Prioridade máxima: execute antes de qualquer outro SAST. Consulte `AUDITORIA.md` para o checklist completo.
