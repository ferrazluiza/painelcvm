import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

remove_span = re.compile(r"\<\/?spanOrder\>") # item que não sei o que é, mas que aparece várias vezes; quero tirar para visualizar melhor
extract_document = re.compile(r"frmExibirArquivoIPEExterno\.aspx\?NumeroProtocoloEntrega=\d+") # parte do link para visualizar o documento
remove_date = re.compile(r"\<spanOrder\>\d+\<\/spanOrder\> ") # mais uma vez aparecendo

def get_link(html):
  global extract_document
  url_link = extract_document.findall(html)
  if len(url_link) > 0:
    return f'<a href="https://www.rad.cvm.gov.br/ENET/{url_link[0]}">documento</a>'
  return "no document"

def get_date(date, fmt):
  global remove_date
  re_date = remove_date.sub("", date)
  if re.match(r"\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}", re_date):
    fmt = "%d/%m/%Y %H:%M"
  elif re.match(r"\d{2}\/\d{2}\/\d{4}", re_date):
    fmt = "%d/%m/%Y"
  elif re.match(r"\d{4}", re_date):
    fmt = "%Y"
  else:
    print(re_date)
    return None
  return datetime.strptime(re_date, fmt)

def get_data():

    # vendo se as variáveis que criei funcionam como fitro
    cookies = {}
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'x-dtpc': "28\{263272083_726h32vFTURCFHLJNDVGUPAKUMUVDFMEKPUGADS-0e0\}",
        'Sec-GPC': '1',
        'Origin': 'https://www.rad.cvm.gov.br',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.rad.cvm.gov.br/ENET/frmConsultaExternaCVM.aspx?tipoconsulta=CVM',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    # Criando um dicionário com os filtros que eu quero utilizar
    filtros = dict(
        # companhia_aberta = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'EST_-1,IPE_-1_-1_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        anuncio_de_encerramento = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_89_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        anuncio_de_inicio = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_90_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        aquisicao_alienacao = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_51_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        aumento_de_capital_subscricao = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_96_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        aviso_ao_mercado = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_91_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        comunicado_inicio_oferta_esforcorestrito = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_100_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        demonstracoes_anualcompleta = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_37_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        demonstacoes_intermediaria = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_46_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        esclarecimento_cvmb3 = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_112_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        outros_comunicados = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_53_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        press_release = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_-1_29_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        fato_relevante = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_4_-1_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
        comunicado_mercado = "{ dataDe: '', dataAte: '' , empresa: '', setorAtividade: '-1', categoriaEmissor: '-1', situacaoEmissor: '-1', tipoParticipante: '1', dataReferencia: '', categoria: 'IPE_6_-1_-1', periodo: '0', horaIni: '', horaFim: '', palavraChave:'',ultimaDtRef:'false', tipoEmpresa:'0', token: '', versaoCaptcha: ''}",
    )

    columns = ["filtro", "Código_CVM", "Empresa", "Categoria", "Tipo", "Espécie", "Data_Referência", "Data_Entrega", "Status", "V", "Modalidade", "Ações", "Resultado"]

    # colunas a serem limpas
    id_column = "Código_CVM"
    span_column = "Espécie"
    global remove_span
    document_column = "Ações"
    
    date_columns = {"Data_Referência": "%d/%m/%Y", "Data_Entrega": "%d/%m/%Y %H:%M"} # explicando como eu quero que o programa leia a data que tá na tabela (útil para filtro por hora mais pra frente)

    rows = []
    for nome, filtro_data in filtros.items():
      response = requests.post('https://www.rad.cvm.gov.br/ENET/frmConsultaExternaCVM.aspx/ListarDocumentos', headers=headers, data=filtro_data, cookies = cookies)
      dados = ("&*" + response.json()['d']['dados']).split("$&")[:-1]
      # como deu pra ver no split lá em cima, cada 12 linhas dizem respeito aos dados de uma única empresa
      # então eu quero que o programa leve em conta cada 12 tempos como uma linha no df 
      for i in range(0, len(dados), 12): 
        rows.append([nome, *dados[i:i + 12]])

    # limpando as colunas
    df = pd.DataFrame(data = rows, columns = columns)
    df[id_column] = df[id_column].apply(lambda x: x[2:])
    df[document_column] = df[document_column].apply(get_link)
    df[span_column] = df[span_column].apply(lambda x: remove_span.sub("", x))

    for col, fmt in date_columns.items():
      df[col] = df[col].apply(get_date, fmt = fmt)

    return df