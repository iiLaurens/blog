Title: Scraping korean audio fragments for Anki cards
Slug: korean-audio-scraping-for-anki
Date: 2016-05-22 12:44
Tags: Anki, korean, audio, scraper, python
Author: Laurens

Besides programming, I am also quite fond of the Korean language. One of the apps I
use to study korean is [Anki](www.ankisrs.net). Anki is a program that enables people
to remember information efficiently using a spaced repetition algorithm. Anki is definitely
not a sexy app by any means, especially compared to the webbased [Memrise](www.memrise.com),
but it provides a huge amount of control for the end-user. I have come to love Anki for
this very reason.

Anki also provides an easy distribution system where people can share their *decks*. If there
is any language and language course that you are taking, there is probably someone out
there who did it before you and shared an Anki deck for it. Finding quality decks however is
rather hard. Luckily, for the Korean language I found an excellent [Korean vocabulary deck
by Evita](https://ankiweb.net/shared/info/4066961604). For what it's worth, I like to
give credits to her for making my studies so much easier. The deck contains thousands of the
most common words in decreasing order. There is a decent amount of sounds added to,
which really helps with getting the pronunciation right. Unfortunately, too often I found
that sounds are missing. I really wanted to have a more complete set of sound fragments to
improve my studies so decided to write a little script in Python to do this for me.
I will briefly guide you through the steps that are needed to run this script.

# Scraping sound fragments and adding it to your deck
First, obtain the [Korean vocabulary deck by Evita](https://ankiweb.net/shared/info/4066961604) to operate on.
**If you already have made progress in this deck and do not want to lose it**,
it is also possible to export this deck from your own Anki environment. Make sure to include
the progress whilst exporting the `.apkg` file. Copy this file to a empty directory,
for example in `C:\tmp\`, and rename it to `in.apkg`.

The python 3 script at the bottom of this page will scrape the dictionary pages of
[Naver](www.naver.com) (preferred) or [Daum](www.daum.net). Put this script in the working directory, in my case `C:\tmp\script.py`.
Then open a command window in that folder (`shift` + `right click`, then choose *open command
window here* if you are on Windows). The following command will start the script, make sure
that python 3 is installed:

```
python script.py
```

Executing the script will take a few hours. Please wait for it to finish. But no worries,
the script can be interrupted. Simply run the script again to continue where it left off.
In the end, a new file should have appeared named `out.apkg`. This is the new deck,
containing all your originals cards and progress of you Korean vocabulary deck (by *Evita*),
and extended to have more sound fragments. In total, I found that this script adds **4130 new sound fragments**, making a total of 4823 notes with audio and just around 90 that still lack audio. That's quite a significant improvement!

# Can't you just give me your deck?
You clearly see the code and think, should I really run this and set this all up? No,
I understand completely as true programmers are inherently lazy (hence they let programs
do their work). I have simply uploaded a fresh copy of the original deck as stated above,
on which my script did all the heavy lifting. You can simply [download it here]({filename}/files/Korean vocabulary by Evita and Laurens.apkg). I hope this helps you!


### The python script
```python
import sqlite3 as lite
import sys
import requests
from lxml import html
import re
import os
import json
import codecs
from shutil import copyfile, make_archive
import zipfile

# Do not forget to set the working directory. A sdubdirectory named 'download' is expected to be in it.
dir = '.\\' # relative path


def loop_anki_cards():
    copyfile(dir + 'unzip\\collection.anki2', dir + "download\\" + 'collection.anki2')
    con = lite.connect(dir + "download\\" + 'collection.anki2')
    with con:
        cur = con.cursor()
        cur.execute("SELECT id,flds FROM notes")

        rows = cur.fetchall()

        current = 0
        total = len(rows)
        success = 0

        for row in rows:
            current += 1
            fields = row[1].split('\x1f')
            word = fields[0]
            wordE = fields[1]

            if fields[-1] == '':
                print("Attempting to fetch word: {}".format(wordE.encode('utf-8')))
                fetch = fetch_mp3(word)
                if fetch:
                    success += 1
                    fields[-1] = '[sound:_kr_voc_evita_' + word + '.mp3]'
            else:
                # rename the filenames of sound fragmetns to have a prefix, to stop name collision errors with other decks
                fields[-1] = fields[-1][:7] + '_kr_voc_evita_' + fields[-1][7:]

            a = '\x1f'.join(fields).replace("'", "''")

            cur.execute("UPDATE notes SET flds = '" + a + "' WHERE id = " + str(row[0]))
        con.commit()
        return success


def fetch_mp3(word):
    filename = '_kr_voc_evita_' + word + '.mp3'
    if os.path.exists(dir + 'download\\' + filename):
        # File already exists, so no need to download again
        print('>> Sound fragment already exists')
        return filename

    url = fetch_mp3_url(word)
    if url:
        with open(dir + 'download\\' + filename, 'xb') as out_file:
            try:
                file = requests.get(url).content
                out_file.write(file)
                del file
                print('>> Succesfully saved word')
                return filename
            except:
                return None
    else:
        return None


def fetch_mp3_url(word):
    # First attempt naver, if unable to extract sound, try daum.
    url = naver_url(word)
    if not url:
        url = daum_url(word)
    return url


def daum_url(word):
    ############
    # ATTEMPT 1: Standard Daum
    ############
    pre_url = 'http://alldic.daum.net/search.do?q='
    post_url = '&dic=kor'

    # get html and parse it into a searchable tree for python
    page = requests.get(pre_url + word + post_url)
    tree = html.fromstring(page.content)

    # find the mp3 url file javascript code using a XPath
    string = tree.xpath('//*[@id="mArticle"]/div[1]/div[2]/div[2]/div[1]/div/strong/span/a/@href')

    # If succesfully found, extract the sound url from the javascript event between the quotes
    if len(string) > 0:
        mp3 = string[0]
        print(">> Found sound fragment on Daum")
        return mp3

    ############
    # ATTEMPT 2: Daum forwarded
    ############
    # If we get here, it means we couldn't find the sound url because this is a redirecting page. Follow the redirect:
    regex = re.search(".+has_exact_redirect', '(.*)_(.*)'.*", page.text)
    try:
        url = 'http://alldic.daum.net/word/view.do?wordid=%s&q=%s&supid=%s' % (regex.group(1), word, regex.group(2))
        page = requests.get(url)

        tree = html.fromstring(page.content)
        string = tree.xpath('//*[@id="mSub"]/div/div[2]/div/em/span[2]/span/a[1]/@href')
        if len(string) > 0:
            mp3 = string[0]
            print(">> Followed redirect and found sound fragment on Daum")
            return mp3
    except:
            return None

def naver_url(word):
    url = 'http://dic.naver.com/search.nhn?dicQuery={}&query={}'.format(word, word)

    # get html and parse it into a searchable tree for python
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # find the mp3 url file javascript code using a XPath
    i = 1
    while tree.xpath('//ul[contains(@class,"lst_krdic")]/li[%d]/p' % i):
        # Check for each entry what is the precise word
        element = tree.xpath('//ul[contains(@class,"lst_krdic")]/li[%d]/p/a/span' % i)
        if len(element) > 0:
            text = element[0].xpath('string()')
            if text == word:
                # We got a word that matches the one we want. Try and find a audio link
                element = tree.xpath('//ul[contains(@class,"lst_krdic")]/li[%d]/p/a[2]/@playlist' % i)
                if len(element) > 0:
                    # we found a playlist, return the link and exit the function
                    print(">> Found sound fragment on Naver")
                    return element[0]
        i += 1
    return None


def edit_media_file():
    with open(dir + 'unzip\\media', encoding="utf8") as data_file:
        data = json.load(data_file)
    i = len(data)
    for j in range(i):
        print("Moving file...({}/{})".format(j, i - 1))
        data[str(j)] = "_kr_voc_evita_" + data[str(j)]
        copyfile(dir + "unzip\\" + str(j), dir + "download\\" + str(j))
    i = len(data)
    for filename in [x for x in os.listdir(dir + "\\download") if x[-4:] == ".mp3"]:
        data[i] = filename
        os.rename(dir + "download\\" + filename, dir + "download\\" + str(i))
        i += 1

    with codecs.open(dir + 'download\\media', 'w+', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def prepare_dirs():
    # make directories
    if not os.path.exists('unzip'):
        os.makedirs('unzip')
    if not os.path.exists('download'):
        os.makedirs('download')

    with zipfile.ZipFile('in.apkg', "r") as z:
        z.extractall(dir + 'unzip')


def zipdir(dirpath, filename):
    ziph = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    # ziph is zipfile handle
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            ziph.write(os.path.join(root, file), file)


if __name__ == "__main__":
    prepare_dirs()
    addedcount = loop_anki_cards()
    edit_media_file()
    zipdir(dir + "download\\", 'out.apkg')
    print("SUCCESFULLY ADDED {} SOUND FRAGMENTS".format(addedcount))

```
