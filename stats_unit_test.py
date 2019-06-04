from artist import Stats

import unittest

simple_test_dic = {"wow": 1,
            "a": 5}

dict_stats = Stats(simple_test_dic)


class TestDictMethods(unittest.TestCase):

    simple_test_dic = {"wow": 1,
                       "a": 5}

    dict_stats = Stats(simple_test_dic)

    def test_unique_words(self):
        self.assertEqual(dict_stats.get_unique_words(), 2)
        self.assertEqual(dict_stats.get_unique_words_minus(), 1)

    def test_ave_length_word(self):
        self.assertEqual(dict_stats.get_ave_length_word(), 8/6)
        self.assertEqual(dict_stats.get_ave_length_unique_word(), 2)
        self.assertEqual(dict_stats.get_ave_length_word_minus(), 3)
        self.assertEqual(dict_stats.get_ave_length_unique_word_minus(), 3)

    def test_starting_letter(self):
        self.assertEqual(dict_stats.get_starting_letter_count()['w'], 1)
        self.assertEqual(dict_stats.get_starting_letter_count()['a'], 5)
        self.assertFalse('a' in dict_stats.get_starting_letter_count_minus())


if __name__ == '__main__':
    unittest.main()
