# -*- coding: utf-8 -*-
"""Executa um teste identificado para cada um dos 30 exercícios."""

import unittest

from testeExercicios import TesteExercicios


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TesteExercicios))
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if resultado.wasSuccessful() else 1)
