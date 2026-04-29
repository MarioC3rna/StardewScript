from pathlib import Path
import unittest

from src.error_table import ErrorTable
from src.lexer import lexer, set_error_table as set_lexer_error_table
from src.parser import parser, set_error_table as set_parser_error_table


ROOT = Path(__file__).resolve().parents[1]
VALID_DIR = ROOT / 'src' / 'tests' / 'valid_programs'
INVALID_DIR = ROOT / 'src' / 'tests' / 'invalid_programs'


def compile_code(code):
    error_table = ErrorTable(source_code=code)
    set_lexer_error_table(error_table)
    set_parser_error_table(error_table)
    lexer.lineno = 1
    result = parser.parse(code, lexer=lexer)
    return result, error_table


class TestValidPrograms(unittest.TestCase):
    def test_all_valid_programs_compile(self):
        for file_path in sorted(VALID_DIR.glob('*.sdw')):
            with self.subTest(program=file_path.name):
                code = file_path.read_text(encoding='utf-8')
                result, error_table = compile_code(code)
                self.assertIsNotNone(result, f'{file_path.name} no generó AST')
                self.assertFalse(error_table.errors, f'{file_path.name} generó errores: {error_table.errors}')


class TestInvalidPrograms(unittest.TestCase):
    def test_all_invalid_programs_fail(self):
        for file_path in sorted(INVALID_DIR.glob('*.sdw')):
            with self.subTest(program=file_path.name):
                code = file_path.read_text(encoding='utf-8')
                result, error_table = compile_code(code)
                self.assertTrue(result is None or error_table.errors, f'{file_path.name} no falló como se esperaba')


if __name__ == '__main__':
    unittest.main(verbosity=2)