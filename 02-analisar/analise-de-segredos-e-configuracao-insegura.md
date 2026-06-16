# Análise de segredos e configuração insegura

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A02:2021 - Cryptographic Failures
**Ferramentas sugeridas:** TruffleHog, Gitleaks
**Intenção:** Detectar segredos hardcoded, configuração insegura e exposição de variáveis de ambiente.

## Como usar
Cole o código de configuração, arquivos .env.example, código de inicialização e qualquer lugar onde credenciais sao carregadas. Cole também o .gitignore se disponível.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_DE_CONFIG}} | Código de configuração, arquivos .env.example, arquivo de inicialização da aplicação |

## Prompt
```
Analise {{CODIGO_DE_CONFIG}} como especialista em segurança de configuração e identifique:

(1) Segredos hardcoded: API keys, tokens, senhas, certificados embutidos no código;
(2) Variaveis de ambiente: segredos esperados, fallbacks inseguros (padrão vazio ou fraco);
(3) Exposição de configuração: endpoints que retornam configuração, logs com segredos, stack traces em produção;
(4) Configuração de CORS, CSP e headers de segurança ausentes ou permissivos;
(5) Segredos em comentários, strings de debug ou histórico de código;
(6) Dependencias com acesso a ambiente mais amplo do que o necessario.
```

## Saída esperada
Lista de segredos expostos ou configuração insegura com localização e recomendação de correção.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Use junto com TruffleHog para cobertura completa de vazamento de segredos. Consulte `AUDITORIA.md` para o checklist completo.
