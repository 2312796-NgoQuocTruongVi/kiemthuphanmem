class GPSSignalLostError(Exception):
    """Raised when the device loses its GPS signal."""


def get_current_location() -> tuple[float, float]:
    """Return the device's current latitude and longitude."""
    return (10.0, 105.0)
