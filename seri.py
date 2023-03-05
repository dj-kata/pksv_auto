#!/usr/bin/python3
# usage: $0 num_box(default=1)
import nxbt

from PIL import Image, ImageOps
import sys, cv2, time, re
import numpy as np

import pyocr
import pyocr.builders

import os
from discordwebhook import Discord
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hdl1 = logging.FileHandler(filename='log/seri.log')
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

cap_img     = '/share/obs/obs.png'
webhook_url = 'https://discord.com/api/webhooks/........'
discord     = Discord(url=webhook_url)

# OP画面を事前に用意したものと比較し、類似度を返す
def judge_startscreen():
    target = cv2.imread('./data/title.png')
    while True:
        try:
            img = cv2.imread(cap_img)
        except:
            time.sleep(0.2)
            continue
        if img is not None:
            break
    hist1 = cv2.calcHist([target],[2],None,[256],[0,256])
    hist2 = cv2.calcHist([img],[2],None,[256],[0,256])
    diff = cv2.compareHist(hist1,hist2,0)
    #logger.info(f"diff = {diff:.4f}")
    return diff

# 黒画面かどうかを判定する
def judge_black():
    while True:
        try:
            img = cv2.imread(cap_img)
        except:
            time.sleep(0.2)
            continue
        if img is not None:
            break
    img = img[0:800,:]
    #logger.info(f"sum = {img.sum()}")
    ret = False
    if img.sum() < 100000:
        ret = True
    return ret

def get_seri():
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        logger.error("No OCR tool found")
        sys.exit(1)

    tool = tools[0]
    logger.info("Will use tool '%s'" % (tool.get_name()))

    while True:
        try:
            img = cv2.imread(cap_img)
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
            break
        except:
            time.sleep(0.2)
            continue
    ymask = cv2.inRange(img_hsv, np.array([30,127,0]),np.array([40,255,255]))
    res = cv2.bitwise_and(img, img, mask=ymask)

    # 収縮フィルタでノイズ除去
    kernel = np.ones((5,5),np.uint8)
    res = cv2.erode(res,kernel,iterations = 4)
    kernel = np.ones((3,3),np.uint8)
    res = cv2.erode(res,kernel,iterations = 1)
    res = cv2.dilate(res,kernel,iterations = 1)


    ii = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)
    ii = cv2.adaptiveThreshold(ii, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,9)
    contours, hierarchy = cv2.findContours(ii, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    msgs = [] # メッセージウィンドウ座標の集合
    for i in range(len(contours)):
        cnt = contours[i]
        x,y,w,h = cv2.boundingRect(cnt)
        if h > 89 and h < 120 and w > 180:
            skip = False
            for m in msgs: # 既存のメッセージから遠くないものは除外
                dist2 = (m[0]-x)*(m[0]-x)+(m[1]-y)*(m[1]-y)
                if dist2 < 400*400:
                    skip = True
            if not skip:
                res = cv2.rectangle(res, (x,y), (x+w,y+h), (0,0,255), 2)
                msgs.append([x,y,w,h])

    ret = ''
    # メッセージ枠が3つあれば処理
    # move_camera_seriが動かなかった場合ここで止められるので、
    # 気になる場合は2にする等してください
    if len(msgs) >= 3:
        for m in msgs:
            x,y,w,h = m
            tmp_res=img[y:y+h,x:x+w]
            pilimg = Image.fromarray(tmp_res)

            txt = tool.image_to_string(
                pilimg,
                lang="jpn",
                builder=pyocr.builders.TextBuilder(tesseract_layout=6)
            )
            ret += txt

    cv2.imwrite('detect.png', res)
    cv2.imwrite('input.png', img)
    return ret

def pk_start():
    nx.press_buttons(controller_index, [nxbt.Buttons.A])
    time.sleep(2.5)
    nx.press_buttons(controller_index, [nxbt.Buttons.A])
    time.sleep(1.4)

def pk_quit():
    nx.press_buttons(controller_index, [nxbt.Buttons.HOME])
    time.sleep(0.9)
    nx.press_buttons(controller_index, [nxbt.Buttons.X])
    time.sleep(0.9)
    nx.press_buttons(controller_index, [nxbt.Buttons.A])
    time.sleep(4.4)

def move_camera():
    nx.tilt_stick(controller_index, nxbt.Sticks.RIGHT_STICK,  0,  -100, tilted=1.0)
    time.sleep(0.3)

def release_oneline():
    for i in range(6):
        release_one()
        if i < 5:
            nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_RIGHT])
            time.sleep(0.1)
    for i in range(5):
        nx.press_buttons(controller_index, [nxbt.Buttons.DPAD_LEFT])
        time.sleep(0.1)

def do():
    target=['ラフラフ', 'ルアー', 'レヘル', 'フレント', 'ヘヒー', 'ムーン','スヒート','トリーム']
    conv=[
        ['バ','ハ'],
        ['ビ','ヒ'],
        ['ブ','フ'],
        ['ベ','ヘ'],
        ['ボ','ホ'],
        ['パ','ハ'],
        ['ピ','ヒ'],
        ['プ','フ'],
        ['ペ','ヘ'],
        ['ポ','ホ'],
        ['ド','ト'],
        ['一','ー'],
        ['-','ー'],
    ]
    chk = False
    ii = 1

    while True:
        logger.info(f"ii = {ii}")
        logger.info('OCR is running...')
        while 1: # ウィンドウが出る前にキャプチャを拾ってしまった場合の対策
            ocr = get_seri()
            if ocr != '':
                break
        tmp = ocr
        ocr_for_disp = ocr.replace('\n','')
        logger.info(f'ii={ii} ocr={ocr_for_disp}')
        for c in conv:
            tmp = tmp.replace(c[0], c[1])
        for t in target:
            if t in tmp:
                chk = True
                break
        if chk:
            logger.info(f'ii={ii} 対象アイテムが見つかりました！! ({t})')
            discord.post(content=f'@kata 対象アイテムが見つかりました！(ii={ii}, {t})')
            break
        logger.info('not found! quiting...')
        pk_quit()
        time.sleep(1)
        logger.info('resetting...')
        pk_start()
        # タイトル画面を待つ
        while True:
            st = judge_startscreen()
            if st > 0.94:
                logger.info(f"diff = {st:.4f}")
                break
            else:
                time.sleep(0.5)
                continue
        nx.press_buttons(controller_index, [nxbt.Buttons.A])
        time.sleep(7) # 確実に黒画面に入るようにsleep
        # 黒画面終了を待つ
        while True:
            blk = judge_black()
            if not blk:
                break
            else:
                time.sleep(0.5)
                continue
        move_camera()
        ii+=1

    logger.info(f'完了しました！')

do()