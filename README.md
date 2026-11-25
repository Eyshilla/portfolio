# Portfólio da Eyshilla

Portfólio pessoal em pixel art: um único `index.html` com HTML, CSS e JavaScript puros, sem build nem dependências (só as fontes do Google Fonts).

## Como editar o conteúdo

Todo o conteúdo fica no array `PADRAO`, no início do `<script>` do `index.html`. Cada linha tem as chaves `tipo`, `titulo`, `detalhe`, `descricao`, `tags`, `link`, `arquivo`, `miniatura` e `mostrar`.

- A ordem das linhas é a ordem na tela.
- Para esconder uma linha, use `mostrar: "não"`.
- Separe as etiquetas com ponto e vírgula (`"BI; Dados"`).
- Coloque os PDFs e imagens dos certificados na pasta `certificados/` e informe só o nome do arquivo em `arquivo` ou `miniatura`.

## Editar pelo Google Planilhas (sem mexer no código)

Você pode trocar o conteúdo do site editando uma planilha, em vez do `PADRAO`. O arquivo `conteudo-portfolio.xlsx` já vem preenchido com os dados atuais.

1. Baixe o arquivo `conteudo-portfolio.xlsx` deste repositório.
2. Abra o [Google Planilhas](https://sheets.google.com), clique em **Arquivo > Importar > Fazer upload** e envie o `.xlsx`. Escolha **Criar nova planilha**.
3. Na planilha nova, clique em **Arquivo > Compartilhar > Publicar na Web**.
4. Na primeira caixa, escolha a aba **Dados**. Na segunda, escolha **Valores separados por vírgula (.csv)**. Clique em **Publicar** e confirme.
5. Copie o link que aparece (ele termina em `output=csv`).
6. No GitHub, abra o `index.html`, clique no lápis (**Edit**) e cole o link entre as aspas de `PLANILHA_URL`, no início do `<script>`:
   ```js
   const PLANILHA_URL = 'https://docs.google.com/spreadsheets/d/e/.../pub?gid=0&single=true&output=csv';
   ```
   Clique em **Commit changes**. Esta é a única edição de código necessária.
7. A partir daí, tudo o que você mudar na aba **Dados** aparece no site em alguns minutos (o Google pode levar até 5 minutos para atualizar o link publicado).

Dicas da planilha:

- A aba **Como usar** explica cada `tipo` e as colunas que ele usa.
- Para esconder uma linha, escolha `não` na coluna `mostrar`. As linhas que começam com `EXEMPLO` já vêm escondidas: copie uma delas para criar um item novo.
- Não renomeie a coluna `tipo`. Sem ela, ou se a planilha não carregar, o site usa os dados do `PADRAO` como reserva.

### Certificados (PDFs e imagens)

1. No GitHub, abra a pasta `certificados/` e clique em **Add file > Upload files**.
2. Arraste os PDFs e imagens e clique em **Commit changes**.
3. Na planilha, escreva só o nome do arquivo na coluna `arquivo` (ex.: `excel.pdf`). Se o certificado tiver uma página de validação, use a coluna `link`, que tem prioridade sobre `arquivo`.
4. Para escolher a imagem do card, escreva o nome de uma imagem da pasta em `miniatura` (ex.: `excel.png`). Sem miniatura, o card mostra a própria imagem (se o certificado for `.png`, `.jpg`, `.webp`...) ou um ícone de PDF/LINK.

### Conferir a versão

Abra o site com `?status` no fim do endereço, por exemplo `https://<seu-usuario>.github.io/<nome-do-repositorio>/?status`. No fim da página aparece a versão e de onde veio o conteúdo:

- `planilha carregada (N linhas)`: o site está lendo a planilha;
- `dados do próprio arquivo`: `PLANILHA_URL` está vazio;
- `planilha indisponível (motivo), usando dados de reserva`: a planilha não carregou e o site usou o `PADRAO`.

Para gerar o `conteudo-portfolio.xlsx` de novo a partir do `PADRAO`: `pip install openpyxl` e `python3 tools/gerar_planilha.py`.

## Como publicar no GitHub Pages

1. No repositório, abra **Settings > Pages**.
2. Em **Build and deployment > Source**, escolha **Deploy from a branch**.
3. Selecione a branch **main** e a pasta **/ (root)** e clique em **Save**.
4. Depois de alguns minutos o site fica disponível em `https://<seu-usuario>.github.io/<nome-do-repositorio>/`.

Para ver localmente, basta abrir o `index.html` no navegador.
