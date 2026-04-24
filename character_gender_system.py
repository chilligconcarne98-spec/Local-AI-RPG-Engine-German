# -*- coding: utf-8 -*-
"""
👥 GENDER DEFINITIONS FÜR ALLE CHARAKTERE
Definiert Geschlechter für korrekte Pronomen und Ansprache
Verhindert Verwechslungen wie "Shino ist ein Mädchen"
"""


def get_character_genders():
    """👥 Vollständige Gender-Definitionen für alle Charaktere"""

    return {
        # 🏠 HAUPTCHARAKTERE
        "tsunade": {
            "gender": "female",
            "pronouns": {"de": {"er/sie": "sie", "sein/ihr": "ihr", "ihm/ihr": "ihr"}},
            "titles": ["Hokage", "Tsunade-sama", "die legendäre Sannin"],
            "anrede": "weiblich"
        },

        "sukuna": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Junge", "Sukuna-kun"],
            "anrede": "männlich"
        },

        # 🍃 TEAM 7
        "naruto": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Hyperaktive", "Naruto-kun", "der zukünftige Hokage"],
            "anrede": "männlich"
        },

        "sasuke": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Uchiha", "Sasuke-kun", "der Rächer"],
            "anrede": "männlich"
        },

        "sakura": {
            "gender": "female",
            "pronouns": {"de": {"er/sie": "sie", "sein/ihr": "ihr", "ihm/ihr": "ihr"}},
            "titles": ["die Medizin-Ninja", "Sakura-chan", "die Starke"],
            "anrede": "weiblich"
        },

        "kakashi": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["Kakashi-sensei", "der Copy-Ninja", "der späte Sensei"],
            "anrede": "männlich"
        },

        # 👥 ROOKIE 9
        "hinata": {
            "gender": "female",
            "pronouns": {"de": {"er/sie": "sie", "sein/ihr": "ihr", "ihm/ihr": "ihr"}},
            "titles": ["Hinata-chan", "die Schüchterne", "Byakugan-Prinzessin"],
            "anrede": "weiblich"
        },

        "shino": {  # 🔥 WICHTIG: Shino ist MÄNNLICH!
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Geheimnisvolle", "Shino-kun", "der Insekten-Nutzer"],
            "anrede": "männlich",
            "note": "Oft fälschlicherweise für weiblich gehalten wegen ruhiger Art"
        },

        "kiba": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Wilde", "Kiba-kun", "der Hunde-Ninja"],
            "anrede": "männlich"
        },

        "neji": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["das Genie", "Neji-kun", "der Schicksals-Philosoph"],
            "anrede": "männlich"
        },

        "shikamaru": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Faule", "das Strategie-Genie", "Shikamaru-kun"],
            "anrede": "männlich"
        },

        "choji": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Freundliche", "Choji-kun", "der Große"],
            "anrede": "männlich"
        },

        "ino": {
            "gender": "female",
            "pronouns": {"de": {"er/sie": "sie", "sein/ihr": "ihr", "ihm/ihr": "ihr"}},
            "titles": ["die Eitle", "Ino-chan", "die Schöne"],
            "anrede": "weiblich"
        },

        "tenten": {
            "gender": "female",
            "pronouns": {"de": {"er/sie": "sie", "sein/ihr": "ihr", "ihm/ihr": "ihr"}},
            "titles": ["die Waffen-Expertin", "Tenten-chan", "die Präzise"],
            "anrede": "weiblich"
        },

        "lee": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Enthusiast", "Lee-kun", "der grüne Blitz"],
            "anrede": "männlich"
        },

        # 👨‍🏫 ERWACHSENE/SENSEI
        "guy": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["Guy-sensei", "der Jugend-Enthusiast", "Might Guy"],
            "anrede": "männlich"
        },

        "asuma": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["Asuma-sensei", "der Raucher", "der väterliche Sensei"],
            "anrede": "männlich"
        },

        "kurenai": {
            "gender": "female",
            "pronouns": {"de": {"er/sie": "sie", "sein/ihr": "ihr", "ihm/ihr": "ihr"}},
            "titles": ["Kurenai-sensei", "die Genjutsu-Meisterin", "die Elegante"],
            "anrede": "weiblich"
        },

        "shizune": {
            "gender": "female",
            "pronouns": {"de": {"er/sie": "sie", "sein/ihr": "ihr", "ihm/ihr": "ihr"}},
            "titles": ["Shizune-san", "die Assistentin", "die Medizin-Expertin"],
            "anrede": "weiblich"
        },

        # 👑 CLAN-OBERHÄUPTER
        "hiashi": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["Hiashi-san", "das Clan-Oberhaupt", "der Hyuga-Patriarch"],
            "anrede": "männlich"
        },

        "tsume": {
            "gender": "female",
            "pronouns": {"de": {"er/sie": "sie", "sein/ihr": "ihr", "ihm/ihr": "ihr"}},
            "titles": ["Tsume-san", "die Wilde", "die Inuzuka-Matriarchin"],
            "anrede": "weiblich"
        },

        "choza": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["Choza-san", "der Freundliche", "das Akimichi-Oberhaupt"],
            "anrede": "männlich"
        },

        "danzo": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["Danzo-sama", "der Kriegsfalke", "ROOT-Anführer"],
            "anrede": "männlich"
        },

        "shikaku": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["Shikaku-san", "der Stratege", "Nara-Oberhaupt"],
            "anrede": "männlich"
        },

        # 💀 BÖSEWICHTE
        "itachi": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Verräter", "das Genie", "der rätselhafte Uchiha"],
            "anrede": "männlich"
        },

        "kisame": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Hai", "das Monster", "der Schwertträger"],
            "anrede": "männlich"
        },

        "pain": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Gott", "Pain-sama", "der Anführer"],
            "anrede": "männlich"
        },

        "orochimaru": {
            "gender": "male",  # Achtung: Orochimaru wechselt Körper, aber ursprünglich männlich
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["die Schlange", "der Verräter", "das Monster"],
            "anrede": "männlich",
            "note": "Wechselt Körper, aber in männlicher Form referenzieren"
        },

        "kabuto": {
            "gender": "male",
            "pronouns": {"de": {"er/sie": "er", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": ["der Spion", "der Medizin-Ninja", "die rechte Hand"],
            "anrede": "männlich"
        }
    }


def get_character_gender(character_name):
    """👤 Holt Gender-Info für spezifischen Charakter"""
    genders = get_character_genders()
    char_lower = character_name.lower()

    if char_lower in genders:
        return genders[char_lower]
    else:
        # Fallback für unbekannte Charaktere
        return {
            "gender": "unknown",
            "pronouns": {"de": {"er/sie": "es", "sein/ihr": "sein", "ihm/ihr": "ihm"}},
            "titles": [f"der/die Unbekannte {character_name}"],
            "anrede": "neutral"
        }


def get_correct_pronoun(character_name, pronoun_type="er/sie"):
    """🔤 Holt korrektes Pronomen für Charakter"""
    gender_info = get_character_gender(character_name)
    return gender_info["pronouns"]["de"].get(pronoun_type, "er/sie")


def create_gender_prompt_addition(character_name):
    """🎯 Erstellt Gender-Zusatz für AI-Prompts"""
    gender_info = get_character_gender(character_name)

    gender = gender_info["gender"]
    pronouns = gender_info["pronouns"]["de"]

    if gender == "male":
        gender_instruction = f"""
## 👨 GENDER: MÄNNLICH
{character_name.title()} ist ein MANN/JUNGE.
Verwende männliche Pronomen: {pronouns['er/sie']}, {pronouns['sein/ihr']}, {pronouns['ihm/ihr']}
NICHT "sie" verwenden! {character_name.title()} ist MÄNNLICH!
"""
    elif gender == "female":
        gender_instruction = f"""
## 👩 GENDER: WEIBLICH  
{character_name.title()} ist eine FRAU/MÄDCHEN.
Verwende weibliche Pronomen: {pronouns['er/sie']}, {pronouns['sein/ihr']}, {pronouns['ihm/ihr']}
NICHT "er" verwenden! {character_name.title()} ist WEIBLICH!
"""
    else:
        gender_instruction = f"""
## ❓ GENDER: UNBEKANNT
Geschlecht von {character_name.title()} ist unbekannt. Verwende neutrale Sprache.
"""

    return gender_instruction


def add_gender_to_character_personalities():
    """🔧 Fügt Gender-Info zu Character Personalities hinzu"""

    genders = get_character_genders()

    def enhance_personality_with_gender(character_name, personality_data):
        """Erweitert Persönlichkeits-Daten um Gender-Info"""

        if character_name.lower() in genders:
            gender_info = genders[character_name.lower()]

            # Füge Gender-Section hinzu
            personality_data["gender_info"] = {
                "gender": gender_info["gender"],
                "pronouns": gender_info["pronouns"]["de"],
                "titles": gender_info["titles"],
                "anrede": gender_info["anrede"],
                "prompt_addition": create_gender_prompt_addition(character_name)
            }

            # Füge gender-spezifische Speech Examples hinzu
            if gender_info["gender"] == "male":
                if "speech_examples" not in personality_data:
                    personality_data["speech_examples"] = {}

                personality_data["speech_examples"]["gender_reference"] = [
                    f"Ich bin ein Mann.", f"Als Junge...", f"Wir Männer..."
                ]
            elif gender_info["gender"] == "female":
                if "speech_examples" not in personality_data:
                    personality_data["speech_examples"] = {}

                personality_data["speech_examples"]["gender_reference"] = [
                    f"Ich bin eine Frau.", f"Als Mädchen...", f"Wir Frauen..."
                ]

        return personality_data

    return enhance_personality_with_gender


def create_gender_statistics():
    """📊 Erstellt Gender-Statistiken"""
    genders = get_character_genders()

    male_count = sum(1 for info in genders.values() if info["gender"] == "male")
    female_count = sum(1 for info in genders.values() if info["gender"] == "female")

    male_chars = [name for name, info in genders.items() if info["gender"] == "male"]
    female_chars = [name for name, info in genders.items() if info["gender"] == "female"]

    stats = f"""
📊 GENDER STATISTIKEN:

👨 MÄNNLICH ({male_count}):
{', '.join(sorted(male_chars))}

👩 WEIBLICH ({female_count}):
{', '.join(sorted(female_chars))}

⚠️ HÄUFIGE VERWECHSLUNGEN:
• Shino (MÄNNLICH - nicht weiblich!)
• Orochimaru (MÄNNLICH - wechselt Körper aber referenziere als männlich)
• Neji (MÄNNLICH)

💡 INTEGRATION TIPPS:
• Nutze create_gender_prompt_addition() für AI-Prompts
• Verwende get_correct_pronoun() für korrekte Pronomen
• Füge gender_info zu Persönlichkeiten hinzu
"""

    return stats


# 🧪 TEST FUNKTION

def test_gender_system():
    """🧪 Testet das Gender-System"""

    test_characters = ["shino", "hinata", "naruto", "tsunade", "orochimaru"]

    print("🧪 GENDER SYSTEM TEST:")
    print("=" * 30)

    for char in test_characters:
        gender_info = get_character_gender(char)
        pronoun = get_correct_pronoun(char)

        print(f"\n{char.title()}:")
        print(f"  Gender: {gender_info['gender']}")
        print(f"  Pronomen: {pronoun}")
        print(f"  Anrede: {gender_info['anrede']}")

        if "note" in gender_info:
            print(f"  ⚠️ Hinweis: {gender_info['note']}")


if __name__ == "__main__":
    print("👥 CHARACTER GENDER SYSTEM")
    print("=" * 40)

    # Teste das System
    test_gender_system()

    # Zeige Statistiken
    print("\n" + create_gender_statistics())

    # Beispiel für Prompt-Addition
    print("\n🎯 BEISPIEL PROMPT-ADDITION:")
    print(create_gender_prompt_addition("shino"))