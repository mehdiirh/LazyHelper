from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.http.response import JsonResponse

from config.models import Command, Config
from api.models import ReceivedRequest

from utils.api import tools as api_tools
from utils.core import exceptions

import json


class TestApiTools(TestCase):

    fixtures = ['test_fixtures/fixtures.json']

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_superuser('test_superuser', password='passwd')

        cls.user = user
        cls.headers = {
            'content_type': 'application/json',
            'HTTP_AUTHORIZATION': user.profile.api_key
        }

    def setUp(self) -> None:
        self.kwargs = {
            'request': RequestFactory(),
            'data': {'test': True},
            'status_code': 200,
            'message': 'test message',
            'return_json': False,
        }

    def test_api_response(self):
        self.assertIsInstance(api_tools.api_response(**self.kwargs), JsonResponse)

        self.kwargs['return_json'] = True
        json_response = api_tools.api_response(**self.kwargs)
        self.assertIsInstance(json_response, dict)
        self.assertEqual(json_response['data'], {'test': True})
        self.assertEqual(json_response['meta']['code'], 200)
        self.assertEqual(json_response['meta']['status'], 'ok')
        self.assertEqual(json_response['meta']['message'], 'test message')

        self.kwargs['status_code'] = 404
        del self.kwargs['data']
        json_response = api_tools.api_response(**self.kwargs)
        self.assertIsInstance(json_response, dict)
        self.assertIsNone(json_response['data'])
        self.assertEqual(json_response['meta']['code'], 404)
        self.assertEqual(json_response['meta']['status'], 'fail')

    def test_save_received_api_requests(self):

        request = RequestFactory().post(
            reverse('list-of-commands'),
            **self.headers,
        )

        self.kwargs['return_json'] = True
        response = api_tools.api_response(**self.kwargs, commit=False)

        saved_object = api_tools.save_received_request(
            request=request,
            response=response,
            status_code=response['meta']['code']
        )

        self.assertIsInstance(saved_object, ReceivedRequest)
        self.assertIsNotNone(saved_object.pk)
        self.assertEqual(saved_object.user, self.user)
        self.assertEqual(saved_object.path, reverse('list-of-commands'))
        self.assertEqual(saved_object.client_ip, '127.0.0.1')
        self.assertEqual(saved_object.method, 'POST')
        self.assertEqual(
            json.loads(saved_object.headers).get('authorization'),
            f'{self.user.profile.api_key[:3]}***************{self.user.profile.api_key[-3:]}'
        )

    def test_get_request_data_with_get_method(self):

        request = RequestFactory().get(
            reverse('list-of-commands'),
            data={'test': True, 'TestData': ['here', 'is', 'a', 'list']},
            **self.headers,
        )

        data = api_tools.get_request_data(request)

        self.assertIsNotNone(data.get('test'))
        self.assertIsNotNone(data.get('testdata'))  # should be lowercase
        self.assertEqual(data['test'], 'True')
        self.assertEqual(data['testdata'], ['here', 'is', 'a', 'list'])

    def test_get_request_data_with_post_method(self):

        request = RequestFactory().post(
            reverse('list-of-commands'),
            data={'test': True, 'TestData': ['here', 'is', 'a', 'list']},
            **self.headers,
        )

        data = api_tools.get_request_data(request)

        self.assertIsNotNone(data.get('test'))
        self.assertIsNotNone(data.get('TestData'))
        self.assertTrue(data['test'])
        self.assertEqual(data['TestData'], ['here', 'is', 'a', 'list'])

    def test_get_request_headers_with_get_method(self):

        request = RequestFactory().get(
            reverse('list-of-commands'),
            **self.headers,
        )
        headers = api_tools.get_request_headers(request)

        self.assertIsInstance(headers, dict)
        self.assertEqual(headers.get('authorization'), self.user.profile.api_key)  # should be lowercase

    def test_get_request_headers_with_post_method(self):
        request = RequestFactory().post(
            reverse('list-of-commands'),
            **self.headers,
        )
        headers = api_tools.get_request_headers(request)

        self.assertIsInstance(headers, dict)
        self.assertEqual(headers.get('authorization'), self.user.profile.api_key)  # should be lowercase

    def test_search_query_creation(self):

        search_fields = ['is_test', 'is_query']
        query_dict = {'is_test': '1', 'is_query': 'yes', 'not_working': 'no'}

        search_query = api_tools.get_search_query(search_fields, query_dict)
        self.assertIsInstance(search_query, dict)
        self.assertEqual(search_query, {'is_test': '1', 'is_query': 'yes'})

        search_query = api_tools.get_search_query(search_fields, {})
        self.assertEqual(search_query, {})

        with self.assertRaises(AttributeError):
            api_tools.get_search_query(search_fields, [])

        with self.assertRaises(AttributeError):
            api_tools.get_search_query(search_fields, 'query')

    def test_user_security_check_with_api_key(self):
        response = self.client.post(
            reverse('list-of-commands'),
            **self.headers
        )
        request = response.wsgi_request

        self.assertTrue(api_tools.user_security_check(request))

    def test_user_security_check_with_login(self):
        self.client.login(username='test_superuser', password='passwd')
        response = self.client.get(
            reverse('control'),
        )
        request = response.wsgi_request

        self.assertTrue(api_tools.user_security_check(request))

    def test_user_security_check_with_login_not_required(self):
        config = Config.objects.get(key='login-required')
        config.active = False
        config.save()

        response = self.client.get(
            reverse('control'),
        )
        request = response.wsgi_request

        self.assertTrue(api_tools.user_security_check(request))

    def test_user_security_check_authentication_error(self):
        response = self.client.get(
            reverse('control'),
        )
        request = response.wsgi_request

        with self.assertRaises(exceptions.AuthenticationError):
            api_tools.user_security_check(request)


class TestApiEndpoints(TestCase):

    fixtures = ['test_fixtures/fixtures.json']

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_superuser('test_superuser')
        cls.headers = {
            'content_type': 'application/json',
            'HTTP_AUTHORIZATION': user.profile.api_key
        }

    def test_command_execution_with_api(self):

        response = self.client.post(
            reverse('exec-command'),
            data={'command': 'test-command'},
            **self.headers,
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data']['output'], None)
        self.assertEqual(data['meta']['status'], 'ok')
        self.assertEqual(data['data']['command'], '')

    def test_command_execution_with_api_when_command_is_not_defined(self):

        response = self.client.post(
            reverse('exec-command'),
            data={'command': 'x-some-dummy-command-x'},
            **self.headers,
        )

        data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertIsNone(data['data'])
        self.assertEqual(data['meta']['status'], 'fail')
        self.assertEqual(data['meta']['message'], 'command is not valid')

    def test_command_execution_with_api_when_command_is_not_provided(self):

        response = self.client.post(
            reverse('exec-command'),
            **self.headers,
        )

        data = response.json()
        print(data)

        self.assertEqual(response.status_code, 400)
        self.assertIsNone(data['data'])
        self.assertEqual(data['meta']['status'], 'fail')
        self.assertEqual(data['meta']['message'], 'no command provided')

    def test_get_list_of_commands(self):

        command = Command.objects.get(pk=1)

        response = self.client.post(
            reverse('list-of-commands'),
            **self.headers,
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['meta']['status'], 'ok')
        self.assertEqual(data['data']['1']['command'], command.command)
        self.assertEqual(data['data']['1']['short_code'], command.short_code)
        self.assertEqual(len(data['data']), 1)
