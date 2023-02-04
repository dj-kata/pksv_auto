import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

#スタート地点: ホーム画面から

class start(JoycontrolPlugin):
    async def button_ctl(self, *buttons, p_sec=0.05, w_sec=0.05):
        # ボタンの押下時間と解放後待機時間を指定する
        await self.button_press(*buttons)
        await self.wait(p_sec)
        await self.button_release(*buttons)
        await self.wait(w_sec)
    async def run(self):
        await self.button_ctl('a',p_sec=0.2,w_sec=2.6) # ソフト選択
        await self.button_ctl('a',p_sec=0.2,w_sec=1.5) # ユーザ選択