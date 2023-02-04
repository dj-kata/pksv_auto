#!/usr/bin/python3
# 初期位置: カメラ移動だけで3人のメッセージが見える位置
# 1日前でセーブ&ゲーム終了 -> 1日後にして起動 -> メッセージが出た状態で開始
# (本体の再起動だけでリセマラができる状態)
# ->でHome押下->コントローラ->持ちかた/順番を変えるでAを押した状態
# (コントローラの接続が解除される)

# キャプチャ画像を/share/obs/obs.pngから取得する前提としているが、
# 直接キャプチャボードを接続する場合はcv2.imread()の部分をカスタマイズすること。
# キャプボ映像にScreenshot Filterを挿入して、
# raspi4上のsamba共有ディレクトリに直接書いていけばよい
# Screenshot FilterのDestinationはOutput to fileとする。

# 濁音・半濁音の判定がかなり難しいため、全て清音に直してから判定している。
# そのため、検出対象の文字列も「ラフラフ」などになっている

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

hdl1 = logging.FileHandler(filename='seri.log')
hdl1.setLevel(logging.INFO)
hdl1.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
hdl2 = logging.StreamHandler()
hdl2.setLevel(logging.INFO)
hdl2.setFormatter(logging.Formatter("%(asctime)s   %(message)s"))
logger.addHandler(hdl1)
logger.addHandler(hdl2)

cap_img     = '/share/obs/obs.png'
bt_macaddr  = 'BC:9E:BB:F4:07:13'
webhook_url = 'https://discord.com/api/webhooks/637686494991089684/rzUsDWKFN5FLnpXq3JR9ZirvwbkE3hcV_w0z6Ixo7G5Om9cE6MWdMyJ6CHwWVipX_z-l'
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
    logger.info(f"diff = {diff:.4f}")
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
    logger.info(f"sum = {img.sum()}")
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

if __name__ == '__main__':

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

    logger.info(f"コントローラのペアリングを開始")
    os.system(f"sudo joycontrol-pluginloader -r {bt_macaddr} common/pairing.py")

    while True:
        logger.info(f"ii = {ii}")
        logger.info('\n\nOCR is running...\n\n')
        while 1: # ウィンドウが出る前にキャプチャを拾ってしまった場合の対策
            ocr = get_seri()
            if ocr != '':
                break
        tmp = ocr
        for c in conv:
            tmp = tmp.replace(c[0], c[1])
        for t in target:
            if t in tmp:
                chk = True
                break
        if chk:
            logger.info(f'ii={ii} 対象アイテムが見つかりました！! ({t})')
            discord.post(content=f'対象アイテムが見つかりました！(ii={ii}, {t})')
            break
        logger.info('not found! quiting...')
        os.system(f'sudo joycontrol-pluginloader -r {bt_macaddr} common/quit.py')
        time.sleep(1)
        logger.info('resetting...')
        os.system(f'sudo joycontrol-pluginloader -r {bt_macaddr} common/start.py')
        # タイトル画面を待つ
        while True:
            st = judge_startscreen()
            if st > 0.94:
                break
            else:
                time.sleep(0.5)
                continue
        os.system(f'sudo joycontrol-pluginloader -r {bt_macaddr} common/press_a.py')
        time.sleep(7) # 確実に黒画面に入るようにsleep
        # 黒画面終了を待つ
        while True:
            blk = judge_black()
            if not blk:
                break
            else:
                time.sleep(0.5)
                continue
        os.system(f'sudo joycontrol-pluginloader -r {bt_macaddr} core/move_camera_seri.py')
        ii+=1
