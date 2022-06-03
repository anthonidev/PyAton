from django.test import TestCase

from apps.shipping.models import Shipping


class CouponTestCase(TestCase):
    def setUp(self):
        Shipping.objects.create(
            name="Prueba", time_to_delivery="3 dias", price=15)

    def test_shipping(self):
        one = Shipping.objects.get(name="Prueba")

        print("Shipping :")
        self.assertEquals(one.name, "Prueba")
        self.assertEquals(one.photo, None)
        self.assertEquals(one.time_to_delivery, "3 dias")
        self.assertEquals(one.price, 15)
        pass
