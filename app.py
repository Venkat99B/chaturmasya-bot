import os
import gradio as gr
from google.genai import client
from google.genai import types
from google.colab import userdata

try:
    api_key = userdata.get('GEMINI_API_KEY')
    ai = client.Client(api_key=api_key)
except Exception as e:
    print("Error: Make sure GEMINI_API_KEY is active in your Colab Secrets.")

with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    knowledge_base = f.read()

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

def respond(user_message, chat_history):
    if not user_message or not user_message.strip():
        return "", chat_history
    
    try:
        response = ai.models.generate_content(
            model='gemini-3.6-flash',
            contents=user_message,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        bot_message = response.text
    except Exception as e:
        bot_message = f"An error occurred: {str(e)}"
    
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": bot_message})
    return "", chat_history

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
        "labels": ["⏰ पूजेची वेळ", "🍲 प्रसाद वेळ", "🏨 रूम बुकिंग माहिती", "📍 दर्शन प्रेक्षणीय स्थळे", "🛺 ऑटो रिक्षा चालक", "🚕 टॅक्सी ड्रायव्हर्स"],
        "queries": ["पूजा आणि दर्शनाची अचूक वेळ काय आहे?", "तीर्थ प्रसादाची वेळ काय आहे?", "रूम बुकिंगचे शुल्क आणि जवळचे हॉटेल्स काय आहेत?", "मठाच्या जवळ कोणती दर्शन घेण्यासारखी मंदिरे आहेत?", "स्थानिक प्रवासासाठी ऑटो ड्रायव्हर्सचे phone नंबर द्या", "दूरच्या प्रवासासाठी टॅक्सी चालकांचे संपर्क क्रमांक द्या"]
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

with gr.Blocks(title="Chaturmasya Assistant") as demo:
    gr.Markdown("# 🪔 Shri Uttaradi Math Chaturmasya Assistant")
    
    lang_dropdown = gr.Dropdown(
        choices=list(LANGUAGE_DATA.keys()), 
        value="ಕನ್ನಡ (Kannada)", 
        label="🔤 Choose Your Language / ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ"
    )
    
    gr.Markdown("---")
    
    # FIXED: Added index numbers [0] to [5] so each button renders its individual string label uniquely
    with gr.Row():
        btn0 = gr.Button(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["labels"][0])
        btn1 = gr.Button(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["labels"][1])
        btn2 = gr.Button(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["labels"][2])
    with gr.Row():
        btn3 = gr.Button(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["labels"][3])
        btn4 = gr.Button(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["labels"][4])
        btn5 = gr.Button(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["labels"][5])
        
    chatbot = gr.Chatbot(label="Chat History / ಸಂಭಾಷಣೆ ವಿವರಗಳು")
    msg = gr.Textbox(label="Type your custom question here / ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ")
    clear = gr.ClearButton([msg, chatbot])
    
    # Map index numbers to hidden tracking state arrays
    q0 = gr.State(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["queries"][0])
    q1 = gr.State(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["queries"][1])
    q2 = gr.State(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["queries"][2])
    q3 = gr.State(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["queries"][3])
    q4 = gr.State(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["queries"][4])
    q5 = gr.State(LANGUAGE_DATA["ಕನ್ನಡ (Kannada)"]["queries"][5])

    # FIXED: Group updates so language swapping updates button items independently by index
    def update_language(selected_lang):
        data = LANGUAGE_DATA[selected_lang]
        return [
            gr.update(value=data["labels"][0]), gr.update(value=data["labels"][1]), gr.update(value=data["labels"][2]),
            gr.update(value=data["labels"][3]), gr.update(value=data["labels"][4]), gr.update(value=data["labels"][5]),
            data["queries"][0], data["queries"][1], data["queries"][2],
            data["queries"][3], data["queries"][4], data["queries"][5]
        ]
        
    lang_dropdown.change(
        fn=update_language, 
        inputs=lang_dropdown, 
        outputs=[btn0, btn1, btn2, btn3, btn4, btn5, q0, q1, q2, q3, q4, q5]
    )
    
    btn0.click(fn=respond, inputs=[q0, chatbot], outputs=[msg, chatbot])
    btn1.click(fn=respond, inputs=[q1, chatbot], outputs=[msg, chatbot])
    btn2.click(fn=respond, inputs=[q2, chatbot], outputs=[msg, chatbot])
    btn3.click(fn=respond, inputs=[q3, chatbot], outputs=[msg, chatbot])
    btn4.click(fn=respond, inputs=[q4, chatbot], outputs=[msg, chatbot])
    btn5.click(fn=respond, inputs=[q5, chatbot], outputs=[msg, chatbot])
    
    msg.submit(fn=respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

demo.launch(theme=gr.themes.Soft(), share=True, debug=True)
