from dotenv import load_dotenv
import os
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv()

logger = logging.getLogger(__name__)

#pegando o env por aqui por que dentro do metodo estava dando erro
KEY_AZURE = os.getenv("AZURE_STORAGE_ACCESS_KEY")


class ConnectAzureBlobStorage:

    def __init__(self, account_url: str):
        self.account_url = account_url

    def get_blob_service_client_account_key(self):
        shared_access_key = KEY_AZURE
        if shared_access_key:
            logger.info("Conectando ao Azure Blob Storage usando chave de acesso da conta.")
            credential = shared_access_key
        else:
            logger.info(
                "AZURE_STORAGE_ACCESS_KEY não encontrado, usando DefaultAzureCredential. "
                "Certifique-se de ter feito 'az login' ou definido uma identidade gerenciada."
            )
            credential = DefaultAzureCredential()

        try:
            client = BlobServiceClient(self.account_url, credential=credential)
            logger.info("Conexão ao Azure Blob Storage estabelecida com sucesso.")
            return client
        except Exception as e:
            logger.error("Erro ao conectar ao Azure Blob Storage: %s", e)
            return None
    
class UploadBlobFile:
    def __init__(self, blob_service_client: BlobServiceClient, container_name: str, blob_name: str, file_path: str, file_name: str):
        self.blob_service_client = blob_service_client
        self.container_name = container_name
        self.blob_name = blob_name
        self.file_path = file_path
        self.file_name = file_name

    def upload(self) -> None:

        logger.info("Iniciando upload do arquivo para o Azure Blob Storage.")

        try:
            # Create a BlobClient
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=self.blob_name)


            with open(self.file_path, "rb") as data:
                blob_client.upload_blob(
                    data=data,
                    overwrite=True,
                )

            logger.info("Upload do arquivo %s para o Azure Blob Storage concluído com sucesso.", self.file_name)

        except Exception as e:
            logger.error("Erro ao fazer upload do arquivo para o Azure Blob Storage: %s", e)



#testar manual kkkk

if __name__ == "__main__":
    # configuração básica de logging para ver o que acontece
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    connectAzure = ConnectAzureBlobStorage(account_url="https://dadosbostonmurilo.blob.core.windows.net")
    blob_service_client = connectAzure.get_blob_service_client_account_key()
    if blob_service_client is not None:
        uploader = UploadBlobFile(blob_service_client=blob_service_client, 
                                    container_name="servicosbostonzip",
                                    blob_name="boston_data.zip",
                                    file_path="data/dados_boston_2015.csv",
                                    file_name="boston_data.csv")
        uploader.upload()
