# -*- coding: utf-8 -*-
"""
👥 COMPANION SYSTEM - Charaktere mitnehmen auf Reisen
Erweitert das RPG um die Möglichkeit, NPCs als Begleiter mitzunehmen
"""

import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class CompanionStatus(Enum):
    """Status eines Begleiters"""
    AVAILABLE = "available"  # Verfügbar zum Mitnehmen
    FOLLOWING = "following"  # Folgt Sukuna aktiv
    BUSY = "busy"  # Beschäftigt, nicht verfügbar
    REJECTED = "rejected"  # Hat Ablehnung geäußert
    SUGGESTED = "suggested"  # Hat selbst vorgeschlagen mitzukommen


class CompanionMood(Enum):
    """Stimmung des Begleiters"""
    EXCITED = "excited"  # Aufgeregt mitzukommen
    WILLING = "willing"  # Bereit mitzukommen
    NEUTRAL = "neutral"  # Neutral
    HESITANT = "hesitant"  # Zögerlich
    UNWILLING = "unwilling"  # Unwillig


@dataclass
class Companion:
    """Begleiter-Objekt mit Status und Eigenschaften"""
    character_name: str
    status: CompanionStatus
    mood: CompanionMood
    current_location: str
    relationship_level: int

    # Companion-spezifische Eigenschaften
    suggested_locations: List[str]  # Orte die sie vorschlagen
    travel_preferences: List[str]  # Bevorzugte Reiseziele
    rejection_reasons: List[str]  # Gründe für Ablehnungen

    # Dynamische Werte
    fatigue_level: int = 0  # Müdigkeitslevel (0-100)
    happiness_level: int = 50  # Glückslevel (0-100)
    last_interaction: str = ""  # Letzte Interaktion


class CompanionSystem:
    """👥 Hauptsystem für Begleiter-Management"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.companions: Dict[str, Companion] = {}
        self.active_companion: Optional[str] = None
        self.companion_history = []

        # Initialisiere Companion-Templates
        self.companion_templates = self._initialize_companion_templates()

        # Erstelle Companions aus verfügbaren Charakteren
        self._initialize_companions()

    def _initialize_companion_templates(self) -> Dict[str, Dict]:
        """Initialisiert Companion-Templates für verschiedene Charaktere"""
        return {
            "tsunade": {
                "suggested_locations": ["hospital", "dorf_zentrum", "training_area", "wald"],
                "travel_preferences": ["medical_areas", "safe_locations"],
                "rejection_reasons": ["Ich habe Hokage-Pflichten", "Es ist zu gefährlich für dich"],
                "base_mood": CompanionMood.WILLING,
                "travel_comments": [
                    "Komm, lass uns zusammen gehen. Ich passe auf dich auf.",
                    "Es wird gut sein, etwas frische Luft zu schnappen.",
                    "Bleib nah bei mir, mein kleiner Wolf."
                ],
                "rejection_comments": [
                    "Tut mir leid, Sukuna. Ich habe wichtige Hokage-Geschäfte zu erledigen.",
                    "Das ist zu gefährlich. Du gehst da nicht allein hin.",
                    "Heute nicht, Liebling. Mama hat zu viel Arbeit."
                ]
            },

            "naruto": {
                "suggested_locations": ["ramen_shop", "training_area", "dorf_zentrum"],
                "travel_preferences": ["food_places", "training_areas", "fun_locations"],
                "rejection_reasons": ["Training mit Kakashi-sensei", "Mission", "Bin zu müde"],
                "base_mood": CompanionMood.EXCITED,
                "travel_comments": [
                    "Ja! Lass uns zusammen gehen, dattebayo!",
                    "Das wird bestimmt cool! Komm schon!",
                    "Endlich mal was anderes als Training!"
                ],
                "rejection_comments": [
                    "Sorry, ich hab Training mit Kakashi-sensei, dattebayo!",
                    "Heute geht nicht, aber morgen bestimmt!",
                    "Ich bin total kaputt vom Training..."
                ]
            },

            "sasuke": {
                "suggested_locations": ["training_area", "uchiha_district", "forest"],
                "travel_preferences": ["quiet_places", "training_areas"],
                "rejection_reasons": ["Training", "Will allein sein", "Zu langweilig"],
                "base_mood": CompanionMood.NEUTRAL,
                "travel_comments": [
                    "Wenn es hilft, stärker zu werden... gut.",
                    "Komm mit. Aber halt mich nicht auf.",
                    "Solange es nicht langweilig wird."
                ],
                "rejection_comments": [
                    "Ich trainiere. Allein.",
                    "Geh ohne mich. Ich habe zu tun.",
                    "Das klingt... langweilig."
                ]
            },

            "sakura": {
                "suggested_locations": ["hospital", "flower_shop", "library"],
                "travel_preferences": ["peaceful_places", "learning_areas"],
                "rejection_reasons": ["Medizin-Studium", "Hilfe im Hospital", "Training"],
                "base_mood": CompanionMood.WILLING,
                "travel_comments": [
                    "Gerne! Ich zeige dir interessante Orte.",
                    "Das klingt entspannend nach dem ganzen Lernen.",
                    "Lass uns gehen! Ich kenne den Weg."
                ],
                "rejection_comments": [
                    "Sorry, ich muss für mein Medizin-Studium lernen.",
                    "Tsunade-sama braucht mich im Hospital.",
                    "Heute geht nicht, ich hab Training."
                ]
            },

            "kakashi": {
                "suggested_locations": ["memorial", "library", "training_area"],
                "travel_preferences": ["quiet_places", "memorial_sites"],
                "rejection_reasons": ["Mission", "Liest Icha Icha", "Training mit Team"],
                "base_mood": CompanionMood.NEUTRAL,
                "travel_comments": [
                    "Sicher. Ein Spaziergang tut gut.",
                    "Warum nicht? Ich habe Zeit.",
                    "Komm mit. Aber langsam."
                ],
                "rejection_comments": [
                    "Sorry, ich habe eine Mission.",
                    "Gerade am spannendsten Teil meines Buches...",
                    "Team 7 wartet auf mich."
                ]
            },

            "kiba": {
                "suggested_locations": ["forest", "training_area", "inuzuka_compound"],
                "travel_preferences": ["outdoor_areas", "wild_places"],
                "rejection_reasons": ["Training mit Akamaru", "Clan-Pflichten"],
                "base_mood": CompanionMood.EXCITED,
                "travel_comments": [
                    "Yeah! Akamaru und ich kommen mit!",
                    "Endlich mal raus! Das wird wild!",
                    "Pack-Leader, wir folgen dir!"
                ],
                "rejection_comments": [
                    "Akamaru ist krank, sorry!",
                    "Mutter hat Clan-Training angesetzt...",
                    "Heute nicht, wir sind müde vom Laufen."
                ]
            },

            "hinata": {
                "suggested_locations": ["garden", "library", "quiet_places"],
                "travel_preferences": ["peaceful_places", "beautiful_locations"],
                "rejection_reasons": ["Clan-Training", "Zu schüchtern", "Vater verbietet es"],
                "base_mood": CompanionMood.HESITANT,
                "travel_comments": [
                    "W-wenn du möchtest... ich komme mit.",
                    "Das klingt... schön. Gerne.",
                    "I-ich zeige dir ruhige Orte..."
                ],
                "rejection_comments": [
                    "T-tut mir leid... Vater verbietet es.",
                    "Ich... ich bin zu nervös...",
                    "Clan-Training wartet auf mich..."
                ]
            }
        }

    def _initialize_companions(self):
        """Erstellt Companion-Objekte aus verfügbaren Charakteren"""

        # Hole verfügbare Charaktere aus Relationship System
        characters = []
        if hasattr(self.game_data, 'relationship_system'):
            try:
                relationships = self.game_data.relationship_system.get_all_relationships()
                characters = list(relationships.keys())
            except:
                pass

        # Fallback characters
        if not characters:
            characters = ["tsunade", "naruto", "sasuke", "sakura", "kakashi", "kiba", "hinata"]

        for character in characters:
            if character in self.companion_templates:
                template = self.companion_templates[character]

                # Hole Relationship Level
                rel_level = 0
                if hasattr(self.game_data, 'relationship_system'):
                    try:
                        rel_info = self.game_data.relationship_system.get_relationship_info(character)
                        rel_level = rel_info.get('level', 0)
                    except:
                        pass

                # Erstelle Companion
                companion = Companion(
                    character_name=character,
                    status=CompanionStatus.AVAILABLE,
                    mood=template['base_mood'],
                    current_location=getattr(self.game_data, 'current_location', 'konoha'),
                    relationship_level=rel_level,
                    suggested_locations=template['suggested_locations'].copy(),
                    travel_preferences=template['travel_preferences'].copy(),
                    rejection_reasons=template['rejection_reasons'].copy()
                )

                self.companions[character] = companion

        print(f"✅ Companion System initialisiert mit {len(self.companions)} möglichen Begleitern")

    def suggest_companion_travel(self, current_location: str, suggested_location: str) -> Optional[str]:
        """🎯 NPCs schlagen vor, mitzukommen"""

        # Finde NPCs die am aktuellen Ort sind
        available_npcs = self._get_available_companions_at_location(current_location)

        if not available_npcs:
            return None

        # Wähle NPC basierend auf Vorlieben für das Ziel
        suggesting_npc = None
        for npc in available_npcs:
            companion = self.companions[npc]

            # Prüfe ob NPC diesen Ort vorschlagen würde
            if (suggested_location in companion.suggested_locations or
                    any(pref in suggested_location for pref in companion.travel_preferences)):

                # Beziehungslevel-Check
                if companion.relationship_level > 25:  # Nur bei guter Beziehung
                    suggesting_npc = npc
                    break

        if suggesting_npc:
            return self._generate_travel_suggestion(suggesting_npc, suggested_location)

        return None

    def _get_available_companions_at_location(self, location: str) -> List[str]:
        """Findet verfügbare Companions am gegebenen Ort"""
        available = []

        for char_name, companion in self.companions.items():
            if (companion.status == CompanionStatus.AVAILABLE and
                    companion.current_location == location and
                    companion.mood != CompanionMood.UNWILLING):
                available.append(char_name)

        return available

    def _generate_travel_suggestion(self, npc: str, location: str) -> str:
        """Generiert Vorschlag-Text vom NPC"""
        companion = self.companions[npc]
        template = self.companion_templates.get(npc, {})

        travel_comments = template.get('travel_comments', [f"Lass uns zusammen zu {location} gehen!"])
        comment = random.choice(travel_comments)

        return f"*{npc.title()} schaut auf* '{comment}'\n\n" \
               f"💭 {npc.title()} möchte dich zu {location} begleiten!\n" \
               f"**Antworten**: '/accept {npc}' oder '/decline {npc}'"

    def accept_companion(self, character: str) -> str:
        """✅ Akzeptiert einen Begleiter"""
        if character not in self.companions:
            return f"❌ {character} ist nicht verfügbar als Begleiter."

        companion = self.companions[character]

        # Prüfe ob bereits ein Begleiter aktiv
        if self.active_companion:
            return f"❌ {self.active_companion.title()} begleitet dich bereits. Verwende '/dismiss {self.active_companion}' zuerst."

        # Aktiviere Begleiter
        companion.status = CompanionStatus.FOLLOWING
        companion.happiness_level = min(100, companion.happiness_level + 20)
        self.active_companion = character

        # Aktualisiere Relationship
        if hasattr(self.game_data, 'relationship_system'):
            try:
                self.game_data.relationship_system.change_relationship(
                    character, +5, "Reise-Begleitung akzeptiert", show_message=False
                )
            except:
                pass

        return f"✅ {character.title()} begleitet dich jetzt auf deinen Reisen!\n" \
               f"💫 +5 Beziehungspunkte mit {character.title()}"

    def decline_companion(self, character: str) -> str:
        """❌ Lehnt einen Begleiter ab"""
        if character not in self.companions:
            return f"❌ {character} ist nicht verfügbar."

        companion = self.companions[character]
        companion.status = CompanionStatus.REJECTED
        companion.mood = CompanionMood.HESITANT
        companion.happiness_level = max(0, companion.happiness_level - 10)

        # Kleine Relationship-Penalty
        if hasattr(self.game_data, 'relationship_system'):
            try:
                self.game_data.relationship_system.change_relationship(
                    character, -2, "Reise-Begleitung abgelehnt", show_message=False
                )
            except:
                pass

        return f"💔 {character.title()} ist enttäuscht, dass du allein gehen möchtest.\n" \
               f"📉 -2 Beziehungspunkte mit {character.title()}"

    def dismiss_companion(self) -> str:
        """👋 Entlässt aktuellen Begleiter"""
        if not self.active_companion:
            return "❌ Du hast keinen aktiven Begleiter."

        character = self.active_companion
        companion = self.companions[character]

        # Reset Status
        companion.status = CompanionStatus.AVAILABLE
        companion.mood = CompanionMood.NEUTRAL
        self.active_companion = None

        return f"👋 {character.title()} kehrt zu eigenen Aktivitäten zurück."

    def travel_with_companion(self, new_location: str) -> str:
        """🚶‍♂️ Reist mit Begleiter zu neuem Ort"""
        if not self.active_companion:
            return ""  # Kein Begleiter, normale Reise

        character = self.active_companion
        companion = self.companions[character]

        # Update Location für beide
        companion.current_location = new_location
        self.game_data.current_location = new_location

        # Generiere Reise-Kommentar
        travel_response = self._generate_travel_response(character, new_location)

        # Update Fatigue und Happiness
        companion.fatigue_level = min(100, companion.fatigue_level + 10)

        # Beziehungs-Bonus für gemeinsame Zeit
        if random.random() < 0.3:  # 30% Chance
            if hasattr(self.game_data, 'relationship_system'):
                try:
                    self.game_data.relationship_system.change_relationship(
                        character, +1, "Gemeinsame Reisezeit", show_message=False
                    )
                except:
                    pass

        return travel_response

    def _generate_travel_response(self, character: str, location: str) -> str:
        """Generiert Reise-Kommentare vom Begleiter"""
        companion = self.companions[character]

        # Character-spezifische Reise-Kommentare
        travel_responses = {
            "tsunade": [
                f"*Tsunade hält deine Hand fest* 'Bleib nah bei mir in {location}.'",
                f"*schaut sich um* 'Interessant hier in {location}. Lass uns vorsichtig sein.'",
                f"*beschützend* 'Wenn etwas passiert, kommst du sofort zu mir, verstanden?'"
            ],
            "naruto": [
                f"*springt aufgeregt herum* 'Wow! {location} ist so cool, dattebayo!'",
                f"*grinst breit* 'Das war eine super Idee, hierher zu gehen!'",
                f"*schaut sich neugierig um* 'Was machen wir als nächstes hier?'"
            ],
            "sasuke": [
                f"*schweigt und beobachtet {location} aufmerksam*",
                f"*nickt* '{location}... akzeptabel.'",
                f"*kühler Blick* 'Lass uns das schnell erledigen.'"
            ],
            "sakura": [
                f"*lächelt* '{location} ist wirklich schön!'",
                f"*interessiert* 'Erzähl mir von diesem Ort.'",
                f"*hilfsbereit* 'Falls du etwas brauchst, sag Bescheid!'"
            ],
            "kiba": [
                f"*schnüffelt in der Luft* 'Riecht interessant hier!'",
                f"*Akamaru bellt zustimmend* 'Er mag {location} auch!'",
                f"*aufgeregt* 'Lass uns hier rumrennen!'"
            ],
            "hinata": [
                f"*schüchtern* 'E-es ist schön hier...'",
                f"*leise* 'Danke dass ich mitkommen durfte...'",
                f"*bewundert die Umgebung* 'So friedlich...'"
            ]
        }

        responses = travel_responses.get(character, [f"*{character} folgt dir nach {location}*"])
        response = random.choice(responses)

        return f"\n👥 **BEGLEITER**: {response}"

    def get_companion_status(self) -> str:
        """📊 Zeigt Companion-Status"""
        if not self.active_companion:
            return "👤 **BEGLEITER**: Niemand\n" \
                   "💡 Verwende '/suggest' für Begleiter-Vorschläge!"

        character = self.active_companion
        companion = self.companions[character]

        mood_emoji = {
            CompanionMood.EXCITED: "🤩",
            CompanionMood.WILLING: "😊",
            CompanionMood.NEUTRAL: "😐",
            CompanionMood.HESITANT: "😬",
            CompanionMood.UNWILLING: "😠"
        }

        return f"👥 **AKTIVER BEGLEITER**: {character.title()}\n" \
               f"😊 **Stimmung**: {mood_emoji.get(companion.mood, '😐')} {companion.mood.value}\n" \
               f"❤️ **Beziehung**: {companion.relationship_level}\n" \
               f"😴 **Müdigkeit**: {companion.fatigue_level}/100\n" \
               f"📍 **Ort**: {companion.current_location}\n\n" \
               f"💡 Verwende '/dismiss' um {character.title()} zu entlassen"

    def get_available_companions(self) -> List[str]:
        """Gibt verfügbare Companions zurück"""
        current_location = getattr(self.game_data, 'current_location', 'konoha')
        return self._get_available_companions_at_location(current_location)

    def request_companion(self, character: str) -> str:
        """🙋‍♂️ Fragt einen Charakter, ob er mitkommen möchte"""
        if character not in self.companions:
            return f"❌ {character} ist nicht als Begleiter verfügbar."

        companion = self.companions[character]

        # Prüfe ob bereits ein Begleiter aktiv
        if self.active_companion:
            return f"❌ {self.active_companion.title()} begleitet dich bereits."

        # Prüfe Verfügbarkeit basierend auf Relationship und Mood
        success_chance = self._calculate_companion_chance(companion)

        if random.random() < success_chance:
            # Akzeptiert
            return self._generate_companion_acceptance(character)
        else:
            # Lehnt ab
            return self._generate_companion_rejection(character)

    def _calculate_companion_chance(self, companion: Companion) -> float:
        """Berechnet Wahrscheinlichkeit dass Companion mitkommt"""
        base_chance = 0.5

        # Relationship Bonus
        rel_bonus = (companion.relationship_level - 50) / 100  # -0.5 to +1.5

        # Mood Modifier
        mood_modifiers = {
            CompanionMood.EXCITED: 0.3,
            CompanionMood.WILLING: 0.1,
            CompanionMood.NEUTRAL: 0.0,
            CompanionMood.HESITANT: -0.2,
            CompanionMood.UNWILLING: -0.4
        }

        mood_bonus = mood_modifiers.get(companion.mood, 0)

        # Fatigue Penalty
        fatigue_penalty = companion.fatigue_level / 200  # 0 to 0.5

        total_chance = base_chance + rel_bonus + mood_bonus - fatigue_penalty
        return max(0.1, min(0.9, total_chance))  # 10% to 90%

    def _generate_companion_acceptance(self, character: str) -> str:
        """Generiert Akzeptanz-Text"""
        template = self.companion_templates.get(character, {})
        comments = template.get('travel_comments', [f"Gerne! Lass uns gehen."])
        comment = random.choice(comments)

        # Aktiviere sofort
        self.accept_companion(character)

        return f"✅ *{character.title()}*: '{comment}'\n\n" \
               f"👥 {character.title()} begleitet dich jetzt!"

    def _generate_companion_rejection(self, character: str) -> str:
        """Generiert Ablehnungs-Text"""
        template = self.companion_templates.get(character, {})
        comments = template.get('rejection_comments', ["Tut mir leid, heute nicht."])
        comment = random.choice(comments)

        companion = self.companions[character]
        companion.status = CompanionStatus.REJECTED

        return f"❌ *{character.title()}*: '{comment}'\n\n" \
               f"💔 {character.title()} kann heute nicht mitkommen."


def integrate_companion_system(game_data):
    """🔧 Integriert das Companion System in die Hauptanwendung"""

    # Erstelle Companion System
    companion_system = CompanionSystem(game_data)
    game_data.companion_system = companion_system

    # Erweitere Encounter System falls verfügbar
    if hasattr(game_data, 'encounter_system'):
        original_check_encounter = game_data.encounter_system.check_for_encounter

        def enhanced_encounter_with_companion(location_name: str):
            """Erweiterte Encounter-Funktion mit Companion-Support"""

            # Normale Encounter-Logik
            encounter_result = original_check_encounter(location_name)

            # Companion Travel Response
            travel_response = ""
            if hasattr(game_data, 'companion_system') and game_data.companion_system.active_companion:
                travel_response = game_data.companion_system.travel_with_companion(location_name)

            # Kombiniere Responses
            if encounter_result and travel_response:
                # Beide vorhanden
                encounter_result["additional_text"] = travel_response
            elif travel_response and not encounter_result:
                # Nur Companion Response
                encounter_result = {
                    "character": "companion_travel",
                    "additional_text": travel_response
                }

            return encounter_result

        game_data.encounter_system.check_for_encounter = enhanced_encounter_with_companion

    print("👥 COMPANION SYSTEM erfolgreich integriert!")
    print("🎯 Features aktiviert:")
    print("   • NPCs können Reisen vorschlagen")
    print("   • Begleiter-Anfragen und Akzeptanz")
    print("   • Dynamische Reise-Kommentare")
    print("   • Beziehungs-Integration")
    print("   • Companion Status-Tracking")

    return companion_system


if __name__ == "__main__":
    print("👥 COMPANION SYSTEM")
    print("=======================================")
    print("✅ NPCs als Reisebegleiter")
    print("✅ Dynamische Vorschläge")
    print("✅ Akzeptanz/Ablehnung System")
    print("✅ Reise-Kommentare")
    print("✅ Beziehungs-Integration")