#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIBLIOTHEKS-LOCATION SYSTEM für Chat RPG
Vollständige Integration von Bibliothek als neue Location mit Bücher-System
Basiert auf deinen hochgeladenen book_system.py und anderen Dateien
"""

import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class LibraryLocationSystem:
    """Erweiterte Bibliotheks-Location für das RPG mit vollständiger Integration"""

    def __init__(self, game_state, gui, encounter_system=None):
        self.game_state = game_state
        self.gui = gui
        self.encounter_system = encounter_system

        # Lade Bücher-System
        self.book_system = self._init_book_system()

        # Bibliotheks-Locations definieren
        self.library_locations = self._init_library_locations()

        # Spezielle Bibliotheks-Events
        self.library_events = self._init_library_events()

        # Bibliothekar-NPCs
        self.librarians = self._init_librarians()

    def _init_book_system(self):
        """Initialisiert das Bücher-System basierend auf deiner book_system.py"""
        try:
            # Importiere dein Bücher-System
            from book_system import BookSystem
            return BookSystem(self.game_state, self.gui)
        except ImportError:
            print("⚠️ Bücher-System nicht gefunden - verwende Fallback")
            return self._create_fallback_book_system()

    def _create_fallback_book_system(self):
        """Erstellt ein einfaches Fallback-Bücher-System"""

        class SimplebookSystem:
            def __init__(self, game_state, gui):
                self.game_state = game_state
                self.gui = gui
                self.reading_progress = game_state.get("reading_progress", {})

            def get_available_books(self, location):
                return {
                    "basis_geschichte": {
                        "title": "Geschichte von Konoha",
                        "author": "Historiker-Gilde",
                        "type": "geschichte",
                        "chapters": {"1": {"title": "Gründung", "content": "Die Geschichte der Dorfgründung..."}}
                    }
                }

            def read_book(self, location, book_id, chapter=1):
                return True, "Du liest das Buch aufmerksam..."

            def is_book_system_command(self, command):
                """Prüft ob ein Befehl zum Büchersystem gehört"""
                book_commands = ["/bibliothek", "/lesen", "/lesestatistik", "/lesezeichen"]
                return any(command.lower().startswith(cmd) for cmd in book_commands)

            def process_library_command(self, command):
                """Verarbeitet Bibliotheks-Befehle"""
                if command.lower().startswith("/bibliothek"):
                    return True, "📚 Fallback-Büchersystem: Basis-Bücher verfügbar.\n💡 Für vollständige Funktionalität füge book_system.py hinzu!"
                elif command.lower().startswith("/lesen"):
                    return True, "📖 Fallback: Buch wird gelesen...\n💡 Für vollständige Funktionalität füge book_system.py hinzu!"
                elif command.lower().startswith("/lesestatistik"):
                    return True, "📊 Keine Lesestatistiken verfügbar.\n💡 Für vollständige Funktionalität füge book_system.py hinzu!"
                else:
                    return False, "Bibliotheks-System nicht vollständig geladen."

        return SimplebookSystem(self.game_state, self.gui)

    def _init_library_locations(self) -> Dict:
        """Definiert alle Bibliotheks-Locations für das Encounter-System"""
        return {
            "konoha_hauptbibliothek": {
                "name": "Konoha Hauptbibliothek - /encounter konoha_hauptbibliothek",
                "description": "Die große öffentliche Bibliothek von Konoha mit umfangreichen Sammlungen zu Geschichte, Jutsu-Grundlagen und Kultur.",
                "base_encounter_rate": 0.4,
                "characters": {
                    "common": ["sakura", "shino", "hinata"],  # Studierende Charaktere
                    "uncommon": ["kakashi", "shikamaru", "ino"],
                    "rare": ["jiraiya"],  # Recherchiert für seine Bücher
                    "epic": [],
                    "legendary": [],
                    "mythic": []
                },
                "library_type": "public",
                "opening_hours": "06:00-22:00",
                "librarian": "mizuki_tanaka",
                "available_sections": [
                    "geschichte_abteilung",
                    "jutsu_grundlagen",
                    "kulturelle_studien",
                    "dorfgesetze",
                    "kinderbuecher",
                    "allgemeine_literatur"
                ],
                "special_features": {
                    "study_rooms": "Private Lernräume verfügbar",
                    "rare_books": "Seltene Bücher mit speziellen Zugangsberechtigungen",
                    "reading_garden": "Ruhiger Außenbereich zum Lesen"
                }
            },

            "tsunades_bibliothek": {
                "name": "Tsunades private Bibliothek - /encounter tsunades_bibliothek",
                "description": "Tsunades persönliche Bibliothek in ihrem Haus mit medizinischen Fachbüchern, Uzumaki-Aufzeichnungen und wertvollen Schriftrollen.",
                "base_encounter_rate": 0.3,
                "characters": {
                    "common": [],
                    "uncommon": ["shizune"],  # Tsunades Assistentin
                    "rare": ["tsunade"],  # Die Hausherrin
                    "epic": [],
                    "legendary": [],
                    "mythic": []
                },
                "library_type": "private_medical",
                "opening_hours": "Nach Einladung von Tsunade",
                "access_requirements": {
                    "tsunade_permission": True,
                    "relationship_level": 50  # Mindest-Beziehungslevel zu Tsunade
                },
                "available_sections": [
                    "medizin_archive",  # Tsunades medizinische Sammlung
                    "uzumaki_legacy",  # Mito's Aufzeichnungen für Sukuna
                    "sealing_techniques",  # Fuinjutsu-Schriftrollen
                    "hokage_documents",  # Persönliche Hokage-Dokumente
                    "personal_research",  # Tsunades eigene Forschung
                    "senju_heritage"  # Senju-Clan Aufzeichnungen
                ],
                "special_features": {
                    "medical_focus": "Spezialisiert auf medizinische und Heilkünste",
                    "uzumaki_access": "Besonderer Zugang für Sukuna zu Uzumaki-Erbe",
                    "private_atmosphere": "Intime, persönliche Bibliothek",
                    "tsunade_guidance": "Tsunade kann persönlich beim Lernen helfen"
                },
                "location_context": "tsunades_haus",  # Verknüpft mit Tsunades Haus
                "emotional_significance": "high"  # Wichtig für Sukuna's Entwicklung
            }
        }

    def _init_library_events(self) -> Dict:
        """Spezielle Events die in Bibliotheken auftreten können"""
        return {
            "study_group": {
                "description": "Eine Gruppe von Ninja-Akademie-Studenten diskutiert intensiv über Jutsu-Theorie.",
                "participants": ["sakura", "ino", "hinata", "shikamaru"],
                "trigger_chance": 0.3,
                "benefits": {
                    "knowledge_boost": 15,
                    "social_interaction": True
                },
                "location": "konoha_hauptbibliothek"
            },

            "rare_book_discovery": {
                "description": "Du entdeckst ein seltenes, bisher unbekanntes Buch in einem versteckten Regal.",
                "trigger_chance": 0.05,
                "benefits": {
                    "unique_knowledge": True,
                    "special_skill": True
                },
                "possible_books": [
                    "uzumaki_sealing_secrets",
                    "first_hokage_diary",
                    "lost_jutsu_scrolls",
                    "ancient_meditation_techniques"
                ]
            },

            "librarian_quest": {
                "description": "Der Bibliothekar bittet dich um Hilfe bei der Suche nach einem vermissten Buch.",
                "trigger_chance": 0.2,
                "quest_reward": {
                    "library_access": "enhanced",
                    "rare_book_permission": True,
                    "reputation_boost": 25
                }
            },

            "forbidden_section_access": {
                "description": "Du findest einen Weg, heimlich die verbotene Sektion zu betreten.",
                "trigger_chance": 0.03,
                "requirements": {
                    "stealth_skill": 30,
                    "night_time": True
                },
                "risks": {
                    "discovery_chance": 0.4,
                    "punishment": "temporary_ban"
                },
                "benefits": {
                    "forbidden_knowledge": True,
                    "kinjutsu_theory": 20
                }
            }
        }

    def _init_librarians(self) -> Dict:
        """NPCs die in Bibliotheken arbeiten"""
        return {
            "mizuki_tanaka": {
                "name": "Mizuki Tanaka",
                "role": "Hauptbibliothekar",
                "location": "konoha_hauptbibliothek",
                "personality": "Freundlich aber strikt bei Bibliotheksregeln",
                "knowledge_areas": ["Geschichte", "Dorfgesetze", "Allgemeinwissen", "Jutsu-Grundlagen"],
                "special_abilities": {
                    "book_recommendation": "Kann perfekte Bücher für deine Interessen empfehlen",
                    "research_assistance": "Hilft bei komplexen Recherchen"
                },
                "dialogue_options": [
                    "Nach Buchempfehlungen fragen",
                    "Über Bibliotheksregeln erkundigen",
                    "Hilfe bei Recherche erbitten",
                    "Nach seltenen Büchern fragen"
                ]
            },

            "tsunade": {
                "name": "Tsunade Senju",
                "role": "Besitzerin der privaten Bibliothek",
                "location": "tsunades_bibliothek",
                "personality": "Direkt und kompetent, aber warmherzig zu Sukuna",
                "knowledge_areas": ["Medizin-Ninjutsu", "Uzumaki-Geschichte", "Fuinjutsu", "Senju-Erbe"],
                "special_abilities": {
                    "medical_guidance": "Kann komplexe medizinische Techniken erklären",
                    "uzumaki_heritage": "Teilt Wissen über Sukuna's Uzumaki-Erbe",
                    "personal_mentoring": "Bietet persönliche Anleitung beim Lernen"
                },
                "special_relationship": {
                    "sukuna": "Mütterliche Figur und Mentorin",
                    "relationship_bonus": "Verbesserte Lerneffizienz wenn Tsunade anwesend ist"
                },
                "dialogue_options": [
                    "Über medizinische Techniken sprechen",
                    "Nach Uzumaki-Geschichte fragen",
                    "Um Hilfe bei Fuinjutsu bitten",
                    "Persönliche Gespräche führen"
                ]
            }
        }

    def get_library_locations_for_encounter_system(self) -> Dict:
        """Gibt alle Bibliotheks-Locations für das Encounter-System zurück"""
        return self.library_locations

    def integrate_with_encounter_system(self, encounter_system):
        """Integriert alle Bibliotheks-Locations in das bestehende Encounter-System"""
        if encounter_system and hasattr(encounter_system, 'locations'):
            # Füge alle Bibliotheks-Locations hinzu
            for loc_id, loc_data in self.library_locations.items():
                encounter_system.locations[loc_id] = loc_data
                print(f"✅ Bibliothek '{loc_data['name']}' zum Encounter-System hinzugefügt")

            print(f"📚 {len(self.library_locations)} Bibliotheks-Locations erfolgreich integriert!")
        else:
            print("⚠️ Encounter-System nicht verfügbar für Integration")

    def integrate_with_environment_system(self, environment_system):
        """Integriert Bibliotheks-Umgebungen in das Environment-System"""
        if environment_system and hasattr(environment_system, 'environment_details'):
            library_environments = self._create_library_environments()

            for loc_id, env_data in library_environments.items():
                environment_system.environment_details[loc_id] = env_data
                print(f"🏛️ Bibliotheks-Umgebung '{loc_id}' hinzugefügt")

    def _create_library_environments(self) -> Dict:
        """Erstellt detaillierte Umgebungsbeschreibungen für Bibliotheken"""
        return {
            "konoha_hauptbibliothek": {
                "base_description": "Eine beeindruckende, mehrstöckige Bibliothek mit hohen Regalen voller Wissen",
                "detailed_description": {
                    "architecture": "Hohe Holzregale reichen bis zur verzierten Decke, verbunden durch elegante Wendeltreppen",
                    "atmosphere": "Ehrfurchtgebietende Stille, nur unterbrochen vom leisen Umblättern der Seiten und gedämpften Schritten",
                    "landmarks": ["der zentrale Lesekuppel mit Oberlicht", "antike Kartenkataloge",
                                  "gemütliche Leseecken mit weichen Kissen"],
                    "smells": ["alter Bucheinband", "Tinte", "schwacher Weihrauch", "Staub von Jahrhunderten"],
                    "textures": ["glattes Papier", "weiches Leder der Einbände", "kühles Holz der Regale"]
                },
                "special_features": {
                    "quiet_hours": "Absolute Stille für tiefes Studium",
                    "research_peak": "Geschäftiges Treiben mit vielen Gelehrten",
                    "evening_atmosphere": "Warmes Kerzenlicht schafft eine magische Stimmung"
                }
            },

            "tsunades_bibliothek": {
                "base_description": "Eine persönliche, gemütliche Bibliothek in Tsunades Haus voller medizinischer Fachbücher und persönlicher Erinnerungen",
                "detailed_description": {
                    "architecture": "Dunkle Holzregale mit medizinischen Fachbüchern, antiken Schriftrollen und persönlichen Aufzeichnungen",
                    "atmosphere": "Warme, private Atmosphäre mit dem Duft von Heilkräutern und einer persönlichen Note",
                    "landmarks": ["Tsunades persönlicher Schreibtisch", "Sammlung medizinischer Instrumente",
                                  "Mitos versiegelte Schriftrollen in einer Ehrenecke"],
                    "smells": ["Heilkräuter und medizinische Tinkturen", "altes Pergament", "Tsunades subtiles Parfüm"],
                    "textures": ["weiches Leder der medizinischen Handbücher", "glatte Schriftrollenoberflächen",
                                 "warmes Holz des Schreibtisches"]
                },
                "special_features": {
                    "medical_focus": "Überall sind medizinische Diagramme und Kräuterproben zu sehen",
                    "uzumaki_corner": "Eine spezielle Ecke mit Mitos Uzumaki-Aufzeichnungen für Sukuna",
                    "tsunade_presence": "Tsunades persönliche Gegenstände machen die Bibliothek sehr persönlich",
                    "healing_atmosphere": "Die Luft ist erfüllt von heilender Energie und Ruhe"
                }
            }
        }

    def visit_library(self, location: str, player_action: str = "browse") -> Dict:
        """Hauptfunktion für Bibliotheksbesuche"""
        if location not in self.library_locations:
            return {"success": False, "message": "📚 Diese Bibliothek existiert nicht!"}

        library_data = self.library_locations[location]

        # Prüfe Zugangsberechtigung
        access_check = self._check_library_access(location)
        if not access_check["allowed"]:
            return {"success": False, "message": f"❌ {access_check['reason']}"}

        result = {
            "success": True,
            "location": location,
            "library_name": library_data["name"],
            "description": library_data["description"],
            "available_actions": self._get_available_library_actions(location),
            "current_books": self.book_system.get_available_books(location),
            "librarian": self.librarians.get(library_data.get("librarian")),
            "special_events": self._check_for_library_events(location)
        }

        # Führe spezifische Aktion aus
        if player_action == "browse":
            result["action_result"] = self._browse_books(location)
        elif player_action == "study":
            result["action_result"] = self._study_in_library(location)
        elif player_action == "ask_librarian":
            result["action_result"] = self._interact_with_librarian(location)
        elif player_action == "explore":
            result["action_result"] = self._explore_library(location)

        return result

    def _check_library_access(self, location: str) -> Dict:
        """Prüft ob der Spieler Zugang zur Bibliothek hat"""
        library_data = self.library_locations[location]
        requirements = library_data.get("access_requirements", {})

        if not requirements:
            return {"allowed": True}


        # Prüfe Rang-Anforderungen (falls vorhanden)
        if "rank" in requirements:
            player_rank = self.game_state.get("rank", "genin")
            required_rank = requirements["rank"]
            if player_rank != required_rank and player_rank not in ["jonin", "hokage"]:
                return {
                    "allowed": False,
                    "reason": f"Zugang erfordert mindestens {required_rank.title()}-Rang!"
                }

        # Prüfe spezielle Berechtigung
        if requirements.get("special_permission"):
            permissions = self.game_state.get("special_permissions", [])
            if "library_access" not in permissions:
                return {
                    "allowed": False,
                    "reason": "Du benötigst eine spezielle Berechtigung!"
                }

        return {"allowed": True}

    def _get_available_library_actions(self, location: str) -> List[str]:
        """Gibt verfügbare Aktionen in der Bibliothek zurück"""
        base_actions = ["browse", "study", "ask_librarian"]

        library_data = self.library_locations[location]

        if location == "geheimbibliothek":
            base_actions.append("explore_forbidden_section")

        if "study_rooms" in library_data.get("special_features", {}):
            base_actions.append("reserve_study_room")

        return base_actions

    def _check_for_library_events(self, location: str) -> List[Dict]:
        """Prüft auf spezielle Events in der Bibliothek"""
        active_events = []

        for event_id, event_data in self.library_events.items():
            # Prüfe ob Event in dieser Location möglich ist
            if event_data.get("location", location) != location:
                continue

            # Prüfe Wahrscheinlichkeit
            if random.random() < event_data.get("trigger_chance", 0.1):
                active_events.append({
                    "id": event_id,
                    "description": event_data["description"],
                    "benefits": event_data.get("benefits", {}),
                    "requirements": event_data.get("requirements", {})
                })

        return active_events

    def _browse_books(self, location: str) -> Dict:
        """Durchstöbern der verfügbaren Bücher"""
        books = self.book_system.get_available_books(location)

        if not books:
            return {
                "action": "browse",
                "result": "📚 Diese Bibliothek scheint leer zu sein oder du hast keinen Zugang zu den Büchern."
            }

        book_list = []
        for book_id, book_data in books.items():
            book_list.append(f"📖 **{book_data['title']}** von {book_data['author']}")

        return {
            "action": "browse",
            "result": f"📚 Du durchstöberst die Regale und findest folgende Bücher:\n\n" + "\n".join(book_list) +
                      f"\n\n💡 Verwende `/lesen <buch_id> <kapitel>` um ein Buch zu lesen!"
        }

    def _study_in_library(self, location: str) -> Dict:
        """Studieren in der Bibliothek für Skill-Bonus"""
        library_data = self.library_locations[location]
        study_bonus = 1.2  # 20% Bonus auf Wissenserwerb in Bibliotheken

        if location == "geheimbibliothek":
            study_bonus = 1.5  # 50% Bonus für geheime Bibliothek
        elif location == "akademie_bibliothek":
            study_bonus = 1.1  # 10% Bonus für Akademie

        return {
            "action": "study",
            "result": f"📖 Du verbringst Zeit mit intensivem Studium. Deine Lerneffizienz ist um {int((study_bonus - 1) * 100)}% erhöht!",
            "bonus_multiplier": study_bonus
        }

    def _interact_with_librarian(self, location: str) -> Dict:
        """Interaktion mit dem Bibliothekar"""
        library_data = self.library_locations[location]
        librarian_id = library_data.get("librarian")

        if not librarian_id or librarian_id not in self.librarians:
            return {
                "action": "ask_librarian",
                "result": "📚 Momentan ist kein Bibliothekar anwesend."
            }

        librarian = self.librarians[librarian_id]

        # Zufällige hilfreiche Aktion des Bibliothekars
        actions = [
            f"📚 {librarian['name']} empfiehlt dir ein Buch basierend auf deinen Interessen.",
            f"🔍 {librarian['name']} hilft dir bei deiner Recherche und zeigt dir versteckte Ressourcen.",
            f"📖 {librarian['name']} erzählt dir interessante Geschichten über die Geschichte der Bibliothek.",
            f"💡 {librarian['name']} gibt dir Tipps für effektiveres Studieren."
        ]

        return {
            "action": "ask_librarian",
            "result": random.choice(actions),
            "librarian": librarian
        }

    def _explore_library(self, location: str) -> Dict:
        """Erkunde versteckte Bereiche der Bibliothek"""
        discovery_chance = 0.3

        if random.random() < discovery_chance:
            discoveries = [
                "🗃️ Du findest einen versteckten Bereich mit alten Dokumenten.",
                "📜 Ein geheimer Durchgang führt zu einem privaten Studienbereich.",
                "🔐 Du entdeckst einen versiegelten Schrank mit seltenen Schriftrollen.",
                "📚 Ein alter Gelehrter hat persönliche Notizen in den Büchern hinterlassen."
            ]

            return {
                "action": "explore",
                "result": random.choice(discoveries),
                "discovery": True
            }
        else:
            return {
                "action": "explore",
                "result": "🔍 Du durchsuchst die Bibliothek gründlich, findest aber nichts Besonderes.",
                "discovery": False
            }

    def process_library_commands(self, command: str) -> Tuple[bool, str]:
        """Verarbeitet spezielle Bibliotheks-Befehle"""
        parts = command.lower().split()

        if not parts:
            return False, "❌ Ungültiger Befehl!"

        action = parts[0]

        # Bibliotheks-spezifische Befehle
        if action == "/bibliotheken":
            return True, self._list_all_libraries()
        elif action == "/bibliothekar":
            if len(parts) < 2:
                return True, "❌ Verwendung: `/bibliothekar <bibliothek>`"
            location = parts[1]
            return True, self._get_librarian_info(location)
        elif action == "/bibliothek_hilfe":
            return True, self._get_library_help()

        # Leite Standard-Buchbefehle an das Buchsystem weiter
        if self.book_system and self.book_system.is_book_system_command(command):
            return self.book_system.process_library_command(command)

        return False, "❌ Unbekannter Bibliotheks-Befehl!"

    def _list_all_libraries(self) -> str:
        """Listet alle verfügbaren Bibliotheken auf"""
        response = "📚 **VERFÜGBARE BIBLIOTHEKEN:**\n\n"

        for loc_id, lib_data in self.library_locations.items():
            access_check = self._check_library_access(loc_id)
            access_status = "✅" if access_check["allowed"] else "🔒"

            response += f"{access_status} **{lib_data['name'].split(' - ')[0]}**\n"
            response += f"   📍 `/encounter {loc_id}` zum Besuchen\n"
            response += f"   📝 {lib_data['description'][:100]}...\n"

            if not access_check["allowed"]:
                response += f"   🚫 {access_check['reason']}\n"

            response += "\n"

        response += "💡 **Tipps:**\n"
        response += "• Verwende `/encounter <bibliothek>` um eine Bibliothek zu besuchen\n"
        response += "• In Bibliotheken kannst du mit `/bibliothek <ort>` verfügbare Bücher sehen\n"
        response += "• Lese Bücher mit `/lesen <buch_id> <kapitel>`\n"
        response += "• Als Uzumaki hast du speziellen Zugang zu Tsunades medizinischen und Fuinjutsu-Sammlungen!\n"

        return response

    def _get_librarian_info(self, location: str) -> str:
        """Gibt Informationen über den Bibliothekar zurück"""
        if location not in self.library_locations:
            return f"❌ Bibliothek '{location}' existiert nicht!"

        library_data = self.library_locations[location]
        librarian_id = library_data.get("librarian")

        if not librarian_id or librarian_id not in self.librarians:
            return f"📚 In der {library_data['name']} ist momentan kein Bibliothekar anwesend."

        librarian = self.librarians[librarian_id]

        response = f"👨‍🏫 **{librarian['name']}**\n"
        response += f"🏛️ **Position:** {librarian['role']}\n"
        response += f"📍 **Standort:** {library_data['name']}\n"
        response += f"🧠 **Persönlichkeit:** {librarian['personality']}\n\n"

        response += f"📚 **Fachgebiete:**\n"
        for area in librarian['knowledge_areas']:
            response += f"   • {area}\n"

        if 'special_abilities' in librarian:
            response += f"\n✨ **Besondere Fähigkeiten:**\n"
            for ability, desc in librarian['special_abilities'].items():
                response += f"   • {desc}\n"

        return response

    def _get_library_help(self) -> str:
        """Gibt Hilfe für das Bibliotheks-System zurück"""
        return """📚 **BIBLIOTHEKS-SYSTEM HILFE:**

🏛️ **Bibliotheken besuchen:**
   • `/encounter <bibliothek>` - Besuche eine Bibliothek
   • `/bibliotheken` - Liste aller verfügbaren Bibliotheken

📖 **Bücher-Befehle:**
   • `/bibliothek <ort>` - Zeige verfügbare Bücher
   • `/lesen <buch_id> <kapitel>` - Lese ein Kapitel
   • `/lesestatistik` - Deine Lesestatistiken

👨‍🏫 **Bibliothekar-Interaktion:**
   • `/bibliothekar <bibliothek>` - Info über den Bibliothekar
   • Im Spiel: Spreche direkt mit NPCs

🎯 **Bibliotheks-Aktionen:**
   • **Browse** - Durchstöbere verfügbare Bücher  
   • **Study** - Studiere für Lernbonus
   • **Ask Librarian** - Bitte um Hilfe
   • **Explore** - Suche nach versteckten Bereichen

💡 **Tipps:**
   • Manche Bibliotheken erfordern spezielle Berechtigungen
   • Studieren in Bibliotheken gibt Lernboni
   • Seltene Events können zusätzliche Belohnungen bringen
   • Als Uzumaki hast du Zugang zu speziellen Versiegelungs-Texten!"""


# =================================================================
# INTEGRATION FUNKTIONEN
# =================================================================

def integrate_library_system(main_game, encounter_system=None, environment_system=None):
    """Integriert das Bibliotheks-System in das Hauptspiel"""

    # Erstelle Bibliotheks-System
    library_system = LibraryLocationSystem(
        main_game.game_state if hasattr(main_game, 'game_state') else {},
        main_game.gui if hasattr(main_game, 'gui') else None,
        encounter_system
    )

    # Integriere in Encounter-System
    if encounter_system:
        library_system.integrate_with_encounter_system(encounter_system)

    # Integriere in Environment-System
    if environment_system:
        library_system.integrate_with_environment_system(environment_system)

    print("📚✅ Bibliotheks-System vollständig integriert!")
    return library_system


def setup_library_integration_for_existing_game(game_instance):
    """Setup-Funktion für bestehende Spiele"""

    # Finde Encounter-System
    encounter_system = None
    if hasattr(game_instance, 'encounter_system'):
        encounter_system = game_instance.encounter_system
    elif hasattr(game_instance, 'simple_encounter_system'):
        encounter_system = game_instance.simple_encounter_system

    # Finde Environment-System
    environment_system = None
    if hasattr(game_instance, 'environment_system'):
        environment_system = game_instance.environment_system

    # Integriere Bibliotheks-System
    library_system = integrate_library_system(
        game_instance,
        encounter_system,
        environment_system
    )

    # Füge zur Spielinstanz hinzu
    game_instance.library_system = library_system

    return library_system


# =================================================================
# TEST FUNKTIONEN
# =================================================================

def test_library_system():
    """Test-Funktion für das Bibliotheks-System"""
    print("📚 === BIBLIOTHEKS-SYSTEM TEST ===")

    # Mock Game State und GUI
    mock_game_state = {
        "skills": {"research": 20, "reading": 15},
        "rank": "genin",
        "special_permissions": []
    }

    class MockGUI:
        def add_message(self, sender, message, color=None):
            print(f"[{sender}] {message}")

    mock_gui = MockGUI()

    # Erstelle System
    library_system = LibraryLocationSystem(mock_game_state, mock_gui)

    # Teste Bibliotheks-Locations
    locations = library_system.get_library_locations_for_encounter_system()
    print(f"\n📚 Verfügbare Bibliotheken: {list(locations.keys())}")

    # Teste Bibliotheksbesuch
    print(f"\n🏛️ Teste Bibliotheksbesuch:")
    visit_result = library_system.visit_library("konoha_hauptbibliothek", "browse")
    print(f"Besuch erfolgreich: {visit_result['success']}")

    # Teste Kommandos
    print(f"\n💬 Teste Bibliotheks-Kommandos:")
    success, response = library_system.process_library_commands("/bibliotheken")
    print(f"Kommando-Verarbeitung: {success}")

    print("\n✅ === LIBRARY TEST COMPLETE ===")


if __name__ == "__main__":
    test_library_system()