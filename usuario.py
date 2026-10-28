class Usuario:
    def __init__(self, identificador, nome, matricula):
        if not nome.strip() or not matricula.strip():
            raise ValueError("Nome e matrícula são obrigatórios.")
        self.__identificador = identificador
        self.__nome = nome.strip()
        self.__matricula = matricula.strip()

    @property
    def identificador(self):
        return self.__identificador

    @property
    def nome(self):
        return self.__nome

    @property
    def matricula(self):
        return self.__matricula

    def __eq__(self, outro):
        return isinstance(outro, Usuario) and self.__identificador == outro.identificador

    def __hash__(self):
        return hash(self.__identificador)

    def __repr__(self):
        return f"Usuario(id={self.__identificador}, nome={self.__nome!r}, matricula={self.__matricula!r})"
