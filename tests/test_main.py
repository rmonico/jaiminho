#!/usr/bin/env python3
from unittest import TestCase, main as unittest_main
from argparse import Namespace
import jaiminho as main
from jaiminho.commands import commons, call


class JaiminhoTests(TestCase):

    def test_GIVEN_a_home_folder_on_cli_THEN_must_find_request_files_on_it(self):
        main.args = Namespace(home_folder='/home/folder')

        request_file = commons.request_file(main.args, 'ab/cd/de')

        self.assertEqual(request_file, '/home/folder/ab/cd/de.yaml')

    def test_GIVEN_a_dict_with_variables_THEN_must_interpolate_its_keys_on_a_format_string(self):
        d = { 'var': 'value', 'another_var': 'another value' }

        returned = call._format_all_strs(d, 'value of var: {var}; value of another_var: {another_var}')

        self.assertEqual(returned, 'value of var: value; value of another_var: another value')

    def test_GIVEN_a_dict_with_namespace_variables_THEN_must_interpolate_its_keys_on_a_format_string(self):
        d = { 'var': Namespace(prop='value'), 'another': Namespace(other='another value') }

        returned = call._format_all_strs(d, 'value of var: {var.prop}; value of another: {another.other}')

        self.assertEqual(returned, 'value of var: value; value of another: another value')

    def test_GIVEN_a_dict_with_dicts_THEM_must_interpolate_strings_inside_them(self):
        d = { 'a': 'value', 'b': 'b value' }

        returned = call._format_all_strs_on_dict(d, { 1: 'a: {a}', 2: 'b: {b}' })

        self.assertDictEqual(returned, { 1: 'a: value', 2: 'b: b value' })


if __name__ == '__main__':
    unittest_main()
