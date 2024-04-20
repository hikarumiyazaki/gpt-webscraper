import re
import sys

import requests

from utils import prompts
from utils.google_client import GoogleClient
from utils.gpt_client import GptClient


def generate_search_word(message):
    prmpt = prompts.GET_KEYWORD_AND_QUESTIONS.format(message=message)
    result_json = GptClient().request_json(prmpt)

    try:
        return (
            result_json["keyword"],
            result_json["response"],
            result_json["is_answered"],
        )
    except KeyError:
        return None, None, False


def google_search(search_word):
    result = GoogleClient().getSearchResponse(search_word)
    return result


def format_html(html_source):
    try:
        html_source = re.sub(r"<head.*?>.*?</head>", "", html_source, flags=re.DOTALL)
        html_source = re.sub(r"<ins.*?>.*?</ins>", "", html_source, flags=re.DOTALL)
        html_source = re.sub(
            r"<iframe.*?>.*?</iframe>", "", html_source, flags=re.DOTALL
        )
        html_source = re.sub(
            r"<script.*?>.*?</script>", "", html_source, flags=re.DOTALL
        )
        html_source = re.sub(r"<style.*?>.*?</style>", "", html_source, flags=re.DOTALL)
        html_source = re.sub(
            r"<header.*?>.*?</header>", "", html_source, flags=re.DOTALL
        )
        html_source = re.sub(
            r"<footer.*?>.*?</footer>", "", html_source, flags=re.DOTALL
        )
        html_source = re.sub(
            r"<noscript.*?>.*?</noscript>", "", html_source, flags=re.DOTALL
        )
        # 改行コードを削除
        html_source = re.sub(r"\n", "/", html_source)
        html_source = re.sub(r"\r", "/", html_source)
        html_source = re.sub(r"\t", "/", html_source)
        html_source = re.sub(r"\s{2,}", "/", html_source)
        html_source = re.sub(r"<[^>]+>", "/", html_source)
        html_source = re.sub(r"/{2,}", "/", html_source)

        return html_source
    except Exception as e:
        print(e)
        raise


def ask_gpt(request, html_source):
    prmpt = prompts.GET_ANSWER.format(request=request, html_source=html_source)
    result_json = GptClient().request_json(prmpt)

    try:
        return (
            result_json["response"],
            result_json["is_answered"],
        )
    except KeyError:
        return None, False


def process_request(text):
    keyword, response, is_answered = generate_search_word(text)
    if is_answered:
        return response
    links = google_search(keyword)
    for link in links:
        response = requests.get(link)
        response.encoding = response.apparent_encoding
        html_source = response.text
        formatted_html = format_html(html_source)
        response, is_answered = ask_gpt(text, formatted_html)
        if is_answered:
            return response


if __name__ == "__main__":
    request = sys.argv[1]
    print(process_request(request))
