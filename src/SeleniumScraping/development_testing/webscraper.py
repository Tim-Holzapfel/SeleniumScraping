import pandas as pd
import requests
from bs4 import BeautifulSoup
import html.parser
from SeleniumScraping.driver.utils import FilePaths
folder_path = FilePaths.programm_folder.joinpath("municipalities")



country_name = "chile".lower()


URL = f"https://www.citypopulation.de/en/{country_name}/admin/"


URL = "https://www.citypopulation.de/en/chile/mun/admin/"

page = requests.get(URL, verify=False)

df_list = pd.read_html(page.text)

df_main = df_list[0]

data_path = folder_path.joinpath(f"{country_name}_municipalities.feather")

df_main.to_feather(data_path)


