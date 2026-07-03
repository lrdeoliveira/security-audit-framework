# Análise de resposta e vazamento de informação

**Pilar:** validar
**Fase:** 3
**Categoria:** dast
**OWASP:** A05:2021 - Security Misconfiguration
**Ferramentas sugeridas:** Burp Suite
**Intenção:** Identificar dados sensíveis expostos em respostas de API, mensagens de erro e headers.

## Como usar
Cole respostas HTTP reais capturadas no proxy ou via curl. Inclua headers, body e mensagens de erro. Quanto mais respostas diferentes, melhor a análise.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{RESPOSTAS_HTTP}} | Respostas HTTP capturadas no proxy com headers, body e mensagens de erro |

## Prompt
```
Atue como especialista em vazamento de informação e analise as respostas HTTP {{RESPOSTAS_HTTP}} para identificar:

(1) PII ou dados sensíveis retornados desnecessariamente: senha hash, token, dados internos de outros usuários;
(2) Stack traces e mensagens de erro que revelam tecnologia, paths internos ou lógica de negócio;
(3) Headers que expõe informação: Server, X-Powered-By, versões, IPs internos;
(4) Dados de usuários além do necessário para a funcionalidade (over-fetching);
(5) Diferenças de resposta que permitem enumeração: usuário existe vs. não existe;
(6) Tokens ou identificadores previsíveis expostos em respostas que deveriam ser opacos.
```

## Saída esperada
Lista de dados sensíveis expostos com endpoint, campo específico e recomendação de correção.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3 - Análise dinâmica. Use depois de capturar trafego no Burp para identificar exposição passiva. Consulte `AUDITORIA.md` para o checklist completo.
