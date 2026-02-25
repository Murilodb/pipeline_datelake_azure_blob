import logging
import colorlog
from get_data import DataDownloader, CompactArchive


def configure_logging():
    handler = colorlog.StreamHandler()
    
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
    )

    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def main():
    configure_logging()
    downloader = DataDownloader(save_path="./data")
    downloader.download_all()

    compact_archive = CompactArchive(path="./data", filename="boston_data.zip")
    compact_archive.create_zip()

if __name__ == "__main__":
    main()