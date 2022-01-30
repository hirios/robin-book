# Robin-Book
Search books (include pt-br), convert and send to kindle

Obs: Windows user, install Calibre-Ebook manually

## Windows Users

Install calibre-ebook on this link -> https://calibre-ebook.com/

```pip install -r requirements.txt```

## Installation Linux


#### Install Calibre-Ebook
```
sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sudo sh /dev/stdin
```
This is to convert EPUB to AZW3

#### Install Python requirements
```
pip install -r requirements.txt
```

## Usage

In the `config.txt` file you must enter your email and [password](https://umd.service-now.com/itsupport?id=kb_article&article=KB0015112&sys_kb_id=76433076dbdf8c904cb035623996194b&spa=1) (*application type password*), host (optional) and port (optional).

```
python main_server.py
```

This command starts a server locally (localhost:8080)<br>
![Image description](https://user-images.githubusercontent.com/35049559/148115530-7392036b-cb52-47bf-a5c2-a3ef5be87cbd.png)

Select a version available on epub (If you want to send to kindle)
![Image description](https://user-images.githubusercontent.com/35049559/127069472-8793b01c-69a9-4542-a5bf-96a5436ea298.png)


## References 
- [1] https://pythoncircle.com/post/212/python-script-1-convert-ebooks-from-epub-to-mobi-format/
- [2] https://github.com/ParampreetR/books_downloader
