import argparse
import traceback

from wodevices.temperature_ctrl import PidParameters

from src.device_control.blaze_control import BlazeController

# 設定命令列參數
parser = argparse.ArgumentParser(description="Blaze 控制程式")
parser.add_argument(
    "-t",
    "--temp",
    type=float,
    default=25,
    help="溫度(°C)，預設值為 25°C",
)
parser.add_argument(
    "-c",
    "--current",
    type=float,
    default=150,
    help="電流(mA)，預設值為 150mA",
)

args = parser.parse_args()
temp: float = args.temp  # 從命令列參數取得溫度
# current: float = args.current  # 從命令列參數取得電流

try:
    # 建立 Blaze 物件
    blaze = BlazeController(
        pid=PidParameters(kp=15.0, ki=1.2, kd=0.0),
        target_temp=temp,
    )

    # 連接設備
    blaze.connect_devices()

    # 取得溫度、電流
    print(f"Current temperature: {blaze.get_temp()} °C")
    print(f"Current current: {blaze.get_current()} mA")
except Exception as e:
    print(f"Error: {e}")
    print(f"{traceback.format_exc()}")
finally:
    blaze.disconnect_devices()
    input("Press Enter to exit...")
