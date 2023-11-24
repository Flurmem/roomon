from typing import List
from models.chat import Chat
from models.chat import Mensagem
from models.sala import Sala
from models.usuario import Usuario
from util.DataBase import Database


class chatRepo:
    @classmethod
    def tabelaChat(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS chat(
            idChat INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            idSala INTEGER,
            dataCriacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fkSala FOREIGN KEY(idSala) REFERENCES sala(idSala) ON DELETE CASCADE
            )

            """
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
        )
        conn.commit()
        conn.close()
        return resultado.rowcount > 0

    @classmethod
    def tabelaMensagem(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS mensagem(
            idMensagem INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            idChat INTEGER,
            idEmissor INTEGER,
            dataEnvio DATETIME DEFAULT CURRENT_TIMESTAMP,
            conteudo TEXT NOT NULL,
            CONSTRAINT fkChat FOREIGN KEY(idChat) REFERENCES chat(idChat) ON DELETE CASCADE,
            CONSTRAINT fkEmissor FOREIGN KEY(idEmissor) REFERENCES pessoa(idPessoa) ON DELETE CASCADE
            )

            """
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
        )
        conn.commit()
        conn.close()
        return resultado.rowcount > 0

    @classmethod
    def criarChat(cls, idSala, chat:Chat) -> Chat:
        sql = '''
        INSERT INTO chat(idSala) VALUES(?)
        '''
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
            (
                idSala
            ),
        )

        if resultado.rowcount > 0:
            chat.idChat = cursor.lastrowid
            conn.commit()
            conn.close()
            return chat
        else:
            conn.close()
            return None

    @classmethod
    def armazenarMensagem(cls, mensagem:Mensagem) -> Mensagem:
        sql = '''
        INSERT INTO mensagem(idChat, idEmissor, conteudo) VALUES(?, ?, ?)
        '''
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
            (
                mensagem.idChat, mensagem.idEmissor, mensagem.conteudo
            ),
        )

        if resultado.rowcount > 0:
            mensagem.idMensagem = cursor.lastrowid
            conn.commit()
            conn.close()
            return mensagem
        else:
            conn.close()
            return None

    @classmethod
    def obterChat(cls, idSala) -> List[Mensagem]:
        sql = """SELECT idMensagem, chat.idChat, idEmissor, dataEnvio, conteudo, nomeUsuario FROM mensagem 
        LEFT JOIN chat on mensagem.idChat = chat.idChat
        LEFT JOIN pessoa on idPessoa = idEmissor 
        WHERE chat.idSala = ?"""
        
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultados = cursor.execute(sql, (idSala,)).fetchall()
        if resultados is not None:
            objetos = [Mensagem(idMensagem=objeto[0], 
                            idChat=objeto[1],
                            idEmissor=objeto[2], 
                            dataEnvio=objeto[3], 
                            conteudo=objeto[4],
                            nomeUsuario=objeto[5]
                            ) for objeto in resultados]
            conn.commit()
            conn.close()
            return objetos
        else:
            conn.close()
            return None
