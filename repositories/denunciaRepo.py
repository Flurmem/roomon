from typing import List
from util.DataBase import Database
from models.denuncia import Denuncia

class denunciaRepo:
    @classmethod
    def tabelaDenuncia(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS denuncia(
            idDenuncia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            idDenunciante INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL
            
            )
            """
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql,)
        conn.commit()
        conn.close()
        return resultado.rowcount > 0
    
    @classmethod
    def insert(cls, denuncia: Denuncia) -> Denuncia:
        sql = "INSERT INTO denuncia(idDenunciante, titulo, descricao) VALUES(?,?,?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql, (denuncia.idDenunciante, denuncia.titulo, denuncia.descricao)
        )
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return denuncia
        else:
            return None

    @classmethod
    def update(cls, denuncia: Denuncia) -> Denuncia:
        sql = "UPDATE denuncia SET titulo = ?, descricao = ? WHERE idDenuncia = ? "
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
            (denuncia.titulo, denuncia.descricao),
        )
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return denuncia
        else:
            conn.close()
            return None
    
    @classmethod
    def delete(cls, idDenuncia: int) -> bool:
        sql = "DELETE FROM denuncia WHERE idDenuncia = ?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idDenuncia,))
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False
    
    @classmethod
    def obterDenuncias(cls, idUsuario) -> List[Denuncia]:
        sql = """SELECT idDenuncia, idDenunciante, titulo, descricao FROM denuncia WHERE idDenunciante = ? """
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultados = cursor.execute(sql, (idUsuario,)).fetchall()
        if resultados is not None:
            objetos = [Denuncia(id=objeto[0],
                                idDenunciante=objeto[1],
                                titulo=objeto[2],
                                descricao=objeto[3]) for objeto in resultados]
            conn.commit()
            conn.close()
            return objetos
        else:
            conn.close()
            return None