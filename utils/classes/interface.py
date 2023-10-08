from abc import ABCMeta, abstractmethod

class StreamlitPage(metaclass=ABCMeta):
    def render(self):
        self.setup_page()
        self.input_handling()

    @abstractmethod
    def setup_page(self):
        pass

    @abstractmethod
    def input_handling(self):
        pass