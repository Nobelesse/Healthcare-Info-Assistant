"""UI labels: the selected language is also passed to Ollama."""
LABELS = {
    "en": {
        "home": "Dashboard", "chat": "AI Health Assistant", "reports": "Report Analyzer", "voice": "Voice Assistant",
        "history": "My History", "insights": "Health Insights", "profile": "My Profile", "about": "About Project",
        "overview": "Overview", "users": "Users", "admin_reports": "All Reports", "conversations": "Conversations", "audit": "Audit Log",
        "logout": "Sign out", "language": "Language", "theme": "Light mode", "online": "Ollama online",
        "offline": "Ollama not ready", "caution": "Educational guidance only — not a medical diagnosis.",
        "welcome": "Welcome back", "ask": "Ask a medical question", "upload": "Analyze report",
        "talk": "Speak to AI", "saved": "Saved successfully.", "nothing": "No records yet.",
    },
    "hi": {
        "home": "डैशबोर्ड", "chat": "AI स्वास्थ्य सहायक", "reports": "रिपोर्ट विश्लेषण", "voice": "वॉइस सहायक",
        "history": "मेरा इतिहास", "insights": "स्वास्थ्य जानकारी", "profile": "मेरी प्रोफ़ाइल", "about": "प्रोजेक्ट के बारे में",
        "overview": "अवलोकन", "users": "उपयोगकर्ता", "admin_reports": "सभी रिपोर्ट", "conversations": "बातचीत", "audit": "ऑडिट लॉग",
        "logout": "साइन आउट", "language": "भाषा", "theme": "लाइट मोड", "online": "Ollama ऑनलाइन",
        "offline": "Ollama तैयार नहीं", "caution": "केवल जानकारी के लिए — यह चिकित्सकीय निदान नहीं है।",
        "welcome": "वापसी पर स्वागत है", "ask": "स्वास्थ्य से जुड़ा सवाल पूछें", "upload": "रिपोर्ट का विश्लेषण करें",
        "talk": "AI से बात करें", "saved": "सफलतापूर्वक सहेजा गया।", "nothing": "अभी कोई रिकॉर्ड नहीं है।",
    },
}


def t(key, language="en"):
    return LABELS.get(language, LABELS["en"]).get(key, key)
