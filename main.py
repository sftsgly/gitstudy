import subprocess
import time


def check_internet_connection():
    try:
        # 通过ping谷歌DNS服务器检测网络连通性（超时1秒）
        subprocess.run(['ping', '-n', '1', '-w', '1000', '8.8.8.8'],
                       check=True,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def connect_to_wifi(ssid, password):
    try:
        # 生成XML配置文件
        xml_config = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""

        # 保存配置文件
        with open(f"{ssid}.xml", "w") as f:
            f.write(xml_config)

        # 添加并连接WiFi配置文件（需要管理员权限）
        subprocess.run(f'netsh wlan add profile filename="{ssid}.xml"', shell=True)
        subprocess.run(f'netsh wlan connect name="{ssid}"', shell=True)
        return True
    except Exception as e:
        print(f"连接失败: {str(e)}")
        return False


if __name__ == "__main__":
    SSID = "TP_LINK450M"
    PASSWORD = "peng301601"
    flag = 0
    while True:
        if check_internet_connection():
            if flag == 0:
                print("网络连接正常")
                flag = 1
        else:
            print("检测到网络断开，尝试重新连接...")
            flag = 0
            if connect_to_wifi(SSID, PASSWORD):
                print("已尝试连接WiFi，等待10秒后验证...")
                time.sleep(10)
            else:
                print("连接失败，请检查配置")

        time.sleep(5)  # 每5秒检查一次