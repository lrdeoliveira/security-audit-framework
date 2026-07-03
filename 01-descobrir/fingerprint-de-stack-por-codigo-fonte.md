# Fingerprint de stack por código-fonte

**Pilar:** descobrir
**Fase:** 1
**Categoria:** recon
**OWASP:** —
**Ferramentas sugeridas:** Manual, ripgrep, syft (SBOM), leitura de manifests
**Intenção:** Identificar tecnologias, frameworks e padrões de código gerado por IA antes do teste.

## Como usar
Cole o package.json, requirements.txt, Dockerfile ou qualquer arquivo de configuração. Funciona melhor com múltiplos arquivos combinados.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{ARQUIVO_DE_CONFIG}} | package.json, requirements.txt, Dockerfile, docker-compose.yml ou combinação |

## Prompt
```
Analise {{ARQUIVO_DE_CONFIG}} e produza um fingerprint de stack com:

(1) Linguagens e runtimes detectados e suas versões;
(2) Frameworks principais: web, ORM, auth, infra;
(3) Padrões que sugerem código gerado por IA: estrutura repetitiva, comentários de scaffold, nomes genéricos, e marcadores concretos como `TODO: implement`, `your-api-key`/`example.com`, restos de comentários de assistente ("As an AI"), tratamento de erro boilerplate idêntico e ausência de lockfile;
(4) Serviços de terceiros integrados: OAuth, pagamentos, storage, email;
(5) Superfície de dependências de alto risco;
(6) Runtimes e versões fora de suporte (EOL): ex. Node ≤16, Python 2.7, PHP 7.x, e tags de imagem base perigosas no Dockerfile (`:latest`, distro EOL);
(7) Lacunas de configuração de segurança: CORS aberto, debug habilitado, TLS ausente.
```

## Saída esperada
Lista de tecnologias com versões, indicadores de código gerado por IA e gaps de segurança de configuração.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 1 - Reconhecimento. Execute antes do SAST para orientar quais regras aplicar. Consulte `AUDITORIA.md` para o checklist completo.
