from .ChooseMenu import BaseScene
import math
import abc

PREV = '<- prev page'
NEXT = '-> next page'
BACK = 'back'
ITEMS_PER_PAGE = 25

PROMPT = [{
    'type': 'list',
    'name': 'action',
    'message': 'Navigation',
    'choices': [NEXT, PREV, BACK]
}]


class BaseViewerScreen(BaseScene):
    def __init__(self, items_per_page=ITEMS_PER_PAGE):
        super().__init__()
        self.items_per_page = items_per_page
        self.cursor = 0

    def load(self):
        items = self.fetch(self.cursor, self.cursor + ITEMS_PER_PAGE)
        if not len(items):
            return []
        else:
            return items

    @abc.abstractmethod
    def fetch(self, start, end):
        pass

    @abc.abstractmethod
    def items_count(self):
        pass

    def next_page(self):
        self.cursor += ITEMS_PER_PAGE
        if self.cursor > self.items_count():
            self.cursor = 0

    def prev_page(self):
        self.cursor -= ITEMS_PER_PAGE
        if self.cursor < 0:
            self.cursor = 0

    def render(self):
        actions = {
            NEXT: self.prev_page,
            PREV: self.next_page,
        }
        while True:
            self.clear()
            print('Page: %i' % math.ceil(self.cursor // ITEMS_PER_PAGE))
            print('Total: %i' % self.items_count())
            print('\n'.join(self.load()))
            answers = self.ask(PROMPT)
            if answers['action'] in actions:
                actions[answers['action']]()
            else:
                return
