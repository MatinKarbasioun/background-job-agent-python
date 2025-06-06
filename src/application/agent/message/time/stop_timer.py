from dataclasses import dataclass
import pykka


@dataclass(frozen=True)
class StopTimerCommand:
    actor: pykka.ActorRef

