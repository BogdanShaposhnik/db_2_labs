from abc import ABC

from chat.Neo4j import GraphDB
from .BaseScreen import BaseScene

TAGS = 'Find Tags'
WAY_BETWEEN_NODES = 'Nodes in certain radius'
PATH = 'Shortest way between nodes'
SPAM = 'Spam Authors'
BLOCKED_TAGS = 'Blocked tags'
EXIT = 'exit'

PROMPT = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            TAGS,
            WAY_BETWEEN_NODES,
            PATH,
            SPAM,
            BLOCKED_TAGS,
            EXIT
        ]
    }
]


class Neo4jScreen(BaseScene):

    def __init__(self, state):
        super().__init__()
        self.db = GraphDB()
        self.thread = None

    def search_tags(self, args):
        self.db.find_by_tag()
        input()

    def nodes_in_radius(self, args):
        count = input("Input radius:  ")
        self.db.nodes_in_radius(count)

    def search_spam(self, args):
        self.db.find_by_spam()
        input()

    def shortest_way(self, args):
        name1 = input("Input first name:  ")
        name2 = input("Input second name:  ")
        self.db.find_shortest_way(name1, name2)
        input()

    def find_blocked_tags(self, args):
        self.db.blocked_tag_messages()
        input()

    def render(self):
        actions = {
            TAGS: self.search_tags,
            PATH: self.shortest_way,
            WAY_BETWEEN_NODES: self.nodes_in_radius,
            SPAM: self.search_spam,
            BLOCKED_TAGS: self.find_blocked_tags
        }
        while True:
            if self.thread:
                self.thread.stop()
            answers = self.ask(PROMPT)
            if answers['action'] in actions:
                actions[answers['action']](answers)
            else:
                return
