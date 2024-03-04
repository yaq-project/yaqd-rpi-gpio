__all__ = ["GpioPwmOutput"]

import time
import asyncio
from typing import Dict, Any, List

import gpiozero  # type: ignore

from yaqd_core import HasLimits, HasPosition, IsDaemon

from .__version__ import __branch__


class GpioPwmOutput(HasLimits, HasPosition, IsDaemon):
    _kind = "gpio-pwm-output"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._controller = gpiozero.PwmOutputDevice(
            pin=config["index"], frequency=config["pwm_frequency"]
        )
        self._watchdog_fed_time = time.time()
        if self._config["watchdog_timeout"] is not None:
            self._loop.create_task(self.watchdog)

    def _connection_lost(self, peername):
        super()._connection_lost(peername)
        if len(self._clients) == 0:
            self._controller.value = 0

    def _set_position(self, value):
        self._controller.value = value
        self._watchdog_fed_time = time.time()

    async def update_state(self):
        while True:
            self._state["position"] = self._controller.value
            await self._busy_sig.wait()

    async def watchdog(self):
        while True:
            if time.time() - self._watchdog_fed_time > self._config["watchdog_timeout"]:
                self._set_position(self._config["watchdog_timeout_destination"])
            await asyncio.sleep(1)
