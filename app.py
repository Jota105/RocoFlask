from flask import Flask
from flask_restful import Api

from resources.speachToText import SpeachToText, home
from resources.textToSpeach import TextToSpeach
from resources.watson import Watson
from resources.speachToText import SpeachToText



app = Flask(__name__)
app.secret_key = 'EiEiO'
api = Api(app)

# a ser borrado

# a ser borrado
api.add_resource(home, '/')
api.add_resource(SpeachToText, '/StT')
api.add_resource(TextToSpeach, '/TtS')
api.add_resource(Watson, '/watson')

if __name__ == '__main__':
    app.run(host ="0.0.0.0", port =5000, debug=True)
