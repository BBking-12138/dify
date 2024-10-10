from abc import ABC, abstractmethod

from flask import Flask


class BasicAssembly(ABC):
    @abstractmethod
    def prepare_app(self, app: Flask):
        raise NotImplementedError
