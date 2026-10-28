class Livro:
    def __init__(self, identificador, titulo, autor, categoria):
        if not titulo.strip() or not autor.strip() or not categoria.strip():
            raise ValueError("Título, autor e categoria são obrigatórios.")
        self.__identificador = identificador
        self.__titulo = titulo.strip()
        self.__autor = autor.strip()
        self.__categoria = categoria.strip()

    @property
    def identificador(self):
        return self.__identificador

    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def categoria(self):
        return self.__categoria

    def __eq__(self, outro):
        return isinstance(outro, Livro) and self.__identificador == outro.identificador

    def __hash__(self):
        return hash(self.__identificador)

    def __repr__(self):
        return f"Livro(id={self.__identificador}, titulo={self.__titulo!r}, categoria={self.__categoria!r})"
