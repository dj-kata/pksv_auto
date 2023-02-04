import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class pairing(JoycontrolPlugin):
    async def run(self):
        # Press the A button when the controller is ready for input.
        logger.info('Pairing completed.')
        await self.button_push('a') # exit
        await self.wait(5.0)
        await self.button_push('b') # exit
        await self.wait(1.0)
        await self.button_push('home') # exit
        await self.wait(2.0)
