import logging
from JoycontrolPlugin import JoycontrolPlugin
import time, sys, os

logger = logging.getLogger(__name__)

#スタート地点: ホーム画面から

class egg_next_box(JoycontrolPlugin):
    async def button_ctl(self, *buttons, p_sec=0.05, w_sec=0.05):
        # ボタンの押下時間と解放後待機時間を指定する
        await self.button_press(*buttons)
        await self.wait(p_sec)
        await self.button_release(*buttons)
        await self.wait(w_sec)
    
    async def next_box(self):
        await self.button_ctl('x',p_sec=0.2,w_sec=1.5)
        await self.button_ctl('a',p_sec=0.5,w_sec=1.7)
        await self.button_ctl('r',p_sec=0.2,w_sec=0.5)
        await self.button_ctl('b',p_sec=0.2,w_sec=1.5)
        await self.button_ctl('b',p_sec=0.2,w_sec=0.5)
        await self.button_ctl('b',p_sec=0.2,w_sec=0.5)

    async def run(self):
        await self.next_box()