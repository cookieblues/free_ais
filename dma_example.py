import io
import os
import requests
import zipfile

from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv

load_dotenv()


def is_zip_file(link: Tag) -> bool:
    return link.attrs["href"].endswith(".zip")


URL = "http://web.ais.dk/aisdata/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

links = soup.find_all("a", href=True)
zip_links = [link for link in links if is_zip_file(link)]

for zip_link in zip_links[-10:]:
    print(zip_link)
    download_link = URL + zip_link.attrs["href"]
    res = requests.get(download_link)
    zip = zipfile.ZipFile(io.BytesIO(res.content))
    zip.extractall(os.environ["storage_directory"])
