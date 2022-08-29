import argparse


def parse_download_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file_id")
    parser.add_argument("save_location")
    return parser.parse_args(argv)


def parse_upload_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    return parser.parse_args(argv)


def parse_delete_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file_id")
    return parser.parse_args(argv)


def parse_list_args(argv):
    parser = argparse.ArgumentParser()
    return parser.parse_args(argv)


class Application:
    def __init__(self, dfs):
        self.dfs = dfs

    def main(self, argv):
        cmd = argv.pop(0)
        if not hasattr(self, cmd):
            raise exit(f"Invalid command {cmd}.")
        self.execute(cmd, argv)

    def execute(self, cmd, argv):
        try:
            getattr(self, cmd)(argv)
        except Exception as error:
            exit(error)

    def list(self, argv):
        args = parse_list_args(argv)

        for file in self.dfs.list():
            print(file.id, file.name, file.size, '-', 'bytes')

    def download(self, argv):
        args = parse_download_args(argv)
        file_id = args.file_id
        save_loc = args.save_location

        self.dfs.download(file_id, save_loc)

    def upload(self, argv):
        args = parse_upload_args(argv)
        path = args.path

        self.dfs.upload(path)

    def delete(self, argv):
        args = parse_delete_args(argv)
        file_id = args.file_id

        self.dfs.delete(file_id)
