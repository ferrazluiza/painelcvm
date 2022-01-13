import requests
import os
from bs4 import BeautifulSoup as bs
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def pagina_inicial():
    return """
        <h1><p>Olá!</h1> 
        Este site faz uma coleta automatizada de relatórios publicados no sistema da CVM a cada 5 minutos. Para saber mais sobre os filtros utilizados,
        <p>
         você pode ler a sessão "Quem & como".</p> 
        <p>Funcionalidade futura: alerta pelo Telegram de fatos relevantes.</p>
        <p></p>
        <p)Se tiver alguma ideia de como melhorar o serviço, manda um e-mail para luizaferraz@pm.me.
        <a href="/quemcomo">Quem & como</a>
    """
  
  
@app.route("/quemcomo")
def quemcomo():
    return """<h1>Quem & Como?</h1>
        <p>Este site foi criado por mim, Luiza Ferraz. Sou jornalista e trabalho como repórter no Pipeline, coluna de negócios do Valor Econômico. Mais informações sobre a criação do servio em breve.</p>
        <a href="/">Página Inicial</a>
    """
