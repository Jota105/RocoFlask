import os
import werkzeug

import json
import sys
import base64

from .watsonAPI import Watson_API

from flask_restful import Resource, reqparse


class Watson(Resource):

    credentials = json.loads(open(os.path.join(os.path.dirname(__file__), 'credentials.json')).read())
    watson = Watson_API(os.path.join(os.path.dirname(__file__), 'credentials.json'))

    def get(self):
        print()
        return {"voices" : self.watson.list_voices()}

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
        data = Watson.parser.parse_args()

        assets_path = os.path.join('./assets/', str(data['_id']) )
        input_file = os.path.join(assets_path, 'input.mp3'  )
        output_file = os.path.join(assets_path, 'output.mp3'  )
        if not os.path.exists( assets_path ):
            os.mkdir(assets_path)

        # Guardar el audio recibido en assets/input.mp3
        bytes_audio = data['audio'].stream.read()
        f = open(input_file, 'wb' )
        f.write(bytes_audio)
        f.close()

        id_conversation = self.watson.roco_endpoint(input_file, output_file)

        # Leer el archivo que fue generado
        ifile = open(output_file, 'rb')
        bytes_audio = ifile.read()
        ifile.close()

        return {"id_conversation": id_conversation, "message": base64.b64encode(bytes_audio).decode('utf-8')}
