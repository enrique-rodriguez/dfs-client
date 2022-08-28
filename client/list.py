class FileLister:
    def __init__(self, metadata, logger):
        self.logger = logger
        self.metadata = metadata

    def list(self):
        return self.metadata.list_files()