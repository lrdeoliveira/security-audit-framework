# Análise de criptografia e proteção de dados

**Pilar:** analisar
**Fase:** 2
**Categoria:** sast
**OWASP:** A02:2021 - Cryptographic Failures
**Ferramentas sugeridas:** Manual, Burp (TLS)
**Intenção:** Auditar uso de criptografia, hash de senhas e proteção de dados em repouso e transito.

## Como usar
Cole código que faz hash de senhas, criptografia de dados, comúnicação TLS/HTTPS e armazenamento de dados sensíveis.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_DE_CRIPTO}} | Código de autenticação, armazenamento de senhas, criptografia de dados ou comúnicação segura |

## Prompt
```
Atue como especialista em criptografia aplicada. Análise NExusyn e identifique:

(1) Hash de senhas: uso de MD5/SHA1 sem salt, ausência de bcrypt/argon2/scrypt;
(2) Criptografia de dados: algoritmos fracos (DES, RC4, ECB mode), IVs estáticos, chaves derivadas de forma insegura;
(3) Geração de números aleatorios: uso de Math.random() ou random() para fins de segurança;
(4) Transmissao de dados: verificações de certificado desabilitadas, TLS 1.0/1.1, cipher suites fracas;
(5) Dados sensíveis em repouso: PII ou dados financeiros sem criptografia em banco de dados ou logs;
(6) Comparação de strings: comparação de tokens sem função de tempo constante (timing attack).
```

## Saída esperada
Auditoria de criptografia com algoritmos identificados, vulnerabilidades e substituicoes recomendadas.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Combine com análise de trafego no Burp para validar TLS em runtime. Consulte `AUDITORIA.md` para o checklist completo.
