import os


class File:
    def __init__(self, path=None, name=None, size=None, id=None, blocks=None):
        self.id = id
        self.name = name
        self.size = size
        self.path = path
        self.blocks = blocks or list()

    @classmethod
    def from_path(cls, path):
        file_stat = os.stat(path)

        return cls(path=path, name=os.path.basename(path), size=file_stat.st_size)

    @classmethod
    def from_json(cls, obj):
        return cls(
            id=obj.get("id"),
            name=obj.get("name"),
            size=int(obj.get("size")),
            blocks=obj.get("blocks", list()),
        )

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def open(self, mode="rb"):
        self.mode = mode
        self.fd = open(self.path, mode)

    def close(self):
        self.fd.close()

    def write(self, block):
        if not self.mode.startswith("w"):
            raise Exception("Can't write to a read only file.")
        self.fd.write(block.content)

    def read(self, buffer_size):
        content = self.fd.read(buffer_size)
        if not content:
            return None
        self.blocks.append(Block(file_id=self.id, content=content))
        return self.blocks[-1]


class Block:
    def __init__(self, file_id, content=None, datanode_id=None, id=None):
        self.id = id
        self.file_id = file_id
        self.content = content
        self.datanode_id = datanode_id

    @classmethod
    def from_json(cls, obj):
        return cls(
            id=obj.get("id"),
            file_id=obj.get("file_id"),
            datanode_id=obj["datanode"]["id"],
        )

    def __len__(self):
        return len(self.content)

    def load_from(self, node):
        self.content = node.get(self.id)
