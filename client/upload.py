from client.file import File
from client.utils import CyclicList


class FileUploader:
    def __init__(self, metadata, progress_hook, logger, block_size=4096):
        self.logger = logger
        self.metadata = metadata
        self.block_size = block_size
        self.progress_hook = progress_hook

    def upload(self, path):
        file = File.from_path(path)
        nodes = self.add_file(file)
        self.progress_hook.initialize("Uploading", file.size + 1)
        self.send_file(file, nodes)
        self.metadata.add_blocks_for(file)
        self.progress_hook.update(1)
        self.progress_hook.dispose()

    def add_file(self, file):
        self.metadata.add_file(file)
        nodelist = self.metadata.list_nodes()
        if len(nodelist) == 0:
            raise Exception("No active nodes available to upload file.")
        return iter(CyclicList(nodelist))

    def send_file(self, file, nodes):
        file.open()
        while blk := file.read(self.block_size):
            self.put_block(blk, nodes)
        file.close()

    def put_block(self, block, nodes):
        # TODO: FIX: If all nodes become inactive, this will create an infinite loop.
        node = next(nodes)
        try:
            node.put(block)
        except node.exception_class:
            """Just skip over this node"""
            return self.put_block(block, nodes)
        self.on_block_sent(len(block))

    def on_block_sent(self, amount):
        self.progress_hook.update(amount)
