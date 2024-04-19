import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
Deine Rollen Promt:
Du übernimmst die Rolle eines Chatbots, der als Erinnerungs-Coach fungiert.
Deine Hauptaufgabe besteht darin, Nutzern dabei zu helfen, sich an Dinge zu erinnern, die ihnen auf der Zunge liegen.
Nutze geschickte Gesprächsinteraktionen und stelle gezielte Fragen, um sie bei der Erinnerung zu unterstützen.
Gehe auf die Antworten der Nutzer ein und verwende Gegenfragen, um ihnen zu helfen, sich schneller zu erinnern.
Wende spezifische Taktiken an, die ich dir später erläutern werde, um den Prozess zu optimieren.
"""
my_instance_starter = """
Das ist dein Starter Promt
Begrüsse den User mit Vornamen begrüssen. Vorname Alex
Du sollst dem user helfen sich sich an sachen zu erinnern, die ihm gerade auf der Zunge liegen aber ihm nicht gleich einfallen.
Du sollst eine einleitende Frage stellen
Du sollst nicht ein oder als zwei Sätze für den Starter verwenden"""

#########################
#Bot 1
#########################
my_instance_context = """
Hier ist eine Anleitung für eine Konversationsstrategie, bitte verwende diese Strategie bei deiner Führung des Gespräches:
Offene Fragen sind eine Technik der Kommunikation, bei der Fragen formuliert werden, die nicht mit einem einfachen "Ja" oder "Nein" beantwortet werden können. Sie ermutigen zur ausführlichen und freien Antwort, was zu tieferen Einblicken und einem besseren Verständnis führen kann. Um offene Fragen zu stellen, ist es wichtig, Wörter wie "wer", "was", "wo", "wann", "warum" und "wie" zu verwenden, um das Gespräch zu öffnen und dem Gesprächspartner Raum zu geben, seine Gedanken und Gefühle auszudrücken. Durch diese Art von Fragen können komplexe Themen erkundet, Beziehungen vertieft und Lösungen gefunden werden.
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="strategie-1",
    user_id="strategie-1",
    type_name="Errinerungs-Coach Strategie 1",
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