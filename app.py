from flask import Flask, request, render_template
from src.data import get_data

app = Flask(__name__)

@app.route("/sobre")
def sobre():
    return """<h1>Sobre</h1>
        <p>O Painel CVM é um projeto open-source que resolve uma dor de cabeça para quem cobre mercado financeiro: a imensa quantidade
        <br>de comunicados (muitas vezes não tão interessantes para nós, jornalistas) que as empresas sobem no sistema da Comissão de Valores Mobiliários (CVM).</p>
        <p>Para conseguir dar uma agilizada nesse processo de procura de agulha no palheiro, eu fiz uma seleção prévia de alguns filtros e disponibilizei
        <br>o resultado desses filtros em uma tabela, essa que você consegue ver na Página Inicial.</p>
        <p>Esse trabalho só foi possível graças à ajuda de Álvaro Justen, Eduardo Cuducos, Luiz Henrique Mendes e Felipe Whitaker.
        <br>Meu nome é Luiza Ferraz, mas pode só chamar de Lu. Você me encontra no <a href="https://pipelinevalor.globo.com/">Pipeline, site de negócios do Valor Econômico</a> e,
        <br>de vez em quando, no <a href="https://twitter.com/luizaferrazc">Twitter</a>. Até mais!</p>
        <p></p>
        <br>
        <a href="/">Página Inicial</a> | <a href="/comofoifeito">Como foi feito</a>
    """

@app.route("/comofoifeito")
def comofoifeito():
    return """<h1>Como foi feito</h1>
        <p>Opa, essa página tá em andamento. Mas só pra você não sair de mãos abanando, fique à vontade para olhar
        <br>o repositório desse projeto. É só <a href="https://github.com/ferrazluiza/painelcvm">clicar aqui</a>.</p>
        <a href="/">Página Inicial</a> | <a href="/sobre">Sobre</a>
    """

@app.route("/")
def pagina_inicial():
    table = get_data().drop(columns = ["filtro", "Código_CVM", "Espécie", "Data_Referência", "Status", "V", "Modalidade"]).sort_values(by = "Data_Entrega", ascending = False)
    return f"""
        <h1><p>Painel CVM</h1> 
        Oi! Aqui embaixo você encontra os últimos comunicados que as empresas subiram na Comissão de Valores Mobiliários (CVM).
        <br>Para saber mais sobre este projeto, navegue pelos links abaixo.
        <br><br>
        <a href="/sobre">Sobre</a> | <a href="/comofoifeito">Como foi feito</a>
        <br><br><br><br><br><br>
        {table.to_html(escape=False, index=False)}
    """



