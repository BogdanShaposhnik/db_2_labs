from .BaseScreen import BaseScene
from .WorkerScreen import WorkerScreen
from .AutomatronScreen import AutomatronScreen
from chat.Neo4j import GraphDB
from .Neo4jScreen import Neo4jScreen

BE_WORKER = 'worker'
START_EMULATION = 'emulation'
Neo4j = 'Neo4j interface'
EXIT = 'exit'

PROMPT = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            BE_WORKER,
            START_EMULATION,
            Neo4j,
            EXIT
        ]
    }
]


class StartScreen(BaseScene):
    def __init__(self, state):
        super().__init__()
        self.redis = state['redis']
        self.state = state
        self.thread = None

    def be_worker(self, *args):
        WorkerScreen(self.state).render()

    def start_emulation(self, *args):
        AutomatronScreen(self.state).render()

    def neo4j_tasks(self, *args):
        Neo4jScreen(self.state).render()

    def render(self):
        actions = {
            BE_WORKER: self.be_worker,
            START_EMULATION: self.start_emulation,
            Neo4j: self.neo4j_tasks
        }
        while True:
            if self.thread:
                self.thread.stop()
            answers = self.ask(PROMPT)
            if answers['action'] in actions:
                actions[answers['action']](answers)
            else:
                return
