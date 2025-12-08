import network_layer
import controller
import json


def load_config(config_path="config.json"):
    """加载配置文件"""
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"[错误] 读取配置文件失败: {e}")
        # 返回默认配置或退出
        raise


# ==================== 主程序 ====================
def main() -> None:
    """主程序入口"""
    print("=" * 50)
    print("ESP32 HTTP 服务器 (简化版)")
    print("=" * 50)

    # 加载配置
    config = load_config()

    # 从配置中读取参数
    WIFI_SSID = config["wifi"]["ssid"]
    WIFI_PWD = config["wifi"]["password"]
    SERVER_PORT = config["server"]["port"]
    LED_PIN = config["hardware"]["led_pin"]

    # 连接网络
    wlan = network_layer.connect_wifi(WIFI_SSID, WIFI_PWD)

    # 初始化硬件控制器
    led_ctrl = controller.LedController(LED_PIN)
    print(f"[硬件] LED 初始化在引脚 {LED_PIN}")

    # 启动服务器
    network_layer.start_server(wlan, led_ctrl, SERVER_PORT)


if __name__ == "__main__":
    main()
