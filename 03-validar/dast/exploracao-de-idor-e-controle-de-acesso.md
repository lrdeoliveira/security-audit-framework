# Exploração de IDOR e controle de acesso

**Pilar:** validar
**Fase:** 3
**Categoria:** dast
**OWASP:** A01:2021 - Broken Access Control
**Ferramentas sugeridas:** Burp Repeater
**Intenção:** Mapear e explorar falhas de autorização por recurso em APIs REST.

## Como usar
Descreva os recursos da API com exemplos de resposta e o modelo de autenticação. Inclua o contexto de roles se existir.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DA_API}} | Documentação da API, exemplos de resposta, modelo de autenticação e roles existentes |

## Prompt
```
Atue como especialista em autorização e IDOR. Dado o contexto da API {{DESCRICAO_DA_API}}, elabore:

(1) Mapa de recursos com identificadores (UUID, ID numerico, slug) e quem deveria ter acesso;
(2) Vetores de IDOR: leitura, escrita e exclusao de recursos de outro usuário;
(3) Escalação horizontal: acesso a dados de peers sem permissão;
(4) Escalação vertical: operações de admin sem a role adequada;
(5) Mass assignment: campos que podem ser alterados sem permissão (role, status, ownerId);
(6) Object-level authorization ausente: endpoints que filtram apenas no frontend.

Para cada vetor: exemplo de requisicao curl e resposta esperada se vulneravel.
```

## Saída esperada
Mapa de vetores de autorização com exemplos de requisicao exploitavel e critérios de confirmação.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3 - Análise dinâmica. Execute no Burp Repeater com dois usuários distintos autenticados. Consulte `AUDITORIA.md` para o checklist completo.
