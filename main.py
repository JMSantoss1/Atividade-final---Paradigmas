from datetime import date

from biblioteca import Biblioteca, ErroBiblioteca
from comparacao_paradigmas import comparar_paradigmas


def formatar_moeda(valor):
    return "R$ " + f"{valor:.2f}".replace(".", ",")


def formatar_data(data):
    return data.strftime("%d/%m/%Y")


def titulo_secao(texto):
    return f"\n{'=' * 60}\n{texto}\n{'=' * 60}"


def popular_biblioteca(biblioteca):
    livros = (
        ("Clean Code", "Robert C. Martin", "Programação"),
        ("Python Fluente", "Luciano Ramalho", "Programação"),
        ("Structure and Interpretation of Computer Programs", "Harold Abelson", "Programação"),
        ("Introdução a Algoritmos", "Thomas Cormen", "Algoritmos"),
        ("Algoritmos: Teoria e Prática", "Thomas Cormen", "Algoritmos"),
        ("Sistemas de Banco de Dados", "Ramez Elmasri", "Banco de Dados"),
    )
    for titulo, autor, categoria in livros:
        biblioteca.cadastrar_livro(titulo, autor, categoria)

    for nome, matricula in (("Ana Souza", "2024001"), ("Bruno Lima", "2024002"), ("Carla Dias", "2024003")):
        biblioteca.cadastrar_usuario(nome, matricula)

    biblioteca.registrar_emprestimo(1, 1, date(2026, 10, 1), prazo_dias=7)
    biblioteca.registrar_emprestimo(2, 2, date(2026, 10, 10))
    biblioteca.registrar_emprestimo(3, 1, date(2026, 10, 20))
    biblioteca.registrar_emprestimo(4, 3, date(2026, 10, 25))
    biblioteca.registrar_emprestimo(5, 2, date(2026, 10, 1), prazo_dias=7)
    biblioteca.registrar_devolucao(5, date(2026, 10, 15))
    biblioteca.registrar_emprestimo(6, 3, date(2026, 11, 5))


def demonstrar_cadastros(biblioteca):
    print(titulo_secao("ACERVO E USUÁRIOS"))
    for livro in biblioteca.listar_livros():
        print(f"  [{livro.identificador}] {livro.titulo} - {livro.autor} ({livro.categoria})")
    for usuario in biblioteca.listar_usuarios():
        print(f"  [{usuario.identificador}] {usuario.nome} - matrícula {usuario.matricula}")


def demonstrar_emprestimos(biblioteca):
    print(titulo_secao("EMPRÉSTIMOS"))
    for emprestimo in biblioteca.listar_emprestimos():
        situacao = (
            "ativo" if emprestimo.ativo
            else f"devolvido em {formatar_data(emprestimo.data_devolucao)}"
        )
        print(
            f"  #{emprestimo.identificador} {emprestimo.livro.titulo} -> {emprestimo.usuario.nome} | "
            f"retirada {formatar_data(emprestimo.data_emprestimo)} | "
            f"prevista {formatar_data(emprestimo.data_prevista_devolucao)} | {situacao}"
        )


def demonstrar_regras(biblioteca):
    print(titulo_secao("REGRAS DE NEGÓCIO"))
    try:
        biblioteca.registrar_emprestimo(1, 2, date(2026, 11, 10))
    except ErroBiblioteca as erro:
        print(f"  Empréstimo recusado: {erro}")
    try:
        biblioteca.cadastrar_usuario("Outra Pessoa", "2024001")
    except ErroBiblioteca as erro:
        print(f"  Cadastro recusado: {erro}")
    try:
        biblioteca.registrar_devolucao(5, date(2026, 11, 10))
    except ErroBiblioteca as erro:
        print(f"  Devolução recusada: {erro}")


def demonstrar_filtragem(biblioteca):
    print(titulo_secao("FILTRAGEM DE LIVROS POR CATEGORIA"))
    for categoria in ("Programação", "algoritmos"):
        livros = biblioteca.buscar_livros_por_categoria(categoria)
        print(f"  {categoria}: {', '.join(livro.titulo for livro in livros)}")


def demonstrar_atrasos(biblioteca, data_referencia):
    print(titulo_secao(f"EMPRÉSTIMOS ATRASADOS EM {formatar_data(data_referencia)}"))
    for emprestimo in biblioteca.consultar_emprestimos_atrasados(data_referencia):
        print(f"  #{emprestimo.identificador} {emprestimo.livro.titulo} ({emprestimo.usuario.nome})")


def demonstrar_relatorio(biblioteca, data_referencia):
    print(titulo_secao(f"RELATÓRIO DE MULTAS EM {formatar_data(data_referencia)}"))
    relatorio = biblioteca.gerar_relatorio_multas(data_referencia)
    for item in relatorio.itens:
        print(
            f"  #{item.identificador_emprestimo} {item.titulo_livro} | {item.nome_usuario} | "
            f"{item.dias_atraso} dia(s) | {formatar_moeda(item.valor)}"
        )
    print(f"  TOTAL: {formatar_moeda(relatorio.total)}")


def demonstrar_estatisticas(biblioteca, data_referencia):
    print(titulo_secao("ESTATÍSTICAS"))
    estatisticas = biblioteca.gerar_estatisticas(data_referencia)
    print("  Livros por categoria:")
    for categoria, quantidade in estatisticas.livros_por_categoria.items():
        print(f"    {categoria}: {quantidade}")
    print("  Empréstimos por usuário (matrícula):")
    for matricula, quantidade in estatisticas.emprestimos_por_usuario.items():
        print(f"    {matricula}: {quantidade}")
    print(f"  Empréstimos ativos: {estatisticas.emprestimos_ativos}")
    print(f"  Empréstimos ativos em atraso: {estatisticas.emprestimos_ativos_em_atraso}")
    print(f"  Valor total das multas: {formatar_moeda(estatisticas.valor_total_multas)}")


def demonstrar_comparacao(biblioteca, data_referencia):
    print(titulo_secao("COMPARAÇÃO: IMPERATIVO x FUNCIONAL (TOTAL DE MULTAS)"))
    imperativo, funcional, equivalentes = comparar_paradigmas(biblioteca.listar_emprestimos(), data_referencia)
    print(f"  Imperativo: {formatar_moeda(imperativo)}")
    print(f"  Funcional : {formatar_moeda(funcional)}")
    print(f"  Resultados equivalentes: {'sim' if equivalentes else 'não'}")


def demonstrar_imutabilidade(biblioteca, data_referencia):
    print(titulo_secao("IMUTABILIDADE"))
    emprestimos_antes = biblioteca.listar_emprestimos()
    livros_antes = biblioteca.listar_livros()
    biblioteca.gerar_relatorio_multas(data_referencia)
    biblioteca.gerar_estatisticas(data_referencia)
    biblioteca.buscar_livros_por_categoria("Programação")
    biblioteca.consultar_emprestimos_atrasados(data_referencia)
    print(f"  Empréstimos inalterados: {emprestimos_antes == biblioteca.listar_emprestimos()}")
    print(f"  Livros inalterados: {livros_antes == biblioteca.listar_livros()}")


def main():
    data_referencia = date(2026, 11, 10)
    biblioteca = Biblioteca()
    popular_biblioteca(biblioteca)
    demonstrar_cadastros(biblioteca)
    demonstrar_emprestimos(biblioteca)
    demonstrar_regras(biblioteca)
    demonstrar_filtragem(biblioteca)
    demonstrar_atrasos(biblioteca, data_referencia)
    demonstrar_relatorio(biblioteca, data_referencia)
    demonstrar_estatisticas(biblioteca, data_referencia)
    demonstrar_comparacao(biblioteca, data_referencia)
    demonstrar_imutabilidade(biblioteca, data_referencia)


if __name__ == "__main__":
    main()
