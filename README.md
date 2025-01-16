# User events
User events has been split into ranges.

## IO
I/O: 0-99
Main: 100-199
Flappy Bird: 200-299

## SPI
SPI must be set to enabled in raspi-config
Install the `spidev` and `mfrc522` Python packages throuth pip
SPI-Py must be installed by entering the `SPI-Py` folder and running `sudo python3 setup.py install`

## Pins
Connect to pins:
Button: 37 (GPIO 26)
Button LED: 33 (GPIO 13, PWM1)
LED strip: 12 (GPIO 18, PWM0)

### RC522:
SDA: 24 (GPIO 8, SPI0 CE0)
SCK: 23 (GPIO 11, SPI0 SCLK)
MOSI: 19 (GPIO 10, SPI0 MOSI)
MISO: 21 (GPIO 9, SPI0 MISO)
RST: 22 (GPIO 25)

## Python packages:
pygame
Rpi.GPIO
rpi_ws281x

## Development
Requires the `Mock.GPIO` library