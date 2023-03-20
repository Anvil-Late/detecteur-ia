from flask import Flask, render_template, request
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from OpenSSL import SSL
from flask_talisman import Talisman

app = Flask('Detecteur-ia')
barthez_tokenizer = AutoTokenizer.from_pretrained("moussaKam/barthez")
model = AutoModelForSequenceClassification.from_pretrained("Anvil-ML/detecteur-ia")

def interpret_pred_with_sensibility(pred):
    low_bond = -6.748472
    high_bound = 6.7176056
    pred_value = pred[0][1].item()
    interpreted_pred = (pred_value - low_bond) / (high_bound - low_bond)
    if interpreted_pred < 0.5:
        proba = "très faible"
    elif interpreted_pred < 0.6:
        proba = "faible"
    elif interpreted_pred < 0.8:
        proba = "modérée"
    elif interpreted_pred < 0.95:
        proba = "élevée"
    else:
        proba = "très élevée"

    return proba


@app.route('/')
def show_predict_isai_form():
    return render_template('predictorform.html')


@app.route('/results', methods=['POST'])
def results():

    form = request.form
    if request.method == 'POST':

        text_sentence = request.form['text_sentence']
        input_ids = torch.tensor(
            [barthez_tokenizer.encode(text_sentence, add_special_tokens=True)]
        )
        predict = model.forward(input_ids)[0]
        result = interpret_pred_with_sensibility(predict)

        return render_template('resultsform.html', text_sentence=text_sentence, result=result)

Talisman(app, content_security_policy=None)

sslctx = ("/etc/letsencrypt/live/detecteur-ia.fr/fullchain.pem", "/etc/letsencrypt/live/detecteur-ia.fr/privkey.pem")
app.run(host="0.0.0.0", port="443", debug=False, use_reloader=False, ssl_context=sslctx)