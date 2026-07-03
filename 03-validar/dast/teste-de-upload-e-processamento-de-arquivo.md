# Teste de upload e processamento de arquivo

**Pilar:** validar
**Fase:** 3
**Categoria:** dast
**OWASP:** A04:2021 - Insecure Design (CWE-434 Unrestricted Upload)
**Ferramentas sugeridas:** Burp Suite
**Intenção:** Explorar vulnerabilidades em endpoints que aceitam upload ou processam arquivos.

## Como usar
Descreva o endpoint de upload com o tipo de arquivo aceito, onde o arquivo é armazenado e como é processado ou servido.

## Variáveis
| Variável | Descrição |
|----------|-----------|
| {{DESCRICAO_DO_UPLOAD}} | Endpoint de upload com tipo de arquivo aceito, destino de armazenamento e forma de processamento |

## Prompt
```
Dado o endpoint de upload {{DESCRICAO_DO_UPLOAD}}, elabore casos de teste para:

(1) Upload de tipo inadequado — 3 eixos (magic bytes vs extensão vs Content-Type): double extension (`.php.jpg`), null byte no filename (`shell.php%00.jpg`), polyglot (`GIF89a;` + `<?php`), bypass de Content-Type;
(2) Execução de servidor: upload de webshell em PHP, JSP ou ASPX conforme o stack;
(3) Path traversal no nome do arquivo: uso de ../ no filename para escrever em diretórios arbitrários;
(4) Zip slip: arquivo ZIP com paths traversal internos;
(5) SSRF via processamento: SVG com entidade externa, PDF com link para interno;
(6) Denial of service: arquivo enorme, zip bomb, imagem que esgota CPU no decompress;
(7) XXE via arquivo estruturado: SVG, XML e documentos OOXML (docx/xlsx são zips com XML) com entidade externa;
(8) SSRF/RCE em pipeline de mídia: ImageTragick (ImageMagick) e ffmpeg com input malicioso;
(9) Pixel flood / decompression bomb de imagem: dimensões enormes que esgotam memória no decode.

Formate com payload e critério de confirmação de vulnerabilidade.

Segurança operacional: use amostras pequenas e ambiente de teste; um webshell plantado precisa ser removido após o PoC; zip bomb / decompression bomb podem derrubar o ambiente — não execute em produção.
```

## Saída esperada
Matriz de ataques de upload com payloads e critérios de confirmação de vulnerabilidade.

## Formato de registro
Achados confirmados devem ser registrados em `templates/registro-de-achado.yaml` seguindo o schema em `AUDITORIA.md`. Use o campo `prompt_origem` com o caminho relativo deste arquivo.

## Onde usar no fluxo
Fase 3 - Análise dinâmica. Use antes de testar manualmente endpoints de upload ou importação de dados. Consulte `AUDITORIA.md` para o checklist completo.
