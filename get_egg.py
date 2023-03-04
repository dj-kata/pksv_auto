#!/usr/bin/python3
# usage: $0 sleeptime(default=220)
import nxbt
import time, sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hdl1 = logging.FileHandler(filename='log/get_egg.log')
hdl1.setLevel(logging.INFO)
hdl1.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
hdl2 = logging.StreamHandler()
hdl2.setLevel(logging.INFO)
hdl2.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
logger.addHandler(hdl1)
logger.addHandler(hdl2)

sleeptime = 220

if len(sys.argv) > 1:
    sleeptime = int(sys.argv[1])

cmd = input('ボックスの先頭を空き領域にしましたか??? (y/)')
if cmd.lower() != 'y':
    sys.exit()

logger.info('ペアリング開始')

# Start the NXBT service
nx = nxbt.Nxbt()

# Create a Pro Controller and wait for it to connect
controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
nx.wait_for_connection(controller_index)

nx.press_buttons(controller_index, [nxbt.Buttons.B])
time.sleep(2.0)
nx.press_buttons(controller_index, [nxbt.Buttons.HOME])
time.sleep(2.0)
nx.press_buttons(controller_index, [nxbt.Buttons.HOME])
time.sleep(2.0)

limit_time = time.time() + 1800
notice_time = time.time() + sleeptime

logger.info('タマゴうみ開始')
while time.time() < limit_time:
    if notice_time < time.time():
        mm = round(limit_time-time.time()) // 60
        ss = round(limit_time-time.time()) % 60
        print(f'あと{mm}分{ss}秒です')
        for i in range(5):
            nx.press_buttons(controller_index, [nxbt.Buttons.A])
            time.sleep(0.8)
        for i in range(100):
            nx.press_buttons(controller_index, [nxbt.Buttons.B])
            #time.sleep(0.8)
        notice_time += sleeptime
logger.info(f'完了しました！')