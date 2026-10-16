import gps_service


MENU = {
    "pho": 50000,
    "bun": 45000,
    "com": 30000,
}

PROMO_CODES = {
    "GIAM10": {"discount": 0.1, "min_os_version": 0},
    "NEW_OS_ONLY": {"discount": 0.2, "min_os_version": 15},
}

RESTAURANTS_BY_LOCATION = {
    "10.0,105.0": ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
}


class YummyApp:
    def __init__(self, network_status: str = "online", os_version: int = 15):
        self.network_status = network_status
        self.os_version = os_version

    def calculate_order_total(self, cart: dict) -> float:
        """Calculate totals for valid items with positive quantities."""
        total = 0.0
        for item, quantity in cart.items():
            if item in MENU and quantity > 0:
                total += MENU[item] * quantity
        return total

    def apply_promo_code(self, total: float, code: str) -> float:
        """Validate and apply a promotion code."""
        if self.network_status == "offline":
            raise ConnectionError(
                "No network connection to validate the code."
            )

        if code not in PROMO_CODES:
            raise ValueError("Invalid promotion code.")

        promo = PROMO_CODES[code]
        if self.os_version < promo["min_os_version"]:
            raise ValueError(
                "This code requires OS version "
                f"{promo['min_os_version']} or later."
            )

        return total * (1 - promo["discount"])

    def get_nearby_restaurants(self) -> list[str] | str:
        """Return nearby restaurants or a message when GPS signal is lost."""
        try:
            lat, lon = gps_service.get_current_location()
            location_key = f"{lat},{lon}"
            return RESTAURANTS_BY_LOCATION.get(location_key, [])
        except gps_service.GPSSignalLostError:
            return "Unable to determine location."
