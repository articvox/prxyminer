from __future__ import annotations

import logging
import threading
from typing import Callable

import schedule
import time


class Scheduler:

    @staticmethod
    def __run_in_thread(check_interval_s: int = 5) -> threading.Event:
        interruptible = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not interruptible.is_set():
                    schedule.run_pending()
                    time.sleep(check_interval_s)

        continuous = ScheduleThread()
        continuous.setDaemon(True)
        continuous.start()

        return interruptible

    def __init__(self):
        self.interrupt = None

    def start(self) -> Scheduler:
        if self.interrupt and not self.interrupt.is_set():
            logging.warning('Scheduler already running, discarding start request')
        else:
            self.interrupt = Scheduler.__run_in_thread()
        return self

    def stop(self) -> Scheduler:
        if self.interrupt and self.interrupt.is_set():
            logging.warning('Scheduler already stopped, discarding stop request')
        else:
            self.interrupt.set()
        return self

    def schedule(self, interval: int, callback: Callable, run_on_schedule = True) -> Scheduler:
        schedule.every(interval).seconds.do(callback)
        if run_on_schedule:
            callback()

        return self
