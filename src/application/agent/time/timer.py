import copy
import time

import pykka
from kink import inject

from src.application.Time import Timer
from src.application.agent.message.time import *


@inject
class TimerAgent(pykka.ThreadingActor):
    def __init__(self, timer: Timer):
        super().__init__()
        self.actorTable = {}
        self.__timer = timer
        self.__timer.create(self.actor_ref)
        self.__timer.call(self.actor_ref, 1)
        self.time = time.time()

    def on_receive(self, msg):
        if isinstance(msg, TimeSignal):
            self.__check()

        elif isinstance(msg, AddActorMessage):
            self.__add_actor(msg)

        elif isinstance(msg, StopTimerCommand):
            self.__remove_actor(msg.actor)

    def __check(self):
        self.time = time.time()
        actors = copy.copy(list(self.actorTable.items()))
        [self.__send_start_command(algorithmRef, startTime) for algorithmRef, startTime in actors]

    def __send_start_command(self, actor_ref: pykka.ActorRef, start_time):
        if self.time >= start_time:
            self.actorTable[actor_ref] = 2 * self.time

            try:
                actor_ref.tell(TimeSignal())

            except pykka.ActorDeadError:
                self.__delete_actor(actor_ref)

            except Exception as e:
                self.__delete_actor(actor_ref)

    def __add_actor(self, msg: AddActorMessage):
        self.actorTable[msg.actor] = msg.startTime

    def __remove_actor(self, actor_ref: pykka.ActorRef):
        self.__delete_actor(actor_ref)

    def __delete_actor(self, actor_ref: pykka.ActorRef):
        try:
            del self.actorTable[actor_ref]

        except Exception as e:
            pass
