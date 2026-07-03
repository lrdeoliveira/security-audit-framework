# Análise de supply chain de LLM

**Pilar:** descobrir
**Fase:** 1
**Categoria:** supply-chain
**OWASP:** LLM03:2025 - Supply Chain (+ LLM04:2025 Data and Model Poisoning)
**Ferramentas sugeridas:** Manual, OSV-Scanner, modelscan, AI-BOM
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

(1) Modelos de terceiros: políticas de uso de dados, jurisdição, retenção de prompts e respostas pelo provedor;
(2) APIs de IA: autenticação, rate limiting, fallback em caso de indisponibilidade;
(3) Fine-tuning e RAG: quais dados do produto foram usados para treinar ou configurar modelos;
(4) Plugins e ferramentas de LLM: superfície de ataque de cada integração, validação de outputs;
(5) Cadeia de confiança: se um modelo externo é comprometido, qual é o impacto máximo no produto;
(6) Conformidade: LGPD, GDPR e regulações setoriais aplicáveis ao processamento por LLMs externos;
(7) Proveniência e integridade de modelos: origem dos pesos (HuggingFace/hubs), arquivos pickle/`.bin` que dão RCE na desserialização, checksums e assinatura (sigstore), scan com `picklescan`/`modelscan`;
(8) Servidores MCP de terceiros como vetor de supply chain: tool poisoning, rug pull e mudança silenciosa de tool;
(9) Prompt/template supply chain: prompts e templates puxados de fontes externas (ex. LangChain Hub);
(10) Pin e versionamento de modelo de geração e de embeddings: risco do provedor mudar comportamento silenciosamente (LLM08:2025).
```

## Saída esperada
Mapa de riscos de supply chain de IA com modelos/APIs avaliados, dados expostos e recomendações de mitigação.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 1 - Reconhecimento. Execute no início de auditorias de produtos que integram IA de terceiros. Consulte `AUDITORIA.md` para o checklist completo.
