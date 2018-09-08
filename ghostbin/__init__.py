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

        # printing info of the same
        print("Paste URL : {}".format(r.url))

        if data["title"] != "":
            print("Paste Title : {}".format(data["title"]))

        if data["expire"] != "-1":
            print("Expiry : {}".format(self.end[data["expire"]]))

        if data["password"] != "":
            print("Password : {}".format(data["password"]))

        print("Syntax Detected : {}".format(self.getLang(data["lang"])))

        pass

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


def main():
    # registring arguments
    parser = ArgumentParser(
        description='Ghost-Lord is the cli version of web based pasting service "GHOSTBIN <https://ghostbin.com>". This program allows you to send and recieve your data from ghostbin with the help of terminal.',
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument(
        "--put", default="", metavar="TEXT/FILE", help="text/file to be pasted"
    )

    parser.add_argument(
        "--lang",
        default="text",
        metavar="LANGUAGE_TYPE",
        help="sets the file language syntax. default : text\nset it to 'auto' if you want to get the language automatically. {need file with extension}\n",
    )

    parser.add_argument(
        "--get", default="", metavar="LINK_OR_ID", help="get the content of paste\n"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="",
        metavar="FILE_NAME",
        help="saves the content of get paste into file\n",
    )

    parser.add_argument(
        "-p",
        "--password",
        default="",
        help="encrypts the paste with password\n",
        metavar="PASSWORD",
    )

    parser.add_argument("-t", "--title", default="", help="sets the paste title\n")

    parser.add_argument(
        "-e",
        "--expire",
        default="-1",
        help="sets the paste expiry. default = -1 (forever)\nTen Minutes : 10m\nAn Hour : 1h\nA Day : 1d\nA Fortnite : 14d",
    )

    # parsing arguments
    args = parser.parse_args()

    # instancing GhostBin
    gbin = GhostBin()

    # if user wants to get the paste
    if args.get != "":
        url = "https://ghostbin.com/paste/"
        recv = args.get.lower()

        # checking if user input complete url with / in end
        if url in recv and recv.endswith("/"):
            gbin.getPaste(recv + "raw", args.output, args.password)
        # checking if user input complete url without / in end
        elif url in recv and not recv.endswith("/"):
            gbin.getPaste(recv + "/raw", args.output, args.password)
        # checking if user input only paste id
        elif url not in recv:
            gbin.getPaste(url + recv + "/raw", args.output, args.password)
        exit(0)  # safe exit

    # validating inputs
    if args.put == "":
        parser.parse_args(["-h"])
    data = {}
    file = ""
    # getting data
    try:
        data["text"] = open(args.put, "r").read()
        file = args.put
    except FileNotFoundError:
        data["text"] = args.put

    # building post data
    data["title"] = args.title
    data["expire"] = args.expire
    if args.lang == "auto":
        data["lang"] = gbin.parseLang(file)
    else:
        data["lang"] = args.lang
    data["password"] = args.password

    # posting data on ghostbin
    gbin.postPaste(data)
