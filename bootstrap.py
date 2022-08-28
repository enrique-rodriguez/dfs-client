import logging
from client.dfs import Dfs
from app import Application
from client.list import FileLister
from client.metadata import MetaData
from client.delete import FileDeleter
from client.upload import FileUploader
from client.download import FileDownloader
from client.utils.progress_bar import TqdmProgressBar


def get_dfs(metadata, progress_bar, logger, config):
    bsize = config.get("block_size", 4096)

    lister = FileLister(metadata, logger)
    deleter = FileDeleter(metadata, progress_bar, logger)
    downloader = FileDownloader(metadata, progress_bar, logger)
    uploader = FileUploader(metadata, progress_bar, logger, block_size=bsize)

    return Dfs(
        lister=lister,
        deleter=deleter,
        uploader=uploader,
        downloader=downloader,
    )


def bootstrap(config):
    meta_host = config.get("meta_host")
    meta_port = config.get("meta_port")

    metadata = MetaData(meta_host, meta_port)
    logger = logging.getLogger(__name__)

    progress_bar = TqdmProgressBar()
    dfs = get_dfs(metadata, progress_bar, logger, config)

    return Application(dfs)
