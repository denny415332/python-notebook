# Packages
from pathlib import Path
from time import time
import pandas as pd
import numpy as np
import colour
from src.device_operator import BlazeOperator, SpectrometerOperator
from src.testcfg import TestConfig, BlazeOpTestCfg, SpectrometerOpTestCfg
from src.calc import (
    extract_spectrum_peaks,
    spectrum_to_spectral_distribution,
    calibrate_spectrum,
)
from src.output_data import SummaryOutput, SpectrumOutput


# Constant
SAVE_CONFIG_DIR = "config_data/"
"儲存設定檔的資料夾路徑"
OUTPUT_DIR = "output/"
"檔案輸出資料夾路徑"


def load_calibration_data(calibration_path: Path) -> tuple[list[float], list[float]]:
    """加載校正資料

    Args:
        calibration_path (Path): 校正檔路徑

    Returns:
        tuple[list[float], list[float]]: 校正資料[[波長, u焦耳/次數], ...]
    """
    df = pd.read_csv(str(calibration_path))
    cal_wavelength, cal_params = df.T.to_numpy()
    return cal_wavelength, cal_params


def fetch_led_data(
    blaze_op: BlazeOperator,
    cfg: TestConfig,
    led_color: str,
    led_current: float,
    led_temp_ref: float,
    calibration_data: tuple[list[float], list[float]],
) -> tuple[np.ndarray, np.ndarray, tuple[float, float], float, float]:
    """獲取 LED 資料

    Args:
        blaze_op (BlazeOperator): Blaze 控制器
        cfg (TestConfig): 測試設定檔資料
        led_color (str): LED 顏色
        led_current (float): LED 電流
        led_temp_ref (float): LED 溫度設定值
        calibration_data (tuple[list[float], list[float]]): 校正資料

    Returns:
        tuple[np.ndarray, np.ndarray, tuple[float, float], float, float]: (LED 光譜, 校正後光譜, 校正後光譜波峰資料(波長, 強度), 量測時 LED 溫度, 量測時 LED 電流)
    """

    led_spectrum = []  # LED 光譜
    cal_spectrum = []  # 校正後光譜
    cal_spectrum_peak = []  # 校正後光譜波峰資料(波長, 強度)
    led_temp = -1  # 量測時 LED 溫度
    led_current = -1  # 量測時 LED 電流

    spec_op = SpectrometerOpTestCfg(cfg)

    # 開啟 LED 燈光並調整溫度
    blaze_op.set_led_state(led_color, led_current)
    blaze_op.change_temperature(led_temp_ref)

    # 調整並取得積分時間
    int_time_micros = spec_op.adjust_integration_time()
    print(f"Adjusted integration time: {int_time_micros/1e6}s")

    # 關閉 LED 燈光，取得背景光譜
    blaze_op.close_led()
    bkg_spectrum = spec_op.fetch_spectrum(int_time_micros)

    # 開啟 LED 燈光，取得 LED 燈光光譜
    blaze_op.set_led_state(led_color, led_current)
    led_spectrum = spec_op.fetch_spectrum(int_time_micros)

    # 計算校正後光譜，並取得其波峰資訊
    cal_spectrum = calibrate_spectrum(
        led_spectrum, bkg_spectrum, calibration_data, int_time_micros / 1e6
    )
    cal_spectrum_peak = extract_spectrum_peaks(cal_spectrum)

    # LED 資訊(溫度、電流)
    led_temp = blaze_op.get_led_temp()
    led_current = blaze_op.get_led_current(led_color)

    return led_spectrum, cal_spectrum, cal_spectrum_peak, led_temp, led_current


def calculate_required_data(
    cal_spectrum: tuple[list[float], list[float]],
) -> tuple[list[float, float], float]:
    """計算所需資料

    Args:
        cal_spectrum (tuple[list[float], list[float]]): 校正後光譜

    Returns:
        tuple[list[float, float], float]: (CIE 1931 XY 座標, 燈光亮度)
    """
    sd = spectrum_to_spectral_distribution(cal_spectrum)
    cie_XYZ = colour.sd_to_XYZ(sd, k=683.002)
    cie_xy = colour.XYZ_to_xy(cie_XYZ)
    liminous_flux = cie_XYZ[1]

    return cie_xy, liminous_flux


# Functions
def measure(
    cfg_path: Path,
    calibration_path: Path,
    SN: str,
    OPND: str,
    LH_or_RH: str,
) -> None:
    """進行測量

    Args:
        cfg_path (Path): 測試設定檔路徑
        calibration_path (Path): 校正檔路徑
        serial_number (int): 光機序號
        op_number (int): 操作員序號
    """
    # 程式碼開始運作時間
    start_time = time()

    # Create Output Folder
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Output data
    summary_out = SummaryOutput()
    spectrum_out = SpectrumOutput()

    # 設定操作員資料以及程式碼運作開始時間
    summary_out.set_operation_data(SN, OPND, LH_or_RH)

    # Load Data
    cfg = TestConfig(SN, Path(SAVE_CONFIG_DIR), OPND)
    cfg.load_config(cfg_path)
    cfg.set_serial_number(SN)
    cfg.set_operator_number(OPND)
    calibration_data = load_calibration_data(calibration_path)

    # measuring data
    blaze_op = BlazeOpTestCfg(cfg)
    blaze_op.open()
    temperatures = cfg.test_parameters["temperatures"]
    colors = cfg.test_parameters["colors"]
    currents = cfg.test_parameters["currents"]
    for temp in temperatures:
        for color in colors:
            for current in currents:
                # Fetch LED data
                led_spectrum, cal_spectrum, cal_spectrum_peak, led_temp, led_current = (
                    fetch_led_data(
                        blaze_op, cfg, color, current, temp, calibration_data
                    )
                )
                cie_xy, liminous_flux = calculate_required_data(cal_spectrum)

                spectrum_out.set_spectrum_data()

    blaze_op.close()

    # 設置程式碼結束時間
    end_time = time()
    process_time = end_time - start_time
    summary_out.set_code_total_time(process_time)
