import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class quit(JoycontrolPlugin):
    async def button_ctl(self, *buttons, p_sec=0.05, w_sec=0.05):
        # ボタンの押下時間と解放後待機時間を指定する
        await self.button_press(*buttons)
        await self.wait(p_sec)
        await self.button_release(*buttons)
        await self.wait(w_sec)
    async def run(self):
        # ゲーム終了
        await self.button_ctl('home',p_sec=0.3, w_sec=1.0)
        await self.button_ctl('x',w_sec=1.0)
        await self.button_ctl('a',w_sec=4.5)
