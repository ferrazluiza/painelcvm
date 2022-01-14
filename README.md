# pt

Bem vinde! Este é um projeto que apoia o jornalismo profissional, porque o acesso à informação de qualidade muda vidas. Apoie e defenda a imprensa. Assine jornais, revistas, newsletters e podcasts. Informe-se antes de opinar e cheque informações antes de compartilhar, para não passar desinformação a diante.

## Sobre o projeto

O [Painel CVM](https://painelcvm.herokuapp.com/) é um serviço gratuito feito para facilitar o acesso a comunicados relevantes emitidos por companhias brasileiras abertas no sistema da Comissão de Valores Mobiliários (CVM). Ele foi pensado como projeto final de conclusão do primeiro semestre da pós graduação de Jornalismo de Dados, Automação e Data Storytelling do Insper. E foi possível graças à ajuda de: [Álvaro Justen](https://github.com/turicas), [Eduardo Cuducos](https://twitter.com/cuducos), [Luiz Henrique Mendes](https://www.linkedin.com/in/luiz-henrique-mendes-76776821/) e [Felipe Whitaker](https://github.com/felipewhitaker).

## Como funciona

Basta atualizar a página para visualizar, ordenado do mais recente para o mais antigo, todos os comunicados emitidos pelas empresas. Então para ver se tem alguma novidade quando você já estiver com o site aberto, dá um F5 ;).

## Bibliotecas utilizadas

- `requests`
- `beautifulsoup4`
- `pandas`
- `os`
- `re`
- `datetime`

## Reproduzindo localmente

1. `git clone https://github.com/ferrazluiza/painelcvm`
2. `pip install -r requirements.txt`
3. `flask run` 
4. E você deveria conseguir ver: `Running on http://127.0.0.1:5000/`

## O que vem por aí
- Opção de visualização apenas com empresas do Ibovespa
- Bot no telegram com aviso de fatos relevantes e comunicados ao mercado de empresas do índice

## Contribua!

- Faça o fork do projeto (https://github.com/ferrazluiza/painelcvm)

    `git clone https://github.com/ferrazluiza/painelcvm`
- Crie uma branch para sua modificação
- Faça o commit
- Push
- Crie um novo Pull Request
