from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from utils import generators
from utils.generators import stylers

from utils.core.tools import copy_content_to_clipboard, linux_package_installed

import string


class TestGeneratorAndStylerTools(TestCase):

    def test_generate_unique_id_tool(self):

        self.assertEqual(len(generators.generate_unique_id(-2)), 0)
        self.assertEqual(len(generators.generate_unique_id(2)), 2)
        self.assertEqual(len(generators.generate_unique_id(4)), 4)
        self.assertEqual(len(generators.generate_unique_id(8)), 8)
        self.assertEqual(len(generators.generate_unique_id(16)), 16)
        self.assertEqual(len(generators.generate_unique_id(32)), 32)

        unique_id = generators.generate_unique_id(32)
        is_hex = [
            True if char in list(string.hexdigits)
            else False
            for char in unique_id
        ]

        self.assertTrue(all(is_hex))

    def test_optimize_json_tool(self):

        self.assertEqual(
            stylers.optimize_json([{'hello': 'bye'}, 'hello']),
            '[{"hello": "bye"}, "hello"]'
        )
        self.assertEqual(
            stylers.optimize_json({'hello': 'world'}),
            '{"hello": "world"}'
        )
        self.assertEqual(
            stylers.optimize_json(['hello', 'bye']),
            '["hello", "bye"]'
        )
        self.assertEqual(
            stylers.optimize_json({'hello'}),
            "{'hello'}"
        )
        self.assertEqual(
            stylers.optimize_json('hello'),
            'hello'
        )

    def test_render_json_tool(self):
        self.assertEqual(
            stylers.render_json(
                stylers.optimize_json({"hello": "world"})
            ),
            """[\n    [ hello ] => [ world ]\n]"""
        )

        self.assertEqual(
            stylers.render_json(
                stylers.optimize_json({"hello": "world"}), html=True
            ),
            """<pre style="background-color: #9a9a9a5c; padding: 12px;">[\n    [ hello ] => [ world ]\n]</pre>"""
        )

        self.assertEqual(stylers.render_json('Hello'), 'Hello')
        self.assertEqual(stylers.render_json(1), 1)


class TestTools(TestCase):

    def test_copy_to_clipboard_tool(self):
        if not linux_package_installed('xclip'):
            return  # stop test if xclip is not installed

        for content in ['hello world', '*', 123, None, '\n', '']:
            status = copy_content_to_clipboard(content)
            self.assertEqual(status, True)


class TestMainPage(TestCase):

    fixtures = ['test_fixtures/fixtures.json']

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('test_superuser', password='passwd')

    def test_main_page_contexts(self):

        self.client.login(username='test_superuser', password='passwd')

        response = self.client.get(
            reverse('control')
        )

        self.assertEqual(len(response.context['custom_buttons']), 1)
        self.assertEqual(response.context['custom_buttons'][0].color, '#C4E538')

