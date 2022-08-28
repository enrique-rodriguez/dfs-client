class Dfs:
    def __init__(self, downloader, uploader, lister, deleter):
        self.lister = lister
        self.deleter = deleter
        self.uploader = uploader
        self.downloader = downloader

    def list(self):
        return self.lister.list()

    def download(self, file_id, save_location):
        return self.downloader.download(file_id, save_location)

    def upload(self, path):
        return self.uploader.upload(path)

    def delete(self, file_id):
        return self.deleter.delete(file_id)