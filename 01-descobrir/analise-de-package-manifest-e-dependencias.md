# Análise de package manifest e dependências

**Pilar:** descobrir
**Fase:** 1-2
**Categoria:** supply-chain
**OWASP:** A06:2021 - Vulnerable Components
**Ferramentas sugeridas:** npm audit, Snyk, Trivy, OSV-Scanner
**Intenção:** Revisar dependências de risco, pacotes obsoletos e indicadores de supply chain compromise.

## Como usar
Cole o package.json, requirements.txt, go.mod ou Gemfile. Inclua o lockfile se disponível para análise de versões pinadas.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{PACKAGE_MANIFEST}} | Arquivo package.json, requirements.txt, go.mod, Gemfile ou equivalente, preferencialmente com lockfile |

## Prompt
```
Atue como especialista em segurança de supply chain. Analise {{PACKAGE_MANIFEST}} e identifique:

(1) Dependencias com CVEs conhecidas de alta severidade e versão vulneravel;
(2) Pacotes obsoletos sem manutencao ativa ha mais de 12 meses;
(3) Nomes suspeitos ou parecidos com pacotes legitimos (typosquatting);
(4) Pacotes com histórico de supply chain compromise ou maintainer takeover;
(5) Dependencias possívelmente alucinadas: nomes que não existem no registro público;
(6) Caminhos de atualização recomendados com menor risco de quebra de compatibilidade.
```

## Saída esperada
Relatório de dependências com CVEs, obsolescencia, suspeitas de typosquatting e recomendações de atualização.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 1 - Reconhecimento / Fase 2 - Análise estática. Execute no início da auditoria e repita a cada ciclo de atualização. Consulte `AUDITORIA.md` para o checklist completo.
