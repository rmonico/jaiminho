#!/usr/bin/env python3
from unittest import SkipTest, TestCase, main as unittest_main
from argparse import Namespace
from jaiminho import main


class JaiminhoTests(TestCase):

    def test_GIVEN_a_home_folder_on_cli_THEN_must_find_request_files_on_it(self):
        main.args = Namespace(home_folder='/home/folder')

        request_file = main._request_file('ab/cd/de')

        self.assertEqual(request_file, '/home/folder/ab/cd/de.yaml')


    def test_GIVEN_a_dict_with_only_non_dict_values_THEN_must_return_them_unchanged(self):
        d = { 'a': 99 }

        returned = main._convert_dicts_to_namespace(d)

        self.assertEqual(type(returned), dict)
        self.assertIn('a', returned)
        self.assertEqual(returned['a'], 99)


    def test_GIVEN_a_dict_with_dict_values_THEN_must_return_them_as_namespaces(self):
        d = { 'a': { 'b': 'value' } }

        returned = main._convert_dicts_to_namespace(d)

        self.assertEqual(type(returned), dict)
        self.assertIn('a', returned)
        self.assertIsInstance(returned['a'], Namespace)
        self.assertTrue(hasattr(returned['a'], 'b'))
        self.assertEqual(returned['a'].b, 'value')


    def test_GIVEN_a_dict_with_variables_THEN_must_interpolate_its_keys_on_a_format_string(self):
        d = { 'var': 'value', 'another_var': 'another value' }

        returned = main._format_all_strs(d, 'value of var: {var}; value of another_var: {another_var}')

        self.assertEqual(returned, 'value of var: value; value of another_var: another value')


    def test_GIVEN_a_dict_with_namespace_variables_THEN_must_interpolate_its_keys_on_a_format_string(self):
        d = { 'var': Namespace(prop='value'), 'another': Namespace(other='another value') }

        returned = main._format_all_strs(d, 'value of var: {var.prop}; value of another: {another.other}')

        self.assertEqual(returned, 'value of var: value; value of another: another value')


    def test_GIVEN_a_dict_with_dicts_THEM_must_interpolate_strings_inside_them(self):
        d = { 'a': 'value', 'b': 'b value' }

        returned = main._format_all_strs_on_dict(d, { 1: 'a: {a}', 2: 'b: {b}' })

        self.assertDictEqual(returned, { 1: 'a: value', 2: 'b: b value' })


if __name__ == '__main__':
    unittest_main()
