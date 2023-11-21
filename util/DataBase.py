import sqlite3

class Database:
    @classmethod
    def createConnection(cls):
        conn = sqlite3.connect("roomon.db")
        return conn


# os metodos da classe são os que voce chama da própria classe, não das instâncias dela
# os métodos da classe não interferem nos objetos necessariamente, são mais gerais
# não da pra chamar um class method a partir de um objeto, apenas por intermédio da classe em si
