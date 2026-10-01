# -*- coding: utf-8 -*-
"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: executar_testes.py
Resumo: Executa todos os testes do projeto.
"""

import unittest

from testeProjeto import TesteProjeto

try:
    from testeExercicios import TesteExercicios
except ImportError:
    TesteExercicios = None


def montar_suite():
    suite = unittest.TestSuite()

    if TesteExercicios is not None:
        suite.addTests(
            unittest.defaultTestLoader.loadTestsFromTestCase(TesteExercicios)
        )

    suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TesteProjeto)
    )
    return suite


if __name__ == "__main__":
    resultado = unittest.TextTestRunner(verbosity=2).run(montar_suite())
    raise SystemExit(0 if resultado.wasSuccessful() else 1)
