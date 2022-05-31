from django.test import TestCase

from apps.coupon.models import Coupon

class CouponTestCase(TestCase):
    def setUp(self):
        Coupon.objects.create(code="5050", value=50)
        Coupon.objects.create(code="6060", value=60)

    def test_coupon_can_use(self):
        fifty = Coupon.objects.get(code="5050")
        sixty = Coupon.objects.get(code="6060")
        self.assertEqual(fifty.can_use(), True)
        self.assertEqual(sixty.can_use(), True)