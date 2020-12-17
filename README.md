# GhostLord

> The project is not maintained

Ghost-Lord is the cli version of web based pasting service [GHOSTBIN](https://ghostbin.com). This
program allows you to put and recieve pastes from ghostbin with the help of terminal.

![image](https://user-images.githubusercontent.com/28386721/45248620-f5e49300-b330-11e8-86fd-ec9f6676fa86.png)


# Features
+ Post pastes directly from your local storage
+ Get pastes and save directly to your local storage
+ Encrypt pastes while posting
+ Set expiry limit while posting
+ Automatic language detection (based on file extension)

# Dependencies
+ [Python 3.x](https://python.org)
+ [NodeJS](http://nodejs.org)

# Requirements
+ cfscrape
+ argparse
+ randua

Note: The recommended way of installing requirements is using pip
```
$ pip install -r requirements.txt
```
_if you get any type of **permission denied error**, use `--user` flag in above_

# How to use
### Posting the data
+ putting a paste
    ```
    $ python bin.py --put [TEXT/FILE NAME]
    ```

+ putting a paste with `auto` language detection
    ```
    $ python bin.py --put [TEXT/FILE NAME] --lang auto
    ```

### Getting the data

+ getting a paste
    ```
    $ python bin.py --get [PASTE ID/PASTE URL]
    ```

+ getting a paste and saving
    ```
    $ python bin.py --get [PASTE ID/PASTE URL] -o [FILENAME]
    ```

Not: For more details see the [help](#help).

# Help
```
usage: bin.py [-h] [--put TEXT/FILE] [--lang LANGUAGE_TYPE] [--get LINK_OR_ID]
              [-o FILE_NAME] [-p PASSWORD] [-t TITLE] [-e EXPIRE]

Ghost-Lord is the cli version of web based pasting service "GHOSTBIN <https://ghostbin.com>". This program allows you to send and recieve your data from ghostbin with the help of terminal.

optional arguments:
  -h, --help            show this help message and exit
  --put TEXT/FILE       text/file to be pasted
  --lang LANGUAGE_TYPE  sets the file language syntax. default : text
                        set it to 'auto' if you want to get the language automatically. {need file with extension}
  --get LINK_OR_ID      get the content of paste
  -o FILE_NAME, --output FILE_NAME
                        saves the content of get paste into file
  -p PASSWORD, --password PASSWORD
                        encrypts the paste with password
  -t TITLE, --title TITLE
                        sets the paste title
  -e EXPIRE, --expire EXPIRE
                        sets the paste expiry. default = -1 (forever)
                        Ten Minutes : 10m
                        An Hour : 1h
                        A Day : 1d
                        A Fortnite : 14d

```

# Using the API
_only for developers_
### How to import
1. include the `ghostbin` folder in your project workspace
2. Use the `GhostBin` class
    ```python
    from ghostbin import GhostBin

    ghost = GhostBin()
    ```

and use

### Api Documentation
_the following are the method of `GhostBin` class_

|Method|Arguments|Description|
|---|---|---|
|parseLang|`nil`|Method to return the syntax id (lang parameter of ghostbin) for the file name|
|getLang|`nil`|Method to get the syntax name by its id|
|getPaste|`url`: Complete URL / Paste ID (required) <br> `output`: Output filename (optional) <br> `password`: Unlock password for protected pastes (optional) |Method to get the content of paste by its ID / URL. I will take password argument while dealing with password protected pastes. Use output paramater if you want to save the contents instead of printing|
|postPaste|`data`: dictionary with [post](#post-data-keys) keys <br>**all keys are mandtory**|Method to post new paste and return the details|
#### Post data keys
|Key|Values|Default Value|Description|
|---|---|---|---|
|text|`any`|`nil` (its mandatory)|contents to be pasted online|
|lang|from `ghostbin/languages.json`|`text`|syntax of paste|
|expiry| Ten Minutes : 10m <br> An Hour : 1h <br> A Day : 1d <br>A Fortnite : 14d |`-1`|expiry/auto delete period|
|password|`any`|_empty string_|encryption password to lock paste|
|title|`any`|_empty string_|title of paste|
# Licence
MIT

# Contribution
If you want to fix any bug or improve feature, feel free to open a pull request for the same
