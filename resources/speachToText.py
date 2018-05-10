from flask_restful import Resource, reqparse
import os
import werkzeug

import json
import sys
import base64

from .watsonAPI import Watson_API

class SpeachToText(Resource):
    """docstring for [object Object]."""


    credentials = json.loads(open(os.path.join(os.path.dirname(__file__), 'credentials.json')).read())
    watson = Watson_API(os.path.join(os.path.dirname(__file__), 'credentials.json'))

    def get(self):
        return {"message": "Y si le quiero enviar unas malcriadas, ¿como hariamos?"}


    parser = reqparse.RequestParser()

    parser.add_argument('audio',
        type=werkzeug.datastructures.FileStorage,
        required=True,
        location='files'
    )
    parser.add_argument('_id',
        type=int,
        required=True,
        help="Every item needs a store_id."
    )

    def post(self):
        data = SpeachToText.parser.parse_args()

        assets_path = os.path.join('./assets/', str(data['_id']) )

        if not os.path.exists( assets_path ):
            os.mkdir(assets_path)

        # Guardar el audio recibido en assets/input.mp3
        bytes_audio = data['audio'].stream.read()
        f = open(os.path.join(assets_path, 'input.mp3'  ), 'wb' )
        f.write(bytes_audio)
        f.close()

        file_path = os.path.join(assets_path, 'input.mp3')

        """
        # Test
        # Leer el archivo que fue guardado
        ifile = open(file_path, 'rb')
        a = ifile.read()
        ifile.close()

        # imprimirlo como texto
        f = open(os.path.join(assets_path, 'test.txt'  ), 'w' )
        f.write(base64.b64encode(a).decode('utf-8'))
        f.close()

        # leer el archivo de texto
        f = open(os.path.join(assets_path, 'test.txt'  ), 'r' )
        b = f.read()
        f.close()

        # guardar lo que lei como mp3
        f = open(os.path.join(assets_path, 'testx.mp3'  ), 'wb' )
        f.write(base64.b64decode(b.encode('utf-8')))
        f.close()
        """
        #return {"mensaje": base64.b64encode(bytes_audio).decode('utf-8')}
        return {"mensaje": self.watson.speech_to_text(file_path)}


class home(Resource):
    def get(self):
        a = os.path.join('../../WATSON_CODE')
        return {"message": [name for name in os.listdir(os.path.join('./../WATSON_CODE')) if os.path.isdir(name)]}
