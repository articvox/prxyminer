from __future__ import annotations

import logging
import threading
from typing import Callable

import schedule


class Scheduler:

    @staticmethod
    def __run() -> threading.Event:
        interruptible = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not interruptible.is_set():
                    schedule.run_pending()

        continuous = ScheduleThread()
        continuous.setDaemon(True)
        continuous.start()

        return interruptible

    def __init__(self):
        self.interruptible = None

    def start(self) -> Scheduler:
        if self.interruptible and not self.interruptible.is_set():
            logging.warning('Scheduler already running - discarding start request')
        else:
            self.interruptible = Scheduler.__run()

        return self

    def stop(self) -> Scheduler:
        if not self.interruptible or (self.interruptible and self.interruptible.is_set()):
            logging.warning('Scheduler already stopped - discarding stop request')
        else:
            self.interruptible.set()

        return self

    def interval(self, interval_s: int, callback: Callable) -> Scheduler:
        try:
            callback()
        finally:
            schedule.every(interval_s).seconds.do(callback)
            return self
