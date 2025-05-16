from seabreeze.spectrometers import Spectrometer
import argparse

# 設定命令列參數
parser = argparse.ArgumentParser(description="光譜儀測量程式")
parser.add_argument(
    "-t",
    "--time",
    type=float,
    default=0.05,
    help="積分時間(秒)，預設值為 0.05 秒",
)

args = parser.parse_args()
int_time_sec = args.time  # 從命令列參數取得積分時間

spec = Spectrometer.from_first_available()  # 取得第一個可用的光譜儀
spec.integration_time_micros(int_time_sec * 1e6)  # 設定積分時間

# 取得光譜強度
intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)

print(f"積分時間: {int_time_sec} 秒")
print(f"最大光譜強度: {max(intensities)}")  # 取得最大光譜強度
spec.close()  # 關閉光譜儀

input("按下 Enter 鍵結束程式...")
