# -*- coding: utf-8 -*-
import os
import json
import random
import string
from datetime import datetime, timedelta
from typing import Union
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
# import re
from django.core.mail import send_mail
from django.db import connection


BOOLEAN_CHOICES = (
    ('N', 'Não'),
    ('S', 'Sim'),
)

dias_da_semana = (
    ('1', 'DOMINGO'),
    ('2', 'SEGUNDA'),
    ('3', 'TERÇA      '),
    ('4', 'QUARTA   '),
    ('5', 'QUINTA    '),
    ('6', 'SEXTA      '),
    ('7', 'SÁBADO     ')
)

# Get data from .env file
with open('.env') as f:
    for line in f:
        if len(line) > 0 and not line.startswith('#') and not line.startswith('\n'):
            key, value = line.strip().split('=')
            os.environ[key] = value

def carregar_dot_env():
    # Get data from .env file
    with open('.env') as f:
        for line in f:
            if len(line) > 0 and not line.startswith('#') and not line.startswith('\n'):
                key, value = line.strip().split('=')
                os.environ[key] = value


def float_format(value, places=2):
    if places == 2:
        value = '{:15.2f}'.format(value).lstrip()
    elif places == 3:
        value = '{:15.3f}'.format(value).lstrip()

    value = value.replace('.', ',')

    return value

def validar_hora(data):

    if len(data) < 5:
        return "NOK"

    hora = int(data[0:2])
    minuto = int(data[3:5])

    validade = True

    if hora > 23:
        validade = False

    if minuto > 59:
        validade = False

    if validade:
        return "OK"
    else:
        return "NOK"

def validar_data(data):
    if len(data) < 10:
        return "NOK"

    dia = int(data[0:2])
    mes = int(data[3:5])
    ano = int(data[6:10])

    validade = True

    i = 0
    while validade and i == 0:
        if (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0:
            bissexto = "sim"
        else:
            bissexto = "nao"

        if mes < 1 or mes > 12:
            validade = False

        if dia > 31 or ((mes == 4 or mes == 6 or mes == 9 or mes == 11) and dia > 30):
            validade = False

        if (mes == 2 and bissexto == "nao" and dia > 28) or (mes == 2 and bissexto == "sim" and dia > 29):
            validade = False

        i += 1

    if validade:
        return "OK"
    else:
        return "NOK"

def totalizar_horas(total, tempo):
    tot = total
    tmp = tempo

    while len(tot) == 7:
        tot = "0" + tot

    if len(tmp) == 7:
        tmp = "0" + tmp
    tot_hor = int(tot[0:2])
    tot_min = int(tot[3:5])
    tot_seg = int(tot[6:8])

    tmp_hor = int(tmp[0:2])
    tmp_min = int(tmp[3:5])
    tmp_seg = int(tmp[6:8])

    tot_hor += tmp_hor
    tot_min += tmp_min
    tot_seg += tmp_seg

    # while tot_seg > 60:
    #     tot_min += 1
    #     tot_seg -= 60

    while tot_min > 60:
        tot_hor += 1
        tot_min -= 60

    if len(str(tot_hor)) == 1:
        retorno = "0" + str(tot_hor)
    else:
        retorno = str(tot_hor)

    if len(str(tot_min)) == 1:
        retorno += ":0" + str(tot_min)
    else:
        retorno += ":" + str(tot_min)

    if len(str(tot_seg)) == 1:
        retorno += ":0" + str(tot_seg)
    else:
        retorno += ":" + str(tot_seg)

    return retorno


def str_to_time(texto):
    return datetime.strptime(texto, '%H::%M::%S').time()

def ajusta_acento(texto):
    retorno = texto

    retorno = retorno.replace('\\xc1', 'Á')
    retorno = retorno.replace('\\xc2', 'Â')
    retorno = retorno.replace('\\xc3', 'Ã')
    retorno = retorno.replace('\\xc7', 'Ç')
    retorno = retorno.replace('\\xc9', 'É')
    retorno = retorno.replace("\\xe1", "á")
    retorno = retorno.replace('\\xe2', 'â')
    retorno = retorno.replace('\\xe3', 'ã')
    retorno = retorno.replace("\\xe4", "ä")
    retorno = retorno.replace('\\xe7', 'ç')
    retorno = retorno.replace('\\xe9', 'é')
    retorno = retorno.replace('\\xed', 'í')
    retorno = retorno.replace('\\xf3', 'ó')
    retorno = retorno.replace('\\xfa', 'ú')
    retorno = retorno.replace('\\xcd', 'Í')
    retorno = retorno.replace('\\xd3', 'Ó')
    retorno = retorno.replace('\\xda', 'Ú')
    retorno = retorno.replace('\\xf5', 'õ')
    retorno = retorno.replace('\\xd5', 'Õ')
    retorno = retorno.replace('\\xf4', 'ô')
    retorno = retorno.replace('\\xea', 'ê')
    retorno = retorno.replace('\\xd4', 'Ô')
    retorno = retorno.replace('\\xdb', 'Û')
    retorno = retorno.replace('\\xeb', 'ë')
    retorno = retorno.replace('\\xef', 'ï')
    retorno = retorno.replace('\\xf6', 'ö')
    retorno = retorno.replace('\\xfc', 'ü')
    retorno = retorno.replace('\\xc4', 'Ä')
    retorno = retorno.replace('\\xcb', 'Ë')
    retorno = retorno.replace('\\xcf', 'Ï')
    retorno = retorno.replace('\\xd6', 'Ö')
    retorno = retorno.replace('\\xdc', 'Ü')
    retorno = retorno.replace('\\u2022', '•')

    return retorno


def formata_data_str(data_str, formato):
    return datetime.strptime(str(data_str), formato)

def formata_data_banco(data_filter):
    # Verifica qual a plataforma
    plataforma = retorna_plataforma()

    if not data_filter:
        dia = "30"
        mes = "12"
        ano = "1899"
    else:
        dia = data_filter[0:2]
        mes = data_filter[3:5]
        ano = data_filter[6:10]

    retorno = ""
    if plataforma == "ORACLE":
        retorno = "TO_DATE(" + dia + "/" + mes + "/" + ano + ")"
    elif plataforma == "MYSQL":
        retorno = ano + "-" + mes + "-" + dia
    elif plataforma == "MSSQL":
        retorno = ano + "-" + mes + "-" + dia
    else:
        retorno = mes + "/" + dia + "/" + ano

    return retorno

def formata_data_hora_banco(data_hora_filter):
    data_hora_filter = str(data_hora_filter)

    # Verifica qual a plataforma
    # plataforma = retorna_plataforma()

    if len(data_hora_filter) <= 6:
        dia = "30"
        mes = "12"
        ano = "1899"

        hora = data_hora_filter[0:2]
        minuto = data_hora_filter[3:5]
        segundo = "00"
    else:
        dia = data_hora_filter[0:2]
        mes = data_hora_filter[3:5]
        ano = data_hora_filter[6:10]

        hora = data_hora_filter[11:13]
        minuto = data_hora_filter[14:16]
        segundo = data_hora_filter[17:19]

        if not segundo:
            segundo = "00"

    retorno = ""
    # if plataforma == "ORACLE":
    #     retorno = "TO_DATE(" + dia + "/" + mes + "/" + ano + " " + hora + ":" + minuto + ":" + segundo + ")"
    # elif plataforma == "MYSQL":
    retorno = ano + "-" + mes + "-" + dia + " " + hora + ":" + minuto + ":" + segundo
    # elif plataforma == "MSSQL":
    #     retorno = ano + "-" + mes + "-" + dia + " " + hora + ":" + minuto + ":" + segundo
    # else:
    #     retorno = mes + "/" + dia + "/" + ano + " " + hora + ":" + minuto + ":" + segundo

    return retorno

def converte_datetime_br(datetime):
    data = str(datetime)

    ano = data[0:4]
    mes = data[5:7]
    dia = data[8:10]
    hora = data[11:]

    convertido = "{}/{}/{} - {}".format(dia, mes, ano, hora)

    return convertido

def retorna_ip_fotos():
#    return 'http://127.0.0.1:8887/'
     return 'http://localhost:9000/media/fotos_cadastros/'

def retorna_informacao_parametro(request, field):
    sql_script = "SELECT "
    sql_script += field + " "
    sql_script += "FROM PARAMETRO "
    sql_script += "WHERE "
    sql_script += "EMPRICODONLINE=" + request.session['usuario_cod_empresa']

    cursor = connection.cursor()
    cursor.execute(sql_script)

    results = dict_fetch_all(cursor)

    valor_campo = ""
    for data in results:
        valor_campo = data[field]

    return valor_campo

def find_index(dicts, key, value):
    class Null: pass
    for i, d in enumerate(dicts):
        if d.get(key, Null) == value:
            return i
    else:
        return -1

def date_to_str_sql(date_string):
    try:
        date_object = str(date_string)
        date_object = date_object[6:10] + '-' + date_object[3:5] + '-' + date_object[0:2]
        return date_object
    except Exception as e:
        return ""
        
def retorna_mensagem_status(status, entrada_saida):
    if not entrada_saida:
        entrada_saida = "I"

    if not status:
        status = "AN"

    value = ""

    if status == "AC":
        value = "Acesso Não Utilizado"
    elif status == "AN":
        value = "Acesso Negado"
    elif status == "CE":
        value = "Lib. Manual Entrada"
    elif status == "CS":
        value = "Lib. Manual Saída"
    elif status == "LE":
        value = "Liberada Entrada"
    elif status == "LS":
        value = "Liberada Saída"
    elif status == "LF" or status == "LB":
        value = "Acesso Liberado"

        if entrada_saida == "E":
            value = "Liberada Entrada"

        if entrada_saida == "S":
            value = "Liberada Saída"
    elif status == "E":
        value = "Entrada"
    elif status == "S":
        value = "Saída"
    elif status == "BL":
        value = "Bloqueado"
    elif status == "JN":
        value = "Fora de Jornada"
    elif status == "TN":
        value = "Turno não cadastrado"
    elif status == "FT":
        value = "Fora de Turno"
    elif status == "ST":
        value = "Sem turno no dia"
    elif status == "BR":
        value = "Bloqueio por Reentrada"
    elif status == "NC":
        value = "Não Cadastrado"
    elif status == "PV":
        value = "Provisório Vencido"
    elif status == "FJ":
        value = "Fora de Jornada"
    elif status == "SJ":
        value = "Jornada não Definida"
    elif status == "AN":
        value = "Acesso não autorizado"
    elif status == "CV":
        value = "Fora da Validade"
    elif status == "VI":
        value = "Via inválida"
    elif status == "CR":
        value = "Créditos Esgotados"
    elif status == "AD":
        value = "Acessos diários esgotados"
    elif status == "CA":
        value = "Crédito Avulso"
    elif status == "ED":
        value = "Erro de Leitura"
    elif status == "BR":
        value = "Bloqueio por Reentrada"
    elif status == "EV":
        value = "Entrada Visitante"
    elif status == "SV":
        value = "Saída Visitante"
    elif status == "PT":
        value = "Registro de Ponto"
    elif status == "JP":
        value = "Fora de Jornada Ponto"
    elif status == "TP":
        value = "Fora de Turno Ponto"
    elif status == "NH":
        value = "Não Habilitado"
    elif status == "SI":
        value = "Senha Incorreta"
    elif status == "AL":
        value = "Ambiente Lotado"
    elif status == "S1":
        if entrada_saida == "O":
            value = "Sensor 1 ON"
        elif entrada_saida == "F":
            value = "Sensor 1 OFF"
    elif status == "S2":
        if entrada_saida == "O":
            value = "Sensor 2 ON"
        elif entrada_saida == "F":
            value = "Sensor 2 OFF"
    elif status == "B1":
        if entrada_saida == "O":
            value = "Botão 1 ON"
        elif entrada_saida == "F":
            value = "Botão 1 OFF"
    elif status == "B2":
        if entrada_saida == "O":
            value = "Botão 2 ON"
        elif entrada_saida == "F":
            value = "Botão 2 OFF"
    elif status == "V1":
        value = "Sensor 1 VIOLADO"
    elif status == "V2":
        value = "Sensor 2 VIOLADO"
    elif status == "T1":
        value = "Sensor 1 ABERTO"
    elif status == "T2":
        value = "Sensor 2 ABERTO"
    elif status == "F0":
        value = "Função 0 Registrada"
    elif status == "F1":
        value = "Função 1 Registrada"
    elif status == "F2":
        value = "Função 2 Registrada"
    elif status == "F3":
        value = "Função 3 Registrada"
    elif status == "F4":
        value = "Função 4 Registrada"
    elif status == "F5":
        value = "Função 5 Registrada"
    elif status == "F6":
        value = "Função 6 Registrada"
    elif status == "F7":
        value = "Função 7 Registrada"
    elif status == "F8":
        value = "Função 8 Registrada"
    elif status == "F9":
        value = "Função 9 Registrada"

    if not value:
        value = "Acesso Negado"

    return value

# -= RETORNA_PLATAFORMA =-
def retorna_plataforma():
    sql_script = "SELECT parma60plataforma FROM parametro WHERE empricodonline=1"
    cursor = connection.cursor()
    cursor.execute(sql_script)
    results = dict_fetch_all(cursor)

    plataforma = ""
    for data in results:
        plataforma = data['parma60plataforma']

    return plataforma

# -= GET_OBJECT_OR_NONE =-
def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

# -= SALVAR_ARQUIVO =-
def salvar_arquivo(folder, file_to_write):
    # EXEMPLO: http://code.runnable.com/UpUJp-2XvjUuAABb/how-to-use-default-filesystemstorage-class-in-django-for-python

    file_content = file_to_write.read()

    #  Salvar arquivo na pasta temporária
    file_storage = FileSystemStorage(location=folder)
    file_storage.file_permissions_mode = 644

    #  Salvar arquivo na pasta temporária
    file_name = str(file_to_write)
    saved_file = file_storage.save(file_name, ContentFile(file_content))

    return saved_file

def enviar_email(destinatario, assunto, mensagem):
    send_mail(
        assunto,
        mensagem,
        settings.EMAIL_HOST_USER,
        [destinatario],
        fail_silently=False,
    )

def gerar_senha_aleatoria():
    tamanho_senha = 5
    caracteres_permitidos = string.ascii_lowercase
    senha_aleatoria = ''.join(random.choice(caracteres_permitidos) for i in range(tamanho_senha))
    return senha_aleatoria

def calcula_codigo(tabela, campo, campos_id, valores_id):
    campos_id_str = ""
    for campo_id in campos_id:
        if not campos_id_str:
            campos_id_str += f"{campo_id} = %s "
        else:
            campos_id_str += f" AND {campo_id} = %s "
    
    if campos_id_str:
        sql_script = f"SELECT COALESCE(MAX({campo}), 0)+1 AS NEXT_KEY FROM {tabela} WHERE {campos_id_str}"
    else:
        sql_script = f"SELECT COALESCE(MAX({campo}), 0)+1 AS NEXT_KEY FROM {tabela}"
    
    cursor = connection.cursor()
    cursor.execute(sql_script, valores_id)
    results = dict_fetch_all(cursor)

    codigo = 0
    for data in results:
        codigo = data['NEXT_KEY']

    return codigo

def calcula_codigo_sem_empresacod(tabela, campo):
    sql_script = f"SELECT COALESCE(MAX({campo}), 0)+1 AS NEXT_KEY FROM {tabela}"
    cursor = connection.cursor()
    cursor.execute(sql_script)
    results = dict_fetch_all(cursor)

    codigo = 0
    for data in results:
        codigo = data['NEXT_KEY']

    return codigo

def convert_boolean_to_sn(value):
        if value == 'on':
            return 'S'
        else:
            return 'N'

def adiciona_dias(input_date_str, nro_dias):
    # Convert the input date string to a datetime object
    input_date = datetime.strptime(input_date_str, '%Y-%m-%d')
    # Add one day to the date
    new_date = input_date + timedelta(days=nro_dias)
    # Format the new date as a string in the same format
    new_date_str = new_date.strftime('%Y-%m-%d')

    return new_date_str


def adiciona_meses(start_date, months_to_add):
    year = start_date.year + (start_date.month + months_to_add - 1) // 12
    month = (start_date.month + months_to_add - 1) % 12 + 1
    day = start_date.day

    # Handle cases where the day exceeds the number of days in the new month
    while day > 28:
        try:
            new_date = datetime(year, month, day)
            break
        except ValueError:
            day -= 1

    return new_date
        
# ------------------------
# ❗ FUNÇÕES BANCO DE 🎲 ❗
# ------------------------


def retorna_sql_json(sql, parametros=[]):
    cursor_ret = connection.cursor()
    
    if parametros:
        cursor_ret.execute(sql, parametros)
    else:
        cursor_ret.execute(sql)

    resultado = dict_fetch_all(cursor_ret)

    return resultado

def dict_to_json(dict_data):
    post_data = dict_data
    json_data = json.dumps(post_data)
    data_object = json.loads(json_data)      
    return data_object

def sql_executa(sql, parametros=[]):
    cursor_ret = connection.cursor()

    if parametros:
        cursor_ret.execute(sql, parametros)
    else:
        cursor_ret.execute(sql)

def sql_localiza(tabela, field, clausula):
    sql_script = "SELECT "
    sql_script += field + " "
    sql_script += "FROM " + tabela + " "
    sql_script += "WHERE "
    sql_script += clausula

    cursor = connection.cursor()
    cursor.execute(sql_script)

    results = dict_fetch_all(cursor)

    valor_campo = ""
    for data in results:
        valor_campo = data[field]

    return valor_campo

def query_insert(nome_tabela, form):
    # Montar os valores para inserção
    campos = []
    valores = []

    # Percorre os campos do form, buscando seus valores
    for campo in form.fields:
        valor = form.data.get(campo, "")
        
        # Ignorar campos vazios ou nulos
        if valor is not None and valor != "":
            campos.append(campo)
            valores.append(valor)

    # Montar a query de INSERT dinamicamente
    campos_str = ', '.join(campos)
    placeholders = ', '.join(['%s'] * len(valores))
    query = f"INSERT INTO {nome_tabela} ({campos_str}) VALUES ({placeholders});"
    
    try:
        # Print da query para debug
        print("🎲 Query:", query)
        print("🎲 Valores:", valores)
        
        with connection.cursor() as cursor:
            cursor.execute(query, valores)
        
        # Certificar-se de que a transação seja commitada
        connection.commit()
        return True  # Inserção bem-sucedida
    
    except Exception as e:
        # Print do erro caso ocorra
        print("🚨 Erro ao inserir:", str(e))
        connection.rollback()  # Reverter a transação em caso de erro
        return False  # Inserção falhou
    
def query_update(nome_tabela, form, campos_ids, valores_ids):
    # Montar os valores para atualização
    campos_e_valores = []

    for campo in form.fields:
        valor = form.data.get(campo, "")
        
        # Ignorar campos vazios ou nulos
        if valor is not None and valor != "":
            campos_e_valores.append((campo, valor))

    # Montar a lista de campos para a cláusula SET
    set_statements = ', '.join([f"{campo} = %s" for campo, _ in campos_e_valores])
    valores_set = [valor for _, valor in campos_e_valores]

    # Montar a query de UPDATE dinamicamente
    query = f"UPDATE {nome_tabela} SET {set_statements} WHERE "

    # Adicionar as condições WHERE para os campos de IDs
    for campo_id in campos_ids:
        query += f"{campo_id} = %s AND "
    
    query = query.rstrip("AND ")  # Remover o último "AND"

    # Valores para os campos de IDs
    valores_ids = valores_ids[:len(campos_ids)]  # Garantir que tenhamos valores suficientes
    valores = valores_set + valores_ids

    try:
        # Executar a query no DB
        print("Query:", query)
        print("Valores:", valores)
        with connection.cursor() as cursor:
            cursor.execute(query, valores)
        
        # Certificar-se de que a transação seja commitada
        connection.commit()
    except Exception as e:
        print("Erro ao inserir:", str(e))
        connection.rollback()  # Reverter a transação em caso de erro
        return False  # Inserção falhou

def query_delete(nome_tabela, campos_ids, valores_ids):
    # Montar a query de DELETE dinamicamente
    query = f"DELETE FROM {nome_tabela} WHERE "

    # Adicionar as condições WHERE para os campos de IDs
    for campo_id in campos_ids:
        query += f"{campo_id} = %s AND "
    
    query = query.rstrip("AND ")  # Remover o último "AND"

    # Valores para os campos de IDs
    valores = valores_ids[:len(campos_ids)]  # Garantir que tenhamos valores suficientes

    # Executar a query no DB
    with connection.cursor() as cursor:
        cursor.execute(query, valores)
    
    # Certificar-se de que a transação seja commitada
    connection.commit()
    
def next_key_value(table, field, extra_filter):
    autoinc_field = 0

    sql_script = "SELECT COALESCE(MAX("+field+"), 0)+1 AS NEXT_KEY "
    sql_script += "FROM " + table + " "
    if extra_filter:
        sql_script += "WHERE " + extra_filter

    cursor = connection.cursor()
    cursor.execute(sql_script)

    data = dict_fetch_all(cursor)

    if data:
        for row in data:
            autoinc_field = int(row['NEXT_KEY'])

    return autoinc_field

def dict_fetch_all(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    # print("💡 dict_fetch_all->columns: ", columns)
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_day_of_week(date_string):
    try:
        # Parse the input date string into a datetime object
        date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        
        # Get the day of the week as an integer (0 = Monday, 6 = Sunday)
        day_of_week = date_obj.weekday()
        
        # Create a list of weekday names
        # weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Return the corresponding weekday name
        return day_of_week # weekdays[day_of_week]
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."
    
