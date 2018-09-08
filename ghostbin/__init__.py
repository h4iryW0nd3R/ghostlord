from argparse import ArgumentParser, RawTextHelpFormatter, RawDescriptionHelpFormatter
from cfscrape import create_scraper
from randua import generate as genua
import json
import os
from os import path
from sys import exit
from urllib.parse import quote


class GhostBin:
    def __init__(self):

        # getting all languages
        self.language = self.__loadLang()

        # setting headers
        self.headers = {
            "User-Agent": genua(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        # creating a scraper
        self.scrape = create_scraper()

        self.end = {
            "-1": "",
            "1m": "One Minute",
            "1h": "One Hour",
            "1d": "One Day",
            "14": "One Fortnite ",
        }
        pass

    def postPaste(self, data):
        # putting data
        r = self.scrape.post(
            "https://ghostbin.com/paste/new", data=data, headers=self.headers
        )

        return {
            "url": r.url,
            "syntax": self.getLang(data["lang"]),
            "password": data["password"],
            "expire": self.end[data["expire"]],
            "title": data["title"],
        }

    def getPaste(self, url, output="", password=""):
        # getting initial response
        r = self.scrape.get(url, headers=self.headers)

        # if found authenticate in url wihout password - password protected and need password
        if r.url.endswith("authenticate") and password == "":
            print("This paste is password protected")
            exit(1)
        # if found authenticate in url with password entered
        elif r.url.endswith("authenticate") and password != "":
            # validating the paste
            pr = self.scrape.post(
                r.url, data={"password": password}, headers=self.headers
            )

            # if still it has authenticate then wrong pass
            if "authenticate" in pr.url:
                print("Wrong password")
                exit(1)
            else:
                # otherwise getting the raw content
                r = self.scrape.get(pr.url + "/raw", headers=self.headers)

                if output == "":  # if no output set then print on terminal
                    print(r.text)
                else:
                    # if output was set then save it to file
                    with open(output, "w") as file:
                        file.write(r.text)
                        file.close()
                pass
        else:
            # the same will happen if paste is public
            if output == "":
                print(r.text)
            else:
                with open(output, "w") as file:
                    file.write(r.text)
                    file.close()

    # public method to parse language from extension if --lang is auto
    def parseLang(self, file):
        # getting file extenstion
        try:
            ext = file.split(".")[1]
        except IndexError:
            return "text"  # returning lang to be "text"

        # traversing all languages
        for lang in self.language:
            if ext == lang["id"]:
                return lang["id"]  # if matched id return
            else:
                try:
                    # checking for alternate ids
                    if ext in lang["alt_ids"]:
                        return lang["id"]
                except KeyError:
                    pass

        return "text"  # fall back to text

    def getLang(self, id):
        return [x["name"] for x in self.language if x["id"] == id][0]

    # private method to load all languages
    def __loadLang(self):
        file = path.join(path.dirname(__file__), "languages.json")
        langs = json.loads(open(file, "r").read())
        return langs

    pass
