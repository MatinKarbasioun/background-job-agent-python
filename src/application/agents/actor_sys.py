import asyncio
from typing import Any

import pykka

from src.application.Time import Timer
from src.application.agents.messages import StartSystemCommand
from src.application.agents.time.timer import TimerAgent


class ActorSystem:
    actor_ref: pykka.ActorRef = None
    event_loop: asyncio.AbstractEventLoop = None
    timer_ref: pykka.ActorRef = None

    def __init__(self, initial_actor: type[pykka.ThreadingActor], timer: Timer, event_loop: asyncio.AbstractEventLoop, **initial_arguments):
        self._actor = initial_actor
        self._arguments = initial_arguments
        self._setup_loop(event_loop)
        self._timer = timer

    def start(self):
        print(self._arguments)
        ActorSystem.timer_ref = TimerAgent.start(timer=self._timer)
        ActorSystem.actor_ref = self._actor.start(**self._arguments)
        ActorSystem.actor_ref.tell(StartSystemCommand())

    @classmethod
    def _setup_loop(cls, loop: asyncio.AbstractEventLoop):
        ActorSystem.event_loop = loop

    @classmethod
    def tell(cls, msg: Any):
        ActorSystem.actor_ref.tell(msg)