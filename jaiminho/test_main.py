#!/usr/bin/env python3
from unittest import SkipTest, TestCase, main as unittest_main
from argparse import Namespace
from jaiminho import main


class JaiminhoTests(TestCase):

    def test_request_file(self):
        main.args = Namespace(home_folder='/home/folder')

        request_file = main._request_file('ab/cd/de')

        self.assertEqual(request_file, '/home/folder/ab/cd/de.yaml')

    def test_namespace_default(self):
        default = main._namespace('ab/cd/de')

        self.assertEqual(default, 'ab/cd')

    def test_make_extensions_should_append_property(self):
        arguments = [{'property': 'value'}, {'another thing': False}]

        definitive = main._make_extensions(arguments)

        self.assertDictEqual(definitive, {
            'property': 'value',
            'another thing': False
        })

    def test_make_extensions_should_overwrite_property(self):
        arguments = [{'property': 'value'}, {'property': 'another value'}]

        definitive = main._make_extensions(arguments)

        self.assertDictEqual(definitive, {'property': 'another value'})

    def test_make_extensions_should_append_property_in_subkeys(self):
        arguments = [{
            'key': {
                'property': 'value'
            }
        }, {
            'key': {
                'another thing': False
            }
        }]

        definitive = main._make_extensions(arguments)

        self.assertDictEqual(
            definitive, {'key': {
                'property': 'value',
                'another thing': False
            }})

    def test_make_extensions_should_extend_external_file(self):
        pass


if __name__ == '__main__':
    unittest_main()
