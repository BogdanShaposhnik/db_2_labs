import abc

YES = 'yes'
NO = 'no'


class BaseScene:
    def __init__(self):
        self.clear()

    @staticmethod
    def clear():
        print('\x1bc')

    def __del__(self):
        self.clear()

    @staticmethod
    def ask_accept(question, answers):
        choices = [YES, NO]
        while True:
            print(question['message'])
            i = 1
            for choice in choices:
                print('%i) %s' % (i, choice))
                i += 1
            tmp_input = input()
            choice_id = None
            try:
                choice_id = int(tmp_input)
            except ValueError:
                print('Please, enter a id of choice')
                continue
            if choice_id < 1 or choice_id > len(choices):
                print('Number of choice is out of bounds')
                continue
            answers[question['name']] = choices[choice_id - 1] == YES
            break

    @staticmethod
    def ask_list(question, answers):
        choices = question['choices']
        while True:
            print(question['message'])
            i = 1
            for choice in choices:
                print('%i) %s' % (i, choice))
                i += 1
            tmp_input = input()
            choice_id = None
            try:
                choice_id = int(tmp_input)
            except ValueError:
                print('Please, enter a id of choice')
                continue
            if choice_id < 1 or choice_id > len(choices):
                print('Number of choice is out of bounds')
                continue
            answers[question['name']] = choices[choice_id - 1]
            break

    @staticmethod
    def ask_input(question, answers):
        while True:
            print(question['message'])
            tmp_input = input()
            if 'validate' in question:
                err = question['validate'](tmp_input)
                if err:
                    print(err)
                    continue
            if not len(tmp_input):
                if 'default' in question:
                    tmp_input = question['default']()
                else:
                    tmp_input = ''
            answers[question['name']] = tmp_input
            break

    def ask(self, questions=None):
        answers = {}
        for question in questions:
            qtype = question['type']
            if 'condition' in question and not question['condition'](answers):
                continue
            if qtype == 'input':
                self.ask_input(question, answers)
            elif qtype == 'list':
                self.ask_list(question, answers)
            elif qtype == 'accept':
                self.ask_accept(question, answers)
        return answers

    @abc.abstractmethod
    def render(self):
        pass
