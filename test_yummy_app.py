import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 2}), 100000)

    def test_calculate_total_for_multiple_items(self):
        self.assertEqual(
            self.app.calculate_order_total({"pho": 1, "bun": 1}), 95000
        )

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 0}), 0.0)


class TestMediumLevel(unittest.TestCase):
    def test_apply_promo_code_online(self):
        app = YummyApp(network_status="online")
        self.assertEqual(app.apply_promo_code(100000, "GIAM10"), 90000)

    def test_apply_promo_code_offline_raises_connection_error(self):
        app = YummyApp(network_status="offline")
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_new_os_promo_code_on_supported_os(self):
        app = YummyApp(os_version=15)
        self.assertEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

    def test_new_os_promo_code_on_unsupported_os(self):
        app = YummyApp(os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")

    def test_apply_unknown_promo_code_raises_value_error(self):
        app = YummyApp()
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NOT_A_CODE")


class TestHardLevel(unittest.TestCase):
    def test_gps_service_returns_default_location(self):
        self.assertEqual(gps_service.get_current_location(), (10.0, 105.0))

    @patch(
        "yummy_app.gps_service.get_current_location",
        return_value=(10.0, 105.0),
    )
    def test_nearby_restaurants_inside_supported_area(self, get_location):
        app = YummyApp()
        self.assertEqual(
            app.get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        get_location.assert_called_once_with()

    @patch(
        "yummy_app.gps_service.get_current_location",
        return_value=(20.0, 110.0),
    )
    def test_nearby_restaurants_outside_supported_area(self, get_location):
        app = YummyApp()
        self.assertEqual(app.get_nearby_restaurants(), [])
        get_location.assert_called_once_with()

    @patch(
        "yummy_app.gps_service.get_current_location",
        side_effect=gps_service.GPSSignalLostError,
    )
    def test_nearby_restaurants_when_gps_signal_is_lost(self, get_location):
        app = YummyApp()
        self.assertEqual(
            app.get_nearby_restaurants(), "Khong the xac dinh vi tri."
        )
        get_location.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
