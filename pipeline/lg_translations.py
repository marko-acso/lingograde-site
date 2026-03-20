"""
LingoGrade Translations Module — All supported languages.
Import this in lingograde_docx.py and lg_send.py.
"""

# Language code mapping from native language name (German, English, or native)
LANG_CODES = {
    # German names
    "Russisch": "ru", "Ukrainisch": "uk", "Französisch": "fr", "Spanisch": "es",
    "Italienisch": "it", "Serbisch": "sr", "Kroatisch": "hr", "Englisch": "en",
    "Bulgarisch": "bg", "Polnisch": "pl", "Portugiesisch": "pt", "Tschechisch": "cs",
    "Ungarisch": "hu", "Norwegisch": "no", "Schwedisch": "sv", "Finnisch": "fi",
    "Dänisch": "da", "Niederländisch": "nl", "Flämisch": "nl", "Türkisch": "tr",
    "Albanisch": "sq", "Rumänisch": "ro", "Rätoromanisch": "rm", "Arabisch": "ar",
    "Hindi": "hi", "Afrikaans": "af", "Griechisch": "el", "Japanisch": "ja",
    "Koreanisch": "ko", "Chinesisch": "zh",
    # English names
    "Russian": "ru", "Ukrainian": "uk", "French": "fr", "Spanish": "es",
    "Italian": "it", "Serbian": "sr", "Croatian": "hr", "English": "en",
    "Bulgarian": "bg", "Polish": "pl", "Portuguese": "pt", "Czech": "cs",
    "Hungarian": "hu", "Norwegian": "no", "Swedish": "sv", "Finnish": "fi",
    "Danish": "da", "Dutch": "nl", "Flemish": "nl", "Turkish": "tr",
    "Albanian": "sq", "Romanian": "ro", "Romansh": "rm", "Arabic": "ar",
    "Hindi": "hi", "Afrikaans": "af", "Greek": "el", "Japanese": "ja",
    "Korean": "ko", "Chinese": "zh",
    # Native script names
    "Русский": "ru", "Українська": "uk", "Français": "fr", "Español": "es",
    "Italiano": "it", "Српски": "sr", "Hrvatski": "hr", "Български": "bg",
    "Polski": "pl", "Português": "pt", "Čeština": "cs", "Magyar": "hu",
    "Norsk": "no", "Svenska": "sv", "Suomi": "fi", "Dansk": "da",
    "Nederlands": "nl", "Türkçe": "tr", "Shqip": "sq", "Română": "ro",
    "Rumantsch": "rm", "العربية": "ar", "हिन्दी": "hi", "Ελληνικά": "el",
}

# ═══════════════════════════════════════════════════════
# TERM TRANSLATIONS (error classes, stability, labels)
# ═══════════════════════════════════════════════════════
TRANSLATIONS = {
    # ── Language names ──
    "Russisch":       {"en": "Russian",    "ru": "Русский",     "uk": "Російська",   "fr": "Russe",       "es": "Ruso",        "it": "Russo",       "sr": "Руски",       "hr": "Ruski",       "bg": "Руски",       "pl": "Rosyjski",    "pt": "Russo",       "cs": "Ruský",       "hu": "Orosz",       "no": "Russisk",     "sv": "Ryska",       "fi": "Venäjä",      "da": "Russisk",     "nl": "Russisch",    "tr": "Rusça",       "sq": "Rusisht",     "ro": "Rusă",        "ar": "الروسية",      "hi": "रूसी",         "af": "Russies",     "el": "Ρωσικά"},
    "Englisch":       {"en": "English",    "ru": "Английский",  "uk": "Англійська",  "fr": "Anglais",     "es": "Inglés",      "it": "Inglese",     "sr": "Енглески",    "hr": "Engleski",    "bg": "Английски",   "pl": "Angielski",   "pt": "Inglês",      "cs": "Anglický",    "hu": "Angol",       "no": "Engelsk",     "sv": "Engelska",    "fi": "Englanti",    "da": "Engelsk",     "nl": "Engels",      "tr": "İngilizce",   "sq": "Anglisht",    "ro": "Engleză",     "ar": "الإنجليزية",    "hi": "अंग्रेज़ी",     "af": "Engels",      "el": "Αγγλικά"},
    "Französisch":    {"en": "French",     "ru": "Французский", "uk": "Французька",  "fr": "Français",    "es": "Francés",     "it": "Francese",    "sr": "Француски",   "hr": "Francuski",   "bg": "Френски",     "pl": "Francuski",   "pt": "Francês",     "cs": "Francouzský", "hu": "Francia",     "no": "Fransk",      "sv": "Franska",     "fi": "Ranska",      "da": "Fransk",      "nl": "Frans",       "tr": "Fransızca",   "sq": "Frëngjisht",  "ro": "Franceză",    "ar": "الفرنسية",     "hi": "फ़्रेंच",       "af": "Frans",       "el": "Γαλλικά"},
    "Spanisch":       {"en": "Spanish",    "ru": "Испанский",   "uk": "Іспанська",   "fr": "Espagnol",    "es": "Español",     "it": "Spagnolo",    "sr": "Шпански",     "hr": "Španjolski",  "bg": "Испански",    "pl": "Hiszpański",  "pt": "Espanhol",    "cs": "Španělský",   "hu": "Spanyol",     "no": "Spansk",      "sv": "Spanska",     "fi": "Espanja",     "da": "Spansk",      "nl": "Spaans",      "tr": "İspanyolca",  "sq": "Spanjisht",   "ro": "Spaniolă",    "ar": "الإسبانية",    "hi": "स्पेनिश",      "af": "Spaans",      "el": "Ισπανικά"},
    "Italienisch":    {"en": "Italian",    "ru": "Итальянский", "uk": "Італійська",  "fr": "Italien",     "es": "Italiano",    "it": "Italiano",    "sr": "Италијански", "hr": "Talijanski",  "bg": "Италиански",  "pl": "Włoski",      "pt": "Italiano",    "cs": "Italský",     "hu": "Olasz",       "no": "Italiensk",   "sv": "Italienska",  "fi": "Italia",      "da": "Italiensk",   "nl": "Italiaans",   "tr": "İtalyanca",   "sq": "Italisht",    "ro": "Italiană",    "ar": "الإيطالية",    "hi": "इतालवी",       "af": "Italiaans",   "el": "Ιταλικά"},
    "Serbisch":       {"en": "Serbian",    "ru": "Сербский",    "uk": "Сербська",    "fr": "Serbe",       "es": "Serbio",      "it": "Serbo",       "sr": "Српски",      "hr": "Srpski",      "bg": "Сръбски",     "pl": "Serbski",     "pt": "Sérvio",      "cs": "Srbský",      "hu": "Szerb",       "no": "Serbisk",     "sv": "Serbiska",    "fi": "Serbia",      "da": "Serbisk",     "nl": "Servisch",    "tr": "Sırpça",      "sq": "Serbisht",    "ro": "Sârbă",       "ar": "الصربية",      "hi": "सर्बियाई",     "af": "Serwies",     "el": "Σερβικά"},
    "Kroatisch":      {"en": "Croatian",   "ru": "Хорватский",  "uk": "Хорватська",  "fr": "Croate",      "es": "Croata",      "it": "Croato",      "sr": "Хрватски",    "hr": "Hrvatski",    "bg": "Хърватски",   "pl": "Chorwacki",   "pt": "Croata",      "cs": "Chorvatský",  "hu": "Horvát",      "no": "Kroatisk",    "sv": "Kroatiska",   "fi": "Kroatia",     "da": "Kroatisk",    "nl": "Kroatisch",   "tr": "Hırvatça",    "sq": "Kroatisht",   "ro": "Croată",      "ar": "الكرواتية",    "hi": "क्रोएशियाई",   "af": "Kroaties",    "el": "Κροατικά"},
    "Ukrainisch":     {"en": "Ukrainian",  "ru": "Украинский",  "uk": "Українська",  "fr": "Ukrainien",   "es": "Ucraniano",   "it": "Ucraino",     "sr": "Украјински",  "hr": "Ukrajinski",  "bg": "Украински",   "pl": "Ukraiński",   "pt": "Ucraniano",   "cs": "Ukrajinský",  "hu": "Ukrán",       "no": "Ukrainsk",    "sv": "Ukrainska",   "fi": "Ukraina",     "da": "Ukrainsk",    "nl": "Oekraïens",   "tr": "Ukraynaca",   "sq": "Ukrainisht",  "ro": "Ucraineană",  "ar": "الأوكرانية",   "hi": "यूक्रेनी",     "af": "Oekraïens",   "el": "Ουκρανικά"},
    "Bulgarisch":     {"en": "Bulgarian",  "ru": "Болгарский",  "uk": "Болгарська",  "fr": "Bulgare",     "es": "Búlgaro",     "it": "Bulgaro",     "sr": "Бугарски",    "hr": "Bugarski",    "bg": "Български",   "pl": "Bułgarski",   "pt": "Búlgaro",     "cs": "Bulharský",   "hu": "Bolgár",      "no": "Bulgarsk",    "sv": "Bulgariska",  "fi": "Bulgaria",    "da": "Bulgarsk",    "nl": "Bulgaars",    "tr": "Bulgarca",    "sq": "Bullgarisht", "ro": "Bulgară",     "ar": "البلغارية",    "hi": "बल्गेरियाई",   "af": "Bulgaars",    "el": "Βουλγαρικά"},
    "Polnisch":       {"en": "Polish",     "ru": "Польский",    "uk": "Польська",    "fr": "Polonais",    "es": "Polaco",      "it": "Polacco",     "sr": "Пољски",      "hr": "Poljski",     "bg": "Полски",      "pl": "Polski",      "pt": "Polonês",     "cs": "Polský",      "hu": "Lengyel",     "no": "Polsk",       "sv": "Polska",      "fi": "Puola",       "da": "Polsk",       "nl": "Pools",       "tr": "Lehçe",       "sq": "Polonisht",   "ro": "Poloneză",    "ar": "البولندية",    "hi": "पोलिश",       "af": "Pools",       "el": "Πολωνικά"},
    "Portugiesisch":  {"en": "Portuguese", "ru": "Португальский","uk": "Португальська","fr": "Portugais",  "es": "Portugués",   "it": "Portoghese",  "sr": "Португалски", "hr": "Portugalski", "bg": "Португалски",  "pl": "Portugalski", "pt": "Português",   "cs": "Portugalský", "hu": "Portugál",    "no": "Portugisisk", "sv": "Portugisiska","fi": "Portugali",   "da": "Portugisisk", "nl": "Portugees",   "tr": "Portekizce",  "sq": "Portugalisht","ro": "Portugheză",  "ar": "البرتغالية",   "hi": "पुर्तगाली",    "af": "Portugees",   "el": "Πορτογαλικά"},
    "Deutsch":        {"en": "German",     "ru": "Немецкий",    "uk": "Німецька",    "fr": "Allemand",    "es": "Alemán",      "it": "Tedesco",     "sr": "Немачки",     "hr": "Njemački",    "bg": "Немски",      "pl": "Niemiecki",   "pt": "Alemão",      "cs": "Německý",     "hu": "Német",       "no": "Tysk",        "sv": "Tyska",       "fi": "Saksa",       "da": "Tysk",        "nl": "Duits",       "tr": "Almanca",     "sq": "Gjermanisht", "ro": "Germană",     "ar": "الألمانية",    "hi": "जर्मन",        "af": "Duits",       "el": "Γερμανικά"},
    "Tschechisch":    {"en": "Czech",      "ru": "Чешский",     "uk": "Чеська",      "fr": "Tchèque",     "es": "Checo",       "it": "Ceco",        "sr": "Чешки",       "hr": "Češki",       "bg": "Чешки",       "pl": "Czeski",      "pt": "Checo",       "cs": "Čeština",     "hu": "Cseh",        "no": "Tsjekkisk",   "sv": "Tjeckiska",   "fi": "Tšekki",      "da": "Tjekkisk",    "nl": "Tsjechisch",  "tr": "Çekçe",       "sq": "Çekisht",     "ro": "Cehă",        "ar": "التشيكية",     "hi": "चेक",          "af": "Tsjeggies",   "el": "Τσεχικά"},
    "Ungarisch":      {"en": "Hungarian",  "ru": "Венгерский",  "uk": "Угорська",    "fr": "Hongrois",    "es": "Húngaro",     "it": "Ungherese",   "sr": "Мађарски",    "hr": "Mađarski",    "bg": "Унгарски",    "pl": "Węgierski",   "pt": "Húngaro",     "cs": "Maďarský",    "hu": "Magyar",      "no": "Ungarsk",     "sv": "Ungerska",    "fi": "Unkari",      "da": "Ungarsk",     "nl": "Hongaars",    "tr": "Macarca",     "sq": "Hungarisht",  "ro": "Maghiară",    "ar": "المجرية",      "hi": "हंगेरियाई",    "af": "Hongaars",    "el": "Ουγγρικά"},
    "Türkisch":       {"en": "Turkish",    "ru": "Турецкий",    "uk": "Турецька",    "fr": "Turc",        "es": "Turco",       "it": "Turco",       "sr": "Турски",      "hr": "Turski",      "bg": "Турски",      "pl": "Turecki",     "pt": "Turco",       "cs": "Turecký",     "hu": "Török",       "no": "Tyrkisk",     "sv": "Turkiska",    "fi": "Turkki",      "da": "Tyrkisk",     "nl": "Turks",       "tr": "Türkçe",      "sq": "Turqisht",    "ro": "Turcă",       "ar": "التركية",      "hi": "तुर्की",       "af": "Turks",       "el": "Τουρκικά"},
    "Rumänisch":      {"en": "Romanian",   "ru": "Румынский",   "uk": "Румунська",   "fr": "Roumain",     "es": "Rumano",      "it": "Rumeno",      "sr": "Румунски",    "hr": "Rumunjski",   "bg": "Румънски",    "pl": "Rumuński",    "pt": "Romeno",      "cs": "Rumunský",    "hu": "Román",       "no": "Rumensk",     "sv": "Rumänska",    "fi": "Romania",     "da": "Rumænsk",     "nl": "Roemeens",    "tr": "Rumence",     "sq": "Rumanisht",   "ro": "Română",      "ar": "الرومانية",    "hi": "रोमानियाई",    "af": "Roemeens",    "el": "Ρουμανικά"},
    "Albanisch":      {"en": "Albanian",   "ru": "Албанский",   "uk": "Албанська",   "fr": "Albanais",    "es": "Albanés",     "it": "Albanese",    "sr": "Албански",    "hr": "Albanski",    "bg": "Албански",    "pl": "Albański",    "pt": "Albanês",     "cs": "Albánský",    "hu": "Albán",       "no": "Albansk",     "sv": "Albanska",    "fi": "Albania",     "da": "Albansk",     "nl": "Albanees",    "tr": "Arnavutça",   "sq": "Shqip",       "ro": "Albaneză",    "ar": "الألبانية",    "hi": "अल्बानियाई",   "af": "Albanees",    "el": "Αλβανικά"},
    "Arabisch":       {"en": "Arabic",     "ru": "Арабский",    "uk": "Арабська",    "fr": "Arabe",       "es": "Árabe",       "it": "Arabo",       "sr": "Арапски",     "hr": "Arapski",     "bg": "Арабски",     "pl": "Arabski",     "pt": "Árabe",       "cs": "Arabský",     "hu": "Arab",        "no": "Arabisk",     "sv": "Arabiska",    "fi": "Arabia",      "da": "Arabisk",     "nl": "Arabisch",    "tr": "Arapça",      "sq": "Arabisht",    "ro": "Arabă",       "ar": "العربية",      "hi": "अरबी",         "af": "Arabies",     "el": "Αραβικά"},
    # ── Error classes ──
    "Verbposition":       {"en": "Verb Position",     "ru": "Позиция глагола",      "uk": "Позиція дієслова",    "fr": "Position du verbe",    "es": "Posición del verbo",   "it": "Posizione del verbo",  "sr": "Позиција глагола",    "hr": "Pozicija glagola",    "bg": "Позиция на глагола",  "pl": "Pozycja czasownika",  "pt": "Posição do verbo",    "cs": "Pozice slovesa",      "hu": "Igehelyzet",          "no": "Verbposisjon",        "sv": "Verbposition",        "fi": "Verbin sijainti",     "da": "Verbposition",        "nl": "Werkwoordpositie",    "tr": "Fiil konumu",         "sq": "Pozicioni i foljes",  "ro": "Poziția verbului",    "ar": "موضع الفعل",          "hi": "क्रिया स्थिति"},
    "Kasus/Artikel":      {"en": "Cases/Articles",    "ru": "Падежи/Артикли",       "uk": "Відмінки/Артиклі",    "fr": "Cas/Articles",         "es": "Casos/Artículos",      "it": "Casi/Articoli",        "sr": "Падежи/Чланови",      "hr": "Padeži/Članovi",      "bg": "Падежи/Членове",      "pl": "Przypadki/Rodzajniki", "pt": "Casos/Artigos",       "cs": "Pády/Členy",          "hu": "Esetek/Névelők",      "no": "Kasus/Artikler",      "sv": "Kasus/Artiklar",      "fi": "Sijat/Artikkelit",    "da": "Kasus/Artikler",      "nl": "Naamvallen/Lidwoorden","tr": "Haller/Artikeller",   "sq": "Rasat/Nyjat",         "ro": "Cazuri/Articole",     "ar": "الحالات/أدوات التعريف","hi": "कारक/उपपद"},
    "Präpositionen":      {"en": "Prepositions",      "ru": "Предлоги",             "uk": "Прийменники",         "fr": "Prépositions",         "es": "Preposiciones",        "it": "Preposizioni",         "sr": "Предлози",            "hr": "Prijedlozi",          "bg": "Предлози",            "pl": "Przyimki",            "pt": "Preposições",         "cs": "Předložky",           "hu": "Elöljárószók",        "no": "Preposisjoner",       "sv": "Prepositioner",       "fi": "Prepositiot",         "da": "Præpositioner",       "nl": "Voorzetsels",         "tr": "Edatlar",             "sq": "Parafjalet",          "ro": "Prepoziții",          "ar": "حروف الجر",           "hi": "सम्बन्ध सूचक"},
    "Wortstellung":       {"en": "Word Order",        "ru": "Порядок слов",         "uk": "Порядок слів",        "fr": "Ordre des mots",       "es": "Orden de palabras",    "it": "Ordine delle parole",  "sr": "Ред речи",            "hr": "Red riječi",          "bg": "Словоред",            "pl": "Szyk zdania",         "pt": "Ordem das palavras",  "cs": "Slovosled",           "hu": "Szórend",             "no": "Ordstilling",         "sv": "Ordföljd",            "fi": "Sanajärjestys",       "da": "Ordstilling",         "nl": "Woordvolgorde",       "tr": "Sözcük dizimi",       "sq": "Rendi i fjalëve",     "ro": "Ordinea cuvintelor",  "ar": "ترتيب الكلمات",       "hi": "शब्द क्रम"},
    "Zeitformen":         {"en": "Tenses",            "ru": "Времена",              "uk": "Часи",                "fr": "Temps",                "es": "Tiempos",              "it": "Tempi",                "sr": "Времена",             "hr": "Vremena",             "bg": "Времена",             "pl": "Czasy",               "pt": "Tempos",              "cs": "Časy",                "hu": "Igeidők",             "no": "Tider",               "sv": "Tempus",              "fi": "Aikamuodot",          "da": "Tider",               "nl": "Tijden",              "tr": "Zamanlar",            "sq": "Kohët",               "ro": "Timpuri",             "ar": "الأزمنة",             "hi": "काल"},
    "Register/Wortwahl":  {"en": "Register/Word Choice","ru": "Регистр/Выбор слов",  "uk": "Регістр/Вибір слів",  "fr": "Registre/Choix de mots","es": "Registro/Elección",   "it": "Registro/Scelta lessicale","sr": "Регистар/Избор речи","hr": "Registar/Izbor riječi","bg": "Регистър/Избор на думи","pl": "Rejestr/Dobór słów", "pt": "Registo/Escolha",     "cs": "Registr/Volba slov",  "hu": "Regiszter/Szóválasztás","no": "Register/Ordvalg",   "sv": "Register/Ordval",     "fi": "Rekisteri/Sanavalinnat","da": "Register/Ordvalg",   "nl": "Register/Woordkeuze", "tr": "Üslup/Sözcük seçimi", "sq": "Regjistri/Zgjedhja",  "ro": "Registru/Alegerea",   "ar": "السجل/اختيار الكلمات", "hi": "शैली/शब्द चयन"},
    "Wortwahl":           {"en": "Word Choice",       "ru": "Выбор слов",           "uk": "Вибір слів",          "fr": "Choix de mots",        "es": "Elección de palabras", "it": "Scelta lessicale",     "sr": "Избор речи",          "hr": "Izbor riječi",        "bg": "Избор на думи",       "pl": "Dobór słów",          "pt": "Escolha de palavras", "cs": "Volba slov",          "hu": "Szóválasztás",        "no": "Ordvalg",             "sv": "Ordval",              "fi": "Sanavalinnat",        "da": "Ordvalg",             "nl": "Woordkeuze",          "tr": "Sözcük seçimi",       "sq": "Zgjedhja e fjalëve",  "ro": "Alegerea cuvintelor", "ar": "اختيار الكلمات",       "hi": "शब्द चयन"},
    # ── Stability levels ──
    "niedrig":     {"en": "Low",              "ru": "Низкий",              "uk": "Низький",            "fr": "Faible",             "es": "Bajo",               "it": "Basso",              "sr": "Низак",              "hr": "Nizak",              "bg": "Нисък",              "pl": "Niski",              "pt": "Baixo",              "cs": "Nízký",              "hu": "Alacsony",           "no": "Lav",                "sv": "Låg",                "fi": "Matala",             "da": "Lav",                "nl": "Laag",               "tr": "Düşük",              "sq": "I ulët",             "ro": "Scăzut",             "ar": "منخفض",              "hi": "कम"},
    "niedrig bis mittel": {"en": "Low to Medium",  "ru": "Низкий-средний",      "uk": "Низький-середній",   "fr": "Faible à moyen",     "es": "Bajo a medio",       "it": "Basso-medio",        "sr": "Низак до средnji",   "hr": "Nizak do srednji",   "bg": "Нисък до среден",    "pl": "Niski-średni",       "pt": "Baixo a médio",      "cs": "Nízký-střední",      "hu": "Alacsony-közepes",   "no": "Lav til middels",    "sv": "Låg till medel",     "fi": "Matala-keskitaso",   "da": "Lav til middel",     "nl": "Laag-gemiddeld",     "tr": "Düşük-orta",         "sq": "I ulët-mesatar",     "ro": "Scăzut-mediu",       "ar": "منخفض-متوسط",        "hi": "कम-मध्यम"},
    "mittel":      {"en": "Medium",            "ru": "Средний",             "uk": "Середній",           "fr": "Moyen",              "es": "Medio",              "it": "Medio",              "sr": "Средnji",            "hr": "Srednji",            "bg": "Среден",             "pl": "Średni",             "pt": "Médio",              "cs": "Střední",            "hu": "Közepes",            "no": "Middels",            "sv": "Medel",              "fi": "Keskitaso",          "da": "Middel",             "nl": "Gemiddeld",          "tr": "Orta",               "sq": "Mesatar",            "ro": "Mediu",              "ar": "متوسط",              "hi": "मध्यम"},
    "hoch":        {"en": "High",              "ru": "Высокий",             "uk": "Високий",            "fr": "Élevé",              "es": "Alto",               "it": "Alto",               "sr": "Висок",              "hr": "Visok",              "bg": "Висок",              "pl": "Wysoki",             "pt": "Alto",               "cs": "Vysoký",             "hu": "Magas",              "no": "Høy",                "sv": "Hög",                "fi": "Korkea",             "da": "Høj",                "nl": "Hoog",               "tr": "Yüksek",             "sq": "I lartë",            "ro": "Ridicat",            "ar": "مرتفع",              "hi": "उच्च"},
    "instabil":    {"en": "Unstable",          "ru": "Нестабильный",        "uk": "Нестабільний",       "fr": "Instable",           "es": "Inestable",          "it": "Instabile",          "sr": "Нестабилан",         "hr": "Nestabilan",         "bg": "Нестабилен",         "pl": "Niestabilny",        "pt": "Instável",           "cs": "Nestabilní",         "hu": "Instabil",           "no": "Ustabil",            "sv": "Instabil",           "fi": "Epävakaa",           "da": "Ustabil",            "nl": "Instabiel",          "tr": "Kararsız",           "sq": "I paqëndrueshëm",   "ro": "Instabil",           "ar": "غير مستقر",          "hi": "अस्थिर"},
    "teilstabil":  {"en": "Partially Stable",  "ru": "Частично стабильный", "uk": "Частково стабільний","fr": "Partiellement stable","es": "Parcialmente estable","it": "Parzialmente stabile","sr": "Делимично стабилан","hr": "Djelomično stabilan","bg": "Частично стабилен",  "pl": "Częściowo stabilny", "pt": "Parcialmente estável","cs": "Částečně stabilní",  "hu": "Részben stabil",     "no": "Delvis stabil",      "sv": "Delvis stabil",      "fi": "Osittain vakaa",     "da": "Delvist stabil",     "nl": "Gedeeltelijk stabiel","tr": "Kısmen kararlı",    "sq": "Pjesërisht stabil",  "ro": "Parțial stabil",     "ar": "مستقر جزئياً",       "hi": "आंशिक रूप से स्थिर"},
    "stabil":      {"en": "Stable",            "ru": "Стабильный",          "uk": "Стабільний",         "fr": "Stable",             "es": "Estable",            "it": "Stabile",            "sr": "Стабилан",           "hr": "Stabilan",           "bg": "Стабилен",           "pl": "Stabilny",           "pt": "Estável",            "cs": "Stabilní",           "hu": "Stabil",             "no": "Stabil",             "sv": "Stabil",             "fi": "Vakaa",              "da": "Stabil",             "nl": "Stabiel",            "tr": "Kararlı",            "sq": "Stabil",             "ro": "Stabil",             "ar": "مستقر",              "hi": "स्थिर"},
    # ── Labels ──
    "Ziel":                {"en": "Goal",              "ru": "Цель",              "uk": "Ціль",              "fr": "Objectif",           "es": "Objetivo",           "it": "Obiettivo",          "sr": "Циљ",              "hr": "Cilj",              "bg": "Цел",              "pl": "Cel",              "pt": "Objetivo",          "cs": "Cíl",              "hu": "Cél",              "no": "Mål",              "sv": "Mål",              "fi": "Tavoite",          "da": "Mål",              "nl": "Doel",             "tr": "Hedef",            "sq": "Qëllimi",          "ro": "Obiectiv",         "ar": "الهدف",            "hi": "लक्ष्य"},
    "Schritt":             {"en": "Step",              "ru": "Шаг",               "uk": "Крок",              "fr": "Étape",              "es": "Paso",               "it": "Passo",              "sr": "Корак",            "hr": "Korak",             "bg": "Стъпка",           "pl": "Krok",             "pt": "Passo",             "cs": "Krok",             "hu": "Lépés",            "no": "Steg",             "sv": "Steg",             "fi": "Askel",            "da": "Trin",             "nl": "Stap",             "tr": "Adım",             "sq": "Hapi",             "ro": "Pasul",            "ar": "الخطوة",           "hi": "कदम"},
    "Fokus":               {"en": "Focus",             "ru": "Фокус",             "uk": "Фокус",             "fr": "Focus",              "es": "Enfoque",            "it": "Focus",              "sr": "Фокус",            "hr": "Fokus",             "bg": "Фокус",            "pl": "Fokus",            "pt": "Foco",              "cs": "Zaměření",         "hu": "Fókusz",           "no": "Fokus",            "sv": "Fokus",            "fi": "Painopiste",       "da": "Fokus",            "nl": "Focus",            "tr": "Odak",             "sq": "Fokusi",           "ro": "Focus",            "ar": "التركيز",          "hi": "ध्यान केंद्र"},
    "Was du gut machst":   {"en": "What you do well",  "ru": "Что ты делаешь хорошо","uk": "Що ти робиш добре","fr": "Ce que tu fais bien","es": "Lo que haces bien", "it": "Cosa fai bene",      "sr": "Шта добро радиш",  "hr": "Što dobro radiš",   "bg": "Какво правиш добре","pl": "Co robisz dobrze",  "pt": "O que fazes bem",   "cs": "Co děláš dobře",   "hu": "Amit jól csinálsz","no": "Hva du gjør bra",  "sv": "Vad du gör bra",   "fi": "Mitä teet hyvin",  "da": "Hvad du gør godt", "nl": "Wat je goed doet", "tr": "İyi yaptığın",     "sq": "Çfarë bën mirë",   "ro": "Ce faci bine",     "ar": "ما تفعله جيداً",   "hi": "आप क्या अच्छा करते हैं"},
    "Beispiel":            {"en": "Example",           "ru": "Пример",            "uk": "Приклад",           "fr": "Exemple",            "es": "Ejemplo",            "it": "Esempio",            "sr": "Пример",           "hr": "Primjer",           "bg": "Пример",           "pl": "Przykład",         "pt": "Exemplo",           "cs": "Příklad",          "hu": "Példa",            "no": "Eksempel",         "sv": "Exempel",          "fi": "Esimerkki",        "da": "Eksempel",         "nl": "Voorbeeld",        "tr": "Örnek",            "sq": "Shembull",         "ro": "Exemplu",          "ar": "مثال",             "hi": "उदाहरण"},
    # ── Block D labels ──
    "Top Problems":        {"en": "Top Problems:",         "ru": "Основные проблемы:",       "uk": "Основні проблеми:",      "fr": "Problèmes principaux:",   "es": "Problemas principales:", "it": "Problemi principali:",    "sr": "Главни проблеми:",       "hr": "Glavni problemi:",       "bg": "Основни проблеми:",      "pl": "Główne problemy:",       "pt": "Principais problemas:",  "cs": "Hlavní problémy:",       "hu": "Fő problémák:",         "no": "Hovedproblemer:",        "sv": "Huvudproblem:",          "fi": "Pääongelmat:",           "da": "Hovedproblemer:",        "nl": "Belangrijkste problemen:","tr": "Ana sorunlar:",          "sq": "Problemet kryesore:",    "ro": "Probleme principale:",   "ar": "المشاكل الرئيسية:",      "hi": "मुख्य समस्याएँ:"},
    "Key Recommendation":  {"en": "Key Recommendation:",   "ru": "Ключевая рекомендация:",   "uk": "Ключова рекомендація:",  "fr": "Recommandation clé:",     "es": "Recomendación clave:",   "it": "Raccomandazione chiave:", "sr": "Кључна препорука:",      "hr": "Ključna preporuka:",     "bg": "Ключова препоръка:",     "pl": "Kluczowa rekomendacja:", "pt": "Recomendação principal:", "cs": "Klíčové doporučení:",     "hu": "Fő ajánlás:",           "no": "Hovedanbefaling:",       "sv": "Nyckelrekommendation:",  "fi": "Keskeinen suositus:",    "da": "Nøgleanbefaling:",       "nl": "Belangrijkste aanbeveling:","tr": "Temel öneri:",          "sq": "Rekomandimi kryesor:",   "ro": "Recomandare cheie:",     "ar": "التوصية الرئيسية:",      "hi": "मुख्य सिफारिश:"},
    "Next Steps":          {"en": "Next Steps:",           "ru": "Следующие шаги:",          "uk": "Наступні кроки:",        "fr": "Prochaines étapes:",      "es": "Próximos pasos:",        "it": "Prossimi passi:",         "sr": "Следећи кораци:",        "hr": "Sljedeći koraci:",       "bg": "Следващи стъпки:",       "pl": "Następne kroki:",        "pt": "Próximos passos:",       "cs": "Další kroky:",            "hu": "Következő lépések:",    "no": "Neste steg:",            "sv": "Nästa steg:",            "fi": "Seuraavat askeleet:",    "da": "Næste trin:",            "nl": "Volgende stappen:",      "tr": "Sonraki adımlar:",       "sq": "Hapat e ardhshëm:",      "ro": "Pașii următori:",        "ar": "الخطوات التالية:",       "hi": "अगले कदम:"},
}

# ═══════════════════════════════════════════════════════
# SCORE CARD LABELS (trilingual)
# ═══════════════════════════════════════════════════════
SCORE_LABELS = {
    "en": ["ACTIVE", "PASSIVE", "OVERALL", "CONFIDENCE"],
    "de": ["AKTIV", "PASSIV", "GESAMT", "SELBSTVERTRAUEN"],
    "ru": ["АКТИВНЫЙ", "ПАССИВНЫЙ", "ОБЩИЙ", "УВЕРЕННОСТЬ"],
    "uk": ["АКТИВНИЙ", "ПАСИВНИЙ", "ЗАГАЛЬНИЙ", "ВПЕВНЕНІСТЬ"],
    "fr": ["ACTIF", "PASSIF", "GLOBAL", "CONFIANCE"],
    "es": ["ACTIVO", "PASIVO", "GENERAL", "CONFIANZA"],
    "it": ["ATTIVO", "PASSIVO", "GLOBALE", "FIDUCIA"],
    "sr": ["АКТИВАН", "ПАСИВАН", "УКУПНО", "ПОУЗДАЊЕ"],
    "hr": ["AKTIVNO", "PASIVNO", "UKUPNO", "POUZDANJE"],
    "bg": ["АКТИВЕН", "ПАСИВЕН", "ОБЩ", "УВЕРЕНОСТ"],
    "pl": ["AKTYWNY", "PASYWNY", "OGÓLNY", "PEWNOŚĆ"],
    "pt": ["ATIVO", "PASSIVO", "GERAL", "CONFIANÇA"],
    "cs": ["AKTIVNÍ", "PASIVNÍ", "CELKOVÝ", "DŮVĚRA"],
    "hu": ["AKTÍV", "PASSZÍV", "ÖSSZESÍTETT", "MAGABIZTOSSÁG"],
    "no": ["AKTIV", "PASSIV", "SAMLET", "SELVTILLIT"],
    "sv": ["AKTIV", "PASSIV", "ÖVERGRIPANDE", "SJÄLVFÖRTROENDE"],
    "fi": ["AKTIIVINEN", "PASSIIVINEN", "KOKONAIS", "ITSELUOTTAMUS"],
    "da": ["AKTIV", "PASSIV", "SAMLET", "SELVTILLID"],
    "nl": ["ACTIEF", "PASSIEF", "ALGEMEEN", "ZELFVERTROUWEN"],
    "tr": ["AKTİF", "PASİF", "GENEL", "GÜVEN"],
    "sq": ["AKTIV", "PASIV", "PËRGJITHSHËM", "BESIM"],
    "ro": ["ACTIV", "PASIV", "GENERAL", "ÎNCREDERE"],
    "ar": ["نشط", "سلبي", "إجمالي", "ثقة"],
    "hi": ["सक्रिय", "निष्क्रिय", "समग्र", "आत्मविश्वास"],
    "af": ["AKTIEF", "PASSIEF", "ALGEHEEL", "SELFVERTROUE"],
}

# ═══════════════════════════════════════════════════════
# DETAIL STRIP LABELS
# ═══════════════════════════════════════════════════════
DETAIL_LABELS = {
    "en": ["ERROR FOCUS", "STABILITY", "SELF-CORRECTION", "RE-ASSESS"],
    "de": ["FEHLERFOKUS", "STABILITÄT", "SELBSTKORREKTUR", "NEUBEWERTUNG"],
    "ru": ["ФОКУС ОШИБОК", "СТАБИЛЬНОСТЬ", "САМОКОРРЕКЦИЯ", "ПЕРЕОЦЕНКА"],
    "uk": ["ФОКУС ПОМИЛОК", "СТАБІЛЬНІСТЬ", "САМОКОРЕКЦІЯ", "ПЕРЕОЦІНКА"],
    "fr": ["ERREURS CLÉS", "STABILITÉ", "AUTO-CORRECTION", "RÉ-ÉVALUATION"],
    "es": ["ERRORES CLAVE", "ESTABILIDAD", "AUTOCORRECCIÓN", "REEVALUACIÓN"],
    "it": ["ERRORI CHIAVE", "STABILITÀ", "AUTOCORREZIONE", "RIVALUTAZIONE"],
    "sr": ["ФОКУС ГРЕШАКА", "СТАБИЛНОСТ", "САМОКОРЕКЦИЈА", "ПОНОВНА ПРОЦЕНА"],
    "hr": ["FOKUS GREŠAKA", "STABILNOST", "SAMOKOREKCIJA", "PONOVNA PROCJENA"],
    "bg": ["ФОКУС НА ГРЕШКИ", "СТАБИЛНОСТ", "САМОКОРЕКЦИЯ", "ПРЕОЦЕНКА"],
    "pl": ["FOKUS BŁĘDÓW", "STABILNOŚĆ", "AUTOKOREKTA", "PONOWNA OCENA"],
    "pt": ["FOCO DE ERROS", "ESTABILIDADE", "AUTOCORREÇÃO", "REAVALIAÇÃO"],
    "cs": ["ZAMĚŘENÍ CHYB", "STABILITA", "AUTOKOREKCE", "PŘEHODNOCENÍ"],
    "hu": ["HIBAFÓKUSZ", "STABILITÁS", "ÖNJAVÍTÁS", "ÚJRAÉRTÉKELÉS"],
    "no": ["FEILFOKUS", "STABILITET", "SELVKORRIGERING", "REVURDERING"],
    "sv": ["FELFOKUS", "STABILITET", "SJÄLVKORRIGERING", "OMVÄRDERING"],
    "fi": ["VIRHEFOKUS", "VAKAUS", "ITSEKORJAUS", "UUDELLEENARVIOINTI"],
    "da": ["FEJLFOKUS", "STABILITET", "SELVKORREKTION", "REVURDERING"],
    "nl": ["FOUTENFOCUS", "STABILITEIT", "ZELFCORRECTIE", "HERBEOORDELING"],
    "tr": ["HATA ODAĞI", "KARARLILIK", "ÖZ DÜZELTME", "YENİDEN DEĞERLENDİRME"],
    "sq": ["FOKUSI I GABIMEVE", "STABILITETI", "VETËKORRIGJIMI", "RIVLERËSIMI"],
    "ro": ["FOCUS ERORI", "STABILITATE", "AUTOCORECTARE", "REEVALUARE"],
    "ar": ["تركيز الأخطاء", "الاستقرار", "التصحيح الذاتي", "إعادة التقييم"],
    "hi": ["त्रुटि फोकस", "स्थिरता", "आत्म-सुधार", "पुनर्मूल्यांकन"],
}

# ═══════════════════════════════════════════════════════
# REASSESSMENT PERIODS
# ═══════════════════════════════════════════════════════
REASSESS = {
    "en": {"3 Monate": "3 Months", "6 Monate": "6 Months", "6 Wochen": "6 Weeks", "8 Wochen": "8 Weeks", "12 Wochen": "12 Weeks"},
    "ru": {"3 Monate": "3 месяца", "6 Monate": "6 месяцев", "6 Wochen": "6 недель", "8 Wochen": "8 недель", "12 Wochen": "12 недель"},
    "uk": {"3 Monate": "3 місяці", "6 Monate": "6 місяців", "6 Wochen": "6 тижнів", "8 Wochen": "8 тижнів", "12 Wochen": "12 тижнів"},
    "fr": {"3 Monate": "3 mois", "6 Monate": "6 mois", "6 Wochen": "6 semaines", "8 Wochen": "8 semaines", "12 Wochen": "12 semaines"},
    "es": {"3 Monate": "3 meses", "6 Monate": "6 meses", "6 Wochen": "6 semanas", "8 Wochen": "8 semanas", "12 Wochen": "12 semanas"},
    "it": {"3 Monate": "3 mesi", "6 Monate": "6 mesi", "6 Wochen": "6 settimane", "8 Wochen": "8 settimane", "12 Wochen": "12 settimane"},
    "sr": {"3 Monate": "3 месеца", "6 Monate": "6 месеци", "6 Wochen": "6 недеља", "8 Wochen": "8 недеља", "12 Wochen": "12 недеља"},
    "hr": {"3 Monate": "3 mjeseca", "6 Monate": "6 mjeseci", "6 Wochen": "6 tjedana", "8 Wochen": "8 tjedana", "12 Wochen": "12 tjedana"},
    "bg": {"3 Monate": "3 месеца", "6 Monate": "6 месеца", "6 Wochen": "6 седмици", "8 Wochen": "8 седмици", "12 Wochen": "12 седмици"},
    "pl": {"3 Monate": "3 miesiące", "6 Monate": "6 miesięcy", "6 Wochen": "6 tygodni", "8 Wochen": "8 tygodni", "12 Wochen": "12 tygodni"},
    "pt": {"3 Monate": "3 meses", "6 Monate": "6 meses", "6 Wochen": "6 semanas", "8 Wochen": "8 semanas", "12 Wochen": "12 semanas"},
    "cs": {"3 Monate": "3 měsíce", "6 Monate": "6 měsíců", "6 Wochen": "6 týdnů", "8 Wochen": "8 týdnů", "12 Wochen": "12 týdnů"},
    "hu": {"3 Monate": "3 hónap", "6 Monate": "6 hónap", "6 Wochen": "6 hét", "8 Wochen": "8 hét", "12 Wochen": "12 hét"},
    "no": {"3 Monate": "3 måneder", "6 Monate": "6 måneder", "6 Wochen": "6 uker", "8 Wochen": "8 uker", "12 Wochen": "12 uker"},
    "sv": {"3 Monate": "3 månader", "6 Monate": "6 månader", "6 Wochen": "6 veckor", "8 Wochen": "8 veckor", "12 Wochen": "12 veckor"},
    "fi": {"3 Monate": "3 kuukautta", "6 Monate": "6 kuukautta", "6 Wochen": "6 viikkoa", "8 Wochen": "8 viikkoa", "12 Wochen": "12 viikkoa"},
    "da": {"3 Monate": "3 måneder", "6 Monate": "6 måneder", "6 Wochen": "6 uger", "8 Wochen": "8 uger", "12 Wochen": "12 uger"},
    "nl": {"3 Monate": "3 maanden", "6 Monate": "6 maanden", "6 Wochen": "6 weken", "8 Wochen": "8 weken", "12 Wochen": "12 weken"},
    "tr": {"3 Monate": "3 ay", "6 Monate": "6 ay", "6 Wochen": "6 hafta", "8 Wochen": "8 hafta", "12 Wochen": "12 hafta"},
    "sq": {"3 Monate": "3 muaj", "6 Monate": "6 muaj", "6 Wochen": "6 javë", "8 Wochen": "8 javë", "12 Wochen": "12 javë"},
    "ro": {"3 Monate": "3 luni", "6 Monate": "6 luni", "6 Wochen": "6 săptămâni", "8 Wochen": "8 săptămâni", "12 Wochen": "12 săptămâni"},
    "ar": {"3 Monate": "3 أشهر", "6 Monate": "6 أشهر", "6 Wochen": "6 أسابيع", "8 Wochen": "8 أسابيع", "12 Wochen": "12 أسبوع"},
    "hi": {"3 Monate": "3 महीने", "6 Monate": "6 महीने", "6 Wochen": "6 सप्ताह", "8 Wochen": "8 सप्ताह", "12 Wochen": "12 सप्ताह"},
}

# ═══════════════════════════════════════════════════════
# UI STRINGS (prepared for, confidential, TOC heading, etc.)
# ═══════════════════════════════════════════════════════
PREPARED_FOR = {
    "en": "Prepared exclusively for {name}",
    "ru": "Подготовлено эксклюзивно для {name}",
    "uk": "Підготовлено ексклюзивно для {name}",
    "fr": "Préparé exclusivement pour {name}",
    "es": "Preparado exclusivamente para {name}",
    "it": "Preparato esclusivamente per {name}",
    "sr": "Припремљено ексклузивно за {name}",
    "hr": "Pripremljeno ekskluzivno za {name}",
    "bg": "Подготвено ексклузивно за {name}",
    "pl": "Przygotowane specjalnie dla {name}",
    "pt": "Preparado exclusivamente para {name}",
    "cs": "Připraveno výhradně pro {name}",
    "hu": "Kizárólag {name} számára készítve",
    "no": "Utarbeidet eksklusivt for {name}",
    "sv": "Förberett exklusivt för {name}",
    "fi": "Valmistettu yksinomaan henkilölle {name}",
    "da": "Udarbejdet eksklusivt til {name}",
    "nl": "Exclusief opgesteld voor {name}",
    "tr": "{name} için özel olarak hazırlandı",
    "sq": "Përgatitur ekskluzivisht për {name}",
    "ro": "Pregătit exclusiv pentru {name}",
    "ar": "أُعد حصرياً لـ {name}",
    "hi": "{name} के लिए विशेष रूप से तैयार",
}

CONFIDENTIAL = {
    "en": "CONFIDENTIAL", "de": "VERTRAULICH",
    "ru": "КОНФИДЕНЦИАЛЬНО", "uk": "КОНФІДЕНЦІЙНО", "fr": "CONFIDENTIEL",
    "es": "CONFIDENCIAL", "it": "RISERVATO", "sr": "ПОВЕРЉИВО",
    "hr": "POVJERLJIVO", "bg": "ПОВЕРИТЕЛНО", "pl": "POUFNE",
    "pt": "CONFIDENCIAL", "cs": "DŮVĚRNÉ", "hu": "BIZALMAS",
    "no": "KONFIDENSIELT", "sv": "KONFIDENTIELLT", "fi": "LUOTTAMUKSELLINEN",
    "da": "FORTROLIGT", "nl": "VERTROUWELIJK", "tr": "GİZLİ",
    "sq": "KONFIDENCIALE", "ro": "CONFIDENȚIAL", "ar": "سري", "hi": "गोपनीय",
}

TOC_HEADING = {
    "de": "Was dieser Bericht enthält",
    "en": "What This Report Contains",
    "ru": "Что содержит этот отчёт", "uk": "Що містить цей звіт",
    "fr": "Contenu de ce rapport", "es": "Contenido de este informe",
    "it": "Contenuto di questo rapporto", "sr": "Шта садржи овај извештај",
    "hr": "Što sadrži ovo izvješće", "bg": "Какво съдържа този доклад",
    "pl": "Co zawiera ten raport", "pt": "O que este relatório contém",
    "cs": "Co tento report obsahuje", "hu": "Mit tartalmaz ez a jelentés",
    "no": "Hva denne rapporten inneholder", "sv": "Vad denna rapport innehåller",
    "fi": "Mitä tämä raportti sisältää", "da": "Hvad denne rapport indeholder",
    "nl": "Wat dit rapport bevat", "tr": "Bu rapor ne içeriyor",
    "sq": "Çfarë përmban ky raport", "ro": "Ce conține acest raport",
    "ar": "محتوى هذا التقرير", "hi": "इस रिपोर्ट में क्या है",
}

CLOSING = {
    "en": "This report was prepared by Marko for {name}.",
    "ru": "Этот отчёт подготовлен Марко для {name}.",
    "uk": "Цей звіт підготовлений Марко для {name}.",
    "fr": "Ce rapport a été préparé par Marko pour {name}.",
    "es": "Este informe fue preparado por Marko para {name}.",
    "it": "Questo rapporto è stato preparato da Marko per {name}.",
    "sr": "Овај извештај је припремио Марко за {name}.",
    "hr": "Ovaj izvještaj je pripremio Marko za {name}.",
    "bg": "Този доклад е подготвен от Марко за {name}.",
    "pl": "Ten raport został przygotowany przez Marko dla {name}.",
    "pt": "Este relatório foi preparado por Marko para {name}.",
    "cs": "Tuto zprávu připravil Marko pro {name}.",
    "hu": "Ezt a jelentést Marko készítette {name} számára.",
    "no": "Denne rapporten ble utarbeidet av Marko for {name}.",
    "sv": "Denna rapport förbereddes av Marko för {name}.",
    "fi": "Tämän raportin laati Marko henkilölle {name}.",
    "da": "Denne rapport blev udarbejdet af Marko til {name}.",
    "nl": "Dit rapport is opgesteld door Marko voor {name}.",
    "tr": "Bu rapor Marko tarafından {name} için hazırlanmıştır.",
    "sq": "Ky raport u përgatit nga Marko për {name}.",
    "ro": "Acest raport a fost pregătit de Marko pentru {name}.",
    "ar": "أعد هذا التقرير ماركو لـ {name}.",
    "hi": "यह रिपोर्ट मार्को द्वारा {name} के लिए तैयार की गई।",
}

MARKO_NATIVE = {
    "ru": "Марко", "uk": "Марко", "sr": "Марко", "bg": "Марко",
    "ar": "ماركو", "hi": "मार्को", "el": "Μάρκο",
}

# ═══════════════════════════════════════════════════════
# SECTION BANNERS (German + native)
# ═══════════════════════════════════════════════════════
BANNERS = {
    "problems":    {"de": "TOP {n} STRUKTURELLE PROBLEME",     "en": "TOP {n} STRUCTURAL PROBLEMS",     "ru": "ТОП-{n} СТРУКТУРНЫХ ПРОБЛЕМ",       "uk": "ТОП-{n} СТРУКТУРНИХ ПРОБЛЕМ",      "fr": "TOP {n} PROBLÈMES STRUCTURELS",     "es": "TOP {n} PROBLEMAS ESTRUCTURALES",  "it": "TOP {n} PROBLEMI STRUTTURALI",      "sr": "ТОП {n} СТРУКТУРНИХ ПРОБЛЕМА",     "hr": "TOP {n} STRUKTURNIH PROBLEMA",     "bg": "ТОП-{n} СТРУКТУРНИ ПРОБЛЕМИ",      "pl": "TOP {n} PROBLEMÓW STRUKTURALNYCH", "pt": "TOP {n} PROBLEMAS ESTRUTURAIS",    "cs": "TOP {n} STRUKTURÁLNÍCH PROBLÉMŮ",  "hu": "TOP {n} STRUKTURÁLIS PROBLÉMA",    "no": "TOPP {n} STRUKTURELLE PROBLEMER",  "sv": "TOPP {n} STRUKTURELLA PROBLEM",    "fi": "TOP {n} RAKENTEELLISTA ONGELMAA",  "da": "TOP {n} STRUKTURELLE PROBLEMER",   "nl": "TOP {n} STRUCTURELE PROBLEMEN",    "tr": "EN ÖNEMLİ {n} YAPISAL SORUN",      "sq": "TOP {n} PROBLEME STRUKTURORE",     "ro": "TOP {n} PROBLEME STRUCTURALE",     "ar": "أهم {n} مشاكل هيكلية",             "hi": "शीर्ष {n} संरचनात्मक समस्याएँ"},
    "corrections": {"de": "DIE {n} BESTEN HEBELKORREKTUREN",   "en": "TOP {n} LEVER CORRECTIONS",       "ru": "ТОП-{n} КОРРЕКЦИЙ РЫЧАГА",          "uk": "ТОП-{n} ВАЖІЛЬНИХ КОРЕКЦІЙ",       "fr": "LES {n} MEILLEURES CORRECTIONS",    "es": "LAS {n} MEJORES CORRECCIONES",     "it": "LE {n} MIGLIORI CORREZIONI LEVA",   "sr": "НАЈБОЉИХ {n} КОРЕКЦИЈА ПОЛУГЕ",    "hr": "NAJBOLJIH {n} KOREKCIJA POLUGE",   "bg": "ТОП-{n} КОРЕКЦИИ НА ЛОСТА",        "pl": "TOP {n} KOREKCJI DŹWIGNI",        "pt": "TOP {n} CORREÇÕES DE ALAVANCA",    "cs": "TOP {n} PÁKOVÝCH KOREKCÍ",         "hu": "TOP {n} EMELŐ KORREKCIÓ",          "no": "TOPP {n} SPAKKORREKSJONER",        "sv": "TOPP {n} HÄVSTÅNGSKORREKTIONER",   "fi": "TOP {n} VIVUN KORJAUSTA",          "da": "TOP {n} LØFTESTANGSKORREKTIONER",  "nl": "TOP {n} HEFBOOMCORRECTIES",        "tr": "EN İYİ {n} KALDIRAÇ DÜZELTMESİ",   "sq": "TOP {n} KORRIGJIME LEVASH",        "ro": "TOP {n} CORECȚII DE PÂRGHIE",      "ar": "أفضل {n} تصحيحات رافعة",           "hi": "शीर्ष {n} लीवर सुधार"},
    "solutions":   {"de": "TOP {n} LÖSUNGEN",                  "en": "TOP {n} SOLUTIONS",               "ru": "ТОП-{n} РЕШЕНИЙ",                   "uk": "ТОП-{n} РІШЕНЬ",                   "fr": "TOP {n} SOLUTIONS",                 "es": "TOP {n} SOLUCIONES",               "it": "TOP {n} SOLUZIONI",                 "sr": "ТОП {n} РЕШЕЊА",                   "hr": "TOP {n} RJEŠENJA",                 "bg": "ТОП-{n} РЕШЕНИЯ",                  "pl": "TOP {n} ROZWIĄZAŃ",               "pt": "TOP {n} SOLUÇÕES",                 "cs": "TOP {n} ŘEŠENÍ",                   "hu": "TOP {n} MEGOLDÁS",                 "no": "TOPP {n} LØSNINGER",               "sv": "TOPP {n} LÖSNINGAR",               "fi": "TOP {n} RATKAISUA",                "da": "TOP {n} LØSNINGER",                "nl": "TOP {n} OPLOSSINGEN",              "tr": "EN İYİ {n} ÇÖZÜM",                 "sq": "TOP {n} ZGJIDHJE",                 "ro": "TOP {n} SOLUȚII",                  "ar": "أفضل {n} حلول",                    "hi": "शीर्ष {n} समाधान"},
    "engine":      {"de": "SATZMOTOR",                         "en": "SENTENCE ENGINE",                 "ru": "РЕЧЕВОЙ ДВИГАТЕЛЬ",                 "uk": "МОВНИЙ ДВИГУН",                    "fr": "MOTEUR DE PHRASE",                  "es": "MOTOR DE ORACIÓN",                 "it": "MOTORE DI FRASE",                   "sr": "МОТОР РЕЧЕНИЦЕ",                   "hr": "MOTOR REČENICE",                   "bg": "РЕЧЕВИ ДВИГАТЕЛ",                   "pl": "SILNIK ZDAŃ",                     "pt": "MOTOR DE FRASE",                   "cs": "VĚTNÝ MOTOR",                      "hu": "MONDATMOTOR",                      "no": "SETNINGSMOTOR",                    "sv": "MENINGSMOTOR",                     "fi": "LAUSEMOOTTORI",                    "da": "SÆTNINGSMOTOR",                    "nl": "ZINSMOTOR",                        "tr": "CÜMLE MOTORU",                      "sq": "MOTORI I FJALISË",                 "ro": "MOTORUL FRAZEI",                   "ar": "محرك الجمل",                       "hi": "वाक्य इंजन"},
    "activation":  {"de": "AKTIVIERUNG",                       "en": "ACTIVATION",                      "ru": "АКТИВАЦИЯ",                         "uk": "АКТИВАЦІЯ",                        "fr": "ACTIVATION",                        "es": "ACTIVACIÓN",                       "it": "ATTIVAZIONE",                       "sr": "АКТИВАЦИЈА",                       "hr": "AKTIVACIJA",                       "bg": "АКТИВИРАНЕ",                        "pl": "AKTYWACJA",                       "pt": "ATIVAÇÃO",                         "cs": "AKTIVACE",                         "hu": "AKTIVÁLÁS",                        "no": "AKTIVERING",                       "sv": "AKTIVERING",                       "fi": "AKTIVOINTI",                       "da": "AKTIVERING",                       "nl": "ACTIVERING",                       "tr": "AKTİVASYON",                        "sq": "AKTIVIZIMI",                       "ro": "ACTIVARE",                         "ar": "التنشيط",                          "hi": "सक्रियण"},
    "hw_a":        {"de": "HAUSAUFGABE A \u2014 STRUKTUR",     "en": "HOMEWORK A \u2014 STRUCTURE",     "ru": "ДОМАШНЕЕ ЗАДАНИЕ A \u2014 СТРУКТУРА","uk": "ДОМАШНЄ ЗАВДАННЯ A \u2014 СТРУКТУРА","fr": "DEVOIRS A \u2014 STRUCTURE",         "es": "TAREA A \u2014 ESTRUCTURA",         "it": "COMPITI A \u2014 STRUTTURA",         "sr": "ДОМАЋИ A \u2014 СТРУКТУРА",        "hr": "ZADAĆA A \u2014 STRUKTURA",        "bg": "ДОМАШНА РАБОТА A \u2014 СТРУКТУРА", "pl": "ZADANIE A \u2014 STRUKTURA",      "pt": "TAREFA A \u2014 ESTRUTURA",        "cs": "ÚKOL A \u2014 STRUKTURA",          "hu": "HÁZI A \u2014 STRUKTÚRA",          "no": "LEKSE A \u2014 STRUKTUR",          "sv": "LÄXA A \u2014 STRUKTUR",           "fi": "KOTITEHTÄVÄ A \u2014 RAKENNE",     "da": "LEKTIE A \u2014 STRUKTUR",         "nl": "HUISWERK A \u2014 STRUCTUUR",      "tr": "ÖDEV A \u2014 YAPI",                "sq": "DETYRË A \u2014 STRUKTURË",        "ro": "TEMĂ A \u2014 STRUCTURĂ",          "ar": "واجب أ \u2014 البنية",             "hi": "गृहकार्य A \u2014 संरचना"},
    "hw_b":        {"de": "HAUSAUFGABE B \u2014 PRÄZISION",    "en": "HOMEWORK B \u2014 PRECISION",     "ru": "ДОМАШНЕЕ ЗАДАНИЕ B \u2014 ТОЧНОСТЬ","uk": "ДОМАШНЄ ЗАВДАННЯ B \u2014 ТОЧНІСТЬ","fr": "DEVOIRS B \u2014 PRÉCISION",        "es": "TAREA B \u2014 PRECISIÓN",          "it": "COMPITI B \u2014 PRECISIONE",        "sr": "ДОМАЋИ B \u2014 ПРЕЦИЗНОСТ",       "hr": "ZADAĆA B \u2014 PRECIZNOST",       "bg": "ДОМАШНА РАБОТА B \u2014 ПРЕЦИЗНОСТ","pl": "ZADANIE B \u2014 PRECYZJA",       "pt": "TAREFA B \u2014 PRECISÃO",         "cs": "ÚKOL B \u2014 PŘESNOST",           "hu": "HÁZI B \u2014 PONTOSSÁG",          "no": "LEKSE B \u2014 PRESISJON",         "sv": "LÄXA B \u2014 PRECISION",          "fi": "KOTITEHTÄVÄ B \u2014 TARKKUUS",    "da": "LEKTIE B \u2014 PRÆCISION",        "nl": "HUISWERK B \u2014 PRECISIE",       "tr": "ÖDEV B \u2014 HASSASIYET",          "sq": "DETYRË B \u2014 PRECIZION",        "ro": "TEMĂ B \u2014 PRECIZIE",           "ar": "واجب ب \u2014 الدقة",              "hi": "गृहकार्य B \u2014 सटीकता"},
    "hw_c":        {"de": "HAUSAUFGABE C \u2014 SPRECHFLUSS",  "en": "HOMEWORK C \u2014 SPEAKING FLUENCY","ru": "ДОМАШНЕЕ ЗАДАНИЕ C \u2014 БЕГЛОСТЬ РЕЧИ","uk": "ДОМАШНЄ ЗАВДАННЯ C \u2014 ПЛАВНІСТЬ МОВЛЕННЯ","fr": "DEVOIRS C \u2014 FLUIDITÉ ORALE","es": "TAREA C \u2014 FLUIDEZ ORAL",    "it": "COMPITI C \u2014 FLUENZA ORALE",    "sr": "ДОМАЋИ C \u2014 ТЕЧНОСТ ГОВОРА",   "hr": "ZADAĆA C \u2014 TEČNOST GOVORA",   "bg": "ДОМАШНА РАБОТА C \u2014 ПЛАВНОСТ НА РЕЧТА","pl": "ZADANIE C \u2014 PŁYNNOŚĆ MOWY","pt": "TAREFA C \u2014 FLUÊNCIA ORAL",   "cs": "ÚKOL C \u2014 PLYNULOST ŘEČI",    "hu": "HÁZI C \u2014 BESZÉDFOLYÉKONYSÁG",  "no": "LEKSE C \u2014 TALEFLYT",          "sv": "LÄXA C \u2014 TALFLYT",            "fi": "KOTITEHTÄVÄ C \u2014 PUHEEN SUJUVUUS","da": "LEKTIE C \u2014 TALEFLYDENDE",  "nl": "HUISWERK C \u2014 SPREEKVLOEIENDHEID","tr": "ÖDEV C \u2014 KONUŞMA AKICILIĞI","sq": "DETYRË C \u2014 RRJEDHSHMËRI E TË FOLURIT","ro": "TEMĂ C \u2014 FLUENȚA VORBIRII","ar": "واجب ج \u2014 طلاقة الكلام",     "hi": "गृहकार्य C \u2014 बोलने की प्रवाहिता"},
    "weekly":      {"de": "WOCHENPLAN",                        "en": "WEEKLY PLAN",                     "ru": "НЕДЕЛЬНЫЙ ПЛАН",                    "uk": "ТИЖНЕВИЙ ПЛАН",                    "fr": "PLAN HEBDOMADAIRE",                 "es": "PLAN SEMANAL",                     "it": "PIANO SETTIMANALE",                 "sr": "НЕДЕЉНИ ПЛАН",                     "hr": "TJEDNI PLAN",                      "bg": "СЕДМИЧЕН ПЛАН",                     "pl": "PLAN TYGODNIOWY",                 "pt": "PLANO SEMANAL",                    "cs": "TÝDENNÍ PLÁN",                     "hu": "HETI TERV",                        "no": "UKEPLAN",                          "sv": "VECKOPLAN",                        "fi": "VIIKKOSUUNNITELMA",                "da": "UGEPLAN",                          "nl": "WEEKPLAN",                         "tr": "HAFTALIK PLAN",                     "sq": "PLANI JAVOR",                      "ro": "PLAN SĂPTĂMÂNAL",                  "ar": "الخطة الأسبوعية",                  "hi": "साप्ताहिक योजना"},
    "mini":        {"de": "MINI-BLOCK",                        "en": "MINI BLOCK",                      "ru": "МИНИ-БЛОК",                         "uk": "МІНІ-БЛОК",                        "fr": "MINI-BLOC",                         "es": "MINI-BLOQUE",                      "it": "MINI-BLOCCO",                       "sr": "МИНИ-БЛОК",                        "hr": "MINI-BLOK",                        "bg": "МИНИ-БЛОК",                         "pl": "MINI-BLOK",                       "pt": "MINI-BLOCO",                       "cs": "MINI-BLOK",                        "hu": "MINI-BLOKK",                       "no": "MINI-BLOKK",                       "sv": "MINI-BLOCK",                       "fi": "MINILOHKO",                        "da": "MINI-BLOK",                        "nl": "MINI-BLOK",                        "tr": "MİNİ BLOK",                         "sq": "MINI-BLLOK",                       "ro": "MINI-BLOC",                        "ar": "كتلة صغيرة",                       "hi": "मिनी ब्लॉक"},
    "cefr":        {"de": "CEFR-EINSTUFUNG",                   "en": "CEFR RATING",                     "ru": "ОЦЕНКА CEFR",                       "uk": "ОЦІНКА CEFR",                      "fr": "ÉVALUATION CECR",                   "es": "EVALUACIÓN MCER",                  "it": "VALUTAZIONE QCER",                  "sr": "ЦЕФР ОЦЕНА",                       "hr": "CEFR PROCJENA",                    "bg": "ОЦЕНКА CEFR",                       "pl": "OCENA CEFR",                      "pt": "AVALIAÇÃO CEFR",                   "cs": "HODNOCENÍ CEFR",                   "hu": "CEFR ÉRTÉKELÉS",                   "no": "CEFR-VURDERING",                   "sv": "CEFR-BEDÖMNING",                   "fi": "CEFR-ARVIOINTI",                   "da": "CEFR-VURDERING",                   "nl": "CEFR-BEOORDELING",                 "tr": "CEFR DEĞERLENDİRMESİ",             "sq": "VLERËSIMI CEFR",                   "ro": "EVALUARE CEFR",                    "ar": "تقييم CEFR",                       "hi": "CEFR मूल्यांकन"},
}

# ═══════════════════════════════════════════════════════
# EMAIL TRANSLATIONS (for lg_send.py)
# ═══════════════════════════════════════════════════════
EMAIL = {
    "en": {"subj": "Dein Sprachbericht / Your Language Report",           "greet": "Hi",        "body": "Your German language assessment report is ready. You will find it attached.",                                      "close": "Best regards"},
    "ru": {"subj": "Dein Sprachbericht / Твой языковой отчёт",           "greet": "Привет",    "body": "Твой персональный отчёт об оценке немецкого языка готов. Ты найдёшь его в приложении.",                             "close": "С наилучшими пожеланиями"},
    "uk": {"subj": "Dein Sprachbericht / Твій мовний звіт",              "greet": "Привіт",    "body": "Твій персональний звіт про оцінку німецької мови готовий. Ти знайдеш його у додатку.",                              "close": "З найкращими побажаннями"},
    "fr": {"subj": "Dein Sprachbericht / Ton rapport linguistique",       "greet": "Bonjour",   "body": "Ton rapport d'évaluation en allemand est prêt. Tu le trouveras en pièce jointe.",                                  "close": "Cordialement"},
    "es": {"subj": "Dein Sprachbericht / Tu informe lingüístico",         "greet": "Hola",      "body": "Tu informe de evaluación de alemán está listo. Lo encontrarás adjunto.",                                            "close": "Saludos cordiales"},
    "it": {"subj": "Dein Sprachbericht / Il tuo rapporto linguistico",    "greet": "Ciao",      "body": "Il tuo rapporto di valutazione del tedesco è pronto. Lo troverai in allegato.",                                    "close": "Cordiali saluti"},
    "sr": {"subj": "Dein Sprachbericht / Твој језички извештај",          "greet": "Здраво",    "body": "Твој извештај о процени немачког језика је спреман. Наћи ћеш га у прилогу.",                                      "close": "Са најбољим жељама"},
    "hr": {"subj": "Dein Sprachbericht / Tvoje jezično izvješće",         "greet": "Bok",       "body": "Tvoje izvješće o procjeni njemačkog jezika je spremno. Naći ćeš ga u prilogu.",                                    "close": "Srdačan pozdrav"},
    "bg": {"subj": "Dein Sprachbericht / Твоят езиков доклад",            "greet": "Здравей",   "body": "Твоят персонален доклад за оценка на немски език е готов. Ще го намериш в прикачения файл.",                       "close": "С най-добри пожелания"},
    "pl": {"subj": "Dein Sprachbericht / Twój raport językowy",           "greet": "Cześć",     "body": "Twój spersonalizowany raport z oceny języka niemieckiego jest gotowy. Znajdziesz go w załączniku.",                "close": "Z poważaniem"},
    "pt": {"subj": "Dein Sprachbericht / O teu relatório linguístico",    "greet": "Olá",       "body": "O teu relatório personalizado de avaliação de alemão está pronto. Encontrá-lo-ás em anexo.",                       "close": "Com os melhores cumprimentos"},
    "cs": {"subj": "Dein Sprachbericht / Tvá jazyková zpráva",            "greet": "Ahoj",      "body": "Tvá personalizovaná zpráva o hodnocení němčiny je připravena. Najdeš ji v příloze.",                                "close": "S pozdravem"},
    "hu": {"subj": "Dein Sprachbericht / Nyelvi jelentésed",              "greet": "Szia",      "body": "Személyre szabott német nyelvértékelési jelentésed elkészült. A csatolmányban találod.",                            "close": "Üdvözlettel"},
    "no": {"subj": "Dein Sprachbericht / Din språkrapport",               "greet": "Hei",       "body": "Din personlige vurderingsrapport for tysk er klar. Du finner den vedlagt.",                                         "close": "Med vennlig hilsen"},
    "sv": {"subj": "Dein Sprachbericht / Din språkrapport",               "greet": "Hej",       "body": "Din personliga bedömningsrapport för tyska är klar. Du hittar den bifogad.",                                       "close": "Med vänliga hälsningar"},
    "fi": {"subj": "Dein Sprachbericht / Kieliraporttisi",                "greet": "Hei",       "body": "Henkilökohtainen saksan kielen arviointiraporttisi on valmis. Löydät sen liitteenä.",                               "close": "Ystävällisin terveisin"},
    "da": {"subj": "Dein Sprachbericht / Din sprograpport",               "greet": "Hej",       "body": "Din personlige vurderingsrapport for tysk er klar. Du finder den vedhæftet.",                                      "close": "Med venlig hilsen"},
    "nl": {"subj": "Dein Sprachbericht / Je taalrapport",                 "greet": "Hoi",       "body": "Je persoonlijke beoordelingsrapport voor Duits is klaar. Je vindt het in de bijlage.",                              "close": "Met vriendelijke groeten"},
    "tr": {"subj": "Dein Sprachbericht / Dil raporun",                    "greet": "Merhaba",   "body": "Kişiselleştirilmiş Almanca dil değerlendirme raporun hazır. Ekte bulabilirsin.",                                   "close": "Saygılarımla"},
    "sq": {"subj": "Dein Sprachbericht / Raporti yt gjuhësor",            "greet": "Përshëndetje","body": "Raporti yt i personalizuar i vlerësimit të gjermanishtes është gati. Do ta gjesh në bashkëngjitje.",              "close": "Me respekt"},
    "ro": {"subj": "Dein Sprachbericht / Raportul tău lingvistic",        "greet": "Bună",      "body": "Raportul tău personalizat de evaluare a limbii germane este gata. Îl vei găsi atașat.",                             "close": "Cu stimă"},
    "ar": {"subj": "Dein Sprachbericht / تقريرك اللغوي",                  "greet": "مرحباً",    "body": "تقريرك الشخصي لتقييم اللغة الألمانية جاهز. ستجده مرفقاً.",                                                        "close": "مع أطيب التحيات"},
    "hi": {"subj": "Dein Sprachbericht / आपकी भाषा रिपोर्ट",              "greet": "नमस्ते",    "body": "जर्मन भाषा मूल्यांकन की आपकी व्यक्तिगत रिपोर्ट तैयार है। आप इसे संलग्नक में पाएँगे।",                            "close": "सादर"},
}


# ═══════════════════════════════════════════════════════
# TOC ITEMS (What This Report Contains)
# ═══════════════════════════════════════════════════════
TOC_FULL = {
    "de": [
        "Präzise Wahrnehmung — was in deiner Sitzung passiert ist",
        "Strukturelle Stärken — was du gut machst (mit Belegen)",
        "Zentrale Struktur-Erkenntnis — das eine Muster dieser Sitzung",
        "Top 5 Strukturelle Probleme — mit Transkript-Belegen",
        "5 Hebel-Korrekturen — die Änderungen mit dem größten Effekt",
        "Top 5 Lösungen — konkrete Übungen mit Ergebnissen",
        "Satzmotor — dein personalisiertes tägliches Training",
        "Hausaufgaben A, B, C — Struktur, Präzision, Sprechfluss",
        "8-Wochen-Architektur — dein personalisierter Plan",
        "Zusammenfassung — Kernergebnisse in deiner Sprache"
    ],
    "en": [
        "Precise Perception — what happened in your session",
        "Structural Strengths — what you do well (with evidence)",
        "Core Structural Insight — the one pattern that defines this session",
        "Top 5 Structural Problems — with transcript evidence",
        "5 Lever Corrections — the changes with the highest impact",
        "Top 5 Solutions — concrete drills with expected outcomes",
        "Sentence Engine — your personalized daily drill",
        "Homework A, B, C — structure, precision, and fluency exercises",
        "8-Week Training Architecture — your personalized roadmap",
        "Full Summary — key findings in your language"
    ],
    "ru": [
        "Точное восприятие — что произошло на занятии",
        "Структурные сильные стороны — что ты делаешь хорошо",
        "Ключевое структурное наблюдение — главный паттерн",
        "Топ-5 структурных проблем — с доказательствами",
        "5 рычажных коррекций — максимальный эффект",
        "Топ-5 решений — конкретные упражнения",
        "Речевой двигатель — ежедневное упражнение",
        "Домашние задания A, B, C — структура, точность, беглость",
        "8-недельный план — персональный план",
        "Полное резюме — ключевые результаты"
    ],
    "uk": [
        "Точне спостереження — що сталося на занятті",
        "Структурні сильні сторони — що ти робиш добре",
        "Ключове спостереження — головний патерн",
        "Топ-5 структурних проблем — з доказами",
        "5 важільних корекцій — максимальний ефект",
        "Топ-5 рішень — конкретні вправи",
        "Мовний двигун — щоденна вправа",
        "Домашні завдання A, B, C — структура, точність, плавність",
        "8-тижневий план — персональний план",
        "Повне резюме — ключові результати"
    ],
    "fr": [
        "Perception précise — ce qui s'est passé en session",
        "Forces structurelles — ce que tu fais bien",
        "Insight structurel central — le schéma clé",
        "Top 5 problèmes structurels — avec preuves",
        "5 corrections leviers — les changements clés",
        "Top 5 solutions — exercices concrets",
        "Moteur de phrase — ton exercice quotidien",
        "Devoirs A, B, C — structure, précision, fluidité",
        "Architecture de 8 semaines — ton plan",
        "Résumé complet — résultats clés dans ta langue"
    ],
    "es": [
        "Percepción precisa — qué pasó en tu sesión",
        "Fortalezas estructurales — qué haces bien",
        "Insight estructural central — el patrón clave",
        "Top 5 problemas estructurales — con evidencia",
        "5 correcciones palanca — cambios de mayor impacto",
        "Top 5 soluciones — ejercicios concretos",
        "Motor de oraciones — tu ejercicio diario",
        "Deberes A, B, C — estructura, precisión, fluidez",
        "Arquitectura de 8 semanas — tu plan",
        "Resumen completo — resultados clave en tu idioma"
    ],
    "it": [
        "Percezione precisa — cosa è successo nella sessione",
        "Punti di forza strutturali — cosa fai bene",
        "Intuizione strutturale centrale — il pattern chiave",
        "Top 5 problemi strutturali — con prove",
        "5 correzioni leva — cambiamenti a maggior impatto",
        "Top 5 soluzioni — esercizi concreti",
        "Motore frasale — il tuo esercizio quotidiano",
        "Compiti A, B, C — struttura, precisione, fluenza",
        "Architettura di 8 settimane — il tuo piano",
        "Riepilogo completo — risultati chiave nella tua lingua"
    ],
    "sr": [
        "Прецизна перцепција — шта се десило",
        "Структурне снаге — шта добро радиш",
        "Кључни увид — главни образац",
        "Топ 5 проблема — са доказима",
        "5 корекција — највећи ефекат",
        "Топ 5 решења — конкретне вежбе",
        "Мотор реченице — дневна вежба",
        "Домаћи A, B, C — структура, прецизност, течност",
        "8-недељни план — персонализовани план",
        "Резиме — кључни резултати"
    ],
    "hr": [
        "Precizna percepcija — što se dogodilo",
        "Strukturne snage — što dobro radiš",
        "Ključni uvid — glavni obrazac",
        "Top 5 problema — s dokazima",
        "5 korekcija — najveći učinak",
        "Top 5 rješenja — konkretne vježbe",
        "Motor rečenice — dnevna vježba",
        "Zadaća A, B, C — struktura, preciznost, tečnost",
        "8-tjedni plan — personalizirani plan",
        "Sažetak — ključni rezultati"
    ],
    "bg": [
        "Точно наблюдение — какво се случи",
        "Структурни силни страни — какво правиш добре",
        "Ключово прозрение — главният модел",
        "Топ 5 проблеми — с доказателства",
        "5 корекции — най-голям ефект",
        "Топ 5 решения — конкретни упражнения",
        "Речеви двигател — ежедневно упражнение",
        "Домашна работа A, B, C — структура, прецизност, плавност",
        "8-седмичен план — персонален план",
        "Пълно резюме — ключови резултати"
    ],
    "pl": [
        "Precyzyjna obserwacja — co wydarzyło się na lekcji",
        "Mocne strony — co robisz dobrze (z dowodami)",
        "Kluczowy wgląd — główny wzorzec",
        "Top 5 problemów — z dowodami",
        "5 korekcji dźwigni — największy efekt",
        "Top 5 rozwiązań — konkretne ćwiczenia",
        "Silnik zdań — codzienne ćwiczenie",
        "Zadania domowe A, B, C — struktura, precyzja, płynność",
        "8-tygodniowy plan — spersonalizowany plan",
        "Podsumowanie — kluczowe wyniki w twoim języku"
    ],
    "pt": [
        "Perceção precisa — o que aconteceu na sessão",
        "Forças estruturais — o que fazes bem",
        "Insight central — o padrão chave",
        "Top 5 problemas — com provas",
        "5 correções de alavanca — maior impacto",
        "Top 5 soluções — exercícios concretos",
        "Motor de frase — exercício diário",
        "Trabalhos A, B, C — estrutura, precisão, fluência",
        "Plano de 8 semanas — plano personalizado",
        "Resumo completo — resultados chave"
    ],
    "ar": [
        "الملاحظة الدقيقة — ماذا حدث في جلستك",
        "نقاط القوة البنيوية — ما تفعله جيداً",
        "الرؤية البنيوية المركزية — النمط الرئيسي",
        "أهم 5 مشاكل بنيوية — مع أدلة",
        "5 تصحيحات رافعة — التغييرات الأهم",
        "أفضل 5 حلول — تمارين ملموسة",
        "محرك الجمل — تمرينك اليومي",
        "واجبات A, B, C — البنية، الدقة، الطلاقة",
        "خطة 8 أسابيع — خطتك الشخصية",
        "ملخص كامل — النتائج الرئيسية بلغتك"
    ],
    "tr": [
        "Kesin gözlem — seansında neler oldu",
        "Yapısal güçlü yönler — neleri iyi yapıyorsun",
        "Temel yapısal içgörü — ana kalıp",
        "En önemli 5 sorun — kanıtlarla",
        "5 kaldıraç düzeltmesi — en büyük etki",
        "En iyi 5 çözüm — somut alıştırmalar",
        "Cümle motoru — günlük alıştırman",
        "Ödevler A, B, C — yapı, hassasiyet, akıcılık",
        "8 haftalık plan — kişisel planın",
        "Tam özet — kendi dilinde sonuçlar"
    ],
    "sq": [
        "Perceptimi i saktë — çfarë ndodhi",
        "Pikat e forta — çfarë bën mirë",
        "Vështrimi qendror — modeli kryesor",
        "Top 5 probleme — me dëshmi",
        "5 korrigjime — ndikimi më i madh",
        "Top 5 zgjidhje — ushtrime konkrete",
        "Motori i fjalisë — ushtimi ditor",
        "Detyra A, B, C — strukturë, precizion, rrjedhshmëri",
        "Plani 8-javor — plani personal",
        "Përmbledhje — rezultatet kryesore"
    ],
    "ro": [
        "Percepție precisă — ce s-a întâmplat",
        "Puncte forte — ce faci bine",
        "Insight central — modelul cheie",
        "Top 5 probleme — cu dovezi",
        "5 corecții pârghie — cel mai mare impact",
        "Top 5 soluții — exerciții concrete",
        "Motorul frazei — exercițiul zilnic",
        "Teme A, B, C — structură, precizie, fluență",
        "Plan de 8 săptămâni — planul personalizat",
        "Rezumat complet — rezultate cheie"
    ],
    "hu": [
        "Pontos megfigyelés — mi történt az órádon",
        "Erősségek — mit csinálsz jól",
        "Központi felismerés — a fő minta",
        "Top 5 probléma — bizonyítékokkal",
        "5 emelő korrekció — legnagyobb hatás",
        "Top 5 megoldás — konkrét gyakorlatok",
        "Mondatmotor — napi gyakorlat",
        "Házi feladat A, B, C — struktúra, pontosság, folyékonyság",
        "8 hetes terv — személyes terv",
        "Összefoglalás — kulcseredmények"
    ],
    "cs": [
        "Přesné vnímání — co se stalo",
        "Silné stránky — co děláš dobře",
        "Klíčový vhled — hlavní vzorec",
        "Top 5 problémů — s důkazy",
        "5 korekcí — největší dopad",
        "Top 5 řešení — konkrétní cvičení",
        "Větný motor — denní cvičení",
        "Úkoly A, B, C — struktura, přesnost, plynulost",
        "8-týdenní plán — osobní plán",
        "Shrnutí — klíčové výsledky"
    ],
    "no": [
        "Presis observasjon",
        "Strukturelle styrker",
        "Sentral innsikt",
        "Topp 5 problemer",
        "5 korreksjoner",
        "Topp 5 løsninger",
        "Setningsmotor",
        "Lekser A, B, C",
        "8-ukersplan",
        "Sammendrag"
    ],
    "sv": [
        "Precis observation",
        "Strukturella styrkor",
        "Central insikt",
        "Topp 5 problem",
        "5 korrektioner",
        "Topp 5 lösningar",
        "Meningsmotor",
        "Läxor A, B, C",
        "8-veckorsplan",
        "Sammanfattning"
    ],
    "fi": [
        "Tarkka havainto",
        "Rakenteelliset vahvuudet",
        "Keskeinen oivallus",
        "Top 5 ongelmaa",
        "5 korjausta",
        "Top 5 ratkaisua",
        "Lausemoottori",
        "Kotitehtävät A, B, C",
        "8 viikon suunnitelma",
        "Yhteenveto"
    ],
    "da": [
        "Præcis observation",
        "Strukturelle styrker",
        "Central indsigt",
        "Top 5 problemer",
        "5 korrektioner",
        "Top 5 løsninger",
        "Sætningsmotor",
        "Lektier A, B, C",
        "8-ugersplan",
        "Resumé"
    ],
    "nl": [
        "Precieze observatie",
        "Structurele sterktes",
        "Centraal inzicht",
        "Top 5 problemen",
        "5 correcties",
        "Top 5 oplossingen",
        "Zinsmotor",
        "Huiswerk A, B, C",
        "8-wekenplan",
        "Samenvatting"
    ],
    "hi": [
        "सटीक अवलोकन",
        "संरचनात्मक शक्तियाँ",
        "केंद्रीय अंतर्दृष्टि",
        "शीर्ष 5 समस्याएँ",
        "5 सुधार",
        "शीर्ष 5 समाधान",
        "वाक्य इंजन",
        "गृहकार्य A, B, C",
        "8-सप्ताह योजना",
        "सारांश"
    ]
}
