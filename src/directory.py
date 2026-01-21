from node import Node
import datetime

class Directory(Node):
    def __init__(self, name, owner=None):
        super().__init__(name, owner)
        self.children = {}
    
    def is_directory(self):
        return True
    
    def add(self, node):
        if node.name in self.children:
            raise ValueError(f"Node with name '{node.name}' already exists")
        
        self.children[node.name] = node
        node.parent = self
        self._update_modified_at()
    
    def remove(self, name):
        if name in self.children:
            self.children[name].parent = None
            del self.children[name]
            self._update_modified_at()
            return True
        return False
    
    def get(self, name):
        return self.children.get(name)
    
    def size(self):
        total = 0
        for child in self.children.values():
            total += child.size()
        return total
    
    def list_paths(self, prefix=""):
        paths = []
        current_path = f"{prefix}/{self.name}" if prefix else self.name
        
        for child in self.children.values():
            child_paths = child.list_paths(current_path)
            paths.extend(child_paths)
        
        return paths
    
    def tree(self, indent=0):
        indent_str = " " * indent
        result = f"{indent_str}{self.name}/ (size: {self.size()} bytes)\n"
        
        # Сортируем детей: сначала директории, потом файлы
        sorted_children = sorted(
            self.children.values(),
            key=lambda x: (not x.is_directory(), x.name.lower())
        )
        
        for child in sorted_children:
            result += child.tree(indent + 2) + "\n"
        
        return result.rstrip()
    
    def to_dict(self):
        children_dict = {}
        for name, child in self.children.items():
            children_dict[name] = child.to_dict()
        
        return {
            "type": "directory",
            "name": self.name,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "size": self.size(),
            "children_count": len(self.children),
            "children": children_dict
        }