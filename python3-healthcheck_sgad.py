#!/usr/local/bin/python3.12
import oracledb
import os

# Lendo senha de variavel do ambiente
userpwd = os.environ.get("PYTHON_DB_PASSWORD")

def Corrige_SGAD(): 
    connection = pool.acquire() 
    pool.wait_timeout = 1000
    if connection.is_healthy():
        update_sql = "UPDATE CORE.cosetting SET VALUE = 'TRUE' WHERE id = 681" 
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(update_sql) 
                connection.commit ()

# Criando pool de conexões caso seja necessario algum paralelismo no futuro
pool = oracledb.create_pool(user="tosp", password=userpwd, dsn="10.129.48.68/tosprd", min=1, max=5, increment=1)
connection = pool.acquire()
pool.wait_timeout = 1000
if connection.is_healthy():
    # Linhas para possiveis coletas de informacoes do banco de dados, util em caso de debug
    #print("Healthy connection!")
    #print(oracledb.__version__)
    #print("Database version:", connection.version)
    #print("Hostname:", connection.dsn)
    select_sql = "SELECT ID, KEY, VALUE, UPDATED FROM CORE.cosetting WHERE id = 681"
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            for ID, KEY, VALUE, UPDATED in cursor.execute(select_sql):
                if VALUE == "TRUE":
                    print(ID, KEY, VALUE, UPDATED)
                    #print("Correto")
                else:
                    print(ID, KEY, VALUE, UPDATED)
                    #print("Corrigindo SGAD")
                    Corrige_SGAD()
        connection.close()
    pool.close()
else:
    print("Error - Unusable connection. Please check the database and network settings.")

