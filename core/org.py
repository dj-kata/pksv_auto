import logging
from JoycontrolPlugin import JoycontrolPlugin
import time, sys, os

logger = logging.getLogger(__name__)

#スタート地点: ホーム画面から

class hatch_egg(JoycontrolPlugin):
    async def button_ctl(self, *buttons, p_sec=0.05, w_sec=0.05):
        # ボタンの押下時間と解放後待機時間を指定する
        await self.button_press(*buttons)
        await self.wait(p_sec)
        await self.button_release(*buttons)
        await self.wait(w_sec)
    # 手持ちの孵化済みポケモンをBOXに戻し、次の卵を手持ちに入れる
    # idx=0の場合は1列目の卵の移動のみ行う
    async def swap(self, idx):
        await self.button_ctl('x',p_sec=0.2,w_sec=1.5)
        await self.button_ctl('a',p_sec=0.2,w_sec=1.7)
        await self.button_ctl('left',p_sec=0.2,w_sec=0.2)
        # 孵化済の列へ移動
        if idx > 0:
            # 2～5匹目を同時選択
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('minus',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('a',p_sec=0.2,w_sec=0.5)
            for i in range(idx):
                await self.button_ctl('right',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('up',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('a',p_sec=0.2,w_sec=0.5)

        # 次のたまご列を選択
        if idx < 6:
            await self.button_ctl('right',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('minus',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('a',p_sec=0.2,w_sec=0.5)
            # 手持ちに移動
            for i in range(idx+1):
                await self.button_ctl('left',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('down',p_sec=0.2,w_sec=0.2)
            await self.button_ctl('a',p_sec=0.2,w_sec=0.5)

        # メニューを閉じる
        await self.button_ctl('b',p_sec=0.2,w_sec=1.5)
        await self.button_ctl('b',p_sec=0.2,w_sec=0.5)
        await self.button_ctl('b',p_sec=0.2,w_sec=0.5)

    async def hatch_egg(self):
        await self.button_ctl('plus', w_sec=2.0)

        limit_time = time.time() + 200
        notice_time = time.time() + 60

        await self.right_stick(angle=315)
        await self.left_stick(angle=45)

        while time.time() < limit_time:
            await self.button_ctl('a')
            await self.wait(0.5)
            await self.button_ctl('a')
            await self.wait(0.5)
            await self.button_ctl('l_stick')
            await self.wait(0.5)
            
            if notice_time < time.time():
                logger.info('あと{}秒です'.format(round(limit_time-notice_time)))
                notice_time += 60

        await self.right_stick('center')
        await self.left_stick('center')
        await self.button_ctl('plus', p_sec=0.2, w_sec=2.5)
    
    async def next_box(self):
        await self.button_ctl('x',p_sec=0.2,w_sec=1.5)
        await self.button_ctl('a',p_sec=0.5,w_sec=1.7)
        await self.button_ctl('r',p_sec=0.2,w_sec=0.5)
        await self.button_ctl('b',p_sec=0.2,w_sec=1.5)
        await self.button_ctl('b',p_sec=0.2,w_sec=0.5)
        await self.button_ctl('b',p_sec=0.2,w_sec=0.5)

    async def run(self):
        #await self.button_ctl('plus', p_sec=0.2)
        num_box=3
        for j in range(num_box):
            for i in range(6):
                await self.swap(i)
                await self.hatch_egg()
            await self.swap(6)
            await self.next_box()