import unittest
from CubeEngine import CubeEngine


class TestRenderCube(unittest.TestCase):
    def test_x(self):
        cube_engine = CubeEngine(
            screen_width=1000,
            screen_height=1000,
            unit_px=100,
            dist_factor=0.5,
            size=1
        )
        self.assertEqual(500, cube_engine.x(0))
        self.assertEqual(550, cube_engine.x(1))
        self.assertEqual(575, cube_engine.x(2))
        self.assertEqual(587, cube_engine.x(3))
        self.assertEqual(450, cube_engine.x(-1))
        self.assertEqual(425, cube_engine.x(-2))
        self.assertEqual(413, cube_engine.x(-3))


if __name__ == '__main__':
    unittest.main()
