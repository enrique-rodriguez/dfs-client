import abc
import tqdm


class ProgressBar(abc.ABC):
    @abc.abstractmethod
    def initialize(self, desc, file_size):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, amount):
        raise NotImplementedError

    @abc.abstractmethod
    def dispose(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on_error(self, error):
        raise NotImplementedError


class TqdmProgressBar(ProgressBar):
    def __init__(self):
        self.pbar = None

    def initialize(self, desc, total):
        self.pbar = tqdm.tqdm(total=total, unit=" bytes", desc=desc)

    def update(self, amount):
        self.pbar.update(amount)

    def dispose(self):
        self.pbar.close()

    def on_error(self, error):
        self.pbar.close()

    def set_description(self, desc):
        self.desc = desc
        if self.pbar:
            self.pbar.set_description(self.desc)
