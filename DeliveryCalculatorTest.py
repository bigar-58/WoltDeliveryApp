import unittest
from WoltDeliveryApp import calculate_delivery_fee


"""
A handful of unittests to check functionality of delivery fee calculator application
following AAA structure for testing.
"""
class DeliveryCalculatorTest(unittest.TestCase):

    def test_small_order_surcharge(self):
        # Cart value less than 10€ should have a surcharge
        fee = calculate_delivery_fee(500, 1000, 3, "2024-01-15T13:00:00Z")
        self.assertEqual(fee, 700)  # 2€ delivery + 5€ surcharge

    def test_no_surcharge_large_order(self):
        # Cart value 200€ or more should have free delivery
        fee = calculate_delivery_fee(20000, 1000, 3, "2024-01-15T13:00:00Z")
        self.assertEqual(fee, 0)

    def test_additional_distance_fee(self):
        # Test delivery fee for extra distance
        fee = calculate_delivery_fee(1500, 1600, 3, "2024-01-15T13:00:00Z")
        self.assertEqual(fee, 400)  # 2€ base + 1€ for additional distance

    def test_bulk_items_fee(self):
        # Test additional fee for bulk items
        fee = calculate_delivery_fee(3000, 1000, 14, "2024-01-15T13:00:00Z")
        self.assertEqual(fee, 820)  # 2€ base + 6.20€ bulk items fee

    def test_friday_rush_hour(self):
        # Test increased fee during Friday rush hour
        fee = calculate_delivery_fee(3000, 1000, 4, "2024-01-19T16:00:00Z")
        self.assertEqual(fee, int(200 * 1.2))  # 2€ base fee increased by 1.2x


if __name__ == '__main__':
    unittest.main()
