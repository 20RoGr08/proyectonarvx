import streamlit as st
from google import genai

# Configuración de la interfaz web
st.set_page_config(page_title="Mi Asistente IA", page_icon="🤖", layout="centered")

st.title("🤖 Mi Asistente Personal con Gemini")
st.write("Pregúntame sobre código, cálculo, ciberseguridad o lo que necesites.")

# Leer la API Key de forma segura desde el archivo secrets.toml
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

SYSTEM_INSTRUCTION = (
    "Eres un asistente técnico ultra eficiente. "
    "Responde de forma extremadamente directa, concisa y ve directo al grano. "
    "Evita saludos largos, introducciones y explicaciones innecesarias. "
    "Entrega únicamente la información precisa, fórmulas o código limpio."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                # Usamos los modelos más recientes de la familia Flash
                modelos_a_probar = ["gemini-3.5-flash", "gemini-3.6-flash", "gemini-2.5-flash"]
                respuesta_exitosa = None
                
                for modelo in modelos_a_probar:
                    try:
                        response = client.models.generate_content(
                            model=modelo,
                            contents=prompt,
                            config={"system_instruction": SYSTEM_INSTRUCTION}
                        )
                        respuesta_exitosa = response.text
                        break # Si responde con éxito, salimos del ciclo
                    except Exception:
                        continue # Si falla, intenta con el siguiente modelo automáticamente
                
                if respuesta_exitosa:
                    st.markdown(respuesta_exitosa)
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_exitosa})
                else:
                    st.error("Los servidores están experimentando una alta demanda temporal. Por favor, espera un segundo y vuelve a enviarlo.")
                    
            except Exception as e:
                st.error(f"Ocurrió un error de conexión: {str(e)}")