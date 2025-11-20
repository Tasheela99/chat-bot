from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from app.models import ChatRequest, ChatResponse
from app.config import settings
from app.contexts.context_data import get_context

app = FastAPI(
    title="Government Chatbot API",
    description="Context-aware chatbot for government services",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
groq_client = Groq(api_key=settings.groq_api_key)

@app.get("/")
async def root():
    return {
        "message": "Government Chatbot API",
        "status": "active",
        "available_contexts": ["presidents_fund", "presidents_office"]
    }
    try:
        return {
            "message": "Government Chatbot API",
            "status": "active",
            "available_contexts": ["presidents_fund", "presidents_office"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contexts")
async def list_contexts():
    """List all available contexts dynamically from context files"""
    import os
    context_dir = os.path.dirname(__file__) + "/contexts"
    context_files = [
        f[:-3] for f in os.listdir(context_dir)
        if f.endswith('.py') and f not in ('__init__.py', 'context_data.py', 'default.py')
    ]
    return {
        "contexts": context_files,
        "total": len(context_files)
    }
    try:
        context_dir = os.path.dirname(__file__) + "/contexts"
        if not os.path.exists(context_dir):
            raise HTTPException(status_code=500, detail="Context directory not found.")
        context_files = [
            f[:-3] for f in os.listdir(context_dir)
            if f.endswith('.py') and f not in ('__init__.py', 'context_data.py', 'default.py')
        ]
        return {
            "contexts": context_files,
            "total": len(context_files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi import Request
from fastapi.responses import JSONResponse

@app.post("/chat", response_model=ChatResponse)
async def chat(request: Request):
    """
    Main chat endpoint
    Accepts a JSON body with 'context', 'question', optional 'conversation_history', and optional 'language'.
    """
    try:
        body = await request.json()
        context_name = body.get("context")
        question = body.get("question")
        conversation_history = body.get("conversation_history", [])
        language = body.get("language", "en")

        from app.contexts.context_data import get_context
        context_data = get_context(context_name, language=language)

        # Check for greetings and provide welcome responses
        greetings = {
            "en": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "greetings", "welcome"],
            "si": ["හායි", "හලෝ", "ආයුබෝවන්", "සුබ උදෑසනක්", "සුබ දවසක්", "සුබ සන්ධ්‍යාවක්", "නමස්කාර"],
            "ta": ["வணக்கம்", "ஹலோ", "ஹாய்", "காலை வணக்கம்", "மாலை வணக்கம்", "நமஸ்காரம்"]
        }
        
        welcome_responses = {
            "en": f"Hello! Welcome to the {context_name.replace('_', ' ').title()} information service. How can I assist you today?",
            "si": f"ආයුබෝවන්! {context_name.replace('_', ' ').title()} තොරතුරු සේවයට සාදරයෙන් පිළිගනිමු. අද මම ඔබට කෙසේ උපකාර කළ හැකිද?",
            "ta": f"வணக்கம்! {context_name.replace('_', ' ').title()} தகவல் சேवைக்கு வரவேற்கிறோம். இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?"
        }
        
        question_lower = question.lower().strip()
        if any(greeting in question_lower for greeting in greetings.get(language, greetings["en"])):
            return ChatResponse(
                answer=welcome_responses.get(language, welcome_responses["en"]),
                context_used=context_name,
                success=True
            )

        # Handle common general questions about the service
        common_questions = {
            "en": {
                "what is": "The President's Fund of Sri Lanka is a government initiative that provides financial assistance for medical treatments, particularly for kidney patients, cancer patients, children with special needs, persons with disabilities, and disaster relief beneficiaries.",
                "about": "The President's Fund helps Sri Lankan citizens access medical care by providing financial support for surgeries and treatments. Applications can be submitted through local Divisional Secretariats.",
                "help": "The President's Fund provides medical assistance for various conditions. You can apply through the website (www.presidentsfund.gov.lk), WhatsApp (0740854527), or your nearest Divisional Secretariat.",
                "services": "The President's Fund offers financial assistance for medical treatments including support for kidney patients, cancer patients, children with special needs, persons with disabilities, and disaster relief situations."
            },
            "si": {
                "what is": "ශ්‍රී ලංකා ජනාධිපති අරමුදල රජයේ මුලපිරීමක් වන අතර එය වෛද්‍ය ප්‍රතිකාර සඳහා, විශේෂයෙන් වකුගඩු රෝගීන්, පිළිකා රෝගීන්, විශේෂ අවශ්‍යතා ඇති දරුවන්, ආබාධිත පුද්ගලයන් සහ ආපදා සහන ලබන්නන් සඳහා මූල්‍ය ආධාර ලබා දෙයි.",
                "about": "ජනාධිපති අරමුදල ශ්‍රී ලාංකික පුරවැසියන්ට ශල්‍යකර්ම සහ ප්‍රතිකාර සඳහා මූල්‍ය ආධාර ලබා දීමෙන් වෛද්‍ය සේවාවන්ට ප්‍රවේශය ලබා දෙයි. ප්‍රාදේශීය ලේකම් කාර්යාල හරහා අයදුම්පත් ඉදිරිපත් කළ හැකිය.",
                "help": "ජනාධිපති අරමුදල විවිධ රෝග තත්ත්වයන් සඳහා වෛද්‍ය ආධාර ලබා දෙයි. ඔබට වෙබ් අඩවිය (www.presidentsfund.gov.lk), WhatsApp (0740854527), හෝ ආසන්නතම ප්‍රාදේශීය ලේකම් කාර්යාලය හරහා අයදුම් කළ හැකිය.",
                "services": "ජනාධිපති අරමුදල වකුගඩු රෝගීන්, පිළිකා රෝගීන්, විශේෂ අවශ්‍යතා ඇති දරුවන්, ආබාධිත පුද්ගලයන් සහ ආපදා තත්ත්වයන් සඳහා මූල්‍ය ආධාර ඇතුළුව වෛද්‍ය ප්‍රතිකාර සඳහා මූල්‍ය ආධාර ලබා දෙයි."
            },
            "ta": {
                "what is": "இலங்கை ஜனாதிபதி நிதியம் அரசாங்கத்தின் முன்முயற்சியாகும், இது மருத்துவ சிகிச்சைகளுக்கு, குறிப்பாக சிறுநீரக நோயாளிகள், புற்றுநோய் நோயாளிகள், சிறப்பு தேவைகள் உள்ள குழந்தைகள், மாற்றுத்திறனாளிகள் மற்றும் பேரிடர் நிவாரண பயனாளிகளுக்கு நிதி உதவி வழங்குகிறது.",
                "about": "ஜனாதிபதி நிதியம் இலங்கை குடிமக்களுக்கு அறுவை சிகிச்சைகள் மற்றும் சிகிச்சைகளுக்கு நிதி உதவி வழங்குவதன் மூலம் மருத்துவ பராமரிப்பை அணுக உதவுகிறது. உள்ளூர் பிரதேச செயலாளர் அலுவலகங்கள் மூலம் விண்ணப்பங்களை சமர்ப்பிக்க முடியும்.",
                "help": "ஜனாதிபதி நிதியம் பல்வேறு நிலைமைகளுக்கு மருத்துவ உதவி வழங்குகிறது. நீங்கள் இணையதளம் (www.presidentsfund.gov.lk), WhatsApp (0740854527), அல்லது அருகிலுள்ள பிரதேச செயலாளர் அலுவலகம் மூலம் விண்ணப்பிக்க முடியும்.",
                "services": "ஜனாதிபதி நிதியம் சிறுநீரக நோயாளிகள், புற்றுநோய் நோயாளிகள், சிறப்பு தேவைகள் உள்ள குழந்தைகள், மாற்றுத்திறனாளிகள் மற்றும் பேரிடர் சூழ்நிலைகளுக்கான ஆதரவு உட்பட மருத்துவ சிகிச்சைகளுக்கு நிதி உதவி வழங்குகிறது."
            }
        }
        
        # Check for common questions
        lang_questions = common_questions.get(language, common_questions["en"])
        for keyword, answer in lang_questions.items():
            if keyword in question_lower:
                return ChatResponse(
                    answer=answer,
                    context_used=context_name,
                    success=True
                )

        # Check for bad words (simple list, can be expanded)
        BAD_WORDS = [
            "fuck", "shit", "bitch", "asshole", "bastard", "damn", "piss", "dick", "cunt", "fag", "slut", "whore",
            "පිස්සෝ", "කෙල්ල", "පොන්නයා", "පකයා", "පකී", "පොන්නි", "பொன்னையா", "பக்கியா", "பொன்னி", "பக்கி"
        ]
        if any(bad_word in question.lower() for bad_word in BAD_WORDS):
            return JSONResponse(
                status_code=400,
                content={
                    "answer": "",
                    "context_used": context_name,
                    "success": False,
                    "error": "Inappropriate language detected."
                }
            )

        # Try FAQ answer if available, but enforce question language matches selected language
        faq_answer = None
        import re
        def is_sinhala(text):
            return bool(re.search(r"[\u0D80-\u0DFF]", text))
        def is_tamil(text):
            return bool(re.search(r"[\u0B80-\u0BFF]", text))
        def is_english(text):
            return bool(re.search(r"[A-Za-z]", text))

        # Language check logic
        from fastapi import status
        from fastapi.responses import JSONResponse
        if language == "en" and not is_english(question):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "answer": "Please ask your question in English.",
                    "context_used": context_name,
                    "success": False,
                    "error": "Question language does not match selected language."
                }
            )
        if language == "si" and not is_sinhala(question):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "answer": "කරුණාකර ඔබේ ප්‍රශ්නය සිංහලෙන් ඉදිරිපත් කරන්න.",
                    "context_used": context_name,
                    "success": False,
                    "error": "Question language does not match selected language."
                }
            )
        if language == "ta" and not is_tamil(question):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "answer": "தயவுசெய்து உங்கள் கேள்வியை தமிழில் கேளுங்கள்.",
                    "context_used": context_name,
                    "success": False,
                    "error": "Question language does not match selected language."
                }
            )

        try:
            import importlib
            context_mod_name = f"app.contexts.{context_name}{'_' + language if language != 'en' else ''}"
            context_mod = importlib.import_module(context_mod_name)
            if hasattr(context_mod, 'get_faq_answer'):
                faq_answer = context_mod.get_faq_answer(question)
        except Exception:
            pass
        if faq_answer and not faq_answer.startswith("Sorry"):
            return ChatResponse(
                answer=faq_answer,
                context_used=context_name,
                success=True
            )
        if faq_answer and faq_answer.startswith("Sorry"):
            hotline = {
                "en": "Please call the President's Fund hotline at +94-11-2354354 for further assistance.",
                "si": "කරුණාකර වැඩිදුර උපදෙස් සඳහා ජනාධිපති අරමුදලේ හොට්ලයින් +94-11-2354354 අමතන්න.",
                "ta": "மேலும் உதவிக்கு ஜனாதிபதி நிதி ஹாட்லைன் +94-11-2354354 ஐ அழைக்கவும்."
            }
            return ChatResponse(
                answer=hotline.get(language, hotline["en"]),
                context_used=context_name,
                success=False,
                error="Question not found in FAQ."
            )

        # Build the messages for Groq
        messages = [
            {
                "role": "system",
                "content": f"{context_data['system_prompt']}\n\nContext Information:\n{context_data['context_info']}"
            }
        ]
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({
            "role": "user",
            "content": question
        })
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model=settings.groq_model,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False
        )
        answer = chat_completion.choices[0].message.content
        return ChatResponse(
            answer=answer,
            context_used=context_name,
            success=True
        )
    except Exception as e:
        return ChatResponse(
            answer="",
            context_used=body.get("context", ""),
            success=False,
            error=str(e)
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "government-chatbot-api"}
    try:
        return {"status": "healthy", "service": "government-chatbot-api"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)