import abc


class Command(metaclass=abc.ABCMeta):
    name: str
    aliases: [str]

    def __init__(self):
        self.name = ''
        self.aliases = []

    def run(self, event, args: [str]):
        return
