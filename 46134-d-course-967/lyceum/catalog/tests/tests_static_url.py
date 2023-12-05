from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
import parameterized

__all__ = []


class StaticURLTests(TestCase):
    @parameterized.parameterized.expand(
        [
            (reverse("catalog:item_list"), 200),
            (reverse("catalog:new"), 200),
            (reverse("catalog:friday"), 200),
            (reverse("catalog:unverified"), 200),
        ],
    )
    def test_catalog_endpoint(self, url, status):
        response = Client().get(url)
        self.assertEqual(response.status_code, status)

    def test_catalog_int_endpoint(self):
        right_data = [
            reverse(
                "catalog:item_convert_re_detail",
                kwargs={"conv_int": "1"},
            ),
            reverse(
                "catalog:item_convert_re_detail",
                kwargs={"conv_int": "0123"},
            ),
        ]
        wrong_data = ["/catalog/ad/", "/catalog/12d"]
        for url in right_data:
            response = Client().get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)
        for url in wrong_data:
            response = Client().get(url)
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_catalog_re_int_and_convert_int_endpoint(self):
        right_data = {
            reverse(
                "catalog:item_convert_re_detail",
                kwargs={"conv_int": "2"},
            ): "2",
            reverse(
                "catalog:item_convert_re_detail",
                kwargs={"conv_int": "222"},
            ): "222",
        }
        wrong_data = [
            "/catalog/re/ad",
            "/catalog/re/12d",
            "/catalog/converter/0",
        ]
        for url in right_data:
            response = Client().get(url)
            response_decoded = response.content.decode("utf-8")
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(response_decoded, right_data[url])
        for url in wrong_data:
            response = Client().get(url)
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
