from flask import Flask, render_template, url_for, redirect
from flask import request
from time import sleep
import webbrowser
import download
import socket
import ast


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
IPs = {}


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        kindle_email = request.form["k_email"]
        bookname = request.form["b_name"]
        return redirect(url_for("search", bookname=bookname, email=kindle_email))

    return render_template("index.html")


@app.route('/book/<bookname>/<email>')
def search(bookname, email):
    IP_client = request.environ['REMOTE_ADDR']

    # ATRIBUINDO LISTA AO IP DE SOLICITAÇÃO
    IPs[IP_client] = download.search(bookname)

    if len(IPs[IP_client]) == 0:
        return """<h1>!!! LIVRO NAO ENCONTRADO !!!</h1>"""
    html_return = []
    cont = 0
    for x in IPs[IP_client]:
        book_index = str(cont)
        book_name = x["name"]
        book_autor = x["author"]
        book_format = x["extension"]

        html_mold = f"""
        <body>
        <div id="loading"></div>
        <div id="content"></div>
        <a id="a_link" href="/select/{book_index}/{email}">
            <h2 style="color: red;" onclick="LOAD2()">{book_name}</h2>
        </a>
        <h2 id="h_um">  {book_autor}</h2>
        <h2 id="h_dois"> {book_format}</h2><br>
        </body>
        """

        html_return.append(html_mold)
        cont += 1


    return "".join(html_return), 200


@app.route('/select/<index>/<email>')
def select(index, email):
    IP_client = request.environ['REMOTE_ADDR']

    if IP_client in IPs:
        try:
            download.down(IPs[IP_client][int(index)], email=email)
            return """
            <h2>Livro enviado com sucesso!<h2>
            <button type="button" onclick="location.href='/';">RETURN</button>
            """

        except Exception as err:
            print(err)
            return "<h2>Falha no download do livro :( <h2>"

    return redirect(url_for("home"))


def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip_machine = s.getsockname()[0]
	s.close()
	return ip_machine


with open('config.txt') as f:
	config = ast.literal_eval(f.read())


HOST = config['host']
PORT = config['port']


if not HOST:
	HOST = get_ip()

if not PORT:
	PORT = 5000
else:
	PORT = int(PORT)	


if __name__ == '__main__':
    #webbrowser.open(f'http://localhost:{PORT}')
    app.run(host=HOST, port=PORT, debug=True, use_reloader=True)
    
