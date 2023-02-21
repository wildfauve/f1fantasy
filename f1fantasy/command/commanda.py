from f1fantasy import model

from . import helpers


class CommandRunner:
    def __init__(self):
        self.commands = []
        self.results = None

    def cmd(self, fn, *args, **kwargs):
        self.commands.append((fn, args, kwargs))
        return self

    def run(self):
        self.results = [fn(*args, **{**kwargs, **self.opts()}) for fn, args, kwargs in self.commands]
        helpers.save()
        return self

    def opts(self):
        return {"opts": {"in_runner": True}}

def runner():
    return CommandRunner()


def command():
    def inner(fn):
        def try_it(*args, **kwargs):
            result = fn(*args, **kwargs)
            opts = kwargs.get('opts', dict())
            if result and result == model.Result.OK and not opts.get('in_runner', None):
                helpers.save()
            return result

        return try_it

    return inner
