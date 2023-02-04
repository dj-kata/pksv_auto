import logging
from JoycontrolPlugin import JoycontrolPlugin, JoycontrolPluginError
import time, sys, os

logger = logging.getLogger(__name__)

#スタート地点: ホーム画面から

class egg_swap(JoycontrolPlugin):
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
        await self.button_ctl('left',p_sec=0.1,w_sec=0.2)
        # 孵化済の列へ移動
        if idx > 0:
            # 2～5匹目を同時選択
            await self.button_ctl('down',p_sec=0.2,w_sec=2.2)
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

    async def run(self):
        if self.options is None:
            raise JoycontrolPluginError('Plugin options is not set.')
        await self.swap(int(self.options[0]))