#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Naruto RPG - Büchersystem (Überarbeitet)
Vollständiges System mit separaten Inhalts-Dateien für bessere Wartbarkeit
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class BookSystem:
    """Hauptklasse für das Büchersystem - jetzt mit modularen Inhalts-Dateien"""

    def __init__(self, game_state, gui):
        self.game_state = game_state
        self.gui = gui
        self.library_data = self._load_library_data()
        self.reading_progress = self._load_reading_progress()

    def _load_library_data(self) -> Dict:
        """Lädt die Bibliotheksdaten aus separaten Dateien"""
        library_data = {}

        # Tsunades Bibliothek laden
        try:
            from buecher_tsunade_inhalt import get_tsunades_library
            library_data["tsunades_haus"] = get_tsunades_library()
            print("✅ Tsunades Bibliothek geladen")
        except ImportError as e:
            print(f"⚠️ Tsunades Bibliothek nicht gefunden: {e}")
            library_data["tsunades_haus"] = self._get_fallback_tsunade_library()

        # Konoha Bibliothek laden
        try:
            from buecher_konoha_inhalt import get_konoha_library
            library_data["konoha_bibliothek"] = get_konoha_library()
            print("✅ Konohas Bibliothek geladen")
        except ImportError as e:
            print(f"⚠️ Konohas Bibliothek nicht gefunden: {e}")
            library_data["konoha_bibliothek"] = self._get_fallback_konoha_library()

        # Weitere Bibliotheken können hier hinzugefügt werden
        try:
            from buecher_geheim_inhalt import get_secret_library
            library_data["geheimbibliothek"] = get_secret_library()
            print("✅ Geheimbibliothek geladen")
        except ImportError:
            # Geheimbibliothek ist optional
            pass

        return library_data

    def _get_fallback_tsunade_library(self) -> Dict:
        """Fallback für Tsunades Bibliothek wenn Datei fehlt"""
        return {
            "location_name": "Tsunades Bibliothek (Fallback)",
            "description": "Basis-Bibliothek - Inhalts-Datei fehlt!",
            "access_level": "private",
            "books": {
                "basis_buch": {
                    "title": "Basis-Medizinisches Handbuch",
                    "author": "Konoha Medical Corps",
                    "location": "Tsunades Arbeitszimmer",
                    "type": "medizin",
                    "access_required": "tsunade_permission",
                    "reading_time_minutes": 30,
                    "chapters": {
                        "1": {
                            "title": "Grundlagen",
                            "content": "Dies ist ein Fallback-Buch. Bitte füge buecher_tsunade_inhalt.py hinzu für vollständigen Inhalt.",
                            "knowledge_gain": {"medical_basics": 10}
                        }
                    }
                }
            }
        }

    def _get_fallback_konoha_library(self) -> Dict:
        """Fallback für Konoha Bibliothek wenn Datei fehlt"""
        return {
            "location_name": "Konoha Bibliothek (Fallback)",
            "description": "Basis-Bibliothek - Inhalts-Datei fehlt!",
            "access_level": "public",
            "books": {
                "basis_geschichte": {
                    "title": "Grundlagen der Ninja-Geschichte",
                    "author": "Historiker-Gilde",
                    "location": "Geschichtsabteilung",
                    "type": "geschichte",
                    "reading_time_minutes": 20,
                    "chapters": {
                        "1": {
                            "title": "Dorfgründung",
                            "content": "Dies ist ein Fallback-Buch. Bitte füge buecher_konoha_inhalt_backup.py hinzu für vollständigen Inhalt.",
                            "knowledge_gain": {"basic_history": 10}
                        }
                    }
                }
            }
        }

    def _load_reading_progress(self) -> Dict:
        """Lädt den Lesefortschritt des Spielers"""
        return self.game_state.get("reading_progress", {})

    def _save_reading_progress(self):
        """Speichert den Lesefortschritt"""
        if "reading_progress" not in self.game_state:
            self.game_state["reading_progress"] = {}
        self.game_state["reading_progress"] = self.reading_progress

    def get_available_books(self, location: str) -> Dict:
        """Gibt verfügbare Bücher an einem Ort zurück"""
        if location not in self.library_data:
            return {}

        location_data = self.library_data[location]
        available_books = {}

        for book_id, book_data in location_data["books"].items():
            if self._can_access_book(book_data):
                available_books[book_id] = book_data

        return available_books

    def _can_access_book(self, book_data: Dict) -> bool:
        """Prüft ob der Spieler Zugang zu einem Buch hat"""
        access_required = book_data.get("access_required", "none")

        if access_required == "none":
            return True
        elif access_required == "tsunade_permission":
            # 🔓 VEREINFACHT: Tsunade erlaubt Sukuna fast alles zu lesen
            return True
        elif access_required == "uzumaki_bloodline":
            # Sukuna hat Uzumaki-Blut
            return True
        elif access_required == "medical_interest":
            # 🔓 VEREINFACHT: Sukuna kann medizinische Bücher lesen
            return True
        elif access_required == "chakra_mastery":
            # 🔓 VEREINFACHT: Sukuna kann Chakra-Bücher lesen
            return True
        elif access_required == "very_high_relationship":
            # Sehr hohe Beziehung zu Tsunade erforderlich
            tsunade_relationship = self.game_state.get("relationships", {}).get("tsunade", {}).get("level", 0)
            return tsunade_relationship >= 200
        elif access_required == "hokage_clearance":
            # Nur mit höchster Berechtigung
            return False  # Sukuna ist noch zu jung

        return False

    def read_book(self, location: str, book_id: str, chapter_num: int = 1) -> Tuple[bool, str]:
        """Liest ein Kapitel eines Buches"""
        if location not in self.library_data:
            return False, "❌ Dieser Ort existiert nicht!"

        location_data = self.library_data[location]
        if book_id not in location_data["books"]:
            return False, "❌ Dieses Buch existiert nicht!"

        book_data = location_data["books"][book_id]

        if not self._can_access_book(book_data):
            return False, f"❌ Du hast keinen Zugang zu '{book_data['title']}'!"

        if str(chapter_num) not in book_data["chapters"]:
            return False, f"❌ Kapitel {chapter_num} existiert nicht!"

        chapter = book_data["chapters"][str(chapter_num)]

        # Prüfe Anforderungen für das Kapitel
        requirements = chapter.get("requirements", {})
        if not self._check_requirements(requirements):
            return False, "❌ Du erfüllst die Anforderungen für dieses Kapitel nicht!"

        # Markiere als gelesen
        if book_id not in self.reading_progress:
            self.reading_progress[book_id] = {"chapters_read": [], "time_spent": 0}

        if chapter_num not in self.reading_progress[book_id]["chapters_read"]:
            self.reading_progress[book_id]["chapters_read"].append(chapter_num)

        # Füge Lesezeit hinzu
        reading_time = book_data.get("reading_time_minutes", 30) // len(book_data["chapters"])
        self.reading_progress[book_id]["time_spent"] += reading_time

        # Wissensgewinn anwenden
        self._apply_knowledge_gain(chapter.get("knowledge_gain", {}))

        # Emotionale Auswirkungen
        emotional_impact = chapter.get("emotional_impact")
        if emotional_impact:
            self._apply_emotional_impact(emotional_impact)

        # Spezielle Freischaltungen
        special_unlock = chapter.get("special_unlock")
        if special_unlock:
            self._handle_special_unlock(special_unlock)

        # Korruptionsrisiko prüfen
        if chapter.get("corruption_risk"):
            self._handle_corruption_risk()

        self._save_reading_progress()

        # Formatiere die Ausgabe
        response = f"""📖 **{book_data['title']}**
📍 *{book_data.get('location', 'Unbekannter Ort')}*
✍️ *von {book_data['author']}*

**Kapitel {chapter_num}: {chapter['title']}**

{chapter['content']}

---
⏱️ Lesezeit: {reading_time} Minuten
"""

        # Wissensgewinn anzeigen
        if chapter.get("knowledge_gain"):
            response += f"\n🧠 **Wissen erhalten:**\n"
            for skill, amount in chapter["knowledge_gain"].items():
                response += f"   • {skill.replace('_', ' ').title()}: +{amount}\n"

        # Spezielle Effekte anzeigen
        if special_unlock:
            response += f"\n🔓 **Besonderes freigeschaltet:** {special_unlock}\n"

        if emotional_impact:
            response += f"\n💭 **Emotionale Wirkung:** {emotional_impact}\n"

        return True, response

    def _check_requirements(self, requirements: Dict) -> bool:
        """Prüft ob Anforderungen erfüllt sind"""
        for req, value in requirements.items():
            if req == "uzumaki_bloodline" and value:
                return True  # Sukuna hat Uzumaki-Blut
            elif req == "relationship_level":
                tsunade_level = self.game_state.get("relationships", {}).get("tsunade", {}).get("level", 0)
                if tsunade_level < value:
                    return False
            elif req in ["fuinjutsu", "chakra_control", "medical_knowledge", "mental_strength"]:
                current_level = self.game_state.get("skills", {}).get(req, 0)
                if current_level < value:
                    return False
        return True

    def _apply_knowledge_gain(self, knowledge_gain: Dict):
        """Wendet Wissensgewinn an"""
        if "skills" not in self.game_state:
            self.game_state["skills"] = {}

        for skill, amount in knowledge_gain.items():
            current = self.game_state["skills"].get(skill, 0)
            self.game_state["skills"][skill] = current + amount

    def _apply_emotional_impact(self, impact: str):
        """Wendet emotionale Auswirkungen an"""
        if impact == "deep_connection_to_heritage":
            # Stärkt Verbindung zur Uzumaki-Herkunft
            if "emotional_state" not in self.game_state:
                self.game_state["emotional_state"] = {}
            self.game_state["emotional_state"]["uzumaki_connection"] = True

            # Beziehung zu Tsunade stärken
            if "relationships" in self.game_state and "tsunade" in self.game_state["relationships"]:
                self.game_state["relationships"]["tsunade"]["level"] += 10

        elif impact == "overwhelming_love":
            # Massive Beziehungsstärkung zu Tsunade
            if "relationships" in self.game_state and "tsunade" in self.game_state["relationships"]:
                self.game_state["relationships"]["tsunade"]["level"] += 25

    def _handle_special_unlock(self, unlock: str):
        """Behandelt spezielle Freischaltungen"""
        if unlock == "mitos_chakra_crystal":
            # Mitos Chakra-Kristall freischalten
            if "special_items" not in self.game_state:
                self.game_state["special_items"] = {}
            self.game_state["special_items"]["mitos_chakra_crystal"] = {
                "name": "Mitos Chakra-Kristall",
                "description": "Ein Notfall-Energiespeicher der ersten Jinchuriki",
                "power": 1000,
                "uses": 1
            }
            self.gui.add_message("BESONDERES",
                                 "🔮 Du hast Mitos geheimen Chakra-Kristall entdeckt! Ein mächtiger Notfall-Energiespeicher.",
                                 self.gui.colors["success"])

    def _handle_corruption_risk(self):
        """Behandelt Korruptionsrisiko beim Lesen verbotener Techniken"""
        # Warnung ausgeben - könnte mentale Auswirkungen haben
        self.gui.add_message("WARNUNG",
                             "⚠️ Das Lesen verbotener Techniken kann deine Weltanschauung beeinflussen...",
                             self.gui.colors["warning"])

    def get_library_command_help(self) -> str:
        """Gibt Hilfe für Bibliotheks-Befehle zurück"""
        available_locations = list(self.library_data.keys())
        location_list = "`, `/bibliothek ".join(available_locations)

        return f"""📚 **BIBLIOTHEKS-BEFEHLE:**

🏛️ **Verfügbare Bibliotheken:**
   • `/bibliothek {location_list}`

📖 **Lesen:**
   • `/lesen <buch_id> <kapitel>` - Lese ein spezifisches Kapitel

📊 **Fortschritt:**
   • `/lesestatistik` - Zeige deinen Lesefortschritt
   • `/lesezeichen` - Gespeicherte Lesezeichen (bald verfügbar)

💡 **Beispiele:**
   • `/bibliothek tsunades_haus` - Tsunades Privatbibliothek
   • `/lesen gesetzbuch_konoha 1` - Kapitel 1 des Gesetzbuchs
   • `/lesen mito_fuinjutsu_notizen 2` - Bijuu-Versiegelungstechniken

💡 **Tipps:**
   • Manche Bücher erfordern bestimmte Fähigkeiten oder Beziehungen
   • Lesen verbessert dein Wissen und kann neue Möglichkeiten eröffnen
   • Als Uzumaki hast du Zugang zu speziellen Fuinjutsu-Texten!"""

    def process_library_command(self, command: str) -> Tuple[bool, str]:
        """Verarbeitet Bibliotheks-Befehle"""
        parts = command.lower().split()

        if len(parts) == 0:
            return False, "❌ Ungültiger Befehl!"

        action = parts[0]

        if action == "/bibliothek":
            if len(parts) < 2:
                return True, self.get_library_command_help()

            location = parts[1]
            if location not in self.library_data:
                available = ", ".join(self.library_data.keys())
                return True, f"❌ Unbekannte Bibliothek '{location}'!\n\nVerfügbar: {available}"

            books = self.get_available_books(location)

            if not books:
                return True, f"❌ Keine Bücher verfügbar in {location}!\n(Möglicherweise fehlen Zugangsberechtigungen)"

            location_data = self.library_data[location]
            response = f"📚 **{location_data['location_name']}**\n"
            response += f"📝 {location_data['description']}\n\n"

            for book_id, book_data in books.items():
                chapters_read = len(self.reading_progress.get(book_id, {}).get("chapters_read", []))
                total_chapters = len(book_data["chapters"])
                progress = f"({chapters_read}/{total_chapters})"

                response += f"📖 **{book_data['title']}**\n"
                response += f"   ✍️ von {book_data['author']}\n"
                response += f"   📍 {book_data.get('location', 'Unbekannter Ort')}\n"
                response += f"   📊 Fortschritt: {progress}\n"
                response += f"   🔍 `/lesen {book_id} 1` um zu beginnen\n\n"

            return True, response

        elif action == "/lesen":
            if len(parts) < 3:
                return True, "❌ Verwendung: `/lesen <buch_id> <kapitel_nummer>`"

            book_id = parts[1]
            try:
                chapter_num = int(parts[2])
            except ValueError:
                return True, "❌ Kapitel-Nummer muss eine Zahl sein!"

            # Finde das Buch in allen Bibliotheken
            for location, location_data in self.library_data.items():
                if book_id in location_data["books"]:
                    success, response = self.read_book(location, book_id, chapter_num)
                    return True, response

            return True, f"❌ Buch '{book_id}' nicht gefunden!"

        elif action == "/lesestatistik":
            return True, self._get_reading_statistics()

        elif action == "/lesezeichen":
            return True, "📑 Lesezeichen-Feature kommt bald!"

        return False, "❌ Unbekannter Bibliotheks-Befehl!"

    def _get_reading_statistics(self) -> str:
        """Gibt Lesestatistiken zurück"""
        if not self.reading_progress:
            return "📊 Du hast noch keine Bücher gelesen!\n\n💡 Versuche `/bibliothek tsunades_haus` um zu beginnen."

        response = "📊 **DEINE LESESTATISTIKEN:**\n\n"
        total_time = 0
        total_chapters = 0

        for book_id, progress in self.reading_progress.items():
            # Finde Buchtitel
            book_title = "Unbekanntes Buch"
            for location_data in self.library_data.values():
                if book_id in location_data["books"]:
                    book_title = location_data["books"][book_id]["title"]
                    break

            chapters_read = len(progress["chapters_read"])
            time_spent = progress["time_spent"]

            response += f"📖 **{book_title}**\n"
            response += f"   📊 {chapters_read} Kapitel gelesen\n"
            response += f"   ⏱️ {time_spent} Minuten\n\n"

            total_chapters += chapters_read
            total_time += time_spent

        response += f"🎯 **GESAMT:**\n"
        response += f"   📚 {len(self.reading_progress)} Bücher angefangen\n"
        response += f"   📄 {total_chapters} Kapitel gelesen\n"
        response += f"   ⏰ {total_time} Minuten (≈{total_time // 60}h {total_time % 60}m)\n"

        # Wissensstand anzeigen
        skills = self.game_state.get("skills", {})
        if skills:
            response += f"\n🧠 **ERLERNTES WISSEN:**\n"
            for skill, level in sorted(skills.items()):
                if level > 0:
                    response += f"   • {skill.replace('_', ' ').title()}: {level}\n"

        return response

    def get_available_locations(self) -> List[str]:
        """Gibt verfügbare Bibliotheks-Orte zurück"""
        return list(self.library_data.keys())

    def is_book_system_command(self, command: str) -> bool:
        """Prüft ob ein Befehl zum Büchersystem gehört"""
        book_commands = ["/bibliothek", "/lesen", "/lesestatistik", "/lesezeichen"]
        return any(command.lower().startswith(cmd) for cmd in book_commands)

    def add_new_library(self, library_id: str, library_data: Dict):
        """Fügt eine neue Bibliothek hinzu (für Erweiterungen)"""
        self.library_data[library_id] = library_data
        print(f"✅ Neue Bibliothek '{library_data['location_name']}' hinzugefügt!")

    def reload_libraries(self):
        """Lädt alle Bibliotheken neu (nützlich für Entwicklung)"""
        print("🔄 Lade Bibliotheken neu...")
        self.library_data = self._load_library_data()
        print("✅ Bibliotheken neu geladen!")


# ===== INTEGRATION IN MAIN SYSTEM =====
def create_book_system(game_state, gui):
    """Factory-Funktion zum Erstellen des Büchersystems"""
    return BookSystem(game_state, gui)


# ===== TESTING =====
if __name__ == "__main__":
    # Test-Implementierung
    test_game_state = {
        "skills": {"chakra_control": 30, "medical_knowledge": 25},
        "relationships": {"tsunade": {"level": 100}}
    }


    class MockGUI:
        def __init__(self):
            self.colors = {"warning": "#orange", "success": "#green"}

        def add_message(self, sender, message, color):
            print(f"[{sender}] {message}")


    gui = MockGUI()
    book_system = BookSystem(test_game_state, gui)

    # Test verfügbare Bibliotheken
    locations = book_system.get_available_locations()
    print(f"Verfügbare Bibliotheken: {locations}")

    # Test verfügbare Bücher
    if "tsunades_haus" in locations:
        books = book_system.get_available_books("tsunades_haus")
        print(f"Verfügbare Bücher in Tsunades Haus: {list(books.keys())}")

    print("\n✅ Büchersystem erfolgreich getestet!")