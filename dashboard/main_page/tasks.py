
from .models import Comics

from bs4 import BeautifulSoup
import requests


def get_comics():

    d = {
        "Dilbert": {
            "url": "http://dilbert.com/",
            "tag": "a",
            "image": {"class": "img-comic-link"}},
        "Rhymes with Orange": {
            "url": "http://rhymeswithorange.com/",
            "tag": "div",
            "image": {"id": "comicpanel"}},
        "Savage Chickens": {
            "url": "http://www.savagechickens.com/",
            "tag": "div",
            "image": {"class": "entry_content"},
            "title": "alt"},
        "xkcd": {
            "url": "https://www.xkcd.com/",
            "tag": "div",
            "image": {"id": "comic"},
            "alt": "title",
            "title": "alt"},
        "Owl Turd Comics": {
            "url": "http://owlturdcomix.tumblr.com/",
            "tag": "div",
            "image": {"class": "post post-photo"}},
        "SMBC": {
            "url": "http://www.smbc-comics.com/",
            "tag": "div",
            "image": {"id": "cc-comicbody"},
            "alt": "title"},
        "Commit Strip": {
            "nav_page": {
                "url": "http://www.commitstrip.com/en/",
                "tag": "div",
                "redirect": {"class": "excerpt"}},
            "tag": "div",
            "image": {"class": "entry-content"}},
        "The Pigeon Gazette": {
            "url": "http://www.gocomics.com/the-pigeon-gazette",
            "tag": "picture",
            "image": {"class": "img-fluid item-comic-image"}},
        "Wizard of Id": {
            "url": "http://www.gocomics.com/wizardofid",
            "tag": "picture",
            "image": {"class": "img-fluid item-comic-image"}}
    }

    spoof = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 " \
            "(KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"

    headers = {"User-Agent": spoof, "referer": "{}"}

    for comic, data in d.items():
        title = comic
        alt = ''
        if data.get("nav_page"):
            r = requests.get(data["nav_page"]["url"], headers={"User-Agent": spoof, "referer": data["nav_page"]["url"]})
            soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')
            new_url = soup.find(data["nav_page"]["tag"], data["nav_page"]["redirect"]).a["href"]
            r = requests.get(new_url, headers={"User-Agent": spoof, "referer": new_url})

        else:
            r = requests.get(data["url"], headers=headers)

        soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')
        image = soup.find(data["tag"], data["image"]).img['src']
        link = "{}{}".format("https:" if not image.startswith("http") else "", image)
        if data.get("alt"):
            alt = soup.find(data["tag"], data["image"]).img[data["alt"]]
        if data.get("title"):
            t = soup.find(data["tag"], data["image"]).img[data["title"]]
            if t:
                title = "{} - {}".format(comic, t)
        results = Comics.objects.filter(image_link=link)

        if len(results) is 0:
            row = Comics(image_link=link, comic_title=title, alt_text=alt)
            row.save()
