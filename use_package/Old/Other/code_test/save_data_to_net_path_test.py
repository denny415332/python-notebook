import os
import subprocess

drive_letter = "Z:"  # 指定一個未使用的磁碟代號
remote_path = r"\\YOUNGOPTICS\UserHome\kexian.kuo"
user = r"YOUNGOPTICS\kexian.kuo"
password = "Kk95090415332"
filename = "example.txt"

# 1. 使用 net use 映射網路磁碟
subprocess.call(["net", "use", drive_letter, remote_path, password, "/user:" + user])

# 2. 寫入檔案到映射的磁碟中
file_path = os.path.join(drive_letter, filename)
with open(file_path, "w", encoding="utf-8") as f:
    f.write("這是一個測試內容，儲存在網路位置！")
print(f"檔案已成功儲存至 {file_path}")

# 3. 完成後斷開網路磁碟連線
subprocess.call(["net", "use", drive_letter, "/delete"])
