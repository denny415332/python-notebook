# Packages
import json
from pathlib import Path
from seabreeze.spectrometers import list_devices
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import colour
from wopcprotocol.common import LedState, LedCurrent
from src.testcfg import TestConfig
from src.device_operator import BlazeOperator, SpectrometerOperator
from src.calc import spectrum_to_spectral_distribution, calibration_spectrum
from src.draw_plot import draw_cie_xy_plot


# Constant
TEST_CONFIG_PATH = "config_data/QEP05178_test_params.json"
"設定檔路徑"
SAVE_CONFIG_DIR = "config_data/"
"儲存設定檔的資料夾路徑"
OUTPUT_DIR = "output/"
"檔案輸出資料夾路徑"


def load_calibration_data(calibration_path: Path) -> list[float, float]:
    """加載校正資料

    Args:
        calibration_path (Path): 校正檔路徑

    Returns:
        list[float, float]: 校正資料[[波長, u焦耳/次數], ...]
    """
    return pd.read_csv(str(calibration_path)).to_numpy()


def run_spectrometer(
    cfg: TestConfig, calibration_data: list[float, float]
) -> tuple[np.ndarray, np.ndarray, float, np.ndarray, float]:
    """運行 Spectrometer ，並取得客戶所需資料

    Args:
        cfg (TestConfig): 測試設定檔
        calibration_data (list[float, float]): 校正資料

    Returns:
        tuple[np.ndarray, np.ndarray, float, np.ndarray, float]:
        [校正前光譜, 校正後光譜, 校正後光譜亮度, 校正後光譜色座標, 校正後光譜波峰]
    """
    # outputs
    old_spectrum = np.array([])  # 校正前光譜
    new_spectrum = np.array([])  # 校正後光譜
    liminous_flux = 0  # 校正後光譜亮度
    cie_xy = np.array([0, 0])  # 校正後光譜色座標
    peak = 0  # 校正後光譜波峰(文件裡寫波長)

    spec_op = SpectrometerOperator(cfg)

    # 取得校正前、校正後光譜與校正後光譜波峰
    old_spectrum = spec_op.fetch_spectrum()
    new_spectrum = calibration_spectrum(
        old_spectrum[0], old_spectrum[1], calibration_data
    )
    peak = max(new_spectrum[1])

    # 取得色相圖座標與亮度
    sd = spectrum_to_spectral_distribution(new_spectrum[0], new_spectrum[1])
    cie_XYZ = colour.sd_to_XYZ(sd)
    cie_xy = colour.XYZ_to_xy(cie_XYZ)
    liminous_flux = cie_XYZ[1]

    return old_spectrum, new_spectrum, liminous_flux, cie_xy, peak


# Functions
def measure(cfg_path: Path, calibration_path: Path) -> None:
    """進行測量

    Args:
        cfg_path (Path): 測試設定檔路徑
        calibration_path (Path): 校正檔路徑
    """
    # Create Folder
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Load Data
    cfg = TestConfig("", Path(SAVE_CONFIG_DIR))
    cfg.load_config(cfg_path)
    calibration_data = load_calibration_data(calibration_path)

    # measuring data
    blaze_op = BlazeOperator(cfg)
    blaze_op.open()
    temperatures = cfg.test_parameters["temperatures"]
    colors = cfg.test_parameters["colors"]
    currents = cfg.test_parameters["currents"]
    for temp in temperatures:
        blaze_op.change_temperature(temp)
        for color in colors:
            for current in currents:
                # Set LED State and Current
                led_state = {k: False for k in cfg.test_parameters["colors"]}
                led_state[color] = True
                blaze_op.set_led_state(
                    state=LedState(**led_state),
                    current=LedCurrent(**{color: current}),
                )

                # DEBUG LED Data
                led_temp = blaze_op.blaze.temperature_controller.get_temperature()
                print(f"Measuring spectra at temp: {temp}, ", end="")
                print(f"LED temp: {led_temp}, ", end="")
                print(f"color: {color}, ", end="")
                print(f"current: {current}mA")

                # Fetch Spectometer data
                old_spectrum, new_spectrum, liminous_flux, cie_xy, peak = (
                    run_spectrometer(cfg, calibration_data)
                )

                # Save data to excel
                save_file_prefix = f"{OUTPUT_DIR}{temp}_{color}_{current}"
                data = {
                    "校正前光譜波長": old_spectrum[0],
                    "校正前光譜強度": old_spectrum[1],
                    "校正後光譜波長": new_spectrum[0],
                    "校正後光譜強度": new_spectrum[1],
                    "亮度": [liminous_flux],
                    "色座標": cie_xy,
                    "波長": [peak],
                }
                pd.DataFrame.from_dict(data, orient="index").to_excel(
                    f"{save_file_prefix}_data.xlsx"
                )
                print(f"亮度: {liminous_flux}, 色座標: {cie_xy}, 波長: {peak}")

                # Draw and Save CIE Plot
                fig, _ = draw_cie_xy_plot(cie_xy)
                fig.savefig(f"{save_file_prefix}_color_space.png")
                plt.show(fig)

    blaze_op.close()


def measure_in_temp(cfg_path: Path, temperature: float = 25) -> None:
    """進行測量

    Args:
        cfg_path (Path): 測試設定檔路徑
        temperature (float, optional): 測試的 LED 溫度. Defaults to 25.
    """

    # Create Folder
    Path(SAVE_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Load Config data
    cfg = TestConfig(list_devices()[0].serial_number, Path(SAVE_CONFIG_DIR))
    cfg.load_config(cfg_path)

    # measure
    blaze_op = BlazeOperator(cfg)
    blaze_op.open()
    blaze_op.change_temperature(temperature)
    for color in cfg.test_parameters["colors"]:
        for current in cfg.test_parameters["currents"]:
            # Set LED State and Current
            led_state = {k: False for k in cfg.test_parameters["colors"]}
            led_state[color] = True
            blaze_op.set_led_state(
                state=LedState(**led_state),
                current=LedCurrent(**{color: current}),
            )

            # DEBUG LED Data
            led_temp = blaze_op.blaze.temperature_controller.get_temperature()
            print(f"Measuring spectra at temp: {temperature}, ", end="")
            print(f"LED temp: {led_temp}, ", end="")
            print(f"color: {color}, ", end="")
            print(f"current: {current}mA")

            # Fetch Spectometer data
            old_spectrum, new_spectrum, liminous_flux, cie_xy, peak = run_spectrometer(
                cfg
            )

            # Save data to json
            data = {
                "校正前光譜波長": old_spectrum[0],
                "校正前光譜強度": old_spectrum[1],
                "校正後光譜波長": new_spectrum[0],
                "校正後光譜強度": new_spectrum[1],
                "亮度": [liminous_flux],
                "色座標": cie_xy,
                "波長": [peak],
            }
            out_data_file = (
                Path(OUTPUT_DIR) / f"{temperature}_{color}_{current}_data.json"
            )
            with out_data_file.open("w+") as f:
                json.dump(data, f)

            # Draw and Save CIE Plot
            out_fig_file = (
                Path(OUTPUT_DIR) / f"{temperature}_{color}_{current}_color_space.png"
            )
            fig, _ = draw_cie_xy_plot(cie_xy[3])
            fig.savefig(out_fig_file)
            plt.show(fig)

    blaze_op.close()
