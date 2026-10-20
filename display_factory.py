import os


def create_display():
    display_type = os.getenv(
        "MEDIA_SENTINEL_DISPLAY",
        "oled",
    ).strip().lower()

    if display_type == "oled":
        from oled import SSD1306

        return SSD1306()

    if display_type == "tft":
        from tft import TFT

        return TFT()

    raise ValueError(
        f"Unsupported display: {display_type!r}. "
        "Choose 'oled' or 'tft'."
    )