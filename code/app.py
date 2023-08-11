# from pysentimiento import analyzer  # Español
from pysentimiento import create_analyzer
from langdetect import detect
from flask import Flask, render_template, request
import spacy

# Analisis de sentimientos
# from nltk.sentiment.vader import SentimentIntensityAnalyzer  # Ingles
# sid = SentimentIntensityAnalyzer()

analyzer = create_analyzer(task="sentiment", lang="es")
analyzer_eng = create_analyzer(task="sentiment", lang="en")

app = Flask(__name__)


@app.route("/")
def indice():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def procesa_texto():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        idioma = detect(rawtext)
        sentimientos = []
        if idioma == 'es':
            try:
                nlp = spacy.load("es_core_news_md")
            except:  # Si el idioma no existe, descargalo
                # spacy.cli.download("es_dep_news_trf")
                print(
                    "No reconozco el idioma,se queda cargado Español: es_core_news_md, por defecto ")
                nlp = spacy.load("es_core_news_md")
            print("Idioma Español: cargamos es_dep_news_trf")
            # Analisis de sentimiento
            sentimientos = analyzer.predict(rawtext)
            # print(sentimientos)

        elif idioma == 'en':
            try:
                nlp = spacy.load("en_core_web_md")
            except:
                # spacy.cli.download("en_core_web_trf")
                print(
                    "No reconozco el idioma,se queda cargado Ingles: en_core_web_md, por defecto ")
                nlp = spacy.load("en_core_web_md")
            print("Idioma Ingles: cargamos en_core_web_md")
            # Analisis de sentimiento
            sentimientos = analyzer_eng.predict(rawtext)
            # print(sentimientos)
            # sentimientos = sid.polarity_scores(rawtext) #con # from nltk.sentiment.vader import SentimentIntensityAnalyzer  # Ingles

        else:
            try:
                nlp = spacy.load("es_core_news_md")
            except:  # Si el idioma no existe, descargalo
                # spacy.cli.download("es_dep_news_trf")
                # nlp = spacy.load("es_dep_news_trf")
                nlp = spacy.load("es_core_news_md")
                print(
                    "No reconozco el idioma,se queda cargado Español: es_dep_news_trf, por defecto ")

        opcion = request.form['taskoption']
        doc = nlp(rawtext)
        results = [(entidad.label_, entidad.text) for entidad in doc.ents]

        entidad_ORG = []
        entidad_PER = []
        entidad_LOC = []
        entidad_TIME = []
        entidad_LANGUAGE = []
        entidad_MISC = []

        for entidad in doc.ents:
            # print(entidad.label_, entidad.text)
            if entidad.label_ == 'ORG':
                entidad_ORG.append((entidad.label_, entidad.text))
            elif entidad.label_ == 'PER' or entidad.label_ == 'PERSON':
                entidad_PER.append((entidad.label_, entidad.text))
            elif entidad.label_ == 'LOC' or entidad.label_ == 'GPE':
                entidad_LOC.append((entidad.label_, entidad.text))
            elif entidad.label_ == 'TIME':
                entidad_TIME.append((entidad.label_, entidad.text))
            elif entidad.label_ == 'LANGUAGE':
                entidad_LANGUAGE.append((entidad.label_, entidad.text))
            elif entidad.label_ == 'MISC':
                entidad_MISC.append((entidad.label_, entidad.text))

        if opcion == 'organization':
            results = entidad_ORG
            num_of_results = len(results)
        elif opcion == 'person':
            results = entidad_PER
            num_of_results = len(results)
        elif opcion == 'location':
            results = entidad_LOC
            num_of_results = len(results)
        elif opcion == 'time':
            results = entidad_TIME
            num_of_results = len(results)
        elif opcion == 'language':
            results = entidad_LANGUAGE
            num_of_results = len(results)
        elif opcion == 'misc':
            results = entidad_MISC
            num_of_results = len(results)
        else:
            results = [(entity.label_, entity.text) for entity in doc.ents]
            num_of_results = len(results)

    return render_template('index.html', num_of_results=num_of_results, results=results, sentimientos=sentimientos)


if __name__ == '__main__':
    app.run(debug=True)
