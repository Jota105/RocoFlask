import re
import json
from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import AssistantV1
from watson_developer_cloud.assistant_v1 import Context
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions,EntitiesOptions,KeywordsOptions
from watson_developer_cloud import LanguageTranslatorV2


class Watson_API:
    def __init__(self, credentials_file):
        self.credentials = json.loads(open(credentials_file).read())

    def init_service(self, service, service_name, **kwargs):
        url      = self.credentials[service_name][0]['credentials']['url']
        username = self.credentials[service_name][0]['credentials']['username']
        password = self.credentials[service_name][0]['credentials']['password']
        if service_name == 'conversation' or service_name== "natural_language_understanding":
            return service(kwargs['version'], url, username, password)
        return service(url, username, password)

    def text_to_speech(self, text, output_file, audio_format='audio/mp3',
                                                voice='es-ES_EnriqueVoice'):
        text2speech = self.init_service(TextToSpeechV1, 'text_to_speech')
        with open(output_file, 'wb') as audio_file:
            audio = text2speech.synthesize(text, accept=audio_format, voice=voice)
            audio_file.write(audio.content)

    def list_voices(self):
        text2speech = self.init_service(TextToSpeechV1, 'text_to_speech')
        return [voice['name'] for voice in text2speech.list_voices()['voices']]

    def speech_to_text(self, input_file, audio_format='audio/mp3',
                                         model='es-ES_BroadbandModel'):
        speech2text = self.init_service(SpeechToTextV1, 'speech_to_text')
        with open(input_file, 'rb') as audio_file:
            text = speech2text.recognize(audio=audio_file, content_type=audio_format,
                                         model=model)
        return text['results'][0]['alternatives'][0]['transcript']

    def list_models(self):
        speech2text = self.init_service(SpeechToTextV1, 'speech_to_text')
        return [model['name'] for model in speech2text.list_models()['models']]

    def get_emotions(self, message):
        version='2018-03-16'
        analyzer = self.init_service(NaturalLanguageUnderstandingV1,'natural_language_understanding', version=version)
        response = analyzer.analyze(text=message,features=Features(
                    entities=EntitiesOptions(
                      emotion=True,
                      sentiment=True,
                      limit=2),
                    keywords=KeywordsOptions(
                      emotion=True,
                      sentiment=True,
                      limit=2)))
        print(json.dumps(response, indent=2))

    def translate(self, message):
        translator = self.init_service(LanguageTranslatorV2, 'natural_language_translator')
        translation = translator.translate(text=message, model_id='es-en')
        return translation['translations'][0]
        #print(json.dumps(translation, indent=2, ensure_ascii=False))


    def send_message(self, message, index=0, context=None, output_index=0):
        pattern = re.compile('version=(\d+-\d+-\d+)')
        version = pattern.findall('/v1/workspaces?version=2018-02-16')[0]
        assistant = self.init_service(AssistantV1, 'conversation', version=version)
        workspace_id = assistant.list_workspaces()['workspaces'][index]['workspace_id']
        # print(workspace_id)
        response = assistant.message(workspace_id, input={'text': message}, context=context)
        print(context)
        # print(response)
        return response['output']['text'][output_index], response['context']['conversation_id']

    def list_workspaces(self):
        pattern = re.compile('version=(\d+-\d+-\d+)')
        version = pattern.findall('/v1/workspaces?version=2018-02-16')[0]
        assistant = self.init_service(AssistantV1, 'conversation', version=version)
        return [workspace['name'] for workspace in assistant.list_workspaces()['workspaces']]

    def roco_endpoint(self, audio_input, audio_output, context_id=None, workspace_index=1,
                      output_index=0):
        text_input = self.speech_to_text(audio_input)
        print('Input <', text_input)
        text_output, context_id = self.send_message(text_input, workspace_index,
                                        Context(context_id), output_index=output_index)
        print('Output >', text_output)
        if len(text_output) > 0:
            self.text_to_speech(text_output, audio_output)
        return context_id, text_output
