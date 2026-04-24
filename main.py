# -*- coding: utf-8 -*-
"""
Hauptdatei für das Chat RPG - CLEANED VERSION
Entfernt redundante Enhancement-Systeme für bessere Performance
"""
from selectors import SelectSelector

import customtkinter as ctk
from tkinter import messagebox
import os
from openai import OpenAI
import json
import random
from datetime import timedelta
import sys
import re

from moduls import encounter_system
from moduls.modern_gui_tutorial import ModernRPGGUI

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'moduls'))

# Basis-Module aus Root (bleiben im Root)
import backstory
from backstory import GAME_START_DATE, calculate_days_with_tsunade

# Erstelle eine kompatible Variable für Legacy-Code
MAIN_BACKSTORY = backstory.get_current_backstory()

# ✅ CORE SYSTEMS ONLY - Nur die wichtigsten Module laden

# 1. Advanced Prompt System (CORE)
try:
    from moduls.advanced_prompt_system import *

    print("✅ Erweitertes Prompt System geladen")
except ImportError as e:
    print(f"⚠️ Erweitertes Prompt System Import Fehler: {e}")

# 2. Environment System (CORE)
try:
    from moduls.environment_system import EnvironmentSystem, create_environment_system
    from moduls.environment_integration import setup_safe_enhanced_encounter_system

    print("✅ Environment System Module geladen")
except ImportError as e:
    print(f"⚠️ Environment System Import Fehler: {e}")

# 3. Basic Encounter System (CORE)
try:
    from moduls.encounter_system import SimpleEncounterSystem

    print("✅ Encounter System Module geladen")
except ImportError as e:
    print(f"⚠️ Encounter System Import Fehler: {e}")

# 4. Maternal System (CORE - vereinfacht)
try:
    import moduls.maternal_system as maternal_system
    import moduls.maternal_behavior_system as maternal_behavior_system
    from moduls.maternal_system import EnhancedMaternalSystem
    from moduls.maternal_behavior_system import MaternalBehaviorEngine

    print("✅ Maternal System Module geladen")
except ImportError as e:
    print(f"⚠️ Maternal System Import Fehler: {e}")

# 5. Relationship System (SIMPLIFIED)
try:
    from moduls.relationship_integration import setup_relationship_system_for_gui

    RELATIONSHIP_SYSTEM_AVAILABLE = True
    print("✅ Relationship System Module verfügbar!")
except ImportError as e:
    print(f"⚠️ Relationship System nicht verfügbar: {e}")
    RELATIONSHIP_SYSTEM_AVAILABLE = False
#6 Geheimnis System
try:
    from moduls.secret_system import integrate_secret_system, SecretSystemIntegration
    SECRET_SYSTEM_AVAILABLE = True
    print("✅ Claude Secret System Module geladen!")
except ImportError as e:
    print(f"⚠️ Claude Secret System Import Fehler: {e}")
    SECRET_SYSTEM_AVAILABLE = False

#7 Companion System
try:
    from moduls.companion_system import integrate_companion_system, CompanionSystem, CompanionStatus, CompanionMood
    COMPANION_SYSTEM_AVAILABLE = True
    print("✅ Companion System Module geladen!")
except ImportError as e:
    print(f"⚠️ Companion System Import Fehler: {e}")
    COMPANION_SYSTEM_AVAILABLE = False

# Claude Memory System
try:
    from moduls.advanced_memory_system import integrate_advanced_memory_system, AdvancedMemorySystem
    ADVANCED_MEMORY_AVAILABLE = True
    print("✅ Advanced Memory System Module geladen!")
except ImportError as e:
    print(f"⚠️ Advanced Memory System Import Fehler: {e}")
    ADVANCED_MEMORY_AVAILABLE = False

# 9. 💭 EMOTIONAL INTELLIGENCE ENGINE (CLAUDE ULTRA)
try:
    from moduls.emotional_intelligence_engine import integrate_advanced_emotional_intelligence, AdvancedEmotionalIntelligence
    ADVANCED_EMOTIONAL_INTELLIGENCE_AVAILABLE = True
    print("✅ Emotional Intelligence Engine Module geladen!")
except ImportError as e:
    print(f"⚠️ Emotional Intelligence Engine Import Fehler: {e}")
    ADVANCED_EMOTIONAL_INTELLIGENCE_AVAILABLE = False

#10 ⏰ TIME SYSTEM
try:
    from moduls.game_time_system import integrate_time_system
    TIME_SYSTEM_AVAILABLE = True
    print("✅ Game Time System Module geladen!")
except ImportError as e:
    print(f"⚠️ Time System Import Fehler: {e}")
    TIME_SYSTEM_AVAILABLE = False

# 11. 🔮 ENHANCED PREDICTIVE INTELLIGENCE (NEU)
try:
    from moduls.enhanced_predictive_intelligence import integrate_enhanced_predictive_intelligence
    ENHANCED_PREDICTIVE_AVAILABLE = True
    print("✅ Enhanced Predictive Intelligence Module geladen!")
except ImportError as e:
    print(f"⚠️ Enhanced Predictive Import Fehler: {e}")
    ENHANCED_PREDICTIVE_AVAILABLE = False

#12. # 👨‍👩‍👧 FAMILY TIME SYSTEM Integration
try:
    from moduls.family_time_system import integrate_family_time_system
    FAMILY_TIME_AVAILABLE = True
    print("✅ Family Time System Module geladen!")
except ImportError as e:
    print(f"⚠️ Family Time System Import Fehler: {e}")
    FAMILY_TIME_AVAILABLE = False

# 13 BIBLIOTHEKS-SYSTEM
try:
    from moduls.library_location_system import LibraryLocationSystem
    LIBRARY_SYSTEM_AVAILABLE = True
    print("✅ Bibliotheks-System Module geladen!")
except ImportError as e:
    print(f"⚠️ Bibliotheks-System Import Fehler: {e}")
    LIBRARY_SYSTEM_AVAILABLE = False

# 14 KINOREIFE ATMOSPHERE
try:
    from moduls.atmospheric_elements_system import integrate_atmospheric_system

    ATMOSPHERIC_SYSTEM_AVAILABLE = True
    print("✅ Kinoreife Atmosphäre geladen!")
except ImportError as e:
    print(f"⚠️ Kinoreife Atmosphäre System Import Fehler: {e}")
    ATMOSPHERIC_SYSTEM_AVAILABLE = False

# 15 KAMPFSYSTEM
try:
    from moduls.advanced_combat_system import integrate_combat_system
    COMBAT_SYSTEM_AVAILABLE = True
    print("✅ Advanced Combat System Module geladen!")
except ImportError as e:
    print(f"⚠️ Advanced Combat System Import Fehler: {e}")
    COMBAT_SYSTEM_AVAILABLE = False

# 16 GENIN-TEAM SYSTEM
try:
    from moduls.genin_team_system import integrate_genin_team_system
    GENIN_TEAM_AVAILABLE = True
    print("✅ Genin Team Formation System Module geladen!")
except ImportError as e:
    print(f"⚠️ Genin Team System Import Fehler: {e}")
    GENIN_TEAM_AVAILABLE = False

#17 TEAM FIX BEIBEHALTEN!
try:
    from team_system_integration_fix import integrate_team_fix
    TEAM_FIX_AVAILABLE = True
except ImportError:
    TEAM_FIX_AVAILABLE = False

#18 SLEEP MANAGEMENT
try:
    from moduls.sleep_management_system import integrate_sleep_system
    SLEEP_SYSTEM_AVAILABLE = True
    print("✅ Sleep Management System Module geladen!")
except ImportError as e:
    print(f"⚠️ Sleep Management System Import Fehler: {e}")
    SLEEP_SYSTEM_AVAILABLE = False

#19 REISE-VORSCHLAG
try:
    from moduls.ai_location_suggestion_system import check_ai_response_for_travel_suggestion, \
    integrate_ai_location_detection

    TRAVEL_SUGGESTION_AVAILABLE = True
    print("✅ Reise Vorschlag Module geladen!")
except ImportError as e:
    print(f"⚠️ Reise Vorschlag Module Import Fehler: {e}")
    TRAVEL_SUGGESTION_AVAILABLE = False


#20 ADVANCED GERMAN GRAMMAR
from moduls.advanced_german_grammar import ProperGermanLanguageProcessor



# GUI Import (bleibt im Root)
from rpg_gui import RPG_GUI

# ✅ ENHANCED DATETIME JSON FIX
import json
from datetime import datetime


class EnhancedDateTimeEncoder(json.JSONEncoder):
    """Erweiterte JSON Encoder für alle datetime Objekte"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, 'isoformat'):  # Für custom datetime Klassen
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):  # Für komplexe Objekte
            return str(obj)
        return super().default(obj)


# Patch ALLE json Funktionen
_original_dump = json.dump
_original_dumps = json.dumps


def enhanced_dump(obj, fp, **kwargs):
    kwargs.setdefault('cls', EnhancedDateTimeEncoder)
    kwargs.setdefault('default', str)  # Fallback für alle anderen Objekte
    return _original_dump(obj, fp, **kwargs)


def enhanced_dumps(obj, **kwargs):
    kwargs.setdefault('cls', EnhancedDateTimeEncoder)
    kwargs.setdefault('default', str)  # Fallback für alle anderen Objekte
    return _original_dumps(obj, **kwargs)


json.dump = enhanced_dump
json.dumps = enhanced_dumps

print("✅ Enhanced DateTime JSON Fix aktiviert")

# --- KONSTANTEN UND PFADE ---
SAVES_DIR = "saves"
AUTOSAVE_PATH = os.path.join(SAVES_DIR, "autosave.json")
GAME_RULES_PATH = "prompts/gamerules.txt"

# --- LLM KONSTANTEN FÜR LM STUDIO ---
LM_MODEL = "meta-llama-3.1-8b-claude-imat"
LM_STUDIO_BASE_URL = "http://127.0.0.1:1234/v1"
LM_STUDIO_API_KEY = "not-needed"

# --- CTk APPEARANCE SETTINGS ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Fallback-Definitionen (werden überschrieben falls Module laden)
maternal_system = None
maternal_behavior_system = None


# ✅ SAFE JSON OPERATIONS
def safe_json_save(data, filepath):
    """Sichere JSON Speicherung mit error handling"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, cls=EnhancedDateTimeEncoder, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ JSON Save Fehler: {e}")
        return False


def safe_json_load(filepath):
    """Sichere JSON Ladung mit error handling"""
    try:
        if not os.path.exists(filepath):
            print(f"⚠️ Datei nicht gefunden: {filepath}")
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ JSON Load Fehler: {e}")
        return None


class GameData:
    """
    VEREINFACHTE GameData Klasse - nur die wichtigsten Enhancement-Systeme
    """

    def __init__(self):
        print("🚀 Initialisiere VEREINFACHTE Game Data...")

        # Lade Spielregeln
        self.load_game_rules()

        self.chat_messages = []  # <--- DIESE ZEILE FEHLT!


        #Lade deutsche Grammatik
        self.german_processor = ProperGermanLanguageProcessor()


        # Standard-Charaktere
        self.main_characters = ["tsunade", "sukuna"]
        self.active_character = "tsunade"

        # Spiel-Status
        self.encounter_active = False
        self.current_backstory = backstory.get_current_backstory()
        self.current_location = 'tsunades_haus'

        # Game State mit locations
        self.game_state = {
            'current_location': 'tsunades_haus_kueche',
            'tsunade_location': 'tsunades_haus_kueche',
            'sukuna_location': 'tsunades_haus_kueche',
            'story_state': 'beginning',
            'day': 3,
            'relationships': {
                'tsunade': {'level': 100, 'events': []},
                'sukuna': {'level': 0, 'events': []}
            },
            # ROOM SYSTEM
            'room_customization': {
                'has_new_bed': False,
                'has_desk': False,
                'has_bookshelf': False,
                'total_spent': 0
            },

            # ✅ NEU: RYO & MISSION TRACKING
            'player_stats': {
                'ryo': 500,  # Start-Geld
                'experience': 0,
                'missions_completed': 0,
                'level': 1
            },
            'mission_history': [],
            'active_mission': None
        }

        # initalisiere Encounter History
        self.encountered_characters = []


        # 🆕 MESSAGE COUNTER FÜR AUTO TIME ADVANCE
        self.message_counter = 0
        self.messages_per_hour = 40  # Alle 40 Nachrichten = +1 Stunde

        # 🆕 DAY TRACKING
        if 'day' not in self.game_state:
            self.game_state['day'] = 1

        # ✅ CORE SYSTEMS SETUP
        self.setup_core_systems()



        # ✅ LM Studio Client
        self.setup_lm_studio_client()

        print("✅ Vereinfachte Game Data initialisiert!")

        #Team fix beibehalten!
        if TEAM_FIX_AVAILABLE:
            integrate_team_fix(self)

    def get(self, key, default=None):
        """Dict-like get method für Kompatibilität"""
        try:
            return getattr(self, key, default)
        except:
            return default

    def start_encounter(self, character_name):
        if character_name not in self.encountered_characters:
            self.encountered_characters.append(character_name)
            print(f"✅ Erste Begegnung mit {character_name} getrackt!")

    def increment_message_counter(self):
        """📊 Zählt Nachrichten und advance Zeit automatisch"""
        self.message_counter += 1

        if self.message_counter >= self.messages_per_hour:
            # Zeit voranspulen
            if hasattr(self, 'time_system') and self.time_system:
                try:
                    old_time = self.time_system.get_current_game_time()
                    old_day = self.game_state.get('day', 1)

                    self.time_system.advance_time(60)  # +60 Minuten
                    new_time = self.time_system.get_formatted_time()

                    # 🆕 CHECK FOR DAY CHANGE
                    new_day = self._calculate_current_day(new_time)
                    if new_day > old_day:
                        self.game_state['day'] = new_day
                        print(f"📅 NEW DAY: Tag {new_day}")

                    print(f"⏰ AUTO TIME ADVANCE: {new_time} (nach {self.message_counter} Nachrichten)")

                    # Counter zurücksetzen
                    self.message_counter = 0

                    return new_time  # Gib neue Zeit zurück
                except Exception as e:
                    print(f"⚠️ Auto Time Advance Fehler: {e}")

            # Counter trotzdem zurücksetzen
            self.message_counter = 0

        return None  # Keine Zeit advancement

    def _calculate_current_day(self, formatted_time):
        """📅 Berechnet aktuellen Tag basierend auf Game Time"""
        try:
            # Einfache Implementierung: Jede 24 Stunden = +1 Tag
            if hasattr(self, 'time_system'):
                current_game_time = self.time_system.get_current_game_time()
                start_time = getattr(self.time_system, 'start_time', current_game_time)

                # Berechne vergangene Stunden
                time_diff = current_game_time - start_time
                hours_passed = time_diff.total_seconds() / 3600

                # Tag = 1 + (vergangene Stunden / 24)
                return int(1 + (hours_passed // 24))
        except:
            pass

        return self.game_state.get('day', 1)

    def setup_core_systems(self):
        """Initialisiert nur die wichtigsten Systeme ohne Konflikte"""

        # 1. Maternal System (CORE)
        try:
            self.maternal_system = EnhancedMaternalSystem(game_state=self.game_state, gui=None)
            self.behavior_engine = MaternalBehaviorEngine(self.maternal_system)
            print("✅ Maternal System initialisiert")
        except Exception as e:
            print(f"⚠️ Maternal System Fehler: {e}")
            self.maternal_system = None
            self.behavior_engine = None

        # 2. Basic Encounter System (CORE) - Muss ZUERST initialisiert werden
        try:
            self.encounter_system = SimpleEncounterSystem(self, gui=None)  # GUI wird später gesetzt
            print("✅ Encounter System initialisiert")
        except Exception as e:
            print(f"⚠️ Encounter System Fehler: {e}")
            self.encounter_system = None

        # 3. Environment System (SIMPLIFIED) - Braucht encounter_system
        try:
            if self.encounter_system:
                self.environment_system = create_environment_system(self.encounter_system)
                self.enhanced_encounter = setup_safe_enhanced_encounter_system(self)
            else:
                self.environment_system = None
                self.enhanced_encounter = None
            print("✅ Environment System initialisiert")
        except Exception as e:
            print(f"⚠️ Environment System Fehler: {e}")
            self.environment_system = None
            self.enhanced_encounter = None

        # 4. Relationship System (nur wenn verfügbar)
        if RELATIONSHIP_SYSTEM_AVAILABLE:
            try:
                # Stelle sicher, dass game_state die richtige Struktur hat
                if 'relationships' not in self.game_state:
                    self.game_state['relationships'] = {
                        'tsunade': {'level': 0, 'events': []},
                        'sukuna': {'level': 0, 'events': []}
                    }

                self.relationship_system = None  # Wird von GUI initialisiert
                self.relationship_manager = None
                print("✅ Relationship System bereit")

            except Exception as e:
                print(f"⚠️ Relationship System Setup Fehler: {e}")
                self.relationship_system = None
                self.relationship_manager = None

        #5. Secret System
        if SECRET_SYSTEM_AVAILABLE:
            try:
                integrate_secret_system(self)
                print("🎭 Secret System erfolgreich integriert!")
            except Exception as e:
                print(f"⚠️ Secret System Integration Fehler: {e}")

        #6. Companion System
        if COMPANION_SYSTEM_AVAILABLE:
            try:
                integrate_companion_system(self)
                print("👥 Companion System erfolgreich integriert!")
            except Exception as e:
                print(f"⚠️ Companion System Integration Fehler: {e}")

        #7.
        if ADVANCED_MEMORY_AVAILABLE:
            try:
                integrate_advanced_memory_system(self)
                print("🧠 Advanced Memory System erfolgreich integriert!")
            except Exception as e:
                print(f"⚠️ Memory System Integration Fehler: {e}")

        #8.
        if ADVANCED_EMOTIONAL_INTELLIGENCE_AVAILABLE:
            try:
                integrate_advanced_emotional_intelligence(self)
                print("🧠 Emotional Intelligence Engine erfolgreich integriert!")
            except Exception as e:
                print(f"⚠️ Emotional Integration Fehler: {e}")

        #9
        if ENHANCED_PREDICTIVE_AVAILABLE:
            try:
                integrate_enhanced_predictive_intelligence(self)
                print("🔮 Enhanced Predictive Intelligence erfolgreich integriert!")
            except Exception as e:
                print(f"⚠️ Enhanced Predictive Intelligence Fehler: {e}")

        #10
        if TIME_SYSTEM_AVAILABLE:
            try:
                integrate_time_system(self)
                print("Zeitsystem erfolgreich integriert!")
                if hasattr(self, 'maternal_system') and hasattr(self, 'time_system'):
                    self.maternal_system.set_time_system(self.time_system)
                    print("✅ Maternal System mit Game Time System verknüpft!")
            except Exception as e:
                print(f"Zeitsystem Integration Fehler: {e}")

        #11
        if FAMILY_TIME_AVAILABLE:
            try:
                integrate_family_time_system(self)
                print("👨‍👩‍👧 Family Time System erfolgreich integriert!")
            except Exception as e:
                print(f"⚠️ Family Time Integration Fehler: {e}")

        #12
        if LIBRARY_SYSTEM_AVAILABLE:
            try:
                self.library_system = LibraryLocationSystem(
                    self.game_state, None, self.encounter_system
                )

                # Integriere in Encounter-System
                if self.encounter_system:
                    self.library_system.integrate_with_encounter_system(self.encounter_system)
                    print("✅ Bibliotheken in Encounter-System integriert")

                print("📚✅ Bibliotheks-System erfolgreich initialisiert!")

            except Exception as e:
                print(f"❌ Bibliotheks-System Fehler: {e}")

        #13
        #if ATMOSPHERIC_SYSTEM_AVAILABLE:
           # try:
                #integrate_atmospheric_system(self)
                #print("🌅 Atmospheric Elements System erfolgreich integriert!")
           # except Exception as e:
                #print(f"⚠️ Atmospheric Elements System Integration Fehler: {e}")

        #14
        if COMBAT_SYSTEM_AVAILABLE:
            try:
                integrate_combat_system(self)
                print("⚔️ Advanced Combat System erfolgreich integriert!")
            except Exception as e:
                print(f"⚠️ Combat System Integration Fehler: {e}")

        #15
        if GENIN_TEAM_AVAILABLE:
            try:
                integrate_genin_team_system(self)
                print("👥 Genin Team Formation System erfolgreich integriert!")
            except Exception as e:
                print(f"⚠️ Genin Team System Integration Fehler: {e}")

        #16
        if SLEEP_SYSTEM_AVAILABLE:
            try:
                integrate_sleep_system(self)
                print("🌙 Sleep Management System erfolgreich integriert!")
            except Exception as e:
                print(f"⚠️ Sleep Management System Integration Fehler: {e}")

        #17
        if TRAVEL_SUGGESTION_AVAILABLE:
            try:
                integrate_ai_location_detection(self)
                print("AI Location Detection für Reisen geladen!")
            except Exception as e:
                print(f"⚠️ AI Location Detection Fehler: {e}")







    def setup_lm_studio_client(self):
        """Initialisiert den LM Studio Client"""
        try:
            self.client = OpenAI(
                base_url=LM_STUDIO_BASE_URL,
                api_key=LM_STUDIO_API_KEY
            )
            print("✅ LM Studio Client verbunden")
        except Exception as e:
            print(f"❌ LM Studio Connection Fehler: {e}")
            self.client = None

    def load_game_rules(self):
        """Lädt die Spielregeln aus der Datei"""
        try:
            with open(GAME_RULES_PATH, 'r', encoding='utf-8') as f:
                self.game_rules = f.read()
            print("✅ Spielregeln geladen")
        except FileNotFoundError:
            print("⚠️ Spielregeln-Datei nicht gefunden - verwende Standard-Regeln")

    def _detect_companion_offer(self, ai_response: str):
        """Erkennt wenn ein Charakter im Dialog anbietet mitzukommen"""

        import moduls.companion_system

        offer_keywords = [
            'ich komme mit', 'ich begleite', 'ich gehe mit',
            'ich bringe dich', 'komm, wir gehen', 'ich komm mit',
            'ich zeige dir', 'lass uns zusammen', 'ich passe auf dich auf',
            'ich begleite dich', 'gehen wir zusammen', 'ich komme auch',
            'warte, ich komme'
        ]

        if not any(keyword in ai_response.lower() for keyword in offer_keywords):
            return

        character = self.active_character.lower()


        if not hasattr(self, 'companion_system') or not self.companion_system:
            return

        try:
            # Companion muss im System existieren
            if character not in self.companion_system.companions:
                return

            companion = self.companion_system.companions[character]

            # Status auf SUGGESTED setzen
            companion.status = CompanionStatus.SUGGESTED
            companion.mood = CompanionMood.WILLING

            print(f"✅ Companion Offer erkannt: {character.title()} möchte mitkommen!")

            if hasattr(self, 'gui') and self.gui:
                self.gui.display_message(
                    "System",
                    f"💭 {character.title()} möchte dich begleiten!\n"
                    f"Tippe '/accept {character}' um sie/ihn mitzunehmen, "
                    f"oder '/decline {character}' um alleine zu gehen.",
                    "info"
                )
        except Exception as e:
            print(f"⚠️ Companion Offer Fehler für {character}: {e}")


    def get_llm_response(self, user_input: str) -> str:
        """
           NEUGESCHRIEBEN: Saubere Message-History, korrektes System/User-Trennung,
           alle Systeme korrekt integriert.
           """
        if not self.client:
            return "[FEHLER] LM Studio Client nicht verfügbar. Ist LM Studio gestartet?"

        try:
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # 1. SYSTEM PROMPT BAUEN (Charakter, Regeln, Kontext)
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            system_prompt = self._build_enhanced_system_prompt()
            system_prompt = self.sanitize_prompt(system_prompt)

            # ← DEBUG: Temporär einkommentieren um Prompt zu prüfen
            print("=" * 60)
            print("📋 SYSTEM PROMPT PREVIEW:")
            print(system_prompt[:1000])  # Erste 1000 Zeichen
            print("=" * 60)

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # 2. CONVERSATION HISTORY AUFBAUEN
            # Echte Chat-History als abwechselnde user/assistant Rollen
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            messages = [{"role": "system", "content": system_prompt}]

            # Hole Chat-History aus der GUI (wo sie live gespeichert wird)
            raw_history = []
            if hasattr(self, 'gui') and self.gui and hasattr(self.gui, 'chat_messages'):
                raw_history = self.gui.chat_messages
            elif hasattr(self, 'chat_messages'):
                raw_history = self.chat_messages

            # Letzte N Nachrichten als echte Konversation einfügen
            # (NICHT den aktuellen user_input, der kommt separat unten)
            HISTORY_TURNS = 6  # = 6 Nachrichten = ~3 Hin-und-Her
            recent_history = raw_history[-HISTORY_TURNS:] if raw_history else []

            character_name = self.active_character.title()

            for sender, message in recent_history:
                if not message or not message.strip():
                    continue  # Leere Nachrichten überspringen

                if sender == "Du" or sender.lower() == "sukuna":
                    messages.append({"role": "user", "content": message})
                elif sender == character_name or sender.lower() == self.active_character.lower():
                    messages.append({"role": "assistant", "content": message})
                # System-Nachrichten, Fehler etc. überspringen

            # Aktuellen User-Input als letzte Nachricht
            messages.append({"role": "user", "content": user_input})

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # 3. ZUSATZ-KONTEXT aus aktiven Systemen (kompakt, als system-injection)
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            context_parts = []

            # Umgebungs-Kontext
            if hasattr(self, 'environment_system') and self.environment_system:
                try:
                    env_context = None
                    for method_name in ['get_current_environment_description',
                                        'get_environment_description',
                                        'get_location_description',
                                        'describe_location']:
                        if hasattr(self.environment_system, method_name):
                            env_context = getattr(self.environment_system, method_name)(self.current_location)
                            break

                    if env_context:
                        context_parts.append(f"[ORT] {env_context}")
                except Exception as e:
                    print(f"⚠️ Environment Context Fehler: {e}")

            # Relationship-Status (kompakt, nur wenn relevant)
            if hasattr(self, 'relationship_system') and self.relationship_system:
                try:
                    rel_info = self.relationship_system.get_relationship_info(self.active_character)
                    rel_level = rel_info.get('level', 0)
                    rel_title = rel_info.get('titel', 'Neutral')
                    context_parts.append(f"[BEZIEHUNG zu Sukuna] Level {rel_level} – {rel_title}")
                except Exception as e:
                    print(f"⚠️ Relationship Context Fehler: {e}")

            # Maternal-Status (kompakt)
            if hasattr(self, 'maternal_system') and self.maternal_system:
                try:
                    mat_level = self.maternal_system.get_current_level()
                    mat_cat = self.maternal_system.get_level_category()
                    if mat_level > 0:
                        context_parts.append(f"[MÜTTERLICHKEIT] Level {mat_level} – {mat_cat}")
                except Exception as e:
                    print(f"⚠️ Maternal Context Fehler: {e}")

            # Companion-Status
            if hasattr(self, 'companion_system') and self.companion_system:
                try:
                    active_comp = self.companion_system.active_companion
                    if active_comp:
                        context_parts.append(f"[COMPANION] {active_comp.title()} begleitet Sukuna gerade.")
                except Exception as e:
                    print(f"⚠️ Companion Context Fehler: {e}")

            # Kontext als eigene System-Nachricht einfügen (NICHT in den User-Input mischen!)
            if context_parts:
                context_block = "\n".join(context_parts)
                # Füge NACH dem system prompt, VOR der history ein
                messages.insert(1, {
                    "role": "system",
                    "content": f"## AKTUELLER SPIELSTATUS (nur zur Info, nicht vorlesen):\n{context_block}"
                })

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # 4. DEBUG LOG (kannst du später auskommentieren)
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            print(f"📨 LLM Request: {len(messages)} Messages | Charakter: {character_name}")
            print(f"   System: {len(system_prompt)} Zeichen | History: {len(recent_history)} Nachrichten")

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # 5. LLM ANFRAGE
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            response = self.client.chat.completions.create(
                model= LM_MODEL,  # dein aktuelles Modell
                messages=messages,
                max_tokens=500,
                temperature=0.85,
                top_p=0.90,
                frequency_penalty=0.35,
                presence_penalty=0.20,
                extra_body={
                    "min_p": 0.05,
                    "repeat_penalty": 1.07,
                    "top_k": 45,
                    "thinking": False
                }
            )

            ai_response = response.choices[0].message.content.strip()

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # 6. RESPONSE CLEANING
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # Entferne Charakter-Präfix wenn das Modell ihn selbst schreibt (z.B. "Tsunade: ...")
            if ai_response.startswith(f"{character_name}:"):
                ai_response = ai_response[len(f"{character_name}:"):].strip()

            # Entferne bekannte Corruption-Patterns
            ai_response = self.sanitize_prompt(ai_response)

            # Entferne hardcoded Family-Time Strings (aus deinem alten Code)
            import re
            ai_response = re.sub(r'\*öffnet Arme einladend\*.*', '', ai_response, flags=re.DOTALL).strip()
            ai_response = re.sub(r'💭 \*[^*]+spürt:[^*]*\*', '', ai_response).strip()
            ai_response = re.sub(r'\*liebevoll aber bestimmt\*', '', ai_response).strip()

            # Fallback falls Antwort leer
            if not ai_response:
                ai_response = f'*{character_name} schweigt kurz und schaut dich nachdenklich an.*'

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # 7. SYSTEME NACH ANTWORT UPDATEN
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            self._update_systems_after_response(user_input, ai_response)

            print(f"✅ AI Response ({len(ai_response)} Zeichen): {ai_response[:80]}...")
            return ai_response

        except Exception as e:
            print(f"❌ LLM Fehler: {e}")
            import traceback
            traceback.print_exc()
            return f"[FEHLER] LM Studio nicht erreichbar oder Modell-Fehler.\nDetails: {str(e)}"

    def sanitize_prompt(self, prompt: str) -> str:
        """Entfernt bekannte Corruption-Patterns aus Prompts"""
        import re
        prompt = re.sub(r'<\|begin_of_text\|>.*?Familie Steiner.*', '', prompt, flags=re.DOTALL)
        prompt = re.sub(r'§ \d+.*?Der Vertrag kommt.*', '', prompt, flags=re.DOTALL)
        return prompt.strip()

    def _get_current_time_context(self):
        """Gibt aktuellen Zeit-Kontext zurück"""
        try:
            # Versuche das Time System zu nutzen
            if hasattr(self, 'time_system') and self.time_system:
                current_time = self.time_system.get_current_game_time()
                period = self.time_system.get_time_period()
                return f"{current_time.strftime('%H:%M')} ({period.value})"
            elif hasattr(self, 'game_time_system') and self.game_time_system:
                current_time = self.game_time_system.get_current_game_time()
                period = self.game_time_system.get_time_period()
                return f"{current_time.strftime('%H:%M')} ({period.value})"
            else:
                # Fallback auf echte Zeit
                from datetime import datetime
                now = datetime.now()
                hour = now.hour
                if 5 <= hour < 12:
                    period = "Morgen"
                elif 12 <= hour < 17:
                    period = "Nachmittag"
                elif 17 <= hour < 21:
                    period = "Abend"
                else:
                    period = "Nacht"
                return f"{now.strftime('%H:%M')} ({period})"
        except Exception as e:
            print(f"⚠️ Time Context Error: {e}")
            return "Unbekannte Zeit"

    def _build_conversation_context(self):
        """Drastically limit conversation context"""
        try:
            if hasattr(self, 'gui') and hasattr(self.gui, 'chat_history'):
                chat_history = self.gui.chat_history

                # ✅ ONLY KEEP LAST 4 MESSAGES (instead of more)
                recent_messages = chat_history[-4:] if len(chat_history) > 4 else chat_history

                context_lines = []
                for sender, message in recent_messages:
                    if sender == "Du":
                        context_lines.append(f"Sukuna: {message}")
                    elif sender == "Tsunade":
                        context_lines.append(f"Tsunade: {message}")

                # Limit total context length
                context = "\n".join(context_lines[-4:])  # Only last 3 exchanges
                return context[:800]  # Hard limit: 500 characters
        except:
            pass
        return ""

    def get_recent_context(self, max_messages=6):
        """Get only recent messages to avoid repetition loops"""
        return self.chat_messages[-max_messages:] if len(self.chat_messages) > max_messages else self.chat_messages

    def _build_enhanced_system_prompt(self):
        """
        NEUGESCHRIEBEN: Klare Layer-Struktur, kein Durcheinander.
        Aufbau: IDENTITÄT → WELT → CHARAKTER-ZUSTAND → REGELN → FORMAT
        Fix: AdvancedPromptSystem ergänzt identity_block, überschreibt ihn nicht.
        """

        character_name = self.active_character.title()
        current_backstory = backstory.get_current_backstory()

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # ENCOUNTER-CHARAKTER: Eigener, kompakter Prompt — fertig
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        if self.encounter_active and character_name.lower() not in ['tsunade']:
            print(f"🎭 Encounter-Prompt für {character_name}")
            return self._build_encounter_character_prompt(current_backstory)

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # LAYER 1: IDENTITÄT
        # Basis: _get_character_identity()
        # Erweiterung: AdvancedPromptSystem constitutional + personality (falls vorhanden)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        identity_block = self._get_character_identity(character_name)

        # ✅ FIX: AdvancedPromptSystem erweitert identity_block, ersetzt ihn NICHT
        if hasattr(self, 'advanced_prompt_system') and self.advanced_prompt_system:
            try:
                aps = self.advanced_prompt_system
                constitutional = aps.layers.get('constitutional', '').strip()
                personality = aps.layers.get('personality', '').strip()

                # Nur anhängen wenn nicht leer und nicht schon enthalten
                extra_parts = []
                if constitutional and constitutional not in identity_block:
                    extra_parts.append(constitutional)
                if personality and personality not in identity_block:
                    extra_parts.append(personality)

                if extra_parts:
                    identity_block = identity_block + "\n\n" + "\n\n".join(extra_parts)
                    print(f"✅ AdvancedPromptSystem: constitutional + personality zu identity_block hinzugefügt")
            except Exception as e:
                print(f"⚠️ AdvancedPromptSystem identity_block Erweiterung Fehler: {e} — nutze Standard")

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # LAYER 2: WELT & KONTEXT
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        time_context = self._get_current_time_context()
        day = self.game_state.get('day', 1)

        world_block = f"""## WELT & SITUATION
            Ort: {self.current_location}
            Tageszeit: {time_context} | Tag: {day}
            Backstory: {current_backstory}
            Encounter aktiv: {'Ja' if self.encounter_active else 'Nein'}"""

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # LAYER 3: CHARAKTER-ZUSTAND (dynamisch)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        state_parts = []

        # Maternal System (nur für Tsunade)
        if self.active_character.lower() == 'tsunade' and hasattr(self, 'maternal_system') and self.maternal_system:
            try:
                mat_level = self.maternal_system.get_current_level()
                mat_data = self.maternal_system.get_current_behavior_data()
                mat_behavior = self._format_maternal_behavior_for_prompt(mat_data)

                state_parts.append(f"""## MÜTTERLICHKEITS-ZUSTAND (Level {mat_level}/1000)
            Kategorie: {mat_data.get('category', 'Unbekannt')}
            Verhalten: {mat_behavior}""")
            except Exception as e:
                print(f"⚠️ Maternal State Fehler: {e}")

        # Relationship Level
        if hasattr(self, 'relationship_system') and self.relationship_system:
            try:
                rel_info = self.relationship_system.get_relationship_info(self.active_character)
                rel_level = rel_info.get('level', 0)
                rel_title = rel_info.get('titel', 'Neutral')
                state_parts.append(f"## BEZIEHUNG ZU SUKUNA\nLevel: {rel_level} – {rel_title}")
            except Exception as e:
                print(f"⚠️ Relationship State Fehler: {e}")

        # Companion Status
        if hasattr(self, 'companion_system') and self.companion_system:
            try:
                active = self.companion_system.active_companion
                if active:
                    state_parts.append(f"## COMPANION\n{active.title()} begleitet Sukuna gerade.")
            except Exception as e:
                print(f"⚠️ Companion State Fehler: {e}")

        # Secret System
        if hasattr(self, 'secret_system') and self.secret_system:
            try:
                known = getattr(self.secret_system, 'discovered_secrets', [])
                if known:
                    state_parts.append(f"## BEKANNTE GEHEIMNISSE\n" + "\n".join(f"- {s}" for s in known[-3:]))
            except Exception as e:
                print(f"⚠️ Secret State Fehler: {e}")

        state_block = "\n\n".join(state_parts) if state_parts else ""

        # Memory Context (kompakt, max 3 relevante Memories)
        if hasattr(self, 'advanced_memory_system') and self.advanced_memory_system:
            try:
                relevant_memories = self.advanced_memory_system.recall_relevant_memories(
                    self.active_character,
                    context="aktuelle_interaktion",
                    limit=3
                )
                if relevant_memories:
                    memory_lines = "\n".join(f"- {m.content}" for m in relevant_memories)
                    state_parts.append(f"## ERINNERUNGEN AN SUKUNA\n{memory_lines}")
            except Exception as e:
                print(f"⚠️ Memory State Fehler: {e}")

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # LAYER 4: SPIELREGELN
        # AdvancedPromptSystem 'rules'-Layer ergänzt game_rules (falls vorhanden)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        rules_block = ""
        if hasattr(self, 'game_rules') and self.game_rules:
            rules_block = f"## SPIELREGELN (ABSOLUT EINZUHALTEN)\n{self.game_rules}"

        # ✅ FIX: AdvancedPromptSystem 'rules'-Layer zusätzlich einbinden
        if hasattr(self, 'advanced_prompt_system') and self.advanced_prompt_system:
            try:
                aps_rules = self.advanced_prompt_system.layers.get('rules', '').strip()
                if aps_rules and aps_rules not in rules_block:
                    rules_block = rules_block + "\n\n" + aps_rules if rules_block else aps_rules
                    print(f"✅ AdvancedPromptSystem: rules-Layer zu rules_block hinzugefügt")
            except Exception as e:
                print(f"⚠️ AdvancedPromptSystem rules-Layer Fehler: {e}")

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # LAYER 5: FORMAT & VERHALTEN
        # AdvancedPromptSystem 'formatting'-Layer ergänzt format_block
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        format_block = f"""## ANTWORT-FORMAT (IMMER EINHALTEN)
            - Schreibe NUR als {character_name}, nie als Sukuna oder Erzähler
            - Mix aus Aktion und Sprache: *Aktion* "Dialog"
            - 3–5 Sätze pro Antwort. Nicht zu kurz, nicht zu lang
            - Duze Sukuna immer, auch wenn du höflich bist
            - Beschreibe NIEMALS Sukunas Gedanken, Gefühle, Aussagen, Antworten oder Aktionen
            - Wiederhole NICHT deine letzte Antwort — variiere Sprache und Reaktion
            - Antworte auf das was Sukuna GERADE gesagt hat, nicht auf alte Nachrichten"""

        # ✅ FIX: AdvancedPromptSystem 'formatting'-Layer zusätzlich einbinden
        if hasattr(self, 'advanced_prompt_system') and self.advanced_prompt_system:
            try:
                aps_fmt = self.advanced_prompt_system.layers.get('formatting', '').strip()
                if aps_fmt and aps_fmt not in format_block:
                    format_block = format_block + "\n\n" + aps_fmt
                    print(f"✅ AdvancedPromptSystem: formatting-Layer zu format_block hinzugefügt")
            except Exception as e:
                print(f"⚠️ AdvancedPromptSystem formatting-Layer Fehler: {e}")

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # ZUSAMMENSETZEN
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        all_layers = [
            identity_block,
            world_block,
            state_block,
            rules_block,
            format_block,
        ]

        final_prompt = "\n\n---\n\n".join(block for block in all_layers if block and block.strip())

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # BUDGET-CHECK: Prompt nicht zu lang für 4GB VRAM
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        MAX_PROMPT_CHARS = 4900

        if len(final_prompt) > MAX_PROMPT_CHARS:
            print(f"⚠️ Prompt zu lang ({len(final_prompt)} Zeichen), kürze state_block")
            final_prompt = final_prompt[:MAX_PROMPT_CHARS]

        print(f"📝 System Prompt gebaut: {len(final_prompt)} Zeichen | Charakter: {character_name}")
        return final_prompt


    def _get_character_identity(self, character_name: str) -> str:

        # Hauptcharaktere
        identities = {
            "tsunade": """## DU BIST TSUNADE SENJU
    Fünfte Hokage von Konoha. Legendäre Sannin. Medizinische Meisterin.
    Persönlichkeit: Direkt, autoritär, aber tief fürsorglich. Kann hart wirken, ist aber zutiefst loyal.
    Sprache: Kurz, bestimmt, gelegentlich sarkastisch. Kein unnötiges Gerede.
    Du trägst Verantwortung für Sukuna — nicht als Freundin, sondern als Mentorin und Beschützerin.""",

            "sukuna": """## KONTEXT: SUKUNA (SPIELER-CHARAKTER)
    Sukuna ist der SPIELER. Schreibe NIEMALS seine Gedanken, Gefühle, Antworten oder Aktionen.
    Warte immer auf seine Eingabe.""",
        }

        return identities.get(character_name.lower(), f"""## DU BIST {character_name.upper()}
    Sei authentisch als dieser Charakter. Zeige seine typische Persönlichkeit, Sprache und Eigenheiten.
    Duze Sukuna immer. Beschreibe nie Sukunas Gedanken oder Aktionen.""")

    def _get_encounter_character_identity(self, character_name: str) -> str:
        """Identitäts-Block für Encounter-NPCs — nutzt dein bestehendes Characters-Modul"""
        try:
            from moduls.characters import get_character_info
            char_info = get_character_info(character_name.lower())
            if char_info:
                return f"""## DU BIST {character_name.upper()}
    {char_info.get('description', '')}
    Persönlichkeit: {char_info.get('personality', 'Authentisch und charaktertypisch')}
    Sprechweise: {char_info.get('speech_style', 'Natürlich und charakteristisch')}
    Duze Sukuna. Beschreibe nie Sukunas Gedanken oder Aktionen."""
        except Exception as e:
            print(f"⚠️ Character Info Fehler für {character_name}: {e}")

        # Fallback
        return f"""## DU BIST {character_name.upper()}
    Bleibe authentisch als {character_name}. Zeige typische Persönlichkeit und Sprache.
    Duze Sukuna. Beschreibe nie Sukunas Gedanken oder Aktionen."""

    def _build_encounter_character_prompt(self, current_backstory, conversation_context=""):
        """Baut einen komplett separaten Prompt für Encounter-Charaktere"""
        character_name = self.active_character.title()

        # Prüfe ob erste Begegnung
        encountered = getattr(self, 'encountered_characters', [])
        is_first_meeting = character_name.lower() not in [c.lower() for c in encountered]

        if is_first_meeting:
            meeting_context = (
                f"ERSTKONTAKT: Du siehst Sukuna zum ERSTEN MAL. "
                f"Du kennst ihn NICHT. Er ist dir fremd. "
                f"Reagiere entsprechend deiner Persönlichkeit auf einen Fremden. "
                f"Du weißt NICHTS über ihn außer was du gerade siehst."
            )
        else:
            meeting_context = (
                f"Du kennst Sukuna bereits von einer früheren Begegnung. "
                f"Ihr habt schon miteinander gesprochen."
            )

        # ✨ PERSONALITY INTEGRATION
        personality_prompt = f"Du bist {character_name} - authentisch und natürlich."  # Fallback

        # VOR dem system_prompt f-string:
        recent = self.get_recent_context(4)
        context_string = "\n".join([f"{s}: {m}" for s, m in recent]) if recent else "Kein bisheriges Gespräch"

        try:
            from moduls.enhanced_character_personality_system import EnhancedCharacterPersonalitySystem

            if character_name.lower() == "tsunade":
                if hasattr(self, 'maternal_system') and self.maternal_system is not None:
                    try:
                        personality_system = EnhancedCharacterPersonalitySystem(
                            maternal_system=self.maternal_system
                        )
                        print(f"✅ Maternal System für {character_name} aktiviert")
                    except Exception as e:
                        print(f"❌ Maternal System Test fehlgeschlagen: {e}")
                        personality_system = EnhancedCharacterPersonalitySystem(maternal_system=None)
                else:
                    print(f"⚠️ Maternal System nicht verfügbar für {character_name}")
                    personality_system = EnhancedCharacterPersonalitySystem(maternal_system=None)
            else:
                personality_system = EnhancedCharacterPersonalitySystem(maternal_system=None)

            # ✅ FIX: personality_prompt IMMER setzen
            personality_prompt = personality_system.get_personality_prompt(character_name)
            print("✅ ERWEITERTES CHARAKTEREIGENSCHAFTEN-SYSTEM GELADEN!")


        except Exception as e:
            print(f"⚠️ Encounter Personality Error: {e}")
            # Fallback bleibt von oben


        encounter_prompt = f"""CHARAKTER IDENTITÄT: {character_name}
        DEIN NAME: {character_name}  
        DU BIST: {character_name}

        ## SPEZIELLE PERSÖNLICHKEIT:
        {personality_prompt}

        ## SZENE:
        {meeting_context}
        ORT: {self.current_location}
        AKTUELLE ZEIT: {self._get_current_time_context()}

        ##
        Variiere deine Antworten auch bei ähnlichen Situationen!
        BISHERIGES GESPRÄCH (NICHT WIEDERHOLEN!):
        {context_string}
        Deine nächste Antwort MUSS sich inhaltlich und sprachlich vom obigem unterscheiden!

        ## KRITISCHE REGELN:
        1. Sei authentisch als {character_name}, keine generative KI!
        2. Zeige persönliche Eigenschaften und natürliche Reaktionen
        3. Schreibe NIEMALS "*Sukuna*" Aktionen, Gedanken oder Verhalten
        4. Schreibe NUR "*{character_name}*" Aktionen, Gedanken, Verhalten!
        5. Du darfst NICHT Aktionen von Sukuna oder dem User spielen/schreiben
        6. Du antwortest in 3 bis 6 Sätzen mit nonverbalen UND verbalen Text!

        KRITISCHE GAMERULES EINHALTUNG:
        Halte dich AUCH an die Gamerules: {self.game_rules}

        - WARTE auf Sukunas nächste Eingabe!"""

        # ✅ CONVERSATION CONTEXT HINZUFÜGEN (CRITICAL!)
        if conversation_context:
            encounter_prompt += f"\n\n{conversation_context}"
            print(f"✅ Conversation Context hinzugefügt: {len(conversation_context)} Zeichen")
        else:
            print("⚠️ Kein Conversation Context verfügbar")


        return encounter_prompt

    def _update_systems_after_response(self, user_input: str, ai_response: str):
        """Updates die Systeme nach einer AI Response - VEREINFACHT"""

        # Maternal System Update (falls verfügbar)
        if self.maternal_system and self.behavior_engine:
            try:
                # Einfache Maternal Level Updates basierend auf Keywords
                if any(keyword in user_input.lower() for keyword in ['mama', 'hilfe', 'trost', 'umarmung']):
                    self.maternal_system.increase_level(5, "Positive Interaktion")
                elif any(keyword in user_input.lower() for keyword in ['weg', 'allein', 'nicht']):
                    self.maternal_system.increase_level(-2, "Distanzierung")
            except Exception as e:
                print(f"⚠️ Maternal System Update Fehler: {e}")

        # Relationship System Update (falls verfügbar) - FIXED VERSION
        if hasattr(self, 'relationship_system') and self.relationship_system:
            try:
                # Basis Relationship Updates
                if any(keyword in user_input.lower() for keyword in ['danke', 'lieb', 'schön']):
                    # Versuche verschiedene Methoden-Namen
                    if hasattr(self.relationship_system, 'modify_relationship'):
                        self.relationship_system.modify_relationship(self.active_character, 2, "Positive Interaktion")
                    elif hasattr(self.relationship_system, 'change_relationship'):
                        self.relationship_system.change_relationship(self.active_character, 2, "Positive Interaktion")
                    elif hasattr(self.relationship_system, 'update_relationship'):
                        self.relationship_system.update_relationship(self.active_character, 2, "Positive Interaktion")

                elif any(keyword in user_input.lower() for keyword in ['dumm', 'schlecht', 'hasse']):
                    # Versuche verschiedene Methoden-Namen
                    if hasattr(self.relationship_system, 'modify_relationship'):
                        self.relationship_system.modify_relationship(self.active_character, -3, "Negative Interaktion")
                    elif hasattr(self.relationship_system, 'change_relationship'):
                        self.relationship_system.change_relationship(self.active_character, -3, "Negative Interaktion")
                    elif hasattr(self.relationship_system, 'update_relationship'):
                        self.relationship_system.update_relationship(self.active_character, -3, "Negative Interaktion")

            except AttributeError as e:
                print(f"⚠️ Relationship System Methode nicht gefunden: {e}")
            except Exception as e:
                print(f"⚠️ Relationship System Update Fehler: {e}")



    def _get_character_personality(self, character_name):
        """Enhanced Character Personality mit Maternal System Integration"""
        try:
            from moduls.enhanced_character_personality_system import EnhancedCharacterPersonalitySystem

            personality_system = EnhancedCharacterPersonalitySystem(
                maternal_system=self.maternal_system,
                relationship_system=getattr(self, 'relationship_system', None)
            )

            return personality_system.get_personality_prompt(character_name)

        except Exception as e:
            print(f"⚠️ Enhanced Personality System Fehler: {e}")
            return f"Du bist {character_name.title()} - authentisch und natürlich."

    def save_game(self, filepath):
        """Speichert den Spielstand"""
        chat_messages_to_save = getattr(self, 'chat_messages', [])




        save_data = {
            'game_state': self.game_state,
            'active_character': self.active_character,
            'encounter_active': self.encounter_active,
            'current_location': self.current_location,
            'encountered_characters': self.encountered_characters,
            'chat_messages': chat_messages_to_save # 🔧 FIX: Füge chat_messages hinzu
        }

        # Team System Data hinzufügen
        if hasattr(self, 'genin_team_system'):
            save_data['genin_team_system'] = self.genin_team_system.get_save_data()

        # Maternal System State
        if self.maternal_system:
            try:
                save_data['maternal_level'] = self.maternal_system.get_current_level()
                save_data['maternal_history'] = self.maternal_system.level_history
            except:
                pass

        # ✨ RELATIONSHIP SYSTEM STATE
        if hasattr(self, 'relationship_system') and self.relationship_system:
            try:
                # Speichere alle Relationship Daten
                if hasattr(self.relationship_system, 'relationships'):
                    save_data['relationships'] = self.relationship_system.relationships
                elif hasattr(self.relationship_system, 'get_all_relationships'):
                    save_data['relationships'] = self.relationship_system.get_all_relationships()
                else:
                    # Fallback: Game State relationships
                    save_data['relationships'] = self.game_state.get('relationships', {})

                print("✅ Relationship Daten für Speicherung vorbereitet")
            except Exception as e:
                print(f"⚠️ Relationship Save Fehler: {e}")
                # Fallback
                save_data['relationships'] = self.game_state.get('relationships', {})

            # 🔮 SECRET SYSTEM STATE
        if hasattr(self, 'secret_system') and self.secret_system:
            try:
                save_data['secret_system'] = self.secret_system.secret_engine.save_secrets_data()
                print(
                        f"✅ Secret System Daten gespeichert ({len(save_data['secret_system'].get('secrets', {}))} secrets)")
            except Exception as e:
                    print(f"⚠️ Secret System Save Fehler: {e}")

        # 🔧 DEBUG: Zeige was gespeichert wird
        print(f"💾 DEBUG: Speichere {len(save_data.get('chat_messages', []))} chat_messages")

        return safe_json_save(save_data, filepath)

    def load_game(self, filepath):
        """Lädt den Spielstand"""
        data = safe_json_load(filepath)
        if not data:
            return False

        if hasattr(self, 'genin_team_system') and 'genin_team_system' in data:
            self.genin_team_system.load_save_data(data['genin_team_system'])

        try:
            self.game_state = data.get('game_state', self.game_state)
            self.active_character = data.get('active_character', 'tsunade')
            self.encounter_active = data.get('encounter_active', False)
            self.current_location = data.get('current_location', 'tsunades_haus')
            self.encountered_characters = data.get('encountered_characters', [])

            # 🔧 FIX: Lade chat_messages
            if 'chat_messages' in data:
                self.chat_messages = data.get('chat_messages', [])
                print(f"💾 DEBUG: {len(self.chat_messages)} chat_messages geladen")
            else:
                self.chat_messages = []
                print("💾 DEBUG: Keine chat_messages im Save gefunden")

            # Restore Maternal System
            if self.maternal_system and 'maternal_level' in data:
                self.maternal_system.current_level = data['maternal_level']
                if 'maternal_history' in data:
                    self.maternal_system.level_history = data['maternal_history']

                # 🔮 SECRET SYSTEM LOAD
            if 'secret_system' in data and hasattr(self, 'secret_system'):
                try:
                    self.secret_system.secret_engine.load_secrets_data(data['secret_system'])
                    secrets_count = len(data['secret_system'].get('secrets', {}))
                    print(f"✅ Secret System wiederhergestellt ({secrets_count} secrets)")
                except Exception as e:
                    print(f"⚠️ Secret System Load Fehler: {e}")

            # ✨ RESTORE RELATIONSHIP SYSTEM
            if 'relationships' in data and hasattr(self, 'relationship_system') and self.relationship_system:
                try:
                    relationships_data = data['relationships']

                    # Restore zu MinimalRelationshipSystem
                    if hasattr(self.relationship_system, 'relationships'):
                        self.relationship_system.relationships.update(relationships_data)

                    # Update auch game_state
                    if 'relationships' not in self.game_state:
                        self.game_state['relationships'] = {}
                    self.game_state['relationships'].update(relationships_data)

                    print("✅ Relationship Daten geladen")
                except Exception as e:
                    print(f"⚠️ Relationship Load Fehler: {e}")

            # Fallback: Relationship Data aus game_state
            elif 'relationships' in data:
                try:
                    self.game_state['relationships'] = data['relationships']
                    print("✅ Relationship Daten in game_state geladen")
                except Exception as e:
                    print(f"⚠️ Relationship Fallback Fehler: {e}")

            print("✅ Spielstand geladen")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Laden: {e}")
            return False



    def autosave(self):
        """Automatisches Speichern mit allen Systemen"""
        try:
            success = self.save_game(AUTOSAVE_PATH)
            if success:
                print("✅ Autosave erfolgreich (inkl. Relationships)")
            return success
        except Exception as e:
            print(f"❌ Autosave Fehler: {e}")
            return False

    def _format_maternal_behavior_for_prompt(self, category_data):
        """Formatiert die echten Maternal System Daten für den LLM-Prompt"""
        try:
            behavior_text = ""

            # Zeige die Kategorie deutlich
            category = category_data.get('category', 'Normal')
            behavior_text += f"KATEGORIE: {category}\n\n"

            # Hole private Verhaltensweisen (die wichtigsten für Level 500)
            if 'privat_verhalten' in category_data:
                private_behaviors = category_data['privat_verhalten']
                if private_behaviors:
                    behavior_text += "EXTREM WICHTIGE VERHALTENSWEISEN (zuhause mit Sukuna):\n"
                    for i, behavior in enumerate(private_behaviors[:7]):  # Top 7 wichtigste
                        behavior_text += f"• {behavior}\n"

            # Hole private Dialoge (sehr wichtig für den Ton!)
            if 'dialoge' in category_data:
                dialogs = category_data['dialoge']
                if 'privat' in dialogs and dialogs['privat']:
                    behavior_text += f"\nSO MUSST DU SPRECHEN (private Dialoge):\n"
                    for dialog in dialogs['privat']:  # ALLE Dialoge zeigen
                        behavior_text += f'• "{dialog}"\n'

            # Zusätzliche Betonung für hohe Level
            level_range = category_data.get('range', (0, 100))
            if level_range[0] >= 400:  # Für hohe Level
                behavior_text += f"\n⚠️ KRITISCH: Du bist auf Stufe {level_range[0]}-{level_range[1]}! Das bedeutet EXTREM mütterliches Verhalten!\n"
                behavior_text += "Du MUSST die oben genannten Verhaltensweisen und Dialoge verwenden!\n"
                behavior_text += "Sei NICHT normal - sei überfürsorglich und obsessiv mütterlich!"

            return behavior_text if behavior_text else "Standard mütterliches Verhalten"

        except Exception as e:
            print(f"⚠️ Maternal Behavior Format Fehler: {e}")
            return "Standard mütterliches Verhalten"



def main():
    """
    Hauptfunktion zum Starten der Anwendung - VEREINFACHT
    """
    try:
        # 1. DATENMODELL erstellen
        print("🚀 Initialisiere VEREINFACHTES Spielsystem...")
        data = GameData()

        # 2. GUI erstellen und mit Datenmodell verbinden
        print("🎨 Starte Benutzeroberfläche...")
        app = RPG_GUI(data)

        data.gui = app

        # 3. ANWENDUNG STARTEN
        print("🎮 Anwendung bereit - VEREINFACHTE VERSION!")
        app.mainloop()

    except Exception as e:
        print(f"💥 KRITISCHER FEHLER beim Starten der Anwendung: {e}")
        messagebox.showerror("Kritischer Fehler",
                             f"Die Anwendung konnte nicht gestartet werden:\n\n{e}")


if __name__ == "__main__":
    main()


