"""Curated core UI translations for additional languages.

The original English, Hindi, Marathi and Spanish catalogs remain fully curated.
Additional locales use these safe core labels and English fallback until the optional
local Ollama pack generator has completed remaining translations. This module has
no network access, no access to user data and no third-party translation API.
"""
EXTRA_NAMES = {
    'fr': '🇫🇷 Français', 'de': '🇩🇪 Deutsch',
    'ja': '🇯🇵 日本語', 'zh': '🇨🇳 简体中文',
    'pt': '🇵🇹 Português', 'ru': '🇷🇺 Русский',
    'ar': '🇸🇦 العربية', 'bn': '🇧🇩 বাংলা',
    'ta': '🇮🇳 தமிழ்', 'te': '🇮🇳 తెలుగు',
}
EXTRA_VOICES = {
    'fr': 'fr-FR', 'de': 'de-DE', 'ja': 'ja-JP', 'zh': 'zh-CN',
    'pt': 'pt-PT', 'ru': 'ru-RU', 'ar': 'ar-SA', 'bn': 'bn-IN',
    'ta': 'ta-IN', 'te': 'te-IN',
}
# Columns in this exact order: fr, de, ja, zh, pt, ru, ar, bn, ta, te.
_KEYS = list(EXTRA_NAMES)
CORE = {
'home': ['Tableau de bord','Übersicht','ダッシュボード','仪表盘','Painel','Панель','لوحة التحكم','ড্যাশবোর্ড','முகப்புப் பலகை','డాష్‌బోర్డ్'],
'chat': ['Assistant santé IA','KI-Gesundheitsassistent','AI健康アシスタント','AI 健康助手','Assistente de saúde IA','ИИ-помощник по здоровью','مساعد الصحة بالذكاء الاصطناعي','এআই স্বাস্থ্য সহায়ক','AI சுகாதார உதவியாளர்','AI ఆరోగ్య సహాయకుడు'],
'reports': ['Analyse des rapports','Befundanalyse','検査結果の分析','报告分析','Análise de relatórios','Анализ анализов','تحليل التقارير','রিপোর্ট বিশ্লেষণ','அறிக்கை பகுப்பாய்வு','నివేదిక విశ్లేషణ'],
'voice': ['Assistant vocal','Sprachassistent','音声アシスタント','语音助手','Assistente de voz','Голосовой помощник','المساعد الصوتي','ভয়েস সহায়ক','குரல் உதவியாளர்','వాయిస్ సహాయకుడు'],
'history': ['Mon historique','Mein Verlauf','履歴','我的历史记录','O meu histórico','Моя история','سجلي','আমার ইতিহাস','எனது வரலாறு','నా చరిత్ర'],
'insights': ['Indicateurs de santé','Gesundheitsübersicht','健康インサイト','健康洞察','Indicadores de saúde','Показатели здоровья','مؤشرات الصحة','স্বাস্থ্য তথ্য','உடல்நலத் தகவல்கள்','ఆరోగ్య సమాచారం'],
'profile': ['Mon profil','Mein Profil','プロフィール','我的资料','O meu perfil','Мой профиль','ملفي الشخصي','আমার প্রোফাইল','எனது சுயவிவரம்','నా ప్రొఫైల్'],
'about': ['À propos du projet','Über das Projekt','プロジェクトについて','关于项目','Sobre o projeto','О проекте','حول المشروع','প্রকল্প সম্পর্কে','திட்டம் பற்றி','ప్రాజెక్ట్ గురించి'],
'overview': ['Vue d’ensemble','Übersicht','概要','概览','Visão geral','Обзор','نظرة عامة','সংক্ষিপ্ত বিবরণ','மேலோட்டம்','అవలోకనం'],
'users': ['Utilisateurs','Benutzer','ユーザー','用户','Utilizadores','Пользователи','المستخدمون','ব্যবহারকারী','பயனர்கள்','వినియోగదారులు'],
'admin_reports': ['Tous les rapports','Alle Berichte','すべてのレポート','全部报告','Todos os relatórios','Все отчёты','جميع التقارير','সব রিপোর্ট','அனைத்து அறிக்கைகள்','అన్ని నివేదికలు'],
'conversations': ['Conversations','Unterhaltungen','会話','对话记录','Conversas','Диалоги','المحادثات','কথোপকথন','உரையாடல்கள்','సంభాషణలు'],
'audit': ["Journal d'accès",'Zugriffsprotokoll','アクセスログ','访问日志','Registo de acesso','Журнал доступа','سجل الوصول','প্রবেশ লগ்','அணுகல் பதிவு','యాక్సెస్ లాగ్'],
'logout': ['Se déconnecter','Abmelden','ログアウト','退出登录','Terminar sessão','Выйти','تسجيل الخروج','লগ আউট','வெளியேறு','లాగ్ అవుట్'],
'sidebar_user_portal': ['ESPACE UTILISATEUR','BENUTZERBEREICH','ユーザーポータル','用户入口','ÁREA DO UTILIZADOR','РАЗДЕЛ ПОЛЬЗОВАТЕЛЯ','بوابة المستخدم','ব্যবহারকারী বিভাগ','பயனர் பகுதி','వినియోగదారు విభాగం'],
'sidebar_admin_portal': ['ADMINISTRATION','ADMINISTRATORBEREICH','管理者ポータル','管理员入口','ADMINISTRAÇÃO','РАЗДЕЛ АДМИНИСТРАТОРА','بوابة المسؤول','অ্যাডমিন বিভাগ','நிர்வாகப் பகுதி','అడ్మిన్ విభాగం'],
'sidebar_project': ['PROJET','PROJEKT','プロジェクト','项目','PROJETO','ПРОЕКТ','المشروع','প্রকল্প','திட்டம்','ప్రాజెక్ట్'],
'sidebar_preferences': ['LANGUE ET APPARENCE','SPRACHE UND DESIGN','言語と表示','语言与外观','IDIOMA E APARÊNCIA','ЯЗЫК И ОФОРМЛЕНИЕ','اللغة والمظهر','ভাষা ও চেহারা','மொழி மற்றும் தோற்றம்','భాష మరియు రూపం'],
'sidebar_language_label': ["Langue de l'interface",'Sprache der Oberfläche','表示言語','界面语言','Idioma da interface','Язык интерфейса','لغة الواجهة','ইন্টারফেসের ভাষা','இடைமுக மொழி','ఇంటర్‌ఫేస్ భాష'],
'sidebar_light_theme': ['Thème clair','Helles Design','ライトモード','浅色主题','Tema claro','Светлая тема','الوضع الفاتح','হালকা থিম','வெளிர் தீம்','లైట్ థీమ్'],
'guest_user_login': ['Connexion utilisateur','Benutzeranmeldung','ユーザーログイン','用户登录','Iniciar sessão','Вход пользователя','دخول المستخدم','ব্যবহারকারী লগইন','பயனர் உள்நுழைவு','వినియోగదారు లాగిన్'],
'guest_register': ['Créer un compte','Konto erstellen','新規登録','创建用户账户','Criar conta','Создать аккаунт','إنشاء حساب','অ্যাকাউন্ট তৈরি করুন','கணக்கு உருவாக்கு','ఖాతా సృష్టించండి'],
'guest_admin_login': ['Connexion administrateur','Administratoranmeldung','管理者ログイン','管理员登录','Início de sessão do administrador','Вход администратора','دخول المسؤول','অ্যাডমিন লগইন','நிர்வாகி உள்நுழைவு','అడ్మిన్ లాగిన్'],
'guest_user_login_desc': ['Connectez-vous en toute sécurité à votre espace santé.','Melden Sie sich sicher in Ihrem Gesundheitsbereich an.','安全に個人の健康スペースへログインします。','安全登录您的个人健康空间。','Entre com segurança no seu espaço de saúde.','Войдите в личный раздел здоровья.','سجّل الدخول بأمان إلى مساحتك الصحية.','আপনার ব্যক্তিগত স্বাস্থ্য বিভাগে নিরাপদে লগইন করুন।','உங்கள் சுகாதாரப் பகுதிக்குப் பாதுகாப்பாக உள்நுழையுங்கள்.','మీ వ్యక్తిగత ఆరోగ్య స్థలంలో సురక్షితంగా ప్రవేశించండి.'],
'guest_register_desc': ['Créez un compte pour poser des questions et analyser vos rapports.','Erstellen Sie ein Konto für Fragen und die Analyse von Befunden.','質問や検査結果の分析のためにアカウントを作成してください。','创建账户，以便提问并分析检查报告。','Crie uma conta para fazer perguntas e analisar relatórios.','Создайте аккаунт для вопросов и анализа отчётов.','أنشئ حسابًا لطرح الأسئلة وتحليل التقارير.','প্রশ্ন করতে ও রিপোর্ট বিশ্লেষণ করতে অ্যাকাউন্ট খুলুন।','கேள்விகள் கேட்கவும் அறிக்கைகளைப் பகுப்பாய்வு செய்யவும் கணக்கு உருவாக்குங்கள்.','ప్రశ్నలు అడగడానికి, నివేదికలు విశ్లేషించడానికి ఖాతా సృష్టించండి.'],
'guest_admin_login_desc': ['Accès réservé à l’administrateur permanent.','Zugang nur für den ständigen Administrator.','常設の管理者専用です。','仅限常设管理员访问。','Acesso reservado ao administrador permanente.','Доступ только для постоянного администратора.','الدخول للمسؤول الدائم فقط.','শুধু স্থায়ী অ্যাডমিনের প্রবেশাধিকার।','நிரந்தர நிர்வாகிக்கு மட்டுமே அனுமதி.','శాశ్వత నిర్వాహకుడికి మాత్రమే ప్రవేశం.'],
'field_username': ["Nom d'utilisateur",'Benutzername','ユーザー名','用户名','Nome de utilizador','Имя пользователя','اسم المستخدم','ব্যবহারকারীর নাম','பயனர் பெயர்','వినియోగదారు పేరు'],
'field_password': ['Mot de passe','Passwort','パスワード','密码','Palavra-passe','Пароль','كلمة المرور','পাসওয়ার্ড','கடவுச்சொல்','పాస్‌వర్డ్'],
'field_full_name': ['Nom complet','Vollständiger Name','氏名','姓名','Nome completo','Полное имя','الاسم الكامل','পুরো নাম','முழுப் பெயர்','పూర్తి పేరు'],
'field_choose_username': ["Choisir un nom d'utilisateur",'Benutzernamen wählen','ユーザー名を選択','选择用户名','Escolher nome de utilizador','Выберите имя пользователя','اختر اسم المستخدم','ব্যবহারকারীর নাম বেছে নিন','பயனர் பெயரைத் தேர்ந்தெடுக்கவும்','వినియోగదారు పేరును ఎంచుకోండి'],
'field_email': ['Adresse e-mail','E-Mail-Adresse','メールアドレス','电子邮箱','Endereço de e-mail','Электронная почта','البريد الإلكتروني','ইমেইল ঠিকানা','மின்னஞ்சல் முகவரி','ఈమెయిల్ చిరునామా'],
'field_confirm_password': ['Confirmer le mot de passe','Passwort bestätigen','パスワードの確認','确认密码','Confirmar palavra-passe','Подтвердите пароль','تأكيد كلمة المرور','পাসওয়ার্ড নিশ্চিত করুন','கடவுச்சொல்லை உறுதிப்படுத்தவும்','పాస్‌వర్డ్ నిర్ధారించండి'],
'field_preferred_language': ['Langue préférée','Bevorzugte Sprache','希望する言語','首选语言','Idioma preferido','Предпочитаемый язык','اللغة المفضلة','পছন্দের ভাষা','விருப்ப மொழி','ఇష్టమైన భాష'],
'field_admin_password': ['Mot de passe administrateur','Administratorpasswort','管理者パスワード','管理员密码','Palavra-passe do administrador','Пароль администратора','كلمة مرور المسؤول','অ্যাডমিন পাসওয়ার্ড','நிர்வாகி கடவுச்சொல்','అడ్మిన్ పాస్‌వర్డ్'],
'action_sign_in': ['Se connecter en sécurité','Sicher anmelden','安全にログイン','安全登录','Iniciar sessão em segurança','Безопасный вход','تسجيل الدخول بأمان','নিরাপদে লগইন করুন','பாதுகாப்பாக உள்நுழைக','సురక్షితంగా లాగిన్ అవ్వండి'],
'action_create_account': ['Créer mon compte','Mein Konto erstellen','アカウントを作成','创建我的账户','Criar a minha conta','Создать мой аккаунт','إنشاء حسابي','আমার অ্যাকাউন্ট তৈরি করুন','என் கணக்கை உருவாக்கு','నా ఖాతాను సృష్టించండి'],
'action_admin_login': ["Ouvrir l'administration",'Adminbereich öffnen','管理画面を開く','打开管理员面板','Abrir painel de administração','Открыть панель администратора','فتح لوحة الإدارة','অ্যাডমিন প্যানেল খুলুন','நிர்வாகப் பலகையைத் திற','అడ్మిన్ ప్యానల్ తెరవండి'],
'guest_welcome_line': ['Vos questions de santé, expliquées simplement.','Ihre Gesundheitsfragen, einfach erklärt.','健康の疑問をわかりやすく解説。','简单解答您的健康疑问。','As suas dúvidas de saúde, explicadas com clareza.','Понятные ответы на вопросы о здоровье.','أسئلتك الصحية بإجابات واضحة.','স্বাস্থ্য সংক্রান্ত প্রশ্নের সহজ উত্তর।','உங்கள் உடல்நலக் கேள்விகளுக்கு எளிய விளக்கம்.','మీ ఆరోగ్య ప్రశ్నలకు సులభమైన సమాధానాలు.'],
'guest_welcome_desc': ['Comprenez les maladies et analyses dans votre langue avec une IA locale.','Verstehen Sie Befunde und Gesundheitsthemen in Ihrer Sprache.','ローカルAIで病気や検査を母語で理解できます。','借助本地 AI，以您的语言了解疾病与检查结果。','Compreenda condições e exames na sua língua com IA local.','Изучайте анализы и заболевания на своём языке с локальным ИИ.','افهم الحالات والفحوصات بلغتك باستخدام ذكاء اصطناعي محلي.','স্থানীয় এআই দিয়ে নিজের ভাষায় রোগ ও পরীক্ষা বুঝুন।','உள்ளூர் AI உதவியுடன் உங்கள் மொழியில் நோய்களையும் பரிசோதனைகளையும் புரிந்துகொள்ளுங்கள்.','స్థానిక AI సహాయంతో మీ భాషలో వ్యాధులు, పరీక్షలను అర్థం చేసుకోండి.'],
'hero_eyebrow': ['CONSEILS SANTÉ AVEC IA','KI-GESTÜTZTE GESUNDHEITSINFOS','AIによる健康情報','AI 驱动的健康知识','SAÚDE COM IA','ИНФОРМАЦИЯ О ЗДОРОВЬЕ С ИИ','معلومات صحية مدعومة بالذكاء الاصطناعي','এআই স্বাস্থ্য তথ্য','AI சுகாதாரத் தகவல்','AI ఆరోగ్య సమాచారం'],
'hero_title_1': ['La santé intelligente,','Intelligente Gesundheitsinfos,','医療情報を','智能健康资讯，','Saúde inteligente,','Здоровье и знания,','رعاية صحية ذكية،','সহজ স্বাস্থ্য তথ্য,','தெளிவான மருத்துவத் தகவல்,','సులభమైన ఆరోగ్య సమాచారం,'],
'hero_title_2': ['expliquée simplement.','einfach erklärt.','やさしく解説。','简单易懂。','explicada com clareza.','простыми словами.','بشرح مبسط.','সহজ ব্যাখ্যায়।','எளிய விளக்கத்தில்.','సులభ వివరణతో.'],
'hero_chip_1': ['IA multilingue','Mehrsprachige KI','多言語AI','多语言 AI','IA multilingue','Многоязычный ИИ','ذكاء اصطناعي متعدد اللغات','বহুভাষিক এআই','பன்மொழி AI','బహుభాషా AI'],
'hero_chip_2': ['IA locale • Ollama','Lokale KI • Ollama','ローカルAI • Ollama','本地 AI • Ollama','IA local • Ollama','Локальный ИИ • Ollama','ذكاء اصطناعي محلي • Ollama','স্থানীয় এআই • Ollama','உள்ளூர் AI • Ollama','స్థానిక AI • Ollama'],
'hero_chip_3': ['Éducation santé','Gesundheitsbildung','健康に関する学習','健康教育','Educação em saúde','Медицинское просвещение','تثقيف صحي','স্বাস্থ্য শিক্ষা','சுகாதாரக் கல்வி','ఆరోగ్య అవగాహన'],
'caution': ['Informations éducatives uniquement — pas un diagnostic.','Nur zur Information – keine Diagnose.','教育目的の情報であり診断ではありません。','仅用于健康教育，并非医疗诊断。','Apenas informação educativa — não é diagnóstico.','Только справочная информация — не диагноз.','للتثقيف فقط، وليس تشخيصًا طبيًا.','শুধু শিক্ষামূলক তথ্য — চিকিৎসা নির্ণয় নয়।','கல்விக்காக மட்டுமே — மருத்துவ நோயறிதல் அல்ல.','విద్యా సమాచారం మాత్రమే — వైద్య నిర్ధారణ కాదు.'],
'emergency': ["En cas d'urgence, contactez immédiatement les secours.",'Bei akuten Symptomen sofort den Notruf wählen.','緊急の症状がある場合は直ちに救急サービスへ。','出现紧急症状时请立即联系急救服务。','Em caso de urgência, contacte os serviços de emergência.','При опасных симптомах немедленно обращайтесь за экстренной помощью.','عند ظهور أعراض طارئة، اتصل بالطوارئ فورًا.','জরুরি উপসর্গে অবিলম্বে জরুরি সেবার সাহায্য নিন।','அவசர அறிகுறிகள் ஏற்பட்டால் உடனடியாக அவசர சேவைகளை அணுகவும்.','అత్యవసర లక్షణాలుంటే వెంటనే అత్యవసర సేవలను సంప్రదించండి.'],
'about_title': ['À propos de Healthcare Info Assistant','Über Healthcare Info Assistant','Healthcare Info Assistant について','关于 Healthcare Info Assistant','Sobre Healthcare Info Assistant','О Healthcare Info Assistant','حول Healthcare Info Assistant','Healthcare Info Assistant সম্পর্কে','Healthcare Info Assistant பற்றி','Healthcare Info Assistant గురించి'],
'about_overline': ['NOTRE OBJECTIF','UNSER ZIEL','私たちの目的','我们的宗旨','O NOSSO OBJETIVO','НАША ЦЕЛЬ','هدفنا','আমাদের লক্ষ্য','எங்கள் நோக்கம்','మా లక్ష్యం'],
'brand_specialty': ['IA • SANTÉ','KI • MEDIZINTECHNIK','AI • 医療技術','AI • 医疗科技','IA • SAÚDE','ИИ • МЕДТЕХ','الذكاء الاصطناعي • التقنية الطبية','এআই • মেডটেক','AI • மருத்துவத் தொழில்நுட்பம்','AI • మెడ్‌టెక్'],
'status_high': ['Élevé','Hoch','高い','偏高','Elevado','Высокий','مرتفع','বেশি','அதிகம்','అధికం'],
'status_low': ['Faible','Niedrig','低い','偏低','Baixo','Низкий','منخفض','কম','குறைவு','తక్కువ'],
'status_in': ['Dans la plage indiquée','Im angegebenen Bereich','記載範囲内','在报告参考范围内','Dentro do intervalo indicado','В указанном диапазоне','ضمن المدى المذكور','উল্লিখিত সীমার মধ্যে','குறிப்பிட்ட வரம்பில்','ఇచ్చిన పరిధిలో'],
'status_uneval': ['Non évalué','Nicht bewertet','未評価','未评估','Não avaliado','Не оценено','لم يُقيّم','মূল্যায়িত নয়','மதிப்பிடப்படவில்லை','మూల్యాంకనం చేయలేదు'],
'play': ['Écouter','Abspielen','再生','播放','Ouvir','Воспроизвести','تشغيل','শুনুন','ஒலிக்கச் செய்','వినండి'],
'stop': ['Arrêter','Stopp','停止','停止','Parar','Остановить','إيقاف','থামান','நிறுத்து','ఆపు'],
'speed': ['Vitesse','Tempo','速度','语速','Velocidade','Скорость','السرعة','গতি','வேகம்','వేగం'],
'admin_overview': ["Centre d'administration",'Verwaltungszentrale','管理センター','管理中心','Centro de administração','Центр управления','مركز الإدارة','প্রশাসন কেন্দ্র','நிர்வாக மையம்','నిర్వాహక కేంద్రం'],
'profile_save': ['Enregistrer le profil','Profil speichern','プロフィールを保存','保存资料','Guardar perfil','Сохранить профиль','حفظ الملف الشخصي','প্রোফাইল সংরক্ষণ করুন','சுயவிவரத்தைச் சேமி','ప్రొఫైల్‌ను సేవ్ చేయండి'],
'action_delete': ['Supprimer','Löschen','削除','删除','Eliminar','Удалить','حذف','মুছুন','நீக்கு','తొలగించు'],
'empty': ['Aucun résultat pour le moment.','Noch keine Einträge.','まだ記録がありません。','暂无记录。','Ainda não há registos.','Пока нет записей.','لا توجد سجلات بعد.','এখনও কোনো রেকর্ড নেই।','இன்னும் பதிவுகள் இல்லை.','ఇంకా రికార్డులు లేవు.'],
}
CORE.update({
'hero_desc': [
    "Comprenez les problèmes de santé, la nutrition et les rapports médicaux grâce à une IA locale — privée, multilingue et accessible.",
    'Verstehen Sie Erkrankungen, Ernährung und medizinische Befunde mit lokaler KI — privat, mehrsprachig und verständlich.',
    'ローカルAIで、健康状態、栄養、検査結果を分かりやすく理解できます。プライバシーと多言語対応を重視しています。',
    '通过本地 AI 了解健康状况、营养知识和医疗报告，注重隐私、多语言和易读性。',
    'Compreenda condições de saúde, nutrição e relatórios médicos com IA local — privada e multilingue.',
    'Узнавайте о здоровье, питании и медицинских анализах с локальным ИИ — конфиденциально и понятно.',
    'افهم الحالات الصحية والتغذية والتقارير الطبية باستخدام ذكاء اصطناعي محلي يدعم عدة لغات ويحترم الخصوصية.',
    'স্থানীয় এআই দিয়ে স্বাস্থ্য, পুষ্টি এবং পরীক্ষার রিপোর্ট সহজে বুঝুন — ব্যক্তিগত ও বহুভাষিক।',
    'உள்ளூர் AI மூலம் உடல்நலம், ஊட்டச்சத்து, மருத்துவ அறிக்கைகளை எளிதாகப் புரிந்துகொள்ளுங்கள்.',
    'స్థానిక AI తో ఆరోగ్య పరిస్థితులు, పోషణ మరియు వైద్య నివేదికలను సులభంగా అర్థం చేసుకోండి.'
],
'field_consent': [
    "J’autorise l’administrateur permanent 'Mr. Doc' à accéder à mes données de compte, au texte des rapports médicaux enregistrés, aux réponses de l’IA et à l’historique des conversations. Ce logiciel est éducatif et non un service médical confidentiel.",
    "Ich willige ein, dass der ständige Administrator 'Mr. Doc' auf meine gespeicherten Kontodaten, extrahierten medizinischen Berichte, KI-Antworten und Gesprächsverläufe zugreifen darf. Dies ist Lernsoftware und keine vertrauliche medizinische Behandlung.",
    "常設管理者 'Mr. Doc' が保存されたアカウント情報、医療レポートから抽出した文章、AIの回答、会話履歴にアクセスすることに同意します。このソフトウェアは教育目的であり、秘密保持された診療サービスではありません。",
    "我同意常设管理员 'Mr. Doc' 查看我保存的账户信息、医疗报告提取文本、AI 回复及对话记录。本软件仅用于教育，不提供保密的临床医疗服务。",
    "Autorizo o administrador permanente 'Mr. Doc' a consultar dados da conta, textos extraídos de relatórios médicos, respostas da IA e histórico de conversas. Este software é educativo, não é um serviço clínico confidencial.",
    "Я разрешаю постоянному администратору 'Mr. Doc' просматривать сохранённые данные моего аккаунта, тексты медицинских отчётов, ответы ИИ и историю бесед. Это образовательное ПО, а не конфиденциальная медицинская помощь.",
    "أوافق على وصول المسؤول الدائم 'Mr. Doc' إلى بيانات حسابي المحفوظة ونصوص التقارير الطبية المستخرجة وردود الذكاء الاصطناعي وسجل المحادثات. هذا برنامج تعليمي وليس خدمة رعاية طبية سرية.",
    "স্থায়ী প্রশাসক 'Mr. Doc' আমার সংরক্ষিত অ্যাকাউন্ট তথ্য, চিকিৎসা রিপোর্টের লেখা, এআই উত্তর এবং কথোপকথনের ইতিহাস দেখতে পারবেন — এতে আমি সম্মতি দিচ্ছি। এটি শিক্ষামূলক সফটওয়্যার, গোপনীয় চিকিৎসাসেবা নয়।",
    "நிரந்தர நிர்வாகியான 'Mr. Doc' எனது சேமிக்கப்பட்ட கணக்குத் தகவல், மருத்துவ அறிக்கையிலிருந்து எடுக்கப்பட்ட உரை, AI பதில்கள் மற்றும் உரையாடல் வரலாற்றைப் பார்வையிட நான் ஒப்புக்கொள்கிறேன். இது கல்வி மென்பொருள்; ரகசிய மருத்துவச் சேவை அல்ல.",
    "శాశ్వత నిర్వాహకుడు 'Mr. Doc' నా నిల్వ చేసిన ఖాతా వివరాలు, వైద్య నివేదికల పాఠ్యం, AI జవాబులు, సంభాషణ చరిత్రను చూడటానికి నేను అంగీకరిస్తున్నాను. ఇది విద్యా సాఫ్ట్‌వేర్ మాత్రమే, గోప్య వైద్య సేవ కాదు."
],
'consent_intro': [
    'Veuillez lire le consentement. L’administrateur peut accéder à vos informations médicales enregistrées.',
    'Bitte lesen Sie die Einwilligung. Der Administrator kann gespeicherte Gesundheitsdaten einsehen.',
    '同意内容をご確認ください。管理者は保存された健康情報にアクセスできます。',
    '请仔细阅读同意条款。管理员可访问您保存的健康信息。',
    'Leia o consentimento. O administrador pode aceder às informações de saúde guardadas.',
    'Прочитайте согласие: администратор может просматривать сохранённые данные о здоровье.',
    'يُرجى قراءة الموافقة: يمكن للمسؤول الاطلاع على معلوماتك الصحية المحفوظة.',
    'সম্মতির শর্ত পড়ুন। প্রশাসক আপনার সংরক্ষিত স্বাস্থ্য তথ্য দেখতে পারবেন।',
    'ஒப்புதலைப் படிக்கவும். சேமிக்கப்பட்ட உடல்நலத் தகவலை நிர்வாகி பார்க்க முடியும்.',
    'సమ్మతిని చదవండి. నిల్వ చేసిన ఆరోగ్య సమాచారాన్ని నిర్వాహకుడు చూడగలరు.'
],
'sidebar_user_portal_help': [
    'Votre espace santé privé','Ihr persönlicher Gesundheitsbereich','個人の健康スペース','您的私人健康空间','O seu espaço de saúde','Личный раздел здоровья','مساحتك الصحية الخاصة','আপনার ব্যক্তিগত স্বাস্থ্য স্থান','உங்கள் தனிப்பட்ட சுகாதாரப் பகுதி','మీ వ్యక్తిగత ఆరోగ్య స్థలం'
],
'sidebar_admin_portal_help': [
    'Accès réservé au personnel autorisé','Zugriff nur für Berechtigte','権限のある管理者のみ','仅限授权管理人员','Acesso autorizado','Доступ только для уполномоченных','وصول الإدارة المصرح به','শুধু অনুমোদিত পরিচালনার জন্য','அங்கீகரிக்கப்பட்ட நிர்வாக அணுகல்','అధికారిక నిర్వహణ ప్రవేశం'
],
'sidebar_project_help': [
    'Découvrez les fonctions de cet assistant','Was der Assistent kann','このアシスタントの機能','了解本助手的功能','Conheça o assistente','Возможности помощника','تعرّف على وظائف المساعد','এই সহায়কের কাজগুলো','இந்த உதவியாளரின் பயன்பாடுகள்','సహాయకుని ఉపయోగాలు'
],
'sidebar_preferences_help': [
    'Personnalisez votre expérience','Passen Sie Ihre Ansicht an','表示をカスタマイズ','个性化您的体验','Personalize a sua experiência','Настройте оформление','خصّص تجربتك','নিজের পছন্দ অনুযায়ী সাজান','உங்கள் விருப்பத்தை அமைக்கவும்','మీ అభిరుచులకు అనుగుణంగా మార్చుకోండి'
],
'about_desc': [
    'Votre compagnon intelligent pour mieux comprendre la santé.','Ihr intelligenter Begleiter für Gesundheitsinformationen.','健康情報を理解するためのインテリジェントなパートナー。','您的智能健康信息助手。','O seu companheiro inteligente de informação de saúde.','Ваш интеллектуальный помощник по вопросам здоровья.','رفيقك الذكي لفهم المعلومات الصحية.','স্বাস্থ্য তথ্য বোঝার বুদ্ধিমান সহকারী।','உங்கள் அறிவார்ந்த சுகாதாரத் தகவல் துணை.','మీ తెలివైన ఆరోగ్య సమాచార సహచరుడు.'
],
'hero_stamp': [
    'IA SANTÉ LOCALE','LOKALE GESUNDHEITS-KI','ローカル医療AI','本地健康 AI','IA LOCAL DE SAÚDE','ЛОКАЛЬНЫЙ ИИ ЗДОРОВЬЯ','الذكاء الاصطناعي الصحي المحلي','স্থানীয় স্বাস্থ্য এআই','உள்ளூர் சுகாதார AI','స్థానిక ఆరోగ్య AI'
],
'sidebar_trust': [
    'IA locale · Informations santé éducatives','Lokale KI · Gesundheitsinformationen','ローカルAI・健康学習用','本地 AI · 健康教育','IA local · Educação para a saúde','Локальный ИИ · Справка о здоровье','ذكاء اصطناعي محلي · تثقيف صحي','স্থানীয় এআই · স্বাস্থ্য শিক্ষা','உள்ளூர் AI · சுகாதாரக் கல்வி','స్థానిక AI · ఆరోగ్య అవగాహన'
],
'sidebar_account_secure': [
    'Compte protégé','Geschütztes Konto','保護されたアカウント','受保护账户','Conta protegida','Защищённый аккаунт','حساب محمي','সুরক্ষিত অ্যাকাউন্ট','பாதுகாக்கப்பட்ட கணக்கு','సురక్షిత ఖాతా'
],
'admin_login_intro': [
    "Administrateur permanent : **{username}**. L'inscription publique d'administrateur est désactivée.",
    'Ständiger Administrator: **{username}**. Öffentliche Admin-Registrierung ist deaktiviert.',
    '常設管理者：**{username}**。一般向けの管理者登録はできません。',
    '常设管理员：**{username}**。不允许公开注册管理员。',
    'Administrador permanente: **{username}**. O registo público de administradores está desativado.',
    'Постоянный администратор: **{username}**. Регистрация администраторов закрыта.',
    'المسؤول الدائم: **{username}**. تسجيل المسؤولين للعامة غير متاح.',
    'স্থায়ী প্রশাসক: **{username}**। নতুন অ্যাডমিন নিবন্ধন বন্ধ।',
    'நிரந்தர நிர்வாகி: **{username}**. பொதுவான நிர்வாகி பதிவு முடக்கப்பட்டுள்ளது.',
    'శాశ్వత నిర్వాహకుడు: **{username}**. పబ్లిక్ అడ్మిన్ నమోదు అందుబాటులో లేదు.'
],
'field_new_password': [
    'Mot de passe (10 caractères minimum, lettres et chiffres)',
    'Passwort (mind. 10 Zeichen, Buchstaben und Zahlen)',
    'パスワード（10文字以上、英数字）','密码（至少10个字符，包含字母和数字）',
    'Palavra-passe (10+ caracteres, letras e números)',
    'Пароль (не менее 10 символов, буквы и цифры)',
    'كلمة المرور (10 أحرف على الأقل تشمل حروفًا وأرقامًا)',
    'পাসওয়ার্ড (অন্তত ১০ অক্ষর, বর্ণ ও সংখ্যা)',
    'கடவுச்சொல் (10 எழுத்துகளுக்கு மேல், எழுத்துகள் மற்றும் எண்கள்)',
    'పాస్‌వర్డ్ (కనీసం 10 అక్షరాలు, అక్షరాలు మరియు సంఖ్యలు)'
],
'error_login': [
    'Identifiants incorrects ou compte désactivé.',
    'Falsche Anmeldedaten oder gesperrtes Konto.',
    'ログイン情報が正しくないか、アカウントが無効です。',
    '登录信息错误或账户已停用。',
    'Dados incorretos ou conta desativada.',
    'Неверные данные или аккаунт отключён.',
    'بيانات الدخول غير صحيحة أو الحساب معطّل.',
    'ভুল তথ্য বা অ্যাকাউন্ট নিষ্ক্রিয়।',
    'தவறான உள்நுழைவுத் தகவல் அல்லது முடக்கப்பட்ட கணக்கு.',
    'లాగిన్ వివరాలు తప్పు లేదా ఖాతా నిలిపివేయబడింది.'
],
})

EXTRA_TEXT = {code: {key: values[idx] for key,values in CORE.items()}
              for idx,code in enumerate(_KEYS)}
