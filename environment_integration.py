# -*- coding: utf-8 -*-
#E:\Complete own AI\system_prompts
"""
UMGEBUNGS-SYSTEM INTEGRATION (VOLLSTÄNDIG SICHER)
Erweitert das Encounter System um detaillierte Umgebungsbeschreibungen und Interaktionen
OHNE AUTOMATISCHE GUI-INTEGRATION
"""

import random
from typing import Dict, Optional
from moduls.environment_system import create_environment_system

class SafeEnhancedEncounterSystem:
    """Sichere Version des erweiterten Encounter Systems OHNE GUI-Integration"""

    def __init__(self, original_encounter_system):
        self.original_encounter = original_encounter_system
        self.environment_system = create_environment_system(original_encounter_system)

        # Keine GUI-Integration - nur Environment Commands
        self.environment_commands = {
            "describe": self.describe_location,
            "interact": self.interact_with_environment,
            "weather": self.check_weather,
            "atmosphere": self.get_atmosphere_report
        }

    def enhanced_location_visit(self, location_name: str) -> Dict:
        """Erweiterte Location-Besuch Funktion mit Umgebungsbeschreibung"""

        # Standard Encounter Check
        encounter_result = self.original_encounter.check_for_encounter(location_name)

        # Erweiterte Umgebungsbeschreibung
        environment_desc = self.environment_system.get_location_description(location_name)

        # Verfügbare Interaktionen
        interactions = self.environment_system.get_interactive_options(location_name)

        # Wetter-Modifikatoren für Encounters
        weather_modifier = self.environment_system.get_weather_encounter_modifier()

        # Charakter-Umgebungs-Interaktionen (falls verfügbar)
        enhanced_encounter = None
        character_environment_action = None

        if encounter_result:
            character = encounter_result["character"]

            # Hole Charakter-Umgebungs-Interaktion falls verfügbar
            if hasattr(self, 'char_env_system') and self.char_env_system:
                try:
                    character_environment_action = self.char_env_system.get_character_environment_action(
                        character, location_name,
                        weather=self.environment_system.current_weather
                    )

                    # Erweiterte Encounter-Beschreibung mit Umgebungsinteraktion
                    enhanced_encounter = {
                        **encounter_result,
                        "environment_interaction": character_environment_action,
                        "enhanced_description": self.char_env_system.generate_environmental_encounter_description(
                            character, location_name, self.environment_system.current_weather
                        ),
                        "interaction_options": self.char_env_system.get_combined_interaction(character, location_name)
                    }
                except Exception as e:
                    print(f"⚠️ Charakter-Umgebungs-Interaktion Fehler: {e}")

        result = {
            "location": location_name,
            "environment_description": environment_desc,
            "encounter_result": enhanced_encounter or encounter_result,
            "available_interactions": interactions,
            "weather_effects": weather_modifier,
            "special_atmosphere": self._get_special_atmosphere(location_name),
            "character_environment_action": character_environment_action
        }

        return result

    def describe_location(self, location_name: str, detailed: bool = True) -> str:
        """Gibt detaillierte Ortsbeschreibung zurück"""
        if location_name not in self.original_encounter.locations:
            return f"❌ Unbekannter Ort: {location_name}"

        # Basis-Info aus dem Encounter System
        location_data = self.original_encounter.locations[location_name]
        encounter_info = f"""📍 **{location_data['name'].split(' - ')[0]}**

{location_data['description']}

"""

        # Erweiterte Umgebungsbeschreibung
        environment_desc = self.environment_system.get_location_description(location_name, detailed=detailed)

        # Encounter-Informationen
        encounter_info += f"""🎯 **Encounter-Informationen:**
• Basis-Rate: {location_data.get('base_encounter_rate', 0) * 100:.0f}%
• Wetter-Modifikator: {self.environment_system.get_weather_encounter_modifier():.1f}x

"""

        # Verfügbare Charaktere nach Seltenheit
        characters = location_data.get('characters', {})
        encounter_info += f"👥 **Mögliche Begegnungen:**\n"
        for rarity, char_list in characters.items():
            if char_list:
                rarity_emoji = self._get_rarity_emoji(rarity)
                char_names = ', '.join([c.title() for c in char_list[:3]])
                if len(char_list) > 3:
                    char_names += f" (+{len(char_list) - 3} weitere)"
                encounter_info += f"  {rarity_emoji} {rarity.title()}: {char_names}\n"

        # Interaktionsmöglichkeiten
        interactions = self.environment_system.get_interactive_options(location_name)
        if interactions:
            encounter_info += f"\n🎮 **Verfügbare Interaktionen:**\n"
            for interaction in interactions.keys():
                encounter_info += f"  • /interact {interaction}\n"

        return environment_desc + "\n" + encounter_info

    def interact_with_environment(self, location_name: str, interaction: str) -> str:
        """Führt eine Umgebungsinteraktion aus"""
        if location_name not in self.original_encounter.locations:
            return f"❌ Du befindest dich nicht an einem gültigen Ort: {location_name}"

        result = self.environment_system.perform_interaction(location_name, interaction)

        # Chance auf zufällige Encounter durch Interaktion
        interaction_encounter_chance = 0.2  # 20% Chance
        if random.random() < interaction_encounter_chance:
            encounter = self.original_encounter.check_for_encounter(location_name)
            if encounter:
                char = encounter['character']
                result += f"\n\n🎭 **Überraschung!** Während deiner Aktivität bemerkst du {char.title()}, der/die ebenfalls hier ist!"

        return result

    def check_weather(self) -> str:
        """Gibt aktuelle Wetter-Info zurück"""
        current_weather = self.environment_system.current_weather
        weather_data = self.environment_system.weather_conditions[current_weather]

        weather_info = f"""🌤️ **Aktuelles Wetter: {weather_data['name']}**

📝 Beschreibung: {weather_data['description']}
🎭 Stimmung: {weather_data['mood']}
🎯 Encounter-Modifikator: {weather_data['effects']['encounter_rate_modifier']:.1f}x

"""
        # Wetteränderung anbieten
        change_msg = self.environment_system.update_weather()
        if change_msg:
            weather_info += f"\n{change_msg}"

        return weather_info

    def get_atmosphere_report(self, location_name: str) -> str:
        """Gibt einen atmosphärischen Bericht für einen Ort zurück"""
        if location_name not in self.original_encounter.locations:
            return f"❌ Unbekannter Ort: {location_name}"

        # Basis-Atmosphäre
        base_desc = self.environment_system.get_location_description(location_name,
                                                                     include_weather=True,
                                                                     include_time=True,
                                                                     detailed=False)

        # Aktuelle Aktivität basierend auf Zeit und Wetter
        activity_level = self._calculate_activity_level(location_name)
        activity_desc = self._get_activity_description(activity_level)

        # NPC-Präsenz Simulation
        npc_presence = self._simulate_npc_presence(location_name)

        atmosphere_report = f"""🎭 **Atmosphärischer Bericht**

{base_desc}

📊 **Aktivitätslevel:** {activity_desc}

👥 **Präsenz:** {npc_presence}

💡 **Tipp:** {self._get_location_tip(location_name)}
"""

        return atmosphere_report

    def _get_special_atmosphere(self, location_name: str) -> Optional[str]:
        """Bestimmt spezielle atmosphärische Effekte"""
        current_weather = self.environment_system.current_weather

        special_combos = {
            ("wald", "misty"): "🌫️ Der neblige Wald wirkt besonders mystisch und geheimnisvoll",
            ("onsen", "rainy"): "🌧️ Das Prasseln des Regens auf das warme Wasser schafft eine meditative Atmosphäre",
            ("training_area", "sunny"): "☀️ Das helle Sonnenlicht motiviert zu intensiverem Training",
            ("dorf_zentrum", "stormy"): "⛈️ Die Menschen suchen Schutz in Geschäften, die Straßen sind leerer",
            ("ramen_stand", "cloudy"): "☁️ Das bewölkte Wetter macht warme Ramen besonders verlockend"
        }

        return special_combos.get((location_name, current_weather))

    def _get_rarity_emoji(self, rarity: str) -> str:
        """Gibt Emoji für Seltenheit zurück"""
        rarity_emojis = {
            'common': '🟢', 'uncommon': '🔵', 'rare': '🟣',
            'epic': '🟡', 'legendary': '🔴', 'mythic': '⚫'
        }
        return rarity_emojis.get(rarity, '⚪')

    def _calculate_activity_level(self, location_name: str) -> float:
        """Berechnet Aktivitätslevel basierend auf Zeit, Wetter und Ort"""
        try:
            import backstory
            current_time = backstory.get_current_game_time()
            hour = current_time.hour
        except:
            hour = 12  # Fallback

        # Basis-Aktivität nach Ort
        base_activity = {
            "dorf_zentrum": 0.8,
            "ramen_stand": 0.6,
            "training_area": 0.7,
            "onsen": 0.4,
            "wald": 0.3,
            "hokage_turm": 0.5,
            "academy": 0.6
        }.get(location_name, 0.5)

        # Zeit-Modifikatoren
        if 6 <= hour < 8:
            time_modifier = 0.3
        elif 8 <= hour < 12:
            time_modifier = 1.0
        elif 12 <= hour < 14:
            time_modifier = 1.2
        elif 14 <= hour < 18:
            time_modifier = 1.0
        elif 18 <= hour < 22:
            time_modifier = 0.8
        else:
            time_modifier = 0.2

        # Wetter-Modifikatoren
        weather_modifier = self.environment_system.get_weather_encounter_modifier()

        return min(1.0, base_activity * time_modifier * weather_modifier)

    def _get_activity_description(self, activity_level: float) -> str:
        """Beschreibt das Aktivitätslevel"""
        if activity_level >= 0.8:
            return "Sehr lebhaft - viel Aktivität und viele Menschen"
        elif activity_level >= 0.6:
            return "Lebhaft - normale Aktivität mit moderatem Menschenaufkommen"
        elif activity_level >= 0.4:
            return "Ruhig - wenige Menschen, entspannte Atmosphäre"
        elif activity_level >= 0.2:
            return "Sehr ruhig - kaum Aktivität, friedliche Stille"
        else:
            return "Menschenleer - fast niemand zu sehen"

    def _simulate_npc_presence(self, location_name: str) -> str:
        """Simuliert NPC-Präsenz basierend auf Aktivitätslevel"""
        activity = self._calculate_activity_level(location_name)

        location_npcs = {
            "dorf_zentrum": ["Händler", "Dorfbewohner", "Reisende", "Kinder"],
            "ramen_stand": ["Koch", "Stammgäste", "hungrige Ninja"],
            "training_area": ["trainierende Ninja", "Instruktoren", "Zuschauer"],
            "onsen": ["entspannte Besucher", "Bademeister"],
            "wald": ["Wildtiere", "gelegentliche Wanderer"],
            "hokage_turm": ["Büroangestellte", "Wachen", "Besucher"],
            "academy": ["Studenten", "Lehrer", "Eltern"]
        }.get(location_name, ["vereinzelte Personen"])

        if activity >= 0.7:
            present_npcs = random.sample(location_npcs, min(len(location_npcs), 3))
            return f"Viele Anwesende: {', '.join(present_npcs)}"
        elif activity >= 0.4:
            present_npcs = random.sample(location_npcs, min(len(location_npcs), 2))
            return f"Einige Anwesende: {', '.join(present_npcs)}"
        elif activity >= 0.2:
            present_npcs = random.sample(location_npcs, 1)
            return f"Wenige Anwesende: {present_npcs[0]}"
        else:
            return "Niemand in Sicht"

    def _get_location_tip(self, location_name: str) -> str:
        """Gibt ortsspezifische Tipps"""
        tips = {
            "dorf_zentrum": "Am besten vormittags besuchen für maximale Aktivität",
            "ramen_stand": "Naruto ist oft zwischen 11-14 Uhr hier anzutreffen",
            "training_area": "Sonniges Wetter motiviert zu besserem Training",
            "onsen": "Abends besonders entspannend und romantisch",
            "wald": "Bei Nebel wirkt alles mystischer, perfekt für seltene Begegnungen",
            "hokage_turm": "Werktags zwischen 9-17 Uhr am aktivsten",
            "academy": "Während der Schulzeit beste Chance auf junge Ninja"
        }
        return tips.get(location_name, "Erkunde die Umgebung und interagiere mit ihr")

# =================================================================
# SICHERE SETUP FUNKTION - KEINE GUI INTEGRATION
# =================================================================

def setup_safe_enhanced_encounter_system(original_encounter_system):
    """SICHERE Setup-Funktion OHNE jede GUI-Integration"""

    # Erstelle das sichere Enhanced System
    enhanced_system = SafeEnhancedEncounterSystem(original_encounter_system)

    # Integriere Charakter-Umgebungs-Interaktionen (falls verfügbar)
    try:
        from moduls.character_environment_interaction import integrate_character_environment_interaction
        char_env_system = integrate_character_environment_interaction(
            enhanced_system.environment_system,
            original_encounter_system
        )
        enhanced_system.char_env_system = char_env_system
        print("🎭 Charakter-Umgebungs-Interaktionen aktiviert!")
    except ImportError as e:
        print(f"⚠️ Charakter-Umgebungs-Interaktionen nicht verfügbar: {e}")
        enhanced_system.char_env_system = None
    except Exception as e:
        print(f"⚠️ Charakter-Umgebungs-Integration Fehler: {e}")
        enhanced_system.char_env_system = None

    print("✅ Sicheres Environment System aktiviert (OHNE GUI-Integration)")
    return enhanced_system

# =================================================================
# TEST FUNKTIONEN
# =================================================================

def test_safe_enhanced_encounter():
    """Test für das sichere Enhanced System"""
    print("🧪 === SAFE ENHANCED ENCOUNTER TEST ===")

    # Mock Original Encounter System
    class MockOriginalEncounter:
        def __init__(self):
            self.locations = {
                "dorf_zentrum": {
                    "name": "Dorfzentrum",
                    "description": "Geschäftiges Zentrum",
                    "base_encounter_rate": 0.8,
                    "characters": {"common": ["naruto", "sakura"]}
                }
            }

        def check_for_encounter(self, location):
            if random.random() < 0.5:
                return {"character": "naruto", "rarity": "common", "type": "normal"}
            return None

    original_encounter = MockOriginalEncounter()
    safe_system = setup_safe_enhanced_encounter_system(original_encounter)

    print("🗺️ Testing safe location visit:")
    result = safe_system.enhanced_location_visit("dorf_zentrum")
    print(f"✅ Environment Description Length: {len(result['environment_description'])}")
    print(f"✅ Available Interactions: {len(result['available_interactions'])}")
    print(f"✅ Weather Effects: {result['weather_effects']}")

    print("\n✅ === SAFE TEST COMPLETE ===")

if __name__ == "__main__":
    test_safe_enhanced_encounter()