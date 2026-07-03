# Análise de segredos e configuração insegura

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A05:2021 - Security Misconfiguration (+ CWE-798 Hardcoded Credentials)
**Ferramentas sugeridas:** TruffleHog, Gitleaks
**Intenção:** Detectar segredos hardcoded, configuração insegura e exposição de variáveis de ambiente.

## Como usar
Cole o código de configuração, arquivos .env.example, código de inicialização e qualquer lugar onde credenciais são carregadas. Cole também o .gitignore se disponível.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_DE_CONFIG}} | Código de configuração, arquivos .env.example, arquivo de inicialização da aplicação |

## Prompt
```
Analise {{CODIGO_DE_CONFIG}} como especialista em segurança de configuração e identifique:

(1) Segredos hardcoded: API keys, tokens, senhas, certificados embutidos no código;
(2) Variáveis de ambiente: segredos esperados, fallbacks inseguros (padrão vazio ou fraco); segredos em `ENV`/build-args do Dockerfile; `.env` commitado no repo;
(3) Exposição de configuração: endpoints que retornam configuração, logs com segredos, stack traces em produção; Laravel `APP_DEBUG=true` ou `APP_KEY` exposto; `NEXT_PUBLIC_*` vazando segredo no bundle client do Next.js;
(4) CORS, CSP e headers de segurança → ver `revisao-de-cors-csrf-e-headers-de-seguranca.md`;
(5) Segredos em comentários, strings de debug ou histórico de código (varra o histórico git);
(6) Dependências com acesso a ambiente mais amplo do que o necessário.

Regex de alto sinal para varredura: `AKIA[0-9A-Z]{16}`, `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----`, `sk_live_`, `ghp_`, `xox[baprs]-`.
```

## Saída esperada
Lista de segredos expostos ou configuração insegura com localização e recomendação de correção.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Use junto com TruffleHog para cobertura completa de vazamento de segredos. Consulte `AUDITORIA.md` para o checklist completo.
