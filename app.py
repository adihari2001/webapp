import asyncio
import json
import websockets
from azure.communication.callautomation._shared.models import identifier_from_raw_id
import os
from dotenv import load_dotenv
load_dotenv()

async def handle_client(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            json_object = json.loads(message)
            kind = json_object['kind']
            if kind == 'TranscriptionMetadata':
                print("Transcription metadata")
                print("-------------------------")
                print("Subscription ID:", json_object['transcriptionMetadata']['subscriptionId'])
                print("Locale:", json_object['transcriptionMetadata']['locale'])
                print("Call Connection ID:", json_object['transcriptionMetadata']['callConnectionId'])
                print("Correlation ID:", json_object['transcriptionMetadata']['correlationId'])
            if kind == 'TranscriptionData':
                participant = identifier_from_raw_id(json_object['transcriptionData']['participantRawID'])
                word_data_list = json_object['transcriptionData']['words']
                print("Transcription data")
                print("-------------------------")
                print("Text:", json_object['transcriptionData']['text'])
                print("Format:", json_object['transcriptionData']['format'])
                print("Confidence:", json_object['transcriptionData']['confidence'])
                print("Offset:", json_object['transcriptionData']['offset'])
                print("Duration:", json_object['transcriptionData']['duration'])
                print("Participant:", participant.raw_id)
                print("Result Status:", json_object['transcriptionData']['resultStatus'])
                for word in word_data_list:
                    print("Word:", word['text'])
                    print("Offset:", word['offset'])
                    print("Duration:", word['duration'])
            
    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected")
    except websockets.exceptions.ConnectionClosedError as e:
        print("Connection closed with error: %s", e)
    except Exception as e:
        print("Unexpected error: %s", e)

start_server = websockets.serve(handle_client, "0.0.0.0", int(os.getenv("PORT", 8081)))

print('WebSocket server running on port 8081')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()