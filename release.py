#!/usr/bin/python3
# usage: python3 release.py 逃したいbox数
# 初期位置: 逃したいやつで埋めたboxの左上
# でHome押下->コントローラ->持ちかた/順番を変えるでAを押した状態
# (コントローラの接続が解除される)
# 走査方向は上から下へのジグザグ順
import subprocess
import time, sys, os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hdl1 = logging.FileHandler(filename='release.log')
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

cmd = input('ボックスの先頭にカーソルがありますか? (y/)')
if cmd.lower() != 'y':
    sys.exit()
logger.info(f"コントローラのペアリングを開始")
os.system(f"sudo joycontrol-pluginloader -r {bt_macaddr} common/pairing.py")
logger.info('リリース開始')
os.system(f"timeout 2 sudo joycontrol-pluginloader -r {bt_macaddr} core/release.py -p {sys.argv[1]}")
logger.info(f'完了しました！')