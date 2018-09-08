from ghostbin import GhostBin
from argparse import ArgumentParser, RawTextHelpFormatter

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
rdata = gbin.postPaste(data)

print("Paste URL : {}".format(rdata["url"]))

if rdata["title"] != "":
    print("Paste Title : {}".format(rdata["title"]))

if rdata["expire"] != "":
    print("Expiry : {}".format(rdata["expire"]))

if data["password"] != "":
    print("Password : {}".format(rdata["password"]))

print("Syntax Detected : {}".format(rdata["syntax"]))
