import requests
import logging
import os
import urls
import shutil


logger = logging.getLogger(__name__)

class DataDownloader:
    def __init__(self, save_path: str):
        self.save_path = save_path

    logger.info("Inicando pipeline de download dos dados.")

    # coloquei esse metodo estatico para facilitar buscar as urls no arquivo urls.py, para facilitar a manutenção.
    @staticmethod
    def get_urls():
        yield from urls.data["urls"]

    def download_all(self) -> None:
        os.makedirs(self.save_path, exist_ok=True)

        for year, url in enumerate(self.get_urls(), start=2015):
            logger.info("Iniciando download de %s", year)

            try:
                response = requests.get(url, timeout=30, stream=True)
                response.raise_for_status()

                filename = f"dados_boston_{year}.csv"
                full_path = os.path.join(self.save_path, filename)

                save_archive = SaveArchive(full_path)

                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        save_archive.append(chunk)

                logger.info("Arquivo %s salvo com sucesso.", filename)

            except requests.RequestException as e:
                logger.error("Erro ao baixar %s: %s", url, e)


class SaveArchive:
    def __init__(self, save_path: str):
        self.save_path = save_path

    def append(self, data: bytes) -> None:
        with open(self.save_path, "ab") as file:
            file.write(data)


class CompactArchive:
    def __init__(self, path: str, filename: str):
        self.path = path
        self.filename = filename

    logger.info("Iniciando compactação dos arquivos baixados.")
    
    def create_zip(self) -> None:
        base_name = os.path.join(self.path, self.filename.replace(".zip", ""))
        try:
            shutil.make_archive(base_name, 'zip', self.path)
            logger.info("Arquivo %s criado com sucesso.", self.filename)
        except Exception as e:
            logger.error("Erro ao criar arquivo zip: %s", e)


# Fim da pipeline
logger.info("Pipeline de download e compactação dos dados concluído.")