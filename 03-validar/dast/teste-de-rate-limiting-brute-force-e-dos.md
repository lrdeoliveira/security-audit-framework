# Teste de rate limiting, brute force e DoS de recurso

**Pilar:** validar
**Fase:** 3
**Categoria:** dast
**OWASP:** A04:2021 - Insecure Design (falta de limites) / API4:2023 - Unrestricted Resource Consumption
**Ferramentas sugeridas:** Burp Intruder, ffuf, scripts próprios
**Intenção:** Verificar se endpoints sensíveis e caros têm limites de taxa e proteção contra brute force, enumeração e exaustão de recursos.

## Como usar
Liste os endpoints sensíveis (login, OTP, reset, busca, export, endpoints que disparam IA/email/SMS) e qualquer limite conhecido. Indique o modelo de identidade usado para limitar (IP, conta, API key).

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{ENDPOINTS_E_LIMITES}} | Endpoints sensíveis/caros, limites conhecidos e dimensão usada para rate-limit (IP/conta/key) |

## Prompt
```
Atue como especialista em abuso de recursos e disponibilidade. Para {{ENDPOINTS_E_LIMITES}}, elabore um plano de teste para:

(1) Ausência de rate-limit: login, OTP/MFA, reset de senha, verificação de cupom, endpoints de busca/export;
(2) Brute force / credential stuffing: estimar tentativas viáveis, presença de lockout, CAPTCHA, atraso progressivo;
(3) Bypass de rate-limit: rotação de IP/X-Forwarded-For, troca de header/casing, múltiplas contas, race no contador, reset por janela;
(4) Enumeração em massa: IDs sequenciais, scraping de dados via paginação sem teto;
(5) Exaustão de recursos: payloads grandes, paginação/limit sem teto, expansão (zip bomb, regex catastrófico), N+1 induzido, queries GraphQL profundas/batched;
(6) Amplificação de custo: endpoints que disparam IA/LLM, email, SMS, webhooks ou jobs caros sem cota por usuário (denial-of-wallet);
(7) Falta de teto de upload/concorrência;
(8) Race-condition de limite (single-packet attack): disparar N requisições em paralelo com last-byte sync para estourar cota/cupom antes de o contador atualizar.

Para cada teste: como medir o limite, sinais de bypass e critério de impacto. Use volumes seguros e pare ao confirmar — não derrube o ambiente.
```

## Saída esperada
Plano de teste de limites por endpoint, com método de medição, técnicas de bypass e critério de impacto, em volume não-destrutivo.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3 - Análise dinâmica. Para alvos com IA, faça par com `03-validar/ia/teste-de-denial-of-wallet-e-consumo-ilimitado.md`. Coordene volumes com o dono do ambiente. Consulte `AUDITORIA.md` para o checklist completo.
