import unittest
from transformations import move, rect_center, rotate


class TestTransformations(unittest.TestCase):

    def test_move(self):
        a = (1, 1)
        by = (2, 1)
        self.assertEqual((3, 2), move(a, by))

    def test_rotate(self):
        a = (0, 0)
        c = (1, 0)
        self.assertEqual((1, 1), rotate(a, c, 270))

    def test_rect_center(self):
        rect = [(0, 0), (2, 0), (2, 2), (0, 2)]
        self.assertEqual((1, 1), rect_center(rect))


if __name__ == '__main__':
    unittest.main()
