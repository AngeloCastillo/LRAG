from openai import OpenAI
import textToVector
import searchVector
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def responseAssistant(history, nameDB, metric = "linalg", audio_enabled=False, k = 5, modalities = ["text", "audio"]):
    # Crear una copia de la lista para evitar modificar la original
    local_history = history.copy()
    
    DB = textToVector.loadDB(nameDB)
    
    messUser = local_history[-1]["content"]
    if type(messUser) == list:
        messUser = messUser[0]["text"]

    resultContext = searchVector.searchText(messUser, DB, k, metric)
    context = "\n".join(f"{i+1}). {item[1]['text']}" for i, item in zip(range(len(resultContext)), resultContext))
    system = f"""
    Eres un asistente de IA que responde preguntas sobre el siguiente contexto:
    {context}
    Aunque conozcas información fuera de este contexto, no la menciones. Siempre responde por audio.
    """
    if local_history[0]["role"] != "system":
        local_history.insert(0, {"role": "system", "content": system})
    else:
        preSystem = local_history[0]["content"]
        local_history[0]["content"] = preSystem + "\n\n" + system

    if audio_enabled:
        response = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=modalities,
            audio={"voice": "alloy", "format": "wav"},
            messages=local_history
        )

        return {
            "role": "assistant", 
            "content": response.choices[0].message.audio.transcript, 
            "audio": response.choices[0].message.audio.data,
            "idAudio": response.choices[0].message.audio.id,
            "context": context,
            "tokens_context": int(sum([item[1]["tokens"] for item in resultContext])*0.9),
            "tokens_input": response.usage.prompt_tokens,
            "tokens_output": response.usage.completion_tokens
        }
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=local_history,
            temperature=0
        )
        return {
            "role": "assistant", 
            "content": response.choices[0].message.content, 
            "context": context,
            "tokens_context": int(sum([item[1]["tokens"] for item in resultContext])*0.9),
            "tokens_input": response.usage.prompt_tokens,
            "tokens_output": response.usage.completion_tokens
        }

# de texto a audio
def textToAudio(text, voice = "shimmer"):
    response = client.audio.speech.create(
        model="tts-1-hd",
        input=text,
        voice=voice
    )

    return response.content
