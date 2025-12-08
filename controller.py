from machine import Pin
import time


class BaseController:
    """控制器基类。必须实现下面的方法，你自己派生的类才能成功运行。"""

    def execute_command(self, wlan: network.WLAN, command: str) -> Tuple[str, int]:
        """
        执行命令并返回响应

        参数:
            wlan: 网络连接对象
            command: 要执行的命令字符串

        返回:
            Tuple[响应文本, HTTP状态码]
        """
        raise NotImplementedError("子类必须实现此方法")


class LedController(BaseController):
    """硬件控制类：封装LED操作"""

    def __init__(self, pin_num: int):
        self.led = Pin(pin_num, Pin.OUT)
        self.off()  # 初始状态关闭

    def on(self) -> None:
        """开启LED"""
        self.led.on()
        print("[硬件] LED 开启")

    def off(self) -> None:
        """关闭LED"""
        self.led.off()
        print("[硬件] LED 关闭")

    def blink(self, times: int = 3, delay_ms: int = 200) -> None:
        """闪烁LED，用于视觉反馈"""
        print(f"[硬件] LED 闪烁 {times} 次")
        for _ in range(times):
            self.on()
            time.sleep_ms(delay_ms)
            self.off()
            time.sleep_ms(delay_ms)

    def status(self) -> str:
        """获取LED当前状态"""
        return "ON" if self.led.value() else "OFF"

    def execute_command(self, wlan: network.WLAN, command: str) -> Tuple[str, int]:
        if command == "LED_ON":
            self.on()
            return "LED 已开启", 200
        elif command == "LED_OFF":
            self.off()
            return "LED 已关闭", 200
        elif command == "I_AM_LIVING":
            self.blink(3, 300)
            return "ESP32 收到: i am living (LED已闪烁确认)", 200
        elif command == "HELLO":
            return f"Hello from ESP32! (IP: {wlan.ifconfig()[0]})", 200
        elif command == "STATUS":
            return f"LED状态: {self.status()}, IP: {wlan.ifconfig()[0]}", 200
        else:
            return f"未知指令: {command}", 400
