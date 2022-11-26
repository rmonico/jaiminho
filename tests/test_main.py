#!/usr/bin/env python3
from unittest import SkipTest, TestCase, main as unittest_main
from argparse import Namespace
from jaiminho import main


class JaiminhoTests(TestCase):

    def test_request_file(self):
        main.args = Namespace(home_folder='/home/folder')

        request_file = main._request_file('ab/cd/de')

        self.assertEqual(request_file, '/home/folder/ab/cd/de.yaml')


    def test_GIVEN_a_dict_with_only_non_dict_values_THEN_must_return_them_unchanged(self):
        d = { 'a': 99 }

        retornado = main._convert_dicts_to_namespace(d)

        self.assertEqual(type(retornado), dict)
        self.assertIn('a', retornado)
        self.assertEqual(retornado['a'], 99)


if __name__ == '__main__':
    unittest_main()
