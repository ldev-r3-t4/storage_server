# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.body import Body
from swagger_server.models.problem import Problem
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestAnalyticController(BaseTestCase):
    """ AnalyticController integration test stubs """

    def test_get_analytic(self):
        """
        Test case for get_analytic

        analytic
        """
        response = self.client.open('/v1/analytic/',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_post_analytic(self):
        """
        Test case for post_analytic

        Update the existing analytic
        """
        problem = Body()
        response = self.client.open('/v1/analytic/ver&#x3D;{version}/'.format(version=789),
                                    method='POST',
                                    data=json.dumps(problem),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
