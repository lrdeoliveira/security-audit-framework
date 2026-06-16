# Mapeamento de superfície de ataque

**Pilar:** descobrir
**Fase:** 1
**Categoria:** recon
**OWASP:** —
**Ferramentas sugeridas:** Manual, Burp (passivo)
**Intenção:** Abrir o projeto com visão completa de entradas, integrações e superfície de risco.

## Como usar
Cole o código-fonte, estrutura de diretórios e/ou arquivos de rota. Quanto mais contexto, mais preciso o mapa.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{CODIGO_OU_ESTRUTURA}} | Código-fonte, estrutura de diretórios, arquivos de rota ou combinação dos três |

## Prompt
```
Você e um especialista em segurança ofensiva. Análise {{CODIGO_OU_ESTRUTURA}} e produza um mapa de superfície de ataque com as seguintes seções:

(1) Entradas de usuário e como os dados fluem pelo sistema;
(2) Rotas sensíveis com autenticação, autorização ou lógica de negócio crítica;
(3) Integrações de terceiros e dados compartilhados com serviços externos;
(4) Uso de segredos, variáveis de ambiente e configuração exposta;
(5) Componentes de IA, LLMs, agentes ou MCPs presentes;
(6) Pontos de autenticação e autorização.

Para cada item, classifique o risco como alto, médio ou baixo e justifique em uma linha.
```

## Saída esperada
Relatório organizado por seção com classificação de risco e itens priorizados para teste.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 1 - Reconhecimento. Use no início de qualquer auditoria para orientar o escopo do trabalho. Consulte `AUDITORIA.md` para o checklist completo.
