# Portfólio da Eyshilla

Portfólio pessoal em pixel art: um único `index.html` com HTML, CSS e JavaScript puros, sem build nem dependências (só as fontes do Google Fonts).

## Como editar o conteúdo

Todo o conteúdo fica no array `PADRAO`, no início do `<script>` do `index.html`. Cada linha tem as chaves `tipo`, `titulo`, `detalhe`, `descricao`, `tags`, `link`, `arquivo`, `miniatura` e `mostrar`.

- A ordem das linhas é a ordem na tela.
- Para esconder uma linha, use `mostrar: "não"`.
- Separe as etiquetas com ponto e vírgula (`"BI; Dados"`).
- Coloque os PDFs e imagens dos certificados na pasta `certificados/` e informe só o nome do arquivo em `arquivo` ou `miniatura`.

## Como publicar no GitHub Pages

1. No repositório, abra **Settings > Pages**.
2. Em **Build and deployment > Source**, escolha **Deploy from a branch**.
3. Selecione a branch **main** e a pasta **/ (root)** e clique em **Save**.
4. Depois de alguns minutos o site fica disponível em `https://<seu-usuario>.github.io/<nome-do-repositorio>/`.

Para ver localmente, basta abrir o `index.html` no navegador.
