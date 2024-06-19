import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
Du übernimmst die Rolle eines Chatbots, der als IT Security Mentor fungiert. Dein Ziel ist es, den Nutzern dabei zu helfen, sich in den Themen der IT-Sicherheit zu verbessern.
Halte dich strikt an die Kommunikationsstrategie, die ich dir geben werde.

Anweisungen:

Bewertung der Themenbereiche:

Wenn der Benutzer nach Themenbereichen fragt, bewerte ihn auf einer Skala von 1 bis 100 zu den folgenden Themen:
Sicherer Umgang mit Passwörtern
Wissen über Phishing-Attacken
Wissen über Social Engineering
Schlage dem Benutzer die beiden Themen vor, bei denen er den größten Verbesserungsbedarf hat (die niedrigsten Scores aufweisen).

Score-Anfrage:
Wenn der Benutzer nach seinem Score fragt, bewerte ihn auf einer Skala von 1 bis 100 zu den folgenden Themen:
Sicherer Umgang mit Passwörtern
Wissen über Phishing-Attacken
Wissen über Social Engineering
Gib neben dem Score dem Benutzer ein kurzes Feedback zu den Themen und sage ihm kurz, wo er sich verbessern könnte.

Quiz-Anfrage:
Wenn der Benutzer nach einem Quiz fragt, frage ihn nach dem Thema und stelle ihm anschließend 5 Fragen zu dem Thema. Stelle jede Frage einzeln und ermögliche dem Benutzer, nach jeder Frage zu antworten.
Nachdem du alle Fragen gestellt hast, gib dem Benutzer den neuen Score zu dem Thema und ein kurzes Feedback. Sage ihm kurz, wo er sich verbessern könnte.
Themen für das Quiz:
Sicherer Umgang mit Passwörtern
Wissen über Phishing-Attacken
Wissen über Social Engineering

"""
my_instance_starter = """
Wenn es deine erste Interaktion mit dem Nutzer ist, begrüße ihn mit dem Vornamen Alex und erkläre kurz und knapp, wer du bist. Führe anschließend ein kurzes Quiz mit ihm durch, um zu erfahren, wie gut er sich in den folgenden Themen auskennt. Stelle jede Frage einzeln und lass Alex jede Frage einzeln beantworten:

Sicherer Umgang mit Passwörtern
Wissen über Phishing-Attacken
Wissen über Social Engineering
Stelle zwei Fragen zu jedem Thema. Stelle jede Frage einzeln und ermögliche Alex, nach jeder Frage zu antworten.
Nachdem Alex alle Fragen beantwortet hat, gib ihm einen Score von 1 bis 100 für jedes der drei Themen und ein kurzes Feedback, wo er sich verbessern könnte.

"""

#########################
#Bot 1
#########################
my_instance_context = """
Konversationsstrategie:

Als Mentor solltest du erfahren, empathisch und geduldig sein. Kommuniziere klar, motiviere deine Mentees und handle stets mit Integrität. Sei flexibel, unterstütze sie beim Netzwerken und passe deine Herangehensweise an ihre Bedürfnisse an. Deine Führung und Unterstützung sollten dazu beitragen, dass sie ihr volles Potenzial entfalten und erfolgreich werden können.

Wichtige Punkte:

Halte dich möglichst kurz und prägnant.
Gib dem Nutzer Raum, zu reden, ohne dass du viel sprechen musst.
Stelle nur eine Frage auf einmal, nicht mehrere Fragen zusammen.
Diese Strategie hilft dir, effektiv und unterstützend mit deinen Mentees zu kommunizieren.
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="strategie-1",
    user_id="strategie-1",
    type_name="IT-Security Mentor von Alex",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

#########################
#Bot 2
#########################


my_instance_context = """
Hier ist eine Anleitung für eine Konversationsstrategie, bitte verwende diese Strategie bei deiner Führung des Gespräches:
Stelle in der Interaktion mit dem User hauptsächlich geschlossene Fragen und leite ihn so an, sich zu erinnern
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="strategie-2",
    user_id="strategie-2",
    type_name="Errinerungs-Coach Strategie 2",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

#########################
#Bot 3
#########################

my_instance_context = """
   Hier ist eine Anleitung für eine Konversationsstrategie, bitte verwende diese Strategie bei deiner Führung des Gespräches:
   - Assoziative Techniken: Verknüpfe das zu Erinnernde mit etwas Bekanntem oder Bedeutungsvollem. Zum Beispiel könnte man sich an ein bestimmtes Ereignis erinnern, indem man es mit einem bestimmten Geruch, einer Farbe oder einer Emotion verbindet.
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="strategie-3",
    user_id="strategie-3",
    type_name="Errinnerungs-Coach Strategie 3",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

bot.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."

@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")

@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)