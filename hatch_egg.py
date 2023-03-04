#!/usr/bin/python3
# usage: $0 [num_box] [ptime]
import nxbt
import time, sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hdl1 = logging.FileHandler(filename='log/hatch_egg.log')
hdl1.setLevel(logging.INFO)
hdl1.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
hdl2 = logging.StreamHandler()
hdl2.setLevel(logging.INFO)
hdl2.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
logger.addHandler(hdl1)
logger.addHandler(hdl2)

num_box=1
ptime = 300
if len(sys.argv) > 1:
    num_box = int(sys.argv[1])
if len(sys.argv) > 2:
    ptime = int(sys.argv[2])

cmd = input('ボックスの先頭をタマゴ領域にしましたか??? (y/) : ')
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

def swap(idx):
    time.sleep(1)
    nx.press_buttons(controller_index, [nxbt.Buttons.X])
    time.sleep(1.4)
    nx.press_buttons(controller_index, [nxbt.Buttons.A])
    time.sleep(1.6)
    nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_LEFT])

    # 孵化済みの列へ移動
    if idx > 0:
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(2.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.MINUS])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.A])
        time.sleep(0.4)
        for i in range(idx):
            nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_RIGHT])
            time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_UP])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.A])
        time.sleep(0.4)
    
    # 次のたまご列を選択
    if idx < 6:
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_RIGHT])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.MINUS])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.A])
        time.sleep(0.4)
        # 手持ちに移動
        for i in range(idx+1):
            nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_LEFT])
            time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        time.sleep(0.1)
        nx.press_buttons(controller_index, [nxbt.Buttons.A])
        time.sleep(0.4)

    # 次のボックスへ
    if idx == 6:
        nx.press_buttons(controller_index, [nxbt.Buttons.R])
        time.sleep(0.4)

    # メニューを閉じる
    nx.press_buttons(controller_index, [nxbt.Buttons.B])
    time.sleep(1.4)
    nx.press_buttons(controller_index, [nxbt.Buttons.B])
    time.sleep(0.4)
    nx.press_buttons(controller_index, [nxbt.Buttons.B])
    time.sleep(0.4)

def hatch_col():
    ptime = 300
    limit_time = time.time() + ptime # 11000属は少し長めに
    notice_time = time.time() + 60
    #nx.tilt_stick(controller_index, nxbt.Sticks.LEFT_STICK,  100,  50, tilted=ptime, block=False)
    #nx.tilt_stick(controller_index, nxbt.Sticks.RIGHT_STICK, 100, -50, tilted=ptime, block=False)

    while time.time() < limit_time:
        nx.tilt_stick(controller_index, nxbt.Sticks.LEFT_STICK,  0,  100, tilted=2.5)
        nx.press_buttons(controller_index, [nxbt.Buttons.A])
        nx.tilt_stick(controller_index, nxbt.Sticks.LEFT_STICK,  0,  -100, tilted=2.5)
        nx.press_buttons(controller_index, [nxbt.Buttons.A])

        if notice_time<time.time():
            print('あと{}秒です'.format(round(limit_time-notice_time)))
            notice_time += 60

def do(num_box):
    logger.info('孵化開始')
    for i in range(num_box):
        logger.info(f"i,j = ({i},0), swap")
        swap(0)
        for j in range(1,7):
            logger.info(f"i,j = ({i},{j}), hatch")
            hatch_col()
            logger.info(f"i,j = ({i},{j}), swap")
            swap(j)
            time.sleep(2)
    logger.info(f'完了しました！')

do(num_box)