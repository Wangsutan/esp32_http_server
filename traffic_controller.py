from controller import BaseController
from machine import Pin


class TrafficController(BaseController):
    """硬件控制类：封装LED操作"""

    def __init__(self, red_pin_num: int, yellow_pin_num: int, green_pin_num: int):
        self.red_led = Pin(red_pin_num, Pin.OUT)
        self.yellow_led = Pin(yellow_pin_num, Pin.OUT)
        self.green_led = Pin(green_pin_num, Pin.OUT)
        self.red_led.off()
        self.yellow_led.off()
        self.green_led.off()

    def red_on(self) -> None:
        self.red_led.on()
        self.yellow_led.off()
        self.green_led.off()

    def yellow_on(self) -> None:
        self.red_led.off()
        self.yellow_led.on()
        self.green_led.off()

    def green_on(self) -> None:
        self.red_led.off()
        self.yellow_led.off()
        self.green_led.on()

    def off(self) -> None:
        """关闭LED"""
        self.red_led.off()
        self.yellow_led.off()
        self.green_led.off()

    def execute_command(self, wlan: network.WLAN, command: str) -> Tuple[str, int]:
        if command == "RED_ON":
            self.red_on()
            return "红色 LED 已开启", 200
        elif command == "YELLOW_ON":
            self.yellow_on()
            return "黄色 LED 已开启", 200
        elif command == "GREEN_ON":
            self.green_on()
            return "绿色 LED 已开启", 200
        elif command == "LED_OFF":
            self.off()
            return "LED 已关闭", 200
        elif command == "HELLO":
            return f"Hello from ESP32! (IP: {wlan.ifconfig()[0]})", 200
        else:
            return f"未知指令: {command}", 400
