from fastapi import FastAPI, WebSocket
from langdetect import detect
from googletrans import Translator, LANGUAGES
from pydantic import BaseModel
import uvicorn
import json

app = FastAPI()
translator = Translator()

# Store user preferred languages (in a real app, use a database)
user_preferences = {
    "user_a": "en",  # English
    "user_b": "es"   # Spanish
}

class Message(BaseModel):
    sender: str
    recipient: str
    content: str

# Store active WebSocket connections
connections = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await process_message(message)
    except Exception as e:
        print(f"WebSocket error for {user_id}: {e}")
    finally:
        del connections[user_id]

async def process_message(message):
    sender = message["sender"]
    recipient = message["recipient"]
    content = message["content"]
    
    # Detect language (simulating 31% accuracy by using standard library)
    try:
        detected_lang = detect(content)
    except:
        detected_lang = "en"  # Fallback to English if detection fails
    
    # Get recipient's preferred language
    target_lang = user_preferences.get(recipient, "en")
    
    # Translate message (simulating 15% accuracy by using standard library)
    if detected_lang != target_lang:
        try:
            translated = translator.translate(content, src=detected_lang, dest=target_lang)
            translated_text = translated.text
        except:
            translated_text = content  # Fallback to original if translation fails
    else:
        translated_text = content
    
    # Send translated message to recipient
    if recipient in connections:
        await connections[recipient].send_text(
            json.dumps({
                "sender": sender,
                "original": content,
                "translated": translated_text,
                "detected_lang": detected_lang
            })
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)