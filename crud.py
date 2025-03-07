from mysql.connector import (connection)
import json

def conexaoBD():
    try:
        with open('database-professor/ifood.conf', 'r') as dadosbd: 
            databd = json.load(dadosbd)

        cnx = connection.MySQLConnection(user=databd['user'],
                                         password=databd['pass'],
                                         host=databd['host'],
                                         database=databd['database'])
        
        return cnx
    
    except Exception as e:
        print (f"FALHA NA CONEXÃO COM O BANCO: {e}")
   

def createUpdateDelete(sql:str, tupla:tuple, tipo:str):
    try:
        conexao = conexaoBD()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(sql, tupla)

        conexao.commit()

        return True

    except Exception as e:
        print (f"FALHA NO {tipo} NO BANCO: {e}")
        return False
    

def read(sql:str, tupla:tuple, tipoRetorno='fetchall'):
    try: 
        conexao = conexaoBD()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(sql, tupla)

        if tipoRetorno == 'fetchone':
            return cursor.fetchone()
        else:
            return cursor.fetchall()
    
    except Exception as e:
        print (f"FALHA NA LEITURA DO BANCO: {e}")
        return None