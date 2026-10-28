import unittest
from datetime import date
from decimal import Decimal

from biblioteca import Biblioteca, EmprestimoJaDevolvido, LivroIndisponivel, MatriculaDuplicada
from comparacao_paradigmas import comparar_paradigmas
from funcoes_puras import (
    calcular_multa,
    filtrar_livros_por_categoria,
    gerar_relatorio_multas,
    selecionar_emprestimos_atrasados,
)


class TestesBiblioteca(unittest.TestCase):
    def setUp(self):
        self.biblioteca = Biblioteca()
        self.livro_a = self.biblioteca.cadastrar_livro("Livro A", "Autor 1", "Programação")
        self.livro_b = self.biblioteca.cadastrar_livro("Livro B", "Autor 2", "Algoritmos")
        self.livro_c = self.biblioteca.cadastrar_livro("Livro C", "Autor 3", "Programação")
        self.ana = self.biblioteca.cadastrar_usuario("Ana", "001")
        self.bruno = self.biblioteca.cadastrar_usuario("Bruno", "002")

    def test_livro_nao_pode_ser_emprestado_duas_vezes(self):
        self.biblioteca.registrar_emprestimo(self.livro_a.identificador, self.ana.identificador, date(2026, 10, 1))
        with self.assertRaises(LivroIndisponivel):
            self.biblioteca.registrar_emprestimo(self.livro_a.identificador, self.bruno.identificador, date(2026, 10, 2))

    def test_devolucao_libera_livro(self):
        emprestimo = self.biblioteca.registrar_emprestimo(self.livro_a.identificador, self.ana.identificador, date(2026, 10, 1))
        self.biblioteca.registrar_devolucao(emprestimo.identificador, date(2026, 10, 5))
        self.assertTrue(self.biblioteca.livro_disponivel(self.livro_a.identificador))
        self.assertEqual(self.biblioteca.consultar_emprestimo(emprestimo.identificador).data_devolucao, date(2026, 10, 5))

    def test_devolucao_duplicada_e_recusada(self):
        emprestimo = self.biblioteca.registrar_emprestimo(self.livro_a.identificador, self.ana.identificador, date(2026, 10, 1))
        self.biblioteca.registrar_devolucao(emprestimo.identificador, date(2026, 10, 5))
        with self.assertRaises(EmprestimoJaDevolvido):
            self.biblioteca.registrar_devolucao(emprestimo.identificador, date(2026, 10, 6))

    def test_matricula_duplicada(self):
        with self.assertRaises(MatriculaDuplicada):
            self.biblioteca.cadastrar_usuario("Outro", "001")

    def test_calculo_de_multa(self):
        self.assertEqual(calcular_multa(5, Decimal("2.00")), Decimal("10.00"))
        self.assertEqual(calcular_multa(0, Decimal("2.00")), Decimal("0.00"))
        self.assertEqual(calcular_multa(5, Decimal("2.00")), calcular_multa(5, Decimal("2.00")))

    def test_sem_atraso_na_data_prevista(self):
        self.biblioteca.registrar_emprestimo(self.livro_a.identificador, self.ana.identificador, date(2026, 10, 1), prazo_dias=7)
        self.assertEqual(self.biblioteca.consultar_emprestimos_atrasados(date(2026, 10, 8)), ())
        self.assertEqual(len(self.biblioteca.consultar_emprestimos_atrasados(date(2026, 10, 9))), 1)

    def test_relatorio_ignora_devolvidos_e_soma_multas(self):
        ativo = self.biblioteca.registrar_emprestimo(self.livro_a.identificador, self.ana.identificador, date(2026, 10, 1), prazo_dias=7)
        devolvido = self.biblioteca.registrar_emprestimo(self.livro_b.identificador, self.bruno.identificador, date(2026, 10, 1), prazo_dias=7)
        self.biblioteca.registrar_devolucao(devolvido.identificador, date(2026, 10, 20))
        relatorio = self.biblioteca.gerar_relatorio_multas(date(2026, 10, 18))
        self.assertEqual(len(relatorio.itens), 1)
        self.assertEqual(relatorio.itens[0].identificador_emprestimo, ativo.identificador)
        self.assertEqual(relatorio.total, Decimal("20.00"))

    def test_filtragem_nao_altera_colecao_original(self):
        livros = self.biblioteca.listar_livros()
        copia = tuple(livros)
        resultado = filtrar_livros_por_categoria(livros, "programação")
        self.assertEqual(livros, copia)
        self.assertEqual(resultado, (self.livro_a, self.livro_c))

    def test_funcoes_puras_nao_alteram_emprestimos(self):
        self.biblioteca.registrar_emprestimo(self.livro_a.identificador, self.ana.identificador, date(2026, 10, 1))
        antes = self.biblioteca.listar_emprestimos()
        selecionar_emprestimos_atrasados(antes, date(2026, 12, 1))
        gerar_relatorio_multas(antes, date(2026, 12, 1))
        self.assertEqual(antes, self.biblioteca.listar_emprestimos())
        self.assertTrue(all(emprestimo.ativo for emprestimo in antes))

    def test_estatisticas(self):
        self.biblioteca.registrar_emprestimo(self.livro_a.identificador, self.ana.identificador, date(2026, 10, 1), prazo_dias=7)
        self.biblioteca.registrar_emprestimo(self.livro_b.identificador, self.ana.identificador, date(2026, 10, 1), prazo_dias=30)
        estatisticas = self.biblioteca.gerar_estatisticas(date(2026, 10, 10))
        self.assertEqual(dict(estatisticas.livros_por_categoria), {"Programação": 2, "Algoritmos": 1})
        self.assertEqual(dict(estatisticas.emprestimos_por_usuario), {"001": 2})
        self.assertEqual(estatisticas.emprestimos_ativos, 2)
        self.assertEqual(estatisticas.emprestimos_ativos_em_atraso, 1)
        self.assertEqual(estatisticas.valor_total_multas, Decimal("4.00"))

    def test_paradigmas_equivalentes(self):
        self.biblioteca.registrar_emprestimo(self.livro_a.identificador, self.ana.identificador, date(2026, 10, 1), prazo_dias=7)
        self.biblioteca.registrar_emprestimo(self.livro_b.identificador, self.bruno.identificador, date(2026, 10, 3), prazo_dias=7)
        for referencia in (date(2026, 9, 1), date(2026, 10, 9), date(2026, 11, 30)):
            imperativo, funcional, equivalentes = comparar_paradigmas(self.biblioteca.listar_emprestimos(), referencia)
            self.assertTrue(equivalentes)
            self.assertEqual(imperativo, funcional)


if __name__ == "__main__":
    unittest.main()
