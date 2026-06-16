# Revisão de IaC gerado por IA

**Pilar:** analisar
**Fase:** 2
**Categoria:** supply-chain
**OWASP:** A05:2021 - Security Misconfiguration
**Ferramentas sugeridas:** Checkov, Trivy
**Intenção:** Identificar misconfigurações em infraestrutura como código produzida por assistentes de IA.

## Como usar
Cole os arquivos Terraform, CloudFormation, Kubernetes manifests ou Dockerfiles. Contextualize o ambiente e o provedor de cloud.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{ARQUIVOS_IAC}} | Arquivos Terraform, CloudFormation, Kubernetes manifests, Dockerfiles ou docker-compose.yml |
| {{AMBIENTE}} | Ambiente alvo: produção, staging, desenvolvimento; e provedor de cloud: AWS, GCP, Azure, on-premise |

## Prompt
```
Atue como especialista em segurança de infraestrutura. Análise {{ARQUIVOS_IAC}} para ambiente {{AMBIENTE}} e identifique:

(1) Exposição de rede: portas abertas desnecessariamente, security groups permissivos (0.0.0.0/0);
(2) IAM e permissões: roles com permissões mais amplas do que necessario, wildcards em policies;
(3) Armazenamento: buckets S3 com acesso público, objetos sem criptografia, logging desabilitado;
(4) Imagens de container: uso de imagem :latest, usuário root, capabilities desnecessarias;
(5) Segredos em IaC: credenciais hardcoded em vars ou outputs, valores sensíveis em state;
(6) Padroes de IA: configurações com valores de placeholder, comentários de scaffold em arquivo de produção.
```

## Saída esperada
Lista de misconfigurações com severidade, localização no arquivo e configuração correta recomendada.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 2 - Análise estática. Use em paralelo com Checkov e Trivy para cobertura completa. Consulte `AUDITORIA.md` para o checklist completo.
