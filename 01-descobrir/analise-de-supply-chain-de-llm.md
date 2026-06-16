# Análise de supply chain de LLM

**Pilar:** descobrir
**Fase:** 1
**Categoria:** supply-chain
**OWASP:** A06:2021 - Vulnerable Components
**Ferramentas sugeridas:** Manual, OSV-Scanner
**Intenção:** Mapear riscos de modelos externos, APIs de IA e dados de treinamento usados no produto.

## Como usar
Descreva quais modelos, APIs de IA e serviços de dados externos o produto usa. Inclua como sao invocados, que dados recebem e qual nível de confianca tem.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{NOME_DO_PRODUTO}} | Nome e contexto do produto sendo avaliado |
| {{DESCRICAO_DE_DEPENDENCIAS_IA}} | Lista de modelos, APIs e serviços de IA externos usados com descrição de como sao invocados |

## Prompt
```
Analise o ecossistema de IA externo de {{NOME_DO_PRODUTO}} como especialista em supply chain de sistemas de IA. Contexto: {{DESCRICAO_DE_DEPENDENCIAS_IA}}. Avalie:

(1) Modelos de terceiros: politicas de uso de dados, jurisdicao, retenção de prompts e respostas pelo provedor;
(2) APIs de IA: autenticação, rate limiting, fallback em caso de indisponibilidade;
(3) Fine-tuning e RAG: quais dados do produto foram usados para treinar ou configurar modelos;
(4) Plugins e ferramentas de LLM: superfície de ataque de cada integração, validação de outputs;
(5) Cadeia de confianca: se um modelo externo e comprometido, qual e o impacto máximo no produto;
(6) Conformidade: LGPD, GDPR e regulações setoriais aplicaveis ao processamento por LLMs externos.
```

## Saída esperada
Mapa de riscos de supply chain de IA com modelos/APIs avaliados, dados expostos e recomendações de mitigação.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 1 - Reconhecimento. Execute no início de auditorias de produtos que integram IA de terceiros. Consulte `AUDITORIA.md` para o checklist completo.
