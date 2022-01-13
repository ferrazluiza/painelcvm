from flask import Flask, request, render_template
from .data import get_data

app = Flask(__name__)

@app.route("/quemcomo")
def quemcomo():
    return """<h1>Quem & Como?</h1>
        <p>Este site foi criado por mim, Luiza Ferraz. Sou jornalista e trabalho como repórter no Pipeline, coluna de negócios do Valor Econômico. Mais informações sobre a criação do servio em breve.</p>
        <a href="/">Página Inicial</a>
    """

@app.route("/")
def pagina_inicial():
    table = get_data().drop(columns = ["filtro", "Código_CVM", "Espécie", "Data_Referência", "Status", "V", "Modalidade"])
    return f"""
        <h1><p>Dashboard CVM</h1> 
        Este site faz uma coleta automatizada de relatórios publicados no sistema da CVM a cada 5 minutos. Para saber mais sobre os filtros utilizados,
        <p>
         você pode ler a sessão "Quem & como".</p> 
        <p>Funcionalidade futura: alerta pelo Telegram de fatos relevantes.</p>
        <p></p>
        <p>Se tiver alguma ideia de como melhorar o serviço, manda um e-mail para luizaferraz@pm.me.</p>
        <a href="/quemcomo">Quem & como</a>
        <br><br><br><br><br><br>
        {table.to_html(escape=False, index=False)}
    """



