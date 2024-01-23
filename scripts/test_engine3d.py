import unittest
from engine3d import Engine3D


class TestRenderCube(unittest.TestCase):
    def test_x(self):
        engine3d = Engine3D(
            screen_width=1000,
            screen_height=1000,
            unit_px=100,
            dist_factor=0.5,
            size=1
        )
        self.assertEqual(500, engine3d.x(0))
        self.assertEqual(550, engine3d.x(1))
        self.assertEqual(575, engine3d.x(2))
        self.assertEqual(587, engine3d.x(3))
        self.assertEqual(450, engine3d.x(-1))
        self.assertEqual(425, engine3d.x(-2))
        self.assertEqual(413, engine3d.x(-3))


if __name__ == '__main__':
    unittest.main()
