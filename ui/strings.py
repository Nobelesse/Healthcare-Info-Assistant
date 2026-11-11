"""Curated UI strings and optional on-device translation packs.

The original four locales are complete. Additional languages have curated core
labels, with English fallback until a local translation pack is generated.
Neither project name nor user-provided content is automatically translated.
"""

LANGUAGES = {
    'en': 'English',
    'hi': 'हिन्दी',
    'mr': 'मराठी',
    'es': 'Español',
}
VOICE_LOCALES = {'en': 'en-IN', 'hi': 'hi-IN', 'mr': 'mr-IN', 'es': 'es-ES'}

# All entries: English, Hindi, Marathi, Spanish. Project name is intentionally unchanged.
C = {
'home': ('Dashboard','डैशबोर्ड','डॅशबोर्ड','Panel principal'),
'chat': ('AI Health Assistant','एआई स्वास्थ्य सहायक','एआय आरोग्य सहाय्यक','Asistente de salud con IA'),
'reports': ('Report Analyzer','रिपोर्ट विश्लेषक','अहवाल विश्लेषक','Analizador de informes'),
'voice': ('Voice Assistant','आवाज़ सहायक','आवाज सहाय्यक','Asistente de voz'),
'history': ('My History','मेरा इतिहास','माझा इतिहास','Mi historial'),
'insights': ('Health Insights','स्वास्थ्य जानकारी','आरोग्य माहिती','Indicadores de salud'),
'profile': ('My Profile','मेरी प्रोफ़ाइल','माझे प्रोफाइल','Mi perfil'),
'about': ('About Project','परियोजना के बारे में','प्रकल्पाविषयी','Acerca del proyecto'),
'overview': ('Overview','अवलोकन','आढावा','Resumen'),
'users': ('Users','उपयोगकर्ता','वापरकर्ते','Usuarios'),
'admin_reports': ('All Reports','सभी रिपोर्ट','सर्व अहवाल','Todos los informes'),
'conversations': ('Conversations','बातचीत','संभाषणे','Conversaciones'),
'audit': ('Access Log','पहुँच का रिकॉर्ड','प्रवेश नोंद','Registro de acceso'),
'logout': ('Sign out','साइन आउट करें','बाहेर पडा','Cerrar sesión'),
'caution': ('For education only — not a medical diagnosis.','केवल शैक्षिक जानकारी — यह चिकित्सा निदान नहीं है।','फक्त शैक्षणिक माहिती — हे वैद्यकीय निदान नाही.','Solo información educativa; no es un diagnóstico médico.'),
'emergency': ('For urgent symptoms, contact emergency services immediately.','गंभीर लक्षण होने पर तुरंत आपातकालीन सेवाओं से संपर्क करें।','गंभीर लक्षणांसाठी तात्काळ आपत्कालीन सेवांना संपर्क करा.','Ante síntomas urgentes, contacte inmediatamente a emergencias.'),
'sidebar_user_portal': ('USER PORTAL','उपयोगकर्ता पोर्टल','वापरकर्ता विभाग','PORTAL DE USUARIOS'),
'sidebar_user_portal_help': ('Your private healthcare space','आपका व्यक्तिगत स्वास्थ्य खाता','तुमचे वैयक्तिक आरोग्य खाते','Tu espacio de salud personal'),
'sidebar_admin_portal': ('ADMIN PORTAL','प्रशासक पोर्टल','प्रशासक विभाग','PORTAL DE ADMINISTRACIÓN'),
'sidebar_admin_portal_help': ('Authorized management access','केवल अधिकृत प्रबंधन के लिए','फक्त अधिकृत व्यवस्थापनासाठी','Acceso de gestión autorizado'),
'sidebar_project': ('PROJECT','परियोजना','प्रकल्प','PROYECTO'),
'sidebar_project_help': ('What this assistant does','यह सहायक क्या करता है','हा सहाय्यक काय करतो','Qué hace este asistente'),
'sidebar_preferences': ('LANGUAGE & APPEARANCE','भाषा और रूप-रंग','भाषा आणि स्वरूप','IDIOMA Y APARIENCIA'),
'sidebar_preferences_help': ('Personalize your experience','अपनी पसंद तय करें','तुमच्या आवडीनुसार निवडा','Personaliza tu experiencia'),
'sidebar_light_theme': ('Light theme','हल्की थीम','प्रकाश थीम','Tema claro'),
'sidebar_workspace': ('YOUR DASHBOARD','आपका डैशबोर्ड','तुमचा डॅशबोर्ड','TU PANEL'),
'sidebar_workspace_help': ('Your healthspace overview','आपके स्वास्थ्य खाते का सार','आरोग्य खात्याचा आढावा','Resumen de tu espacio de salud'),
'sidebar_assistance': ('AI HEALTH TOOLS','एआई स्वास्थ्य सुविधाएँ','एआय आरोग्य साधने','HERRAMIENTAS DE SALUD'),
'sidebar_assistance_help': ('Ask, analyze or speak','पूछें, विश्लेषण करें या बोलें','विचारा, विश्लेषण करा किंवा बोला','Pregunta, analiza o habla'),
'sidebar_your_health': ('YOUR HEALTHSPACE','आपका स्वास्थ्य खाता','तुमचे आरोग्य खाते','TU ESPACIO DE SALUD'),
'sidebar_your_health_help': ('Private history and settings','निजी इतिहास और सेटिंग','खाजगी इतिहास आणि सेटिंग्ज','Historial y ajustes privados'),
'sidebar_admin_dashboard': ('ADMIN DASHBOARD','प्रशासक डैशबोर्ड','प्रशासक डॅशबोर्ड','PANEL DE ADMINISTRACIÓN'),
'sidebar_admin_dashboard_help': ('Platform activity','प्लेटफ़ॉर्म की गतिविधि','प्रणालीवरील हालचाल','Actividad de la plataforma'),
'sidebar_management': ('ACCOUNT MANAGEMENT','खाता प्रबंधन','खाते व्यवस्थापन','GESTIÓN DE CUENTAS'),
'sidebar_management_help': ('Users, reports and conversations','उपयोगकर्ता, रिपोर्ट और बातचीत','वापरकर्ते, अहवाल आणि संभाषणे','Usuarios, informes y conversaciones'),
'sidebar_privacy': ('PRIVACY & SECURITY','गोपनीयता और सुरक्षा','गोपनीयता आणि सुरक्षा','PRIVACIDAD Y SEGURIDAD'),
'sidebar_privacy_help': ('Review recorded access','दर्ज पहुँच की जाँच करें','नोंदवलेला प्रवेश तपासा','Consulta los accesos registrados'),
'sidebar_language_label': ('Interface language','इंटरफ़ेस की भाषा','इंटरफेसची भाषा','Idioma de la interfaz'),
'guest_user_login': ('User Login','उपयोगकर्ता लॉगिन','वापरकर्ता लॉगिन','Iniciar sesión'),
'guest_register': ('Create User Account','नया खाता बनाएँ','नवीन खाते तयार करा','Crear una cuenta'),
'guest_admin_login': ('Admin Login','प्रशासक लॉगिन','प्रशासक लॉगिन','Acceso de administrador'),
'guest_user_login_desc': ('Sign in securely to your personal healthspace.','अपने स्वास्थ्य खाते में सुरक्षित प्रवेश करें।','तुमच्या आरोग्य खात्यात सुरक्षित प्रवेश करा.','Entra de forma segura en tu espacio de salud.'),
'guest_register_desc': ('Create an account to ask questions and analyze medical reports.','स्वास्थ्य सवाल पूछने और रिपोर्ट समझने के लिए खाता बनाएँ।','आरोग्य प्रश्न विचारण्यासाठी आणि अहवाल समजून घेण्यासाठी खाते तयार करा.','Crea una cuenta para consultar y analizar informes médicos.'),
'guest_admin_login_desc': ('Restricted access for the permanent system administrator.','स्थायी प्रणाली प्रशासक के लिए सीमित प्रवेश।','कायमस्वरूपी प्रणाली प्रशासकासाठी मर्यादित प्रवेश.','Acceso restringido al administrador permanente.'),
'guest_welcome_line': ('Your health questions, clearly explained.','आपके स्वास्थ्य सवालों के आसान जवाब।','तुमच्या आरोग्य प्रश्नांची सोपी उत्तरे.','Tus dudas de salud, explicadas con claridad.'),
'guest_welcome_desc': ('Understand conditions and lab tests in your language using local AI.','स्थानीय एआई से अपनी भाषा में बीमारियाँ और जाँच समझें।','स्थानिक एआय वापरून आपल्या भाषेत आजार व चाचण्या समजून घ्या.','Comprende condiciones y análisis con IA local en tu idioma.'),
'field_username': ('Username','उपयोगकर्ता नाम','वापरकर्तानाव','Nombre de usuario'),
'field_password': ('Password','पासवर्ड','पासवर्ड','Contraseña'),
'field_full_name': ('Full name','पूरा नाम','पूर्ण नाव','Nombre completo'),
'field_choose_username': ('Choose a username','उपयोगकर्ता नाम चुनें','वापरकर्तानाव निवडा','Elige un usuario'),
'field_email': ('Email address','ईमेल पता','ईमेल पत्ता','Correo electrónico'),
'field_new_password': ('Password (10+ characters, letters and numbers)','पासवर्ड (कम से कम 10 वर्ण, अक्षर और अंक)','पासवर्ड (किमान १० वर्ण, अक्षरे व अंक)','Contraseña (10+ caracteres, letras y números)'),
'field_confirm_password': ('Confirm password','पासवर्ड की पुष्टि करें','पासवर्डची पुष्टी करा','Confirma la contraseña'),
'field_preferred_language': ('Preferred language','पसंदीदा भाषा','पसंतीची भाषा','Idioma preferido'),
'field_consent': ("I consent to the permanent administrator 'Mr. Doc' accessing my stored account details, extracted medical report text, AI responses and conversation history. This is educational software, not confidential clinical care.","मैं सहमत हूँ कि स्थायी प्रशासक 'Mr. Doc' मेरे खाते का विवरण, सहेजे गए मेडिकल रिपोर्ट का पाठ, एआई उत्तर और बातचीत का इतिहास देख सकते हैं। यह केवल शैक्षिक ऐप है, गोपनीय चिकित्सकीय सेवा नहीं।","कायमस्वरूपी प्रशासक 'Mr. Doc' माझ्या खात्याची माहिती, वैद्यकीय अहवालातील मजकूर, एआय उत्तरे आणि संभाषणांचा इतिहास पाहू शकतात, यास मी संमती देतो/देते. हे शैक्षणिक सॉफ्टवेअर आहे, गोपनीय वैद्यकीय सेवा नाही.","Doy mi consentimiento para que el administrador permanente 'Mr. Doc' acceda a los datos de mi cuenta, textos de informes, respuestas de IA e historial. Esta aplicación es educativa, no una atención clínica confidencial."),
'consent_intro': ('Please review the consent checkbox. The administrator can access your stored health information.','सहमति ध्यान से पढ़ें। प्रशासक आपकी सहेजी गई स्वास्थ्य जानकारी देख सकते हैं।','संमती काळजीपूर्वक वाचा. प्रशासक तुमची जतन केलेली आरोग्य माहिती पाहू शकतात.','Lee el consentimiento: el administrador puede acceder a tus datos de salud guardados.'),
'field_admin_password': ('Administrator password','प्रशासक पासवर्ड','प्रशासक पासवर्ड','Contraseña de administración'),
'admin_login_intro': ('Permanent administrator: **{username}**. Public administrator registration is disabled.','स्थायी प्रशासक: **{username}**। सार्वजनिक प्रशासक पंजीकरण बंद है।','कायमस्वरूपी प्रशासक: **{username}**. सार्वजनिक प्रशासक नोंदणी बंद आहे.','Administrador permanente: **{username}**. No se permite registrar administradores.'),
'admin_setup_warning': ('Administrator not initialized. Set ADMIN_INITIAL_PASSWORD in .env, run `python -m scripts.init_admin`, then restart.','प्रशासक तैयार नहीं है। .env में ADMIN_INITIAL_PASSWORD सेट करें, `python -m scripts.init_admin` चलाएँ और फिर से शुरू करें।','प्रशासक तयार नाही. .env मध्ये ADMIN_INITIAL_PASSWORD सेट करा, `python -m scripts.init_admin` चालवा आणि पुन्हा सुरू करा.','Administrador no inicializado. Define ADMIN_INITIAL_PASSWORD en .env, ejecuta `python -m scripts.init_admin` y reinicia.'),
'admin_setup_invalid': ('Invalid administrator configuration','अमान्य प्रशासक कॉन्फ़िगरेशन','अवैध प्रशासक संरचना','Configuración de administrador no válida'),
'action_sign_in': ('Sign in securely','सुरक्षित प्रवेश करें','सुरक्षित प्रवेश करा','Iniciar sesión de forma segura'),
'action_create_account': ('Create my account','मेरा खाता बनाएँ','माझे खाते तयार करा','Crear mi cuenta'),
'action_admin_login': ('Open admin dashboard','प्रशासक डैशबोर्ड खोलें','प्रशासक डॅशबोर्ड उघडा','Abrir panel de administración'),
'error_login': ('Incorrect credentials or disabled account.','गलत लॉगिन विवरण या खाता निष्क्रिय है।','चुकीची लॉगिन माहिती किंवा खाते निष्क्रिय आहे.','Credenciales incorrectas o cuenta desactivada.'),
'error_admin_login': ('Incorrect administrator password or account not initialized.','प्रशासक पासवर्ड गलत है या खाता तैयार नहीं है।','प्रशासक पासवर्ड चुकीचा आहे किंवा खाते तयार नाही.','Contraseña incorrecta o cuenta no inicializada.'),
'error_password_mismatch': ('The passwords do not match.','दोनों पासवर्ड मेल नहीं खाते।','दोन्ही पासवर्ड जुळत नाहीत.','Las contraseñas no coinciden.'),
'session_expired': ('Your session ended or your account is disabled. Please sign in again.','आपका सत्र समाप्त हो गया या खाता निष्क्रिय है। दोबारा प्रवेश करें।','तुमचे सत्र संपले किंवा खाते निष्क्रिय आहे. पुन्हा प्रवेश करा.','Tu sesión terminó o tu cuenta está desactivada. Vuelve a entrar.'),
'sidebar_trust': ('Local AI · Health education only','स्थानीय एआई · केवल स्वास्थ्य शिक्षा','स्थानिक एआय · फक्त आरोग्य शिक्षण','IA local · Solo educación sanitaria'),
'sidebar_account_secure': ('SECURE ACCOUNT','सुरक्षित खाता','सुरक्षित खाते','CUENTA SEGURA'),
'hero_eyebrow': ('AI-POWERED HEALTH INSIGHTS','एआई आधारित स्वास्थ्य जानकारी','एआय-आधारित आरोग्य माहिती','INFORMACIÓN SANITARIA CON IA'),
'hero_title_1': ('Intelligent Healthcare,','बुद्धिमान स्वास्थ्य सेवा,','बुद्धिमान आरोग्य सेवा,','Salud inteligente,'),
'hero_title_2': ('Simply Explained.','आसान भाषा में।','सोप्या भाषेत.','Explicada con claridad.'),
'hero_desc': ('Understand health conditions, nutrition and medical reports with private local AI — in your language.','स्थानीय निजी एआई की मदद से अपनी भाषा में बीमारियाँ, पोषण और मेडिकल रिपोर्ट समझें।','खाजगी स्थानिक एआयद्वारे आपल्या भाषेत आजार, पोषण आणि वैद्यकीय अहवाल समजून घ्या.','Comprende condiciones, nutrición e informes con IA local privada, en tu idioma.'),
'hero_welcome': ('WELCOME BACK, {name}','वापसी पर स्वागत है, {name}','पुन्हा स्वागत आहे, {name}','QUÉ BUENO VERTE, {name}'),
'hero_chip_1': ('Multilingual AI','बहुभाषी एआई','बहुभाषिक एआय','IA multilingüe'),
'hero_chip_2': ('Offline AI · Ollama','ऑफ़लाइन एआई · Ollama','ऑफलाइन एआय · Ollama','IA sin conexión · Ollama'),
'hero_chip_3': ('Health education','स्वास्थ्य शिक्षा','आरोग्य शिक्षण','Educación sanitaria'),
'hero_stamp': ('LOCAL HEALTH AI','स्थानीय स्वास्थ्य एआई','स्थानिक आरोग्य एआय','IA DE SALUD LOCAL'),
'footer': ('Local AI • Privacy-first demonstration. Educational information, not medical advice or diagnosis. Verify report values with your laboratory and clinician.','स्थानीय एआई • गोपनीयता-प्राथमिकता वाला प्रदर्शन। यह जानकारी शिक्षा के लिए है, चिकित्सा सलाह या निदान नहीं। रिपोर्ट के मान प्रयोगशाला और डॉक्टर से जाँचें।','स्थानिक एआय • गोपनीयता-प्रथम प्रात्यक्षिक. ही शैक्षणिक माहिती आहे, वैद्यकीय सल्ला किंवा निदान नाही. तपासणीचे निष्कर्ष प्रयोगशाळा व डॉक्टरांकडून तपासा.','IA local • Demostración con prioridad en privacidad. Información educativa, no consejo ni diagnóstico médico. Confirma resultados con tu laboratorio y médico.'),
'play': ('Play answer','उत्तर सुनें','उत्तर ऐका','Escuchar respuesta'),
'stop': ('Stop','रोकें','थांबवा','Detener'),
'speed': ('Speed','गति','गती','Velocidad'),
'speech_stopped': ('Stopped','रोक दिया गया','थांबले','Detenido'),
'speech_unavailable': ('Voice playback unavailable in this browser','इस ब्राउज़र में आवाज़ उपलब्ध नहीं है','या ब्राउझरमध्ये आवाज उपलब्ध नाही','Voz no disponible en este navegador'),
'speech_speaking': ('Speaking…','बोला जा रहा है…','बोलले जात आहे…','Hablando…'),
'speech_finished': ('Finished','समाप्त','पूर्ण झाले','Terminado'),
'speech_voice_missing': ('System voice; language voice may not be installed','सिस्टम की आवाज़; इस भाषा की आवाज़ शायद उपलब्ध नहीं है','प्रणालीचा आवाज; ही भाषा उपलब्ध नसू शकते','Voz del sistema; quizá no haya voz para este idioma'),
'speech_audio_error': ('Audio stopped or unavailable','आवाज़ रुक गई या उपलब्ध नहीं है','आवाज थांबला किंवा उपलब्ध नाही','Audio detenido o no disponible'),
}
C.update({
'dash_stats_chat': ('Medical conversations','स्वास्थ्य बातचीत','आरोग्य संभाषणे','Conversaciones médicas'),
'dash_stats_reports': ('Reports analyzed','विश्लेषित रिपोर्ट','विश्लेषित अहवाल','Informes analizados'),
'dash_stats_voice': ('Voice questions','आवाज़ के सवाल','आवाजातील प्रश्न','Preguntas de voz'),
'dash_stats_model': ('Local AI model','स्थानीय एआई मॉडल','स्थानिक एआय मॉडेल','Modelo de IA local'),
'dash_heading': ('Everything you need, in one place','सभी स्वास्थ्य सुविधाएँ, एक ही जगह','सर्व आरोग्य सुविधा, एकाच ठिकाणी','Todo lo que necesitas en un lugar'),
'dash_desc': ('Ask a question, understand a report or speak with your assistant.','सवाल पूछें, रिपोर्ट समझें या सहायक से बोलें।','प्रश्न विचारा, अहवाल समजून घ्या किंवा सहाय्यकाशी बोला.','Pregunta, comprende un informe o habla con tu asistente.'),
'dash_chat_desc': ('Explore conditions, deficiencies and nutrition information.','बीमारियाँ, पोषक तत्वों की कमी और भोजन की जानकारी समझें।','आजार, पोषक घटकांची कमतरता आणि आहार समजून घ्या.','Explora condiciones, deficiencias y nutrición.'),
'dash_reports_desc': ('Understand lab results and reported reference ranges.','लैब जाँच और उसकी बताई गई सामान्य सीमाएँ समझें।','प्रयोगशाळेचे निष्कर्ष आणि दिलेल्या संदर्भ मर्यादा समजून घ्या.','Comprende resultados y rangos de laboratorio.'),
'dash_voice_desc': ('Ask naturally and listen to the answer.','बोलकर सवाल पूछें और जवाब सुनें।','बोलून प्रश्न विचारा आणि उत्तर ऐका.','Habla y escucha la respuesta.'),
'dash_insights_desc': ('Explore saved report trends.','सहेजी गई रिपोर्ट के रुझान देखें।','जतन केलेल्या अहवालांचे कल पाहा.','Explora tendencias de informes guardados.'),
'action_open': ('Open ↗','खोलें ↗','उघडा ↗','Abrir ↗'),
'journey': ('YOUR AI HEALTH JOURNEY','आपकी एआई स्वास्थ्य यात्रा','तुमचा एआय आरोग्य प्रवास','TU RECORRIDO CON IA'),
'journey_1': ('Ask or speak','पूछें या बोलें','विचारा किंवा बोला','Pregunta o habla'),
'journey_2': ('Understand','समझें','समजून घ्या','Comprende'),
'journey_3': ('Review report','रिपोर्ट देखें','अहवाल पाहा','Revisa informe'),
'journey_4': ('Consult a clinician','डॉक्टर से सलाह लें','डॉक्टरांचा सल्ला घ्या','Consulta a un médico'),
'chat_overline': ('MEDICAL ASSISTANT','चिकित्सा सहायक','वैद्यकीय सहाय्यक','ASISTENTE MÉDICO'),
'chat_desc': ('Ask about conditions, symptoms, deficiencies, diet and wellness.','बीमारी, लक्षण, पोषक तत्वों की कमी, भोजन या स्वास्थ्य के बारे में पूछें।','आजार, लक्षणे, कमतरता, आहार किंवा आरोग्याविषयी विचारा.','Pregunta sobre síntomas, enfermedades, deficiencias, dieta y bienestar.'),
'chat_detail': ('Answer length','उत्तर की लंबाई','उत्तराची लांबी','Extensión de respuesta'),
'detail_short': ('Short','संक्षिप्त','थोडक्यात','Breve'),
'detail_standard': ('Standard','सामान्य','सामान्य','Normal'),
'detail_detailed': ('Detailed','विस्तृत','सविस्तर','Detallada'),
'chat_vegetarian': ('Vegetarian food suggestions','शाकाहारी भोजन के सुझाव','शाकाहारी आहार सूचना','Sugerencias vegetarianas'),
'chat_try': ('Try asking about Vitamin B12 deficiency, PCOS or high LDL cholesterol.','विटामिन बी12 की कमी, पीसीओएस या बढ़े हुए एलडीएल कोलेस्ट्रॉल के बारे में पूछें।','व्हिटॅमिन बी१२ कमतरता, पीसीओएस किंवा वाढलेल्या एलडीएल कोलेस्टेरॉलबद्दल विचारा.','Prueba con déficit de B12, SOP o colesterol LDL elevado.'),
'chat_placeholder': ('Ask a health question…','स्वास्थ्य से जुड़ा सवाल लिखें…','आरोग्याविषयी प्रश्न लिहा…','Escribe tu pregunta de salud…'),
'chat_wait': ('Generating answer with local AI…','स्थानीय एआई से उत्तर तैयार किया जा रहा है…','स्थानिक एआय उत्तर तयार करत आहे…','Generando respuesta con IA local…'),
'chat_disclaimer': ('AI health information can contain mistakes. Consult a licensed professional for diagnosis or treatment.','एआई की स्वास्थ्य जानकारी में गलतियाँ हो सकती हैं। निदान या इलाज के लिए योग्य डॉक्टर की सलाह लें।','एआय आरोग्य माहितीमध्ये चुका असू शकतात. निदान किंवा उपचारासाठी पात्र डॉक्टरांचा सल्ला घ्या.','La IA puede equivocarse. Consulta a un profesional para diagnóstico o tratamiento.'),
'reports_overline': ('MEDICAL DOCUMENT ANALYSIS','चिकित्सा दस्तावेज़ विश्लेषण','वैद्यकीय दस्तऐवज विश्लेषण','ANÁLISIS DE DOCUMENTOS MÉDICOS'),
'reports_desc': ('Upload a lab report to understand its values and reference ranges.','लैब रिपोर्ट अपलोड करके उसके मान और सामान्य सीमाएँ समझें।','प्रयोगशाळा अहवाल अपलोड करून त्यातील मूल्ये आणि मर्यादा समजून घ्या.','Sube un informe de laboratorio para comprender sus resultados y rangos.'),
'reports_intro_title': ('SMART DOCUMENT SCAN','स्मार्ट दस्तावेज़ जाँच','स्मार्ट दस्तऐवज तपासणी','ANÁLISIS INTELIGENTE'),
'reports_intro_desc': ('Text PDFs · 10 MB maximum · 12 pages maximum · Original PDFs not stored','पाठ वाली पीडीएफ · अधिकतम 10 एमबी · अधिकतम 12 पृष्ठ · मूल फ़ाइल सहेजी नहीं जाती','मजकूर असलेली पीडीएफ · कमाल १० एमबी · कमाल १२ पाने · मूळ फाइल साठवली जात नाही','PDF con texto · Máximo 10 MB · Hasta 12 páginas · No se guarda el original'),
'reports_upload': ('Choose a medical lab PDF','लैब की पीडीएफ रिपोर्ट चुनें','प्रयोगशाळेचा पीडीएफ अहवाल निवडा','Selecciona un PDF médico'),
'reports_consent_note': ('Upload only reports you are authorized to share. Extracted text is stored and accessible to the administrator under your signup consent.','केवल अपनी या साझा करने की अनुमति वाली रिपोर्ट अपलोड करें। निकाला गया पाठ सहेजा जाता है और सहमति के अनुसार प्रशासक देख सकते हैं।','फक्त स्वतःचे किंवा परवानगी असलेले अहवाल अपलोड करा. काढलेला मजकूर साठवला जातो व संमतीनुसार प्रशासक पाहू शकतात.','Sube solo informes autorizados. El texto extraído se guarda y el administrador puede consultarlo según tu consentimiento.'),
'reports_oversize': ('File exceeds the 10 MB limit.','फ़ाइल 10 एमबी की सीमा से बड़ी है।','फाइल १० एमबी मर्यादेपेक्षा मोठी आहे.','El archivo supera los 10 MB.'),
'reports_analyze': ('Analyze with local AI','स्थानीय एआई से विश्लेषण करें','स्थानिक एआयद्वारे विश्लेषण करा','Analizar con IA local'),
'reports_extracting': ('Extracting report measurements…','रिपोर्ट के मान निकाले जा रहे हैं…','अहवालातील मूल्ये काढत आहे…','Extrayendo resultados…'),
'reports_parsed': ('Read {pages} pages and found {count} possible results. Check against the original.','{pages} पृष्ठ पढ़े गए और {count} संभावित नतीजे मिले। मूल रिपोर्ट से जाँचें।','{pages} पाने वाचली आणि {count} संभाव्य निकाल सापडले. मूळ अहवालाशी पडताळा करा.','Leídas {pages} páginas; encontrados {count} posibles resultados. Verifica el original.'),
'reports_generating': ('Preparing medical explanation with Ollama…','Ollama से स्वास्थ्य जानकारी तैयार की जा रही है…','Ollama द्वारे आरोग्य माहिती तयार होत आहे…','Preparando explicación con Ollama…'),
'reports_saved': ('Analysis saved to your history.','विश्लेषण आपके इतिहास में सहेजा गया।','विश्लेषण तुमच्या इतिहासात जतन झाले.','Análisis guardado en tu historial.'),
'reports_saved_title': ('Your saved reports','आपकी सहेजी गई रिपोर्ट','तुमचे जतन केलेले अहवाल','Tus informes guardados'),
'reports_saved_desc': ('Choose a report to view its analysis.','विश्लेषण देखने के लिए रिपोर्ट चुनें।','विश्लेषण पाहण्यासाठी अहवाल निवडा.','Elige un informe para ver el análisis.'),
'reports_library': ('REPORT LIBRARY','रिपोर्ट संग्रह','अहवाल संग्रह','BIBLIOTECA DE INFORMES'),
'reports_select': ('Saved report','सहेजी गई रिपोर्ट','जतन केलेला अहवाल','Informe guardado'),
'reports_source': ('View extracted source text (private information)','निकाला गया मूल पाठ देखें (निजी जानकारी)','काढलेला मूळ मजकूर पाहा (खाजगी माहिती)','Ver texto extraído (datos privados)'),
'reports_delete': ('Delete this saved report','इस सहेजी रिपोर्ट को मिटाएँ','हा जतन केलेला अहवाल हटवा','Eliminar este informe'),
'reports_delete_warning': ('This permanently removes the extracted text and summary; the original PDF was never stored.','इससे निकाला गया पाठ और सार हमेशा के लिए मिट जाएगा; मूल पीडीएफ सहेजी नहीं गई थी।','काढलेला मजकूर आणि सारांश कायमचा हटेल; मूळ पीडीएफ साठवली नव्हती.','Esto elimina el texto y resumen guardados; el PDF original nunca se almacenó.'),
'reports_delete_confirm': ('Confirm report deletion','रिपोर्ट मिटाने की पुष्टि करें','अहवाल हटवण्याची पुष्टी करा','Confirmar eliminación'),
'lab_none': ('No reliable lab values and reference ranges detected. Verify the PDF manually.','जाँच के भरोसेमंद मान और सीमाएँ नहीं मिलीं। मूल पीडीएफ खुद जाँचें।','विश्वसनीय चाचणी मूल्ये आणि मर्यादा मिळाल्या नाहीत. मूळ पीडीएफ तपासा.','No se detectaron resultados y rangos fiables. Verifica el PDF.'),
'lab_col_name': ('Test','जाँच','चाचणी','Prueba'),
'lab_col_result': ('Result','नतीजा','निकाल','Resultado'),
'lab_col_unit': ('Unit','इकाई','एकक','Unidad'),
'lab_col_range': ('Report range','रिपोर्ट में दी गई सीमा','अहवालातील मर्यादा','Rango del informe'),
'lab_col_comparison': ('Range comparison','सीमा से तुलना','मर्यादेशी तुलना','Comparación de rangos'),
'status_in': ('Within stated range','दी गई सीमा के भीतर','दिलेल्या मर्यादेत','Dentro del rango indicado'),
'status_high': ('High','सीमा से ऊपर','मर्यादेपेक्षा जास्त','Alto'),
'status_low': ('Low','सीमा से नीचे','मर्यादेपेक्षा कमी','Bajo'),
'status_uneval': ('Not evaluated','मूल्यांकन नहीं हुआ','मूल्यांकन झाले नाही','Sin evaluar'),
'lab_verify': ('Values and ranges are extracted heuristically. Verify every measurement against the original PDF before acting.','मान और सीमाएँ अनुमानित पहचान से निकाले जाते हैं। कोई कदम उठाने से पहले मूल रिपोर्ट से हर मान मिलाएँ।','मूल्ये आणि मर्यादा अंदाजाधारित पद्धतीने काढली जातात. कोणतीही कृती करण्यापूर्वी मूळ अहवाल तपासा.','Los valores se extraen automáticamente; verifica cada medición con el PDF original.'),
'export_txt': ('Download summary (.txt)','सारांश डाउनलोड करें (.txt)','सारांश डाउनलोड करा (.txt)','Descargar resumen (.txt)'),
'export_pdf': ('Download PDF summary','पीडीएफ सारांश डाउनलोड करें','पीडीएफ सारांश डाउनलोड करा','Descargar resumen PDF'),
'export_note': ('For non-English content, use the UTF-8 text download; PDF export currently supports English only.','अंग्रेज़ी के अलावा अन्य भाषाओं के लिए यूटीएफ-8 पाठ डाउनलोड करें; पीडीएफ निर्यात अभी केवल अंग्रेज़ी में उपलब्ध है।','इंग्रजीखेरीज अन्य भाषांसाठी यूटीएफ-८ मजकूर डाउनलोड करा; पीडीएफ निर्यात सध्या फक्त इंग्रजीत आहे.','Para otros idiomas, usa el archivo de texto UTF-8; el PDF solo admite inglés.'),
'export_disclaimer': ('Educational only; verify with the original report.','केवल शिक्षा के लिए; मूल रिपोर्ट से जाँचें।','फक्त शिक्षणासाठी; मूळ अहवाल तपासा.','Solo educación; verifica el informe original.'),
})
C.update({
'voice_overline': ('VOICE INTERACTION','आवाज़ से बातचीत','आवाजाद्वारे संवाद','INTERACCIÓN POR VOZ'),
'voice_desc': ('Record your question, transcribe it locally and listen to the AI answer.','सवाल बोलकर रिकॉर्ड करें, स्थानीय रूप से लिखित में बदलें और एआई का उत्तर सुनें।','प्रश्न रेकॉर्ड करा, स्थानिकरित्या मजकूरात बदला आणि एआय उत्तर ऐका.','Graba tu pregunta, transcríbela localmente y escucha la respuesta.'),
'voice_permission': ('Microphone permission required. First use may download a local Whisper model. Browser voices depend on the installed system voices.','माइक्रोफ़ोन की अनुमति ज़रूरी है। पहली बार स्थानीय व्हिस्पर मॉडल डाउनलोड हो सकता है। बोली गई आवाज़ ब्राउज़र की उपलब्ध आवाज़ों पर निर्भर है।','मायक्रोफोन परवानगी आवश्यक. पहिल्यांदा स्थानिक व्हिस्पर मॉडेल डाउनलोड होऊ शकते. आवाज ब्राउझरमधील उपलब्ध आवाजांवर अवलंबून असतो.','Se requiere permiso de micrófono. La primera vez puede descargarse Whisper. Las voces dependen del navegador.'),
'voice_record': ('Record a health question','स्वास्थ्य से जुड़ा सवाल रिकॉर्ड करें','आरोग्याचा प्रश्न रेकॉर्ड करा','Graba una pregunta de salud'),
'voice_detect': ('Detect spoken language automatically','बोली गई भाषा अपने आप पहचानें','बोललेली भाषा आपोआप ओळखा','Detectar idioma hablado automáticamente'),
'voice_transcribing': ('Transcribing locally…','स्थानीय रूप से आवाज़ लिखी जा रही है…','स्थानिकरित्या आवाज मजकूरात बदलत आहे…','Transcribiendo localmente…'),
'voice_review': ('Review and edit recognized text','पहचाने गए पाठ की जाँच करें और सुधारें','ओळखलेला मजकूर तपासा आणि दुरुस्त करा','Revisa y corrige el texto reconocido'),
'voice_review_note': ('Your recording was sent automatically. Check medical names; edit the text to ask again only if needed.','रिकॉर्डिंग समाप्त होते ही सवाल अपने आप भेज दिया गया है। मेडिकल नाम जाँचें; गलती हो तो पाठ सुधारकर दोबारा पूछें।','रेकॉर्डिंग पूर्ण झाल्यावर प्रश्न आपोआप पाठवला आहे. वैद्यकीय नावे तपासा; गरज असल्यास मजकूर सुधारून पुन्हा विचारा.','La pregunta se envió automáticamente al terminar de grabar. Revisa los términos médicos y corrige el texto solo si necesitas volver a preguntar.'),
'voice_ask': ('Ask Ollama','Ollama से पूछें','Ollama ला विचारा','Preguntar a Ollama'),
'voice_generating': ('Generating answer…','उत्तर तैयार हो रहा है…','उत्तर तयार होत आहे…','Generando respuesta…'),
'voice_saved': ('Answer saved in your history.','उत्तर इतिहास में सहेजा गया।','उत्तर इतिहासात जतन झाले.','Respuesta guardada en tu historial.'),
'voice_response': ('AI answer','एआई का उत्तर','एआय उत्तर','Respuesta de IA'),
'history_desc': ('Review and delete saved questions and answers.','सहेजे गए सवाल और जवाब देखें या मिटाएँ।','जतन केलेले प्रश्न आणि उत्तरे पाहा किंवा हटवा.','Consulta y elimina preguntas y respuestas guardadas.'),
'history_overline': ('PRIVATE HISTORY','निजी इतिहास','खाजगी इतिहास','HISTORIAL PRIVADO'),
'empty': ('No records yet.','अभी कोई रिकॉर्ड नहीं है।','अद्याप नोंदी नाहीत.','Todavía no hay registros.'),
'history_type': ('Question type','सवाल का प्रकार','प्रश्नाचा प्रकार','Tipo de pregunta'),
'history_all': ('All','सभी','सर्व','Todos'),
'history_medical': ('Medical chat','स्वास्थ्य बातचीत','आरोग्य संभाषण','Chat médico'),
'history_voice': ('Voice','आवाज़','आवाज','Voz'),
'history_question': ('Your question','आपका सवाल','तुमचा प्रश्न','Tu pregunta'),
'history_answer': ('AI answer','एआई का उत्तर','एआय उत्तर','Respuesta de IA'),
'action_delete': ('Delete','मिटाएँ','हटवा','Eliminar'),
'insights_desc': ('Explore stored report findings; this is not a diagnostic dashboard.','सहेजी गई रिपोर्ट के नतीजे देखें; यह निदान करने वाला डैशबोर्ड नहीं है।','जतन केलेल्या अहवालांचे निकाल पाहा; हा निदान करणारा डॅशबोर्ड नाही.','Explora informes guardados; no es un panel diagnóstico.'),
'insights_overline': ('HEALTH DATA VISUALIZATION','स्वास्थ्य आँकड़ों का दृश्य','आरोग्य माहितीचे आलेख','VISUALIZACIÓN DE SALUD'),
'insights_empty': ('Upload a report first to see health insights.','स्वास्थ्य जानकारी देखने के लिए पहले रिपोर्ट अपलोड करें।','आरोग्य माहिती पाहण्यासाठी आधी अहवाल अपलोड करा.','Primero sube un informe para ver indicadores.'),
'insights_saved': ('Saved reports','सहेजी रिपोर्ट','जतन केलेले अहवाल','Informes guardados'),
'insights_parsed': ('Extracted results','निकाले गए नतीजे','काढलेले निकाल','Resultados extraídos'),
'insights_flags': ('Out-of-range findings','सीमा से बाहर नतीजे','मर्यादेबाहेरील निकाल','Resultados fuera de rango'),
'insights_no_labs': ('No structured values available for charts.','चार्ट बनाने के लिए व्यवस्थित मान उपलब्ध नहीं हैं।','आलेखासाठी रचनेत मूल्ये उपलब्ध नाहीत.','No hay valores estructurados para gráficos.'),
'insights_range_title': ('Comparison with report ranges','रिपोर्ट की सीमाओं से तुलना','अहवालातील मर्यादांशी तुलना','Comparación con rangos'),
'insights_tests_title': ('Most frequently extracted tests','सबसे अधिक निकाली गई जाँचें','सर्वाधिक काढलेल्या चाचण्या','Pruebas más frecuentes'),
'insights_count': ('Number of results','नतीजों की संख्या','निकालांची संख्या','Número de resultados'),
'insights_compare': ('Compare repeated results (same unit only)','बार-बार हुई जाँच की तुलना (केवल समान इकाई)','पुन्हा झालेल्या चाचण्यांची तुलना (फक्त समान एकक)','Comparar resultados repetidos (misma unidad)'),
'insights_test': ('Lab test','प्रयोगशाला जाँच','प्रयोगशाळा चाचणी','Prueba de laboratorio'),
'insights_units_warning': ('Cannot compare different or unknown units. Check the original reports.','अलग या अज्ञात इकाइयों की तुलना नहीं की जा सकती। मूल रिपोर्ट जाँचें।','भिन्न किंवा अज्ञात एककांची तुलना शक्य नाही. मूळ अहवाल तपासा.','No se pueden comparar unidades distintas o desconocidas. Consulta el informe.'),
'insights_need_two': ('At least two reports with this measurement are needed.','इस जाँच वाली कम से कम दो रिपोर्ट चाहिए।','या चाचणीचे किमान दोन अहवाल आवश्यक आहेत.','Se necesitan al menos dos informes con esta medición.'),
'insights_chart_note': ('Different laboratories or methods may not be comparable; no diagnosis is inferred.','अलग प्रयोगशालाओं या तरीकों की तुलना सही न भी हो; इससे निदान नहीं होता।','भिन्न प्रयोगशाळा किंवा पद्धती तुलना करण्यायोग्य नसतील; यावरून निदान होत नाही.','Distintos laboratorios quizá no sean comparables; no se deduce diagnóstico.'),
'insights_warning': ('Results are compared only with printed report ranges, not medical diagnostic thresholds. Always verify with a clinician.','नतीजों की तुलना केवल रिपोर्ट में छपी सीमाओं से है, निदान सीमा से नहीं। डॉक्टर से पुष्टि करें।','निकालांची तुलना फक्त अहवालातील मर्यादांशी आहे, निदान मर्यादांशी नाही. डॉक्टरांकडून पुष्टी करा.','Los resultados se comparan con rangos impresos, no umbrales diagnósticos. Consúltalo con un médico.'),
'profile_desc': ('Manage account preferences and stored medical records.','खाते की पसंद और सहेजे गए मेडिकल रिकॉर्ड प्रबंधित करें।','खात्याच्या निवडी आणि जतन केलेल्या वैद्यकीय नोंदी व्यवस्थापित करा.','Gestiona preferencias y datos médicos guardados.'),
'profile_overline': ('ACCOUNT & PRIVACY','खाता और गोपनीयता','खाते आणि गोपनीयता','CUENTA Y PRIVACIDAD'),
'profile_details': ('Account details','खाते का विवरण','खात्याची माहिती','Datos de la cuenta'),
'profile_display': ('Display name','दिखाई देने वाला नाम','दाखवायचे नाव','Nombre visible'),
'profile_save': ('Save profile','प्रोफ़ाइल सहेजें','प्रोफाइल जतन करा','Guardar perfil'),
'profile_short_name': ('Enter at least two characters for the name.','नाम में कम से कम दो वर्ण लिखें।','नावासाठी किमान दोन वर्ण लिहा.','El nombre debe tener al menos dos caracteres.'),
'profile_updated': ('Profile updated.','प्रोफ़ाइल बदल दी गई।','प्रोफाइल अद्ययावत झाले.','Perfil actualizado.'),
'profile_change_password': ('Change password','पासवर्ड बदलें','पासवर्ड बदला','Cambiar contraseña'),
'profile_current_password': ('Current password','वर्तमान पासवर्ड','सध्याचा पासवर्ड','Contraseña actual'),
'profile_new_password': ('New password (10+ letters and numbers)','नया पासवर्ड (कम से कम 10 वर्ण, अक्षर और अंक)','नवीन पासवर्ड (किमान १० वर्ण, अक्षरे व अंक)','Nueva contraseña (10+ letras y números)'),
'profile_password_changed': ('Password changed.','पासवर्ड बदल दिया गया।','पासवर्ड बदलला.','Contraseña cambiada.'),
'profile_password_wrong': ('Current password is incorrect.','वर्तमान पासवर्ड गलत है।','सध्याचा पासवर्ड चुकीचा आहे.','La contraseña actual no es correcta.'),
'profile_delete': ('Delete my account and medical data','मेरा खाता और मेडिकल डेटा मिटाएँ','माझे खाते आणि वैद्यकीय माहिती हटवा','Eliminar mi cuenta y datos médicos'),
'profile_delete_warning': ('Irreversible: deletes your profile, chats, report text and summaries. Minimal audit metadata may remain.','इस कार्रवाई को वापस नहीं किया जा सकता: प्रोफ़ाइल, बातचीत, रिपोर्ट का पाठ और सारांश मिट जाएँगे। कुछ ऑडिट जानकारी बच सकती है।','हे पूर्ववत होणार नाही: प्रोफाइल, संभाषणे, अहवाल मजकूर आणि सारांश हटतील. काही लेखापरीक्षण नोंदी उरू शकतात.','Es irreversible: elimina el perfil, mensajes y resultados guardados. Pueden conservarse metadatos de auditoría.'),
'profile_confirm_type': ('Type DELETE to confirm','पुष्टि के लिए DELETE लिखें','पुष्टीसाठी DELETE लिहा','Escribe DELETE para confirmar'),
'profile_your_password': ('Your password','आपका पासवर्ड','तुमचा पासवर्ड','Tu contraseña'),
'profile_delete_submit': ('Permanently delete account','खाता हमेशा के लिए मिटाएँ','खाते कायमचे हटवा','Eliminar cuenta definitivamente'),
'profile_delete_error': ('Confirmation text or password incorrect.','पुष्टि का पाठ या पासवर्ड गलत है।','पुष्टी मजकूर किंवा पासवर्ड चुकीचा आहे.','Texto de confirmación o contraseña incorrecta.'),
})
C.update({
'admin_overview': ('Administration center','प्रशासन केंद्र','प्रशासन केंद्र','Centro de administración'),
'admin_overview_desc': ('Platform summary with audited access to stored information.','सहेजी जानकारी तक दर्ज पहुँच के साथ प्रणाली का सार।','जतन केलेल्या माहितीत नोंदवलेल्या प्रवेशासह प्रणालीचा आढावा.','Resumen de la plataforma con acceso auditado a la información.'),
'admin_overline': ('ADMINISTRATION · MR. DOC','प्रशासन · MR. DOC','प्रशासन · MR. DOC','ADMINISTRACIÓN · MR. DOC'),
'admin_registered': ('Registered users','पंजीकृत उपयोगकर्ता','नोंदणीकृत वापरकर्ते','Usuarios registrados'),
'admin_convos': ('AI conversations','एआई बातचीत','एआय संभाषणे','Conversaciones de IA'),
'admin_analyzed': ('Analyzed reports','विश्लेषित रिपोर्ट','विश्लेषित अहवाल','Informes analizados'),
'admin_voice': ('Voice sessions','आवाज़ के सत्र','आवाज सत्रे','Sesiones de voz'),
'admin_privacy_title': ('Privacy by design','डिज़ाइन में गोपनीयता','रचनेतच गोपनीयता','Privacidad desde el diseño'),
'admin_privacy_desc': ('Medical report text and conversation contents are hidden until an authorized administrator opens a record. Consent is checked and successful access is logged. Passwords and original PDFs are never displayed.','मेडिकल रिपोर्ट का पाठ और बातचीत अधिकृत प्रशासक द्वारा रिकॉर्ड खोलने तक छिपे रहते हैं। सहमति जाँची जाती है और पहुँच दर्ज होती है। पासवर्ड तथा मूल पीडीएफ नहीं दिखाई जातीं।','अधिकृत प्रशासक नोंद उघडेपर्यंत वैद्यकीय अहवाल आणि संभाषणाचा मजकूर लपवला जातो. संमती तपासली जाते व प्रवेश नोंदवला जातो. पासवर्ड आणि मूळ पीडीएफ दाखवल्या जात नाहीत.','Los informes y conversaciones se ocultan hasta que un administrador abre el registro. Se verifica el consentimiento y se registra el acceso. Nunca se muestran contraseñas ni PDFs originales.'),
'admin_account_status': ('Account status','खाते की स्थिति','खात्याची स्थिती','Estado de las cuentas'),
'admin_active': ('Active','सक्रिय','सक्रिय','Activa'),
'admin_inactive': ('Inactive','निष्क्रिय','निष्क्रिय','Inactiva'),
'admin_recent': ('Recent registrations','हाल के पंजीकरण','अलीकडील नोंदण्या','Registros recientes'),
'admin_joined': ('Joined','पंजीकरण तिथि','नोंदणी तारीख','Fecha de registro'),
'admin_no_users': ('No registered users yet.','अभी कोई उपयोगकर्ता पंजीकृत नहीं है।','अद्याप नोंदणीकृत वापरकर्ते नाहीत.','Todavía no hay usuarios registrados.'),
'admin_directory_tip': ('Use the user directory to manage accounts.','खाते प्रबंधित करने के लिए उपयोगकर्ता सूची खोलें।','खाती व्यवस्थापित करण्यासाठी वापरकर्ता सूची उघडा.','Usa el directorio para gestionar cuentas.'),
'admin_user_directory': ('User directory','उपयोगकर्ता सूची','वापरकर्ता सूची','Directorio de usuarios'),
'admin_user_directory_desc': ('Find users and manage access; detailed views are audited.','उपयोगकर्ता खोजें और पहुँच प्रबंधित करें; विवरण देखने की प्रविष्टि दर्ज होती है।','वापरकर्ते शोधा व प्रवेश व्यवस्थापित करा; तपशील पाहण्याची नोंद होते.','Busca usuarios y gestiona su acceso; se auditan las consultas.'),
'admin_directory_overline': ('ACCOUNT DIRECTORY','खाता सूची','खाते सूची','DIRECTORIO DE CUENTAS'),
'admin_search': ('Search username, name or email','उपयोगकर्ता नाम, नाम या ईमेल खोजें','वापरकर्तानाव, नाव किंवा ईमेल शोधा','Buscar usuario, nombre o correo'),
'admin_search_hint': ('Type a search term…','खोजने के लिए लिखें…','शोधण्यासाठी लिहा…','Escribe un término…'),
'admin_found': ('{count} users found. Passwords and hashes are never shown.','{count} उपयोगकर्ता मिले। पासवर्ड कभी नहीं दिखाए जाते।','{count} वापरकर्ते सापडले. पासवर्ड दाखवले जात नाहीत.','Se encontraron {count} usuarios. Las contraseñas nunca se muestran.'),
'admin_view_profile': ('View profile details (audited)','प्रोफ़ाइल विवरण देखें (दर्ज होगा)','प्रोफाइल तपशील पाहा (नोंद केली जाईल)','Ver perfil (auditado)'),
'admin_preferred_lang': ('Preferred language','पसंदीदा भाषा','पसंतीची भाषा','Idioma preferido'),
'admin_consent': ('Consent acknowledged','सहमति दी गई','संमती दिली','Consentimiento aceptado'),
'admin_yes': ('Yes','हाँ','होय','Sí'),
'admin_no': ('No','नहीं','नाही','No'),
'admin_last_login': ('Last login','अंतिम प्रवेश','शेवटचा प्रवेश','Último acceso'),
'admin_account': ('Account','खाता','खाते','Cuenta'),
'admin_disabled': ('Disabled','निष्क्रिय','बंद','Desactivada'),
'admin_deactivate': ('Deactivate user','उपयोगकर्ता निष्क्रिय करें','वापरकर्ता निष्क्रिय करा','Desactivar usuario'),
'admin_reactivate': ('Reactivate user','उपयोगकर्ता सक्रिय करें','वापरकर्ता पुन्हा सक्रिय करा','Reactivar usuario'),
'admin_reports_title': ('Stored medical reports','सहेजी मेडिकल रिपोर्ट','जतन केलेले वैद्यकीय अहवाल','Informes médicos guardados'),
'admin_reports_desc': ('Private content loads only after an authorized, recorded action.','निजी जानकारी केवल अधिकृत और दर्ज कार्रवाई के बाद दिखाई जाती है।','खाजगी माहिती फक्त अधिकृत आणि नोंदवलेल्या कृतीनंतर दाखवली जाते.','Los datos privados solo se cargan tras un acceso autorizado y registrado.'),
'admin_sensitive_reports': ('SENSITIVE REPORT ACCESS','संवेदनशील रिपोर्ट पहुँच','संवेदनशील अहवाल प्रवेश','ACCESO A INFORMES SENSIBLES'),
'admin_no_reports': ('No consent-authorized reports found.','सहमति वाली कोई रिपोर्ट नहीं मिली।','संमती असलेले अहवाल सापडले नाहीत.','No hay informes con consentimiento.'),
'admin_report_header': ('Report #{id} · User #{user} · {date}','रिपोर्ट #{id} · उपयोगकर्ता #{user} · {date}','अहवाल #{id} · वापरकर्ता #{user} · {date}','Informe #{id} · Usuario #{user} · {date}'),
'admin_report_pages': ('{pages} pages. Filename and findings are hidden until opened.','{pages} पृष्ठ। फ़ाइल नाम और नतीजे खोलने तक छिपे हैं।','{pages} पाने. फाइल नाव आणि निष्कर्ष उघडेपर्यंत लपवले आहेत.','{pages} páginas. El nombre y los resultados se ocultan hasta abrir.'),
'admin_open_report': ('Open report and log access','रिपोर्ट खोलें और पहुँच दर्ज करें','अहवाल उघडा आणि प्रवेश नोंदवा','Abrir informe y registrar acceso'),
'admin_no_consent': ('Unavailable or consent missing.','उपलब्ध नहीं है या सहमति नहीं मिली।','उपलब्ध नाही किंवा संमती नाही.','No disponible o falta consentimiento.'),
'admin_file': ('File','फ़ाइल','फाइल','Archivo'),
'admin_extracted': ('View extracted private text','निकाला गया निजी पाठ देखें','काढलेला खाजगी मजकूर पाहा','Ver texto privado extraído'),
'admin_convos_title': ('Conversation access','बातचीत तक पहुँच','संभाषण प्रवेश','Acceso a conversaciones'),
'admin_convos_desc': ('Questions and responses remain hidden until access is recorded.','पहुँच दर्ज होने तक सवाल और जवाब छिपे रहते हैं।','प्रवेश नोंदवला जाईपर्यंत प्रश्न आणि उत्तरे लपवली जातात.','Preguntas y respuestas ocultas hasta registrar el acceso.'),
'admin_sensitive_chat': ('SENSITIVE CHAT ACCESS','संवेदनशील बातचीत पहुँच','संवेदनशील संभाषण प्रवेश','ACCESO A CONVERSACIONES'),
'admin_no_convos': ('No conversations with consent found.','सहमति वाली कोई बातचीत नहीं मिली।','संमती असलेली संभाषणे सापडली नाहीत.','No hay conversaciones con consentimiento.'),
'admin_chat_header': ('Conversation #{id} · User #{user} · {date}','बातचीत #{id} · उपयोगकर्ता #{user} · {date}','संभाषण #{id} · वापरकर्ता #{user} · {date}','Conversación #{id} · Usuario #{user} · {date}'),
'admin_open_chat': ('Open conversation and log access','बातचीत खोलें और पहुँच दर्ज करें','संभाषण उघडा आणि प्रवेश नोंदवा','Abrir conversación y registrar acceso'),
'admin_audit_title': ('Access audit trail','पहुँच का ऑडिट इतिहास','प्रवेश तपासणी इतिहास','Historial de auditoría'),
'admin_audit_desc': ('Recent administrator events without private medical content.','निजी मेडिकल सामग्री के बिना हाल की प्रशासकीय गतिविधियाँ।','खाजगी वैद्यकीय मजकुराशिवाय अलीकडील प्रशासकीय घटना.','Actividad reciente sin contenido médico privado.'),
'admin_audit_overline': ('ACCOUNTABILITY','उत्तरदायित्व','जबाबदारी','RESPONSABILIDAD'),
'admin_no_audit': ('No access events yet.','अभी पहुँच की कोई प्रविष्टि नहीं है।','अद्याप प्रवेश नोंदी नाहीत.','No hay eventos de acceso.'),
'admin_filter': ('Filter by event','घटना के अनुसार छाँटें','घटनेनुसार फिल्टर करा','Filtrar por evento'),
'admin_all': ('All events','सभी घटनाएँ','सर्व घटना','Todos los eventos'),
'admin_time': ('Time','समय','वेळ','Hora'),
'admin_actor': ('Actor ID','प्रशासक क्रमांक','प्रशासक क्रमांक','ID del actor'),
'admin_action': ('Action','कार्रवाई','कृती','Acción'),
'admin_user_id': ('User ID','उपयोगकर्ता क्रमांक','वापरकर्ता क्रमांक','ID de usuario'),
'admin_record_id': ('Record ID','रिकॉर्ड क्रमांक','नोंद क्रमांक','ID de registro'),
'admin_audit_note': ('Access events identify who opened a record; they contain no medical details or passwords.','पहुँच की प्रविष्टि बताती है कि रिकॉर्ड किसने खोला; इसमें मेडिकल जानकारी या पासवर्ड नहीं हैं।','प्रवेश नोंद कोणाने रेकॉर्ड उघडले हे सांगते; त्यात वैद्यकीय तपशील किंवा पासवर्ड नसतात.','El registro indica quién abrió un dato; no incluye información médica ni contraseñas.'),
'about_title': ('About Healthcare Info Assistant','Healthcare Info Assistant के बारे में','Healthcare Info Assistant विषयी','Acerca de Healthcare Info Assistant'),
'about_desc': ('Your Intelligent Healthcare Information Companion.','आपका बुद्धिमान स्वास्थ्य जानकारी साथी।','तुमचा बुद्धिमान आरोग्य माहिती साथी.','Tu acompañante inteligente de información sanitaria.'),
'about_overline': ('OUR PURPOSE','हमारा उद्देश्य','आमचा उद्देश','NUESTRO PROPÓSITO'),
'about_intro': ('Healthcare Info Assistant helps people understand general health topics, nutritional deficiencies and lab reports using local AI. You can ask questions, upload a PDF or use your voice. It supports multiple interface languages but is not a clinical diagnostic device.','Healthcare Info Assistant स्थानीय एआई से सामान्य स्वास्थ्य, पोषक तत्वों की कमी और लैब रिपोर्ट समझने में मदद करता है। आप सवाल पूछ सकते हैं, पीडीएफ अपलोड कर सकते हैं या आवाज़ का उपयोग कर सकते हैं। यह कई इंटरफ़ेस भाषाओं का समर्थन करता है, लेकिन चिकित्सकीय निदान उपकरण नहीं है।','Healthcare Info Assistant स्थानिक एआय वापरून सामान्य आरोग्य, पोषणातील कमतरता व प्रयोगशाळा अहवाल समजून घेण्यास मदत करतो. तुम्ही प्रश्न विचारू शकता, पीडीएफ अपलोड करू शकता किंवा आवाज वापरू शकता. यात अनेक भाषा आहेत, पण हे वैद्यकीय निदान उपकरण नाही.','Healthcare Info Assistant ayuda a comprender temas de salud, deficiencias e informes usando IA local. Puedes preguntar, subir un PDF o usar la voz. Admite varios idiomas, pero no es una herramienta de diagnóstico.'),
'about_card_chat': ('AI medical chat','एआई चिकित्सा बातचीत','एआय वैद्यकीय संभाषण','Chat médico con IA'),
'about_card_chat_desc': ('Clear explanations about health, nutrition and when to seek care.','स्वास्थ्य, पोषण और डॉक्टर से कब मिलें, इसकी आसान जानकारी।','आरोग्य, आहार आणि डॉक्टरांना कधी भेटावे याविषयी सोपी माहिती.','Explicaciones sobre salud, nutrición y cuándo consultar.'),
'about_card_report': ('Lab report analysis','लैब रिपोर्ट विश्लेषण','प्रयोगशाळा अहवाल विश्लेषण','Análisis de laboratorio'),
'about_card_report_desc': ('Compares values with reference ranges provided by the report.','मानों की तुलना रिपोर्ट में दी गई सामान्य सीमाओं से करता है।','अहवालातील दिलेल्या मर्यादांशी मूल्यांची तुलना करतो.','Compara valores con rangos incluidos en el informe.'),
'about_card_voice': ('Voice and languages','आवाज़ और भाषाएँ','आवाज आणि भाषा','Voz e idiomas'),
'about_card_voice_desc': ('Local speech recognition and browser-based spoken replies.','स्थानीय आवाज़ पहचान और ब्राउज़र से बोले गए जवाब।','स्थानिक वाणी ओळख आणि ब्राउझरमधील बोलकी उत्तरे.','Reconocimiento local y respuestas habladas del navegador.'),
'about_how': ('How it works','यह कैसे काम करता है','हे कसे कार्य करते','Cómo funciona'),
'about_how_desc': ('Local-first technology designed for clarity and accessibility.','स्पष्टता और सुविधा के लिए स्थानीय तकनीक।','सुलभता आणि स्पष्टतेसाठी स्थानिक तंत्रज्ञान.','Tecnología local, clara y accesible.'),
'about_how_overline': ('BEHIND THE EXPERIENCE','इसके पीछे की तकनीक','मागील तंत्रज्ञान','CÓMO ESTÁ HECHO'),
'about_step_1': ('Streamlit interface','स्ट्रीमलिट इंटरफ़ेस','स्ट्रीमलिट इंटरफेस','Interfaz Streamlit'),
'about_step_2': ('Local Ollama AI','स्थानीय Ollama एआई','स्थानिक Ollama एआय','IA local Ollama'),
'about_step_3': ('Plain-language explanations','आसान भाषा में जवाब','सोप्या भाषेतील उत्तरे','Explicaciones claras'),
'about_step_4': ('PDF extraction and optional OCR','पीडीएफ से पाठ और वैकल्पिक अक्षर पहचान','पीडीएफ मजकूर आणि पर्यायी अक्षर ओळख','Extracción PDF y OCR opcional'),
'about_step_5': ('Password hashing and local database','पासवर्ड सुरक्षा और स्थानीय डेटाबेस','पासवर्ड सुरक्षा आणि स्थानिक डेटाबेस','Contraseñas cifradas y base de datos local'),
'about_step_6': ('Speech recognition and playback','आवाज़ पहचान और जवाब सुनना','वाणी ओळख आणि उत्तर ऐकणे','Reconocimiento y reproducción de voz'),
'about_privacy': ('Privacy and limitations','गोपनीयता और सीमाएँ','गोपनीयता आणि मर्यादा','Privacidad y límites'),
'about_privacy_desc': ('Understand what the application does and what it cannot guarantee.','जानें यह ऐप क्या करता है और क्या गारंटी नहीं दे सकता।','अॅप काय करते आणि कशाची खात्री देऊ शकत नाही ते समजून घ्या.','Conoce lo que puede y no puede garantizar la aplicación.'),
'about_privacy_overline': ('TRUST & SAFETY','विश्वास और सुरक्षा','विश्वास आणि सुरक्षा','CONFIANZA Y SEGURIDAD'),
'about_privacy_1': ('Stored messages and extracted report text are held in the local SQLite database.','सहेजे गए संदेश और रिपोर्ट का निकाला गया पाठ स्थानीय SQLite डेटाबेस में रखा जाता है।','जतन केलेले संदेश आणि अहवालातील मजकूर स्थानिक SQLite डेटाबेसमध्ये साठवला जातो.','Los mensajes y textos extraídos se guardan en SQLite local.'),
'about_privacy_2': ('The permanent administrator Mr. Doc can see stored data with registration consent; sensitive reads are logged.','स्थायी प्रशासक Mr. Doc पंजीकरण पर दी गई सहमति के अनुसार सहेजा डेटा देख सकते हैं; संवेदनशील पहुँच दर्ज होती है।','कायमस्वरूपी प्रशासक Mr. Doc नोंदणीतील संमतीनुसार जतन केलेली माहिती पाहू शकतात; संवेदनशील प्रवेश नोंदवला जातो.','El administrador permanente Mr. Doc puede consultar datos con consentimiento; los accesos se registran.'),
'about_privacy_3': ('Original PDFs are not stored. Scanned documents may require optional OCR software.','मूल पीडीएफ सहेजी नहीं जातीं। स्कैन दस्तावेज़ों के लिए वैकल्पिक अक्षर पहचान सॉफ़्टवेयर चाहिए।','मूळ पीडीएफ साठवल्या जात नाहीत. स्कॅन दस्तऐवजांसाठी पर्यायी अक्षर ओळख सॉफ्टवेअर लागू शकते.','No se guardan los PDFs originales. Los escaneos pueden requerir OCR.'),
'about_privacy_4': ('Local Ollama processes the AI prompts; no paid Gemini API is required.','स्थानीय Ollama एआई सवालों पर काम करता है; सशुल्क Gemini एपीआई की ज़रूरत नहीं है।','स्थानिक Ollama एआय प्रश्न हाताळतो; सशुल्क Gemini एपीआयची गरज नाही.','Ollama procesa localmente; no hace falta una API de Gemini.'),
'about_privacy_5': ('AI can be wrong. Lab comparisons must be verified, and medical decisions belong with qualified clinicians.','एआई गलत हो सकता है। लैब तुलना जाँचें और चिकित्सकीय निर्णय योग्य डॉक्टर से लें।','एआय चुकीचे असू शकते. प्रयोगशाळेतील तुलना तपासा आणि वैद्यकीय निर्णय पात्र डॉक्टरांकडून घ्या.','La IA puede errar. Verifica los análisis y consulta decisiones médicas con profesionales.'),
'about_privacy_6': ('This is an educational local demonstration, not a certified medical product or hosted patient portal.','यह स्थानीय शैक्षिक प्रदर्शन है, प्रमाणित चिकित्सा उपकरण या ऑनलाइन रोगी पोर्टल नहीं।','हे स्थानिक शैक्षणिक प्रात्यक्षिक आहे, प्रमाणित वैद्यकीय उत्पादन किंवा ऑनलाइन रुग्ण पोर्टल नाही.','Es una demostración local educativa, no un producto médico certificado ni portal clínico.'),
'about_resources': ('Independent medical resources','स्वतंत्र चिकित्सा जानकारी के स्रोत','स्वतंत्र वैद्यकीय माहिती स्रोत','Fuentes médicas independientes'),
})

C.update({
'ollama_ready': ('Local Ollama is ready.','स्थानीय Ollama तैयार है।','स्थानिक Ollama तयार आहे.','Ollama local está listo.'),
'ollama_offline': ('Ollama is not ready. Make sure the service and selected model are running.','Ollama तैयार नहीं है। सेवा और चुने गए मॉडल को चालू करें।','Ollama तयार नाही. सेवा आणि निवडलेले मॉडेल सुरू करा.','Ollama no está listo. Inicia el servicio y el modelo seleccionado.'),
'generic_error': ('Action failed: check your input, installed model and setup.','कार्रवाई पूरी नहीं हुई: अपना विवरण, स्थापित मॉडल और सेटअप जाँचें।','कृती अयशस्वी: तुमची माहिती, स्थापित मॉडेल आणि सेटअप तपासा.','No se pudo completar: revisa tus datos, el modelo y la configuración.'),
'auth_error': ('Please check your information: username must be unique, email valid, password at least 10 characters with letters and digits, and consent required.','कृपया विवरण जाँचें: उपयोगकर्ता नाम अलग हो, ईमेल सही हो, पासवर्ड में कम से कम 10 वर्ण, अक्षर और अंक हों तथा सहमति आवश्यक है।','कृपया माहिती तपासा: वापरकर्तानाव वेगळे, ईमेल योग्य, पासवर्ड किमान १० वर्ण व अक्षरे-अंक असलेला आणि संमती आवश्यक आहे.','Revisa tus datos: usuario único, correo válido, contraseña de al menos 10 caracteres con letras y números y consentimiento obligatorio.'),
'auth_password_error': ('Password change failed. Use at least 10 characters with letters and numbers.','पासवर्ड नहीं बदला। कम से कम 10 वर्ण तथा अक्षर और अंक इस्तेमाल करें।','पासवर्ड बदलला नाही. किमान १० वर्ण तसेच अक्षरे आणि अंक वापरा.','No se cambió la contraseña. Usa 10 o más caracteres con letras y números.'),
})

C.update({
'brand_specialty': ('AI • MEDTECH','एआई • चिकित्सा तकनीक','एआय • वैद्यकीय तंत्रज्ञान','IA • TECNOLOGÍA MÉDICA'),
'event_admin_login': ('Administrator signed in','प्रशासक ने प्रवेश किया','प्रशासकाने प्रवेश केला','Inicio de sesión de administrador'),
'event_user_login': ('User signed in','उपयोगकर्ता ने प्रवेश किया','वापरकर्त्याने प्रवेश केला','Inicio de sesión de usuario'),
'event_user_registered': ('User registered','उपयोगकर्ता पंजीकृत हुआ','वापरकर्त्याची नोंदणी झाली','Usuario registrado'),
'event_admin_read_conversation': ('Conversation viewed','बातचीत देखी गई','संभाषण पाहिले','Conversación consultada'),
'event_admin_read_report': ('Report viewed','रिपोर्ट देखी गई','अहवाल पाहिला','Informe consultado'),
'event_admin_read_user_profile': ('Profile viewed','प्रोफ़ाइल देखी गई','प्रोफाइल पाहिले','Perfil consultado'),
'event_admin_user_status_change': ('User account status changed','उपयोगकर्ता खाते की स्थिति बदली गई','वापरकर्ता खात्याची स्थिती बदलली','Estado de cuenta modificado'),
'event_user_report_deleted': ('Report deleted','रिपोर्ट मिटाई गई','अहवाल हटवला','Informe eliminado'),
'event_user_account_deleted': ('Account deleted','खाता मिटाया गया','खाते हटवले','Cuenta eliminada'),
})



# Extra languages are selectable without exposing arbitrary user text input.
# Existing four complete catalogs are preserved byte-for-byte. The fallback for
# any unavailable extra-language string is intentionally English (not a fake
# machine translation); optional Ollama-built locale packs improve coverage.
from ui.extra_languages import EXTRA_NAMES, EXTRA_TEXT, EXTRA_VOICES
from functools import lru_cache
import json
from pathlib import Path
from config.settings import ROOT

LANGUAGES.update(EXTRA_NAMES)
VOICE_LOCALES.update(EXTRA_VOICES)
for _key, _row in list(C.items()):
    C[_key] = tuple(_row) + tuple(EXTRA_TEXT[code].get(_key, _row[0]) for code in EXTRA_NAMES)

@lru_cache(maxsize=1)
def _locale_cache():
    path = ROOT / 'instance' / 'locale_overrides.json'
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def translated_override(language: str, key: str) -> str | None:
    catalog = _locale_cache().get(language, {})
    value = catalog.get(key) if isinstance(catalog, dict) else None
    return value if isinstance(value, str) and value.strip() else None


def locale_coverage(language: str) -> tuple[int, int]:
    """Number of localized items, never claim full support from English fallback."""
    if language in {'en', 'hi', 'mr', 'es'}:
        return len(C), len(C)
    overrides = _locale_cache().get(language, {})
    extra = EXTRA_TEXT.get(language, {})
    total = len(C)
    return sum(1 for key in C if key in extra or (isinstance(overrides, dict) and key in overrides)), total


def reload_locale_cache():
    _locale_cache.cache_clear()


def event_label(raw: str, language: str = 'en') -> str:
    key = 'event_' + raw
    return t(key, language) if key in C else raw.replace('_', ' ')

def t(key: str, language: str = 'en', **params) -> str:
    """Translate UI labels with strict locale coverage and safe formatting."""
    if language not in LANGUAGES:
        language = 'en'
    row = C.get(key)
    if row is None:
        raise KeyError(f'Unknown UI translation key: {key}')
    value = row[tuple(LANGUAGES).index(language)]
    override = translated_override(language, key)
    if override:
        value = override
    return value.format(**params) if params else value


def supported(code: str) -> str:
    return code if code in LANGUAGES else 'en'


def local_status(value: str, language='en') -> str:
    key = {'Within stated range': 'status_in', 'High': 'status_high',
           'Low': 'status_low', 'Not evaluated': 'status_uneval'}.get(value, 'status_uneval')
    return t(key, language)
