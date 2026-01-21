from node import Node
import datetime

class File(Node):
    def __init__(self, name, content="", owner=None):
        super().__init__(name, owner)
        self.content = content
        self.tags = []
    
    def is_file(self):
        return True
    
    def size(self):
        return len(self.content.encode('utf-8'))
    
    def modify(self, new_content):
        self.content = new_content
        self._update_modified_at()
    
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
            self._update_modified_at()
    
    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
            self._update_modified_at()
    
    def list_paths(self, prefix=""):
        full_path = f"{prefix}/{self.name}" if prefix else self.name
        return [full_path]
    
    def tree(self, indent=0):
        indent_str = " " * indent
        return f"{indent_str}{self.name} ({self.size()} bytes)"
    
    def to_dict(self):
        return {
            "type": "file",
            "name": self.name,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "size": self.size(),
            "tags": self.tags,
            "content_length": len(self.content)
        }