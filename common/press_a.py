import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class press_a(JoycontrolPlugin):
    async def run(self):
        await self.button_push('a') # Aボタンを押す
        await self.wait(0.5)
