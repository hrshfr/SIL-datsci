from flask import Flask, request, render_template
from logging.config import dictConfig
import pickle
import datetime as dt
import numpy as np
import babel.numbers

LOGGER = ({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

dictConfig(LOGGER)

bawang_bonggol_model = pickle.load(open('./model/BawangBonggol.pkl','rb'))
beras_medium_model = pickle.load(open('./model/BerasMedium.pkl','rb'))
cabe_merah_keriting_model = pickle.load(open('./model/CabeMerahKeriting.pkl','rb'))
daging_ayam_model = pickle.load(open('./model/DagingAyam.pkl','rb'))
daging_sapi_model = pickle.load(open('./model/DagingSapi.pkl','rb'))
gula_pasir_model = pickle.load(open('./model/GulaPasir.pkl','rb'))
kedelai_model = pickle.load(open('./model/Kedelai.pkl','rb'))
minyak_goreng_kemasan_model = pickle.load(open('./model/MinyakGorengKemasan.pkl','rb'))
telur_ayam_model = pickle.load(open('./model/TelurAyam.pkl','rb'))
terigu_model = pickle.load(open('./model/Terigu.pkl','rb'))

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def predict():
    if request.method == "GET":
        return render_template("index.html")

    commodity = request.form.get("komoditas")
    date = request.form.get("tanggal")

    app.logger.info('Start prediction. Commodity: %s, Date: %s.', commodity, date)

    prediction = get_prediction(commodity, date)

    currency_string = babel.numbers.format_currency(round(prediction), "Rp", locale='id_ID')

    app.logger.info('Prediction ends with response: %s', currency_string)

    return render_template("index.html", currency_string=currency_string, date=date)

def get_prediction(commodity, date):
    value = np.array([[dt.datetime.toordinal(dt.datetime.strptime(date, '%Y-%m-%d'))]])

    match commodity:
        case "Bawang Bonggol":
            return bawang_bonggol_model.predict(value)[0][0]
        case "Beras Medium":
            return beras_medium_model.predict(value)[0][0]
        case "Cabe Merah Keriting":
            return cabe_merah_keriting_model.predict(value)[0][0]
        case "Daging Ayam":
            return daging_ayam_model.predict(value)[0][0]
        case "Daging Sapi":
            return daging_sapi_model.predict(value)[0][0]
        case "Gula Pasir":
            return gula_pasir_model.predict(value)[0][0]
        case "Kedelai":
            return kedelai_model.predict(value)[0][0]
        case "Minyak Goreng Kemasan":
            return minyak_goreng_kemasan_model.predict(value)[0][0]
        case "Telur Ayam":
            return telur_ayam_model.predict(value)[0][0]
        case "Terigu":
            return terigu_model.predict(value)[0][0]

if __name__ == "__main__":
    app.run(debug=True)