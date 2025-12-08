# Arduino EUNO ESP32 局域网/物联网/远程控制示例项目

## 简介

本项目通过 http 协议，实现了一个简单的 Arduino EUNO ESP32 开发板的，关于局域网/物联网/远程控制的，控制板载 LED 的示例项目。由于仅使用不安全的 http 协议等因素，**请勿在不安全的网络环境中使用该项目代码**。

核心配置信息，存放在配置文件`config.json`中，注意修改其中的 WiFi 账号和密码等配置。

项目结构：

```text
tree ./
./
├── boot.py
├── config.json
├── controller.py
├── main.py
├── network_layer.py
├── Readme.md
└── request_parser.py

1 directory, 7 files
```

## 配置

将该项目路径下的所有.py脚本，以及**根据自己的网络情况修改好**的配置文件`config.json`，上传至Arduino EUNO ESP32 开发板。

`config.json`配置文件内容如下：

```json
{
  "wifi": {
    "ssid": "my_wifi",
    "password": "my_wifi_password"
  },
  "server": {
    "port": 8080
  },
  "hardware": {
    "led_pin": 13
  }
}

```

`led_pin`采用了相应开发板上板载 LED 的引脚。

上传方式有：

1. 打开 thonny 软件，通过`View->Files`打开文件视图，将本地脚本上传至开发板。
2. 通过命令行程序上传代码。linux系统下，通过`ls /dev/ttyUSB*`查询对应的串口。通过`ampy --port /dev/ttyUSB1 put your_script.py`上传代码。

代码上传成功后，只需

- 在thonny的GUI界面运行代码，或者
- 通过一些命令行启动开发板上代程序，或者
- 按开发板上的重置按钮

即可启动软硬件，控制板载 LED。

本项目自带`boot.py`脚本，使得开发板一旦上电，就会自动运行该项目。

## 使用

开发板正常运行后，通过处在同一局域网中的网络浏览器，在其地址栏发送以下类似命令，即可使用相应功能。

```text
http://192.168.1.100:8080/LED_ON
```

请替换成自己开发板的 IP 地址以及端口。开发板一开始会输出这些相关信息，注意观察。

由于网络编码问题，网页上可能会显示乱码，请谅解。

命令清单如下，可以把示例命令`LED_ON`替换成其他命令：

- `LED_ON`：开灯
- `LED_OFF`：关灯
- `I_AM_LIVING`：我还活着
- `HELLO`：打招呼
- `STATUS`：获取状态

## 注意事项

本项目只使用了**未加密**的 http 协议，并且没有在代码中设计足够安全的防护措施，因此：

**绝对不要在安全性要求高的生产环境中使用。**

**绝对不要在安全性要求高的生产环境中使用。**

**绝对不要在安全性要求高的生产环境中使用。**
