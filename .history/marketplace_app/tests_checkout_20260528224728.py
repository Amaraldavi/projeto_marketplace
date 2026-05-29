from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Cart, CartItem, Category, Listing, Order, PaymentTransaction, TradeRequest


class CheckoutFlowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.buyer = User.objects.create_user(username='buyer', email='buyer@example.com', password='Pwd12345!')
        self.seller = User.objects.create_user(username='seller', email='seller@example.com', password='Pwd12345!')
        self.category = Category.objects.create(name='Eletrônicos')
        self.listing = Listing.objects.create(
            seller=self.seller,
            category=self.category,
            title='Fone Bluetooth',
            description='Descrição do produto',
            price=Decimal('199.90'),
            listing_type=Listing.SALE,
            condition=Listing.NEW,
        )
        self.trade_listing = Listing.objects.create(
            seller=self.seller,
            category=self.category,
            title='Console para troca',
            description='Descrição da troca',
            price=Decimal('350.00'),
            listing_type=Listing.TRADE,
            condition=Listing.USED,
        )
        cart = Cart.objects.create(user=self.buyer)
        CartItem.objects.create(cart=cart, listing=self.listing, desired_action=CartItem.BUY)
        self.client.login(username='buyer', password='Pwd12345!')

    def _checkout_data(self):
        return {
            'payment_method': Order.PIX,
            'delivery_method': Order.TO_AGREE,
            'notes': 'Entregar em horário comercial',
            'recipient_name': 'João Silva',
            'recipient_phone': '(11) 99999-9999',
            'postal_code': '01001-000',
            'street': 'Rua das Flores',
            'number': '123',
            'complement': 'Apto 45',
            'neighborhood': 'Centro',
            'city': 'São Paulo',
            'state': 'SP',
        }

    def test_checkout_generates_simulated_qr_before_finalizing_order(self):
        checkout_url = reverse('checkout')

        response = self.client.post(checkout_url, self._checkout_data())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'QR code de simulação')
        self.assertEqual(Order.objects.count(), 0)
        self.assertIn('checkout_pending_purchase', self.client.session)

        confirm_response = self.client.post(checkout_url, {'confirm_purchase': '1'}, follow=True)

        self.assertEqual(confirm_response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.get(buyer=self.buyer)
        self.assertEqual(order.status, Order.PAID)
        self.assertEqual(order.items.count(), 1)

        payment_transaction = PaymentTransaction.objects.get(order=order)
        self.assertEqual(payment_transaction.status, PaymentTransaction.APPROVED)
        self.assertFalse(payment_transaction.checkout_url)

        self.assertNotIn('checkout_pending_purchase', self.client.session)

    def test_purchase_checkout_does_not_consume_trade_items(self):
        cart = Cart.objects.get(user=self.buyer)
        trade_item = CartItem.objects.create(cart=cart, listing=self.trade_listing, desired_action=CartItem.TRADE)

        checkout_url = reverse('checkout')
        response = self.client.get(checkout_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.listing.title)
        self.assertNotContains(response, self.trade_listing.title)

        response = self.client.post(checkout_url, self._checkout_data())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'QR code de simulação')

        confirm_response = self.client.post(checkout_url, {'confirm_purchase': '1'}, follow=True)

        self.assertEqual(confirm_response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(TradeRequest.objects.count(), 0)
        self.assertTrue(CartItem.objects.filter(pk=trade_item.pk).exists())
        self.assertEqual(CartItem.objects.get(pk=trade_item.pk).desired_action, CartItem.TRADE)

    def test_trade_checkout_creates_requests_without_generating_order(self):
        cart = Cart.objects.get(user=self.buyer)
        CartItem.objects.create(cart=cart, listing=self.trade_listing, desired_action=CartItem.TRADE)

        trade_checkout_url = f"{reverse('checkout')}?action=trade"
        response = self.client.get(trade_checkout_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.trade_listing.title)
        self.assertNotContains(response, self.listing.title)

        confirm_response = self.client.post(trade_checkout_url, follow=True)

        self.assertEqual(confirm_response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(TradeRequest.objects.count(), 1)
        self.assertTrue(CartItem.objects.filter(listing=self.listing).exists())