# -*- coding: utf-8 -*-
"""
🔧 FIXED RELATIONSHIP SYSTEM für das Naruto RPG
Verwaltet alle Beziehungen zwischen Sukuna und anderen Charakteren
"""

from typing import Optional, Dict, Any
import json


def safe_string_check(needle, haystack):
    """Sichere String-in-String Prüfung"""
    try:
        return str(needle).lower() in str(haystack).lower()
    except (TypeError, AttributeError):
        return False


class MaternalSystemProtocol:
    """Protocol für Maternal System Interface"""

    def get_current_level(self) -> int:
        return 0

    def get_level_category(self, level=None) -> str:
        return "unknown"


class FixedRelationshipSystem:
    """🔧 Korrigiertes Relationship System mit besserer Fehlerbehandlung"""

    def __init__(self, game_state=None, gui=None, maternal_system: Optional[MaternalSystemProtocol] = None):
        self.maternal_system = maternal_system
        self.game_state = game_state or {}
        self.gui = gui
        self.relationship_history = []

        # Sichere Initialisierung
        self.relationships = {}

        # Lade Beziehungen
        try:
            self.relationships = self.load_relationships_safely()
            print(f"✅ Relationship System initialisiert mit {len(self.relationships)} Charakteren")
        except Exception as e:
            print(f"⚠️ Relationship System Initialisierung Fehler: {e}")
            self.relationships = self.get_minimal_fallback()

        # Game Settings
        self.ingame_age_of_genin = 13
        self.days_elapsed = 0

        # Plot Status
        self.plot_status = {
            "Sasuke_Status": "Sasuke ist im Dorf von Konoha.",
            "Jiraiya_Status": "Jiraiya ist am Leben.",
            "Genin_Alter": f"Alle Genin sind {self.ingame_age_of_genin} Jahre alt.",
            "Akatsuki_Status": "Akatsuki ist passiv und stellt keine direkte, präsente Gefahr für Konoha dar."
        }

    def load_relationships_safely(self) -> Dict[str, Dict[str, Any]]:
        """Lädt Beziehungen mit verbesserter Fehlerbehandlung"""
        relationships = {}

        # Versuch 1: Lade aus characters.py
        try:
            from moduls.characters import get_all_characters
            all_chars = get_all_characters()

            for char_name, char_data in all_chars.items():
                if char_name.startswith("_"):  # Skip Metadaten
                    continue

                # Sichere Extraktion der Bindung
                bindung = self._safe_get_bindung(char_data)

                relationships[char_name] = {
                    "level": bindung,
                    "titel": self.get_relationship_level_text(bindung),
                    "gruppe": self.get_character_group(char_name, char_data)
                }

                # Aktualisiere game_state sicher
                self._safe_update_game_state(char_name, char_data, bindung)

            print(f"✅ {len(relationships)} Charaktere aus characters.py geladen")

            # Überschreibe mit game_state Werten
            self._apply_game_state_overrides(relationships)

            return relationships

        except ImportError:
            print("⚠️ characters.py nicht gefunden - verwende Fallback")
            return self.get_fallback_relationships()
        except Exception as e:
            print(f"⚠️ Fehler beim Laden aus characters.py: {e}")
            return self.get_fallback_relationships()

    def _safe_get_bindung(self, char_data):
        """Sichere Extraktion der Bindung aus Character-Daten"""
        try:
            bindung = char_data.get("bindung_sukuna", 0)
            return int(bindung) if bindung is not None else 0
        except (ValueError, TypeError):
            return 0

    def _safe_update_game_state(self, char_name, char_data, bindung):
        """Sichere Aktualisierung des game_state"""
        try:
            if char_name not in self.game_state:
                self.game_state[char_name] = char_data.copy() if char_data else {}

            # Stelle sicher dass bindung_sukuna existiert
            if "bindung_sukuna" not in self.game_state[char_name]:
                self.game_state[char_name]["bindung_sukuna"] = bindung
        except Exception as e:
            print(f"⚠️ Game State Update Fehler für {char_name}: {e}")

    def _apply_game_state_overrides(self, relationships):
        """Wendet game_state Overrides sicher an"""
        try:
            for char_name, char_data in self.game_state.items():
                if isinstance(char_data, dict) and "bindung_sukuna" in char_data:
                    try:
                        level = int(char_data["bindung_sukuna"])
                        if char_name in relationships:
                            relationships[char_name]["level"] = level
                            relationships[char_name]["titel"] = self.get_relationship_level_text(level)
                    except (ValueError, TypeError):
                        continue
        except Exception as e:
            print(f"⚠️ Game State Override Fehler: {e}")

    def get_fallback_relationships(self) -> Dict[str, Dict[str, Any]]:
        """Fallback-Beziehungen mit allen wichtigen Charakteren"""
        base_relationships = {
            # Main Characters
            "tsunade": {"level": 100, "titel": "Beschützerin 💖", "gruppe": "main"},

            # Team 7
            "naruto": {"level": 0, "titel": "Neutral 😐", "gruppe": "team_7"},
            "sasuke": {"level": 0, "titel": "Neutral 😐", "gruppe": "team_7"},
            "sakura": {"level": 0, "titel": "Neutral 😐", "gruppe": "team_7"},
            "kakashi": {"level": 0, "titel": "Neutral 😐", "gruppe": "team_7"},

            # Rookie 9
            "hinata": {"level": 0, "titel": "Neutral 😐", "gruppe": "rookie_9"},
            "kiba": {"level": 0, "titel": "Neutral 😐", "gruppe": "rookie_9"},
            "shino": {"level": 0, "titel": "Neutral 😐", "gruppe": "rookie_9"},
            "choji": {"level": 0, "titel": "Neutral 😐", "gruppe": "rookie_9"},
            "shikamaru": {"level": 0, "titel": "Neutral 😐", "gruppe": "rookie_9"},
            "ino": {"level": 0, "titel": "Neutral 😐", "gruppe": "rookie_9"},
            "lee": {"level": 0, "titel": "Neutral 😐", "gruppe": "rookie_9"},
            "tenten": {"level": 0, "titel": "Neutral 😐", "gruppe": "rookie_9"},
            "neji": {"level": 0, "titel": "Neutral 😐", "gruppe": "rookie_9"},

            # Adult Ninjas
            "shizune": {"level": 0, "titel": "Neutral 😐", "gruppe": "adults"},
            "hiashi": {"level": 0, "titel": "Neutral 😐", "gruppe": "adults"},
            "tsume": {"level": 0, "titel": "Neutral 😐", "gruppe": "adults"},
            "choza": {"level": 0, "titel": "Neutral 😐", "gruppe": "adults"},
            "inoichi": {"level": 0, "titel": "Neutral 😐", "gruppe": "adults"},
            "shikaku": {"level": 0, "titel": "Neutral 😐", "gruppe": "adults"},
            "might_guy": {"level": 0, "titel": "Neutral 😐", "gruppe": "adults"},

            # Villains
            "orochimaru": {"level": -50, "titel": "Misstrauisch 😠", "gruppe": "villains"},
            "kabuto": {"level": -30, "titel": "Kühl 😕", "gruppe": "villains"},
            "danzo": {"level": -40, "titel": "Misstrauisch 😠", "gruppe": "villains"},

            # Akatsuki
            "itachi": {"level": 0, "titel": "Neutral 😐", "gruppe": "akatsuki"},
            "kisame": {"level": -20, "titel": "Kühl 😕", "gruppe": "akatsuki"},
            "pain": {"level": -30, "titel": "Kühl 😕", "gruppe": "akatsuki"},
            "sasori": {"level": -25, "titel": "Kühl 😕", "gruppe": "akatsuki"},
            "deidara": {"level": -20, "titel": "Kühl 😕", "gruppe": "akatsuki"},
            "hidan": {"level": -35, "titel": "Misstrauisch 😠", "gruppe": "akatsuki"}
        }

        # Überschreibe mit game_state Werten falls verfügbar
        try:
            for char_name, char_data in self.game_state.items():
                if isinstance(char_data, dict) and "bindung_sukuna" in char_data:
                    try:
                        level = int(char_data["bindung_sukuna"])
                        if char_name in base_relationships:
                            base_relationships[char_name]["level"] = level
                            base_relationships[char_name]["titel"] = self.get_relationship_level_text(level)
                    except (ValueError, TypeError):
                        continue
        except Exception as e:
            print(f"⚠️ Fallback Override Fehler: {e}")

        return base_relationships

    def get_minimal_fallback(self) -> Dict[str, Dict[str, Any]]:
        """Minimaler Fallback bei kritischen Fehlern"""
        return {
            "tsunade": {"level": 100, "titel": "Beschützerin 💖", "gruppe": "main"},
            "naruto": {"level": 0, "titel": "Neutral 😐", "gruppe": "team_7"},
            "sasuke": {"level": 0, "titel": "Neutral 😐", "gruppe": "team_7"},
            "sakura": {"level": 0, "titel": "Neutral 😐", "gruppe": "team_7"}
        }

    def get_character_group(self, char_name, char_data=None):
        """Bestimmt die Charaktergruppe sicher"""
        try:
            if char_data and "gruppe" in char_data:
                return char_data["gruppe"]

            # Fallback basierend auf Namen
            team_7 = ["naruto", "sasuke", "sakura", "kakashi"]
            rookie_9 = ["hinata", "kiba", "shino", "choji", "shikamaru", "ino", "lee", "tenten", "neji"]
            akatsuki = ["itachi", "kisame", "pain", "sasori", "deidara", "hidan"]
            adults = ["shizune", "hiashi", "tsume", "choza", "inoichi", "shikaku", "might_guy"]
            villains = ["orochimaru", "kabuto", "danzo"]

            char_lower = char_name.lower()

            if char_lower == "tsunade":
                return "main"
            elif char_lower in team_7:
                return "team_7"
            elif char_lower in rookie_9:
                return "rookie_9"
            elif char_lower in akatsuki:
                return "akatsuki"
            elif char_lower in adults:
                return "adults"
            elif char_lower in villains:
                return "villains"
            else:
                return "andere"

        except Exception:
            return "andere"

    def get_relationship_level_text(self, bindung):
        """Konvertiert numerischen Bindungswert zu Text sicher"""
        try:
            bindung = int(bindung)
        except (ValueError, TypeError):
            bindung = 0

        if bindung >= 150:
            return "Unzertrennlich 💕"
        elif bindung >= 100:
            return "Bester Freund 💙"
        elif bindung >= 75:
            return "Enger Freund 😊"
        elif bindung >= 50:
            return "Guter Freund 🙂"
        elif bindung >= 25:
            return "Freundlich 😌"
        elif bindung >= 10:
            return "Positiv 🙂"
        elif bindung >= -10:
            return "Neutral 😐"
        elif bindung >= -25:
            return "Kühl 😕"
        elif bindung >= -50:
            return "Misstrauisch 😠"
        elif bindung >= -75:
            return "Feindlich 😡"
        elif bindung >= -100:
            return "Verhasst 🤬"
        else:
            return "Todesfeind ☠️"

    def get_relationship_info(self, character):
        """Gibt Beziehungsinfo für einen Charakter zurück"""
        try:
            if character in self.relationships:
                return self.relationships[character].copy()
            else:
                return {"level": 0, "titel": "Neutral 😐", "gruppe": "andere"}
        except Exception:
            return {"level": 0, "titel": "Neutral 😐", "gruppe": "andere"}

    def get_relationship_level(self, character):
        """Gibt nur das Level zurück (für Secret System Kompatibilität)"""
        try:
            info = self.get_relationship_info(character)
            return info.get("level", 0)
        except Exception:
            return 0

    def change_relationship(self, character, amount, reason="", show_message=True):
        """Ändert Beziehung und aktualisiert die Anzeige sicher"""
        try:
            # Stelle sicher dass Charakter existiert
            if character not in self.relationships:
                self.relationships[character] = {
                    "level": 0,
                    "titel": "Neutral 😐",
                    "gruppe": self.get_character_group(character)
                }

            # Sichere Wert-Extraktion
            old_level = self.relationships[character].get("level", 0)
            try:
                old_level = int(old_level)
            except (ValueError, TypeError):
                old_level = 0

            try:
                amount = int(amount)
            except (ValueError, TypeError):
                amount = 0

            # Berechne neuen Level
            new_level = old_level + amount
            new_level = max(-200, min(200, new_level))  # Begrenze auf -200 bis +200

            # Aktualisiere Relationship
            self.relationships[character]["level"] = new_level
            self.relationships[character]["titel"] = self.get_relationship_level_text(new_level)

            # Aktualisiere game_state sicher
            try:
                if character in self.game_state:
                    if isinstance(self.game_state[character], dict):
                        self.game_state[character]["bindung_sukuna"] = new_level
                    else:
                        self.game_state[character] = {"bindung_sukuna": new_level}
                else:
                    self.game_state[character] = {"bindung_sukuna": new_level}
            except Exception as e:
                print(f"⚠️ Game State Update Fehler: {e}")

            # Zeige Nachricht sicher
            try:
                if show_message and abs(amount) >= 3 and self.gui and hasattr(self.gui, 'display_message'):
                    emoji = "💚" if amount > 0 else "💔"
                    direction = "verbessert" if amount > 0 else "verschlechtert"

                    message = f"{emoji} Beziehung zu {character.title()} {direction} ({amount:+d})"
                    if reason:
                        message += f" - {reason}"

                    # Verwende display_message falls verfügbar
                    color = "success" if amount > 0 else "danger"
                    self.gui.display_message("BEZIEHUNG", message, color)
            except Exception as e:
                print(f"⚠️ GUI Message Fehler: {e}")

            # Aktualisiere Anzeige
            try:
                self.refresh_display()
            except Exception as e:
                print(f"⚠️ Display Refresh Fehler: {e}")

            return True

        except Exception as e:
            print(f"❌ Relationship Change Fehler für {character}: {e}")
            return False

    def modify_relationship(self, character, amount, reason=""):
        """Alias für change_relationship (Secret System Kompatibilität)"""
        return self.change_relationship(character, amount, reason, show_message=False)

    def refresh_display(self):
        """Aktualisiert die Beziehungsanzeige sicher"""
        if not self.gui or not hasattr(self.gui, 'relationships_display'):
            return

        try:
            content = "💕 BEZIEHUNGEN ZU SUKUNA\n\n"

            # Gruppiere Beziehungen
            groups = {
                "main": "👑 HAUPTCHARAKTERE",
                "team_7": "🥷 TEAM 7",
                "rookie_9": "👥 ROOKIE 9",
                "adults": "👨‍🦳 ERWACHSENE",
                "akatsuki": "⚡ AKATSUKI",
                "villains": "💀 SCHURKEN",
                "andere": "❓ ANDERE"
            }

            for group_key, group_title in groups.items():
                group_chars = [(name, data) for name, data in self.relationships.items()
                               if data.get("gruppe", "andere") == group_key]

                if group_chars:
                    content += f"{group_title}\n"
                    group_chars.sort(key=lambda x: x[1].get("level", 0), reverse=True)

                    for char_name, char_data in group_chars:
                        level = char_data.get("level", 0)
                        titel = char_data.get("titel", "Neutral 😐")
                        content += f"  {char_name.title()}: {level} - {titel}\n"

                    content += "\n"

            # Aktualisiere Display
            if hasattr(self.gui.relationships_display, 'config'):
                self.gui.relationships_display.config(state="normal")
                self.gui.relationships_display.delete("1.0", "end")
                self.gui.relationships_display.insert("1.0", content)
                self.gui.relationships_display.config(state="disabled")

        except Exception as e:
            print(f"❌ Display Refresh Fehler: {e}")
            try:
                # Fallback-Anzeige
                fallback_content = f"❌ FEHLER beim Laden der Beziehungen: {e}\n\n"
                fallback_content += "💡 Stelle sicher dass alle Module verfügbar sind."

                if hasattr(self.gui.relationships_display, 'config'):
                    self.gui.relationships_display.config(state="normal")
                    self.gui.relationships_display.delete("1.0", "end")
                    self.gui.relationships_display.insert("1.0", fallback_content)
                    self.gui.relationships_display.config(state="disabled")
            except:
                pass  # Silent fallback failure

    def get_all_relationships(self):
        """Gibt alle Beziehungen zurück sicher"""
        try:
            return self.relationships.copy()
        except Exception:
            return {}

    def reset_relationship(self, character):
        """Setzt Beziehung zurück auf 0"""
        return self.change_relationship(character, -self.get_relationship_level(character), "Reset")

    def save_relationships(self, filepath):
        """Speichert Beziehungen in Datei"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.relationships, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Relationship Save Fehler: {e}")
            return False

    def load_relationships(self, filepath):
        """Lädt Beziehungen aus Datei"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.relationships = json.load(f)
            self.refresh_display()
            return True
        except Exception as e:
            print(f"❌ Relationship Load Fehler: {e}")
            return False


# Legacy Kompatibilität
RelationshipSystem = FixedRelationshipSystem

if __name__ == "__main__":
    print("🔧 FIXED RELATIONSHIP SYSTEM")
    print("=======================================")
    print("✅ Verbesserte Fehlerbehandlung")
    print("✅ Sichere String-Operationen")
    print("✅ Robuste Daten-Extraktion")
    print("✅ Secret System Kompatibilität")
    print("✅ GUI Integration")