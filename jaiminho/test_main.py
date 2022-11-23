#!/usr/bin/env python3
from unittest import SkipTest, TestCase, main as unittest_main
from argparse import Namespace
from jaiminho import main


class JaiminhoTests(TestCase):

    def test_request_file(self):
        main.args = Namespace(home_folder='/home/folder')

        request_file = main._request_file('ab/cd/de')

        self.assertEqual(request_file, '/home/folder/ab/cd/de.yaml')


if __name__ == '__main__':
    unittest_main()
