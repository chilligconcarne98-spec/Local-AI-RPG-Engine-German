# rpg_gui.py - CLEANED VERSION
# -*- coding: utf-8 -*-
"""
GUI-Komponente für das Chat RPG - VEREINFACHT
Entfernt redundante Enhancement-Systeme für bessere Performance
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk

import re

# ✅ CORE SYSTEMS ONLY - Nur die wichtigsten Imports

import backstory  # Added for backstory display

try:
    # Maternal System
    import moduls.maternal_system as maternal_system
    import moduls.maternal_behavior_system as maternal_behavior_system
    from moduls.maternal_system import EnhancedMaternalSystem
    from moduls.maternal_behavior_system import MaternalBehaviorEngine

    print("✅ Maternal System Module geladen")
except ImportError as e:
    print(f"⚠️ Maternal System Import Fehler: {e}")

try:
    from moduls.advanced_prompt_system import *

    print("✅ Erweitertes Prompt System geladen")
except ImportError as e:
    print(f"⚠️ Erweitertes Prompt System Import Fehler: {e}")

try:
    from moduls.environment_system import EnvironmentSystem, create_environment_system
    from moduls.environment_integration import setup_safe_enhanced_encounter_system

    print("✅ Environment System Module geladen")
except ImportError as e:
    print(f"⚠️ Environment System Import Fehler: {e}")

try:
    from moduls.encounter_system import SimpleEncounterSystem

    print("✅ Encounter System Module geladen")
except ImportError as e:
    print(f"⚠️ Encounter System Import Fehler: {e}")

# RELATIONSHIP SYSTEM - SIMPLIFIED
try:
    from moduls.relationship_integration import setup_relationship_system_for_gui

    RELATIONSHIP_SYSTEM_AVAILABLE = True
    print("✅ Relationship System Module verfügbar!")
except ImportError as e:
    print(f"⚠️ Relationship System nicht verfügbar: {e}")
    RELATIONSHIP_SYSTEM_AVAILABLE = False

# ✨ ADVANCED RELATIONSHIP TRIGGERS
try:
    from moduls.advanced_relationship_triggers import AdvancedRelationshipTriggers

    ADVANCED_TRIGGERS_AVAILABLE = True
    print("✅ Advanced Relationship Triggers verfügbar!")
except ImportError as e:
    ADVANCED_TRIGGERS_AVAILABLE = False
    print(f"⚠️ Advanced Relationship Triggers Import Fehler: {e}")



    # Fallback: Minimaler Trigger-System
    class SimpleRelationshipTriggers:
        def __init__(self):
            pass

        def analyze_relationship_impact(self, message, character):
            # Basic keyword analysis
            message_lower = message.lower()

            # Positive keywords
            if any(word in message_lower for word in ['danke', 'toll', 'super', 'lieb', 'schön']):
                return +3, ['Positive Interaktion']
            # Negative keywords
            elif any(word in message_lower for word in ['dumm', 'schlecht', 'hasse', 'nervig']):
                return -5, ['Negative Interaktion']

            return 0, []


    AdvancedRelationshipTriggers = SimpleRelationshipTriggers


class RPG_GUI(ctk.CTk):
    """Hauptfenster der RPG-Anwendung - VEREINFACHT."""

    def __init__(self, data_model):
        super().__init__()

        self.data = data_model
        # Charakterporträts
        # from direct_portrait_fix import add_real_images_to_rpg_gui
        # add_real_images_to_rpg_gui(self)
        print("🔍 DEBUG: Versuche Character Portraits System zu importieren...")
        try:
            from moduls.simple_portraits_fix import add_simple_portraits_to_relationships
            add_simple_portraits_to_relationships(self)
            self.character_portraits = True
            print("✅ Simple Portraits System aktiviert!")
        except Exception as e:
            print(f"⚠️ Simple Portraits Fehler: {e}")
            self.character_portraits = False

        # Setze GUI-Instanz im Datenmodell (für Callbacks)
        if hasattr(self.data, 'maternal_system') and self.data.maternal_system:
            self.data.maternal_system.gui = self
        if hasattr(self.data, 'behavior_engine') and self.data.behavior_engine:
            self.data.behavior_engine.gui = self
        if hasattr(self.data, 'encounter_system') and self.data.encounter_system:
            self.data.encounter_system.gui = self

        self.title("🎮 Chat RPG - Sukuna & Tsunade (✨ OPTIMIERT)")
        self.geometry("1100x700")
        self.minsize(800, 500)

        # ✨ Farben für Nachrichten definieren
        self.colors = {
            "success": "#28a745",
            "danger": "#dc3545",
            "warning": "#ffc107",
            "info": "#17a2b8",
            "relationship_accent": "#e91e63",
            "maternal": "#ff69b4",
            "character": "#6f42c1",
            "system": "#6c757d"
        }

        # Erstelle die Menüleiste
        self.create_menubar()

        # Initialisiere die GUI-Komponenten
        self.setup_start_screen()
        self.setup_game_interface()



        # ✨ SIMPLIFIED - Relationship System Setup
        self.setup_simplified_relationship_system()

        # ✅ INITIAL STATUS TAB LOAD
        try:
            # Kurze Verzögerung um sicherzustellen dass alle Tabs ready sind
            self.after(100, self.update_status_tab)
            print("🔄 Initial Status Tab Load geplant")
        except Exception as e:
            print(f"⚠️ Initial Status Load Fehler: {e}")

        # ✨ Advanced Relationship Triggers Setup
        try:
            self.relationship_triggers = AdvancedRelationshipTriggers()
            print("✅ Advanced Relationship Triggers aktiviert!")
        except Exception as e:
            print(f"⚠️ Relationship Triggers Fehler: {e}")
            self.relationship_triggers = None

        # Umgebung
        if hasattr(self.data, 'enhanced_encounter') and self.data.enhanced_encounter:
            print("✅ Environment System in GUI verfügbar!")
            self.data.current_location = 'tsunades_haus'
        else:
            print("✅ Environment System bereit")

        #Erweiterte Prompts
        if hasattr(self.data, '_build_enhanced_system_prompt'):
            print("✅ Enhanced System Prompt verfügbar")
        else:
            print("⚠️ Enhanced System Prompt nicht verfügbar")

        # Registriere das Window-Close-Event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Speichert alle Nachrichten
        self.chat_messages = []


        # Zeige das Startmenü - GANZ ZUM SCHLUSS
        try:
            self.show_start_screen()
        except Exception as e:
            print(f"❌ Fehler beim Zeigen des Startmenüs: {e}")
            # Fallback: Zeige direkt das Spiel
            self.show_game_interface()

    def setup_simplified_relationship_system(self):
        """Initialisiert ein VEREINFACHTES Relationship System"""
        print("🚀 Initialisiere VEREINFACHTES Relationship System...")

        try:
            if RELATIONSHIP_SYSTEM_AVAILABLE:
                # FALLBACK: Erstelle ein Mini-Relationship-System falls das echte fehlschlägt
                class MinimalRelationshipSystem:
                    def __init__(self):
                        self.relationships = {
                            'tsunade': {'level': 0, 'titel': 'Neutral', 'gruppe': 'main'},
                            'sukuna': {'level': 0, 'titel': 'Neutral', 'gruppe': 'main'}
                        }

                    def get_relationship_info(self, character):
                        char_lower = str(character).lower()
                        return self.relationships.get(char_lower, {'level': 0, 'titel': 'Unbekannt'})

                    def modify_relationship(self, character, amount, reason):
                        char_lower = str(character).lower()
                        if char_lower in self.relationships:
                            old_level = self.relationships[char_lower]['level']
                            new_level = old_level + amount
                            self.relationships[char_lower]['level'] = new_level
                            print(f"💝 {character.title()}: {old_level} → {new_level} ({amount:+d}) - {reason}")
                            return True
                        return False

                    def get_relationship_summary_for_prompt(self, character):
                        """Gibt Relationship Summary für Prompt zurück"""
                        try:
                            info = self.get_relationship_info(character)
                            level = info.get('level', 0)
                            return f"Relationship Level mit {character.title()}: {level}"
                        except:
                            return f"Relationship mit {character.title()}: Unbekannt"

                # Versuche das echte System zuerst
                try:
                    from moduls.relationship_system import RelationshipSystem

                    # Stelle sicher, dass game_state korrekt formatiert ist
                    if isinstance(self.data.game_state, dict) and 'relationships' in self.data.game_state:
                        # Überprüfe und korrigiere die Relationship-Datenstruktur
                        relationships = self.data.game_state['relationships']

                        # Stelle sicher, dass alle Einträge Dicts sind
                        for char_name, char_data in relationships.items():
                            if not isinstance(char_data, dict):
                                relationships[char_name] = {'level': 0, 'events': []}
                            elif 'level' not in char_data:
                                char_data['level'] = 0
                            elif not isinstance(char_data['level'], (int, float)):
                                char_data['level'] = 0

                    self.data.relationship_system = RelationshipSystem(
                        game_state=self.data.game_state,
                        gui=self,
                        maternal_system=self.data.maternal_system if hasattr(self.data, 'maternal_system') else None
                    )

                    print("✅ Echtes Relationship System initialisiert!")

                except Exception as real_error:
                    print(f"⚠️ Echtes Relationship System Fehler: {real_error}")
                    print("🔄 Verwende Minimal-Fallback...")

                    # Fallback auf Minimal-System
                    self.data.relationship_system = MinimalRelationshipSystem()
                    print("✅ Minimal Relationship System aktiviert!")

                # Test: Lade Tsunade Info - ROBUSTE VERSION
                try:
                    test_info = self.data.relationship_system.get_relationship_info('tsunade')
                    print(f"✅ Test Tsunade Level: {test_info.get('level', 0)}")
                except Exception as test_error:
                    print(f"⚠️ Relationship Test Fehler: {test_error}")

                # 🔄 FIX: Refresh Relationship Display nach System-Initialisierung
                print("🔄 Refreshing Relationship Display nach System-Setup...")
                try:
                    if hasattr(self, 'refresh_relationships_display'):
                        self.refresh_relationships_display()
                        print("✅ Relationship Display nach System-Setup refreshed!")
                except Exception as e:
                    print(f"⚠️ Relationship Refresh Fehler: {e}")

                # Einfacher /relationship Command
                self.add_simplified_relationship_command()

            else:
                print("⚠️ Relationship System nicht verfügbar")
                self.data.relationship_system = None

        except Exception as e:
            print(f"❌ Relationship System Setup Fehler: {e}")
            # Setze fallback
            self.data.relationship_system = None

    def add_simplified_relationship_command(self):
        """Fügt einen VEREINFACHTEN /relationship Command hinzu"""
        # Das wird in der send_message Methode behandelt
        pass

    def create_menubar(self):
        """Erstellt die Menüleiste"""
        # Placeholder für Menüfunktionen
        pass

    def setup_start_screen(self):
        """Erstellt das Startmenü."""
        self.start_frame = ctk.CTkFrame(self)

        # Titel
        ctk.CTkLabel(self.start_frame, text="🎮 Chat RPG - Sukuna & Tsunade",
                     font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(50, 30))

        # Beschreibung
        description = """
Ein textbasiertes RPG-Erlebnis im Naruto-Universum.

Du spielst als Sukuna Jinro, ein 13-jähriger Junge, der bei Tsunade lebt.
Deine Entscheidungen formen eure Beziehung und das Spiel.

🎭 OPTIMIERTE VERSION: Weniger Enhancement-Konflikte!
💖 Maternal System zeigt Level-Änderungen live im Chat!
✨ ACTION DETECTION: Schreibe "*umarmt*" und das Level steigt!
💕 RELATIONSHIP SYSTEM: Vereinfacht aber funktional!
🗺️ LOCATION-BASED ENCOUNTERS: Besuche verschiedene Orte!

Viel Spaß beim Spielen!
        """

        ctk.CTkLabel(self.start_frame, text=description, justify="left",
                     font=ctk.CTkFont(size=14)).pack(pady=20, padx=50)

        # Buttons
        button_frame = ctk.CTkFrame(self.start_frame)
        button_frame.pack(pady=30)

        ctk.CTkButton(button_frame, text="🎯 Neues Spiel", command=self.start_new_game_flow,
                      font=ctk.CTkFont(size=16), width=200, height=40).pack(pady=10)

        ctk.CTkButton(button_frame, text="📁 Spiel laden", command=self.load_game_flow,
                      font=ctk.CTkFont(size=16), width=200, height=40).pack(pady=10)

        ctk.CTkButton(button_frame, text="❌ Beenden", command=self.quit,
                      font=ctk.CTkFont(size=16), width=200, height=40).pack(pady=10)

    def setup_game_interface(self):
        """Erstellt die Haupt-Spieloberfläche."""
        self.game_frame = ctk.CTkFrame(self)

        # --- LINKE SEITE: CHAT-BEREICH ---
        chat_frame = ctk.CTkFrame(self.game_frame)
        chat_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=(0, 10))

        # Chat-Titel
        self.chat_title = ctk.CTkLabel(chat_frame, text="💬 Chat mit Tsunade",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.chat_title.pack(pady=(10, 5), padx=10)

        # ✨ NEU: Location Image System hinzufügen
        self.location_system = LocationImageSystem(chat_frame, self.data)

        # Chat-Display (jetzt unter dem Location Image)
        self.chat_display = ctk.CTkTextbox(chat_frame, state="disabled",
                                           font=ctk.CTkFont(family="Segoe UI", size=12))
        self.chat_display.pack(fill=ctk.BOTH, expand=True, padx=10, pady=(5, 10))



        # Bind resize events
        self.chat_display.bind('<Configure>', lambda e: None)

        # Input-Bereich
        input_frame = ctk.CTkFrame(chat_frame)
        input_frame.pack(fill=ctk.X, padx=10, pady=(0, 10))

        self.user_input = ctk.CTkEntry(input_frame, placeholder_text="Schreibe deine Nachricht...",
                                       font=ctk.CTkFont(size=12))
        self.user_input.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(0, 10))
        self.user_input.bind('<Return>', self.handle_user_input)

        self.send_button = ctk.CTkButton(input_frame, text="📤 Senden", width=100, command=self.handle_user_input)
        self.send_button.pack(side="right", padx=(0, 15), pady=15)

        # ✅ NEU: Regenerate Button
        self.regenerate_button = ctk.CTkButton(
            input_frame,
            text="🔄 Neu",
            width=60,
            fg_color="#2d4a2d",  # Dunkles Grün
            hover_color="#3d6b3d",
            text_color="white",
            font=("Segoe UI", 11),
            corner_radius=8,
            command=self.regenerate_last_response,
            state="disabled"  # Start deaktiviert bis erste Antwort da
        )
        self.regenerate_button.pack(side="right", padx=(0, 5), pady=15)

        # --- RECHTE SEITE: TAB SYSTEM ---
        self.setup_simple_tabs()

    def setup_simple_tabs(self):
        """Tab-System anstatt Popup-Fenster"""

        # Tab-Container
        self.tab_view = ctk.CTkTabview(self.game_frame, width=350)
        self.tab_view.pack(side=ctk.RIGHT, fill=ctk.Y, padx=(10, 0))

        # Tabs erstellen
        self.tab_view.add("🎮 Aktionen")
        self.tab_view.add("🗺️ Locations")
        self.tab_view.add("📊 Status")
        self.tab_view.add("💝 Beziehungen")
        self.tab_view.add("📜 Backstory")
        self.tab_view.add("❓ Hilfe")

        # --- AKTIONEN TAB ---
        actions_tab = self.tab_view.tab("🎮 Aktionen")

        # Command-Bereich
        ctk.CTkLabel(actions_tab, text="⚡ Schnell-Befehle",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        command_frame = ctk.CTkScrollableFrame(actions_tab)
        command_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Command-Buttons
        commands = [
            ("🔄 Status anzeigen", "/status"),
            ("🏠 Zurück zu Tsunade", "/return"),
            ("⏰ 1h vorspulen", "/time 1 0"),
            ("🌅 3h vorspulen", "/time 3 0"),
            ("📈 Maternal +10", "/maternal +10"),
            ("📉 Maternal -10", "/maternal -10"),
            ("📁 Spiel speichern", "/save"),
            ("❓ Alle Befehle", "/help")
        ]

        for text, command in commands:
            btn = ctk.CTkButton(command_frame, text=text, width=280,
                                command=lambda cmd=command: self.execute_quick_command(cmd))
            btn.pack(pady=2)

        # --- LOCATIONS TAB ---
        self.setup_locations_tab()

        # --- STATUS TAB ---
        status_tab = self.tab_view.tab("📊 Status")
        self.status_text = ctk.CTkTextbox(status_tab, font=ctk.CTkFont(family="Consolas"), state="disabled")
        self.status_text.pack(fill="both", expand=True, padx=10, pady=10)

        # --- BACKSTORY TAB ---
        backstory_tab = self.tab_view.tab("📜 Backstory")

        # ✨ WICHTIG: Erstelle die backstory_display hier!
        self.backstory_display = ctk.CTkTextbox(backstory_tab, font=ctk.CTkFont(size=12), state="disabled")
        self.backstory_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Zusätzlich erstelle auch backstory_text für die update_backstory_tab Funktion
        self.backstory_text = self.backstory_display

        # --- HILFE TAB ---
        help_tab = self.tab_view.tab("❓ Hilfe")

        help_text = """🎮 VERFÜGBARE BEFEHLE:

🎯 NAVIGATION:
- /help - Diese Hilfe anzeigen
- /status - Aktueller Spielstatus
- /return - Zurück zu Tsunade

🗺️ LOCATIONS & ENCOUNTERS:
- /encounter [ort] - Ort besuchen (z.B. /encounter onsen)
- /locations - Alle verfügbaren Orte anzeigen

📚 BIBLIOTHEKS-SYSTEM:
- /bibliotheken - Liste aller Bibliotheken
- /bibliothek <ort> - Zeige Bücher an einem Ort
- /lesen <buch_id> <kapitel> - Lese ein Kapitel
- /lesestatistik - Deine Lesestatistiken
- /bibliothek_hilfe - Vollständige Bibliotheks-Hilfe

👥 Companion System:
- /companion - Zeigt aktuellen Begleiter-Status
- /suggest - Zeigt verfügbare Begleiter am Ort
- /ask [name] - Fragt Charakter ob er mitkommt
- /accept [name] - Akzeptiert Begleiter-Angebot
- /decline [name] - Lehnt Begleiter ab
- /dismiss - Entlässt aktuellen Begleiter

**ERKLÄRUNG DES COMPANION SYSTEMS***
[Du] /suggest
[System] 👥 VERFÜGBARE BEGLEITER in tsunades_haus:
- Tsunade: 😊 willing (❤️100)
- Shizune: 😐 neutral (❤️25)

[Du] /ask tsunade
[Tsunade] ✅ "Komm, lass uns zusammen gehen. Ich passe auf dich auf."
👥 Tsunade begleitet dich jetzt!

[Du] /encounter dorf_zentrum
[System] 📍 Du besuchst dorf_zentrum.
👥 BEGLEITER: *Tsunade schaut sich beschützend um* 'Interessant hier. Lass uns vorsichtig sein.

[Du] "Mir ist langweilig..."

[Tsunade] "Weißt du was? Lass uns ins Dorfzentrum gehen. Frische Luft wird dir gut tun."

💭 Tsunade möchte dich zu dorf_zentrum begleiten!
**Antworten**: '/accept tsunade' oder '/decline tsunade'
*******---------------**********************************************
-------------------------------------------------------------------
👥 GENIN TEAM SYSTEM (ab Tag 5):
- /team_status - Zeigt aktuellen Team-Status  
- /call_team - Ruft Team zur aktuellen Location
- /team_mission - Zeigt verfügbare Team-Missionen
- /start_mission [mission_id] - Startet eine Mission (z.B. /start_mission first_mission)
- /breakfast - Frühstück-Szene (manuell, für Testing)

🎯 MISSION SYSTEM:
- /team_mission - Zeige verfügbare Missionen
- /start_mission first_mission - Starte Katzen-Mission (D-Rang)
- /start_mission bandit_patrol - Starte Banditen-Mission (C-Rang, nach 1. Mission)

📋 MISSION ABLAUF:
1. Bekomme Team (Tag 5 Event oder /encounter hokage_turm)
2. /team_mission - Siehe verfügbare Missionen
3. Gehe zur richtigen Location (z.B. /encounter dorf_zentrum)
4. /start_mission [id] - Starte Mission
5. Rede mit deinem Team und löse die Mission!

💡 MISSION BEISPIEL:
/encounter dorf_zentrum          # Gehe zur Location
/team_mission                    # Zeigt: "Verschollene Katze finden"  
/start_mission first_mission     # Mission startet!
🐱 *Team versammelt sich, Auftraggeber erscheint*
"Meine Katze Princess ist weg!"  # Mission-Szenario beginnt

🌅 TEAM FORMATION PROCESS:
- Tag 5: Tsunade weckt dich persönlich auf (bei tsunades_haus)
- Frühstück-Szene mit mütterlicher Fürsorge
- Team-Zuteilung im Hokage-Büro (emotional + offiziell)
- Permanente Team-Mechaniken ab Tag 6'''"""

        help_textbox = ctk.CTkTextbox(help_tab, height=400)
        help_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        help_textbox.insert("1.0", help_text)
        help_textbox.configure(state="disabled")

        print("✅ Tab-System vollständig initialisiert")

    def setup_locations_tab(self):
        """Erstellt den Locations-Tab mit allen verfügbaren Orten"""
        locations_tab = self.tab_view.tab("🗺️ Locations")

        # Header
        ctk.CTkLabel(locations_tab, text="🗺️ VERFÜGBARE ORTE",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        # Scrollable Frame für Location-Buttons
        locations_frame = ctk.CTkScrollableFrame(locations_tab)
        locations_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Standard-Locations (falls kein Encounter System verfügbar)
        default_locations = {
            'tsunades_haus': {'name': 'Tsunades Haus', 'description': 'Dein Zuhause'},
            'dorf_zentrum': {'name': 'Dorf Zentrum', 'description': 'Das Herz von Konoha'},
            'training_area': {'name': 'Trainingsgelände', 'description': 'Hier trainieren die Ninja'},
            'onsen': {'name': 'Heiße Quellen', 'description': 'Entspannung pur'},
            'ramen_stand': {'name': 'Ramen Stand', 'description': 'Ichiraku Ramen'},
            'hokage_turm': {'name': 'Hokage Turm', 'description': 'Zentrum der Macht'},
            'academy': {'name': 'Ninja Akademie', 'description': 'Hier lernen angehende Ninja'},
            'wald': {'name': 'Wald von Konoha', 'description': 'Mystischer Waldbereich'},
        }

        # Hole verfügbare Locations vom Encounter System oder verwende Standard
        if hasattr(self.data, 'encounter_system') and self.data.encounter_system and hasattr(self.data.encounter_system,
                                                                                             'locations'):
            locations = self.data.encounter_system.locations
        else:
            locations = default_locations

        for location_key, location_data in locations.items():
            # Location Button mit Name und Beschreibung
            location_name = location_data.get('name', location_key)

            # Frame für jede Location
            loc_frame = ctk.CTkFrame(locations_frame)
            loc_frame.pack(fill="x", padx=5, pady=3)

            # Location Button
            btn_text = f"🏛️ {location_name.split(' - ')[0]}"  # Entferne Command-Teil
            loc_btn = ctk.CTkButton(
                loc_frame,
                text=btn_text,
                width=200,
                command=lambda loc=location_key: self.visit_location(loc)
            )
            loc_btn.pack(side="left", padx=5, pady=5)

            # Info Button
            info_btn = ctk.CTkButton(
                loc_frame,
                text="ℹ️",
                width=30,
                command=lambda loc=location_key: self.show_location_info(loc)
            )
            info_btn.pack(side="right", padx=5, pady=5)

        # Info-Text
        info_text = """💡 TIPPS:
• Klicke auf einen Ort um ihn zu besuchen
• ℹ️ zeigt Infos über den Ort
• Verschiedene Tageszeiten beeinflussen die Begegnungen"""

        info_label = ctk.CTkLabel(locations_tab, text=info_text,
                                  font=ctk.CTkFont(size=10), justify="left")
        info_label.pack(pady=10, padx=10)

        # --- ✨ BEZIEHUNGEN TAB ---
        self.setup_relationships_tab()

    def start_new_game_flow(self):
        """Startet ein neues Spiel"""
        self.display_message("System", "🎮 Willkommen im Chat RPG! Es ist 7 Uhr Morgens und du bist mit Tsunade, deiner Adoptivmutter, in der Küche",
                             "system")
        self.show_game_interface()

    def load_game_flow(self):
        """Lädt ein Spiel"""
        self.load_game_dialog()

    def start_new_game(self):
        """Startet ein neues Spiel"""
        self.start_new_game_flow()

    def execute_quick_command(self, command):
        """Führt einen Schnell-Befehl aus"""
        # Simuliere Eingabe in das Input-Feld
        self.user_input.delete(0, ctk.END)
        self.user_input.insert(0, command)
        # Führe den Befehl aus
        self.handle_user_input()

    def visit_location(self, location_key):
        """Besucht einen Ort und führt Encounter-Check durch"""
        try:
            # Verwende den /encounter Befehl
            command = f"/encounter {location_key}"
            self.user_input.delete(0, ctk.END)
            self.user_input.insert(0, command)
            self.handle_user_input()
        except Exception as e:
            self.display_message("FEHLER", f"Fehler beim Besuchen von {location_key}: {e}", "danger")

    def show_location_info(self, location_key):
        """Zeigt detaillierte Informationen über einen Ort"""
        try:
            # Standard-Locations info
            default_info = {
                'tsunades_haus': "Dein warmes Zuhause bei Tsunade. Hier findest du immer Geborgenheit.",
                'dorf_zentrum': "Das lebendige Herz von Konoha mit vielen Geschäften und Menschen.",
                'training_area': "Hier trainieren die Ninja ihre Fähigkeiten. Perfekt zum Üben.",
                'onsen': "Heiße Quellen zum Entspannen. Sehr beliebt bei den Bewohnern.",
                'ramen_stand': "Ichiraku Ramen - der beste Ramen in ganz Konoha!",
                'hokage_turm': "Das Zentrum der Macht. Hier regiert der Hokage das Dorf.",
                'academy': "Die Ninja-Akademie, wo junge Ninja ihre Ausbildung beginnen.",
                'wald': "Der mystische Wald von Konoha. Gefährlich aber wunderschön."
            }

            info_text = default_info.get(location_key, f"Informationen über {location_key} sind nicht verfügbar.")

            # Zeige Info als Message
            self.display_message("Location Info", f"📍 {location_key.title()}:\n{info_text}", "info")

        except Exception as e:
            self.display_message("FEHLER", f"Fehler beim Anzeigen von Location Info: {e}", "danger")

    def handle_user_input(self, event=None):
        """Handler für Benutzereingaben - RECURSION-SICHER"""

        # 🛡️ PROCESSING GUARD
        if hasattr(self, '_processing_input') and self._processing_input:
            print("⚠️ Input bereits in Verarbeitung - überspringe")
            return "break"

        self._processing_input = True

        try:
            message = self.user_input.get().strip()
            if not message:
                return

            self.user_input.delete(0, ctk.END)

            # Handle special commands
            if message.startswith('/'):
                self.handle_command(message)
            else:
                # Normal message processing
                self.send_message(message)

        except Exception as e:
            print(f"❌ Handle User Input Fehler: {e}")

        finally:
            # 🛡️ GUARD RESET
            self._processing_input = False

    def send_message(self, message=None):
        """Sendet eine Nachricht - PERFEKT KORRIGIERT"""

        # 🛡️ RECURSION BREAKER
        if hasattr(self, '_in_send_message') and self._in_send_message:
            print("🚨 RECURSION VERHINDERT! send_message bereits aktiv.")
            return

        self._in_send_message = True
        ai_response = "[SYSTEM] Fallback-Antwort - LLM nicht verfügbar"

        try:
            # Message holen  ← HIER: nur 8 Leerzeichen, nicht 11
            if message is None:
                message = self.user_input.get().strip()
                if not message:
                    return
                self.user_input.delete(0, ctk.END)

            # ✅ AUSSERHALB des if-Blocks
            self.last_user_message = message
            if hasattr(self, 'regenerate_button'):
                self.regenerate_button.configure(state="normal")

            # ✅ Beim Regenerieren nicht nochmal anzeigen
            if not getattr(self, '_is_regenerating', False):
                self.display_message("Du", message, "user")

            # 🆕 AUTO TIME ADVANCE - MESSAGE COUNTER
            try:
                if hasattr(self, 'data') and self.data and hasattr(self.data, 'increment_message_counter'):
                    new_time = self.data.increment_message_counter()
                    if new_time:  # Zeit wurde advanced
                        self.display_message("Time", f"⏰ Zeit vergeht... {new_time}", "info")

                        # 🆕 CHECK FOR PENDING EVENTS
                        if hasattr(self.data, 'pending_event'):
                            event = self.data.pending_event
                            if event['type'] == 'hokage_summon':
                                # 🌅 PERSÖNLICHE WAKEUP-SZENE (nur wenn zuhause)
                                if self.data.current_location == 'tsunades_haus':
                                    self.display_message("MORNING WAKEUP", event['message'], "success")
                                else:
                                    self.display_message("HOKAGE SUMMON", event['message'], "warning")
                                delattr(self.data, 'pending_event')  # Event nur einmal zeigen

            except Exception as e:
                print(f"⚠️ Auto Time Advance Fehler: {e}")

            # 🕐 LOADING MESSAGE
            self.display_message("System",
                                 "🤖 Antwort wird generiert... (20-30 Sekunden)",
                                 "info")
            self.update()

            # Process triggers (MIT RECURSION SCHUTZ)
            try:
                if not hasattr(self, '_processing_triggers') or not self._processing_triggers:
                    self._processing_triggers = True
                    try:
                        self.process_message_triggers(message)
                    finally:
                        self._processing_triggers = False
            except Exception as e:
                print(f"⚠️ Trigger-Verarbeitung Fehler: {e}")
                if hasattr(self, '_processing_triggers'):
                    self._processing_triggers = False

            # 🤖 Get AI response (KORREKTE EINRÜCKUNG & LOGIK)
            try:
                if hasattr(self, 'data') and self.data and hasattr(self.data, 'get_llm_response'):
                    if not hasattr(self, '_in_get_llm_response') or not self._in_get_llm_response:
                        self._in_get_llm_response = True
                        try:
                            print("🤖 Calling get_llm_response...")
                            ai_response = self.data.get_llm_response(message)
                            print(f"✅ AI Response erhalten: {ai_response[:100]}...")
                        finally:
                            self._in_get_llm_response = False
                    else:
                        print("🚨 LLM Recursion Guard ausgelöst")
                        ai_response = "[SYSTEM] LLM Recursion verhindert. Versuche /help"
                else:
                    print("❌ get_llm_response nicht verfügbar")
                    ai_response = "[SYSTEM] LLM-System nicht verfügbar. Versuche Commands wie /help"

            except RecursionError as e:
                print(f"🚨 RECURSION ERROR: {e}")
                ai_response = "[SYSTEM] Recursion-Fehler verhindert. Versuche /help"

            except Exception as e:
                print(f"❌ LLM Fehler: {e}")
                try:
                    ai_response = self._generate_fallback_response(message)
                except:
                    ai_response = "[SYSTEM] LLM temporär nicht verfügbar. Versuche /help"

            # 🗑️ ERSETZE LOADING MESSAGE MIT ECHTER ANTWORT
            try:
                self.replace_loading_message_with_response(ai_response)
            except Exception as e:
                print(f"❌ Replace Loading Message Fehler: {e}")
                # Fallback: Normale display_message
                try:
                    character_name = "System"
                    if (hasattr(self, 'data') and self.data and
                            hasattr(self.data, 'active_character') and self.data.active_character):
                        character_name = self.data.active_character.title()
                    self.display_message(character_name, ai_response, "character")
                except Exception as e2:
                    print(f"❌ Fallback Display Fehler: {e2}")
                    self.display_message("System", ai_response, "info")

            # 🔄 SYSTEM UPDATES
            try:
                if not hasattr(self, '_updating_systems') or not self._updating_systems:
                    self._updating_systems = True
                    try:
                        self.update_maternal_display()
                        self.update_relationship_display()
                        if hasattr(self, 'data') and self.data and hasattr(self.data, 'autosave'):
                            if hasattr(self, 'chat_messages'):
                                self.data.chat_messages = self.chat_messages.copy()
                            self.data.autosave()
                    finally:
                        self._updating_systems = False
            except Exception as e:
                print(f"⚠️ System Updates Fehler: {e}")
                if hasattr(self, '_updating_systems'):
                    self._updating_systems = False

        except Exception as e:
            print(f"❌ Unerwarteter Fehler in send_message: {e}")
            try:
                self.display_message("System",
                                     f"[FEHLER] Unerwartetes Problem: {str(e)[:100]}",
                                     "danger")
            except:
                print("Konnte Fehlermeldung nicht anzeigen")

        finally:
            # 🛡️ FLAG RESET (IMMER!)
            self._in_send_message = False

            # Reset andere Guards
            if hasattr(self, '_in_get_llm_response'):
                self._in_get_llm_response = False
            if hasattr(self, '_processing_triggers'):
                self._processing_triggers = False
            if hasattr(self, '_updating_systems'):
                self._updating_systems = False

    def regenerate_last_response(self):
        """🔄 Generiert die letzte AI-Antwort neu"""

        if not hasattr(self, 'last_user_message') or not self.last_user_message:
            print("⚠️ Keine letzte User-Nachricht gespeichert")
            return

        print(f"🔄 Regeneriere Antwort für: {self.last_user_message[:50]}...")

        # 1. Letzte AI-Antwort aus chat_messages entfernen
        if hasattr(self, 'chat_messages') and self.chat_messages:
            for i in range(len(self.chat_messages) - 1, -1, -1):
                sender, _ = self.chat_messages[i]
                character_name = self.data.active_character.title() if self.data else "Tsunade"
                if sender == character_name:
                    self.chat_messages.pop(i)
                    print(f"✅ Letzte {character_name}-Antwort aus History entfernt")
                    break

        # 2. Letzte AI-Antwort aus dem Display entfernen
        self._remove_last_ai_message_from_display()

        # 3. Button während Generierung deaktivieren
        self.regenerate_button.configure(state="disabled", text="⏳")
        self._is_regenerating = True

        # 4. Neu generieren mit gleicher Nachricht
        import threading
        def regenerate_thread():
            try:
                self.send_message(self.last_user_message)
            finally:
                # Button wieder aktivieren
                self._is_regenerating = False
                self.after(100, lambda: self.regenerate_button.configure(
                    state="normal", text="🔄 Neu"
                ))

        thread = threading.Thread(target=regenerate_thread, daemon=True)
        thread.start()

    def _remove_last_ai_message_from_display(self):
        """Entfernt die letzte AI-Nachricht aus dem Chat-Display"""
        try:
            self.chat_display.configure(state="normal")

            character_name = self.data.active_character.title() if self.data else "Tsunade"

            # Hole gesamten Text
            content = self.chat_display.get("1.0", "end-1c")
            lines = content.split("\n")

            # Suche letzte AI-Nachricht rückwärts
            last_char_line = -1
            for i in range(len(lines) - 1, -1, -1):
                if f"{character_name}:" in lines[i] or f"[{character_name}]" in lines[i]:
                    last_char_line = i
                    break

            if last_char_line >= 0:
                # Behalte alles VOR der letzten AI-Antwort
                new_content = "\n".join(lines[:last_char_line])
                self.chat_display.delete("1.0", "end")
                if new_content.strip():
                    self.chat_display.insert("1.0", new_content)
                print(f"✅ Letzte {character_name}-Antwort aus Display entfernt")

            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")

        except Exception as e:
            print(f"⚠️ Remove Last Message Fehler: {e}")

    def replace_loading_message_with_response(self, ai_response):
        """SIMPLESTE VERSION: Keine System-Updates, nur Chat-Replace"""

        try:
            character_name = "System"
            if (hasattr(self, 'data') and self.data and
                    hasattr(self.data, 'active_character') and self.data.active_character):
                character_name = self.data.active_character.title()

            cleaned_response = self.clean_message_formatting(ai_response)

            # Suche Loading Message im chat_messages Array
            if hasattr(self, 'chat_messages') and self.chat_messages:
                for i in range(len(self.chat_messages) - 1, -1, -1):  # Rückwärts suchen
                    sender, message = self.chat_messages[i]
                    if sender == "System" and "🤖 Antwort wird generiert" in message:
                        # Ersetze Loading Message
                        self.chat_messages[i] = (character_name, cleaned_response)

                        # Nur Chat Display refresh - KEINE ANDEREN UPDATES!
                        self.chat_display.configure(state="normal")
                        self.chat_display.delete("1.0", "end")

                        # Alle Messages neu hinzufügen
                        for s, m in self.chat_messages:
                            import datetime
                            timestamp = datetime.datetime.now().strftime("%H:%M")
                            # Messages sind bereits gereinigt, nur normale Formatierung
                            formatted_message = f"[{timestamp}] {s}: {m}\n\n"
                            self.chat_display.insert(ctk.END, formatted_message)

                        self.chat_display.see(ctk.END)
                        self.chat_display.configure(state="disabled")

                        print("✅ Loading Message ersetzt (mit gereinigter Formatierung)")
                        return True

            # Fallback: Normale display_message
            print("💡 Loading Message nicht gefunden")
            self.display_message(character_name, cleaned_response, "character")
            return False

        except Exception as e:
            print(f"❌ Loading Replace Fehler: {e}")
            try:
                cleaned_response = self.clean_message_formatting(ai_response)
                self.display_message("System", cleaned_response, "info")
            except:
                print("❌ Fallback fehlgeschlagen!")
            return False

    def _schedule_post_message_updates(self):
        """Plant System-Updates für später ein (verhindert Recursion)"""
        try:
            # Updates mit Delay ausführen um Recursion zu vermeiden
            self.after(100, self._execute_delayed_updates)  # 100ms später
        except Exception as e:
            print(f"⚠️ Update Scheduling Fehler: {e}")

    def _execute_delayed_updates(self):
        """Führt System-Updates mit Delay aus"""
        try:
            # 🛡️ Prüfe ob send_message noch aktiv ist
            if hasattr(self, '_in_send_message') and self._in_send_message:
                # Versuche später nochmal
                self.after(100, self._execute_delayed_updates)
                return

            # Führe Updates aus
            try:
                self.update_maternal_display()
            except Exception as e:
                print(f"⚠️ Delayed Maternal Update Fehler: {e}")

            try:
                self.update_relationship_display()
            except Exception as e:
                print(f"⚠️ Delayed Relationship Update Fehler: {e}")

            try:
                if hasattr(self, 'chat_messages'):
                    self.data.chat_messages = self.chat_messages.copy()
                self.data.autosave()
            except Exception as e:
                print(f"⚠️ Delayed Autosave Fehler: {e}")

        except Exception as e:
            print(f"❌ Delayed Updates Fehler: {e}")

    def _refresh_chat_display_safe(self):
        """Sichere Chat Display Refresh-Methode"""
        try:
            self.chat_display.configure(state="normal")
            self.chat_display.delete("1.0", "end")

            for sender, msg in self.chat_messages:
                import datetime
                timestamp = datetime.datetime.now().strftime("%H:%M")
                formatted_message = f"[{timestamp}] {sender}: {msg}\n\n"
                self.chat_display.insert(ctk.END, formatted_message)

            self.chat_display.see(ctk.END)
            self.chat_display.configure(state="disabled")

        except Exception as e:
            print(f"⚠️ Safe Chat Refresh Fehler: {e}")
            try:
                self.chat_display.configure(state="disabled")
            except:
                pass

    def _execute_post_response_updates(self):
        """Führt Updates nach der Response aus"""
        try:
            self.update_maternal_display()
            self.update_relationship_display()
            if hasattr(self, 'chat_messages'):
                self.data.chat_messages = self.chat_messages.copy()
            self.data.autosave()
        except Exception as e:
            print(f"⚠️ Update Fehler: {e}")

    def _generate_fallback_response(self, message):
        """Intelligente Fallback-Antwort wenn LLM nicht verfügbar ist"""

        message_lower = message.lower()

        if 'bibliothek' in message_lower:
            return "📚 Versuche `/bibliotheken` um alle Bibliotheken zu sehen!"
        elif any(word in message_lower for word in ['hallo', 'hi']):
            return "Hallo! Verwende `/help` für verfügbare Befehle."
        else:
            return f"[SYSTEM] LLM nicht verfügbar. Versuche Commands wie `/help` oder `/bibliotheken`"

    def handle_command(self, user_message: str) -> bool:
        """Prüft, ob die Benutzereingabe ein /Befehl ist und verarbeitet ihn."""

        # Alle Commands sollten mit "/" anfangen
        if not user_message.startswith('/'):
            return False

        # Teile die Eingabe in Teile auf
        parts = user_message[1:].split()  # [1:] um das "/" zu entfernen
        command = parts[0].lower()

        # ===================================================================
        # 📚 BIBLIOTHEKS-SYSTEM COMMANDS (NEU)
        # ===================================================================

        # Prüfe zuerst Library-Commands
        if hasattr(self.data, 'library_system') and self.data.library_system:
            try:
                library_handled, library_response = self.data.library_system.process_library_commands(user_message)
                if library_handled:
                    self.display_message("BIBLIOTHEK", library_response, "info")
                    return True
            except Exception as e:
                print(f"⚠️ Library-Command-Fehler: {e}")

        # ===================================================================
        # 🎯 ENCOUNTER COMMAND (ERWEITERT FÜR BIBLIOTHEKEN)
        # ==================================================================
        if command == "encounter" and len(parts) >= 2:
            location_name = parts[1].lower()
            self.data.current_location = location_name

            # ✅ NEU HINZUFÜGEN - für ALLE Locations:
            if hasattr(self, 'location_system'):
                self.location_system.update_location(location_name)
                print(f"🖼️ Location Image updated for {location_name}")


            if location_name == "sukunas_zimmer":
                room_data = self.data.game_state.get('room_customization', {})

                # 🌙 Sleep System Status checken
                sleep_info = ""
                if hasattr(self.data, 'sleep_system') and self.data.sleep_system:
                    try:
                        current_time = self.data.sleep_system.get_current_game_time()
                        can_sleep, sleep_reason = self.data.sleep_system.can_sleep()

                        if can_sleep:
                            sleep_info = f"\\n🌙 **SCHLAFEN MÖGLICH**: Es ist {current_time.strftime('%H:%M')} Uhr - Du kannst ins Bett gehen!"
                        elif current_time.hour >= 7 and current_time.hour < 20:
                            next_sleep = "20:00"
                            sleep_info = f"\\n⏰ **NOCH ZU FRÜH**: Es ist {current_time.strftime('%H:%M')} Uhr - Schlafen erst ab {next_sleep} möglich"
                        else:
                            sleep_info = f"\\n❌ **SCHLAFEN**: {sleep_reason}"
                    except Exception as e:
                        sleep_info = f"\\n⚠️ **SCHLAF-STATUS**: Fehler beim Abrufen ({str(e)})"

                # 🏠 Zimmer-Beschreibung (KORREKTE EINRÜCKUNG)
                # Alle dynamischen Teile vorher berechnen
                zimmer_zustand = "Das Zimmer wirkt gemütlicher mit deinen neuen Möbeln!" if any(
                    room_data.values()) else "Ein einfaches Gästezimmer mit den nötigsten Möbeln."

                schlafplatz = "Dein neues, komfortables Bett mit eleganter Bettwäsche" if room_data.get(
                    'has_new_bed') else "Ein einfacher Futon auf Tatami-Matten"

                arbeitsplatz = "Dein Schreibtisch am Fenster, perfekt zum Lernen" if room_data.get(
                    'has_desk') else "Kein Schreibtisch vorhanden"

                bibliothek = "Dein Bücherregal voller Ninja-Handbücher und Schriftrollen" if room_data.get(
                    'has_bookshelf') else "Keine Bücher-Aufbewahrung"

                room_description = f"""🏠 **SUKUNAS ZIMMER**

        Du betrittst dein privates Zimmer in Tsunades Haus.
        {zimmer_zustand}

        🛏️ **Schlafplatz**: {schlafplatz}

        📚 **Arbeitsplatz**: {arbeitsplatz}

        📖 **Bibliothek**: {bibliothek}
        {sleep_info}

        💡 **VERFÜGBARE AKTIONEN:**
        • /furniture_shop - Möbel einkaufen
        • /room_status - Zimmer-Status
        • /rest - Im Zimmer ausruhen
        • /study - Jutsu studieren
        • /schlafen_gehen - Schlafen gehen (nur 20:00-23:00) 🌙
        • /schlaf_status - Sleep-System Status"""

                self.display_message("🏠 Sukunas Zimmer", room_description, "location")
                return True

            # ✨ Location Image aktualisieren für andere Locations
            if hasattr(self, 'location_system'):
                self.location_system.update_location(location_name)

            try:
                # ✅ BESSERES ERROR HANDLING mit Library-Support
                if hasattr(self.data, 'encounter_system') and self.data.encounter_system:
                    print(f"🔍 Encounter system check for: {location_name}")

                    # 📚 Spezielle Bibliotheks-Behandlung
                    if 'bibliothek' in location_name:
                        self._handle_library_encounter(location_name)
                    else:
                        self._handle_standard_encounter(location_name)

                else:
                    self.display_message("Location", f"📍 Du besuchst {location_name}.", "info")

            except Exception as e:
                error_msg = f"Encounter Fehler: {e}"
                print(f"❌ FULL ERROR: {error_msg}")
                import traceback
                traceback.print_exc()
                self.display_message("FEHLER", error_msg, "danger")

            self.trigger_status_update()
            return True
        # =================================================================
        # REISEVORSCHLAG
        # =================================================================
        elif command in ["ja", "nein"] or user_message.startswith("/ja") or user_message.startswith("/nein"):
            from moduls.ai_location_suggestion_system import handle_travel_response
            travel_result = handle_travel_response(self.data, user_message)
            if travel_result:
                self.display_message("System", travel_result)
                return travel_result
        # ==================================================================
        # TSUNADES HAUS - RÄUME
        # ==================================================================
        elif command == "/küche":
            if hasattr(self, 'location_system'):
                self.location_system.update_location("tsunades_haus_kueche")
            self.data.current_location = "tsunades_haus_kueche"
            self.display_message("🏠 Du gehst in die Küche.")
            self.trigger_status_update()
            return True

        elif command == "/wohnzimmer":
            if hasattr(self, 'location_system'):
                self.location_system.update_location("tsunades_haus_wohnzimmer")
            self.data.current_location = "tsunades_haus_wohnzimmer"
            self.display_message("🏠 Du gehst ins Wohnzimmer.")
            self.trigger_status_update()
            return True

        elif command == "/schlafzimmer":
            if hasattr(self, 'location_system'):
                self.location_system.update_location("tsunades_haus_schlafzimmer")
            self.data.current_location = "tsunades_haus_schlafzimmer"
            self.display_message("🏠 Du gehst in Tsunades Schlafzimmer.")
            self.trigger_status_update()
            return True

        # ===================================================================
        # MÖBELSHOP
        # ===================================================================
        elif command == "furniture_shop":
            self.handle_furniture_shop()
            return True

        elif command == "buy_bed":
            self.buy_furniture_item('bed')
            return True

        elif command == "buy_desk":
            self.buy_furniture_item('desk')
            return True

        elif command == "buy_bookshelf":
            self.buy_furniture_item('bookshelf')
            return True

        elif command == "buy_package":
            self.buy_furniture_item('package')
            return True

        elif command == "room_status":
            self.show_room_status()
            return True

        elif command == "rest":
            if self.data.current_location == "sukunas_zimmer":
                room_data = self.data.game_state.get('room_customization', {})
                base_rest = 10
                bed_bonus = 15 if room_data.get('has_new_bed') else 0
                total_rest = base_rest + bed_bonus

                rest_msg = f"""💤 **ERHOLUNG IN DEINEM ZIMMER**

        🏥 **Erholung**: +{total_rest} HP
        {'🛏️ Bett-Bonus: +' + str(bed_bonus) + ' HP' if bed_bonus > 0 else '💤 Einfacher Futon: Standard Erholung'}

        🏠 **Du fühlst dich erfrischt und bereit für neue Abenteuer!**"""

                self.display_message("💤 Erholung", rest_msg, "success")
            else:
                self.display_message("💤 Erholung", "❌ Du musst in deinem Zimmer sein um dich auszuruhen!", "warning")
            return True


        # ===================================================================
        # 🛠️ SYSTEM COMMANDS
        # ===================================================================

        elif command in ["help", "hilfe"]:
            self.show_help()
            return True

        elif command == "status":
            self.show_status()
            return True

        elif command == "showtime":
            if hasattr(self.data, 'time_system'):
                summary = self.data.time_system.get_time_summary()
                self.display_message("Time", summary, "info")
            return True

        elif command == "family":
            if hasattr(self.data, 'family_time_system'):
                summary = self.data.family_time_system.get_family_time_summary()
                self.display_message("Family", summary, "info")
            return True

        elif command == "return":
            self.return_to_tsunade()
            return True

        # ==================================================================
        # GENIN TEAM TEST
        # ===================================================================
        elif command == "test_day5" and hasattr(self.data, 'genin_team_system'):
            # 🧪 DEVELOPMENT TEST: Force Day 5 Event
            try:
                # Force Day 5
                self.data.game_state['day'] = 5

                # Gehe nach tsunades_haus falls nicht dort
                self.data.current_location = 'tsunades_haus'

                # Trigger das Event manuell
                if hasattr(self.data, 'genin_team_system'):
                    event_message = self.data.genin_team_system.trigger_hokage_summon()
                    self.display_message("TEST DAY 5", f"🧪 **DEVELOPMENT TEST**\n\n{event_message}", "warning")
                else:
                    self.display_message("TEST", "❌ Genin Team System nicht verfügbar", "danger")

            except Exception as e:
                self.display_message("ERROR", f"Test Day 5 Fehler: {e}", "danger")
            return True

        elif command == "test_breakfast" and hasattr(self.data, 'genin_team_system'):
            # 🍳 DEVELOPMENT TEST: Force Breakfast Scene
            try:
                breakfast = self.data.genin_team_system.handle_morning_breakfast_scene()
                self.display_message("TEST BREAKFAST", f"🧪 **DEVELOPMENT TEST**\n\n{breakfast}", "info")
            except Exception as e:
                self.display_message("ERROR", f"Test Breakfast Fehler: {e}", "danger")
            return True

        elif command == "test_reset" and hasattr(self.data, 'genin_team_system'):
            # 🔄 DEVELOPMENT TEST: Reset für neue Tests
            try:
                self.data.game_state['day'] = 1
                if hasattr(self.data, 'genin_team_system'):
                    self.data.genin_team_system.hokage_summon_triggered = False
                    self.data.genin_team_system.ceremony_completed = False
                    self.data.genin_team_system.team_formed = False
                self.display_message("TEST RESET", "🔄 **DAY 1 RESET** - Bereit für neue Tests!", "success")
            except Exception as e:
                self.display_message("ERROR", f"Test Reset Fehler: {e}", "danger")
            return True

        # ===================================================================
        # 💝 RELATIONSHIP COMMANDS
        # ===================================================================

        elif command in ["relationship", "rel"]:
            self.show_relationship_status()
            return True

        elif command in ["maternal", "mat"]:
            return self._handle_maternal_command(parts)

        # ===================================================================
        # 🎭 SECRET SYSTEM COMMANDS
        # ===================================================================

        elif command == "secrets":
            return self._handle_secrets_command()

        elif command == "discover":
            return self._handle_discover_command(user_message)

        # ===================================================================
        # 👥 COMPANION SYSTEM COMMANDS
        # ===================================================================

        elif command == "companion":
            return self._handle_companion_status()

        elif command == "suggest":
            return self._handle_companion_suggest()

        elif command.startswith("ask") and len(parts) >= 2:
            return self._handle_companion_ask(parts[1].lower())

        elif command.startswith("accept") and len(parts) >= 2:
            return self._handle_companion_accept(parts[1].lower())

        elif command.startswith("decline") and len(parts) >= 2:
            return self._handle_companion_decline(parts[1].lower())

        elif command == "dismiss":
            return self._handle_companion_dismiss()

        # ===================================================================
        # ⚔️ COMBAT SYSTEM COMMANDS
        # ===================================================================

        elif command == "train" and hasattr(self.data, 'combat_system'):
            if len(parts) < 2:
                self.display_message("TRAINING", """⚔️ TRAINING OPTIONEN:

        /train taijutsu [minuten] - Taijutsu Training
        /train ninjutsu [minuten] - Ninjutsu Training  
        /train chakra [minuten] - Chakra Control Training
        /train sword [minuten] - Schwert Training

        Beispiel: /train taijutsu 45""", "info")
                return True

            training_type = parts[1].lower()
            duration = int(parts[2]) if len(parts) > 2 else 30

            try:
                result = self.data.combat_system.start_training_session(training_type, duration)

                if result["success"]:
                    message = f"🏋️ {result['message']}\n\n"
                    for key, value in result["results"].items():
                        message += f"📈 {key.replace('_', ' ').title()}: {value}\n"
                    self.display_message("TRAINING", message, "success")
                else:
                    self.display_message("ERROR", result["message"], "danger")
            except Exception as e:
                self.display_message("ERROR", f"Training Fehler: {e}", "danger")
            return True

        elif command == "spar" and hasattr(self.data, 'combat_system'):
            opponent = parts[1] if len(parts) > 1 else None

            try:
                result = self.data.combat_system.start_sparring_encounter(opponent)

                if result["success"]:
                    message = f"{result['message']}\n\n"
                    combat_log = result["combat_data"]["combat_log"]
                    # Zeige nur die ersten 10 Zeilen des Combat Logs
                    message += "\n".join(combat_log[:10])
                    if len(combat_log) > 10:
                        message += f"\n... (+{len(combat_log) - 10} weitere Zeilen)"
                    self.display_message("SPARRING", message, "info")
                else:
                    self.display_message("ERROR", result["message"], "danger")
            except Exception as e:
                self.display_message("ERROR", f"Sparring Fehler: {e}", "danger")
            return True

        elif command in ["combat_status", "stats"] and hasattr(self.data, 'combat_system'):
            try:
                status = self.data.combat_system.get_character_combat_status()

                if "error" in status:
                    self.display_message("ERROR", status["error"], "danger")
                else:
                    message = f"""📊 COMBAT STATUS - {status['character']}

        🔋 Chakra: {status['chakra']} ({status['chakra_percentage']})

        📈 SKILLS:"""
                    for skill, value in status["skills"].items():
                        message += f"\n   {skill}: {value}"

                    message += f"\n\n🎯 Gelernte Jutsus: {status['total_jutsus']}"
                    if status["learned_jutsus"]:
                        message += f"\n   {', '.join(status['learned_jutsus'][:5])}"
                        if len(status["learned_jutsus"]) > 5:
                            message += f" (+{len(status['learned_jutsus']) - 5} weitere)"

                    self.display_message("COMBAT STATUS", message, "info")
            except Exception as e:
                self.display_message("ERROR", f"Combat Status Fehler: {e}", "danger")
            return True

        elif command in ["jutsus", "jutsu_list"] and hasattr(self.data, 'combat_system'):
            try:
                jutsu_list = self.data.combat_system.get_available_jutsu_list()

                if "error" in jutsu_list:
                    self.display_message("ERROR", jutsu_list["error"], "danger")
                else:
                    message = "📜 VERFÜGBARE JUTSUS:\n\n"

                    for rank, jutsus in jutsu_list.items():
                        if jutsus:  # Nur zeigen wenn Jutsus vorhanden
                            message += f"🎯 {rank.upper()}-RANG:\n"
                            for jutsu in jutsus[:3]:  # Nur erste 3 pro Rang
                                message += f"  • {jutsu['name']} ({jutsu['element']}) - {jutsu['chakra_cost']}\n"
                                message += f"    {jutsu['status']}\n"
                            if len(jutsus) > 3:
                                message += f"    (+{len(jutsus) - 3} weitere)\n"
                            message += "\n"

                    self.display_message("JUTSU LIST", message, "info")
            except Exception as e:
                self.display_message("ERROR", f"Jutsu List Fehler: {e}", "danger")
            return True

        #=====================================================================
        # 🎬 ATMOSPHERIC COMMANDS
        #=====================================================================
        elif command in ["atmo_test", "atmospheric_test"] and hasattr(self.data, 'atmospheric_system'):
            try:
                test_description = self.data.atmospheric_system.generate_atmospheric_description(
                    "Ich schaue in die Ferne",
                    "Die Landschaft ist wunderschön"
                )
                if test_description:
                    self.display_message("ATMOSPHERIC TEST", f"🌅 Generated Description:\n\n{test_description}", "info")
                else:
                    self.display_message("ATMOSPHERIC TEST", "🌅 Keine Atmosphäre generiert (Anti-Wiederholung aktiv)",
                                         "info")
            except Exception as e:
                self.display_message("ERROR", f"Atmospheric Test Fehler: {e}", "danger")
            return True

        elif command in ["atmo_debug", "atmo"] and hasattr(self.data, 'atmospheric_system'):
            try:
                atmo = self.data.atmospheric_system
                context = atmo._gather_context_data()
                debug_info = f"""🌅 ATMOSPHERIC SYSTEM DEBUG:

        📍 **Kontext-Daten:**
        - Location: {context.get('location', 'unknown')}
        - Zeit: {context.get('game_time', 'unknown')}
        - Periode: {context.get('time_period', 'unknown')}
        - Wetter: {context.get('weather', 'unknown')}
        - Jahreszeit: {context.get('season', 'unknown')}
        - Character: {context.get('character', 'unknown')}

        📊 **Verfügbare Locations:**
        {list(atmo.location_atmospheres.keys())}

        🎭 **Letzte Verwendungen:**
        {atmo.last_used_elements[-3:] if atmo.last_used_elements else ['Keine']}

        ⚙️ **System Status:** Aktiv"""

                self.display_message("ATMOSPHERIC DEBUG", debug_info, "info")
            except Exception as e:
                self.display_message("ERROR", f"Atmospheric Debug Fehler: {e}", "danger")
            return True

        elif command == "force_atmo" and hasattr(self.data, 'atmospheric_system'):
            try:
                # Zwinge Atmosphäre für aktuellen Kontext
                forced_description = self.data.atmospheric_system.generate_atmospheric_description(
                    "Zwangs-Atmosphäre", "Test-Response"
                )
                if forced_description:
                    self.display_message("FORCED ATMOSPHERE", f"🎬 {forced_description}", "info")
                else:
                    self.display_message("FORCED ATMOSPHERE", "🎬 Keine Atmosphäre generiert", "info")
            except Exception as e:
                self.display_message("ERROR", f"Force Atmospheric Fehler: {e}", "danger")
            return True

            # ===================================================================
            # 👥 GENIN TEAM SYSTEM COMMANDS
            # ===================================================================

        elif command == "team_status" and hasattr(self.data, 'genin_team_system'):
            try:
                status = self.data.genin_team_system.get_team_status()
                self.display_message("TEAM STATUS", status, "info")
            except Exception as e:
                self.display_message("ERROR", f"Team Status Fehler: {e}", "danger")
            return True

        elif command == "call_team" and hasattr(self.data, 'genin_team_system'):
            try:
                result = self.data.genin_team_system.call_team_to_location()
                self.display_message("TEAM CALL", result, "info")
            except Exception as e:
                self.display_message("ERROR", f"Team Call Fehler: {e}", "danger")
            return True

        elif command == "team_mission" and hasattr(self.data, 'genin_team_system'):
            try:
                missions = self.data.genin_team_system.get_team_missions()
                self.display_message("TEAM MISSIONS", missions, "info")
            except Exception as e:
                self.display_message("ERROR", f"Team Mission Fehler: {e}", "danger")
            return True

        elif command == "breakfast" and hasattr(self.data, 'genin_team_system'):
            # 🍳 Manual Breakfast Scene Trigger (für Testing)
            try:
                breakfast = self.data.genin_team_system.handle_morning_breakfast_scene()
                self.display_message("BREAKFAST", breakfast, "info")
            except Exception as e:
                self.display_message("ERROR", f"Breakfast Fehler: {e}", "danger")
            return True

        elif command == "start_mission" and len(parts) >= 2:
            mission_id = parts[1].lower()

            if hasattr(self.data, 'genin_team_system'):
                try:
                    result = self.handle_start_mission(mission_id)
                    self.display_message("MISSION GESTARTET", result, "info")
                except Exception as e:
                    self.display_message("ERROR", f"Mission Start Fehler: {e}", "danger")
            else:
                self.display_message("ERROR", "Genin Team nicht verfügbar!", "danger")
            return True
        # ==================================================================
        # 🌙 SLEEP MANAGEMENT SYSTEM COMMANDS
        # ==================================================================
        elif command == "schlafen_gehen" or command == "sleep":
            if hasattr(self.data, 'sleep_system') and self.data.sleep_system:
                try:
                    success, sleep_message = self.data.sleep_system.go_to_sleep()

                    if success:
                        # Sleep erfolgreich - Spezielle Formatierung
                        self.display_message("🌙 SCHLAF-SYSTEM", sleep_message, "success")

                        # Trigger Updates für neuen Tag
                        self.trigger_status_update()

                        # Optional: Auto-Location Update
                        if hasattr(self, 'location_system'):
                            self.location_system.update_location('sukunas_zimmer')

                    else:
                        # Sleep nicht möglich
                        self.display_message("🌙 SCHLAF-SYSTEM", sleep_message, "warning")

                except Exception as e:
                    error_msg = f"❌ Fehler beim Schlafen gehen: {e}"
                    self.display_message("ERROR", error_msg, "danger")
                    print(f"⚠️ Sleep System Fehler: {e}")
            else:
                self.display_message("ERROR", "❌ Sleep System nicht verfügbar!", "danger")
            return True

        elif command == "schlaf_status" or command == "sleep_status":
            if hasattr(self.data, 'sleep_system') and self.data.sleep_system:
                try:
                    status_message = self.data.sleep_system.get_sleep_status()
                    self.display_message("🌙 SCHLAF-STATUS", status_message, "info")
                except Exception as e:
                    self.display_message("ERROR", f"❌ Status-Fehler: {e}", "danger")
            else:
                self.display_message("ERROR", "❌ Sleep System nicht verfügbar!", "danger")
            return True

        # ===================================================================
        # 💾 SAVE/LOAD COMMANDS
        # ===================================================================

        elif command == "save":
            self.save_game_dialog()
            return True

        elif command == "load":
            self.load_game_dialog()
            return True

        # ===================================================================
        # ❓ UNBEKANNTE COMMANDS
        # ===================================================================

        else:
            self.display_message("System",
                                 f"❓ Unbekannter Command: {command}\nTippe /help für verfügbare Befehle",
                                 "warning")
            return True

    # ===================================================================
    # BEGLEITUNG VORSCHLAGN ODER ANNEHMEN
    # ====================================================================
    def _handle_companion_status(self):
        """📊 Shows current companion status"""
        try:
            if hasattr(self.data, 'companion_system') and self.data.companion_system:
                status = self.data.companion_system.get_companion_status()
                self.display_message("System", status)
                return status
            else:
                message = "❌ Companion System nicht verfügbar."
                self.display_message("System", message)
                return message
        except Exception as e:
            error_msg = f"⚠️ Companion Status Error: {e}"
            self.display_message("System", error_msg)
            return error_msg

    def _handle_companion_suggest(self):
        """🎯 Shows available companions for current location"""
        try:
            if hasattr(self.data, 'companion_system') and self.data.companion_system:
                current_location = getattr(self.data, 'current_location', 'konoha')
                available = self.data.companion_system.get_available_companions()

                if available:
                    companions_list = "\n".join([f"• {char.title()}" for char in available])
                    message = f"👥 **VERFÜGBARE BEGLEITER** in {current_location.title()}:\n\n" \
                              f"{companions_list}\n\n" \
                              f"💡 Verwende '/ask [name]' um zu fragen ob sie mitkommen!"
                else:
                    message = f"😔 Keine verfügbaren Begleiter in {current_location.title()}."

                self.display_message("System", message)
                return message
            else:
                message = "❌ Companion System nicht verfügbar."
                self.display_message("System", message)
                return message
        except Exception as e:
            error_msg = f"⚠️ Companion Suggest Error: {e}"
            self.display_message("System", error_msg)
            return error_msg

    def _handle_companion_ask(self, character_name):
        """🙋‍♂️ Ask a character to become a companion"""
        try:
            if hasattr(self.data, 'companion_system') and self.data.companion_system:
                result = self.data.companion_system.request_companion(character_name)
                self.display_message("System", result)
                return result
            else:
                message = "❌ Companion System nicht verfügbar."
                self.display_message("System", message)
                return message
        except Exception as e:
            error_msg = f"⚠️ Companion Ask Error: {e}"
            self.display_message("System", error_msg)
            return error_msg

    def _handle_companion_accept(self, character_name):
        """✅ Accept a companion who suggested to join"""
        try:
            if hasattr(self.data, 'companion_system') and self.data.companion_system:
                result = self.data.companion_system.accept_companion(character_name)
                self.display_message("System", result)
                return result
            else:
                message = "❌ Companion System nicht verfügbar."
                self.display_message("System", message)
                return message
        except Exception as e:
            error_msg = f"⚠️ Companion Accept Error: {e}"
            self.display_message("System", error_msg)
            return error_msg

    def _handle_companion_decline(self, character_name):
        """❌ Decline a companion who suggested to join"""
        try:
            if hasattr(self.data, 'companion_system') and self.data.companion_system:
                result = self.data.companion_system.decline_companion(character_name)
                self.display_message("System", result)
                return result
            else:
                message = "❌ Companion System nicht verfügbar."
                self.display_message("System", message)
                return message
        except Exception as e:
            error_msg = f"⚠️ Companion Decline Error: {e}"
            self.display_message("System", error_msg)
            return error_msg

    def _handle_companion_dismiss(self):
        """👋 Dismiss current active companion"""
        try:
            if hasattr(self.data, 'companion_system') and self.data.companion_system:
                result = self.data.companion_system.dismiss_companion()
                self.display_message("System", result)
                return result
            else:
                message = "❌ Companion System nicht verfügbar."
                self.display_message("System", message)
                return message
        except Exception as e:
            error_msg = f"⚠️ Companion Dismiss Error: {e}"
            self.display_message("System", error_msg)
            return error_msg


    # ===================================================================
    # MISSION STARTEN
    # ===================================================================
    def handle_start_mission(self, mission_id: str) -> str:
        """
        🎯 Startet eine Team-Mission
        """

        team_system = self.data.genin_team_system

        # Prüfe ob Team existiert
        if not team_system.team_formed:
            return "❌ Du brauchst ein Team um Missionen zu starten!"

        # Mission Definitionen
        missions = {
            "first_mission": {
                "name": "Verschollene Katze finden",
                "rank": "D-Rang",
                "location": "dorf_zentrum",
                "description": "Die Katze des Feudalherren ist verschwunden!",
                "requirements": {
                    "missions_completed": 0,
                    "min_team_members": 1
                },
                "rewards": {
                    "missions_completed": 1,
                    "experience": 50,
                    "ryo": 1000
                }
            },

            "bandit_patrol": {
                "name": "Banditen-Patrouille",
                "rank": "C-Rang",
                "location": "wald",
                "description": "Banditen bedrohen Reisende im Wald!",
                "requirements": {
                    "missions_completed": 1,
                    "min_team_members": 2
                },
                "rewards": {
                    "missions_completed": 2,
                    "experience": 150,
                    "ryo": 3000
                }
            }
        }

        # Prüfe ob Mission existiert
        if mission_id not in missions:
            available_ids = ", ".join(missions.keys())
            return f"❌ Mission '{mission_id}' nicht gefunden!\n💡 Verfügbare IDs: {available_ids}"

        mission = missions[mission_id]
        team_data = self.data.get('team', {})
        missions_completed = team_data.get('missions_completed', 0)

        # Prüfe Requirements
        if missions_completed < mission["requirements"]["missions_completed"]:
            return f"❌ Du musst zuerst {mission['requirements']['missions_completed']} andere Missionen abschließen!"

        # Prüfe Location
        current_location = getattr(self, 'current_location', '')
        required_location = mission["location"]

        if current_location != required_location:
            return f"""❌ Falsche Location für Mission!

    🎯 **Mission**: {mission['name']}
    📍 **Benötigte Location**: {required_location}
    📍 **Aktuelle Location**: {current_location}

    💡 **Gehe zur richtigen Location**: `/encounter {required_location}`"""

        # Mission starten!
        return self.start_mission_scenario(mission_id, mission)

    def start_mission_scenario(self, mission_id: str, mission: dict) -> str:
        """
        🎬 Startet das Mission-Szenario MIT automatischer Reward-Vergabe
        """

        # Multi-Character Mode für Team aktivieren
        if hasattr(self.data, 'multi_chat'):
            team_data = self.data.game_state.get('team', {})
            team_members = team_data.get('members', [])
            sensei = team_data.get('sensei', 'kakashi')

            # Starte Team Mission Conversation
            all_characters = team_members + [sensei]
            self.data.multi_chat.start_multi_conversation(
                all_characters,
                f"Mission: {mission['name']}"
            )

        # Mission-spezifische Szenarien
        scenarios = {
            "first_mission": self.generate_cat_mission_start(mission),
            "bandit_patrol": self.generate_bandit_mission_start(mission)
        }

        scenario = scenarios.get(mission_id, self.generate_generic_mission_start(mission))

        # Füge Mission zu Game State hinzu
        if 'active_mission' not in self.data.game_state:
            self.data.game_state['active_mission'] = {}

        self.data.game_state['active_mission'] = {
            'mission_id': mission_id,
            'mission_name': mission['name'],
            'started_at': self.data.game_state.get('day', 1),
            'status': 'active'
        }

        # ✅ NEUE FEATURE: SOFORTIGE MISSION COMPLETION & REWARDS
        # (Simuliert dass die Mission sofort erfolgreich abgeschlossen wird)
        completion_reward = self.process_mission_completion(mission_id, mission)

        # Kombiniere Mission Scenario + Completion Reward
        full_scenario = f"""{scenario}

    {completion_reward}"""

        return full_scenario

    def process_mission_completion(self, mission_id: str, mission: dict) -> str:
        """
        🎁 Verarbeitet Mission Completion und vergebe Rewards (Ryo, EXP)
        """

        rewards = mission.get('rewards', {})

        # ✅ PLAYER STATS INITIALISIEREN falls nicht vorhanden
        if 'player_stats' not in self.data.game_state:
            self.data.game_state['player_stats'] = {
                'ryo': 500,  # Start-Geld
                'experience': 0,
                'missions_completed': 0,
                'level': 1
            }

        stats = self.data.game_state['player_stats']
        old_ryo = stats.get('ryo', 0)
        old_exp = stats.get('experience', 0)

        # 💰 RYO REWARD verarbeiten
        ryo_reward = rewards.get('ryo', 0)
        if ryo_reward > 0:
            stats['ryo'] += ryo_reward

        # ⭐ EXPERIENCE REWARD verarbeiten
        exp_reward = rewards.get('experience', 0)
        if exp_reward > 0:
            stats['experience'] += exp_reward

        # 📊 MISSION COUNTER aktualisieren
        if 'missions_completed' in rewards:
            stats['missions_completed'] = rewards['missions_completed']

        # 📜 MISSION HISTORY hinzufügen
        if 'mission_history' not in self.data.game_state:
            self.data.game_state['mission_history'] = []

        self.data.game_state['mission_history'].append({
            'mission_id': mission_id,
            'mission_name': mission['name'],
            'completed_at': self.data.game_state.get('day', 1),
            'rewards_received': rewards,
            'completion_time': self.data.time_system.get_formatted_time() if hasattr(self.data,
                                                                                     'time_system') else 'Unknown'
        })

        # ✅ ACTIVE MISSION als completed markieren
        if 'active_mission' in self.data.game_state:
            self.data.game_state['active_mission']['status'] = 'completed'
            self.data.game_state['active_mission']['completed_at'] = self.data.game_state.get('day', 1)

        # 🎊 LEVEL UP CHECK (optional)
        level_up_text = ""
        current_level = stats.get('level', 1)
        exp_for_next_level = current_level * 100  # Simple: Level 1 = 100 EXP, Level 2 = 200 EXP, etc.

        if stats['experience'] >= exp_for_next_level:
            stats['level'] += 1
            level_up_text = f"""

    🎊 **LEVEL UP!**
    🆙 **Neues Level**: {stats['level']}
    ⭐ **Next Level bei**: {stats['level'] * 100} EXP"""

        # 🎉 REWARD COMPLETION MESSAGE
        reward_message = f"""

    ═══════════════════════════════════════
    🎉 **MISSION ERFOLGREICH ABGESCHLOSSEN!**
    ═══════════════════════════════════════

    📋 **Mission**: {mission['name']} ({mission.get('rank', 'Unbekannt')})
    ✅ **Status**: Erfolgreich abgeschlossen

    💰 **BELOHNUNGEN ERHALTEN:**
       💸 **Ryo**: +{ryo_reward} Ryō ({old_ryo} → {stats['ryo']})
       ⭐ **Experience**: +{exp_reward} EXP ({old_exp} → {stats['experience']})
       📊 **Missions Completed**: {stats['missions_completed']}{level_up_text}

    🎯 **AKTUELLE STATISTIKEN:**
       💰 **Total Ryo**: {stats['ryo']} Ryō
       📈 **Level**: {stats['level']}
       🎖️ **Completed Missions**: {stats['missions_completed']}

    💡 **Nutze /status um deine vollständigen Stats zu sehen!**
    💡 **Nutze /team_mission um neue Missionen zu finden!**

    ═══════════════════════════════════════"""

        self.trigger_status_update()
        return reward_message




    def generate_cat_mission_start(self, mission: dict) -> str:
        """🐱 Katzen-Mission Szenario"""

        return f"""🐱 **MISSION GESTARTET: {mission['name']}**

    📍 **Location**: {mission['location'].title()}
    ⭐ **Rang**: {mission['rank']}

    🎬 **MISSION BRIEFING:**

    *Euer Team versammelt sich im Dorfzentrum*

    **Auftraggeber** (nervöser Adliger): "Bitte, ihr müsst mir helfen! Meine geliebte Katze 'Princess' ist seit gestern verschwunden!"

    *hält ein Bild einer flauschigen weißen Katze hoch*

    "Sie trägt ein rotes Halsband mit einer goldenen Glocke. Princess verlässt normalerweise nie das Dorf!"

    **Mission Ziel**: 
       🔍 Findet Princess die Katze
       🏠 Bringt sie sicher zurück
       💰 Belohnung: 1000 Ryō

    🎯 **TEAM-MODUS AKTIVIERT**: Du kannst jetzt mit deinen Teammitgliedern sprechen und planen!

    💡 **Hinweis**: Nutze '/switch [character]' um zwischen Teammitgliedern zu wechseln"""

    def generate_bandit_mission_start(mission: dict) -> str:
        """⚔️ Banditen-Mission Szenario"""

        return f"""⚔️ **MISSION GESTARTET: {mission['name']}**

    📍 **Location**: {mission['location'].title()}
    ⭐ **Rang**: {mission['rank']}

    🎬 **MISSION BRIEFING:**

    *Euer Team trifft sich am Waldrand*

    **Dorfältester**: "Die Situation wird ernst. Eine Banditengruppe terrorisiert Reisende auf der Hauptstraße zum nächsten Dorf."

    *zeigt auf eine Karte*

    "Sie haben bereits drei Handelskarawanen überfallen. Wir brauchen euch, um sie aufzuspüren und zu neutralisieren."

    **Mission Ziel**: 
       🔍 Findet die Banditen-Versteck
       ⚔️ Neutralisiert die Bedrohung 
       🛡️ Schützt unschuldige Reisende
       💰 Belohnung: 3000 Ryō

    ⚠️ **WARNUNG**: C-Rang Mission - echte Kampfgefahr!

    🎯 **TEAM-MODUS AKTIVIERT**: Koordiniert euch gut - euer Leben hängt von Teamwork ab!"""

    def generate_generic_mission_start(mission: dict) -> str:
        """🎯 Generisches Mission Szenario"""

        return f"""🎯 **MISSION GESTARTET: {mission['name']}**

    📍 **Location**: {mission['location'].title()}
    ⭐ **Rang**: {mission['rank']}

    📝 **Beschreibung**: {mission['description']}

    🎬 **DEIN TEAM IST BEREIT!**

    🎯 **TEAM-MODUS AKTIVIERT**: Arbeitet zusammen um die Mission zu erfüllen!

    💡 **Nutze normale Conversation um mit deinem Team zu interagieren und die Mission zu planen!**"""

    # ===================================================================
    # 📚 BIBLIOTHEKS-SPEZIFISCHE METHODEN
    # ===================================================================

    def _handle_library_encounter(self, location_name):
        """Behandelt Begegnungen in Bibliotheken"""

        # Standard Encounter-Check
        if hasattr(self.data.encounter_system, 'check_for_encounter'):
            encounter = self.data.encounter_system.check_for_encounter(location_name)

            if encounter:
                character = encounter.get("character", "unknown")
                self.data.active_character = character
                self.data.encounter_active = True

                # Tracke den Encounter auch für Bibliotheken
                self.start_encounter_with_character(character)

                self.update_chat_title()

                # 📚 Bibliotheks-spezifische Nachricht
                if location_name == "konoha_hauptbibliothek":
                    success_msg = f"📚 Du betrittst die Konoha Hauptbibliothek und triffst auf {character.title()}!"
                    if character == "sakura":
                        success_msg += "\n💭 Sakura studiert konzentriert medizinische Bücher."
                    elif character == "kakashi":
                        success_msg += "\n📖 Kakashi liest in der Geschichtsabteilung."
                    elif character == "mizuki_tanaka":
                        success_msg += "\n👨‍🏫 Der Bibliothekar Mizuki hilft gerne bei deinen Fragen."

                elif location_name == "tsunades_bibliothek":
                    # Prüfe Zugang
                    access_check = self._check_tsunade_library_access()
                    if not access_check["allowed"]:
                        self.display_message("BIBLIOTHEK", f"🔒 {access_check['reason']}", "warning")
                        return

                    success_msg = f"🏥 Du betrittst Tsunades private Bibliothek und findest {character.title()}!"
                    if character == "tsunade":
                        success_msg += f"\n💖 Tsunade lächelt warmherzig: 'Willkommen in meiner Sammlung, Sukuna.'"
                    elif character == "shizune":
                        success_msg += f"\n📋 Shizune ordnet medizinische Aufzeichnungen."

                success_msg += f"\n\n💡 Verwende `/bibliothek {location_name}` um verfügbare Bücher zu sehen!"
                self.display_message("ENCOUNTER SUCCESS", success_msg, "success")
            else:
                # Auch ohne NPCs können wir die Bibliothek nutzen
                if location_name == "konoha_hauptbibliothek":
                    failure_msg = "📚 Die Konoha Hauptbibliothek ist ruhig - perfekt zum ungestörten Lernen!"
                elif location_name == "tsunades_bibliothek":
                    access_check = self._check_tsunade_library_access()
                    if not access_check["allowed"]:
                        self.display_message("BIBLIOTHEK", f"🔒 {access_check['reason']}", "warning")
                        return
                    failure_msg = "🏥 Tsunades Bibliothek ist leer, aber du kannst ihre wertvollen Bücher durchstöbern."

                failure_msg += f"\n\n💡 Verwende `/bibliothek {location_name}` um verfügbare Bücher zu sehen!"
                self.display_message("BIBLIOTHEK", failure_msg, "info")

    def _check_tsunade_library_access(self):
        """Prüft Zugang zu Tsunades privater Bibliothek"""

        if hasattr(self.data, 'library_system') and self.data.library_system:
            return self.data.library_system._check_library_access("tsunades_bibliothek")

        # Fallback-Prüfung
        tsunade_relationship = 0
        if hasattr(self.data, 'relationships') and 'tsunade' in self.data.relationships:
            tsunade_relationship = self.data.relationships['tsunade'].get('level', 0)

        if tsunade_relationship < 50:
            return {
                "allowed": False,
                "reason": f"Du benötigst eine bessere Beziehung zu Tsunade (Level 50+)! Aktuelle Beziehung: {tsunade_relationship}"
            }

        return {"allowed": True}

    def get_room_image_filename(self) -> str:
        """🖼️ Bestimme welches Zimmer-Bild angezeigt werden soll"""

        room_data = self.data.game_state.get('room_customization', {})

        has_bed = room_data.get('has_new_bed', False)
        has_desk = room_data.get('has_desk', False)
        has_bookshelf = room_data.get('has_bookshelf', False)

        # Determine image based on combination
        if not has_bed and not has_desk and not has_bookshelf:
            return "backgrounds/sukunas_zimmer.jpg"  # Standard room

        elif has_bed and not has_desk and not has_bookshelf:
            return "backgrounds/sukunas_zimmer_bed_updata.jpg"  # Only bed

        elif not has_bed and has_desk and not has_bookshelf:
            return "backgrounds/sukunas_zimmer_schreibtisch.jpg"  # Only desk

        elif has_bed and has_desk and not has_bookshelf:
            return "backgrounds/sukunas_zimmer_bed_schreibtisch_update.jpg"  # Bed + desk

        elif has_bed and not has_desk and has_bookshelf:
            return "backgrounds/sukunas_zimmer_bookshelf_bed_update.jpg"  # Bed + bookshelf

        elif has_bed and has_desk and has_bookshelf:
            return "backgrounds/sukuna_zimmer_bed_bookshelf_schreibtisch_update.jpg"  # Everything

        else:
            return "backgrounds/sukunas_zimmer.jpg"  # Default fallback

    # Wenn ein Encounter erfolgreich startet:
    def start_encounter_with_character(self, character_name):
        # 🔧 FIX: Tracke erste Begegnungen
        if character_name not in self.data.encountered_characters:
            self.data.encountered_characters.append(character_name)
            print(f"✅ Erste Begegnung mit {character_name} getrackt!")
        else:
            print(f"🔄 Wiederholte Begegnung mit {character_name}")

    def _handle_standard_encounter(self, location_name):
        """Behandelt Standard-Begegnungen (nicht-Bibliotheks)"""
        print(f"🔍 ENCOUNTER DEBUG: Checking {location_name}")
        print(f"🔍 BEFORE: active_character = '{self.data.active_character}'")

        # 🆕 SPECIAL: Hokage-Turm Team Formation Event
        if location_name == 'hokage_turm' and hasattr(self.data, 'genin_team_system'):
            try:
                # Prüfe ob Day 5 Event aktiv ist
                if (self.data.genin_team_system.hokage_summon_triggered and
                        not self.data.genin_team_system.ceremony_completed):
                    ceremony_result = self.data.genin_team_system.handle_hokage_encounter()
                    self.display_message("TEAM FORMATION", ceremony_result, "success")
                    return
            except Exception as e:
                print(f"⚠️ Hokage Team Event Fehler: {e}")

        # Companion Response
        companion_response = ""
        if hasattr(self.data, 'companion_system') and self.data.companion_system:
            if self.data.companion_system.active_companion:
                companion_response = self.data.companion_system.travel_with_companion(location_name)

        if hasattr(self.data.encounter_system, 'check_for_encounter'):
            encounter = self.data.encounter_system.check_for_encounter(location_name)
            print(f"🔍 ENCOUNTER RESULT: {encounter}")

            if encounter:
                character = encounter.get("character", "unknown")
                print(f"🔍 SETTING: active_character to '{character}'")
                self.data.active_character = character
                self.data.encounter_active = True
                print(f"🔍 AFTER: active_character = '{self.data.active_character}'")
                print(f"🔍 AFTER: encounter_active = '{self.data.encounter_active}'")

                # 🔧 FIX: Tracke den Encounter
                self.start_encounter_with_character(character)

                self.update_chat_title()

                success_msg = f"🎉 ENCOUNTER SUCCESS: Begegnung mit {character.title()}! Du kannst jetzt mit ihm/ihr sprechen."

                if companion_response:
                    success_msg += companion_response

                self.display_message("ENCOUNTER SUCCESS", success_msg, "success")
            else:
                failure_msg = f"😔 ENCOUNTER MISS: Du findest niemanden im {location_name}. Versuche es später noch einmal!"

                if companion_response:
                    failure_msg += companion_response

                self.display_message("ENCOUNTER MISS", failure_msg, "warning")

    def return_to_tsunade(self):
        """Setzt die Unterhaltung zurück zu Tsunade"""
        self.data.active_character = "tsunade"
        self.data.encounter_active = False
        self.update_chat_title()
        self.display_message("System", "🏠 Du kehrst zu Tsunade zurück.", "info")

    def update_chat_title(self):
        """Aktualisiert den Chat-Titel basierend auf dem aktiven Charakter"""
        current_char = self.data.active_character.title()
        if self.data.encounter_active and current_char != "Tsunade":
            self.chat_title.configure(text=f"💬 Begegnung mit {current_char}")
        else:
            self.chat_title.configure(text="💬 Chat mit Tsunade")

    def show_status(self):
        """Zeigt den aktuellen Status"""
        status_lines = [
            f"📊 SPIELSTATUS",
            f"",
            f"👤 Aktiver Charakter: {self.data.active_character.title()}",
            f"📍 Aktuelle Location: {self.data.current_location}",
            f"🎭 Encounter aktiv: {'Ja' if self.data.encounter_active else 'Nein'}",
        ]

        status_lines.extend([
            f"",
            f"🏠 TSUNADES HAUS:",
            f"",
            f"Gehe in die Küche (/küche), ins Wohnzimmer (/wohnzimmer) oder in Tsunades Schlafzimmer (/schlafzimmer)",
            f"",

            f"🏠 SUKUNAS ZIMMER:",
            f"💰 Finanz-Status: {self.data.player_stats('ryo', 0)} Ryō verfügbar",
            f"💎 Inverstiert: {self.room_data.get('total_spent', 0)} Ryō",
            f"🛏️ Möbel-Status**",
            f"Neues Bett:{'✅ Installiert' if self.room_data.get('has_new_bed') else '❌ Standard Futon'}",
            f"Schreibtisch: {'✅ Installiert' if self.room_data.get('has_desk') else '❌ Nicht vorhanden'}",
            f"Bücherregal: {'✅ Installiert' if self.room_data.get('has_bookshelf') else '❌ Nicht vorhanden'}",
            f"💡 **Nutze /furniture_shop um mehr Möbel zu kaufen!**",
            f"🏠 **Nutze /encounter sukunas_zimmer um dein Zimmer zu besuchen!**"
        ])

        # Maternal System Status
        if self.data.maternal_system:
            try:
                level = self.data.maternal_system.get_current_level()
                category_data = self.data.maternal_system.get_current_behavior_data()
                status_lines.extend([
                    f"",
                    f"💖 MATERNAL SYSTEM:",
                    f"Level: {level}/1000",
                    f"Kategorie: {category_data.get('category', 'Normal')}"
                ])
            except:
                status_lines.append("💖 Maternal System: Fehler beim Laden")

        # Relationship System Status
        if hasattr(self.data, 'relationship_system') and self.data.relationship_system:
            try:
                status_lines.append("")
                status_lines.append("💝 BEZIEHUNGEN:")
                for char in self.data.main_characters:
                    info = self.data.relationship_system.get_relationship_info(char)
                    level = info.get('level', 0)
                    status_lines.append(f"{char.title()}: {level}")
            except:
                status_lines.append("💝 Beziehungen: Fehler beim Laden")

        status_text = "\n".join(status_lines)
        self.display_message("Status", status_text, "info")

    def show_game_interface(self):
        """Zeigt die Haupt-Spieloberfläche an und versteckt das Startmenü."""
        # Das start_frame wird ausgeblendet
        self.start_frame.pack_forget()
        # Das game_frame wird eingeblendet
        self.game_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        # Daten in die GUI laden
        self.update_chat_display()
        self.update_backstory_display()
        self.update_chat_title()

    def update_chat_display(self):
        """Aktualisiert die Chat-Anzeige"""
        # Placeholder - könnte erweitert werden
        pass

    def update_status_tab(self):
        """
        📊 Aktualisiert den Status Tab mit aktuellen Spielerdaten
        """

        if not hasattr(self, 'status_text'):
            return  # Status Tab nicht verfügbar

        # Generate Status Content (gleicher Content wie show_status aber für Tab)
        status_content = self._generate_status_content()

        # Update Status Tab
        try:
            self.status_text.configure(state="normal")  # ✅ WICHTIG: Editierbar machen
            self.status_text.delete("1.0", "end")  # ✅ WICHTIG: Alten Inhalt löschen

            # ✅ SCHÖNES FORMATTING - Zeile für Zeile einfügen
            lines = status_content.split("\\n")
            for i, line in enumerate(lines):
                if i > 0:
                    self.status_text.insert("end", "\n")  # Echter Zeilenwechsel
                self.status_text.insert("end", line)

            self.status_text.configure(state="disabled")  # Wieder read-only
            self.status_text.see("1.0")  # Scroll to top

            print("📊 Status Tab aktualisiert")
        except Exception as e:
            print(f"❌ Status Tab Update Fehler: {e}")


    def _generate_status_content(self) -> str:
        """
        📋 Generiert den Status Content für Tab UND show_status Command
        """

        # Basic Info Header
        status_lines = [
            "📊 LIVE SPIELSTATISTIKEN",
            "=" * 45,
            ""
        ]

        # 🎮 BASIC GAME INFO
        status_lines.extend([
            "🎮 BASIC GAME STATUS:",
            f"👤 Aktiver Charakter: {self.data.active_character.title()}",
            f"📍 Aktuelle Location: {self.data.current_location.replace('_', ' ').title()}",
            f"📅 In-Game Tag: {self.data.game_state.get('day', 1)}",
        ])


        # ⏰ ZEIT SYSTEM
        if hasattr(self.data, 'time_system') and self.data.time_system:
            try:
                current_time = self.data.time_system.get_formatted_time()
                status_lines.append(f"⏰ In-Game Zeit: {current_time}")
            except:
                status_lines.append("⏰ In-Game Zeit: Zeit-System Fehler")
        else:
            status_lines.append("⏰ In-Game Zeit: Zeit-System nicht verfügbar")

        status_lines.append("")

        # 🏠 ZIMMER INFO
        room_data = self.data.game_state.get('room_customization', {})

        has_bed = room_data.get('has_new_bed', False)
        has_desk = room_data.get('has_desk', False)
        has_bookshelf = room_data.get('has_bookshelf', False)
        furniture_count = sum([has_bed, has_desk, has_bookshelf])
        total_spent = room_data.get('total_spent', 0)

        status_lines.extend([
            "🏠 SUKUNAS ZIMMER:",
            "",
            f"🛋️ Möbel: {furniture_count}/3 installiert",
            f"💰 Investiert: {total_spent} Ryō",
        ])

        # Furniture Status
        furniture_status = []
        if has_bed: furniture_status.append("🛏️ Bett")
        if has_desk: furniture_status.append("📚 Schreibtisch")
        if has_bookshelf: furniture_status.append("📖 Bücherregal")

        if furniture_status:
            status_lines.append(f"✅ {', '.join(furniture_status)}")
        else:
            status_lines.append("📦 Noch kein Möbel - besuche /furniture_shop")

        status_lines.extend([
            "",
            "🚪 Besuche dein Zimmer: /encounter sukunas_zimmer",
            ""
        ])

        # 💰 PLAYER STATS (RYO & PROGRESS)
        player_stats = self.data.game_state.get('player_stats', {})
        if player_stats:
            status_lines.extend([
                "💰 PLAYER STATISTIKEN:",
                f"💸 Ryo: {player_stats.get('ryo', 0)} Ryō",
                f"⭐ Experience: {player_stats.get('experience', 0)} EXP",
                f"📊 Level: {player_stats.get('level', 1)}",
                f"🎯 Missions Completed: {player_stats.get('missions_completed', 0)}",
            ])

            # Next Level Progress
            current_level = player_stats.get('level', 1)
            current_exp = player_stats.get('experience', 0)
            exp_needed = (current_level * 100) - current_exp
            if exp_needed > 0:
                status_lines.append(f"📈 EXP bis nächstes Level: {exp_needed}")
            else:
                status_lines.append("🎊 BEREIT FÜR LEVEL UP!")

            status_lines.append("")
        else:
            # Initialize player_stats if missing
            if hasattr(self, 'data'):
                self.data.game_state['player_stats'] = {
                    'ryo': 500, 'experience': 0, 'missions_completed': 0, 'level': 1
                }
            status_lines.extend([
                "💰 PLAYER STATISTIKEN:",
                "💸 Ryo: 500 Ryō (Initialisiert)",
                "⭐ Experience: 0 EXP",
                "📊 Level: 1",
                "🎯 Missions Completed: 0",
                ""
            ])

        # 👥 TEAM STATUS
        if hasattr(self.data, 'genin_team_system') and self.data.genin_team_system:
            if self.data.genin_team_system.team_formed:
                team_data = self.data.game_state.get('team', {})
                team_id = team_data.get('team_id', 'Unknown')
                team_members = team_data.get('members', [])
                sensei = team_data.get('sensei', 'Unknown')

                status_lines.extend([
                    "👥 TEAM STATUS:",
                    f"🎯 Team: {team_id.replace('_', ' ').title()}",
                    f"👨‍🏫 Sensei: {sensei.title()}",
                    f"👥 Mitglieder: {', '.join([m.title() for m in team_members])}",
                    ""
                ])
            else:
                days_until = max(0, 5 - self.data.game_state.get('day', 1))
                if days_until > 0:
                    status_lines.extend([
                        "👥 TEAM STATUS:",
                        f"⏳ Team Formation in {days_until} Tagen",
                        f"💡 Nutze /test_day5 um zu Tag 5 zu springen",
                        ""
                    ])
                else:
                    status_lines.extend([
                        "👥 TEAM STATUS:",
                        "🏛️ Gehe zum Hokage-Turm für Team-Zuteilung",
                        "💡 Command: /encounter hokage_turm",
                        ""
                    ])
        else:
            status_lines.extend([
                "👥 TEAM STATUS:",
                "❌ Team System nicht verfügbar",
                ""
            ])

        # 🎯 MISSION STATUS
        active_mission = self.data.game_state.get('active_mission')
        if active_mission:
            status_lines.extend([
                "🎯 MISSION STATUS:",
                f"📋 {active_mission.get('mission_name', 'Unknown')}",
                f"🗓️ Gestartet: Tag {active_mission.get('started_at', 'Unknown')}",
                f"📊 Status: {active_mission.get('status', 'Unknown').title()}",
                ""
            ])
        else:
            status_lines.extend([
                "🎯 MISSION STATUS:",
                "📭 Keine aktive Mission",
                "💡 Nutze /team_mission für verfügbare Missionen",
                ""
            ])

        # 💖 MATERNAL SYSTEM STATUS (falls vorhanden)
        if hasattr(self.data, 'maternal_system') and self.data.maternal_system:
            try:
                level = self.data.maternal_system.get_current_level()
                category_data = self.data.maternal_system.get_current_behavior_data()
                status_lines.extend([
                    "💖 MATERNAL SYSTEM:",
                    f"💝 Level: {level}/1000",
                    f"📈 Kategorie: {category_data.get('category', 'Normal')}",
                    ""
                ])
            except:
                status_lines.extend([
                    "💖 MATERNAL SYSTEM:",
                    "❌ Fehler beim Laden",
                    ""
                ])

        # 🎭 ENCOUNTER STATUS
        status_lines.extend([
            "🎭 ENCOUNTER INFO:",
            f"🎪 Encounter aktiv: {'✅ Ja' if hasattr(self.data, 'encounter_active') and self.data.encounter_active else '❌ Nein'}",
            f"🎲 Encountered Characters: {len(getattr(self.data, 'encountered_characters', []))} verschiedene",
            ""
        ])

        # 🎮 QUICK COMMANDS
        status_lines.extend([
            "🎮 QUICK COMMANDS:",
            "💰 /team_mission - Neue Missionen",
            "👥 /team_status - Team Info",
            "⏰ /showtime - Aktuelle Zeit",
            "📊 /status - Status Command",
            "",
            "🔄 Dieser Tab wird automatisch aktualisiert!"
        ])

        return "\\n".join(status_lines)

    def show_status(self):
        """📊 Erweiterte show_status die AUCH den Tab aktualisiert"""

        # Generiere Status Content
        status_content = self._generate_status_content()

        # Zeige als Message UND aktualisiere Tab
        self.display_message("📊 Erweiterte Spielstatistiken", status_content, "info")
        self.update_status_tab()  # Tab auch aktualisieren

    def trigger_status_update(self):
        """
        🔄 Triggert automatische Status Updates
        Rufe diese nach wichtigen Events auf
        """

        if hasattr(self, 'update_status_tab'):
            try:
                self.update_status_tab()
            except Exception as e:
                print(f"Status Update Fehler: {e}")

    # 3. Time Advance (falls Time System Updates):
    def advance_time_callback(self):
        self.trigger_status_update()

    # 4. Team Formation (nach Team Events):
    def after_team_formation(self):
        self.trigger_status_update()



    def update_backstory_display(self):
        """Aktualisiert die Backstory-Anzeige"""
        if hasattr(self, 'backstory_display'):
            self.backstory_display.configure(state='normal')
            self.backstory_display.delete('1.0', ctk.END)

            # Hole aktuelle Backstory
            current_backstory = backstory.get_current_backstory()
            self.backstory_display.insert('1.0', current_backstory)
            self.backstory_display.configure(state='disabled')

    def handle_furniture_shop(self):
        """🛍️ Furniture Shop Interface"""

        player_stats = self.data.game_state.get('player_stats', {})
        current_ryo = player_stats.get('ryo', 0)
        room_data = self.data.game_state.get('room_customization', {
            'has_new_bed': False, 'has_desk': False, 'has_bookshelf': False, 'total_spent': 0
        })

        shop_text = f"""
        🏪 **FURNITURE SHOP - Tsunades Haus**
        💰 **Deine Ryo**: {current_ryo} Ryō

        🛏️ **FURNITURE OPTIONEN:**

        1️⃣ **Neues Bett** - 2000 Ryō
           {'✅ GEKAUFT' if room_data.get('has_new_bed') else '❌ Nicht gekauft'}
           🌟 Luxuriöses Bett mit elegantem Design

        2️⃣ **Schreibtisch** - 1500 Ryō  
           {'✅ GEKAUFT' if room_data.get('has_desk') else '❌ Nicht gekauft'}
           📚 Perfekt zum Studieren und Jutsu-Notizen

        3️⃣ **Bücherregal** - 2500 Ryō
           {'✅ GEKAUFT' if room_data.get('has_bookshelf') else '❌ Nicht gekauft'}  
           📖 Für deine wachsende Ninja-Bibliothek

        💎 **TOTAL PACKAGE** - 5500 Ryō (Save 500!)
           {'🎉 KOMPLETT' if all([room_data.get('has_new_bed'), room_data.get('has_desk'), room_data.get('has_bookshelf')]) else '📦 Bundle verfügbar'}

        💡 **COMMANDS:**
        • /buy_bed - Neues Bett kaufen
        • /buy_desk - Schreibtisch kaufen  
        • /buy_bookshelf - Bücherregal kaufen
        • /buy_package - Alles auf einmal (günstiger!)
        • /room_status - Zimmer-Status anzeigen
        """

        self.display_message("🏪 Furniture Shop", shop_text, "info")

    def buy_furniture_item(self, item_type: str) -> bool:
        """🛒 Kaufe einzelnes Furniture Item"""

        prices = {
            'bed': 2000,
            'desk': 1500,
            'bookshelf': 2500,
            'package': 5500
        }

        item_names = {
            'bed': 'Neues Bett',
            'desk': 'Schreibtisch',
            'bookshelf': 'Bücherregal',
            'package': 'Komplett-Paket'
        }

        player_stats = self.data.game_state.get('player_stats', {})
        current_ryo = player_stats.get('ryo', 0)

        if 'room_customization' not in self.data.game_state:
            self.data.game_state['room_customization'] = {
                'has_new_bed': False, 'has_desk': False, 'has_bookshelf': False, 'total_spent': 0
            }

        room_data = self.data.game_state['room_customization']

        # Check if already owned
        if item_type == 'bed' and room_data.get('has_new_bed'):
            self.display_message("🏪 Shop", "❌ Du hast bereits ein neues Bett!", "warning")
            return False

        if item_type == 'desk' and room_data.get('has_desk'):
            self.display_message("🏪 Shop", "❌ Du hast bereits einen Schreibtisch!", "warning")
            return False

        if item_type == 'bookshelf' and room_data.get('has_bookshelf'):
            self.display_message("🏪 Shop", "❌ Du hast bereits ein Bücherregal!", "warning")
            return False

        # Package deal
        if item_type == 'package':
            missing_items = []
            if not room_data.get('has_new_bed'): missing_items.append('bed')
            if not room_data.get('has_desk'): missing_items.append('desk')
            if not room_data.get('has_bookshelf'): missing_items.append('bookshelf')

            if not missing_items:
                self.display_message("🏪 Shop", "❌ Du hast bereits alles!", "warning")
                return False

            package_price = len(missing_items) * 1833  # Reduced price per item

            if current_ryo < package_price:
                self.display_message("🏪 Shop", f"❌ Nicht genug Ryo! Du brauchst {package_price} Ryō.", "danger")
                return False

            # Buy missing items
            player_stats['ryo'] -= package_price
            room_data['total_spent'] += package_price

            for item in missing_items:
                if item == 'bed': room_data['has_new_bed'] = True
                if item == 'desk': room_data['has_desk'] = True
                if item == 'bookshelf': room_data['has_bookshelf'] = True

            success_msg = f"""
        🎉 **PACKAGE DEAL ERFOLGREICH!**

        ✅ **Gekauft**: {', '.join([item_names.get(item, item) for item in missing_items])}
        💰 **Kosten**: {package_price} Ryō
        💸 **Verbleibendes Ryo**: {player_stats['ryo']} Ryō

        🏠 **Dein Zimmer wurde komplett renoviert!**
        💡 **Nutze /encounter sukunas_zimmer um es zu sehen!**
        """
            self.display_message("🎉 Furniture Shop", success_msg, "success")
            self.trigger_status_update()
            return True

        # Single item purchase
        price = prices[item_type]

        if current_ryo < price:
            self.display_message("🏪 Shop", f"❌ Nicht genug Ryo! Du brauchst {price} Ryō.", "danger")
            return False

        # Complete purchase
        player_stats['ryo'] -= price
        room_data['total_spent'] += price

        if item_type == 'bed': room_data['has_new_bed'] = True
        if item_type == 'desk': room_data['has_desk'] = True
        if item_type == 'bookshelf': room_data['has_bookshelf'] = True

        success_msg = f"""
        ✅ **KAUF ERFOLGREICH!**

        🛏️ **Gekauft**: {item_names[item_type]}
        💰 **Kosten**: {price} Ryō
        💸 **Verbleibendes Ryo**: {player_stats['ryo']} Ryō

        🏠 **Dein Zimmer wurde aktualisiert!**
        💡 **Nutze /encounter sukunas_zimmer um die Änderungen zu sehen!**
        """

        self.display_message("✅ Furniture Shop", success_msg, "success")
        self.trigger_status_update()
        if hasattr(self, 'refresh_room_image'):
            self.refresh_room_image()
        return True

    def get_room_image_filename(self) -> str:
        """🖼️ Bestimme welches Zimmer-Bild angezeigt werden soll"""

        room_data = self.data.game_state.get('room_customization', {})

        has_bed = room_data.get('has_new_bed', False)
        has_desk = room_data.get('has_desk', False)
        has_bookshelf = room_data.get('has_bookshelf', False)

        # Determine image based on combination
        if not has_bed and not has_desk and not has_bookshelf:
            return "sukunas_zimmer.jpg"  # Standard room

        elif has_bed and not has_desk and not has_bookshelf:
            return "sukunas_zimmer_bed_updata.jpg"  # Only bed

        elif not has_bed and has_desk and not has_bookshelf:
            return "sukunas_zimmer_schreibtisch.jpg"  # Only desk

        elif has_bed and has_desk and not has_bookshelf:
            return "sukunas_zimmer_bed_schreibtisch_update.jpg"  # Bed + desk

        elif has_bed and not has_desk and has_bookshelf:
            return "sukunas_zimmer_bookshelf_bed_update.jpg"  # Bed + bookshelf

        elif has_bed and has_desk and has_bookshelf:
            return "sukuna_zimmer_bed_bookshelf_schreibtisch_update.jpg"  # Everything

        # Add more combinations as needed
        else:
            return "sukunas_zimmer.jpg"  # Default fallback

    def show_relationship_status(self):
        """Zeigt den Relationship Status"""
        if hasattr(self.data, 'relationship_system') and self.data.relationship_system:
            try:
                for char in self.data.main_characters:
                    info = self.data.relationship_system.get_relationship_info(char)
                    level = info.get('level', 0)
                    self.display_message("System", f"💝 {char.title()}: Level {level}", "info")
            except Exception as e:
                self.display_message("System", f"❌ Relationship System Fehler: {e}", "danger")
        else:
            self.display_message("System", "⚠️ Relationship System nicht verfügbar", "warning")

    def show_maternal_status(self):
        """Zeigt den Maternal Status"""
        if self.data.maternal_system:
            try:
                level = self.data.maternal_system.get_current_level()
                category_data = self.data.maternal_system.get_current_behavior_data()
                self.display_message("System",
                                     f"💖 Maternal Level: {level}/1000\n"
                                     f"Kategorie: {category_data.get('category', 'Normal')}", "info")
            except Exception as e:
                self.display_message("System", f"❌ Maternal System Fehler: {e}", "danger")
        else:
            self.display_message("System", "⚠️ Maternal System nicht verfügbar", "warning")

    def show_location_info(self):
        """Zeigt Location Info"""
        self.display_message("System", f"📍 Aktuelle Location: {self.data.current_location}", "info")

    def show_help(self):
        """Zeigt Hilfe"""
        help_text = """🎮 VERFÜGBARE BEFEHLE:

🎯 NAVIGATION:
- /help - Diese Hilfe anzeigen
- /status - Aktueller Spielstatus
- /return - Zurück zu Tsunade

🗺️ LOCATIONS & ENCOUNTERS:
- /encounter [ort] - Ort besuchen (z.B. /encounter onsen)
- /locations - Alle verfügbaren Orte anzeigen

📚 BIBLIOTHEKS-SYSTEM:
- /bibliotheken - Liste aller Bibliotheken
- /bibliothek <ort> - Zeige Bücher an einem Ort
- /lesen <buch_id> <kapitel> - Lese ein Kapitel
- /lesestatistik - Deine Lesestatistiken
- /bibliothek_hilfe - Vollständige Bibliotheks-Hilfe

👥 Companion System:
- /companion - Zeigt aktuellen Begleiter-Status
- /suggest - Zeigt verfügbare Begleiter am Ort
- /ask [name] - Fragt Charakter ob er mitkommt
- /accept [name] - Akzeptiert Begleiter-Angebot
- /decline [name] - Lehnt Begleiter ab
- /dismiss - Entlässt aktuellen Begleiter

**ERKLÄRUNG DES COMPANION SYSTEMS***
[Du] /suggest
[System] 👥 VERFÜGBARE BEGLEITER in tsunades_haus:
- Tsunade: 😊 willing (❤️100)
- Shizune: 😐 neutral (❤️25)

[Du] /ask tsunade
[Tsunade] ✅ "Komm, lass uns zusammen gehen. Ich passe auf dich auf."
👥 Tsunade begleitet dich jetzt!

[Du] /encounter dorf_zentrum
[System] 📍 Du besuchst dorf_zentrum.
👥 BEGLEITER: *Tsunade schaut sich beschützend um* 'Interessant hier. Lass uns vorsichtig sein.

[Du] "Mir ist langweilig..."

[Tsunade] "Weißt du was? Lass uns ins Dorfzentrum gehen. Frische Luft wird dir gut tun."

💭 Tsunade möchte dich zu dorf_zentrum begleiten!
**Antworten**: '/accept tsunade' oder '/decline tsunade'
*******---------------**********************************************
-------------------------------------------------------------------
👥 GENIN TEAM SYSTEM (ab Tag 5):
- /team_status - Zeigt aktuellen Team-Status  
- /call_team - Ruft Team zur aktuellen Location
- /team_mission - Zeigt verfügbare Team-Missionen
- /start_mission [mission_id] - Startet eine Mission (z.B. /start_mission first_mission)
- /breakfast - Frühstück-Szene (manuell, für Testing)

🎯 MISSION SYSTEM:
- /team_mission - Zeige verfügbare Missionen
- /start_mission first_mission - Starte Katzen-Mission (D-Rang)
- /start_mission bandit_patrol - Starte Banditen-Mission (C-Rang, nach 1. Mission)

📋 MISSION ABLAUF:
1. Bekomme Team (Tag 5 Event oder /encounter hokage_turm)
2. /team_mission - Siehe verfügbare Missionen
3. Gehe zur richtigen Location (z.B. /encounter dorf_zentrum)
4. /start_mission [id] - Starte Mission
5. Rede mit deinem Team und löse die Mission!

💡 MISSION BEISPIEL:
/encounter dorf_zentrum          # Gehe zur Location
/team_mission                    # Zeigt: "Verschollene Katze finden"  
/start_mission first_mission     # Mission startet!
🐱 *Team versammelt sich, Auftraggeber erscheint*
"Meine Katze Princess ist weg!"  # Mission-Szenario beginnt

🌅 TEAM FORMATION PROCESS:
- Tag 5: Tsunade weckt dich persönlich auf (bei tsunades_haus)
- Frühstück-Szene mit mütterlicher Fürsorge
- Team-Zuteilung im Hokage-Büro (emotional + offiziell)
- Permanente Team-Mechaniken ab Tag 6"""

        self.display_message("System", help_text, "info")

    def process_message_triggers(self, message):
        """ERWEITERTE Trigger-Verarbeitung mit Advanced Relationship Triggers"""
        message_lower = message.lower()

        # ✨ ADVANCED RELATIONSHIP TRIGGERS (charakterspezifisch!)
        if self.relationship_triggers and hasattr(self.data, 'relationship_system') and self.data.relationship_system:
            try:
                # 🔧 FIX: Analysiere NUR für anwesende Charaktere
                anwesende_charaktere = []

                # 🔍 DETAILLIERTER DEBUG:
                print(f"🔍 DETAILED CHECK:")
                print(f"  - hasattr(self.data, 'active_character'): {hasattr(self.data, 'active_character')}")
                if hasattr(self.data, 'active_character'):
                    print(f"  - self.data.active_character: '{self.data.active_character}'")
                    print(f"  - type: {type(self.data.active_character)}")
                    print(f"  - bool(self.data.active_character): {bool(self.data.active_character)}")
                    print(f"  - self.data.active_character != 'sukuna': {self.data.active_character != 'sukuna'}")

                # 1. Aktiver Encounter-Character (falls vorhanden)
                if hasattr(self.data, 'active_character') and self.data.active_character:
                    print(f"🔍 CONDITION 1 PASSED")
                    if self.data.active_character != 'sukuna':
                        print(f"🔍 CONDITION 2 PASSED - Adding {self.data.active_character}")
                        anwesende_charaktere.append(self.data.active_character)
                    else:
                        print(f"🔍 CONDITION 2 FAILED - Character is sukuna")
                else:
                    print(f"🔍 CONDITION 1 FAILED")

                # 2. TODO: Hier könnten später weitere anwesende Characters hinzugefügt werden

                print(f"🔍 TRIGGER DEBUG: anwesende_charaktere = {anwesende_charaktere}")

                # Analysiere NUR für anwesende Characters
                for character in anwesende_charaktere:

                    # 🔧 DEBUG: Teste das Trigger-System direkt
                    print(f"🔍 Message für Trigger-Analysis: '{message}'")
                    print(f"🔍 Character für Trigger-Analysis: '{character}'")

                    # Prüfe ob das Trigger-System überhaupt funktioniert
                    if hasattr(self.relationship_triggers, 'character_specific_triggers'):
                        char_triggers = self.relationship_triggers.character_specific_triggers.get(character.lower(),
                                                                                                   {})
                        print(f"🔍 Available triggers for {character}: {list(char_triggers.keys())[:5]}...")  # Erste 5

                    change, trigger_descriptions = self.relationship_triggers.analyze_relationship_impact(
                        message, character
                    )
                    print(f"🔍 Change für {character}: {change}, Triggers: {trigger_descriptions}")

                    if change != 0:
                        print(f"🔍 Applying change {change} to {character}")
                        # Wende die Änderung an
                        old_info = self.data.relationship_system.get_relationship_info(character)
                        old_level = old_info.get('level', 0)

                        success = self.data.relationship_system.modify_relationship(
                            character, change, f"Trigger: {', '.join(trigger_descriptions)}"
                        )

                        if success:
                            new_info = self.data.relationship_system.get_relationship_info(character)
                            new_level = new_info.get('level', 0)

                            # Zeige schöne Benachrichtigung
                            self.add_relationship_notification(character, old_level, new_level, change,
                                                               trigger_descriptions)

            except Exception as e:
                print(f"❌ Advanced Triggers Fehler: {e}")

        # Maternal System Triggers (wie vorher)
        if self.data.maternal_system and self.data.active_character.lower() == 'tsunade':
            try:
                old_level = self.data.maternal_system.get_current_level()
                change_amount = 0
                trigger_reason = ""

                # 🔥 SEHR POSITIVE TRIGGERS (+15 bis +25)
                if any(keyword in message_lower for keyword in
                       ['mama', '*umarmt*', '*kuschelt*', '*schmiegt sich an*', 'ich hab dich lieb',
                        'ich hab dich auch lieb', 'du bist die beste mama', '*weint in ihren armen*']):
                    change_amount = 20
                    trigger_reason = "Intensive liebevolle Interaktion"

                elif any(keyword in message_lower for keyword in
                         ['danke mama', 'beschützt mich', 'du kümmerst dich so gut', 'bin so froh bei dir',
                          'fühle mich sicher']):
                    change_amount = 15
                    trigger_reason = "Dankbarkeit und Vertrauen"

                # 💚 POSITIVE TRIGGERS (+8 bis +12)
                elif any(keyword in message_lower for keyword in
                         ['trösten', 'trost', 'umarmung', '*lächelt*', 'danke']):
                    change_amount = 10
                    trigger_reason = "Positive Interaktion"

                elif any(keyword in message_lower for keyword in
                         ['müde', 'schmerz', 'angst', 'traurig', 'schlecht gefühlt', 'kopfschmerzen', 'krank']):
                    change_amount = 12
                    trigger_reason = "Hilfsbedürftigkeit (aktiviert Fürsorge-Instinkt)"

                # 💔 SEHR NEGATIVE TRIGGERS (-15 bis -25)
                elif any(keyword in message_lower for keyword in
                         ['*rennt weg*', '*schlägt die tür zu*', 'lass mich in ruhe', 'ich hasse dich', 'du nervst']):
                    change_amount = -20
                    trigger_reason = "Ablehnung und Wut"

                elif any(keyword in message_lower for keyword in
                         ['will weg von hier', 'möchte ausziehen', 'brauche dich nicht', 'bin alt genug',
                          'übertreibst']):
                    change_amount = -15
                    trigger_reason = "Unabhängigkeits-Wunsch"

                # 💙 NEGATIVE TRIGGERS (-5 bis -10)
                elif any(keyword in message_lower for keyword in
                         ['*seufzt schwer*', '*genervt*']):
                    change_amount = -5
                    trigger_reason = "Milde Ablehnung"

                elif any(keyword in message_lower for keyword in
                         ['*ignoriert*', 'wie auch immer', 'von mir aus']):
                    change_amount = -8
                    trigger_reason = "Distanziertes Verhalten"

                # 😢 LEICHT NEGATIVE TRIGGERS (-2 bis -4)
                elif any(keyword in message_lower for keyword in
                         ['*zuckt mit den schultern*', 'wenn du meinst']):
                    change_amount = -3
                    trigger_reason = "Gleichgültigkeit"

                # 🎭 SPEZIELLE AKTIONS-TRIGGERS
                elif any(action in message_lower for action in
                         ['*kuschelt sich an sie*', '*nimmt ihre hand*', '*lehnt sich an sie an']):
                    change_amount = 18
                    trigger_reason = "Liebevolle körperliche Geste"

                elif any(action in message_lower for action in
                         ['*versteckt sich hinter ihr*', '*klammert sich an sie*', '*sucht schutz*']):
                    change_amount = 22
                    trigger_reason = "Schutz-suchendes Verhalten (aktiviert Beschützer-Instinkt)"

                elif any(action in message_lower for action in
                         ['*stößt sie weg*', '*läuft aus dem raum*', '*verschränkt die arme*' , '*wehrt sich*', '*drückt sie weg*']):
                    change_amount = -12
                    trigger_reason = "Ablehnende Körpersprache"

                # 🏥 GESUNDHEITS-TRIGGERS (sehr starke Maternal Reaktion)
                elif any(health in message_lower for health in
                         ['verletzt', 'wunde', 'blut', 'schmerzen', 'unfall', 'gefallen']):
                    change_amount = 25
                    trigger_reason = "Verletzung/Gesundheitssorge (extremer Fürsorge-Instinkt)"

                elif any(health in message_lower for health in
                         ['kopfschmerzen', 'bauchschmerzen', 'fieber', 'erkältet', 'übelkeit']):
                    change_amount = 15
                    trigger_reason = "Krankheitssymptome"

                # 💤 ALLTAGS-TRIGGERS
                elif any(daily in message_lower for daily in ['bin müde', 'will schlafen', 'gute nacht']):
                    change_amount = 8
                    trigger_reason = "Fürsorge bei täglichen Bedürfnissen"


                # Level ändern falls Trigger ausgelöst wurde
                if change_amount != 0:
                    if change_amount > 0:
                        self.data.maternal_system.increase_level(change_amount, trigger_reason)
                    else:
                        self.data.maternal_system.increase_level(change_amount,
                                                                 trigger_reason)  # increase_level kann auch negativ

                    new_level = self.data.maternal_system.get_current_level()
                    self.add_maternal_notification(old_level, new_level, change_amount, trigger_reason,
                                                   change_amount > 0)

            except Exception as e:
                print(f"❌ Maternal Trigger Fehler: {e}")

    def add_relationship_notification(self, character, old_level, new_level, change, triggers):
        """Zeigt eine schöne Beziehungsänderungs-Benachrichtigung"""
        try:
            # Emoji basierend auf Änderung
            if change > 0:
                emoji = "💖" if change >= 5 else "😊"
            else:
                emoji = "💔" if change <= -5 else "😕"

            # Hauptnachricht
            char_title = character.title()
            main_msg = f"{emoji} Beziehung zu {char_title}: {old_level} → {new_level} ({change:+d})"

            # Trigger-Details
            trigger_msg = f"🎭 Grund: {', '.join(triggers)}"

            full_message = f"{main_msg}\n{trigger_msg}"

            self.display_message("🤝 BEZIEHUNG", full_message, "info")

            # Aktualisiere Beziehungs-Tab falls vorhanden
            if hasattr(self, 'refresh_relationships_display'):
                try:
                    self.refresh_relationships_display()
                except:
                    pass

        except Exception as e:
            print(f"❌ Relationship Notification Fehler: {e}")

    def display_message(self, sender: str, message: str, message_type: str = "user"):
        """Zeigt eine Nachricht im Chat an - FINAL KORRIGIERT"""
        # 🛡️ RECURSION GUARD
        if hasattr(self, '_in_display_message') and self._in_display_message:
            print(f"⚠️ display_message Recursion verhindert für: {sender}")
            return

        self._in_display_message = True

        try:
            self.chat_display.configure(state="normal")

            cleaned_message = self.clean_message_formatting(message)

            self.chat_messages.append((sender, cleaned_message))

            # Begrenze auf 20 Nachrichten
            if len(self.chat_messages) > 20:
                self.chat_messages = self.chat_messages[-20:]

            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M")

            formatted_message = f"[{timestamp}] {sender}: {cleaned_message}\n\n"

            self.chat_display.insert(ctk.END, formatted_message)
            self.chat_display.see(ctk.END)
            self.chat_display.configure(state="disabled")

        except Exception as e:
            print(f"❌ display_message Fehler: {e}")

        finally:
            self._in_display_message = False

        # Zeitstempel
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")

        # Farbe basierend auf Typ
        color = self.colors.get(message_type, "#ffffff")

        # GEFIXT: Echte \\n\\n für Absätze zwischen Messages!
        formatted_message = f"[{timestamp}] {sender}: {cleaned_message}\n\n"

        # Füge zur Chat-Anzeige hinzu
        self.chat_display.insert(ctk.END, formatted_message)
        self.chat_display.see(ctk.END)
        self.chat_display.configure(state="disabled")

    def clean_message_formatting(self, message: str) -> str:
        """Bereinigt Message-Formatierung - ALLE \\n VARIANTEN"""

        # Sicherheitscheck
        if not message or message is None:
            return ""

        cleaned = str(message)

        # Entferne ALLE \\n Varianten INNERHALB der Message
        cleaned = cleaned.replace("\\\\\\\\n\\\\\\\\n", " ")  # Doppelt-escaped \\\\n\\\\n
        cleaned = cleaned.replace("\\\\\\\\n", " ")  # Doppelt-escaped \\\\n
        cleaned = cleaned.replace("\\\\n\\\\n", " ")  # Escaped \\n\\n
        cleaned = cleaned.replace("\\\\n", " ")  # Escaped \\n
        cleaned = cleaned.replace("\\n\\n", " ")  # Echte \\n\\n
        cleaned = cleaned.replace("\\n", " ")  # Echte \\n

        # Entferne übermäßige Anführungszeichen NUR wenn sie die ganze Message umhüllen
        if len(cleaned) > 2 and cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = cleaned[1:-1]

        # Entferne mehrfache Leerzeichen
        import re
        cleaned = re.sub(r'\\s+', ' ', cleaned)

        return cleaned.strip()

    def add_message(self, sender: str, message: str, color: str = None):
        """Kompatibilitätsmethode für das Maternal System"""
        # Konvertiere color zu message_type
        message_type = "info"
        if color:
            if "relationship_accent" in str(color) or "#e91e63" in str(color):
                message_type = "maternal"
            elif "success" in str(color) or "#28a745" in str(color):
                message_type = "success"
            elif "danger" in str(color) or "#dc3545" in str(color):
                message_type = "danger"
            elif "warning" in str(color) or "#ffc107" in str(color):
                message_type = "warning"

        self.display_message(sender, message, message_type)

    def add_maternal_notification(self, old_level, new_level, change_amount, reason, is_increase):
        """Fügt eine Maternal Level Benachrichtigung hinzu"""
        direction = "+" if is_increase else ""
        emoji = "💖" if is_increase else "💔"

        notification = f"{emoji} Maternal Level: {old_level} → {new_level} ({direction}{change_amount})\nGrund: {reason}"
        self.display_message("Maternal System", notification, "maternal")

    def update_maternal_display(self):
        """Aktualisiert die Maternal System Anzeige"""
        if self.data.maternal_system and hasattr(self, 'maternal_level_label'):
            try:
                level = self.data.maternal_system.get_current_level()
                self.maternal_level_label.configure(text=f"{level}/1000")

                # Progress bar
                progress = min(level / 1000.0, 1.0)
                self.maternal_progress.set(progress)

            except Exception as e:
                print(f"❌ Maternal Display Update Fehler: {e}")

    def update_relationship_display(self):
        """Aktualisiert die Relationship Anzeige"""
        if hasattr(self, 'relationship_display') and hasattr(self.data,
                                                             'relationship_system') and self.data.relationship_system:
            try:
                self.relationship_display.configure(state="normal")
                self.relationship_display.delete("1.0", ctk.END)

                for char in self.data.main_characters:
                    info = self.data.relationship_system.get_relationship_info(char)
                    level = info.get('level', 0)
                    self.relationship_display.insert(ctk.END, f"{char.title()}: {level}\n")

                self.relationship_display.configure(state="disabled")

            except Exception as e:
                print(f"❌ Relationship Display Update Fehler: {e}")

    def setup_relationships_tab(self):
        """✨ NEU: Kompletter Beziehungen Tab mit allen Charakteren"""
        relationships_tab = self.tab_view.tab("💝 Beziehungen")

        # Header
        header_frame = ctk.CTkFrame(relationships_tab)
        header_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(header_frame, text="💝 BEZIEHUNGSSTATUS",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Refresh Button
        refresh_btn = ctk.CTkButton(header_frame, text="🔄 Aktualisieren", width=120,
                                    command=self.refresh_relationships_display)
        refresh_btn.pack(pady=5)

        # Scrollable Frame für alle Beziehungen
        self.relationships_frame = ctk.CTkScrollableFrame(relationships_tab, height=400)
        self.relationships_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # ✨ Erweiterte Charakterliste (alle 31 Charaktere)
        self.all_characters = [
            # Hauptcharaktere
            "tsunade",
            # Team 7
            "naruto", "sasuke", "sakura", "kakashi",
            # Rookie 9
            "hinata", "shino", "kiba", "neji",
            "shikamaru", "choji", "ino", "tenten", "lee",
            # Sensei
            "guy",
            # Andere wichtige Charaktere
            "orochimaru", "shizune", "hiashi", "tsume", "choza", "danzo", "shikaku"
        ]

        # Initialer Aufbau
        self.refresh_relationships_display()

    def refresh_relationships_display(self):
        """Aktualisiert die Beziehungsanzeige"""
        try:
            # 🔧 TEMPORÄRER FIX: Nutze immer Fallback mit Triggern
            print("🎨 Nutze Fallback Display mit Trigger Buttons...")
            self._create_fallback_relationship_display()

        except Exception as e:
            print(f"❌ Relationships Display Fehler: {e}")
            self._create_fallback_relationship_display()

    def _create_fallback_relationship_display(self):
        """Fallback: Normale Beziehungsanzeige ohne Portraits"""
        print("🔍 DEBUG: _create_fallback_relationship_display gestartet")

        try:
            # Lösche alte Inhalte
            print(f"🔍 DEBUG: Lösche alte Widgets in relationships_frame")
            for widget in self.relationships_frame.winfo_children():
                widget.destroy()
            print(f"🔍 DEBUG: {len(self.relationships_frame.winfo_children())} Widgets gelöscht")

            # Prüfe all_characters
            if hasattr(self, 'all_characters'):
                print(f"🔍 DEBUG: all_characters vorhanden: {len(self.all_characters)} Characters")
                print(f"🔍 DEBUG: Erste 5 Characters: {self.all_characters[:5]}")
            else:
                print("❌ DEBUG: all_characters nicht vorhanden!")
                return

            # Erstelle normale Anzeigen mit Trigger Buttons
            count = 0
            for character in self.all_characters:
                if character == getattr(self.data, 'active_character', '').lower():
                    print(f"🔍 DEBUG: Skipping active character: {character}")
                    continue  # Zeige nicht die eigene "Beziehung"

                print(f"🔍 DEBUG: Erstelle Display für {character}")
                count += 1

                char_frame = ctk.CTkFrame(self.relationships_frame)
                char_frame.pack(fill="x", padx=5, pady=2)

                # Character Name (links)
                name_label = ctk.CTkLabel(char_frame, text=f"{character.title()}:",
                                          font=ctk.CTkFont(size=12, weight="bold"), width=100)
                name_label.pack(side="left", padx=5, pady=5)

                # Hole Beziehungsinfo
                try:
                    if hasattr(self.data, 'relationship_system') and self.data.relationship_system:
                        print(f"🔍 DEBUG: Hole Relationship Info für {character}")
                        rel_info = self.data.relationship_system.get_relationship_info(character)
                        print(f"🔍 DEBUG: rel_info für {character}: {rel_info}")
                        level = rel_info.get('level', 0)
                        print(f"🔍 DEBUG: level für {character}: {level}")
                    else:
                        print("❌ DEBUG: Kein relationship_system verfügbar!")
                        level = 0
                except Exception as e:
                    print(f"💥 DEBUG: Exception beim Holen von {character}: {e}")
                    level = 0

                # Level Display
                level_label = ctk.CTkLabel(char_frame, text=f"{level:+d}",
                                           font=ctk.CTkFont(size=11), width=50)
                level_label.pack(side="left", padx=5)

                #Category Display
                category = self._get_relationship_category(level)
                emoji = self._get_relationship_emoji(level)
                category_label = ctk.CTkLabel(char_frame, text=f"{emoji} {category}",
                                              font=ctk.CTkFont(size=10), width=120)
                category_label.pack(side="left", padx=5)

                # 🎭 Trigger Button
                btn_frame = ctk.CTkFrame(char_frame)
                btn_frame.pack(side="right", padx=5, pady=2)

                trigger_btn = ctk.CTkButton(
                    btn_frame,
                    text="📋 Triggers",
                    width=80,
                    height=25,
                    fg_color="purple",
                    hover_color="darkviolet",
                    command=lambda c=character: self.show_character_triggers(c)
                )
                trigger_btn.pack(side="left", padx=2)

            print(f"✅ DEBUG: {count} Character-Displays erstellt!")

        except Exception as e:
            print(f"💥 DEBUG: Fehler in _create_fallback_relationship_display: {e}")
            import traceback
            traceback.print_exc()

    def _get_relationship_category(self, level):
        """Konvertiert Level zu Kategorie"""
        if level >= 75:
            return "Beste Freunde"
        elif level >= 50:
            return "Enge Bindung"
        elif level >= 25:
            return "Gute Freunde"
        elif level >= 10:
            return "Freundlich"
        elif level >= -10:
            return "Neutral"
        elif level >= -25:
            return "Kühl"
        elif level >= -50:
            return "Misstrauisch"
        elif level >= -75:
            return "Feindlich"
        else:
            return "Verhasst"

    def _get_relationship_emoji(self, level):
        """Konvertiert Level zu Emoji"""
        if level >= 75:
            return "💕"
        elif level >= 50:
            return "😊"
        elif level >= 25:
            return "🙂"
        elif level >= 10:
            return "😌"
        elif level >= -10:
            return "😐"
        elif level >= -25:
            return "😕"
        elif level >= -50:
            return "😠"
        elif level >= -75:
            return "😡"
        else:
            return "💔"

    def _get_relationship_color(self, level):
        """Konvertiert Level zu Farbe"""
        if level >= 50:
            return "green"
        elif level >= 25:
            return "lightgreen"
        elif level >= -25:
            return "yellow"
        elif level >= -50:
            return "orange"
        else:
            return "red"

    def show_character_triggers(self, character_name):
        """Zeigt Trigger-Übersicht für einen Character"""
        try:
            # Import des Trigger Systems
            from moduls.advanced_relationship_triggers import AdvancedRelationshipTriggers

            triggers = AdvancedRelationshipTriggers()
            character_lower = character_name.lower()

            # Hole Character Triggers
            char_triggers = triggers.character_specific_triggers.get(character_lower, {})

            if not char_triggers:
                print(f"❌ Keine spezifischen Triggers für {character_name} verfügbar")
                return

            # Erstelle Popup für Trigger-Übersicht
            self._create_trigger_popup(character_name, char_triggers)

        except Exception as e:
            print(f"⚠️ Trigger Display Fehler: {e}")

    def _create_trigger_popup(self, character_name, triggers_dict):
        """Erstellt Trigger-Übersicht Popup"""
        import customtkinter as ctk

        # Popup Window
        popup = ctk.CTkToplevel(self)
        popup.title(f"🎭 {character_name.title()} Triggers")
        popup.geometry("500x400")
        popup.grab_set()  # Modal

        # Scrollable Frame
        scroll_frame = ctk.CTkScrollableFrame(popup)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(scroll_frame, text=f"🎭 {character_name.title()} Relationship Triggers",
                             font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))

        # Separiere Positive/Negative
        positive = {k: v for k, v in triggers_dict.items() if v["value"] > 0}
        negative = {k: v for k, v in triggers_dict.items() if v["value"] < 0}

        # Positive Section
        if positive:
            pos_label = ctk.CTkLabel(scroll_frame, text="📈 POSITIVE TRIGGERS",
                                     font=("Arial", 14, "bold"), text_color="lightgreen")
            pos_label.pack(pady=(10, 5))

            for trigger, data in sorted(positive.items(), key=lambda x: x[1]["value"], reverse=True):
                text = f'✅ "{trigger}" ({data["value"]:+d}) - {data["description"]}'
                entry = ctk.CTkLabel(scroll_frame, text=text, anchor="w", justify="left")
                entry.pack(fill="x", padx=10, pady=1)

        # Negative Section
        if negative:
            neg_label = ctk.CTkLabel(scroll_frame, text="📉 NEGATIVE TRIGGERS",
                                     font=("Arial", 14, "bold"), text_color="lightcoral")
            neg_label.pack(pady=(10, 5))

            for trigger, data in sorted(negative.items(), key=lambda x: abs(x[1]["value"]), reverse=True):
                text = f'❌ "{trigger}" ({data["value"]:+d}) - {data["description"]}'
                entry = ctk.CTkLabel(scroll_frame, text=text, anchor="w", justify="left")
                entry.pack(fill="x", padx=10, pady=1)

        # Close Button
        close_btn = ctk.CTkButton(scroll_frame, text="❌ Schließen", command=popup.destroy)
        close_btn.pack(pady=10)

    def _get_relationship_category(self, level):
        """Konvertiert Level zu Kategorie"""
        if level >= 50:
            return "Enge Bindung"
        elif level >= 25:
            return "Gute Freunde"
        elif level >= 10:
            return "Freundlich"
        elif level >= -5:
            return "Neutral"
        elif level >= -20:
            return "Misstrauisch"
        else:
            return "Feindselig"

    def _get_relationship_emoji(self, level):
        """Gibt passendes Emoji für Level zurück"""
        if level >= 50:
            return "💖"
        elif level >= 25:
            return "😊"
        elif level >= 10:
            return "🙂"
        elif level >= -5:
            return "😐"
        elif level >= -20:
            return "😠"
        else:
            return "💔"

    def _get_relationship_color(self, level):
        """Gibt Farbe für Level zurück"""
        if level >= 25:
            return "#4CAF50"  # Grün
        elif level >= 0:
            return "#2196F3"  # Blau
        elif level >= -20:
            return "#FF9800"  # Orange
        else:
            return "#F44336"  # Rot

    def modify_relationship_quick(self, character, amount):
        """Schnelle Beziehungsänderung über Buttons"""
        try:
            if hasattr(self.data, 'relationship_system') and self.data.relationship_system:
                success = self.data.relationship_system.modify_relationship(
                    character, amount, f"Manuelle Anpassung ({amount:+d})"
                )
                if success:
                    self.display_message("Beziehung", f"💝 {character.title()}: {amount:+d}", "info")
                    self.refresh_relationships_display()
                else:
                    self.display_message("Fehler", f"❌ Konnte Beziehung zu {character} nicht ändern", "danger")
            else:
                self.display_message("Fehler", "❌ Relationship System nicht verfügbar", "warning")
        except Exception as e:
            self.display_message("Fehler", f"❌ Relationship Fehler: {e}", "danger")

    def save_game_dialog(self):
        """Dialog zum Speichern"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Spiel speichern"
        )

        if filepath:
            self.data.chat_messages = self.chat_messages.copy()

            if self.data.save_game(filepath):
                self.display_message("System", f"✅ Spiel gespeichert: {filepath}", "success")
            else:
                self.display_message("System", f"❌ Fehler beim Speichern", "danger")

    def load_game_dialog(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Spiel laden"
        )

        if filepath:
            if self.data.load_game(filepath):
                self.display_message("System", f"✅ Spiel geladen: {filepath}", "success")
                self.update_maternal_display()
                self.update_relationship_display()

                if hasattr(self, 'refresh_relationships_display'):
                    try:
                        self.refresh_relationships_display()
                    except Exception as e:
                        print(f"⚠️ Relationship Display Update nach Load: {e}")

                # 🔧 FIX: Übergebe den korrekten filepath!
                self.restore_chat_messages_display(filepath)

                self.show_game_interface()
            else:
                self.display_message("System", f"❌ Fehler beim Laden", "danger")

    def restore_chat_messages_display(self, filepath=None):
        """🔧 Lädt chat_messages aus der spezifizierten Datei - ERWEITERTE DEBUG VERSION"""
        print("🔍 DEBUG: restore_chat_messages_display gestartet")

        try:
            import json
            import os

            # 🔧 FIX: Nutze den übergebenen filepath oder fallback zu autosave
            if filepath is None:
                filepath = "saves/autosave.json"

            print(f"🔍 DEBUG: Versuche zu laden aus: {filepath}")

            if os.path.exists(filepath):
                print(f"✅ DEBUG: Datei existiert: {filepath}")

                with open(filepath, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)

                # 🔍 DEBUG: Zeige alle verfügbaren Keys
                print(f"🔍 DEBUG: Alle Keys im Save: {list(save_data.keys())}")

                # 🔍 DEBUG: Zeige chat_messages spezifisch
                if "chat_messages" in save_data:
                    chat_msgs = save_data["chat_messages"]
                    print(f"🔍 DEBUG: chat_messages gefunden! Typ: {type(chat_msgs)}, Länge: {len(chat_msgs)}")
                    print(f"🔍 DEBUG: Erste 2 Nachrichten: {chat_msgs[:2]}")
                else:
                    print("❌ DEBUG: 'chat_messages' Key nicht im Save gefunden!")

                    # 🔍 Suche nach ähnlichen Keys
                    similar_keys = [key for key in save_data.keys() if
                                    "chat" in key.lower() or "message" in key.lower()]
                    print(f"🔍 DEBUG: Keys mit 'chat' oder 'message': {similar_keys}")

                # Hole chat_messages aus save data
                saved_chat_messages = save_data.get("chat_messages", [])
                print(f"🔍 DEBUG: Extrahierte chat_messages: {len(saved_chat_messages)} Nachrichten")

                if saved_chat_messages:
                    # Rest der Function...
                    self.chat_display.configure(state="normal")
                    self.chat_display.delete(1.0, ctk.END)
                    self.chat_messages = saved_chat_messages.copy()

                    for sender, message in self.chat_messages:
                        formatted_message = f"[LOAD] {sender}: {message}\n\n"
                        self.chat_display.insert(ctk.END, formatted_message)

                    self.chat_display.see(ctk.END)
                    self.chat_display.configure(state="disabled")

                    print(f"🎉 Chat-Verlauf wiederhergestellt: {len(self.chat_messages)} Nachrichten")
                else:
                    print("⚠️ DEBUG: saved_chat_messages ist leer oder None")
            else:
                print(f"❌ DEBUG: Datei existiert nicht: {filepath}")

        except Exception as e:
            print(f"💥 DEBUG: Exception: {e}")
            import traceback
            traceback.print_exc()

    def on_close(self):
        """Handler für das Schließen des Fensters"""
        try:
            # 🔧 FIX: Sync chat_messages vor Autosave
            if hasattr(self, 'chat_messages'):
                self.data.chat_messages = self.chat_messages.copy()
            self.data.autosave()
            print("✅ Autosave vor Schließen durchgeführt")
        except:
            pass

        self.destroy()

    def show_start_screen(self):
        """Zeigt das Startmenü"""
        try:
            self.game_frame.pack_forget()
        except:
            pass
        self.start_frame.pack(fill="both", expand=True)


print("✅ VEREINFACHTE RPG GUI geladen!")


class LocationImageSystem:
    def __init__(self, parent_frame, data_model):
        self.parent_frame = parent_frame
        self.data = data_model
        self.current_image = None
        self.current_location = None

        # Location-zu-Bild Mapping
        self.location_images = {
            "tsunades_haus": "backgrounds/tsunades_haus.jpg",
            "tsunades_bibliothek": "backgrounds/tsunade_library.jpg",
            "sukunas_zimmer": "backgrounds/sukunas_zimmer.jpg",
            "onsen": "backgrounds/onsen.jpg",
            "dorf_zentrum": "backgrounds/dorf_zentrum.jpg",
            "training_area": "backgrounds/training_area.jpg",
            "ramen_stand": "backgrounds/ramen_stand.jpg",
            "hokage_turm": "backgrounds/hokage_turm.jpg",
            "academy": "backgrounds/academy.jpg",
            "wald": "backgrounds/wald.jpg",
            "memorial_stone": "backgrounds/memorial_stone.jpg",
            "akatsuki_hideout": "backgrounds/akatsuki_hideout.jpg",
            "hospital": "backgrounds/hospital.jpg",
            "konoha_hauptbibliothek": "backgrounds/konoha_libary.jpg"

        }

        self.setup_location_frame()

    def setup_location_frame(self):
        """Erstelle den Location Image Frame über dem Chat"""

        # Location Image Frame
        self.location_frame = ctk.CTkFrame(
            self.parent_frame,
            height=200,
            corner_radius=10
        )
        self.location_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.location_frame.pack_propagate(False)  # Feste Höhe beibehalten

        # Location Image Label
        self.image_label = ctk.CTkLabel(
            self.location_frame,
            text="",
            height=180,
            corner_radius=8
        )
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Location Name Overlay
        self.location_name_label = ctk.CTkLabel(
            self.image_label,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("black", "black"),
            text_color="white",
            corner_radius=6
        )
        self.location_name_label.place(relx=0.5, rely=0.9, anchor="center")

        # Default Location laden
        self.load_location_image("tsunades_haus")

    def load_location_image(self, location_key):
        """Lade Location Bild basierend auf Location Key"""

        if location_key == self.current_location:
            return  # Bereits geladen

        self.current_location = location_key

        try:
            # Finde passendes Bild
            if location_key == "sukunas_zimmer":
                image_path = self.get_dynamic_room_image_path()
            else:
                image_path = self.location_images.get(location_key, "backgrounds/default.jpg")

            # Prüfe ob Datei existiert
            if not os.path.exists(image_path):
                print(f"⚠️ Location Image nicht gefunden: {image_path}")
                self.load_placeholder_image(location_key)
                return

            # Lade und resize Bild
            image = Image.open(image_path)

            # Berechne optimale Größe (Aspect Ratio beibehalten)
            frame_width = 500  # Angepasst an Chat-Breite
            frame_height = 160

            # Resize mit korrektem Aspect Ratio
            image = self.resize_with_aspect_ratio(image, frame_width, frame_height)

            # Runde Ecken hinzufügen (optional)
            image = self.add_rounded_corners(image, radius=15)

            # Zu PhotoImage konvertieren
            self.current_image = ImageTk.PhotoImage(image)

            # Image anzeigen
            self.image_label.configure(image=self.current_image, text="")

            # Location Name aktualisieren


            location_names = {
                "tsunades_haus": "🏠 Tsunades Haus",
                "tsunades_bibliothek": "🏥 Tsunades private Bibliothek",
                "sukunas_zimmer": "Sukunas Zimmer",
                "onsen": "♨️ Heiße Quellen",
                "dorf_zentrum": "🏘️ Dorf Zentrum",
                "training_area": "⚔️ Trainingsgelände",
                "ramen_stand": "🍜 Ichiraku Ramen",
                "hokage_turm": "🏛️ Hokage Turm",
                "academy": "🎓 Ninja Akademie",
                "wald": "🌲 Wald von Konoha",
                "memorial_stone": "🗿 Gedenkstein",
                "konoha_hauptbibliothek": "📚 Konoha Hauptbibliothek",
            }

            if location_key == "sukunas_zimmer":
                display_name = self.get_dynamic_room_name()
            else:
                display_name = location_names.get(location_key, location_key.replace("_", " ").title())
            self.location_name_label.configure(text=display_name)

            print(f"✅ Location Image geladen: {location_key}")

        except Exception as e:
            print(f"❌ Fehler beim Laden von Location Image {location_key}: {e}")
            self.load_placeholder_image(location_key)

    def get_dynamic_room_image_path(self) -> str:
        """🏠 Bestimmt korrektes Zimmer-Bild basierend auf Furniture"""

        room_data = self.data.game_state.get('room_customization', {})
        has_bed = room_data.get('has_new_bed', False)
        has_desk = room_data.get('has_desk', False)
        has_bookshelf = room_data.get('has_bookshelf', False)

        if not has_bed and not has_desk and not has_bookshelf:
            return "backgrounds/sukunas_zimmer.jpg"
        elif has_bed and not has_desk and not has_bookshelf:
            return "backgrounds/sukunas_zimmer_bed_updata.jpg"
        elif not has_bed and has_desk and not has_bookshelf:
            return "backgrounds/sukunas_zimmer_schreibtisch.jpg"
        elif has_bed and has_desk and not has_bookshelf:
            return "backgrounds/sukunas_zimmer_bed_schreibtisch_update.jpg"
        elif has_bed and not has_desk and has_bookshelf:
            return "backgrounds/sukunas_zimmer_bookshelf_bed_update.jpg"
        elif has_bed and has_desk and has_bookshelf:
            return "backgrounds/sukuna_zimmer_bed_bookshelf_schreibtisch_update.jpg"
        else:
            return "backgrounds/sukunas_zimmer.jpg"

    def get_dynamic_room_name(self) -> str:
        """🏠 Dynamischer Room Name mit Furniture Icons"""

        room_data = self.data.game_state.get('room_customization', {})
        base_name = "🏠 Sukunas Zimmer"

        furniture_icons = []
        if room_data.get('has_new_bed'): furniture_icons.append("🛏️")
        if room_data.get('has_desk'): furniture_icons.append("📚")
        if room_data.get('has_bookshelf'): furniture_icons.append("📖")

        if furniture_icons:
            return f"{base_name} {' '.join(furniture_icons)}"
        else:
            return f"{base_name} (Gästezimmer)"

    def refresh_room_image(self):
        """🔄 Force-Refresh des Zimmer-Bildes"""

        if self.current_location == "sukunas_zimmer":
            old_location = self.current_location
            self.current_location = None
            self.load_location_image(old_location)

    def resize_with_aspect_ratio(self, image, target_width, target_height):
        """Resize Bild mit korrektem Aspect Ratio"""

        # Originalgröße
        original_width, original_height = image.size

        # Berechne Scaling Faktoren
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height

        # Verwende kleineren Faktor um in Frame zu passen
        scale_factor = min(width_ratio, height_ratio)

        # Neue Größe berechnen
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def add_rounded_corners(self, image, radius):
        """Füge runde Ecken zu Bild hinzu"""
        try:
            from PIL import ImageDraw

            # Erstelle Mask für runde Ecken
            size = image.size
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), size], radius, fill=255)

            # Konvertiere zu RGBA falls nötig
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            # Wende Mask an
            image.putalpha(mask)
            return image

        except ImportError:
            print("⚠️ PIL ImageDraw nicht verfügbar - keine runden Ecken")
            return image
        except Exception as e:
            print(f"⚠️ Fehler bei runden Ecken: {e}")
            return image

    def load_placeholder_image(self, location_key):
        """Lade Platzhalter-Bild falls Original nicht verfügbar"""

        try:
            # Erstelle einfaches Farb-Gradient als Platzhalter
            width, height = 500, 160

            # Farben basierend auf Location
            location_colors = {
                "tsunades_haus": ("#ffb3ba", "#ff7b7b"),  # Rosa/Rot
                "onsen": ("#bde5ff", "#7bb3ff"),  # Blau
                "dorf_zentrum": ("#c7ffc7", "#7bff7b"),  # Grün
                "training_area": ("#ffe6cc", "#ffb366"),  # Orange
                "ramen_stand": ("#fff2b3", "#ffe066"),  # Gelb
                "hokage_turm": ("#e6ccff", "#b366ff"),  # Lila
                "academy": ("#ffccf2", "#ff66d9"),  # Pink
                "wald": ("#ccffe6", "#66ff99"),  # Hellgrün
                "memorial_stone": ("#e6e6e6", "#b3b3b3")  # Grau
            }

            colors = location_colors.get(location_key, ("#f0f0f0", "#d0d0d0"))

            # Erstelle Gradient Image
            gradient_image = self.create_gradient_image(width, height, colors[0], colors[1])

            # Zu PhotoImage konvertieren
            self.current_image = ImageTk.PhotoImage(gradient_image)

            # Image anzeigen
            self.image_label.configure(image=self.current_image, text="")

            # Location Text
            location_text = f"📍 {location_key.replace('_', ' ').title()}"
            self.location_name_label.configure(text=location_text)

            print(f"✅ Platzhalter-Gradient geladen für: {location_key}")

        except Exception as e:
            print(f"❌ Fehler beim Erstellen des Platzhalters: {e}")
            # Fallback zu Text
            self.image_label.configure(image="", text=f"📍 {location_key.replace('_', ' ').title()}")

    def create_gradient_image(self, width, height, color1, color2):
        """Erstelle Gradient Image"""

        # Konvertiere Hex zu RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)

        # Erstelle Gradient
        image = Image.new('RGB', (width, height))
        pixels = image.load()

        for y in range(height):
            ratio = y / height
            r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
            g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
            b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)

            for x in range(width):
                pixels[x, y] = (r, g, b)

        return image

    def update_location(self, new_location):
        """Update Location Image wenn sich Location ändert"""
        if new_location != self.current_location:
            print(f"🖼️ Location geändert: {self.current_location} → {new_location}")
            self.load_location_image(new_location)


