# RAG Ligero

RAG Ligero es un sistema de recuperación de información y generación de respuestas utilizando modelos de lenguaje avanzados. Este proyecto está diseñado para integrar capacidades de búsqueda vectorial y generación de texto en aplicaciones web.

## Características

- **Búsqueda Vectorial**: Utiliza diferentes métricas (linalg, cosine, jaccard, hamming) para buscar textos similares en una base de datos vectorial.
- **Generación de Respuestas**: Genera respuestas contextuales basadas en un historial de conversación y un contexto proporcionado.
- **Integración de Audio**: Convierte texto a audio utilizando modelos de síntesis de voz.
- **API REST**: Proporciona una API RESTful para interactuar con el sistema.

README.md: Este archivo proporciona una descripción general del proyecto "RAG Ligero". Detalla las características principales del sistema, como la búsqueda vectorial, la generación de respuestas, la integración de audio y la API REST. También incluye instrucciones para la instalación y el uso del sistema.
textToVector.py: Este archivo contiene funciones para convertir texto en vectores utilizando modelos de OpenAI. Incluye la gestión de archivos JSON para almacenar y recuperar datos vectoriales, así como la generación de cadenas aleatorias para nombrar archivos.
searchVector.py: Este archivo implementa funciones para buscar texto en una base de datos vectorial utilizando diferentes métricas de similitud, como linalg, coseno, jaccard y hamming. Cada función de métrica calcula la distancia entre vectores y devuelve los resultados más cercanos.
formatText.py: Este archivo contiene funciones para formatear texto. Incluye la unión de textos cortos, la división de textos largos en fragmentos más pequeños y el formateo de texto utilizando marcadores específicos.
rag.py: Este archivo define funciones para generar respuestas de un asistente de IA utilizando un historial de conversación y un contexto recuperado de una base de datos vectorial. También incluye funciones para convertir texto a audio utilizando modelos de síntesis de voz de OpenAI.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/AngeloCastillo/RAG.git
   cd LRAG
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las credenciales de OpenAI en el archivo `textToVector.py` y `rag.py`.

## Uso

### Iniciar el Servidor

Para iniciar el servidor FastAPI, ejecuta:
