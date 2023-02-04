import logging
from JoycontrolPlugin import JoycontrolPlugin
import time, sys, os

logger = logging.getLogger(__name__)

#スタート地点: ホーム画面から, ライドした状態(plus周りの無反応が防ぎづらい)

class egg_hatch_col(JoycontrolPlugin):
    async def button_ctl(self, *buttons, p_sec=0.05, w_sec=0.05):
        # ボタンの押下時間と解放後待機時間を指定する
        await self.button_press(*buttons)
        await self.wait(p_sec)
        await self.button_release(*buttons)
        await self.wait(w_sec)

    async def hatch_egg(self):
        #await self.button_ctl('plus', p_sec=0.2, w_sec=2.0)

        limit_time = time.time() + 200
        limit_time = time.time() + 250 # 11000属は少し長めに
        notice_time = time.time() + 60

        await self.right_stick(angle=315)
        await self.left_stick(angle=45)

        while time.time() < limit_time:
            await self.button_ctl('a')
            await self.wait(0.5)
            await self.button_ctl('a')
            await self.wait(0.5)
            #await self.button_ctl('l_stick')
            #await self.wait(0.5)
            
            if notice_time < time.time():
                logger.info('あと{}秒です'.format(round(limit_time-notice_time)))
                notice_time += 60

        await self.right_stick('center')
        await self.left_stick('center')
        await self.wait(1.5)
        #await self.button_ctl('plus', p_sec=0.2, w_sec=2.5)

    async def run(self):
        await self.hatch_egg()