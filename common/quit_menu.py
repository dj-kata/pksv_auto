import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class quit_menu(JoycontrolPlugin):
    async def run(self):
        await self.button_push('b') # bボタンを押す
        await self.wait(0.5)
        await self.button_push('b') # bボタンを押す
        await self.wait(0.5)
        await self.button_push('b') # bボタンを押す
        await self.wait(0.5)
        await self.button_push('b') # bボタンを押す
        await self.wait(0.5)
        await self.button_push('b') # bボタンを押す
        await self.wait(0.5)
