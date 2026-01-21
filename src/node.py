import datetime
from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, name, owner=None):
        self.name = name
        self.owner = owner
        self.created_at = datetime.datetime.now()
        self.modified_at = self.created_at
        self._parent = None
    
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value
    
    def rename(self, new_name):
        self.name = new_name
        self._update_modified_at()
    
    def _update_modified_at(self):
        self.modified_at = datetime.datetime.now()
        # Обновляем modified_at у родительской директории
        if self.parent:
            self.parent._update_modified_at()
    
    @abstractmethod
    def size(self):
        pass
    
    @abstractmethod
    def list_paths(self, prefix=""):
        pass
    
    @abstractmethod
    def tree(self, indent=0):
        pass
    
    @abstractmethod
    def to_dict(self):
        pass
    
    def is_file(self):
        return False
    
    def is_directory(self):
        return False