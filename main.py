import logging
from dotenv import load_dotenv
from get_data import DataDownloader, CompactArchive
from salve_Azureblob import ConnectAzureBlobStorage, UploadBlobFile


def configure_logging():
    logger = logging.getLogger()

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

def main():
    load_dotenv()  
    configure_logging()

    downloader = DataDownloader(save_path="./data")
    downloader.download_all()

    compact_archive = CompactArchive(path="./data", filename="boston_data.zip")
    compact_archive.create_zip()

    #coneectando ao azure e fazendo upload do arquivo zip criado
    connectAzure = ConnectAzureBlobStorage(account_url="https://dadosbostonmurilo.blob.core.windows.net")
    blob_service_client = connectAzure.get_blob_service_client_account_key()
    if blob_service_client is not None:
        uploader = UploadBlobFile(blob_service_client=blob_service_client, 
                                    container_name="servicosbostonzip",
                                    blob_name="boston_data.zip",
                                    file_path="data/boston_data.zip",
                                    file_name="boston_data.zip")
        uploader.upload()



if __name__ == "__main__":
    main()

