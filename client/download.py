class FileDownloader:
    def __init__(self, metadata, progress_hook, logger):
        self.logger = logger
        self.metadata = metadata
        self.progress_hook = progress_hook

    def download(self, file_id, save_location):
        if not (file := self.get_file(file_id)):
            raise FileNotFoundError(f"File with id {file_id} not found.")
        file.path = save_location
        self.check_node_health()
        self.write_to_disk(file)

    def get_file(self, file_id):
        try:
            return self.metadata.get_file(file_id, include_blocks=True)
        except self.metadata.exception_class:
            raise Exception("Failed to connect to metadata server.")

    def check_node_health(self):
        nodes = self.metadata.datanodes.values()
        if not (inactive := [node for node in nodes if not node.is_active()]):
            return
        self.logger.warning("The following nodes are not active:")
        for index, node in enumerate(inactive, start=1):
            self.logger.warning(f"{index}. {node.host}:{node.port}")
        raise Exception("Unable to download the file. Make sure all nodes are active")

    def write_to_disk(self, file):
        self.progress_hook.initialize("Downloading", file.size)
        file.open("wb")
        for block in file.blocks[::-1]:
            self.add_block_to_file(file, block)
            self.progress_hook.update(len(block))
        file.close()
        self.progress_hook.dispose()

    def add_block_to_file(self, file, block):
        node = self.metadata.datanodes[block.datanode_id]
        self.load_block(block, node)
        file.write(block)

    def load_block(self, block, node):
        try:
            block.load_from(node)
        except node.exception_class as e:
            self.progress_hook.dispose()
            raise ConnectionError(
                f"Failed to connect to node server at address '{node.host}:{node.port}'."
            )
