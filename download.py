#!/usr/bin/python3
import requests
import mechanize
import subprocess
import urllib.parse
from urllib.parse import unquote
import os


try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

bookname = None
s = requests.Session()
browser = mechanize.Browser()
browser.set_handle_robots(False)


# Download from various mirrors
def download_from_1(download_link):
    """
    Download from mirror 1. Mirror 1 is typically a http://library.lol
    """

    try:
        browser.open(download_link)
        download_page = browser.response().read()
        parser = BeautifulSoup(download_page, "lxml")
        direct_download = parser.find("a").attrs["href"]
        book_content = s.get(direct_download)
        
        if 'Content-Disposition' in book_content.headers:
            bookname = book_content.headers['Content-Disposition'].split('"')[1]
            
        with open("EPUB/" + bookname, "wb") as r:
            r.write(book_content.content)

        os.environ['BOOKNAME'] = bookname
        return True

    except Exception as err:
        print(err)
        return False

    
def download_from_2(download_link):
    """
    Download from mirror 2. Mirror 2 is typically a http://libgen.lc/
    """

    try:
        # THIS "s" equals s = requests.Session()
        download_link = download_link.replace("http://libgen.lc/ads.php?md5=", "http://library.lol/main/")
        response = s.get(download_link)
        direct_download = [x for x in response.text.split('"') if "cloud" in x][0]
        book_content = s.get(direct_download)
        
        if 'Content-Disposition' in book_content.headers:
            bookname = book_content.headers['Content-Disposition'].split('"')[1]
            
        bookname = unquote(bookname)
        with open("EPUB/" + bookname, "wb") as r:
            r.write(book_content.content)

        os.environ['BOOKNAME'] = bookname          
        return True
        
    except Exception as err:
        print(err)
        return False

        
def download_from_3(download_link):
    """
    Download from mirror 3. Mirror 3 is typically a https://3lib.net/
    """

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63',
 'cookie': 'remix_userkey=cb9e9db64085083d632939a8bb3ecd99; remix_userid=9532777'}
    

    try:
        # THIS "s" equals s = requests.Session()
        #print('[+] Download this book: ', download_link) # EXPECTED STRUCTURE: https://3lib.net/book/5227321/d0a115
        response = s.get(download_link, headers=headers)

        direct_link = "https://3lib.net" + [x for x in response.text.split('"') if 'dl' in x][1]
        book_content = s.get(direct_link, headers=headers)
        
        if 'Content-Disposition' in book_content.headers:
            bookname = book_content.headers['Content-Disposition'].split('"')[1][:-5]
                     
        with open("EPUB/" + bookname, "wb") as r:
            r.write(book_content.content)
            return True
        
    except Exception as err:
        print(err)
        return False        


def download_from_4(download_link):
    """
    (broken at time of writing this code)
    Download from mirror 4. Mirror 4 is typically a https://libgen.me/
    """
    pass


def parsebookreq(bookname):
    bookname = urllib.parse.quote(bookname)
    url = f"https://libgen.is/search.php?req={bookname}&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def"
    #print(url)
    return url


def download_book(download_links):
    """
    Try to download from various mirrors until successful download
    """
    
    print('\n[+] Download started...')
    print("[+] Try mirror 1")
    if not download_from_1(download_links[0]):
        print("[+] Try mirror 2")
        if not download_from_2(download_links[1]):
            print("[+] Try mirror 3")
            if not download_from_3(download_links[2]):
                print("[+] Try mirror 4")
                if not download_from_4(download_links[3]):
                    print("[-] Error")
                    return False
                
    print('[+] Download successful!\n')                


def search(bookname):
    # embed bookname in URI and open URI
    url = parsebookreq(bookname)
    browser.open(url)

    # get raw HTML and parse it by lxml parser
    html = browser.response().read()
    parsed_html = BeautifulSoup(html, 'lxml')

    # find all <tr valign="top">
    books = parsed_html.body.find_all('tr', attrs={'valign':'top'})

    books_details = []

    # Iterate all books to fill list of books_details
    for book in books[1:]:
        raw_book_info = book.find_all("td")
        
        # Get all download links in list
        download_links = []
        for download_elmt in raw_book_info[9:14]:
            if not download_elmt.has_attr("style"):
                download_link = download_elmt.find('a').attrs["href"]
                #print(download_link)
                download_links.append(download_link)

        books_details.append({
            "name": raw_book_info[2].text,
            "author": raw_book_info[1].text,
            "publisher": raw_book_info[3].text,
            "year_published": raw_book_info[4].text,
            "pages": raw_book_info[5].text,
            "size": raw_book_info[7].text,
            "extension": raw_book_info[8].text,
            "download_links": download_links
        })

    return books_details


def down(books_details, email):
    # book_details = search(bookname)
    # book_details = book_details[1] or book_details[2] or ....
    
    download_book(books_details["download_links"])
    bookname = os.environ['BOOKNAME']
    os.system("python convert.py")
    print()
    os.system(f'python send_to_kindle.py --email {email} --bookname "{bookname}"')


# books_details = search('bookname')
# cont = 1    
# for x in books_details:
#     print("Índice: ", cont)
#     print(x["name"])
#     print(x["extension"])
#     print(x["author"])
#     print(x["download_links"])
#     cont += 1


# ind = int(input("Digite um índice: ")) - 1
# down(ind)





