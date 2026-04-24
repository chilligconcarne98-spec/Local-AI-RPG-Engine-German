# -*- coding: utf-8 -*-
"""
CHARACTER-ENVIRONMENT INTERACTION SYSTEM
Ermöglicht Charakteren, mit der Umgebung zu interagieren und darauf zu reagieren
"""
#E:\Complete own AI\system_prompts

import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class CharacterEnvironmentInteraction:
    """System für Charakter-Umgebungs-Interaktionen"""

    def __init__(self):
        self.character_environment_behaviors = self._init_character_behaviors()
        self.environmental_triggers = self._init_environmental_triggers()
        self.interaction_combinations = self._init_interaction_combinations()

    def _init_character_behaviors(self) -> Dict:
        """Definiert wie verschiedene Charaktere mit Umgebungen interagieren"""
        return {
            "naruto": {
                "onsen": {
                    "actions": ["planscht herum", "macht Wasserbomben", "entspannt sich laut"],
                    "reactions": ["Das Wasser ist so warm!", "Endlich mal entspannen!", "Ramen wäre jetzt perfekt!"],
                    "triggers": ["hot_water", "steam", "relaxation"]
                },
                "training_area": {
                    "actions": ["übt Rasengan", "macht Klone", "schwitzt intensiv"],
                    "reactions": ["Ich werde stärker!", "Noch eine Runde!", "Sasuke wird staunen!"],
                    "triggers": ["training_equipment", "other_ninjas", "competition"]
                },
                "ramen_stand": {
                    "actions": ["bestellt sofort", "riecht am Dampf", "wippt aufgeregt"],
                    "reactions": ["Das riecht so gut!", "Noch eine Schüssel bitte!", "Bestes Ramen ever!"],
                    "triggers": ["ramen_smell", "cooking_sounds", "hunger"]
                }
            },

            "sakura": {
                "onsen": {
                    "actions": ["entspannt elegant", "pflegt ihre Haare", "genießt die Ruhe"],
                    "reactions": ["So entspannend...", "Meine Haut wird so weich", "Endlich mal Ruhe"],
                    "triggers": ["warm_water", "privacy", "self_care"]
                },
                "training_area": {
                    "actions": ["trainiert Chakra-Kontrolle", "studiert Medizin-Bücher", "übt Heilung"],
                    "reactions": ["Ich muss stärker werden", "Konzentration ist wichtig", "Für mein Team!"],
                    "triggers": ["medical_equipment", "training_dummies", "teamwork"]
                }
            },

            "sasuke": {
                "training_area": {
                    "actions": ["trainiert allein", "perfektioniert Techniken", "schweigt konzentriert"],
                    "reactions": ["...", "Noch nicht stark genug", "Mehr Power..."],
                    "triggers": ["solitude", "training_equipment", "self_improvement"]
                },
                "memorial_stone": {
                    "actions": ["steht stumm da", "berührt die Namen", "erinnert sich"],
                    "reactions": ["...", "Ich werde sie rächen", "Nie wieder..."],
                    "triggers": ["fallen_heroes", "memories", "vengeance"]
                }
            },

            "hinata": {
                "onsen": {
                    "actions": ["entspannt schüchtern", "versteckt sich hinter Dampf", "lauscht der Natur"],
                    "reactions": ["So friedlich...", "N-niemand schaut, oder?", "Die Natur ist schön"],
                    "triggers": ["privacy", "nature_sounds", "peace"]
                },
                "wald": {
                    "actions": ["beobachtet Tiere", "sammelt Blumen", "meditiert leise"],
                    "reactions": ["Die Tiere sind so süß", "Byakugan!", "*flüstert* So schön hier"],
                    "triggers": ["wildlife", "flowers", "natural_beauty"]
                }
            },

            "tsunade": {
                "hokage_turm": {
                    "actions": ["arbeitet an Papieren", "trinkt Sake", "schaut aus dem Fenster"],
                    "reactions": ["So viel Papierkram...", "Das Dorf entwickelt sich gut", "Wo ist mein Sake?"],
                    "triggers": ["paperwork", "village_view", "responsibility"]
                },
                "onsen": {
                    "actions": ["entspannt königlich", "trinkt Sake", "genießt die Wärme"],
                    "reactions": ["Endlich Entspannung", "Das Leben kann schön sein", "Sake und warmes Wasser..."],
                    "triggers": ["luxury", "relaxation", "sake"]
                }
            }
        }

    def _init_environmental_triggers(self) -> Dict:
        """Umgebungsauslöser, die Charakterreaktionen hervorrufen"""
        return {
            "onsen": {
                "weather_effects": {
                    "rainy": "Der Regen auf dem warmen Wasser klingt beruhigend",
                    "cold": "Das warme Wasser ist bei diesem Wetter besonders wohltuend",
                    "misty": "Der Nebel vermischt sich mystisch mit dem Dampf"
                },
                "time_effects": {
                    "evening": "Die Abenddämmerung taucht die Quellen in warmes Licht",
                    "night": "Sterne spiegeln sich im dunklen Wasser",
                    "morning": "Morgendampf steigt von den erwärmten Quellen auf"
                },
                "interaction_opportunities": [
                    "Das warme Wasser lädt zum Entspannen ein",
                    "Dampf umhüllt die Badenden wie ein warmer Schleier",
                    "Mineralgeruch steigt von den natürlichen Quellen auf"
                ]
            },

            "wald": {
                "weather_effects": {
                    "sunny": "Sonnenstrahlen durchbrechen das Blätterdach",
                    "rainy": "Regentropfen prasseln rhythmisch auf die Blätter",
                    "misty": "Mystischer Nebel wabert zwischen den Bäumen"
                },
                "time_effects": {
                    "dawn": "Morgenlicht filtert durch die erwachende Natur",
                    "night": "Mondschein wirft geheimnisvolle Schatten",
                    "dusk": "Abendlicht taucht alles in goldene Töne"
                },
                "interaction_opportunities": [
                    "Äste knacken unter den Füßen",
                    "Vögel zwitschern in den Baumkronen",
                    "Ein Bach murmelt in der Nähe"
                ]
            },

            "training_area": {
                "weather_effects": {
                    "sunny": "Helles Licht motiviert zu intensiverem Training",
                    "cloudy": "Kühle Luft macht längere Trainingseinheiten möglich",
                    "rainy": "Regen macht das Training herausfordernder"
                },
                "interaction_opportunities": [
                    "Trainingsgeräte klirren bei der Nutzung",
                    "Staub wirbelt bei intensiven Bewegungen auf",
                    "Schweißtropfen fallen rhythmisch zu Boden"
                ]
            }
        }

    def _init_interaction_combinations(self) -> Dict:
        """Kombinierte Interaktionen zwischen Spieler, Charakter und Umgebung"""
        return {
            "player_character_environment": {
                "onsen_naruto_player": {
                    "scenario": "Naruto planscht herum während du entspannst",
                    "options": [
                        "Mitmachen und Wasserschlacht beginnen",
                        "Naruto zur Ruhe ermahnen",
                        "Entspannt zuschauen und lachen"
                    ],
                    "outcomes": {
                        "mitmachen": "Naruto freut sich riesig! Ihr habt eine wilde Wasserschlacht!",
                        "ermahnen": "Naruto wird etwas ruhiger, aber grinst immer noch",
                        "zuschauen": "Naruto bemerkt dein Lachen und wird noch übermütiger"
                    }
                },

                "training_area_sasuke_player": {
                    "scenario": "Sasuke trainiert schweigend und intensiv",
                    "options": [
                        "Herausfordern zu einem Sparring",
                        "Sein Training stumm beobachten",
                        "Tipps für seine Technik anbieten"
                    ],
                    "outcomes": {
                        "herausfordern": "Sasuke blickt dich kalt an... 'Wenn du es wagst'",
                        "beobachten": "Sasuke ignoriert dich, aber trainiert noch intensiver",
                        "tipps": "Sasuke stoppt: 'Ich brauche keine Hilfe'"
                    }
                },

                "wald_hinata_player": {
                    "scenario": "Hinata sammelt Blumen und beobachtet Tiere",
                    "options": [
                        "Ihr beim Blumen sammeln helfen",
                        "Gemeinsam Tiere beobachten",
                        "Sie vor einem herabfallenden Ast warnen"
                    ],
                    "outcomes": {
                        "helfen": "Hinata errötet: 'D-danke... das ist sehr nett'",
                        "beobachten": "Hinata flüstert: 'Schau, ein Reh!' *zeigt vorsichtig*",
                        "warnen": "Hinata springt zur Seite: 'Danke! Du hast mich gerettet!'"
                    }
                }
            }
        }

    def get_character_environment_action(self, character: str, location: str,
                                         weather: str = "sunny", time: str = "day") -> Optional[Dict]:
        """Generiert eine Charakter-Umgebungs-Interaktion"""

        character = character.lower()

        if character not in self.character_environment_behaviors:
            return None

        char_behaviors = self.character_environment_behaviors[character]

        if location not in char_behaviors:
            return None

        location_behavior = char_behaviors[location]

        # Zufällige Aktion aus den verfügbaren
        action = random.choice(location_behavior["actions"])
        reaction = random.choice(location_behavior["reactions"])

        # Umgebungskontext hinzufügen
        environment_context = ""
        if location in self.environmental_triggers:
            env_data = self.environmental_triggers[location]

            if weather in env_data.get("weather_effects", {}):
                environment_context += f" {env_data['weather_effects'][weather]}"

            if time in env_data.get("time_effects", {}):
                environment_context += f" {env_data['time_effects'][time]}"

        return {
            "character": character,
            "location": location,
            "action": action,
            "reaction": f'"{reaction}"',
            "environment_context": environment_context,
            "interaction_triggers": location_behavior["triggers"]
        }

    def get_combined_interaction(self, character: str, location: str,
                                 player_action: str = None) -> Optional[Dict]:
        """Generiert eine kombinierte Spieler-Charakter-Umgebung Interaktion"""

        interaction_key = f"{location}_{character.lower()}_player"

        if interaction_key not in self.interaction_combinations["player_character_environment"]:
            return None

        interaction_data = self.interaction_combinations["player_character_environment"][interaction_key]

        result = {
            "scenario": interaction_data["scenario"],
            "options": interaction_data["options"],
            "character": character,
            "location": location
        }

        # Wenn Spieler eine Aktion gewählt hat
        if player_action:
            action_key = player_action.lower()
            for option in interaction_data["options"]:
                if action_key in option.lower():
                    outcome_key = option.split()[0].lower()  # Erstes Wort als Key
                    if outcome_key in interaction_data["outcomes"]:
                        result["outcome"] = interaction_data["outcomes"][outcome_key]
                        break

        return result

    def generate_environmental_encounter_description(self, character: str, location: str,
                                                     weather: str = "sunny") -> str:
        """Generiert eine reiche Encounter-Beschreibung mit Umgebungsinteraktion"""

        char_action = self.get_character_environment_action(character, location, weather)

        if not char_action:
            return f"Du triffst {character.title()} am {location}."

        description = f"""🎭 **ENCOUNTER MIT UMGEBUNGSINTERAKTION**

📍 **Ort:** {location.replace('_', ' ').title()}
🎯 **Charakter:** {character.title()}

🌍 **Szenerie:**
Du näherst dich dem {location.replace('_', ' ')} und bemerkst {character.title()}, der/die {char_action['action']}.{char_action['environment_context']}

🗣️ **{character.title()}** {char_action['reaction']}

🎮 **Du kannst:**
• Mit {character.title()} sprechen
• Die Umgebung erkunden (/interact)
• {character.title()}s Aktivität beobachten

💡 **Tipp:** {character.title()} scheint gerade beschäftigt mit der Umgebung zu sein!"""

        return description

# =================================================================
# INTEGRATION FUNKTIONEN
# =================================================================

def integrate_character_environment_interaction(environment_system, encounter_system):
    """Integriert Charakter-Umgebungs-Interaktionen in das bestehende System"""

    char_env_system = CharacterEnvironmentInteraction()

    def enhanced_encounter_with_environment(location_name: str) -> Dict:
        """Erweiterte Encounter-Funktion mit Charakter-Umgebungs-Interaktionen"""

        # Standard Encounter Check
        encounter = encounter_system.check_for_encounter(location_name)

        if not encounter:
            return None

        character = encounter["character"]

        # Hole Umgebungsinteraktion für diesen Charakter
        char_env_action = char_env_system.get_character_environment_action(
            character, location_name,
            weather=environment_system.current_weather,
            time="day"  # Könnte aus der Zeit kommen
        )

        # Erweiterte Encounter-Daten
        enhanced_encounter = {
            **encounter,
            "environment_interaction": char_env_action,
            "enhanced_description": char_env_system.generate_environmental_encounter_description(
                character, location_name, environment_system.current_weather
            ),
            "interaction_options": char_env_system.get_combined_interaction(character, location_name)
        }

        return enhanced_encounter

    # Ersetze die Standard-Encounter-Funktion
    encounter_system.enhanced_encounter_with_environment = enhanced_encounter_with_environment
    encounter_system.char_env_system = char_env_system

    return char_env_system

# =================================================================
# TEST FUNKTIONEN
# =================================================================

def test_character_environment_interaction():
    """Test für das Charakter-Umgebungs-Interaktionssystem"""

    print("🎭 === CHARACTER ENVIRONMENT INTERACTION TEST ===")

    system = CharacterEnvironmentInteraction()

    test_scenarios = [
        ("naruto", "onsen", "rainy"),
        ("sakura", "training_area", "sunny"),
        ("sasuke", "memorial_stone", "cloudy"),
        ("hinata", "wald", "misty"),
        ("tsunade", "hokage_turm", "sunny")
    ]

    for character, location, weather in test_scenarios:
        print(f"\n🎮 Testing: {character} in {location} bei {weather}")
        print("-" * 50)

        action = system.get_character_environment_action(character, location, weather)
        if action:
            print(f"Action: {action['action']}")
            print(f"Reaction: {action['reaction']}")
            print(f"Environment: {action['environment_context']}")

        description = system.generate_environmental_encounter_description(character, location, weather)
        print(f"\nFull Description:\n{description}")

        print("=" * 50)

if __name__ == "__main__":
    test_character_environment_interaction()