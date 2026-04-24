# -*- coding: utf-8 -*-
"""
💾 ENHANCED SAVE/LOAD SYSTEM - Support für alle neuen Features
Speichert und lädt: Secrets, Companions, Memories, Emotional Intelligence
"""

from datetime import datetime
import json
import os
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import asdict

# --- KONSTANTEN FÜR SPEICHERPFADE ---
SAVES_DIR = "saves"
AUTOSAVE_PATH = os.path.join(SAVES_DIR, "autosave.json")


# --- ENHANCED JSON ENCODER für komplexe Objekte ---
class EnhancedGameDataEncoder(json.JSONEncoder):
    """Erweiterte JSON Encoder für alle Game-Objekte"""

    def default(self, obj):
        if hasattr(obj, '__dict__'):
            # Für dataclass-Objekte
            try:
                return asdict(obj)
            except:
                return obj.__dict__
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, 'value'):
            # Für Enums
            return obj.value
        else:
            try:
                return super().default(obj)
            except:
                return str(obj)


def _prepare_save_data(game_data) -> Dict[str, Any]:
    """🔧 Bereitet alle Game-Daten für Speicherung vor"""

    save_data = {
        "timestamp": datetime.now().isoformat(),
        "version": "claude_ultra_1.0",
        "basic_data": {},
        "advanced_systems": {}
    }

    # === BASIC GAME DATA ===
    save_data["basic_data"] = {
        "chat_messages": getattr(game_data, 'chat_messages', []),
        "game_state": getattr(game_data, 'game_state', {}),
        "current_location": getattr(game_data, 'current_location', 'konoha'),
        "active_character": getattr(game_data, 'active_character', 'tsunade'),
        "encounter_active": getattr(game_data, 'encounter_active', False)
    }

    # === MATERNAL SYSTEM ===
    if hasattr(game_data, 'maternal_system') and game_data.maternal_system:
        try:
            maternal_data = {
                "level": game_data.maternal_system.get_current_level(),
                "category": game_data.maternal_system.get_level_category(),
                "history": getattr(game_data.maternal_system, 'level_history', []),
                "behavioral_data": getattr(game_data.maternal_system, 'behavioral_data', {})
            }
            save_data["advanced_systems"]["maternal_system"] = maternal_data
            print("✅ Maternal System Daten vorbereitet")
        except Exception as e:
            print(f"⚠️ Maternal System Save Fehler: {e}")

    # === RELATIONSHIP SYSTEM ===
    if hasattr(game_data, 'relationship_system') and game_data.relationship_system:
        try:
            relationships_data = {
                "relationships": game_data.relationship_system.get_all_relationships(),
                "relationship_history": getattr(game_data.relationship_system, 'relationship_history', []),
                "plot_status": getattr(game_data.relationship_system, 'plot_status', {})
            }
            save_data["advanced_systems"]["relationship_system"] = relationships_data
            print("✅ Relationship System Daten vorbereitet")
        except Exception as e:
            print(f"⚠️ Relationship System Save Fehler: {e}")

    # === 🔮 SECRET SYSTEM ===
    if hasattr(game_data, 'secret_system') and game_data.secret_system:
        try:
            secret_data = game_data.secret_system.secret_engine.save_secrets_data()
            save_data["advanced_systems"]["secret_system"] = secret_data
            print(f"✅ Secret System Daten vorbereitet ({len(secret_data.get('secrets', {}))} secrets)")
        except Exception as e:
            print(f"⚠️ Secret System Save Fehler: {e}")

    # === 👥 COMPANION SYSTEM ===
    if hasattr(game_data, 'companion_system') and game_data.companion_system:
        try:
            companion_data = {
                "companions": {},
                "active_companion": game_data.companion_system.active_companion,
                "companion_history": getattr(game_data.companion_system, 'companion_history', [])
            }

            # Konvertiere Companion-Objekte
            for char_name, companion in game_data.companion_system.companions.items():
                companion_data["companions"][char_name] = {
                    "character_name": companion.character_name,
                    "status": companion.status.value,
                    "mood": companion.mood.value,
                    "current_location": companion.current_location,
                    "relationship_level": companion.relationship_level,
                    "suggested_locations": companion.suggested_locations,
                    "travel_preferences": companion.travel_preferences,
                    "rejection_reasons": companion.rejection_reasons,
                    "fatigue_level": companion.fatigue_level,
                    "happiness_level": companion.happiness_level,
                    "last_interaction": companion.last_interaction
                }

            save_data["advanced_systems"]["companion_system"] = companion_data
            print(f"✅ Companion System Daten vorbereitet ({len(companion_data['companions'])} companions)")
        except Exception as e:
            print(f"⚠️ Companion System Save Fehler: {e}")

    # === 🧠 ADVANCED MEMORY SYSTEM ===
    if hasattr(game_data, 'advanced_memory_system') and game_data.advanced_memory_system:
        try:
            memory_data = game_data.advanced_memory_system.save_memory_data()
            save_data["advanced_systems"]["advanced_memory_system"] = memory_data

            # Count memories
            total_memories = sum(len(memories) for memories in memory_data.get("character_memories", {}).values())
            print(f"✅ Advanced Memory System Daten vorbereitet ({total_memories} memories)")
        except Exception as e:
            print(f"⚠️ Advanced Memory System Save Fehler: {e}")

    # === 💭 EMOTIONAL INTELLIGENCE ENGINE ===
    if hasattr(game_data, 'emotional_intelligence') and game_data.emotional_intelligence:
        try:
            emotional_data = {
                "character_profiles": {},
                "emotional_context_history": getattr(game_data.emotional_intelligence, 'emotional_context_history', [])
            }

            # Konvertiere Emotional Profiles
            for char_name, profile in game_data.emotional_intelligence.character_profiles.items():
                profile_data = {
                    "character_name": profile.character_name,
                    "primary_emotion": profile.primary_emotion.value,
                    "secondary_emotions": [e.value for e in profile.secondary_emotions],
                    "emotional_stability": profile.emotional_stability,
                    "emotional_intensity": profile.emotional_intensity,
                    "sukuna_emotional_bond": profile.sukuna_emotional_bond,
                    "protective_instinct": profile.protective_instinct,
                    "empathy_level": profile.empathy_level,
                    "emotional_openness": profile.emotional_openness,
                    "emotional_triggers": {k: v.value for k, v in profile.emotional_triggers.items()},
                    "comfort_strategies": profile.comfort_strategies,
                    "stress_responses": profile.stress_responses,
                    "mood_history": [(dt.isoformat(), mood.value) for dt, mood in profile.mood_history],
                    "learned_responses": profile.learned_responses
                }
                emotional_data["character_profiles"][char_name] = profile_data

            save_data["advanced_systems"]["emotional_intelligence"] = emotional_data
            print(f"✅ Emotional Intelligence Daten vorbereitet ({len(emotional_data['character_profiles'])} profiles)")
        except Exception as e:
            print(f"⚠️ Emotional Intelligence Save Fehler: {e}")

    # === ENVIRONMENT SYSTEM ===
    if hasattr(game_data, 'environment_system') and game_data.environment_system:
        try:
            env_data = {
                "current_environment": getattr(game_data.environment_system, 'current_environment', {}),
                "environment_history": getattr(game_data.environment_system, 'environment_history', [])
            }
            save_data["advanced_systems"]["environment_system"] = env_data
            print("✅ Environment System Daten vorbereitet")
        except Exception as e:
            print(f"⚠️ Environment System Save Fehler: {e}")

    # === ENCOUNTER SYSTEM ===
    if hasattr(game_data, 'encounter_system') and game_data.encounter_system:
        try:
            encounter_data = {
                "last_encounters": getattr(game_data.encounter_system, 'last_encounters', {}),
                "encounter_cooldowns": getattr(game_data.encounter_system, 'encounter_cooldowns', {}),
                "encounter_history": getattr(game_data.encounter_system, 'encounter_history', [])
            }
            save_data["advanced_systems"]["encounter_system"] = encounter_data
            print("✅ Encounter System Daten vorbereitet")
        except Exception as e:
            print(f"⚠️ Encounter System Save Fehler: {e}")

    return save_data


def _restore_save_data(save_data: Dict[str, Any], game_data) -> bool:
    """🔧 Stellt alle Game-Daten aus Speicher wieder her"""

    try:
        version = save_data.get("version", "unknown")
        print(f"💾 Lade Spielstand Version: {version}")

        # === BASIC GAME DATA ===
        basic_data = save_data.get("basic_data", {})

        if hasattr(game_data, 'chat_messages'):
            game_data.chat_messages = basic_data.get("chat_messages", [])

        if hasattr(game_data, 'game_state'):
            game_data.game_state.update(basic_data.get("game_state", {}))

        game_data.current_location = basic_data.get("current_location", "konoha")
        game_data.active_character = basic_data.get("active_character", "tsunade")
        game_data.encounter_active = basic_data.get("encounter_active", False)

        # === ADVANCED SYSTEMS ===
        advanced_systems = save_data.get("advanced_systems", {})

        # === MATERNAL SYSTEM ===
        if "maternal_system" in advanced_systems and hasattr(game_data, 'maternal_system'):
            maternal_data = advanced_systems["maternal_system"]
            try:
                if hasattr(game_data.maternal_system, 'set_level'):
                    game_data.maternal_system.set_level(maternal_data.get("level", 0))
                else:
                    game_data.maternal_system.level = maternal_data.get("level", 0)

                if hasattr(game_data.maternal_system, 'level_history'):
                    game_data.maternal_system.level_history = maternal_data.get("history", [])

                print("✅ Maternal System wiederhergestellt")
            except Exception as e:
                print(f"⚠️ Maternal System Load Fehler: {e}")

        # === RELATIONSHIP SYSTEM ===
        if "relationship_system" in advanced_systems and hasattr(game_data, 'relationship_system'):
            rel_data = advanced_systems["relationship_system"]
            try:
                # Lade Relationships
                relationships = rel_data.get("relationships", {})
                game_data.relationship_system.relationships = relationships

                # Lade History
                if hasattr(game_data.relationship_system, 'relationship_history'):
                    game_data.relationship_system.relationship_history = rel_data.get("relationship_history", [])

                # Lade Plot Status
                if hasattr(game_data.relationship_system, 'plot_status'):
                    game_data.relationship_system.plot_status = rel_data.get("plot_status", {})

                print(f"✅ Relationship System wiederhergestellt ({len(relationships)} characters)")
            except Exception as e:
                print(f"⚠️ Relationship System Load Fehler: {e}")

        # === 🔮 SECRET SYSTEM ===
        if "secret_system" in advanced_systems and hasattr(game_data, 'secret_system'):
            secret_data = advanced_systems["secret_system"]
            try:
                game_data.secret_system.secret_engine.load_secrets_data(secret_data)
                secrets_count = len(secret_data.get("secrets", {}))
                print(f"✅ Secret System wiederhergestellt ({secrets_count} secrets)")
            except Exception as e:
                print(f"⚠️ Secret System Load Fehler: {e}")

        # === 👥 COMPANION SYSTEM ===
        if "companion_system" in advanced_systems and hasattr(game_data, 'companion_system'):
            companion_data = advanced_systems["companion_system"]
            try:
                # Import Enums
                from moduls.companion_system import CompanionStatus, CompanionMood, Companion

                # Lade Companions
                companions = {}
                for char_name, comp_data in companion_data.get("companions", {}).items():
                    companion = Companion(
                        character_name=comp_data["character_name"],
                        status=CompanionStatus(comp_data["status"]),
                        mood=CompanionMood(comp_data["mood"]),
                        current_location=comp_data["current_location"],
                        relationship_level=comp_data["relationship_level"],
                        suggested_locations=comp_data["suggested_locations"],
                        travel_preferences=comp_data["travel_preferences"],
                        rejection_reasons=comp_data["rejection_reasons"],
                        fatigue_level=comp_data.get("fatigue_level", 0),
                        happiness_level=comp_data.get("happiness_level", 50),
                        last_interaction=comp_data.get("last_interaction", "")
                    )
                    companions[char_name] = companion

                game_data.companion_system.companions = companions
                game_data.companion_system.active_companion = companion_data.get("active_companion")
                game_data.companion_system.companion_history = companion_data.get("companion_history", [])

                print(f"✅ Companion System wiederhergestellt ({len(companions)} companions)")
            except Exception as e:
                print(f"⚠️ Companion System Load Fehler: {e}")

        # === 🧠 ADVANCED MEMORY SYSTEM ===
        if "advanced_memory_system" in advanced_systems and hasattr(game_data, 'advanced_memory_system'):
            memory_data = advanced_systems["advanced_memory_system"]
            try:
                game_data.advanced_memory_system.load_memory_data(memory_data)
                total_memories = sum(len(memories) for memories in memory_data.get("character_memories", {}).values())
                print(f"✅ Advanced Memory System wiederhergestellt ({total_memories} memories)")
            except Exception as e:
                print(f"⚠️ Advanced Memory System Load Fehler: {e}")

        # === 💭 EMOTIONAL INTELLIGENCE ENGINE ===
        if "emotional_intelligence" in advanced_systems and hasattr(game_data, 'emotional_intelligence'):
            emotional_data = advanced_systems["emotional_intelligence"]
            try:
                # Import Enums und Classes
                from moduls.emotional_intelligence_engine import EmotionalState, EmotionalProfile

                # Lade Emotional Profiles
                profiles = {}
                for char_name, profile_data in emotional_data.get("character_profiles", {}).items():
                    # Konvertiere mood_history zurück
                    mood_history = []
                    for dt_str, mood_str in profile_data.get("mood_history", []):
                        mood_history.append((datetime.fromisoformat(dt_str), EmotionalState(mood_str)))

                    # Konvertiere Triggers zurück
                    triggers = {}
                    for trigger, emotion_str in profile_data.get("emotional_triggers", {}).items():
                        triggers[trigger] = EmotionalState(emotion_str)

                    profile = EmotionalProfile(
                        character_name=profile_data["character_name"],
                        primary_emotion=EmotionalState(profile_data["primary_emotion"]),
                        secondary_emotions=[EmotionalState(e) for e in profile_data.get("secondary_emotions", [])],
                        emotional_stability=profile_data["emotional_stability"],
                        emotional_intensity=profile_data["emotional_intensity"],
                        emotional_triggers=triggers,
                        emotional_expressions={},  # Wird neu initialisiert
                        comfort_strategies=profile_data["comfort_strategies"],
                        stress_responses=profile_data["stress_responses"],
                        sukuna_emotional_bond=profile_data["sukuna_emotional_bond"],
                        protective_instinct=profile_data["protective_instinct"],
                        empathy_level=profile_data["empathy_level"],
                        emotional_openness=profile_data["emotional_openness"],
                        mood_history=mood_history,
                        learned_responses=profile_data.get("learned_responses", {})
                    )
                    profiles[char_name] = profile

                game_data.emotional_intelligence.character_profiles = profiles
                game_data.emotional_intelligence.emotional_context_history = emotional_data.get(
                    "emotional_context_history", [])

                print(f"✅ Emotional Intelligence wiederhergestellt ({len(profiles)} profiles)")
            except Exception as e:
                print(f"⚠️ Emotional Intelligence Load Fehler: {e}")

        # === ENVIRONMENT SYSTEM ===
        if "environment_system" in advanced_systems and hasattr(game_data, 'environment_system'):
            env_data = advanced_systems["environment_system"]
            try:
                if hasattr(game_data.environment_system, 'current_environment'):
                    game_data.environment_system.current_environment = env_data.get("current_environment", {})
                if hasattr(game_data.environment_system, 'environment_history'):
                    game_data.environment_system.environment_history = env_data.get("environment_history", [])
                print("✅ Environment System wiederhergestellt")
            except Exception as e:
                print(f"⚠️ Environment System Load Fehler: {e}")

        # === ENCOUNTER SYSTEM ===
        if "encounter_system" in advanced_systems and hasattr(game_data, 'encounter_system'):
            encounter_data = advanced_systems["encounter_system"]
            try:
                if hasattr(game_data.encounter_system, 'last_encounters'):
                    game_data.encounter_system.last_encounters = encounter_data.get("last_encounters", {})
                if hasattr(game_data.encounter_system, 'encounter_cooldowns'):
                    game_data.encounter_system.encounter_cooldowns = encounter_data.get("encounter_cooldowns", {})
                if hasattr(game_data.encounter_system, 'encounter_history'):
                    game_data.encounter_system.encounter_history = encounter_data.get("encounter_history", [])
                print("✅ Encounter System wiederhergestellt")
            except Exception as e:
                print(f"⚠️ Encounter System Load Fehler: {e}")

        print("💾 ✅ Alle Systeme erfolgreich wiederhergestellt!")
        return True

    except Exception as e:
        print(f"💾 ❌ Kritischer Fehler beim Wiederherstellen: {e}")
        return False


def save_enhanced_game_state(filepath: str, game_data) -> bool:
    """💾 Speichert erweiterten Spielstand mit allen neuen Features"""

    if not filepath:
        print("❌ Kein Dateipfad zum Speichern angegeben.")
        return False

    try:
        # Erstelle Verzeichnis falls nötig
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Bereite alle Daten vor
        print("💾 Bereite Save-Daten vor...")
        save_data = _prepare_save_data(game_data)

        # Speichere mit Enhanced Encoder
        print(f"💾 Speichere in: {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2, cls=EnhancedGameDataEncoder)

        print(f"💾 ✅ Erweiterter Spielstand gespeichert: {filepath}")
        return True

    except Exception as e:
        print(f"💾 ❌ Fehler beim Speichern: {e}")
        return False


def load_enhanced_game_state(filepath: str, game_data) -> bool:
    """💾 Lädt erweiterten Spielstand mit allen neuen Features"""

    if not filepath or not os.path.exists(filepath):
        print(f"💾 ❌ Datei nicht gefunden: {filepath}")
        return False

    try:
        # Lade JSON-Daten
        print(f"💾 Lade von: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            save_data = json.load(f)

        # Prüfe Version
        version = save_data.get("version", "legacy")
        if version == "legacy":
            print("💾 ⚠️ Legacy-Format erkannt, versuche Kompatibilität...")
            return _load_legacy_format(save_data, game_data)

        # Stelle erweiterte Daten wieder her
        print("💾 Stelle erweiterte Daten wieder her...")
        success = _restore_save_data(save_data, game_data)

        if success:
            print(f"💾 ✅ Erweiterter Spielstand geladen: {filepath}")
        else:
            print("💾 ⚠️ Teilweise Wiederherstellung mit Fehlern")

        return success

    except Exception as e:
        print(f"💾 ❌ Fehler beim Laden: {e}")
        return False


def _load_legacy_format(save_data: Dict[str, Any], game_data) -> bool:
    """🔧 Lädt alte Spielstände (Rückwärtskompatibilität)"""

    try:
        print("💾 Legacy-Kompatibilitätsmodus...")

        # Basic Data aus Legacy-Format
        if hasattr(game_data, 'chat_messages'):
            game_data.chat_messages = save_data.get("chat_messages", [])

        if hasattr(game_data, 'game_state'):
            game_data.game_state.update(save_data.get("game_state", {}))

        print("💾 ✅ Legacy-Daten geladen")
        return True

    except Exception as e:
        print(f"💾 ❌ Legacy-Load Fehler: {e}")
        return False


def autosave_enhanced(game_data) -> bool:
    """💾 Automatisches Speichern mit allen Features"""
    return save_enhanced_game_state(AUTOSAVE_PATH, game_data)


def get_save_info(filepath: str) -> Dict[str, Any]:
    """📊 Gibt Informationen über einen Spielstand zurück"""

    if not os.path.exists(filepath):
        return {"exists": False}

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        info = {
            "exists": True,
            "timestamp": data.get("timestamp", "Unknown"),
            "version": data.get("version", "Legacy"),
            "size_kb": round(os.path.getsize(filepath) / 1024, 1),
            "features": {}
        }

        # Feature-Erkennung
        advanced_systems = data.get("advanced_systems", {})

        for system_name in ["secret_system", "companion_system", "advanced_memory_system",
                            "emotional_intelligence", "relationship_system", "maternal_system"]:
            if system_name in advanced_systems:
                system_data = advanced_systems[system_name]

                if system_name == "secret_system":
                    secrets_count = len(system_data.get("secrets", {}))
                    info["features"]["secrets"] = f"{secrets_count} secrets"

                elif system_name == "companion_system":
                    companions_count = len(system_data.get("companions", {}))
                    active = system_data.get("active_companion")
                    info["features"]["companions"] = f"{companions_count} companions" + (
                        f" (active: {active})" if active else "")

                elif system_name == "advanced_memory_system":
                    memories = system_data.get("character_memories", {})
                    total_memories = sum(len(mem_list) for mem_list in memories.values())
                    info["features"]["memories"] = f"{total_memories} memories"

                elif system_name == "emotional_intelligence":
                    profiles = system_data.get("character_profiles", {})
                    info["features"]["emotional_ai"] = f"{len(profiles)} emotional profiles"

                elif system_name == "relationship_system":
                    relationships = system_data.get("relationships", {})
                    info["features"]["relationships"] = f"{len(relationships)} relationships"

        return info

    except Exception as e:
        return {"exists": True, "error": str(e)}


# === EXPORT FUNCTIONS ===

def save_dynamic_state(filepath: Optional[str] = None, chat_messages: Optional[List] = None,
                       game_state: Optional[Dict] = None) -> bool:
    """Legacy-kompatible Speicher-Funktion"""
    target_filepath = filepath if filepath is not None else AUTOSAVE_PATH

    # Erstelle Mock-GameData für Legacy-Calls
    class MockGameData:
        def __init__(self):
            self.chat_messages = chat_messages or []
            self.game_state = game_state or {}

    mock_data = MockGameData()
    return save_enhanced_game_state(target_filepath, mock_data)


def load_dynamic_state(filepath: str = AUTOSAVE_PATH) -> Tuple[List, Dict, bool]:
    """Legacy-kompatible Lade-Funktion"""

    class MockGameData:
        def __init__(self):
            self.chat_messages = []
            self.game_state = {}

    mock_data = MockGameData()
    success = load_enhanced_game_state(filepath, mock_data)

    return mock_data.chat_messages, mock_data.game_state, success


def get_autosave_path() -> str:
    return AUTOSAVE_PATH


def get_saves_dir() -> str:
    return SAVES_DIR


if __name__ == "__main__":
    print("💾 ENHANCED SAVE/LOAD SYSTEM")
    print("=====================================")
    print("✅ Secret System Support")
    print("✅ Companion System Support")
    print("✅ Advanced Memory Support")
    print("✅ Emotional Intelligence Support")
    print("✅ Legacy Compatibility")
    print("✅ Enhanced JSON Encoding")