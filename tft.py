import time

from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from PIL import Image, ImageDraw, ImageFont


class TFT:
    """ST7735 TFT status display for Media Sentinel."""

    def __init__(self):
        serial = spi(
            port=0,
            device=0,
            gpio_DC=24,
            gpio_RST=25,
            bus_speed_hz=1_000_000,
            spi_mode=0,
            reset_hold_time=0.150,
            reset_release_time=0.150,
        )

        self.device = st7735(
            serial,
            width=160,
            height=128,
            rotate=1,
            bgr=True,
        )

        # Keep the display powered while the application runs.
        self.device.persist = True

        self.font = ImageFont.load_default()

    @staticmethod
    def _status(value):
        if value is None:
            return "CHECKING", (255, 200, 0)

        if value:
            return "ONLINE", (0, 220, 100)

        return "OFFLINE", (255, 70, 70)

    def show_status(self, plex, abs_status, windows_agent):
        image = Image.new(
            "RGB",
            (self.device.width, self.device.height),
            (12, 16, 24),
        )
        draw = ImageDraw.Draw(image)

        draw.text(
            (8, 8),
            "MEDIA SENTINEL",
            font=self.font,
            fill=(0, 200, 255),
        )

        draw.line(
            (8, 25, self.device.width - 8, 25),
            fill=(70, 85, 105),
        )

        services = (
            ("PLEX", plex),
            ("AUDIOBOOKSHELF", abs_status),
            ("WINDOWS AGENT", windows_agent),
        )

        for index, (name, value) in enumerate(services):
            y = 38 + index * 26
            status, color = self._status(value)

            draw.text(
                (8, y),
                name,
                font=self.font,
                fill=(220, 225, 235),
            )
            draw.text(
                (8, y + 11),
                status,
                font=self.font,
                fill=color,
            )

        self.device.display(image)
        