import requests
import logging
import os
import urls
import shutil

logger = logging.getLogger(__name__)


class DataDownloader:

    def __init__(self, save_path: str):
        self.save_path = save_path

    @staticmethod
    def get_urls():
        # coloquei esse metodo estastico só para puxar as urls mais facilmente
        yield from urls.data["urls"]

    def _save_response(self, response: requests.Response, target: str) -> None:
        with open(target, "wb") as f:
            shutil.copyfileobj(response.raw, f)

    def _fetch(self, year_url):
        year, url = year_url
        logger.info("Iniciando download de %s", year)
        try:
            r = requests.get(url, timeout=30, stream=True)
            r.raise_for_status()
            filename = f"dados_boston_{year}.csv"
            path = os.path.join(self.save_path, filename)
            self._save_response(r, path)
            logger.info("Arquivo %s salvo com sucesso.", filename)
        except requests.RequestException as e:
            logger.error("Erro ao baixar %s: %s", url, e)

    def download_all(self) -> None:
        os.makedirs(self.save_path, exist_ok=True)
        for year_url in enumerate(self.get_urls(), start=2015):
            self._fetch(year_url)


class CompactArchive:
    def __init__(self, path: str, filename: str):
        self.path = path
        self.filename = filename

    def create_zip(self) -> None:
        logger.info("Iniciando compactação dos arquivos baixados.")
        base_name = os.path.join(self.path, self.filename.replace(".zip", ""))
        try:
            shutil.make_archive(base_name, 'zip', self.path)
            logger.info("Arquivo %s criado com sucesso.", self.filename)
        except Exception as e:
            logger.error("Erro ao criar arquivo zip: %s", e)


if __name__ == "__main__":
    # configuração básica de logging para ver o que acontece
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    # downloader = DataDownloader(save_path="./data")
    # downloader.download_all()

    # compact_archive = CompactArchive(path="./data", filename="boston_data.zip")
    # compact_archive.create_zip()