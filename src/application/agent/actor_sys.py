from pykka import ActorRef

from src.application.agent.task_distributor import TaskDistributor


class ActorSystem:
    manager: ActorRef = None

    def __init__(self):
        ActorSystem.manager = TaskDistributor.start()