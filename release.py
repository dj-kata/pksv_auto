#!/usr/bin/python3
# usage: $0 num_box(default=1)
import nxbt
import time, sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hdl1 = logging.FileHandler(filename='log/release_egg.log')
hdl1.setLevel(logging.INFO)
hdl1.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
hdl2 = logging.StreamHandler()
hdl2.setLevel(logging.INFO)
hdl2.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
logger.addHandler(hdl1)
logger.addHandler(hdl2)

num_box=1
if len(sys.argv) > 1:
    num_box = int(sys.argv[1])

cmd = input('ボックスの先頭にカーソルがありますか? (y/) ')
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

def release_one():
    nx.press_buttons(controller_index, [nxbt.Buttons.A])
    nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_UP])
    nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_UP])
    nx.press_buttons(controller_index, [nxbt.Buttons.A])
    time.sleep(0.5)
    nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_UP])
    nx.press_buttons(controller_index, [nxbt.Buttons.A])
    time.sleep(1.0)
    nx.press_buttons(controller_index, [nxbt.Buttons.A])
    time.sleep(0.5)

def release_oneline():
    for i in range(6):
        release_one()
        if i < 5:
            nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_RIGHT])
    for i in range(5):
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_LEFT])

logger.info('孵化開始')
for i in range(num_box):
    logger.info(f"i,j = ({i},0), release_line")
    release_oneline()
    for j in range(4):
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_DOWN])
        logger.info(f"i,j = ({i},{j+1}), release_line")
        release_oneline()
    # 次のボックスへ移動
    for j in range(4):
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_UP])
    nx.press_buttons(controller_index, [nxbt.Buttons.R])
    time.sleep(2)

logger.info(f'完了しました！')