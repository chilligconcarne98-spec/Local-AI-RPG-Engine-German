# -*- coding: utf-8 -*-
"""
🧭 AI LOCATION SUGGESTION DETECTION & VALIDATION
Detects when characters suggest traveling to locations in AI responses
and validates if the location exists in encounter system
"""

import re
from typing import Optional, Tuple, List


class AILocationSuggestionDetector:
    """Detects and validates location suggestions from AI responses"""

    def __init__(self, encounter_system, companion_system=None):
        self.encounter_system = encounter_system
        self.companion_system = companion_system

        # German location suggestion patterns
        self.suggestion_patterns = [
            # "Lass uns zum/zur/ins/in die [LOCATION] gehen"
            r"lass uns (?:zum?|zur|ins?|in die) ([a-zA-ZäöüÄÖÜß\s]+) gehen",
            # "Wir könnten zum/zur/ins/in die [LOCATION] gehen"
            r"wir könnten (?:zum?|zur|ins?|in die) ([a-zA-ZäöüÄÖÜß\s]+) gehen",
            # "Ich schlage vor, zum/zur/ins/in die [LOCATION] zu gehen"
            r"ich schlage vor,? (?:zum?|zur|ins?|in die) ([a-zA-ZäöüÄÖÜß\s]+) zu gehen",
            # "Sollen wir zum/zur/ins/in die [LOCATION] gehen"
            r"sollen wir (?:zum?|zur|ins?|in die) ([a-zA-ZäöüÄÖÜß\s]+) gehen",
            # "Möchtest du zum/zur/ins/in die [LOCATION] gehen"
            r"möchtest du (?:zum?|zur|ins?|in die) ([a-zA-ZäöüÄÖÜß\s]+) gehen",
            # "Komm mit zum/zur/ins/in die [LOCATION]"
            r"komm mit (?:zum?|zur|ins?|in die) ([a-zA-ZäöüÄÖÜß\s]+)",
        ]

    def detect_location_suggestion(self, ai_response: str, character_name: str) -> Optional[Tuple[str, str]]:
        """
        Detects location suggestions in AI responses
        Returns: (character_name, suggested_location) or None
        """

        response_lower = ai_response.lower()

        for pattern in self.suggestion_patterns:
            matches = re.findall(pattern, response_lower, re.IGNORECASE)

            for match in matches:
                suggested_location = match.strip()

                # Clean up location name
                cleaned_location = self._clean_location_name(suggested_location)

                # Validate location exists
                if self._validate_location_exists(cleaned_location):
                    print(f"🧭 DETECTED: {character_name} suggests traveling to {cleaned_location}")
                    return character_name, cleaned_location

        return None

    def _clean_location_name(self, location: str) -> str:
        """Cleans and normalizes location names"""

        # Remove common German articles and prepositions
        location = re.sub(r'\b(der|die|das|dem|den|ein|eine|einem)\b', '', location, flags=re.IGNORECASE)

        # Remove trailing words that aren't part of location
        location = re.sub(r'\b(dort|hin|hinein|rein|mal|doch|auch)\b.*', '', location, flags=re.IGNORECASE)

        # Clean whitespace
        location = re.sub(r'\s+', ' ', location).strip()

        # Common location mappings
        location_mappings = {
            "training ground": "training_area",
            "trainingsplatz": "training_area",
            "dorf zentrum": "dorf_zentrum",
            "dorfzentrum": "dorf_zentrum",
            "zentrum": "dorf_zentrum",
            "dorf": "dorf_zentrum",
            "marktplatz": "dorf_zentrum",
            "bibliothek": "konoha_hauptbibliothek",
            "tsunades bibliothek": "tsunades_bibliothek",
            "tsunades haus": "tsunades_haus",
            "nach hause": "tsunades_haus",
            "hokage turm": "hokage_turm",
            "hokage büro": "hokage_turm",
            "ramen stand": "ramen_stand",
            "ichiraku": "ramen_stand",
            "ichiraku ramen": "ramen_stand",
            "hospital": "hospital",
            "krankenhaus": "hospital",
            "gedenkstein": "memorial_stone",
            "heldendenkmal": "memorial_stone"
        }

        return location_mappings.get(location.lower(), location.lower().replace(' ', '_'))

    def _validate_location_exists(self, location: str) -> bool:
        """Validates if location exists in encounter system"""

        if not self.encounter_system:
            return False

        # Check if location exists in encounter system
        if hasattr(self.encounter_system, 'locations'):
            return location in self.encounter_system.locations

        # Alternative check if encounter system has different structure
        if hasattr(self.encounter_system, 'available_locations'):
            return location in self.encounter_system.available_locations

        # Try to see if we can encounter to this location (test)
        try:
            # This is a simple test - some encounter systems might have this method
            if hasattr(self.encounter_system, 'is_valid_location'):
                return self.encounter_system.is_valid_location(location)
        except:
            pass

        return False

    def generate_travel_prompt(self, character_name: str, location: str) -> str:
        """Generates travel suggestion prompt for user"""

        location_display = location.replace('_', ' ').title()

        return f"""🧭 **REISE-VORSCHLAG**

💭 {character_name.title()} möchte mit dir {self._get_location_preposition(location)} {location_display} gehen!

**Möchtest du das?**
• `/ja` - Akzeptiere den Vorschlag
• `/nein` - Lehne höflich ab

💡 *Falls du zustimmst, werdet ihr gemeinsam dorthin reisen.*"""

    def _get_location_preposition(self, location: str) -> str:
        """Returns appropriate German preposition for location"""

        preposition_mappings = {
            "training_ground": "zum",
            "dorf_zentrum": "ins",
            "konoha_hauptbibliothek": "zur",
            "tsunades_bibliothek": "zu",
            "tsunades_haus": "nach",
            "hokage_tower": "zum",
            "teuchi_ramen": "zu",
            "konoha_hospital": "ins"
        }

        return preposition_mappings.get(location, "zum")


def integrate_ai_location_detection(game_data):
    """Integrates AI location detection into game system"""

    try:
        # Initialize detector
        detector = AILocationSuggestionDetector(
            encounter_system=getattr(game_data, 'encounter_system', None),
            companion_system=getattr(game_data, 'companion_system', None)
        )

        # Store detector in game data
        game_data.location_detector = detector

        print("🧭 AI Location Detection System integrated!")
        return True

    except Exception as e:
        print(f"⚠️ AI Location Detection integration error: {e}")
        return False


def check_ai_response_for_travel_suggestion(game_data, ai_response: str, character_name: str) -> Optional[str]:
    """
    Checks AI response for travel suggestions and handles them
    Call this after getting AI response in get_llm_response
    """

    if not hasattr(game_data, 'location_detector'):
        return None

    try:
        suggestion = game_data.location_detector.detect_location_suggestion(ai_response, character_name)

        if suggestion:
            character, location = suggestion
            travel_prompt = game_data.location_detector.generate_travel_prompt(character, location)

            # Store pending travel suggestion
            if not hasattr(game_data, 'pending_travel'):
                game_data.pending_travel = {}

            game_data.pending_travel = {
                'character': character,
                'location': location,
                'active': True
            }

            return travel_prompt

    except Exception as e:
        print(f"⚠️ Travel suggestion check error: {e}")

    return None


def handle_travel_response(game_data, user_response: str) -> Optional[str]:
    """
    Handles user response to travel suggestions (/ja or /nein)
    Call this in command processing
    """

    if not hasattr(game_data, 'pending_travel') or not game_data.pending_travel.get('active'):
        return None

    try:
        if user_response.lower() in ['/ja', 'ja']:
            # Accept travel
            character = game_data.pending_travel['character']
            location = game_data.pending_travel['location']

            # Clear pending travel
            game_data.pending_travel = {'active': False}

            # ✅ ADD CHARACTER AS COMPANION FIRST!
            companion_result = ""
            if hasattr(game_data, 'companion_system') and game_data.companion_system:
                try:
                    # Add character as companion for the journey
                    if character in game_data.companion_system.companions:
                        # Check if already has active companion
                        if game_data.companion_system.active_companion:
                            # Temporarily dismiss current companion
                            old_companion = game_data.companion_system.active_companion
                            game_data.companion_system.dismiss_companion()
                            companion_result += f"👋 {old_companion.title()} wartet hier.\n"

                        # Accept new companion
                        accept_result = game_data.companion_system.accept_companion(character)
                        companion_result += f"{accept_result}\n"
                        print(f"🤝 {character} wurde als begleiter für reisen hinzugefügt!")
                    else:
                        companion_result += f"🤝 {character.title()} begleitet dich!\n"
                except Exception as e:
                    print(f"⚠️ Companion integration error: {e}")
                    companion_result += f"🤝 {character.title()} begleitet dich!\n"

                # Execute travel (use encounter system)
            if hasattr(game_data, 'encounter_system'):
                try:
                    # Start encounter at the location
                    result = game_data.encounter_system.start_encounter(location)
                    return f"✅ Du gehst mit {character.title()} {game_data.location_detector._get_location_preposition(location)} {location.replace('_', ' ').title()}!\n\n{companion_result}\n{result}"
                except:
                    pass

                # Fallback: just change location
            game_data.current_location = location
            return f"✅ Du gehst mit {character.title()} {game_data.location_detector._get_location_preposition(location)} {location.replace('_', ' ').title()}!\n\n{companion_result}"




            # Fallback: just change location


        elif user_response.lower() in ['/nein', 'nein']:
            # Decline travel
            character = game_data.pending_travel['character']
            game_data.pending_travel = {'active': False}

            return f"😔 Du lehnst {character.title()}'s Reise-Vorschlag höflich ab."

    except Exception as e:
        print(f"⚠️ Travel response handling error: {e}")

    return None