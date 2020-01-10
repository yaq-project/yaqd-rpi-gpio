import asyncio
from typing import Dict, Any

import gpiozero  # type: ignore

from yaqd_core import Base, set_action


class PinDaemon(Base):
    _kind = "rpi-gpio-pin"
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.index = config["index"]
        self.mode = config["mode"]
        self.pull_up = config["pull_up"]
        if self.mode == "in":
            self.controller = gpiozero.DigitalInputDevice(pin=self.index, pull_up=self.pull_up)
        elif self.mode == "out":
            self.controller = gpiozero.DigitalOutputDevice(pin=self.index)
        self.set_value(self.value)

    def _connection_lost(self, peername):
        super()._connection_lost(peername)
        if len(self._clients) == 0:
            self.controller.value = 0

    def _load_state(self, state):
        """Load an initial state from a dictionary (typically read from the state.toml file).

        Must be tolerant of missing fields, including entirely empty initial states.

        Parameters
        ----------
        state: dict
            The saved state to load.
        """
        # TODO:
        super()._load_state(state)
        self.value = state.get("value", 0)

    def blink(self, up, down):
        self.controller.blink(up, down)

    def get_state(self):
        state = super().get_state()
        state["value"] = self.get_value()
        return state

    def get_value(self):
        return self.value

    @set_action
    def set_value(self, value):
        # TODO: consider if error should be raised in certain modes
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
