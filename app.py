import os
import streamlit as str_ui
from groq import Groq

# 1. Page Configuration
str_ui.set_page_config(page_title="Chaturmasya Assistant", page_icon="🪔", layout="centered")

# 2. Securely Initialize Groq Client
@str_ui.cache_resource
def get_groq_client():
    try:
        api_key = str_ui.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = os.environ.get("GROQ_API_KEY")
        
    if not api_key:
        str_ui.error("API Key missing! Please add GROQ_API_KEY to Streamlit Secrets.")
    return Groq(api_key=api_key)

groq_client = get_groq_client()

# 3. Read Local Knowledge Base Text
try:
    with open("knowledge_base.txt", "r", encoding="utf-8") as f:
        knowledge_base = f.read()
except FileNotFoundError:
    knowledge_base = "Event details: Shri Uttaradi Math Chaturmasya festival updates."

SYSTEM_PROMPT = f"""
You are an expert, humble, and polite AI volunteer assistant for the Shri Uttaradi Math Chaturmasya festival.
Your goal is to assist devotees (especially elders) with their queries regarding schedules, local travel, transport contacts, accommodations, and visiting kshetras.

CRITICAL RULES:
1. ALWAYS respond in the exact same language the user uses to ask their question (Kannada, Telugu, Tamil, Marathi, or English).
2. Use respectful, traditional language appropriate for a math environment.
3. Base your answers strictly on the provided Chaturmasya Event Knowledge Base below. Always provide full driver names, taxi numbers, hotel rates, and distances clearly.
4. Keep answers highly structured and clean for older citizens. Use bold text and bullet points for phone numbers and distances.

Chaturmasya Event Knowledge Base:
{knowledge_base}
"""

# 4. Multilingual Options Mapping
LANGUAGE_DATA = {
    "ಕನ್ನಡ (Kannada)": {
        "labels": ["⏰ ಪೂಜಾ ಸಮಯಗಳು", "🍲 ಪ್ರಸಾದದ ಸಮಯ", "🏨 ರೂಮ್ ಬುಕಿಂಗ್", "📍 ಪ್ರೇಕ್ಷಣೀಯ ಸ್ಥಳಗಳು", "🛺 ಆಟೋ ಚಾಲಕರು", "🚕 ಟ್ಯಾಕ್ಸಿ ಸೇವೆಗಳು"],
        "queries": ["ಪೂಜೆ ಮತ್ತು ದರ್ಶನದ ಸಮಯಗಳು ಯಾವುವು?", "ತೀರ್ಥ ಪ್ರಸಾದದ ಸಮಯ ಯಾವಾಗ?", "ರೂಮ್ ಬುಕಿಂಗ್ ಮತ್ತು ಹತ್ತಿರದ ಹೋಟೆಲ್ ವಿವರಗಳು ಬೇಕು", "ಮಠದ ಸುತ್ತಮುತ್ತ ನೋಡಬೇಕಾದ ದೇವಸ್ಥಾನಗಳು ಯಾವುವು?", "ಸ್ಥಳೀಯ ಪ್ರಯಾಣಕ್ಕಾಗಿ ಆಟೋ ಚಾಲಕರ ಫೋನ್ ನಂಬರ್ ಕೊಡಿ", "ದೂರದ ಪ್ರಯಾಣಕ್ಕಾಗಿ ಟ್ಯಾಕ್ಸಿ ಡ್ರೈವರ್ಗಳ ಫೋನ್ ನಂಬರ್ ಕೊಡಿ"]
    },
    "తెలుగు (Telugu)": {
        "labels": ["⏰ పూజా సమయాలు", "🍲 ప్రసాదం సమయం", "🏨 రూమ్ బుకింగ్", "📍 సందర్శన స్థలాలు", "🛺 ఆటో డ్రైవర్లు", "🚕 టాక్సీ సర్వీస్"],
        "queries": ["పూజ మరియు దర్శనం సమయాలు ఏమిటి?", "తీర్థ ప్రసాదం భోజన సమయాలు ఎప్పుడు?", "రూమ్ బుకింగ్ ధరలు మరియు హోటల్ వివరాలు ఏమిటి?", "మఠం చుట్టుపక్కల సందర్శించవలసిన పుణ్యక్షేత్రాలు ఏమిటి?", "స్థానిక ప్రయాణానికి ఆటో డ్రైవర్ల ఫోన్ నెంబర్లు ఇవ్వండి", "దూర ప్రయాణాలకు టాక్సీ డ్రైవర్ల ఫోన్ నెంబర్లు ఇవ్వండి"]
    },
    "मराठी (Marathi)": {
        "labels": ["⏰ पूजेची वेळ", "🍲 प्रसाद वेळ", "🏨 रूम बुकिंग माहिती", "📍 दर्शन प्रेक्षणीय स्थळे", "🛺 ऑटो रिक्षा चालक", "🚕 टॅक्सी चालकांचे संपर्क क्रमांक"],
        "queries": ["पूजा आणि दर्शनाची अचूक वेळ काय आहे?", "तीर्थ प्रसाद वेळ काय आहे?", "रूಮ್ बुकिंगचे शुल्क आणि जवळचे हॉटेल्स काय आहेत?", "मठाच्या जवळ कोणती दर्शन घेण्यासारखी मंदिरे आहेत?", "स्थानिक प्रवासासाठी ऑटो ด್ರಾಯ್ವರ್ಸ್ಚೆ ಫೋನ್ ನಂಬರ್ ದ್ಯಾ", "दूरच्या प्रवासासाठी टॅक्सी चालकांचे संपर्क क्रमांक द्या"]
    },
    "தமிழ் (Tamil)": {
        "labels": ["⏰ பூஜை நேரங்கள்", "🍲 பிரசாத நேரம்", "🏨 அறை முன்பதிவு", "📍 ஆன்மீக இடங்கள்", "🛺 ஆட்டோ எண்கள்", "🚕 டாக்ஸி எண்கள்"],
        "queries": ["பூஜை மற்றும் தரிசன நேரங்கள் என்ன?", "தீர்த்த பிரசாதம் வழங்கப்படும் நேரம் என்ன?", "அறை முன்பதிவு கட்டணம் மற்றும் தங்கும் விடுதிகள் என்ன?", "மடத்தைச் சுற்றி பார்க்க வேண்டிய ஆன்மீகத் தலங்கள் யாவை?", "உள்ளூர் பயணத்திற்கு ஆட்டோ டிரைவர் போன் எண்கள் கொடுங்கள்", "வெளியூர் பயணத்திற்கு டாக்ஸி சர்வீஸ் போன் எண்கள் கொடுங்கள்"]
    },
    "English": {
        "labels": ["⏰ Pooja Timings", "🍲 Teertha Prasada", "🏨 Room Booking", "📍 Places to Visit", "🛺 Auto Drivers", "🚕 Taxi Services"],
        "queries": ["What are the exact Pooja and Darshana timings today?", "What are the Teertha Prasada lunch hours?", "What is the price and process for hotel/room booking?", "What are the sightseeing temples to visit in and around Dharwad?", "Give me the phone numbers of local auto drivers", "Give me the contact details of taxi services for long distance travel"]
    }
}

str_ui.markdown("# 🪔 Shri Uttaradi Math Chaturmasya Assistant")

selected_lang = str_ui.selectbox("🔤 Choose Your Language / ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", list(LANGUAGE_DATA.keys()))
data = LANGUAGE_DATA[selected_lang]

if "messages" not in str_ui.session_state:
    str_ui.session_state.messages = []

for msg in str_ui.session_state.messages:
    with str_ui.chat_message(msg["role"]):
        str_ui.write(msg["content"])

def process_query(user_query):
    with str_ui.chat_message("user"):
        str_ui.write(user_query)
    str_ui.session_state.messages.append({"role": "user", "content": user_query})
    
    with str_ui.chat_message("assistant"):
        with str_ui.spinner("Thinking..."):
            try:
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_query}
                    ],
                    model="llama-3.1-70b-versatile",
                )
                bot_message = chat_completion.choices.message.content
            except Exception as e:
                bot_message = f"API Error detail: {str(e)}"
            str_ui.write(bot_message)
    str_ui.session_state.messages.append({"role": "assistant", "content": bot_message})

str_ui.markdown("### ⚡ Quick Options / ಸುಲಭ ಆಯ್ಕೆಗಳು")

# FIXED: Explicit row tracking indices [0] to [5] applied perfectly to ensure unique button mapping
col1, col2 = str_ui.columns(2)
with col1:
    if str_ui.button(data["labels"][0], use_container_width=True):
        process_query(data["queries"][0])
    if str_ui.button(data["labels"][1], use_container_width=True):
        process_query(data["queries"][1])
    if str_ui.button(data["labels"][2], use_container_width=True):
        process_query(data["queries"][2])

with col2:
    if str_ui.button(data["labels"][3], use_container_width=True):
        process_query(data["queries"][3])
    if str_ui.button(data["labels"][4], use_container_width=True):
        process_query(data["queries"][4])
    if str_ui.button(data["labels"][5], use_container_width=True):
        process_query(data["queries"][5])

str_ui.markdown("---")

if custom_input := str_ui.chat_input("Or type your custom question here..."):
    process_query(custom_input)
