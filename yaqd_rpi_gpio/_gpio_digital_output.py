__all__ = ["GpioDigitalOutput"]

import asyncio
from typing import Dict, Any, List

import gpiozero  # type: ignore

from yaqd_core import DiscreteHardware

from .__version__ import __branch__


class GpioDigitalOutput(DiscreteHardware):
    _kind = "gpio-digital-output"
    _version = "0.1.0" + f"+{__branch__}" if __branch__ else ""
    traits: List[str] = []
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.index = config["index"]
        self.controller = gpiozero.DigitalOutputDevice(pin=self.index)
        self.set_value(self.value)

    def _connection_lost(self, peername):
        super()._connection_lost(peername)
        if len(self._clients) == 0:
            self.controller.value = 0

    def get_state(self):
        state = super().get_state()
        state["value"] = self.value
        return state

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.controller.value = value

    async def update_state(self):
        """Continually monitor and update the current daemon state."""
        while True:
            self.value = self.controller.value
            self._busy = False
            if self.mode != "in":
                await self._busy_sig.wait()
            else:
                await asyncio.sleep(0.01)
