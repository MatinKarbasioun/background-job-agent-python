from typing import NamedTuple
import pykka


class AddActorMessage(NamedTuple):
    actor: pykka.ActorRef
    startTime: float
