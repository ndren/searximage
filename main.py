import requests
import json
import re

def query(searx_instance, query, format):
    full_url = searx_instance + "?q=!images " + query + "&format=" + format
    return requests.get(full_url).text

def get_urls(searx_instance, query):
    urls = []
    # Currently, URLs from flickr are returned in the form //example.com (see issue tracker: https://github.com/searx/searx/issues/3092)
    broken_url_format = re.compile(r"^//")
    response = json.loads(query(searx_instance, query, "json"))
    for result in response["results"]:
        url = result["img_src"]
        if not url:
            continue
        if broken_url_format.search(url):
            url = "https" + url
        urls.append(url)
    return urls
for url in get_urls("https://INSERT_SEARX.INSTANCE", "INSERT_QUERY"):
    print(url)
# The list of URLs can then be used to quickly download them:
# `python main.py | xargs -P4 curl -O` to run 4 processes in parallel.
