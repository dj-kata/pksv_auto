#!/usr/bin/python3
# 初期位置: 食事パワー発動直後、カゴの前
# でHome押下->コントローラ->持ちかた/順番を変えるでAを押した状態
# (コントローラの接続が解除される)
import subprocess
import time, sys, os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hdl1 = logging.FileHandler(filename='get_egg.log')
hdl1.setLevel(logging.INFO)
hdl1.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
hdl2 = logging.StreamHandler()
hdl2.setLevel(logging.INFO)
hdl2.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
logger.addHandler(hdl1)
logger.addHandler(hdl2)

bt_macaddr  = 'BC:9E:BB:F4:07:13'

limit_time = time.time() + 1800
notice_time = time.time() + 220

cmd = input('ボックスの先頭を空き領域にしましたか??? (y/)')
if cmd.lower() != 'y':
    sys.exit()
logger.info(f"コントローラのペアリングを開始")
os.system(f"sudo joycontrol-pluginloader -r {bt_macaddr} common/pairing.py")
logger.info('孵化作業開始')
os.system('date')
while time.time() < limit_time:
    if notice_time < time.time():
        os.system(f"timeout 2 sudo joycontrol-pluginloader -r {bt_macaddr} core/get_egg_core.py")
        mm = round(limit_time-time.time()) // 60
        ss = round(limit_time-time.time()) % 60
        logger.info(f'あと{mm}分{ss}秒です')
        notice_time += 220
logger.info(f'完了しました！')