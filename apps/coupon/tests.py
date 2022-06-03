from django.test import TestCase

from apps.coupon.models import Coupon

class CouponTestCase(TestCase):
    def setUp(self):
        Coupon.objects.create(code="5050", value=50,num_available=1)
        Coupon.objects.create(code="6A6A", value=60)

    def test_coupon_can_use(self):
        fifty = Coupon.objects.get(code="5050")
        sixty = Coupon.objects.get(code="6A6A")
        
        print("Coupong can use:")
        
        self.assertEquals(fifty.can_use(), True)
        self.assertEqual(sixty.can_use(), True)
        
        
        self.assertEqual(sixty.num_available, 10)
        
        
        self.assertEqual(fifty.num_available, 1)
        self.assertEqual(fifty.use(), False)
        self.assertEqual(fifty.num_available, 0)
        
        
        