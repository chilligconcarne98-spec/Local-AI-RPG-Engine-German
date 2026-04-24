#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌅 ADVANCED ATMOSPHERIC ELEMENTS SYSTEM
Erzeugt dynamische, context-aware atmosphärische Beschreibungen basierend auf:
- current_location (Location tracking)
- game_time (Tageszeit)
- weather conditions
- seasonal variations
- character moods

Integriert sich in get_llm_response() für immersive Beschreibungen
"""

import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class AtmosphericMood(Enum):
    """Verschiedene atmosphärische Stimmungen"""
    PEACEFUL = "peaceful"
    ROMANTIC = "romantic"
    MYSTERIOUS = "mysterious"
    TENSE = "tense"
    COZY = "cozy"
    DRAMATIC = "dramatic"
    MELANCHOLIC = "melancholic"
    ENERGETIC = "energetic"


class AdvancedAtmosphericSystem:
    """🎬 Advanced System für atmosphärische Beschreibungen"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.setup_atmospheric_database()

        # Tracking der letzten Verwendungen (Vermeidung von Wiederholungen)
        self.last_used_elements = []
        self.max_memory = 10

    def setup_atmospheric_database(self):
        """🏗️ Initialisiert die komplette atmosphärische Datenbank"""

        # ========== LOCATION-BASIERTE ATMOSPHÄREN ==========
        self.location_atmospheres = {
            "tsunades_haus": {
                "base_description": "Das gemütliche Zuhause strahlt Wärme und Geborgenheit aus",
                "morning": [
                    "Sanftes Morgenlicht filtert durch die Vorhänge und taucht das Wohnzimmer in goldenes Licht",
                    "Die ersten Sonnenstrahlen des Tages erhellen den Raum mit warmer Atmosphäre",
                    "Friedliche Morgenstimmung erfüllt das Haus mit einer beruhigenden Präsenz"
                ],
                "afternoon": [
                    "Helles Tageslicht durchflutet die Räume und schafft eine lebendige Atmosphäre",
                    "Die warme Nachmittagssonne wirft tanzende Schatten an die Wände",
                    "Eine entspannte Nachmittagsstimmung liegt über dem gemütlichen Heim"
                ],
                "evening": [
                    "Warmes Abendlicht taucht das Haus in romantische, goldene Töne",
                    "Die untergehende Sonne malt sanfte Schatten durch die Fenster",
                    "Eine intime Abendstimmung hüllt das Zuhause in behagliche Wärme"
                ],
                "night": [
                    "Sanftes Kerzenlicht oder Lampen schaffen eine kuschelige Atmosphäre",
                    "Die Dunkelheit draußen macht das Haus zu einem warmen Refugium",
                    "Nächtliche Stille und Intimität erfüllen die vertrauten Räume"
                ],
                "rainy": [
                    "Sanfter Regen prasselt rhythmisch gegen die Fenster",
                    "Das Haus bietet gemütlichen Schutz vor dem Regenwetter draußen",
                    "Regengeräusche schaffen eine beruhigende Geräuschkulisse"
                ],
                "winter": [
                    "Ein warmes Feuer im Kamin knistert behaglich",
                    "Schneeflocken tanzen vor den Fenstern während drinnen Wärme herrscht",
                    "Winterliche Gemütlichkeit erfüllt jeden Winkel des Hauses"
                ]
            },

            "konoha_dorf": {
                "base_description": "Das lebendige Ninja-Dorf pulsiert mit Aktivität und Leben",
                "morning": [
                    "Das Dorf erwacht zu neuem Leben, Händler öffnen ihre Stände",
                    "Morgendliche Geschäftigkeit erfüllt die Straßen von Konoha",
                    "Erste Ninja beginnen ihre täglichen Trainingsroutinen"
                ],
                "afternoon": [
                    "Lebhaftes Treiben charakterisiert die Straßen des Ninja-Dorfes",
                    "Die Mittagssonne beleuchtet die geschäftigen Marktplätze",
                    "Kinder spielen auf den Plätzen während Erwachsene ihren Geschäften nachgehen"
                ],
                "evening": [
                    "Warme Abendstimmung breitet sich über die Dächer von Konoha aus",
                    "Die ersten Lichter gehen in den Häusern und Restaurants an",
                    "Familien versammeln sich zum Abendessen in ihren Heimen"
                ],
                "night": [
                    "Nächtliche Ruhe senkt sich über das schlafende Dorf",
                    "Nur vereinzelte Lichter und Ninja-Patrouillen durchbrechen die Dunkelheit",
                    "Sterne funkeln über den traditionellen Dächern von Konoha"
                ]
            },

            "training_ground": {
                "base_description": "Der Trainingsplatz liegt bereit für intensive Übungen",
                "morning": [
                    "Frische Morgenluft macht den Trainingsplatz ideal für harte Arbeit",
                    "Tau glitzert auf dem Gras des frühmorgendlichen Trainingsgeländes",
                    "Die Ruhe vor dem Training liegt über dem leeren Übungsplatz"
                ],
                "afternoon": [
                    "Intensive Hitze und Sonnenschein fordern die Trainierenden heraus",
                    "Staub wirbelt auf vom intensiven Nachmittagstraining",
                    "Die Sonne brennt erbarmungslos auf den aktiven Trainingsplatz"
                ],
                "evening": [
                    "Sanfte Abendluft macht das Training angenehmer",
                    "Goldenes Abendlicht verleiht dem Training eine magische Atmosphäre",
                    "Die perfekte Zeit für konzentrierte Übungen ohne Tageshitze"
                ]
            },

            "wald": {
                "base_description": "Der geheimnisvolle Wald birgt unbekannte Wunder und Gefahren",
                "morning": [
                    "Morgennebel schwebt mystisch zwischen den alten Bäumen",
                    "Vogelgezwitscher erweckt den Wald zu neuem Leben",
                    "Sonnenstrahlen durchdringen das Blätterdach wie natürliche Scheinwerfer"
                ],
                "afternoon": [
                    "Dappled sunlight creates a natural cathedral in the forest depths",
                    "Das Rauschen der Blätter im Wind schafft eine hypnotische Melodie",
                    "Geheimnisvolle Schatten tanzen zwischen den mächtigen Stämmen"
                ],
                "evening": [
                    "Der Wald verwandelt sich in eine mystische, fast magische Landschaft",
                    "Dämmerlicht lässt jeden Schatten geheimnisvoll und bedeutsam wirken",
                    "Abendliche Waldgeräusche schaffen eine primordiale Atmosphäre"
                ],
                "night": [
                    "Mondschein filtert geisterhaft durch das Blätterdach",
                    "Nächtliche Waldgeräusche erfüllen die Dunkelheit mit Leben",
                    "Jeder Schatten könnte Geheimnisse oder Gefahren bergen"
                ]
            },

            "onsen": {
                "base_description": "Die heißen Quellen strahlen entspannende Ruhe und Heilung aus",
                "morning": [
                    "Sanfter Dampf steigt von den heißen Quellen in die kühle Morgenluft",
                    "Friedliche Morgenstimmung umhüllt die heilenden Gewässer",
                    "Perfekte Ruhe für morgendliche Entspannung und Reflexion"
                ],
                "afternoon": [
                    "Das warme Wasser bietet willkommene Erholung von der Tageshitze",
                    "Entspannende Atmosphäre lädt zu längeren, heilsamen Bädern ein",
                    "Therapeutische Wärme lindert alle Sorgen und Verspannungen"
                ],
                "evening": [
                    "Romantisches Dämmerlicht verstärkt die intime Atmosphäre der Quellen",
                    "Warmer Dampf vermischt sich mit der kühlen Abendluft",
                    "Perfekte Zeit für tiefe Entspannung und emotionale Verbindung"
                ],
                "night": [
                    "Sternenreflektionen tanzen auf der Oberfläche der heißen Quellen",
                    "Nächtliche Intimität und Wärme schaffen unvergessliche Momente",
                    "Die Dunkelheit verstärkt das Gefühl der privaten Oase"
                ]
            }
        }

        # ========== ZEIT-BASIERTE STIMMUNGEN ==========
        self.time_moods = {
            "dawn": ["mystisch", "erwachend", "hoffnungsvoll", "ruhig"],
            "morning": ["energisch", "frisch", "lebendig", "optimistisch"],
            "midday": ["hell", "aktiv", "intensiv", "lebhaft"],
            "afternoon": ["warm", "entspannt", "gemütlich", "friedlich"],
            "evening": ["romantisch", "intim", "golden", "verträumt"],
            "night": ["mysteriös", "intim", "geheimnisvoll", "ruhig"],
            "late_night": ["tief", "still", "privat", "intensiv"]
        }

        # ========== WETTER-EFFEKTE ==========
        self.weather_effects = {
            "sunny": [
                "Strahlender Sonnenschein durchflutet die Szene",
                "Warmes, goldenes Licht verstärkt jede Emotion",
                "Helles Tageslicht lässt alles klar und lebendige wirken"
            ],
            "cloudy": [
                "Sanfte, diffuse Beleuchtung durch Wolken",
                "Gedämpftes Licht schafft eine nachdenkliche Atmosphäre",
                "Bewölkter Himmel verleiht der Szene eine intime Stimmung"
            ],
            "rainy": [
                "Sanfter Regen schafft eine romantische Geräuschkulisse",
                "Regentropfen an den Fenstern verstärken das Gefühl der Geborgenheit",
                "Das Prasseln des Regens bietet beruhigende Hintergrundmusik"
            ],
            "stormy": [
                "Dramatische Sturmwolken verstärken die emotionale Intensität",
                "Blitze erhellen sporadisch die gespannte Atmosphäre",
                "Die Kraft des Sturms spiegelt die innere Dramatik wider"
            ],
            "snowy": [
                "Sanft fallende Schneeflocken schaffen eine märchenhafte Atmosphäre",
                "Winterliche Ruhe liegt über der verschneiten Landschaft",
                "Schneekristalle funkeln wie natürliche Diamanten"
            ]
        }

        # ========== EMOTIONALE MODIFIKATOREN ==========
        self.emotional_atmospheres = {
            AtmosphericMood.ROMANTIC: [
                "Eine intime, fast magnetische Spannung liegt in der Luft",
                "Jede Bewegung, jeder Blick scheint von romantischer Energie erfüllt",
                "Die Atmosphäre pulsiert mit unausgesprochener Anziehung"
            ],
            AtmosphericMood.PEACEFUL: [
                "Tiefe, beruhigende Ruhe erfüllt jeden Winkel des Raumes",
                "Gelassene Stille lädt zu Entspannung und Reflexion ein",
                "Friedliche Energie macht jeden Moment zu einem Geschenk"
            ],
            AtmosphericMood.MYSTERIOUS: [
                "Geheimnisvolle Schatten bergen unbekannte Möglichkeiten",
                "Jede Ecke könnte Überraschungen oder verborgene Wahrheiten enthalten",
                "Mysteriöse Energie macht jeden Moment unvorhersagbar"
            ],
            AtmosphericMood.COZY: [
                "Behagliche Wärme umhüllt wie eine liebevolle Umarmung",
                "Gemütliche Atmosphäre lädt zu intimen Gesprächen ein",
                "Kuschelige Stimmung macht Zeit und Raum irrelevant"
            ],
            AtmosphericMood.DRAMATIC: [
                "Intensive, fast greifbare Spannung elektrisiert die Luft",
                "Jeder Moment scheint von dramatischer Bedeutung erfüllt",
                "Die Atmosphäre ist geladen mit emotionaler Intensität"
            ]
        }

    def generate_atmospheric_description(self, user_input: str = "", ai_response: str = "") -> str:
        """🎭 Generiert dynamische atmosphärische Beschreibung"""

        # 1. Sammle Kontext-Daten
        context = self._gather_context_data()

        # 2. Analysiere emotionalen Ton
        emotional_mood = self._analyze_emotional_mood(user_input, ai_response)

        # 3. Bestimme atmosphärische Elemente
        atmospheric_elements = self._select_atmospheric_elements(context, emotional_mood)

        # 4. Baue finale Beschreibung
        final_description = self._build_atmospheric_description(atmospheric_elements, context)

        # 5. Vermeide Wiederholungen
        final_description = self._ensure_variety(final_description)

        return final_description

    def _gather_context_data(self) -> Dict:
        """📊 Sammelt alle relevanten Kontext-Daten"""

        context = {}

        # Location tracking
        context['location'] = getattr(self.game_data, 'current_location', 'konoha_dorf')

        # Time tracking
        context['time_period'] = self._get_time_period()
        context['game_time'] = self._get_game_time_string()

        # Weather (if available)
        context['weather'] = self._get_current_weather()

        # Character info
        context['character'] = getattr(self.game_data, 'active_character', 'tsunade')

        # Seasonal info
        context['season'] = self._get_current_season()

        return context

    def _get_time_period(self) -> str:
        """🕐 Bestimmt aktuelle Tageszeit"""

        # Versuche game_time_system zu nutzen
        if hasattr(self.game_data, 'time_system'):
            try:
                period = self.game_data.time_system.get_time_period()
                return period.value.lower()
            except:
                pass

        # Fallback auf echte Zeit
        hour = datetime.now().hour
        if 5 <= hour < 7:
            return "dawn"
        elif 7 <= hour < 12:
            return "morning"
        elif 12 <= hour < 14:
            return "midday"
        elif 14 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 21:
            return "evening"
        elif 21 <= hour < 24:
            return "night"
        else:
            return "late_night"

    def _get_game_time_string(self) -> str:
        """📅 Holt formatierte Spielzeit"""

        if hasattr(self.game_data, 'time_system'):
            try:
                return self.game_data.time_system.get_formatted_time()
            except:
                pass

        return datetime.now().strftime("%H:%M")

    def _get_current_weather(self) -> str:
        """🌤️ Bestimmt aktuelles Wetter"""

        # Versuche weather system
        if hasattr(self.game_data, 'time_system'):
            try:
                weather = self.game_data.time_system.current_weather
                return weather.value.lower()
            except:
                pass

        if hasattr(self.game_data, 'environment_system'):
            try:
                weather = self.game_data.environment_system.current_weather
                return weather.lower()
            except:
                pass

        # Zufälliges Wetter als Fallback
        return random.choice(["sunny", "cloudy", "clear"])

    def _get_current_season(self) -> str:
        """🍂 Bestimmt aktuelle Jahreszeit"""

        if hasattr(self.game_data, 'time_system'):
            try:
                return self.game_data.time_system.current_season
            except:
                pass

        # Fallback basierend auf Datum
        month = datetime.now().month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"

    def _analyze_emotional_mood(self, user_input: str, ai_response: str) -> AtmosphericMood:
        """💭 Analysiert emotionale Stimmung für Atmosphäre"""

        combined_text = (user_input + " " + ai_response).lower()

        # Keyword-basierte Stimmungsanalyse
        mood_keywords = {
            AtmosphericMood.ROMANTIC: ["liebe", "küss", "umarm", "nah", "gefühl", "herz", "zärtlich"],
            AtmosphericMood.PEACEFUL: ["ruhig", "entspann", "friedlich", "meditation", "stille"],
            AtmosphericMood.MYSTERIOUS: ["geheimnis", "mystisch", "unbekannt", "schatten", "rätselhaft"],
            AtmosphericMood.COZY: ["gemütlich", "warm", "kuschel", "behaglich", "geborgen"],
            AtmosphericMood.DRAMATIC: ["intensiv", "dramatisch", "spannung", "konflikt", "emotional"],
            AtmosphericMood.MELANCHOLIC: ["traurig", "melancholisch", "nachdenklich", "schwermütig"],
            AtmosphericMood.TENSE: ["angespannt", "nervös", "stress", "konflikt", "sorge"],
            AtmosphericMood.ENERGETIC: ["energie", "aktiv", "lebhaft", "schwung", "motivation"]
        }

        mood_scores = {}
        for mood, keywords in mood_keywords.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > 0:
                mood_scores[mood] = score

        # Wähle Stimmung mit höchstem Score
        if mood_scores:
            return max(mood_scores.keys(), key=lambda x: mood_scores[x])

        return AtmosphericMood.PEACEFUL  # Default

    def _select_atmospheric_elements(self, context: Dict, mood: AtmosphericMood) -> Dict:
        """✨ Wählt passende atmosphärische Elemente"""

        elements = {}

        # 1. Location-basierte Atmosphäre
        location = context['location']
        time_period = context['time_period']

        location_data = self.location_atmospheres.get(location, self.location_atmospheres['konoha_dorf'])

        # Zeitspezifische Beschreibung
        if time_period in location_data:
            elements['location_atmosphere'] = random.choice(location_data[time_period])
        else:
            elements['location_atmosphere'] = location_data.get('base_description', '')

        # 2. Wetter-Effekt (falls passend)
        weather = context.get('weather', 'clear')
        if weather in self.weather_effects and random.random() < 0.4:  # 40% Chance
            elements['weather_effect'] = random.choice(self.weather_effects[weather])

        # 3. Emotionale Atmosphäre
        if mood in self.emotional_atmospheres:
            elements['emotional_atmosphere'] = random.choice(self.emotional_atmospheres[mood])

        # 4. Zeit-basierte Stimmung
        time_mood_words = self.time_moods.get(time_period, ["neutral"])
        elements['time_mood'] = random.choice(time_mood_words)

        return elements

    def _build_atmospheric_description(self, elements: Dict, context: Dict) -> str:
        """🎬 Baut finale atmosphärische Beschreibung"""

        description_parts = []

        # Hauptatmosphäre (Location + Zeit)
        if 'location_atmosphere' in elements:
            description_parts.append(elements['location_atmosphere'])

        # Wetter-Effekt (optional)
        if 'weather_effect' in elements:
            description_parts.append(elements['weather_effect'])

        # Emotionale Verstärkung (bei starker Stimmung)
        if 'emotional_atmosphere' in elements:
            description_parts.append(elements['emotional_atmosphere'])

        # Kombiniere zu flüssiger Beschreibung
        if not description_parts:
            return ""

        # Zufällige Auswahl und Kombination
        if len(description_parts) == 1:
            final_desc = description_parts[0]
        elif len(description_parts) == 2:
            final_desc = f"{description_parts[0]} {description_parts[1]}"
        else:
            # Bei 3+ Elementen: wähle 1-2 zufällig aus
            selected = random.sample(description_parts, min(2, len(description_parts)))
            final_desc = " ".join(selected)

        # Formatierung mit atmosphere marker
        return f"*{final_desc}*\n"

    def _ensure_variety(self, description: str) -> str:
        """🔄 Verhindert Wiederholungen von atmosphärischen Beschreibungen"""

        # Kurze Beschreibung zur Identifikation
        short_desc = description[:50]

        # Prüfe ob kürzlich verwendet
        if short_desc in self.last_used_elements:
            # Versuche alternative Generation
            return ""  # Leere Atmosphäre vermeidet Wiederholung

        # Füge zu verwendeten hinzu
        self.last_used_elements.append(short_desc)

        # Begrenze Memory
        if len(self.last_used_elements) > self.max_memory:
            self.last_used_elements.pop(0)

        return description


def integrate_atmospheric_system(game_data):
    """🌅 Integriert das Atmospheric System in get_llm_response"""

    print("🌅 Integriere Advanced Atmospheric Elements System...")

    # Erstelle Atmospheric System
    atmospheric_system = AdvancedAtmosphericSystem(game_data)
    game_data.atmospheric_system = atmospheric_system

    # Patche get_llm_response Methode
    if hasattr(game_data, 'get_llm_response'):
        original_get_llm_response = game_data.get_llm_response

        def atmospheric_enhanced_llm_response(user_input: str) -> str:
            """🎭 LLM Response mit atmosphärischen Elementen"""

            # Normale Response generieren
            base_response = original_get_llm_response(user_input)

            # Atmosphärische Beschreibung generieren
            atmospheric_description = atmospheric_system.generate_atmospheric_description(
                user_input,
                base_response
            )

            # Kombiniere: Atmosphäre + Response
            if atmospheric_description:
                enhanced_response = atmospheric_description + "\n" + base_response
            else:
                enhanced_response = base_response

            return enhanced_response

        # Ersetze die Methode
        game_data.get_llm_response = atmospheric_enhanced_llm_response
        print("✅ LLM Response mit atmosphärischen Elementen erweitert!")

    # Debug Commands hinzufügen
    _add_atmospheric_debug_commands(game_data)

    print("🎬 ATMOSPHERIC ELEMENTS SYSTEM aktiviert!")
    print("🌟 Features:")
    print("   • Location-basierte Atmosphären")
    print("   • Zeit-sensitive Beschreibungen")
    print("   • Wetter-Effekte")
    print("   • Emotionale Stimmungs-Analyse")
    print("   • Anti-Wiederholungs-System")
    print("   • Debug: /atmo_test, /atmo_debug")

    return atmospheric_system


def _add_atmospheric_debug_commands(game_data):
    """🔧 Fügt Atmospheric Debug Commands hinzu"""

    if hasattr(game_data, 'gui'):
        gui = game_data.gui

        if hasattr(gui, 'handle_command'):
            original_handle_command = gui.handle_command

            def enhanced_handle_command_atmo(user_message):
                """Erweiterte Commands mit Atmospheric Debug"""

                # Atmospheric Test Command
                if user_message.strip().lower().startswith('/atmo_test'):
                    if hasattr(game_data, 'atmospheric_system'):
                        test_description = game_data.atmospheric_system.generate_atmospheric_description(
                            "Ich schaue in die Ferne",
                            "Die Landschaft ist wunderschön"
                        )
                        gui.add_message("ATMOSPHERIC TEST", f"🌅 Generated Description:\n\n{test_description}")
                    else:
                        gui.add_message("ERROR", "Atmospheric System nicht verfügbar")
                    return True

                # Atmospheric Debug Command
                elif user_message.strip().lower() in ['/atmo_debug', '/atmo']:
                    if hasattr(game_data, 'atmospheric_system'):
                        atmo = game_data.atmospheric_system
                        context = atmo._gather_context_data()
                        debug_info = f"""🌅 ATMOSPHERIC SYSTEM DEBUG:

📍 **Kontext-Daten:**
• Location: {context.get('location', 'unknown')}
• Zeit: {context.get('game_time', 'unknown')}
• Periode: {context.get('time_period', 'unknown')}
• Wetter: {context.get('weather', 'unknown')}
• Jahreszeit: {context.get('season', 'unknown')}
• Character: {context.get('character', 'unknown')}

📊 **Verfügbare Locations:**
{list(atmo.location_atmospheres.keys())}

🎭 **Letzte Verwendungen:**
{atmo.last_used_elements[-3:] if atmo.last_used_elements else ['Keine']}

⚙️ **System Status:** Aktiv"""

                        gui.add_message("ATMOSPHERIC DEBUG", debug_info)
                    else:
                        gui.add_message("ERROR", "Atmospheric System nicht verfügbar")
                    return True

                # Force atmospheric generation
                elif user_message.strip().lower().startswith('/force_atmo'):
                    if hasattr(game_data, 'atmospheric_system'):
                        # Zwinge Atmosphäre für aktuellen Kontext
                        forced_description = game_data.atmospheric_system.generate_atmospheric_description(
                            "Zwangs-Atmosphäre", "Test-Response"
                        )
                        gui.add_message("FORCED ATMOSPHERE", f"🎬 {forced_description}")
                    return True

                # Fallback zu original
                return original_handle_command(user_message)

            # Ersetze Command Handler
            gui.handle_command = enhanced_handle_command_atmo


# Utility Function für manuelle Tests
def test_atmospheric_system(game_data):
    """🧪 Testet das Atmospheric System manuell"""

    if not hasattr(game_data, 'atmospheric_system'):
        print("❌ Atmospheric System nicht gefunden!")
        return

    atmo = game_data.atmospheric_system

    test_scenarios = [
        ("Ich schaue in deine Augen", "Du bedeutest mir so viel"),
        ("Es ist so ruhig hier", "Ja, diese Stille ist friedlich"),
        ("Das Wetter ist heute schön", "Perfekt für einen Spaziergang"),
    ]

    print("🧪 === ATMOSPHERIC SYSTEM TEST ===\n")

    for user_input, ai_response in test_scenarios:
        description = atmo.generate_atmospheric_description(user_input, ai_response)
        print(f"INPUT: {user_input}")
        print(f"RESPONSE: {ai_response}")
        print(f"ATMOSPHERE: {description}")
        print("-" * 60)


if __name__ == "__main__":
    print("🌅 ADVANCED ATMOSPHERIC ELEMENTS SYSTEM")
    print("=" * 60)
    print("Verwendung:")
    print("  from atmospheric_elements import integrate_atmospheric_system")
    print("  integrate_atmospheric_system(your_game_data)")
    print("\nFeatures:")
    print("  🏠 Location-basierte Atmosphären")
    print("  🕐 Zeit-sensitive Beschreibungen")
    print("  🌤️ Dynamische Wetter-Effekte")
    print("  💭 Emotionale Stimmungsanalyse")
    print("  🔄 Anti-Wiederholungs-System")
    print("  📊 Debug & Test Commands")