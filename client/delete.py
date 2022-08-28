class FileDeleter:
    def __init__(self, metadata, progress_hook, logger):
        self.logger = logger
        self.metadata = metadata
        self.progress_hook = progress_hook
    
    def delete(self, file_id):
        if not (file := self.get_file(file_id)):
            raise FileNotFoundError(f"File with id {file_id} not found.")
    
    def get_file(self, file_id):
        try:
            return self.metadata.get_file(file_id, include_blocks=False)
        except self.metadata.exception_class:
            raise Exception("Failed to connect to metadata server.")