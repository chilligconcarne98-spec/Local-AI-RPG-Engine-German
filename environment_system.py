# -*- coding: utf-8 -*-
#E:\Complete own AI\system_prompts
"""
ERWEITERTE UMGEBUNGS-SYSTEM für Chat RPG
Detaillierte Ortsbeschreibungen, Wettereffekte, Tageszeit-Atmosphäre und Interaktionsmöglichkeiten
"""

import random
from typing import Dict, Optional
# ✅ NEUE sichere Import-Lösung:
try:
    # Versuche zuerst normalen Import (falls backstory im selben Verzeichnis)
    import backstory
except ImportError:
    # Falls nicht gefunden, füge Parent-Directory zum Path hinzu
    import sys
    import os
    # Füge das Hauptverzeichnis (ein Level höher) zum Python-Path hinzu
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    import backstory

class EnvironmentSystem:
    """Erweiterte Umgebungsverwaltung mit atmosphärischen Beschreibungen"""

    def __init__(self, encounter_system):
        self.encounter_system = encounter_system
        self.weather_conditions = self._init_weather_system()
        self.time_atmospheres = self._init_time_atmospheres()
        self.environment_details = self._init_environment_details()
        self.interactive_elements = self._init_interactive_elements()
        self.current_weather = self._generate_weather()

    def _init_weather_system(self) -> Dict:
        """Initialisiert das Wettersystem"""
        return {
            "sunny": {
                "name": "Sonnenschein",
                "description": "Die warmen Sonnenstrahlen durchfluten",
                "mood": "warm und einladend",
                "effects": {"encounter_rate_modifier": 1.1, "mood_boost": True},
                "probability": 0.4
            },
            "cloudy": {
                "name": "Bewölkt",
                "description": "Graue Wolken ziehen über den Himmel und tauchen alles in diffuses Licht",
                "mood": "ruhig und nachdenklich",
                "effects": {"encounter_rate_modifier": 1.0, "mood_neutral": True},
                "probability": 0.3
            },
            "rainy": {
                "name": "Regnerisch",
                "description": "Sanfte Regentropfen fallen rhythmisch",
                "mood": "melancholisch und gemütlich",
                "effects": {"encounter_rate_modifier": 0.8, "indoor_preference": True},
                "probability": 0.15
            },
            "stormy": {
                "name": "Stürmisch",
                "description": "Dunkle Gewitterwolken brauen sich zusammen",
                "mood": "dramatisch und intensiv",
                "effects": {"encounter_rate_modifier": 0.6, "drama_boost": True},
                "probability": 0.05
            },
            "misty": {
                "name": "Nebelig",
                "description": "Geheimnisvoller Nebel wabert",
                "mood": "mystisch und geheimnisvoll",
                "effects": {"encounter_rate_modifier": 0.9, "mystery_boost": True},
                "probability": 0.1
            }
        }

    def _init_time_atmospheres(self) -> Dict:
        """Atmosphärische Beschreibungen nach Tageszeit"""
        return {
            "dawn": {  # 5-7 Uhr
                "name": "Morgendämmerung",
                "description": "Die ersten Sonnenstrahlen brechen durch den Horizont und tauchen die Welt in goldenes Licht",
                "mood": "friedlich und hoffnungsvoll",
                "sounds": ["Vogelgezwitscher", "leichte Brise", "erwachende Natur"]
            },
            "morning": {  # 7-12 Uhr
                "name": "Vormittag",
                "description": "Die Morgensonne erfüllt die Luft mit warmer Energie",
                "mood": "lebhaft und energiegeladen",
                "sounds": ["geschäftige Aktivität", "Schritte auf den Wegen", "fröhliche Stimmen"]
            },
            "midday": {  # 12-15 Uhr
                "name": "Mittag",
                "description": "Die Sonne steht hoch am Himmel und spendet intensive Wärme",
                "mood": "hell und kraftvoll",
                "sounds": ["summende Insekten", "raschelnde Blätter", "ferne Gespräche"]
            },
            "afternoon": {  # 15-18 Uhr
                "name": "Nachmittag",
                "description": "Das warme Nachmittagslicht verleiht allem einen goldenen Schimmer",
                "mood": "entspannt und gemütlich",
                "sounds": ["sanfter Wind", "spielende Kinder", "gelegentliches Lachen"]
            },
            "evening": {  # 18-22 Uhr
                "name": "Abend",
                "description": "Die Abendsonne taucht den Himmel in orange und purpurne Farben",
                "mood": "romantisch und besinnlich",
                "sounds": ["zirpende Grillen", "leise Unterhaltungen", "das Prasseln von Lagerfeuern"]
            },
            "night": {  # 22-5 Uhr
                "name": "Nacht",
                "description": "Sterne funkeln am dunklen Himmel, während der Mond seinen silbernen Schein wirft",
                "mood": "geheimnisvoll und ruhig",
                "sounds": ["Eulenschreie", "raschelnde Blätter", "ferne Schritte"]
            }
        }

    def _init_environment_details(self) -> Dict:
        """Detaillierte Umgebungsbeschreibungen für jeden Ort"""
        return {
            "dorf_zentrum": {
                "base_description": "Das pulsierende Herz von Konohagakure",
                "detailed_description": {
                    "architecture": "Traditionelle Holzhäuser mit geschwungenen Dächern reihen sich entlang gepflasterter Straßen",
                    "atmosphere": "Geschäftige Ninja und Dorfbewohner eilen vorbei, während Händler ihre Waren anpreisen",
                    "landmarks": ["der große Brunnen im Zentrum", "bunte Marktstände",
                                  "das Bulletin-Board für Missionen"],
                    "smells": ["frisch gebackenes Brot", "würzige Gewürze", "blühende Kirschbäume"],
                    "textures": ["glatte Pflastersteine", "warmes Holz", "weiche Stoffe an den Marktständen"]
                },
                "special_features": {
                    "market_day": "Zusätzliche Marktstände mit exotischen Waren",
                    "festival": "Bunte Dekorationen und feiernde Menschen",
                    "quiet_hours": "Leere Straßen mit nur wenigen Laternen"
                }
            },

            "training_area": {
                "base_description": "Weitläufige Trainingsplätze für ernsthafte Ninja-Übungen",
                "detailed_description": {
                    "architecture": "Robuste Übungspfähle und Zielscheiben sind strategisch über das Gelände verteilt",
                    "atmosphere": "Die Luft vibriert vor Anspannung und Entschlossenheit der trainierenden Ninja",
                    "landmarks": ["die zerbeulte Trainingsbrücke", "Waffenständer", "Meditationskreise aus Steinen"],
                    "smells": ["Schweiß", "aufgewirbelter Staub", "metallene Waffen"],
                    "textures": ["fester Lehmboden", "splittrige Holzpfähle", "kühles Metall"]
                },
                "special_features": {
                    "intensive_training": "Doppelt so viele Ninja trainieren mit erhöhter Intensität",
                    "weapon_practice": "Klirren von Metall und zischende Shuriken durch die Luft",
                    "meditation_time": "Stille Ruhe mit nur gelegentlichem Vogelgezwitscher"
                }
            },

            "onsen": {
                "base_description": "Entspannende heiße Quellen in natürlicher Umgebung",
                "detailed_description": {
                    "architecture": "Natürliche Steinbecken umgeben von traditionellen Holzumkleiden",
                    "atmosphere": "Dampfiger Nebel steigt von den warmen Quellen auf und schafft eine traumhafte Atmosphäre",
                    "landmarks": ["dampfende Quellbecken", "Bambuszäune für Privatsphäre", "steinerne Laternen"],
                    "smells": ["mineralreiches Quellwasser", "Dampf", "blühender Jasmin"],
                    "textures": ["glattes Quellgestein", "warmes Wasser", "weiche Handtücher"]
                },
                "special_features": {
                    "peak_hours": "Viele Besucher genießen die entspannende Atmosphäre",
                    "private_time": "Ruhige, intime Momente mit nur wenigen Gästen",
                    "evening_ambiance": "Laternen werfen warmes Licht auf das dampfende Wasser"
                }
            },

            "wald": {
                "base_description": "Dichter, mystischer Wald um Konoha",
                "detailed_description": {
                    "architecture": "Hohe, uralte Bäume bilden ein natürliches Dach über verschlungenen Pfaden",
                    "atmosphere": "Geheimnisvolles Halbdunkel, durchbrochen von tanzenden Lichtstrahlen",
                    "landmarks": ["der uralte Geisterbaum", "versteckte Höhlen", "sprudelnde Bäche"],
                    "smells": ["feuchte Erde", "Moos", "wilde Blüten"],
                    "textures": ["weiche Blätter unter den Füßen", "raue Baumrinde", "kühle, feuchte Luft"]
                },
                "special_features": {
                    "full_moon": "Silbernes Mondlicht filtert durch die Äste und schafft mystische Schatten",
                    "deep_forest": "Dichtere Vegetation mit vermehrten Tiergeräuschen",
                    "clearings": "Lichtdurchflutete Lichtungen mit wilden Blumenwiesen"
                }
            },

            "ramen_stand": {
                "base_description": "Narutos beliebter Ramen-Stand - ein Ort der Gemeinschaft",
                "detailed_description": {
                    "architecture": "Eine rustikale Holztheke mit hängenden Laternen und Barhockern",
                    "atmosphere": "Warme, einladende Stimmung mit dem stetigen Blubbern der Brühen-Töpfe",
                    "landmarks": ["die dampfenden Ramen-Töpfe", "bunte Menütafeln", "Narutos Stammplatz"],
                    "smells": ["reichhaltige Miso-Brühe", "frische Nudeln", "gebratene Zwiebeln"],
                    "textures": ["warme Holzoberflächen", "glatte Porzellanschalen", "dampfende Hitze"]
                },
                "special_features": {
                    "busy_hours": "Lange Warteschlangen und lebhafte Gespräche",
                    "quiet_service": "Intime Atmosphäre mit wenigen Stammgästen",
                    "special_menu": "Der Koch experimentiert mit neuen, exotischen Ramen-Varianten"
                }
            },

            "hokage_turm": {
                "base_description": "Das administrative Herzstück von Konoha",
                "detailed_description": {
                    "architecture": "Ein imposanter Turm mit breiten Treppen und verglasten Büroräumen",
                    "atmosphere": "Formelle, respektvolle Stimmung mit geschäftiger, aber geordneter Aktivität",
                    "landmarks": ["die große Hokage-Statue", "Archivräume", "Balkon mit Dorfblick"],
                    "smells": ["Pergament und Tinte", "poliertes Holz", "frische Blumen"],
                    "textures": ["kühler Marmorboden", "warmes Holz der Möbel", "schwere Vorhänge"]
                },
                "special_features": {
                    "official_business": "Erhöhte Sicherheit und formal gekleidete Beamte",
                    "quiet_hours": "Gedämpfte Aktivität mit nur wesentlichem Personal",
                    "ceremony_prep": "Dekorationen und Vorbereitungen für offizielle Veranstaltungen"
                }
            }
        }

    def _init_interactive_elements(self) -> Dict:
        """Interaktive Elemente für jeden Ort"""
        return {
            "dorf_zentrum": {
                "inspect_fountain": "Du betrachtest den kunstvollen Brunnen. Das Wasser sprudelt melodisch und spiegelt das Licht.",
                "browse_market": "Du schlenderst zwischen den Marktständen umher und entdeckst interessante Waren.",
                "read_board": "Das Missions-Board zeigt verschiedene verfügbare Aufträge für Ninja aller Ränge.",
                "sit_bench": "Du setzt dich auf eine Bank und beobachtest das geschäftige Treiben des Dorfes."
            },
            "training_area": {
                "practice_target": "Du übst an den Zielscheiben. Deine Präzision verbessert sich merklich.",
                "meditate_circle": "Du findest innere Ruhe im Steinkreis. Deine Chakra-Kontrolle stabilisiert sich.",
                "examine_weapons": "Die Trainingswaffen sind gut gepflegt und zeigen Spuren intensiver Nutzung.",
                "test_strength": "Du testest deine Kraft an den Übungspfählen. Ein zufriedenstellendes Gefühl."
            },
            "onsen": {
                "enter_water": "Du gleitest in das warme Wasser. Sofort entspannen sich deine Muskeln.",
                "enjoy_view": "Du bewunderst die natürliche Schönheit der Umgebung. Sehr friedlich.",
                "feel_steam": "Der warme Dampf umhüllt dich wie eine sanfte Umarmung.",
                "listen_nature": "Du lauschst den beruhigenden Geräuschen der Natur um dich herum."
            },
            "wald": {
                "climb_tree": "Du kletterst geschickt einen Baum hinauf und gewinnst eine neue Perspektive.",
                "follow_path": "Du folgst einem versteckten Pfad tiefer in den mystischen Wald hinein.",
                "listen_wildlife": "Du lauschst den vielfältigen Geräuschen der Waldtiere.",
                "gather_herbs": "Du sammelst nützliche Kräuter und Heilpflanzen für später."
            },
            "ramen_stand": {
                "order_ramen": "Du bestellst eine dampfende Schüssel Ramen. Der Duft ist unwiderstehlich.",
                "chat_cook": "Du unterhältst dich mit dem freundlichen Koch über seine Rezepte.",
                "watch_preparation": "Du beobachtest fasziniert die kunstvolle Zubereitung der Ramen.",
                "enjoy_atmosphere": "Du genießt die warme, gemeinschaftliche Atmosphäre des Standes."
            },
            "hokage_turm": {
                "view_village": "Vom Balkon aus hast du einen atemberaubenden Blick über ganz Konoha.",
                "study_documents": "Du liest interessante Berichte über die Geschichte des Dorfes.",
                "admire_statue": "Du betrachtest ehrfurchtsvoll die imposante Hokage-Statue.",
                "feel_importance": "Die Atmosphäre der Macht und Verantwortung ist spürbar."
            }
        }

    def get_location_description(self, location_name: str, include_weather: bool = True,
                                 include_time: bool = True, detailed: bool = True) -> str:
        """Generiert eine vollständige Ortsbeschreibung"""

        if location_name not in self.environment_details:
            return f"Du befindest dich an einem unbekannten Ort: {location_name}"

        location_data = self.environment_details[location_name]
        description = f"🗺️ {location_data['base_description']}\n\n"

        # Wetter hinzufügen
        if include_weather:
            weather_desc = self._get_weather_description()
            description += f"🌤️ {weather_desc}\n\n"

        # Tageszeit hinzufügen
        if include_time:
            time_desc = self._get_time_description()
            description += f"⏰ {time_desc}\n\n"

        # Detaillierte Beschreibung
        if detailed:
            details = location_data['detailed_description']
            description += f"🏗️ **Architektur:** {details['architecture']}\n"
            description += f"🎭 **Atmosphäre:** {details['atmosphere']}\n"
            description += f"📍 **Markante Punkte:** {', '.join(details['landmarks'])}\n"
            description += f"👃 **Gerüche:** {', '.join(details['smells'])}\n"
            description += f"✋ **Oberflächenbeschaffenheit:** {', '.join(details['textures'])}\n\n"

            # Spezielle Features basierend auf aktuellen Bedingungen
            special = self._get_special_features(location_name)
            if special:
                description += f"✨ **Besonderheiten:** {special}\n\n"

        return description

    def get_interactive_options(self, location_name: str) -> Dict[str, str]:
        """Gibt verfügbare Interaktionen für einen Ort zurück"""
        return self.interactive_elements.get(location_name, {})

    def perform_interaction(self, location_name: str, interaction: str) -> str:
        """Führt eine Interaktion aus und gibt das Ergebnis zurück"""
        interactions = self.get_interactive_options(location_name)

        if interaction in interactions:
            base_result = interactions[interaction]

            # Füge wetterbasierte Modifikationen hinzu
            weather_mod = self._get_weather_interaction_modifier()
            if weather_mod:
                base_result += f" {weather_mod}"

            return base_result
        else:
            return f"❌ Diese Interaktion ist an diesem Ort nicht verfügbar."

    def _generate_weather(self) -> str:
        """Generiert zufälliges Wetter basierend auf Wahrscheinlichkeiten"""
        rand = random.random()
        cumulative = 0

        for weather, data in self.weather_conditions.items():
            cumulative += data['probability']
            if rand <= cumulative:
                return weather

        return 'sunny'  # Fallback

    def _get_weather_description(self) -> str:
        """Gibt Wetterbeschreibung zurück"""
        weather_data = self.weather_conditions[self.current_weather]
        return f"{weather_data['description']} die Umgebung in eine {weather_data['mood']} Stimmung."

    def _get_time_description(self) -> str:
        """Gibt zeitbasierte Beschreibung zurück"""
        current_time = backstory.get_current_game_time()
        hour = current_time.hour

        if 5 <= hour < 7:
            time_period = "dawn"
        elif 7 <= hour < 12:
            time_period = "morning"
        elif 12 <= hour < 15:
            time_period = "midday"
        elif 15 <= hour < 18:
            time_period = "afternoon"
        elif 18 <= hour < 22:
            time_period = "evening"
        else:
            time_period = "night"

        time_data = self.time_atmospheres[time_period]
        sounds_desc = ', '.join(time_data['sounds'])
        return f"{time_data['description']} Die {time_data['mood']} Stimmung wird begleitet von {sounds_desc}."

    def _get_special_features(self, location_name: str) -> Optional[str]:
        """Bestimmt spezielle Features basierend auf aktuellen Bedingungen"""
        location_data = self.environment_details[location_name]
        special_features = location_data.get('special_features', {})

        # Logik für spezielle Bedingungen (vereinfacht)
        current_time = backstory.get_current_game_time()
        hour = current_time.hour

        if location_name == "ramen_stand" and 11 <= hour <= 14:
            return special_features.get('busy_hours')
        elif location_name == "onsen" and 18 <= hour <= 22:
            return special_features.get('evening_ambiance')
        elif location_name == "wald" and self.current_weather == "misty":
            return special_features.get('deep_forest')
        elif location_name == "dorf_zentrum" and 6 <= hour <= 18:
            return special_features.get('market_day')

        return None

    def _get_weather_interaction_modifier(self) -> Optional[str]:
        """Gibt wetterbasierte Interaktionsmodifikationen zurück"""
        weather_effects = {
            "rainy": "Der sanfte Regen verleiht der Erfahrung eine melancholische Note.",
            "sunny": "Das warme Sonnenlicht macht die Aktivität besonders angenehm.",
            "misty": "Der mystische Nebel fügt der Erfahrung eine geheimnisvolle Komponente hinzu.",
            "stormy": "Der dramatische Sturm verstärkt die Intensität der Erfahrung.",
            "cloudy": ""  # Neutral
        }

        return weather_effects.get(self.current_weather, "")

    def update_weather(self) -> str:
        """Aktualisiert das Wetter und gibt Änderungsbeschreibung zurück"""
        old_weather = self.current_weather
        self.current_weather = self._generate_weather()

        if old_weather != self.current_weather:
            old_name = self.weather_conditions[old_weather]['name']
            new_name = self.weather_conditions[self.current_weather]['name']
            return f"🌤️ Das Wetter hat sich von {old_name} zu {new_name} geändert!"

        return ""

    def get_weather_encounter_modifier(self) -> float:
        """Gibt Wetter-Modifikator für Encounter-Raten zurück"""
        return self.weather_conditions[self.current_weather]['effects']['encounter_rate_modifier']

# =================================================================
# INTEGRATION FUNKTIONEN
# =================================================================

def create_environment_system(encounter_system):
    """Factory-Funktion für das Environment System"""
    return EnvironmentSystem(encounter_system)

def get_detailed_location_info(location_name: str, environment_system) -> Dict:
    """Gibt vollständige Locationinfo mit Umgebungsdetails zurück"""
    if not environment_system:
        return {"error": "Environment System nicht verfügbar"}

    return {
        "location": location_name,
        "description": environment_system.get_location_description(location_name),
        "interactions": environment_system.get_interactive_options(location_name),
        "weather": environment_system.current_weather,
        "weather_effects": environment_system.get_weather_encounter_modifier()
    }

# =================================================================
# TEST FUNKTIONEN
# =================================================================

def test_environment_system():
    """Test-Funktion für das Environment System"""
    print("🌍 === ENVIRONMENT SYSTEM TEST ===")

    # Mock Encounter System
    class MockEncounterSystem:
        def __init__(self):
            self.locations = {}

    mock_encounter = MockEncounterSystem()
    env_system = EnvironmentSystem(mock_encounter)

    # Teste verschiedene Locations
    test_locations = ["dorf_zentrum", "onsen", "wald", "ramen_stand"]

    for location in test_locations:
        print(f"\n📍 === {location.upper()} ===")
        desc = env_system.get_location_description(location)
        print(desc)

        print("🎮 Verfügbare Interaktionen:")
        interactions = env_system.get_interactive_options(location)
        for interaction, description in interactions.items():
            print(f"  • {interaction}: {description}")

        print("-" * 50)

    # Teste Wetteränderung
    print(f"\n🌦️ Wettertest:")
    for i in range(3):
        weather_change = env_system.update_weather()
        if weather_change:
            print(f"  {weather_change}")
        else:
            print(f"  Wetter bleibt {env_system.weather_conditions[env_system.current_weather]['name']}")

    print("\n✅ === TEST COMPLETE ===")

if __name__ == "__main__":
    test_environment_system()