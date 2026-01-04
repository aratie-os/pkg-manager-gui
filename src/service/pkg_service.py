from abc import ABC, abstractmethod


class PkgService(ABC):

    @abstractmethod
    def install(self, url: str) -> None:
        pass

    @abstractmethod
    def extract_name(self, base_name: str) -> str:
        pass
    
    @abstractmethod
    def is_installed(self,  base_name: str) -> str:
        pass
    
    @abstractmethod
    def uninstall(self, base_name: str) -> None:
        pass
