import unittest
from clean_episode_filenames import clean_episode_name


class TestRemoveSuffixFunction(unittest.TestCase):
    def test_clean_episode_name(self):
        self.assertEqual(
            clean_episode_name(
                'Modern Family S04E21 How he became us.mkv', 'Modern Family'),
            'Modern Family S04E21.mkv'
        )
        self.assertEqual(
            clean_episode_name('Invalid Format.txt', 'Something'),
            'Invalid Format.txt'
        )


if __name__ == '__main__':
    unittest.main()
