
import unittest

from nlp.features import add_to_matrix, makematrix, remove_from_matrix


class TestMakeMatrix(unittest.TestCase):

    def setUp(self):

        pass

    def test_stuff(self):

        self.assertEquals(2, 2)

    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')
