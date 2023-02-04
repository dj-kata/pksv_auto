import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

#スタート地点: ホーム画面から

class move_camera_seri(JoycontrolPlugin):
    async def button_ctl(self, *buttons, p_sec=0.05, w_sec=0.05):
        # ボタンの押下時間と解放後待機時間を指定する
        await self.button_press(*buttons)
        await self.wait(p_sec)
        await self.button_release(*buttons)
        await self.wait(w_sec)
    async def run(self):
        # カメラ移動
        await self.right_stick(angle=270)
        await self.wait(1.0)
        await self.right_stick('center')
        await self.wait(2.0)
