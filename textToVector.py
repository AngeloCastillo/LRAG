import os
from openai import OpenAI
import formatText
import json
import random
import string
import PyPDF2

# Obtener la clave de la API desde una variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Verificar si la clave de la API está configurada
if not api_key:
    raise ValueError("La clave de la API de OpenAI no está configurada. Establece la variable de entorno 'OPENAI_API_KEY'.")

client = OpenAI(api_key=api_key)

models = ["text-embedding-3-small", "text-embedding-3-large"]

# generar un strgin aleatorio alfanumerico con un parametro de longitud
def randomString(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def loadDB(path):
    if ".json" not in path:
        path = path + ".json"
    if "DBs/" not in path:
        path = "DBs/" + path
    if not os.path.exists(path):
        return []
    with open(path, "r") as file:
        return json.load(file)
    
def saveDB(path, data):
    # si el archivo existe, lo lee y actualiza
    if ".json" not in path:
        path = path + ".json"
    if "DBs/" not in path:
        path = "DBs/" + path
    if os.path.exists(path):
        with open(path, "r") as file:
            existing_data = json.load(file)
        
        # Verifica si el contenido existente es una lista
        if isinstance(existing_data, list):
            if isinstance(data, list):
                existing_data.extend(data)  # Agrega cada elemento de la nueva lista
            else:
                existing_data.append(data)  # Agrega el nuevo diccionario
        else:
            raise ValueError("El contenido del archivo no es una lista.")
        
        with open(path, "w") as file:
            json.dump(existing_data, file, indent=4)
    else:
        # Si el archivo no existe, crea uno nuevo
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

def textToVector(text, model = "text-embedding-3-small"):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding, response.usage.total_tokens

def textToDBVector(listText = [], fileText=None, model="text-embedding-3-small", name="DB", nameRandom=True, withMarker=False, marker="##"):
    # Si se proporciona un archivo de texto o PDF, se procesa primero
    if fileText:
        if fileText.endswith(".txt"):
            isPath = True
            nameFile = fileText.replace(".txt", "")
            nameFile = nameFile[nameFile.rfind("/")+1:].upper()
            fileText = open(fileText, encoding="utf8").read()
        elif fileText.lower().endswith(".pdf"):
            isPath = True
            nameFile = fileText.replace(".pdf", "")
            nameFile = nameFile[nameFile.rfind("/")+1:].upper()
            with open(fileText, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                fileText = ""
                for page in reader.pages:
                    fileText += page.extract_text()
        if withMarker:
            listText = formatText.formatTextMarker(fileText, marker)
        else:
            listText = formatText.formatText(fileText, name)
        

    DB = []
    for text in listText:
        vector, tokens = textToVector(text, model)
        if fileText:
            text = f"{nameFile}\n\n{text}"

        DB.append({"text": text, "vector": vector, "tokens": tokens, "length": len(text)})

    if nameRandom:
        name = name + "_" + randomString(16)

    # guardar en un archivo json
    saveDB(name + ".json", DB)
    return name

