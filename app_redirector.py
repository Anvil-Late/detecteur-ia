from flask import Flask, , request, redirect

app = Flask('redirector')


@app.before_request
def before_request():
    if request.url.startswith("http://"):
        url = request.url.replace('http://', 'https://' , 1)
        code = 301
        return redirect(url, code=code)


@app.route("/")
def redirect():
    return "Redirecting"


sslctx = ("/etc/letsencrypt/live/detecteur-ia.fr/fullchain.pem", "/etc/letsencrypt/live/detecteur-ia.fr/privkey.pem")
app.run(host="0.0.0.0", port="80", debug=False, use_reloader=False, ssl_context=sslctx)
