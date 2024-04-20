import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv("utils/config/.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CUSTOM_SEARCH_ENGINE_ID = os.getenv("CUSTOM_SEARCH_ENGINE_ID")


class GoogleClient:
    def getSearchResponse(self, keyword):
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        start_index = 1
        response = (
            service.cse()
            .list(
                q=keyword,
                cx=CUSTOM_SEARCH_ENGINE_ID,
                lr="lang_ja",
                num=10,
                start=start_index,
            )
            .execute()
        )
        return [item["link"] for item in response["items"]]
