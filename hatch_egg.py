import time, sys, os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hdl1 = logging.FileHandler(filename='hatch.log')
hdl1.setLevel(logging.INFO)
hdl1.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
hdl2 = logging.StreamHandler()
hdl2.setLevel(logging.INFO)
hdl2.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
logger.addHandler(hdl1)
logger.addHandler(hdl2)

bt_macaddr  = 'BC:9E:BB:F4:07:13'

num_box=1
if len(sys.argv) > 1:
    num_box = int(sys.argv[1])


logger.info(f"コントローラのペアリングを開始")
os.system(f"sudo joycontrol-pluginloader -r {bt_macaddr} common/pairing.py")

logger.info(f"num_box = {num_box}")

for i in range(num_box):
    logger.info(f"i,j = ({i},0), swap")
    os.system(f"sudo joycontrol-pluginloader -r {bt_macaddr} core/egg_swap.py -p 0")
    for j in range(1,7):
        logger.info(f"i,j = ({i},{j}), hatch")
        os.system(f"sudo joycontrol-pluginloader -r {bt_macaddr} core/egg_hatch_col.py")
        logger.info(f"i,j = ({i},{j}), swap")
        os.system(f"sudo joycontrol-pluginloader -r {bt_macaddr} core/egg_swap.py -p {j}")

    os.system(f"sudo joycontrol-pluginloader -r {bt_macaddr} core/egg_next_box.py")
