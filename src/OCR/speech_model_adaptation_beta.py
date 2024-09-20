# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START speech_transcribe_with_model_adaptation]
import uuid

import google.auth

from google.cloud import speech_v1p1beta1 as speech

from ocr import get_pattern_string,get_media_file_name
#sys.path.append('../OCR')

adaptationClient = speech.AdaptationClient()

def transcribe_with_model_adaptation(
    project_id, location, storage_uri, custom_class_id, phrase_set_id):

    with open(storage_uri, "rb") as audio_file:
        content = audio_file.read()

    """
    Create`PhraseSet` and `CustomClasses` to create custom lists of similar
    items that are likely to occur in your input data.
    """

    # Create the adaptation client
    adaptation_client = speech.AdaptationClient()

    # The parent resource where the custom class and phrase set will be created.
    parent = f"projects/{project_id}/locations/{location}"

    # Create the custom class resource
    adaptation_client.create_custom_class(
        {
            "parent": parent,
            "custom_class_id": custom_class_id,
            "custom_class": {
                "items": [{"value" : x} for x in get_pattern_string() ]
            },
        }
    )
    custom_class_name = (
        f"projects/{project_id}/locations/{location}/customClasses/{custom_class_id}"
    )
    # Create the phrase set resource
    phrase_set_response = adaptation_client.create_phrase_set(
        {
            "parent": parent,
            "phrase_set_id": phrase_set_id,
            "phrase_set": {
                "boost": 10,
                "phrases": [
                    {"value": f"Visit restaurants like ${{{custom_class_name}}}"}
                ],
            },
        }
    )
    phrase_set_name = phrase_set_response.name
    # The next section shows how to use the newly created custom
    # class and phrase set to send a transcription request with speech adaptation

    # Speech adaptation configuration
    speech_adaptation = speech.SpeechAdaptation(phrase_set_references=[phrase_set_name])

    # speech configuration object
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="en-US",
        adaptation=speech_adaptation,
        enable_automatic_punctuation = True,
        enable_spoken_punctuation = True,
    )

    # The name of the audio file to transcribe
    # storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]

    audio = speech.RecognitionAudio(content=content)

    # Create the speech client
    speech_client = speech.SpeechClient()

    response = speech_client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

    # [END speech_transcribe_with_model_adaptation]

    return response.results[0].alternatives[0].transcript

def get_custom_class_id():
    # The custom class id can't be too long
    custom_class_id = f"customClassId{str(uuid.uuid4())[:8]}"
    return custom_class_id

def get_phrase_set_id():
    # The phrase set id can't be too long
    phrase_set_id = f"phraseSetId{str(uuid.uuid4())[:8]}"
    return phrase_set_id

def model_adaptation():
    STORAGE_URI = get_media_file_name()
    _, PROJECT_ID = google.auth.default()
    LOCATION = "global"
    class_id = get_custom_class_id()
    phrase_id = get_phrase_set_id()

    transcript = transcribe_with_model_adaptation(PROJECT_ID, LOCATION, STORAGE_URI, class_id, phrase_id)
    print("Model Transcript: %s" % transcript)

    with open("../../resources/updatedtranscript/optimized_transcript.txt", "w") as text_file:
        text_file.write("%s" % transcript)

    # clean up resources
    CLASS_PARENT = (
        f"projects/{PROJECT_ID}/locations/{LOCATION}/customClasses/{class_id}"
    )
    adaptationClient.delete_custom_class(name=CLASS_PARENT)

    # clean up resources
    PHRASE_PARENT = (
        f"projects/{PROJECT_ID}/locations/{LOCATION}/phraseSets/{phrase_id}"
    )
    adaptationClient.delete_phrase_set(name=PHRASE_PARENT)
