# -*- coding: utf-8 -*-
"""
GUI MULTI-CHARACTER ENCOUNTER EXTENSION
Erweitert die RPG-GUI um echte Multi-Character Encounter Unterstützung

Diese Erweiterung:
1. Erweitert /encounter Commands um Multi-Character Support
2. Fügt /multi Command hinzu für manuelle Multi-Character Aktivierung
3. Zeigt Multi-Character Status korrekt an
4. Integriert mit dem bestehenden Multi-Character System
"""


def extend_gui_for_multi_character(gui, game_data):
    """
    🔧 HAUPTFUNKTION: Erweitert GUI um Multi-Character Support
    """

    print("🎮 Erweitere GUI für Multi-Character Encounters...")

    # 1. Erweitere handle_encounter_command
    if hasattr(gui, 'handle_encounter_command'):
        original_encounter_handler = gui.handle_encounter_command

        def enhanced_encounter_command(location_name: str) -> bool:
            """
            🎯 ERWEITERTE ENCOUNTER LOGIC: Multi-Character → Single-Character Fallback
            """

            print(f"🔍 Versuche Multi-Character Encounter in {location_name}...")

            # 1. MULTI-CHARACTER ENCOUNTER VERSUCH
            multi_result = attempt_multi_character_encounter(location_name, game_data, gui)

            if multi_result:
                print(f"🎉 Multi-Character Encounter erfolgreich!")
                return True

            # 2. FALLBACK: SINGLE-CHARACTER ENCOUNTER
            print(f"⚪ Fallback zu Single-Character Encounter...")
            return original_encounter_handler(location_name)

        gui.handle_encounter_command = enhanced_encounter_command
        print("✅ /encounter Command erweitert für Multi-Character Support")

    # 2. Füge /multi Command hinzu
    add_multi_character_commands(gui, game_data)

    # 3. Erweitere Status-Display
    extend_status_display(gui, game_data)

    # 4. Erweitere Switch-Command
    enhance_switch_command(gui, game_data)

    print("🎮 ✅ GUI erfolgreich für Multi-Character erweitert!")


def attempt_multi_character_encounter(location_name: str, game_data, gui) -> bool:
    """
    🎭 Versucht Multi-Character Encounter mit echtem System
    """

    # Prüfe ob Multi-Character System verfügbar
    if not hasattr(game_data, 'multi_encounter_system'):
        print("⚠️ multi_encounter_system nicht gefunden")
        return False

    try:
        # Verwende die ECHTE attempt_multi_encounter Methode
        encounter_info = game_data.multi_encounter_system.attempt_multi_encounter(location_name)

        if encounter_info:
            # Multi-Character Encounter erfolgreich!
            display_multi_character_encounter(encounter_info, gui, game_data)
            setup_multi_character_chat(encounter_info, game_data)
            print(f"🎉 Multi-Character Encounter erstellt: {encounter_info}")
            return True
        else:
            print(f"🎲 Multi-Character Chance verpasst ({location_name})")
            return False

    except Exception as e:
        print(f"⚠️ Multi-Character System Fehler: {e}")
        return False

def display_multi_character_encounter(encounter_info, gui, game_data):
    """
    🎭 Zeigt Multi-Character Encounter in der GUI an
    """

    npc_chars = encounter_info.get("npc_characters", encounter_info.get("characters", []))
    primary_npc = encounter_info.get("primary_npc", npc_chars[0] if npc_chars else "unknown")
    situation = encounter_info.get("situation", "Multi-Character Encounter")
    location = encounter_info.get("location", "unknown")

    if len(npc_chars) == 1:
        # Single NPC (aber über Multi-Character System)
        message = f"""🎭 **ENCOUNTER**

📍 **Ort**: {location.title()}
👤 **Begegnung**: {primary_npc.title()}  
📖 **Situation**: {situation}

💭 Du als Sukuna triffst auf {primary_npc.title()}."""

        # Setze aktiven Character
        game_data.active_character = primary_npc

    else:
        # Multi-Character Encounter
        npc_list = ", ".join([char.title() for char in npc_chars])
        others = [char for char in npc_chars if char != primary_npc]

        message = f"""🎉 **MULTI-CHARACTER ENCOUNTER**

📍 **Ort**: {location.title()}
👥 **NPCs**: {npc_list}
🗣️ **Haupt-NPC**: {primary_npc.title()}
📖 **Situation**: {situation}

💭 Du als Sukuna triffst auf mehrere Charaktere! 

🗣️ **Hauptsprecher**: {primary_npc.title()}
👥 **Auch anwesend**: {', '.join([char.title() for char in others])}

🔄 Verwende '/switch [character]' um den Haupt-Gesprächspartner zu wechseln!
📝 Alle anwesenden NPCs können auf deine Nachrichten reagieren!"""

        # Setze aktiven Character auf Primary
        game_data.active_character = primary_npc

        # Markiere Multi-Character Status
        game_data.multi_character_active = True
        game_data.active_multi_encounter = encounter_info

    # Zeige Message in GUI
    if hasattr(gui, 'add_message'):
        gui.add_message("ENCOUNTER", message)
    else:
        print(message)


def setup_multi_character_chat(encounter_info, game_data):
    """
    🎯 Aktiviert Multi-Character Chat System
    """

    npc_chars = encounter_info.get("npc_characters", encounter_info.get("characters", []))
    situation = encounter_info.get("situation", "encounter")

    # Aktiviere Multi-Chat falls verfügbar
    if hasattr(game_data, 'multi_chat'):
        game_data.multi_chat.start_multi_conversation(npc_chars, situation)
        print(f"💬 Multi-Character Chat aktiviert: {npc_chars}")

    # Setze Encounter-Status
    game_data.encounter_active = True
    if len(npc_chars) > 1:
        game_data.conversation_mode = "multi"
    else:
        game_data.conversation_mode = "single"


def add_multi_character_commands(gui, game_data):
    """
    ➕ Fügt neue Multi-Character Commands hinzu
    """

    # Erweitere handle_special_commands
    if hasattr(gui, 'handle_special_commands'):
        original_special_commands = gui.handle_special_commands

        def enhanced_special_commands(user_input: str) -> bool:

            # /multi [location] - Force Multi-Character Encounter
            if user_input.lower().startswith('/multi '):
                location = user_input[7:].strip()
                result = force_multi_character_encounter(location, game_data, gui)
                if result:
                    gui.add_message("SUCCESS", f"✅ Multi-Character Encounter in {location} gestartet!")
                else:
                    gui.add_message("ERROR", f"❌ Kein Multi-Character Encounter in {location} möglich")
                return True

            # /multi_status - Zeige Multi-Character Status
            elif user_input.lower() == '/multi_status':
                show_multi_character_status(gui, game_data)
                return True

            # /multi_test - Teste Multi-Character System
            elif user_input.lower() == '/multi_test':
                test_multi_character_system(gui, game_data)
                return True

            # /force_multi [chars] - Force Multi mit spezifischen Characters
            elif user_input.lower().startswith('/force_multi '):
                chars_input = user_input[13:].strip()
                chars = [char.strip() for char in chars_input.split(',')]
                force_multi_with_characters(chars, game_data, gui)
                return True

            # Fallback zu originalem Handler
            return original_special_commands(user_input)

        gui.handle_special_commands = enhanced_special_commands
        print("✅ Multi-Character Commands hinzugefügt: /multi, /multi_status, /multi_test, /force_multi")


def force_multi_character_encounter(location: str, game_data, gui) -> bool:
    """
    🎯 Erzwingt Multi-Character Encounter an Location
    """

    print(f"🎭 Erzwinge Multi-Character Encounter in {location}...")

    # Versuche mehrere Methoden um Multi-Character zu forcieren
    success = False

    # Methode 1: Über Multi-Character System
    if hasattr(game_data, 'multi_encounter_system'):
        try:
            encounter = game_data.multi_encounter_system.attempt_multi_encounter(location)
            if encounter:
                display_multi_character_encounter(encounter, gui, game_data)
                setup_multi_character_chat(encounter, game_data)
                success = True
        except Exception as e:
            print(f"⚠️ multi_encounter_system force Fehler: {e}")

    # Methode 2: Baue manuellen Multi-Encounter
    if not success:
        success = create_manual_multi_encounter(location, game_data, gui)

    return success


def create_manual_multi_encounter(location: str, game_data, gui) -> bool:
    """
    🔧 Erstellt manuellen Multi-Character Encounter
    """

    # Vordefinierte Multi-Character Gruppen für Locations
    location_groups = {
        "tsunades_haus": {
            "characters": ["tsunade", "shizune"],
            "situation": "Familiäre Fürsorge"
        },
        "training_area": {
            "characters": ["naruto", "sasuke", "sakura"],
            "situation": "Team 7 Training"
        },
        "academy": {
            "characters": ["naruto", "sasuke", "sakura", "ino"],
            "situation": "Academy Reunion"
        },
        "dorf_zentrum": {
            "characters": ["ino", "sakura", "hinata"],
            "situation": "Mädchen-Talk"
        },
        "ramen_stand": {
            "characters": ["naruto", "choji"],
            "situation": "Gemeinsames Essen"
        },
        "hokage_turm": {
            "characters": ["tsunade", "shizune"],
            "situation": "Offizielle Angelegenheiten"
        }
    }

    if location in location_groups:
        group_info = location_groups[location]

        # Erstelle Encounter-Info
        encounter_info = {
            "type": "multi_character",
            "location": location,
            "npc_characters": group_info["characters"],
            "characters": group_info["characters"],  # Fallback
            "primary_npc": group_info["characters"][0],
            "secondary_npcs": group_info["characters"][1:],
            "situation": group_info["situation"]
        }

        display_multi_character_encounter(encounter_info, gui, game_data)
        setup_multi_character_chat(encounter_info, game_data)

        print(f"🎭 Manueller Multi-Character Encounter erstellt: {group_info['characters']}")
        return True

    return False


def force_multi_with_characters(characters: list, game_data, gui):
    """
    🎯 Startet Multi-Character Chat mit spezifischen Characters
    """

    # Filtere gültige Characters
    valid_chars = []
    if hasattr(game_data, 'characters') and hasattr(game_data.characters, 'character_data'):
        available_chars = list(game_data.characters.character_data.keys())
        valid_chars = [char for char in characters if char in available_chars]
    else:
        # Fallback zu bekannten Characters
        known_chars = ["tsunade", "naruto", "sasuke", "sakura", "kakashi", "shizune", "ino", "shikamaru", "choji",
                       "kiba", "hinata"]
        valid_chars = [char for char in characters if char in known_chars]

    if not valid_chars:
        gui.add_message("ERROR", f"❌ Keine gültigen Characters gefunden: {characters}")
        return

    # Erstelle Force-Encounter
    encounter_info = {
        "type": "multi_character",
        "location": "custom",
        "npc_characters": valid_chars,
        "characters": valid_chars,
        "primary_npc": valid_chars[0],
        "secondary_npcs": valid_chars[1:] if len(valid_chars) > 1 else [],
        "situation": "Custom Multi-Character Chat"
    }

    display_multi_character_encounter(encounter_info, gui, game_data)
    setup_multi_character_chat(encounter_info, game_data)

    gui.add_message("SUCCESS", f"🎭 Multi-Character Chat gestartet mit: {', '.join(valid_chars)}")


def show_multi_character_status(gui, game_data):
    """
    📊 Zeigt detaillierten Multi-Character Status
    """

    status_lines = []
    status_lines.append("🎭 === MULTI-CHARACTER STATUS ===")

    # Multi-Character System Status
    systems = []
    if hasattr(game_data, 'multi_chat'):
        systems.append("Chat")
    if hasattr(game_data, 'multi_encounter_system'):
        systems.append("Encounters")
    if hasattr(game_data, 'multi_character_ai'):
        systems.append("AI")
    if hasattr(game_data, 'basic_multi_controller') or hasattr(game_data, 'simple_multi_controller'):
        systems.append("Controller")

    if systems:
        status_lines.append(f"✅ Verfügbare Systeme: {', '.join(systems)}")
    else:
        status_lines.append("❌ Keine Multi-Character Systeme verfügbar")

    # Aktueller Status
    multi_active = getattr(game_data, 'multi_character_active', False)
    conversation_mode = getattr(game_data, 'conversation_mode', 'single')

    status_lines.append(f"📊 Multi-Character Aktiv: {'✅' if multi_active else '❌'}")
    status_lines.append(f"💬 Conversation Mode: {conversation_mode}")

    # Aktiver Encounter
    if hasattr(game_data, 'active_multi_encounter'):
        encounter = game_data.active_multi_encounter
        if encounter:
            chars = encounter.get('npc_characters', encounter.get('characters', []))
            status_lines.append(f"🎭 Aktive NPCs: {', '.join(chars)}")
            status_lines.append(f"📍 Location: {encounter.get('location', 'unknown')}")

    # Multi-Chat Status
    if hasattr(game_data, 'multi_chat'):
        chat_mode = game_data.multi_chat.conversation_mode
        active_chars = game_data.multi_chat.active_characters
        primary = game_data.multi_chat.primary_speaker

        status_lines.append(f"💬 Chat Mode: {chat_mode}")
        if active_chars:
            status_lines.append(f"👥 Chat Characters: {', '.join(active_chars)}")
            status_lines.append(f"🗣️ Primary Speaker: {primary}")

    status_message = "\n".join(status_lines)
    gui.add_message("STATUS", status_message)


def test_multi_character_system(gui, game_data):
    """
    🧪 Testet Multi-Character System
    """

    test_results = []
    test_results.append("🧪 === MULTI-CHARACTER SYSTEM TEST ===")

    # Test 1: Verfügbare Systeme
    tests = {
        "Multi-Chat": hasattr(game_data, 'multi_chat'),
        "Multi-Encounter": hasattr(game_data, 'multi_encounter_system'),
        "Multi-AI": hasattr(game_data, 'multi_character_ai'),
        "Basic Controller": hasattr(game_data, 'basic_multi_controller'),
        "Simple Controller": hasattr(game_data, 'simple_multi_controller')
    }

    for test_name, result in tests.items():
        status = "✅" if result else "❌"
        test_results.append(f"{status} {test_name}: {'Verfügbar' if result else 'Nicht gefunden'}")

    # Test 2: Test Multi-Encounter
    test_results.append("\n🎯 Teste Multi-Encounter...")
    try:
        test_location = "tsunades_haus"
        multi_success = attempt_multi_character_encounter(test_location, game_data, gui)
        test_results.append(
            f"{'✅' if multi_success else '❌'} Multi-Encounter Test: {'Erfolgreich' if multi_success else 'Fehlgeschlagen'}")
    except Exception as e:
        test_results.append(f"❌ Multi-Encounter Test Fehler: {e}")

    test_message = "\n".join(test_results)
    gui.add_message("TEST", test_message)


def extend_status_display(gui, game_data):
    """
    📊 Erweitert Status-Display um Multi-Character Info
    """

    if hasattr(gui, 'get_status_text'):
        original_get_status = gui.get_status_text

        def enhanced_get_status():
            """Erweiterte Status-Anzeige mit Multi-Character"""

            status = original_get_status()

            # Füge Multi-Character Info hinzu
            multi_info = []

            # Multi-Character Aktiv?
            if getattr(game_data, 'multi_character_active', False):
                multi_info.append("🎭 Multi-Character: ✅ Aktiv")

                # Zeige aktive NPCs
                if hasattr(game_data, 'active_multi_encounter'):
                    encounter = game_data.active_multi_encounter
                    if encounter:
                        chars = encounter.get('npc_characters', encounter.get('characters', []))
                        multi_info.append(f"    NPCs: {', '.join(chars)}")

                # Zeige Primary Speaker
                if hasattr(game_data, 'multi_chat') and game_data.multi_chat.primary_speaker:
                    multi_info.append(f"    Hauptsprecher: {game_data.multi_chat.primary_speaker}")
            else:
                multi_info.append("🎭 Multi-Character: ❌ Inaktiv")

            if multi_info:
                status += "\n" + "\n".join(multi_info)

            return status

        gui.get_status_text = enhanced_get_status


def enhance_switch_command(gui, game_data):
    """
    🔄 Verbessert /switch Command für bessere Funktionalität
    """

    # Der /switch Command ist bereits da, aber wir machen ihn robuster
    if hasattr(gui, 'handle_special_commands'):
        original_special_commands = gui.handle_special_commands

        def enhanced_special_commands_with_switch(user_input: str) -> bool:

            # Enhanced /switch Command
            if user_input.lower().startswith('/switch '):
                character_name = user_input[8:].strip().lower()

                # Versuche verschiedene Switch-Methoden
                success = False

                # Methode 1: Multi-Chat System
                if hasattr(game_data, 'multi_chat') and game_data.multi_chat.conversation_mode == "multi":
                    try:
                        success = game_data.multi_chat.switch_primary_speaker(character_name)
                        if success:
                            game_data.active_character = character_name
                            gui.add_message("SUCCESS",
                                            f"🔄 Haupt-Gesprächspartner gewechselt zu: {character_name.title()}")
                        else:
                            available_chars = game_data.multi_chat.active_characters
                            gui.add_message("ERROR",
                                            f"❌ {character_name} nicht verfügbar. Anwesend: {', '.join(available_chars)}")
                    except Exception as e:
                        gui.add_message("ERROR", f"❌ Switch-Fehler: {e}")

                # Methode 2: Controller System
                elif hasattr(game_data, 'simple_multi_controller'):
                    try:
                        success = game_data.simple_multi_controller.switch_character(character_name)
                        if success:
                            gui.add_message("SUCCESS", f"🔄 Character gewechselt zu: {character_name.title()}")
                        else:
                            gui.add_message("ERROR", f"❌ Kann nicht zu {character_name} wechseln")
                    except Exception as e:
                        gui.add_message("ERROR", f"❌ Controller Switch-Fehler: {e}")

                # Fallback: Direkter Character-Wechsel
                else:
                    game_data.active_character = character_name
                    gui.add_message("INFO", f"ℹ️ Character gesetzt auf: {character_name.title()} (Simple Switch)")
                    success = True

                return True

            # Fallback zu Original
            return original_special_commands(user_input)

        gui.handle_special_commands = enhanced_special_commands_with_switch


# Integration Function für main_backup.py
def integrate_gui_multi_character_support(game_data):
    """
    🎯 Hauptintegrationsfunktion für main_backup.py/rpg_gui_backup.py
    """

    print("🎮 Integriere Multi-Character Support in GUI...")

    # Prüfe ob GUI verfügbar ist
    gui = None
    if hasattr(game_data, 'gui'):
        gui = game_data.gui
    else:
        print("⚠️ GUI nicht gefunden - kann Multi-Character Support nicht integrieren")
        return False

    try:
        extend_gui_for_multi_character(gui, game_data)
        return True
    except Exception as e:
        print(f"❌ GUI Multi-Character Integration Fehler: {e}")
        return False


if __name__ == "__main__":
    print("🎮 GUI Multi-Character Extension")
    print("Nutze: integrate_gui_multi_character_support(game_data)")
    print("Neue Commands: /multi, /multi_status, /multi_test, /force_multi")