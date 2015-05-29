from django.test import TestCase

from mock import patch

from ..models import MangoPayPayIn, MangoPayPayInBankWire

from .factories import MangoPayPayInFactory, MangoPayPayInBankWireFactory
from .client import MockMangoPayApi


class MangoPayPayInTests(TestCase):

    def setUp(self):
        self.pay_in = MangoPayPayInFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create(self, mock_client):
        id = 76
        mock_client.return_value = MockMangoPayApi(pay_in_id=id)
        self.assertIsNone(self.pay_in.mangopay_id)
        self.pay_in.create(secure_mode_return_url="http://test.com")
        MangoPayPayIn.objects.get(id=self.pay_in.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_get(self, mock_client):
        mock_client.return_value = MockMangoPayApi()
        self.assertIsNone(self.pay_in.secure_mode_redirect_url)
        self.assertIsNone(self.pay_in.status)
        self.pay_in = self.pay_in.get()
        self.assertIsNotNone(self.pay_in.status)
        self.assertIsNotNone(self.pay_in.secure_mode_redirect_url)


class MangoPayPayInBankWireTests(TestCase):

    def setUp(self):
        self.pay_in = MangoPayPayInBankWireFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create(self, mock_client):
        id = 42
        mock_client.return_value = MockMangoPayApi(pay_in_id=id)
        self.assertIsNone(self.pay_in.mangopay_id)
        self.assertIsNone(self.pay_in.mangopay_bank_account)
        self.assertIsNone(self.pay_in.wire_reference)
        self.pay_in.create()
        MangoPayPayInBankWire.objects.get(id=self.pay_in.id, mangopay_id=id)
        self.assertIsNotNone(self.pay_in.mangopay_bank_account['IBAN'])
        self.assertIsNotNone(self.pay_in.mangopay_bank_account['BIC'])
        self.assertIsNotNone(self.pay_in.wire_reference)
