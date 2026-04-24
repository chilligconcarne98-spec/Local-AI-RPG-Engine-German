# -*- coding: utf-8 -*-
#E:\Complete own AI\system_prompts
"""
ADVANCED ENCOUNTER SYSTEM für Naruto RPG
Vollständiges System mit ALLEN Charakteren aus characters.py
Inklusive Seltenheiten, Zeitbasierte Spawns, Vollmond-Events, und mehr!
"""

import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
try:
    # Versuche zuerst normalen Import (falls backstory im selben Verzeichnis)
    from moduls.characters import get_all_characters
except ImportError:
    # Falls nicht gefunden, füge Parent-Directory zum Path hinzu
    import sys
    import os
    # Füge das Hauptverzeichnis (ein Level höher) zum Python-Path hinzu
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    from moduls.characters import get_all_characters

from moduls.modern_gui_tutorial import ModernRPGGUI

class SimpleEncounterSystem:
    """Erweiterte Begegnungen mit komplexen Spawn-Bedingungen"""

    def __init__(self, game_state, gui):
        self.game_state = game_state
        self.gui = gui
        self.encounter_history = []
        self.cooldowns = {}
        self.character_states = {}

        # Lade alle verfügbaren Charaktere
        self.all_characters = get_all_characters()

        # Initialisiere erweiterte Locations mit ALLEN Charakteren
        self.locations = self._init_advanced_locations()

        # Character Rarities (Seltenheiten)
        self.character_rarities = self._init_character_rarities()

        # Zeitbasierte Spawn-Bedingungen
        self.time_conditions = self._init_time_conditions()

        # Wetter & Mondphasen-Events
        self.special_conditions = self._init_special_conditions()

    def _init_advanced_locations(self) -> Dict:
        """Initialisiert erweiterte Locations mit allen Charakteren"""
        return {
            "dorf_zentrum": {
                "name": "Dorfzentrum - /encounter dorf_zentrum",
                "description": "Geschäftiges Zentrum von Konoha mit Marktständen",
                "base_encounter_rate": 1,
                "characters": {
                    "common": ["naruto", "sakura", "ino", "choji", "shikamaru", "kiba", "hinata", "shino"],
                    "uncommon": ["neji", "lee", "tenten", "kakashi", "kurenai", "asuma"],
                    "rare": ["guy", "shizune", "inoichi", "choza"],
                    "epic": ["tsunade", "hiashi"],
                    "legendary": ["danzo"],
                    "mythic": []
                },
                "time_modifiers": {
                    "morning": 1.2,  # 6-12
                    "afternoon": 1.5,  # 12-18
                    "evening": 0.8,  # 18-22
                    "night": 0.3  # 22-6
                }
            },

            "hokage_turm": {
                "name": "Hokage-Turm - /encounter hokage_turm",
                "description": "Administratives Zentrum, Sitz der Hokage",
                "base_encounter_rate": 0.35,
                "characters": {
                    "common": ["shizune"],
                    "uncommon": ["kakashi", "asuma", "kurenai", "guy", "inoichi"],
                    "rare": ["tsunade"],
                    "epic": ["hiashi", "danzo"],
                    "legendary": [],
                    "mythic": []
                },
                "access_requirements": {
                    "tsunade_permission_level": 50
                }
            },

            "training_area": {
                "name": "Trainingsgelände - /encounter training_area",
                "description": "Weitläufige Trainingsplätze für Ninja-Übungen",
                "base_encounter_rate": 0.65,
                "characters": {
                    "common": ["naruto", "sasuke", "sakura", "kiba", "shino", "choji"],
                    "uncommon": ["neji", "lee", "tenten", "shikamaru", "ino", "hinata"],
                    "rare": ["kakashi", "guy", "asuma", "kurenai"],
                    "epic": ["tsunade"],
                    "legendary": [],
                    "mythic": []
                }
            },

            "wald": {
                "name": "Wald von Konoha - /encounter wald",
                "description": "Dichter Wald um das Dorf - mystisch und geheimnisvoll",
                "base_encounter_rate": 0.55,
                "characters": {
                    "common": ["kiba", "shino", "hinata"],
                    "uncommon": ["kurenai", "naruto", "sasuke"],
                    "rare": ["kakashi", "neji"],
                    "epic": ["tsunade"],
                    "legendary": ["itachi"],  # Nur bei Vollmond!
                    "mythic": []
                },
                "special_spawns": {
                    "full_moon_night": {
                        "characters": ["itachi"],
                        "spawn_rate": 0.15,
                        "cooldown_days": 30
                    }
                }
            },

            "ramen_stand": {
                "name": "Ichiraku Ramen - /encounter ramen_stand",
                "description": "Beliebter Ramen-Stand - Narutos Lieblings-Ort",
                "base_encounter_rate": 0.4,
                "characters": {
                    "common": ["naruto"],  # Fast immer da!
                    "uncommon": ["sakura", "hinata", "choji"],
                    "rare": ["kakashi", "sasuke"],
                    "epic": ["tsunade"],
                    "legendary": [],
                    "mythic": []
                },
                "time_spawns": {
                    "naruto_lunch": {
                        "character": "naruto",
                        "time_range": [11, 14],  # 11-14 Uhr
                        "spawn_chance": 0.85
                    }
                }
            },

            "tsunades_haus": {
                "name": "Tsunades Haus - /encounter tsunades_haus",
                "description": "Dein Zuhause - ruhig und sicher",
                "base_encounter_rate": 0.9,  # Hohe Chance da Tsunade fast immer da ist
                "characters": {
                    "common": ["tsunade"],  # NUR Tsunade!
                    "uncommon": [],  # Shizune ENTFERNT
                    "rare": [],
                    "epic": [],
                    "legendary": [],
                    "mythic": []
                },
                "time_conditions": {
                    "tsunade_home": {
                        "character": "tsunade",
                        "always_home": True,  # Außer bei der Arbeit
                        "work_hours": [9, 17],  # 9-17 Uhr arbeitet sie
                        "work_days": [0, 1, 2, 3, 4]  # Mo-Fr
                    }
                }
            },

            "onsen": {
                "name": "Heiße Quellen - /encounter onsen",
                "description": "Entspannende heiße Quellen am Dorfrand",
                "base_encounter_rate": 0.3,
                "characters": {
                    "common": ["sakura", "ino", "hinata"],
                    "uncommon": ["tsunade", "tenten"],
                    "rare": ["kurenai", "tsume"],
                    "epic": [],
                    "legendary": [],
                    "mythic": []
                },
                "gender_restrictions": ["female_only"]
            },

            "memorial_stone": {
                "name": "Heldengedenkstein - /encounter memorial_stone",
                "description": "Gedenkstein für gefallene Helden - sehr emotional",
                "base_encounter_rate": 0.2,
                "characters": {
                    "common": [],
                    "uncommon": ["sasuke", "kakashi"],
                    "rare": ["sakura", "naruto"],
                    "epic": ["tsunade"],
                    "legendary": [],
                    "mythic": []
                },
                "emotional_encounters": True
            },

            "academy": {
                "name": "Ninja-Akademie - /encounter academy",
                "description": "Ausbildungsort für junge Ninja",
                "base_encounter_rate": 0.4,
                "characters": {
                    "common": ["naruto", "sasuke", "sakura", "ino", "shikamaru", "choji"],
                    "uncommon": ["hinata", "kiba", "shino", "neji", "lee", "tenten"],
                    "rare": ["kakashi", "asuma", "kurenai", "guy"],
                    "epic": [],
                    "legendary": [],
                    "mythic": []
                }
            },

            "hospital": {
                "name": "Konoha-Hospital - /encounter hospital",
                "description": "Medizinisches Zentrum des Dorfes",
                "base_encounter_rate": 0.35,
                "characters": {
                    "common": ["sakura", "shizune"],
                    "uncommon": ["tsunade"],
                    "rare": [],
                    "epic": [],
                    "legendary": [],
                    "mythic": []
                }
            },

            "akatsuki_hideout": {
                "name": "Verlassenes Versteck - /encounter akatsuki_hideout",
                "description": "Ein düsteres, verlassenes Versteck außerhalb Konohas",
                "base_encounter_rate": 0.1,
                "characters": {
                    "common": [],
                    "uncommon": [],
                    "rare": [],
                    "epic": ["sasori", "deidara"],
                    "legendary": ["pain", "hidan", "kisame"],
                    "mythic": ["itachi", "orochimaru"]
                },
                "danger_level": "extreme",
                "access_requirements": {
                    "special_event": True
                },
                "sukunas_zimmer": {
                    "name": "Sukunas Zimmer in Tsunades Haus - /encounter sukunas_zimmer",
                    "description": "Sukunas eigenes Zimmer",
                    "base_encounter_rate": 0.35,
                    "characters": {
                        "common": [],
                        "uncommon": ["tsunade"],
                        "rare": [],
                        "epic": [],
                        "legendary": [],
                        "mythic": []
                    }
                }
            }
        }

    def _get_active_time_spawn_chance(self, location: str) -> float:
        """Gibt die höchste Time-Spawn-Chance für die aktuelle Location zurück"""
        from datetime import datetime

        current_hour = datetime.now().hour
        max_chance = 0.0

        for condition in self.time_conditions.values():
            if condition["location"] != location:
                continue

            time_range = condition["time_range"]

            if time_range[0] <= time_range[1]:
                # Korrektur für inklusives Ende ([11, 14] enthält 14:00 Uhr)
                in_range = time_range[0] <= current_hour <= time_range[1]
            else:
                in_range = current_hour >= time_range[0] or current_hour < time_range[1]

            if in_range:
                max_chance = max(max_chance, condition["spawn_chance"])

        return max_chance

    def _init_character_rarities(self) -> Dict:
        """Definiert Seltenheitsstufen für alle Charaktere"""
        return {
            # COMMON (60% Spawn-Chance)
            "common": {
                "spawn_rate": 0.6,
                "cooldown_minutes": 15,
                "characters": [
                    "naruto", "sakura", "ino", "choji", "shikamaru",
                    "kiba", "hinata", "shino", "shizune"
                ]
            },

            # UNCOMMON (30% Spawn-Chance)
            "uncommon": {
                "spawn_rate": 0.3,
                "cooldown_minutes": 30,
                "characters": [
                    "sasuke", "neji", "lee", "tenten", "kakashi",
                    "asuma", "kurenai", "guy"
                ]
            },

            # RARE (8% Spawn-Chance)
            "rare": {
                "spawn_rate": 0.08,
                "cooldown_minutes": 60,
                "characters": [
                    "tsunade", "inoichi", "choza", "shibi", "hiashi", "tsume"
                ]
            },

            # EPIC (1.5% Spawn-Chance)
            "epic": {
                "spawn_rate": 0.015,
                "cooldown_minutes": 120,
                "characters": [
                    "danzo", "sasori", "deidara", "kabuto"
                ]
            },

            # LEGENDARY (0.4% Spawn-Chance)
            "legendary": {
                "spawn_rate": 0.004,
                "cooldown_minutes": 300,  # 5 Stunden!
                "characters": [
                    "pain", "hidan", "kisame"
                ]
            },

            # MYTHIC (0.1% Spawn-Chance, spezielle Bedingungen)
            "mythic": {
                "spawn_rate": 0.001,
                "cooldown_days": 30,  # 30 Tage Cooldown!
                "characters": [
                    "itachi", "orochimaru"
                ],
                "special_conditions": True
            }
        }

    def _init_time_conditions(self) -> Dict:
        """Zeitbasierte Spawn-Bedingungen"""
        return {
            "naruto_ramen_lunch": {
                "character": "naruto",
                "location": "ramen_stand",
                "time_range": [11, 14],
                "spawn_chance": 0.85,
                "description": "Naruto ist fast immer zum Mittagessen da!"
            },

            "sasuke_night_training": {
                "character": "sasuke",
                "location": "training_area",
                "time_range": [22, 6],
                "spawn_chance": 0.7,
                "description": "Sasuke trainiert oft nachts allein"
            },

            "tsunade_office_hours": {
                "character": "tsunade",
                "location": "hokage_turm",
                "time_range": [9, 17],
                "spawn_chance": 0.6,
                "description": "Tsunade arbeitet tagsüber im Büro"
            },

            "lee_morning_training": {
                "character": "lee",
                "location": "training_area",
                "time_range": [5, 8],
                "spawn_chance": 0.9,
                "description": "Lee trainiert jeden Morgen früh!"
            },

            "itachi_midnight_forest": {
                "character": "itachi",
                "location": "wald",
                "time_range": [23, 1],
                "moon_phase": "full",
                "spawn_chance": 0.15,
                "cooldown_days": 30,
                "description": "Itachi erscheint nur bei Vollmond um Mitternacht"
            }
        }

    def _init_special_conditions(self) -> Dict:
        """Spezielle Bedingungen (Wetter, Events, etc.)"""
        return {
            "full_moon": {
                "affected_characters": ["itachi", "kiba", "tsume"],
                "spawn_modifier": 2.0,
                "description": "Vollmond verstärkt bestimmte Charaktere"
            },

            "rain": {
                "affected_characters": ["pain", "hidan"],
                "spawn_modifier": 1.5,
                "description": "Regen lockt düstere Charaktere an"
            },

            "festival": {
                "affected_characters": ["naruto", "sakura", "ino", "choji", "hinata"],
                "spawn_modifier": 1.8,
                "description": "Festivals bringen fröhliche Charaktere zusammen"
            }
        }

    def check_for_encounter(self, location: str) -> Optional[Dict]:
        """Hauptfunktion: Überprüft Begegnung mit erweiterten Bedingungen + Multi-Character Support"""
        # 💥 HIER EINFÜGEN:
        print(">>> DEBUG CHECK: Funktion check_for_encounter gestartet <<<")

        if location not in self.locations:
            return None

        location_data = self.locations[location]

        # 1. Prüfe Access Requirements
        if not self._check_access_requirements(location_data):
            return None

        # 2. Prüfe Location Cooldown
        if self._is_location_on_cooldown(location):
            return None

        # 3. Berechne finale Spawn-Rate
        final_rate = max(0.9, self._calculate_spawn_rate(location))

        roll = random.random()

        # 💥 HIER DAS GUI-DEBUGGING EINFÜGEN!
        if self.gui and hasattr(self.gui, 'add_message'):
            self.gui.add_message(
                "DEBUG",
                f"Rate: {final_rate:.2f} (Roll: {roll:.2f}). Time Spawn Chance: {self._get_active_time_spawn_chance(location):.2f}",
                getattr(self.gui, 'colors', {}).get("warning", "#f59e0b")
            )
        else:
            print(
                f"DEBUG: Rate: {final_rate:.2f} (Roll: {roll:.2f}). Time Spawn Chance: {self._get_active_time_spawn_chance(location):.2f}")

        if roll > final_rate:
            return None

        # 🎭 NEU: MULTI-CHARACTER ENCOUNTER CHECK
        # Prüfe ob Multi-Character System verfügbar und aktiv ist
        if hasattr(self, 'attempt_multi_encounter'):
            multi_encounter = self.attempt_multi_encounter(location)
            if multi_encounter:
                print(f"🎭 Multi-Character Encounter: {multi_encounter['characters']}")
                return multi_encounter

        # 4. FALLBACK: Normale Single-Character Begegnung
        character = self._select_character(location)

        if not character:
            return None

        # 6. Erstelle erweiterte Begegnung (Single-Character)
        encounter = self._create_advanced_encounter(character, location)

        # 7. Setze Cooldowns
        self._set_cooldowns(character, location)

        # 8. Speichere in Historie
        self._add_to_history(encounter)

        return encounter
    
    def _check_access_requirements(self, location_data: Dict) -> bool:
        """Prüft ob Spieler Zugang zur Location hat"""

        requirements = location_data.get("access_requirements", {})

        for req_type, req_value in requirements.items():
            if req_type == "tsunade_permission_level":
                current_level = self.game_state.get("tsunade", {}).get("bindung_sukuna", 0)
                if current_level < req_value:
                    return False

            elif req_type == "special_event":
                # Hier könnten spezielle Event-Flags geprüft werden
                if not self.game_state.get("special_events_unlocked", False):
                    return False

        return True

    def _calculate_spawn_rate(self, location: str) -> float:
        """
        Berechnet die finale Spawn-Rate (Chance auf Begegnung)
        unter Berücksichtigung von Zeit, Seltenheit, Location und Spezialbedingungen.
        Mit visuellen Debug-Meldungen im GUI-Chat.
        """

        location_data = self.locations.get(location)
        if not location_data:
            return 0.0

        base_rate = location_data.get("base_encounter_rate", 0.3)

        # --- Zeitabhängige Modifikatoren ---
        current_hour = datetime.now().hour
        time_modifiers = location_data.get("time_modifiers", {})
        if 6 <= current_hour < 12:
            time_mod = time_modifiers.get("morning", 1.0)
            time_label = "Morgen"
        elif 12 <= current_hour < 18:
            time_mod = time_modifiers.get("afternoon", 1.0)
            time_label = "Nachmittag"
        elif 18 <= current_hour < 22:
            time_mod = time_modifiers.get("evening", 1.0)
            time_label = "Abend"
        else:
            time_mod = time_modifiers.get("night", 1.0)
            time_label = "Nacht"

        # --- Zeitbasierte Spezial-Spawns (z. B. Naruto beim Mittag) ---
        time_spawn = self._get_active_time_spawn_chance(location)
        time_bonus = 1.0 + (time_spawn * 0.5)  # Bonus bis +50 %

        # --- Spezialbedingungen (Vollmond, Regen, Festival etc.) ---
        special_mod = 1.0
        active_conditions = []
        for cond_name, cond_data in self.special_conditions.items():
            modifier = cond_data.get("spawn_modifier", 1.0)
            if modifier != 1.0:
                special_mod *= modifier
                active_conditions.append(cond_name)

        # --- Zufällige Variation ---
        random_factor = random.uniform(0.9, 1.1)

        # --- Finale Berechnung ---
        spawn_rate = base_rate * time_mod * time_bonus * special_mod * random_factor

        # Mindest- und Maximalwerte
        spawn_rate = max(spawn_rate, 0.25)
        spawn_rate = min(spawn_rate, 0.95)

        # --- 🧠 DEBUG AUSGABE IM CHAT ---
        if hasattr(self, "gui") and hasattr(self.gui, "add_message"):
            debug_text = (
                f"📊 Spawn-Debug für '{location}':\n"
                f"• Basisrate: {base_rate:.2f}\n"
                f"• Tageszeit: {time_label} ×{time_mod:.2f}\n"
                f"• Zeitbonus: +{(time_bonus - 1) * 100:.0f}%\n"
                f"• Spezial-Mods: ×{special_mod:.2f} ({', '.join(active_conditions) if active_conditions else 'Keine'})\n"
                f"• Zufallsfaktor: ×{random_factor:.2f}\n"
                f"➡️ Endgültige Spawn-Wahrscheinlichkeit: {spawn_rate * 100:.1f}%"
            )
            try:
                self.gui.add_message("DEBUG", debug_text, self.gui.colors.get("warning", "#f59e0b"))
            except Exception:
                pass

        return spawn_rate

    def _get_time_info(self) -> Tuple[int, int]:
        """Ruft den aktuellen Wochentag (0=Montag, 6=Sonntag) und die Stunde ab."""
        try:
            # VERSUCH: Zeit via GUI's time_manager abrufen
            weekday = self.gui.time_manager.get_current_weekday()
            hour = self.gui.time_manager.get_current_hour()
        except Exception:
            # Breiter Fallback (Exception fängt alle Arten von Fehlern ab), falls der Zugriff fehlschlägt
            # Wir setzen auf Montag (0), 12:00 Uhr
            weekday = 0
            hour = 12
        return weekday, hour

    def _adjust_encounter_by_time(self, location: str, possible_characters: List[str]) -> List[str]:
        """Entfernt oder fügt Charaktere basierend auf dem Tsunade-Zeitplan hinzu/entfernt sie."""
        weekday, hour = self._get_time_info()

        # Arbeitszeit: Montag (0) bis Freitag (4), 9 bis 17 Uhr
        is_working_hours = (0 <= weekday <= 4) and (9 <= hour < 17)

        if location == "hokage_turm":
            if is_working_hours:
                # Höhere Chance, Tsunade im Büro anzutreffen
                if "tsunade" not in possible_characters:
                    possible_characters.append("tsunade")  # Sicherstellen, dass sie verfügbar ist
            else:
                # Geringere Chance außerhalb der Geschäftszeiten
                if "tsunade" in possible_characters:
                    # Man könnte sie hier entfernen oder einfach die Wahrscheinlichkeit manipulieren.
                    # Fürs Erste: Entfernen, da sie normalerweise nicht da ist.
                    possible_characters.remove("tsunade")

        elif location == "tsunades_haus" or location == "dorf_zentrum":  # Oder andere Orte
            if is_working_hours and "tsunade" in possible_characters:
                # Wenn sie arbeiten MUSS, ist sie an anderen Orten unwahrscheinlich
                possible_characters.remove("tsunade")
            elif not is_working_hours and "tsunade" not in possible_characters:
                # Nach Feierabend oder am Wochenende ist sie zu Hause oder im Dorfzentrum
                # Hier können Sie sie wieder zu den möglichen Charakteren hinzufügen.
                if location != "hokage_turm":
                    possible_characters.append("tsunade")

        return possible_characters

    def get_present_characters_for_display(self, location: str, hour: int) -> List[str]:
        """
        Gibt die Liste der Charaktere zurück, die theoretisch anwesend sein könnten,
        angepasst an die Zeitlogik (z.B. Tsunades Arbeitszeiten).

        KOMPLETT GEFIXT - Löst das "Niemand ist anwesend" Problem!
        """

        # ===== NEUER LOCATION MAPPER für GUI-Kompatibilität =====
        location_aliases = {
            # Tsunades Haus - Alle Räume
            "tsunades_haus_kueche": "tsunades_haus",
            "tsunades_haus_wohnzimmer": "tsunades_haus",
            "tsunades_haus_schlafzimmer": "tsunades_haus",

            # Standard-Locations (direkte Mappings)
            "dorf_zentrum": "dorf_zentrum",
            "training_area": "training_area",
            "ramen_stand": "ramen_stand",
            "hokage_turm": "hokage_turm",
            "wald": "wald",
            "onsen": "onsen",
            "memorial_stone": "memorial_stone",
            "hospital": "hospital",

            # Aliase für ähnliche Locations
            "akademie": "academy",
            "ninja_akademie": "academy",
            "buecherei": "dorf_zentrum",  # Fallback ins Dorfzentrum
            "bibliothek": "dorf_zentrum",
            "park": "dorf_zentrum",
            "ichiraku_ramen": "ramen_stand",
            "ramen_ichiraku": "ramen_stand"
        }

        # Verwende Alias falls verfügbar, sonst Original
        mapped_location = location_aliases.get(location, location)

        print(f"🔍 DEBUG: Location-Mapping: '{location}' -> '{mapped_location}'")

        # Prüfe ob die gemappte Location im System existiert
        if mapped_location not in self.locations:
            print(f"⚠️ WARNING: Location '{location}' (mapped: '{mapped_location}') nicht im Encounter-System gefunden")

            # ===== NOTFALL-FALLBACKS für bekannte Locations =====
            if location.startswith("tsunades_haus"):
                print(f"🏠 FALLBACK: Tsunades Haus erkannt - Tsunade hinzugefügt")
                return ["tsunade"]

            elif "ramen" in location.lower():
                print(f"🍜 FALLBACK: Ramen-Location erkannt - Naruto & Teuchi hinzugefügt")
                return ["naruto", "teuchi"]

            elif location in ["dorf_zentrum", "zentrum", "markt"]:
                print(f"🏘️ FALLBACK: Dorfzentrum erkannt - Standard-NPCs hinzugefügt")
                return ["naruto", "sakura", "kiba", "ino"]

            elif "training" in location.lower():
                print(f"⚔️ FALLBACK: Training-Area erkannt - Kampf-NPCs hinzugefügt")
                return ["sasuke", "lee", "neji", "kakashi"]

            elif "hokage" in location.lower():
                print(f"🏢 FALLBACK: Hokage-Turm erkannt - Offizielle hinzugefügt")
                return ["tsunade", "shizune"]

            else:
                print(f"❌ KEINE FALLBACK-REGEL für Location: {location}")
                return []

        # ===== NORMALE VERARBEITUNG für existierende Locations =====
        location_data = self.locations[mapped_location]

        # Sammle alle möglichen Charaktere aus verschiedenen Quellen
        possible_chars = []

        # QUELLE 1: Alte flache Liste "possible_characters" (Rückwärtskompatibilität)
        if "possible_characters" in location_data:
            possible_chars.extend(location_data["possible_characters"])
            print(f"📋 Charaktere aus possible_characters: {location_data['possible_characters']}")

        # QUELLE 2: Neue Struktur "characters" mit Seltenheitsgruppen
        character_groups = location_data.get("characters", {})
        if character_groups:
            all_rarity_chars = []
            for rarity, char_list in character_groups.items():
                if isinstance(char_list, list):
                    all_rarity_chars.extend(char_list)
            possible_chars.extend(all_rarity_chars)
            print(f"🎭 Charaktere aus Seltenheitsgruppen: {all_rarity_chars}")

        # Entferne Duplikate und leere Einträge
        possible_chars = list(set([char for char in possible_chars if char]))

        # Prüfe ob überhaupt Charaktere definiert sind
        if not possible_chars:
            print(f"⚠️ WARNING: Keine Charaktere für Location '{mapped_location}' definiert")

            # ===== ZUSÄTZLICHE FALLBACKS basierend auf Location-Typ =====
            if mapped_location == "tsunades_haus":
                possible_chars = ["tsunade", "shizune"]
            elif mapped_location == "ramen_stand":
                possible_chars = ["naruto", "teuchi", "choji"]
            elif mapped_location == "dorf_zentrum":
                possible_chars = ["naruto", "sakura", "kiba", "ino", "shikamaru", "choji", "hinata"]
            elif mapped_location == "training_area":
                possible_chars = ["sasuke", "lee", "neji", "tenten", "kakashi", "guy"]
            elif mapped_location == "hokage_turm":
                possible_chars = ["tsunade", "shizune", "kakashi"]
            elif mapped_location == "wald":
                possible_chars = ["kiba", "shino", "hinata", "kurenai"]
            elif mapped_location == "academy":
                possible_chars = ["naruto", "sasuke", "sakura", "ino", "shikamaru", "choji"]
            else:
                print(f"❌ Keine Fallback-Charaktere für '{mapped_location}' verfügbar")
                return []

            print(f"🔄 FALLBACK-Charaktere verwendet: {possible_chars}")

        # ===== ZEITLOGIK ANWENDEN =====
        try:
            adjusted_chars = self._adjust_encounter_by_time(mapped_location, possible_chars.copy())
            print(f"⏰ Nach Zeitlogik: {adjusted_chars}")
        except Exception as e:
            print(f"⚠️ Zeitlogik fehlgeschlagen: {e} - verwende Original-Liste")
            adjusted_chars = possible_chars.copy()

        # ===== ANWESENHEITS-WAHRSCHEINLICHKEIT =====
        present_for_display = []

        for char in adjusted_chars:
            # Unterschiedliche Wahrscheinlichkeiten je nach Charakter und Location
            spawn_chance = 0.7  # Standard

            # Höhere Chance für wichtige Charaktere an ihren Haupt-Locations
            if char == "tsunade" and location.startswith("tsunades_haus"):
                spawn_chance = 0.95  # Fast immer zu Hause
            elif char == "naruto" and "ramen" in mapped_location:
                spawn_chance = 0.9  # Fast immer am Ramen-Stand
            elif char == "sasuke" and mapped_location == "training_area":
                spawn_chance = 0.8  # Oft beim Training
            elif char in ["kakashi", "guy", "asuma", "kurenai"]:
                spawn_chance = 0.6  # Sensei sind seltener

            # Würfle ob Charakter anwesend ist
            if random.random() < spawn_chance:
                present_for_display.append(char)

        # ===== SPEZIELLE REGELN =====

        # REGEL 1: Tsunade ist IMMER zu Hause (außer bei der Arbeit)
        if location.startswith("tsunades_haus") and "tsunade" not in present_for_display:
            try:
                weekday, current_hour = self._get_time_info()
                is_working_hours = (0 <= weekday <= 4) and (9 <= current_hour < 17)

                if not is_working_hours:  # Nach Feierabend oder Wochenende
                    present_for_display.append("tsunade")
                    print(f"🏠 SPEZIAL: Tsunade zu Hause hinzugefügt (Feierabend/Wochenende)")
            except:
                # Fallback: Tsunade ist standardmäßig zu Hause
                if "tsunade" not in present_for_display:
                    present_for_display.append("tsunade")
                    print(f"🏠 SPEZIAL: Tsunade zu Hause hinzugefügt (Fallback)")

        # REGEL 2: Mindestens ein Charakter in wichtigen Locations
        if not present_for_display and mapped_location in ["tsunades_haus", "dorf_zentrum", "ramen_stand"]:
            if mapped_location == "tsunades_haus":
                present_for_display = ["tsunade"]
            elif mapped_location == "ramen_stand":
                present_for_display = ["naruto"]
            elif mapped_location == "dorf_zentrum":
                present_for_display = [random.choice(["naruto", "sakura", "kiba"])]
            print(f"🎯 MINDEST-REGEL: {present_for_display} zu {mapped_location} hinzugefügt")

        # ===== FINAL RESULT =====
        print(f"✅ FINAL: Location '{location}' -> Anwesende Charaktere: {present_for_display}")

        return present_for_display

    def _get_time_modifier(self, location: str, hour: int) -> float:
        """Gibt Zeit-basierten Modifikator zurück"""

        location_data = self.locations[location]
        time_mods = location_data.get("time_modifiers", {})

        if 6 <= hour < 12:
            return time_mods.get("morning", 1.0)
        elif 12 <= hour < 18:
            return time_mods.get("afternoon", 1.0)
        elif 18 <= hour < 22:
            return time_mods.get("evening", 1.0)
        else:
            return time_mods.get("night", 1.0)

    def _get_weather_modifier(self) -> float:
        """Simuliert Wetter-Modifikator"""
        # Hier könnte echte Wetter-API integriert werden
        weather_types = ["sunny", "cloudy", "rainy", "stormy"]
        current_weather = random.choice(weather_types)

        modifiers = {
            "sunny": 1.1,
            "cloudy": 1.0,
            "rainy": 0.8,
            "stormy": 0.6
        }

        return modifiers.get(current_weather, 1.0)

    def _get_moon_modifier(self, location: str) -> float:
        """Berechnet Mondphasen-Modifikator"""

        # Simuliere Mondphase (in echtem Spiel: echte Berechnung)
        moon_phases = ["new", "waxing", "full", "waning"]
        current_phase = random.choice(moon_phases)

        if current_phase == "full":
            if location == "wald":
                return 1.5  # Wald bei Vollmond ist besonders aktiv
            return 1.2
        elif current_phase == "new":
            return 0.9

        return 1.0

    def _get_event_modifier(self) -> float:
        """Berechnet Event-basierten Modifikator"""

        # Hier könnten spezielle Events geprüft werden
        # Festivals, Feiertage, Story-Events, etc.

        return 1.0  # Standardwert

    def _select_character(self, location: str) -> Optional[str]:
        """Wählt Charakter basierend auf Seltenheit und Bedingungen"""

        location_data = self.locations[location]

        # 1. Prüfe zeitbasierte Spawns zuerst (Cooldowm wird hier intern geprüft)
        time_character = self._check_time_spawns(location)
        if time_character:
            return time_character

        # 2. Erstelle gewichtete Liste aller verfügbaren Charaktere
        weighted_characters = []

        for rarity, char_list in location_data["characters"].items():
            if not char_list:
                continue

            rarity_data = self.character_rarities[rarity]
            spawn_rate = rarity_data["spawn_rate"]

            for character in char_list:
                # Prüfe ob Charakter verfügbar ist (inkl. Story/Gender)
                if self._is_character_available(character, location):

                    # 💥 KRITISCHE KORREKTUR: PRÜFE COOLDOWN VOR DEM HINZUFÜGEN ZUM POOL!
                    if not self._is_character_on_cooldown(character):
                        weighted_characters.append((character, spawn_rate))

        if not weighted_characters:
            return None  # Jetzt nur, wenn KEIN Charakter verfügbar ist!

        # 3. Wähle gewichteten zufälligen Charakter
        return self._weighted_random_choice(weighted_characters)

    def _check_time_spawns(self, location: str) -> Optional[str]:
        """Prüft zeitbasierte Spawns"""

        current_hour = datetime.now().hour

        for condition_name, condition in self.time_conditions.items():
            if condition["location"] != location:
                continue

            time_range = condition["time_range"]

            # Prüfe Zeitbereich (kann über Mitternacht gehen)
            if time_range[0] <= time_range[1]:
                # Normaler Bereich (z.B. 9-17)
                in_range = time_range[0] <= current_hour <= time_range[1]
            else:
                # Über Mitternacht (z.B. 22-6)
                in_range = current_hour >= time_range[0] or current_hour < time_range[1]

            if in_range:
                # Prüfe zusätzliche Bedingungen (Mondphase, etc.)
                if self._check_special_spawn_conditions(condition):
                    if random.random() < condition["spawn_chance"]:
                        character = condition["character"]

                        # Prüfe Cooldown für zeitbasierte Spawns
                        #if not self._is_character_on_cooldown(character):
                        return character

        return None

    def _check_special_spawn_conditions(self, condition: Dict) -> bool:
        """Prüft spezielle Spawn-Bedingungen wie Mondphase"""

        if "moon_phase" in condition:
            required_phase = condition["moon_phase"]
            # Hier würde echte Mondphasen-Berechnung stehen
            current_phase = self._get_current_moon_phase()
            if current_phase != required_phase:
                return False

        return True

    def _get_current_moon_phase(self) -> str:
        """Simuliert aktuelle Mondphase"""
        # In echtem Spiel: echte Mondphasen-Berechnung
        phases = ["new", "waxing", "full", "waning"]
        return random.choice(phases)

    def _is_character_available(self, character: str, location: str) -> bool:
        """Prüft ob Charakter für Spawn verfügbar ist"""

        # Prüfe ob Charakter existiert
        if character not in self.all_characters:
            return False

        # Prüfe Gender-Restrictions
        location_data = self.locations[location]
        if "gender_restrictions" in location_data:
            restrictions = location_data["gender_restrictions"]
            if "female_only" in restrictions:
                # Hier würde Gender des Charakters geprüft
                male_characters = [
                    "naruto", "sasuke", "kakashi", "lee", "neji", "shikamaru",
                    "choji", "kiba", "shino", "asuma", "guy", "inoichi",
                    "choza", "hiashi", "danzo", "itachi", "kisame", "pain",
                    "hidan", "deidara", "sasori", "orochimaru", "kabuto"
                ]
                if character in male_characters:
                    return False

        # Prüfe Story-spezifische Verfügbarkeit
        if not self._is_character_story_available(character):
            return False

        return True

    def _is_character_story_available(self, character: str) -> bool:
        """Prüft Story-basierte Verfügbarkeit"""

        # Akatsuki-Mitglieder sind nur in speziellen Locations verfügbar
        akatsuki_members = ["itachi", "kisame", "pain", "hidan", "deidara", "sasori"]

        if character in akatsuki_members:
            # Nur in speziellen Events oder Locations
            return self.game_state.get("akatsuki_encounters_unlocked", False)

        # Danzo ist nur verfügbar wenn bestimmte Story-Punkte erreicht sind
        if character == "danzo":
            return self.game_state.get("danzo_accessible", False)

        return True

    def _weighted_random_choice(self, weighted_list: List[Tuple[str, float]]) -> Optional[str]:
        """Gewichtete zufällige Auswahl"""

        if not weighted_list:
            return None

        total_weight = sum(weight for _, weight in weighted_list)

        if total_weight <= 0:
            return None

        r = random.uniform(0, total_weight)
        current_weight = 0

        for item, weight in weighted_list:
            current_weight += weight
            if current_weight >= r:
                return item

        # Fallback
        return weighted_list[0][0]

    def _is_location_on_cooldown(self, location: str) -> bool:
        """Prüft Location-Cooldown"""

        if location not in self.cooldowns:
            return False

        last_encounter = self.cooldowns[location].get("last_encounter", None)
        if not last_encounter:
            return False

        cooldown_minutes = 15  # Standard Location-Cooldown

        time_diff = datetime.now() - last_encounter
        return time_diff.total_seconds() < (cooldown_minutes * 60)

    def _is_character_on_cooldown(self, character: str) -> bool:
        """Prüft Character-spezifischen Cooldown"""

        if character not in self.cooldowns:
            return False

        char_cooldown = self.cooldowns[character]
        last_encounter = char_cooldown.get("last_encounter", None)

        if not last_encounter:
            return False

        # Bestimme Cooldown basierend auf Seltenheit
        rarity = self._get_character_rarity(character)
        rarity_data = self.character_rarities[rarity]

        if "cooldown_days" in rarity_data:
            # Mythic characters haben Tage-Cooldown
            cooldown_seconds = rarity_data["cooldown_days"] * 24 * 60 * 60
        else:
            # Andere haben Minuten-Cooldown
            cooldown_seconds = rarity_data["cooldown_minutes"] * 60

        time_diff = datetime.now() - last_encounter
        return time_diff.total_seconds() < cooldown_seconds

    def _get_character_rarity(self, character: str) -> str:
        """Bestimmt Seltenheit eines Charakters"""

        for rarity, data in self.character_rarities.items():
            if character in data["characters"]:
                return rarity

        return "common"  # Fallback

    def _create_advanced_encounter(self, character: str, location: str) -> Dict:
        """Erstellt erweiterte Begegnung mit detaillierten Informationen"""

        char_data = self.all_characters.get(character, {})
        location_data = self.locations[location]
        rarity = self._get_character_rarity(character)

        # Bestimme Encounter-Typ basierend auf Charakter und Location
        encounter_type = self._determine_encounter_type(character, location)

        # Generiere kontextuelle Beschreibung
        description = self._generate_encounter_description(
            character, location, encounter_type, rarity
        )

        # Erstelle Aktionsoptionen
        options = self._generate_encounter_options(character, encounter_type)

        # Berechne Belohnungen
        rewards = self._calculate_encounter_rewards(character, rarity)

        encounter = {
            "character": character,
            "character_data": char_data,
            "location": location,
            "location_name": location_data["name"],
            "type": encounter_type,
            "rarity": rarity,
            "description": description,
            "options": options,
            "rewards": rewards,
            "timestamp": datetime.now().isoformat(),
            "mood": self._determine_character_mood(character),
            "special_conditions": self._get_active_conditions(location)
        }

        return encounter

    def _determine_encounter_type(self, character: str, location: str) -> str:
        """Bestimmt Art der Begegnung"""

        # Charakterspezifische Encounter-Präferenzen
        char_prefs = {
            "naruto": ["training", "freundlich", "essen"],
            "sasuke": ["training", "ernst", "allein"],
            "sakura": ["freundlich", "hilfsbereit", "medizinisch"],
            "tsunade": ["autoritär", "fürsorglich", "medizinisch"],
            "itachi": ["mysteriös", "warnend", "geheimnisvoll"],
            "lee": ["training", "enthusiastisch", "motivierend"],
            "kakashi": ["entspannt", "lehrreich", "geheimnisvoll"]
        }

        # Locations-spezifische Modifikationen
        location_mods = {
            "training_area": ["training", "wettkampf"],
            "hospital": ["medizinisch", "hilfsbereit"],
            "wald": ["mysteriös", "ruhig"],
            "ramen_stand": ["essen", "freundlich"]
        }

        possible_types = char_prefs.get(character, ["freundlich"])
        location_types = location_mods.get(location, [])

        # Kombiniere und wähle
        all_types = possible_types + location_types
        return random.choice(all_types)

    def _generate_encounter_description(self, character: str, location: str,
                                        encounter_type: str, rarity: str) -> str:
        """Generiert detaillierte Encounter-Beschreibung"""

        location_name = self.locations[location]["name"]
        char_data = self.all_characters.get(character, {})

        # Basis-Beschreibung je nach Charakter
        char_descriptions = {
            "naruto": {
                "training": f"Du siehst Naruto beim intensiven Training auf dem {location_name}. Er bemerkt dich und winkt energisch!",
                "freundlich": f"Naruto kommt fröhlich auf dich zu, ein breites Grinsen im Gesicht.",
                "essen": f"Naruto sitzt am Ramen-Stand und schlürft genüsslich seine Nudeln."
            },
            "sasuke": {
                "training": f"Sasuke trainiert allein und konzentriert auf dem {location_name}. Seine Bewegungen sind präzise und kraftvoll.",
                "ernst": f"Sasuke steht mit verschränkten Armen da und beobachtet dich mit seinen dunklen Augen.",
                "allein": f"Sasuke scheint tief in Gedanken versunken zu sein."
            },
            "tsunade": {
                "autoritär": f"Tsunade steht mit vor der Brust verschränkten Armen da und mustert dich kritisch.",
                "fürsorglich": f"Tsunade bemerkt dich und ihr Blick wird sofort weicher und besorgter.",
                "medizinisch": f"Tsunade untersucht gerade medizinische Akten und blickt auf, als sie dich sieht."
            },
            "itachi": {
                "mysteriös": f"Eine dunkle Gestalt taucht aus den Schatten auf - es ist Itachi. Seine roten Augen fixieren dich.",
                "warnend": f"Itachi erscheint plötzlich und spricht mit ruhiger, aber eindringlicher Stimme.",
                "geheimnisvoll": f"Du spürst eine Präsenz und drehst dich um - Itachi steht dort, unbeweglich wie eine Statue."
            }
        }

        # Fallback für Charaktere ohne spezifische Beschreibung
        if character not in char_descriptions:
            return f"Du begegnest {character.title()} auf dem {location_name}."

        char_desc = char_descriptions[character]
        description = char_desc.get(encounter_type, f"Du triffst {character.title()} auf dem {location_name}.")

        # Füge Seltenheits-Hinweis hinzu
        rarity_msgs = {
            "rare": " (Seltene Begegnung!)",
            "epic": " ⭐ EPISCHE BEGEGNUNG! ⭐",
            "legendary": " 🌟 LEGENDÄRE BEGEGNUNG! 🌟",
            "mythic": " ✨ MYSTISCHE BEGEGNUNG! ✨"
        }

        if rarity in rarity_msgs:
            description += rarity_msgs[rarity]

        return description

    def _generate_encounter_options(self, character: str, encounter_type: str) -> List[str]:
        """Generiert verfügbare Aktionsoptionen"""

        base_options = ["sprechen", "grüßen", "weitergehen"]

        # Charakterspezifische Optionen
        char_options = {
            "naruto": ["training_anfragen", "ramen_einladen", "jutsu_zeigen"],
            "sasuke": ["training_herausfordern", "respektvoll_grüßen", "abstand_halten"],
            "tsunade": ["um_rat_fragen", "sorgen_teilen", "umarmung"],
            "sakura": ["hilfe_anbieten", "medizin_fragen", "freundlich_sprechen"],
            "itachi": ["vorsichtig_sein", "fragen_stellen", "dankbar_sein"],
            "lee": ["training_mitmachen", "motivation_holen", "technik_lernen"],
            "kakashi": ["lektionen_bitten", "buch_fragen", "entspannt_reden"]
        }

        # Encounter-Type spezifische Optionen
        type_options = {
            "training": ["training_beobachten", "mitmachen", "tipps_bitten"],
            "freundlich": ["unterhalten", "kompliment_machen", "zeit_verbringen"],
            "mysteriös": ["neugierig_fragen", "vorsichtig_bleiben", "respekt_zeigen"],
            "medizinisch": ["verletzung_zeigen", "hilfe_bitten", "lernen"]
        }

        # Kombiniere Optionen
        options = base_options.copy()

        if character in char_options:
            options.extend(char_options[character])

        if encounter_type in type_options:
            options.extend(type_options[encounter_type])

        # Entferne Duplikate und begrenze auf 6 Optionen
        unique_options = list(dict.fromkeys(options))
        return unique_options[:6]

    def _calculate_encounter_rewards(self, character: str, rarity: str) -> Dict:
        """Berechnet Belohnungen für Begegnung"""

        base_rewards = {
            "experience": 10,
            "relationship_points": 2,
            "special_items": []
        }

        # Seltenheits-Multiplikatoren
        rarity_multipliers = {
            "common": 1.0,
            "uncommon": 1.5,
            "rare": 2.0,
            "epic": 3.0,
            "legendary": 5.0,
            "mythic": 10.0
        }

        multiplier = rarity_multipliers.get(rarity, 1.0)

        rewards = {
            "experience": int(base_rewards["experience"] * multiplier),
            "relationship_points": int(base_rewards["relationship_points"] * multiplier),
            "special_items": base_rewards["special_items"].copy()
        }

        # Charakterspezifische Belohnungen
        char_rewards = {
            "itachi": {"special_items": ["sharingan_erkenntnisse", "clan_wissen"]},
            "tsunade": {"special_items": ["medizin_wissen", "jutsu_scrolls"]},
            "kakashi": {"special_items": ["strategie_tipps", "jutsu_bücher"]},
            "orochimaru": {"special_items": ["verbotenes_wissen", "experimenteller_jutsu"]}
        }

        if character in char_rewards:
            rewards.update(char_rewards[character])

        return rewards

    def _determine_character_mood(self, character: str) -> str:
        """Bestimmt aktuelle Stimmung des Charakters"""

        char_data = self.all_characters.get(character, {})
        bindung = char_data.get("bindung_sukuna", 0)

        # Basis-Stimmung basierend auf Bindung
        if bindung > 75:
            base_mood = "sehr_freundlich"
        elif bindung > 25:
            base_mood = "freundlich"
        elif bindung > -25:
            base_mood = "neutral"
        elif bindung > -75:
            base_mood = "misstrauisch"
        else:
            base_mood = "feindselig"

        # Charakterspezifische Stimmungs-Modifikationen
        char_moods = {
            "naruto": ["energisch", "optimistisch", "freundlich"],
            "sasuke": ["ernst", "distanziert", "konzentriert"],
            "sakura": ["hilfsbereit", "freundlich", "entschlossen"],
            "tsunade": ["authorität", "fürsorglich", "beschützend"],
            "itachi": ["ruhig", "mysteriös", "nachdenklich"],
            "lee": ["enthusiastisch", "motiviert", "energisch"]
        }

        if character in char_moods:
            return random.choice(char_moods[character])

        return base_mood

    def _get_active_conditions(self, location: str) -> List[str]:
        """Bestimmt aktive besondere Bedingungen"""

        conditions = []

        # Mondphase
        moon_phase = self._get_current_moon_phase()
        if moon_phase == "full":
            conditions.append("vollmond")

        # Zeit
        hour = datetime.now().hour
        if 22 <= hour or hour < 6:
            conditions.append("nacht")
        elif 6 <= hour < 12:
            conditions.append("morgen")
        elif 12 <= hour < 18:
            conditions.append("nachmittag")
        else:
            conditions.append("abend")

        # Location-spezifische Bedingungen
        location_conditions = {
            "wald": ["mystisch", "ruhig"],
            "training_area": ["aktiv", "energisch"],
            "hospital": ["ruhig", "heilend"],
            "akatsuki_hideout": ["gefährlich", "düster"]
        }

        if location in location_conditions:
            conditions.extend(location_conditions[location])

        return conditions

    def _set_cooldowns(self, character: str, location: str):
        """Setzt Cooldowns für Charakter und Location"""

        current_time = datetime.now()

        # Character Cooldown
        if character not in self.cooldowns:
            self.cooldowns[character] = {}
        self.cooldowns[character]["last_encounter"] = current_time

        # Location Cooldown
        if location not in self.cooldowns:
            self.cooldowns[location] = {}
        self.cooldowns[location]["last_encounter"] = current_time

    def _add_to_history(self, encounter: Dict):
        """Fügt Begegnung zur Historie hinzu"""

        self.encounter_history.append({
            "character": encounter["character"],
            "location": encounter["location"],
            "type": encounter["type"],
            "rarity": encounter["rarity"],
            "timestamp": encounter["timestamp"]
        })

        # Begrenze Historie auf letzten 100 Einträge
        if len(self.encounter_history) > 100:
            self.encounter_history = self.encounter_history[-100:]

    def get_encounter_statistics(self) -> Dict:
        """Gibt Encounter-Statistiken zurück"""

        if not self.encounter_history:
            return {"message": "Noch keine Begegnungen"}

        total_encounters = len(self.encounter_history)

        # Charaktere zählen
        char_counts = {}
        for encounter in self.encounter_history:
            char = encounter["character"]
            char_counts[char] = char_counts.get(char, 0) + 1

        # Seltenheiten zählen
        rarity_counts = {}
        for encounter in self.encounter_history:
            rarity = encounter["rarity"]
            rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1

        # Locations zählen
        location_counts = {}
        for encounter in self.encounter_history:
            location = encounter["location"]
            location_counts[location] = location_counts.get(location, 0) + 1

        return {
            "total_encounters": total_encounters,
            "character_counts": char_counts,
            "rarity_counts": rarity_counts,
            "location_counts": location_counts,
            "last_encounter": self.encounter_history[-1] if self.encounter_history else None
        }

    def get_character_encounter_info(self, character: str) -> Dict:
        """Gibt detaillierte Info über Charakter-Begegnungen"""

        if character not in self.all_characters:
            return {"error": "Charakter nicht gefunden"}

        rarity = self._get_character_rarity(character)
        rarity_data = self.character_rarities[rarity]

        # Prüfe Cooldown-Status
        is_on_cooldown = self._is_character_on_cooldown(character)
        cooldown_info = None

        if is_on_cooldown and character in self.cooldowns:
            last_encounter = self.cooldowns[character]["last_encounter"]
            if "cooldown_days" in rarity_data:
                cooldown_seconds = rarity_data["cooldown_days"] * 24 * 60 * 60
            else:
                cooldown_seconds = rarity_data["cooldown_minutes"] * 60

            time_left = cooldown_seconds - (datetime.now() - last_encounter).total_seconds()
            cooldown_info = {
                "time_left_seconds": max(0, time_left),
                "time_left_formatted": self._format_time_remaining(time_left)
            }

        # Finde verfügbare Locations
        available_locations = []
        for loc_name, loc_data in self.locations.items():
            for rarity_tier, chars in loc_data["characters"].items():
                if character in chars:
                    available_locations.append({
                        "location": loc_name,
                        "name": loc_data["name"],
                        "rarity_tier": rarity_tier,
                        "base_rate": loc_data["base_encounter_rate"]
                    })

        return {
            "character": character,
            "rarity": rarity,
            "spawn_rate": rarity_data["spawn_rate"],
            "is_on_cooldown": is_on_cooldown,
            "cooldown_info": cooldown_info,
            "available_locations": available_locations,
            "special_conditions": self._get_character_special_conditions(character)
        }

    def _format_time_remaining(self, seconds: float) -> str:
        """Formatiert verbleibende Zeit lesbar"""

        if seconds <= 0:
            return "Verfügbar"

        if seconds >= 86400:  # 1 Tag
            days = int(seconds // 86400)
            return f"{days} Tag{'e' if days > 1 else ''}"
        elif seconds >= 3600:  # 1 Stunde
            hours = int(seconds // 3600)
            return f"{hours} Stunde{'n' if hours > 1 else ''}"
        else:
            minutes = int(seconds // 60)
            return f"{minutes} Minute{'n' if minutes > 1 else ''}"

    def _get_character_special_conditions(self, character: str) -> List[str]:
        """Gibt spezielle Spawn-Bedingungen für Charakter zurück"""

        conditions = []

        # Prüfe Zeit-Bedingungen
        for condition_name, condition in self.time_conditions.items():
            if condition["character"] == character:
                time_range = condition["time_range"]
                conditions.append(f"Erscheint zwischen {time_range[0]}:00 - {time_range[1]}:00 Uhr")

                if "moon_phase" in condition:
                    conditions.append(f"Nur bei {condition['moon_phase']}-Mond")

                if "cooldown_days" in condition:
                    conditions.append(f"Cooldown: {condition['cooldown_days']} Tage")

        # Prüfe Story-Bedingungen
        if character in ["itachi", "kisame", "pain", "hidan", "deidara", "sasori"]:
            conditions.append("Akatsuki-Begegnungen müssen freigeschaltet sein")

        if character == "danzo":
            conditions.append("Spezielle Story-Progression erforderlich")

        return conditions

# =================================================================
# HILFSFUNKTIONEN FÜR INTEGRATION
# =================================================================

def create_advanced_encounter_system(game_state, gui):
    """Factory-Funktion für das Advanced Encounter System"""
    return SimpleEncounterSystem(game_state, gui)

def get_all_available_locations():
    """Gibt alle verfügbaren Locations zurück"""
    system = SimpleEncounterSystem({}, None)
    return list(system.locations.keys())

def get_all_spawnable_characters():
    """Gibt alle spawnbaren Charaktere mit ihren Seltenheiten zurück"""
    system = SimpleEncounterSystem({}, None)

    all_spawnable = {}
    for rarity, data in system.character_rarities.items():
        for character in data["characters"]:
            all_spawnable[character] = rarity

    return all_spawnable

# =================================================================
# TEST FUNKTIONEN
# =================================================================

def test_advanced_encounter_system():
    """Test-Funktion für das Advanced Encounter System"""
    print("🧪 === ADVANCED ENCOUNTER SYSTEM TEST ===")

    # Mock Game State
    game_state = {
        "tsunade": {"bindung_sukuna": 100},
        "naruto": {"bindung_sukuna": 50},
        "sasuke": {"bindung_sukuna": 20},
        "itachi": {"bindung_sukuna": 45},
        "akatsuki_encounters_unlocked": True,
        "danzo_accessible": True
    }

    system = SimpleEncounterSystem(game_state, None)

    print(f"📍 Verfügbare Locations: {len(system.locations)}")
    print(f"👥 Verfügbare Charaktere: {len(system.all_characters)}")

    # Teste verschiedene Locations
    test_locations = ["dorf_zentrum", "wald", "ramen_stand", "training_area", "hokage_turm"]

    for location in test_locations:
        print(f"\n🗺️ Testing Location: {location}")
        for i in range(5):
            encounter = system.check_for_encounter(location)
            if encounter:
                char = encounter["character"]
                rarity = encounter["rarity"]
                enc_type = encounter["type"]
                print(f"  ✅ Begegnung {i + 1}: {char} ({rarity}) - {enc_type}")
            else:
                print(f"  ❌ Begegnung {i + 1}: Keine Begegnung")

    # Teste Statistiken
    print(f"\n📊 Encounter Statistics:")
    stats = system.get_encounter_statistics()
    if "total_encounters" in stats:
        print(f"  Total: {stats['total_encounters']}")
        print(f"  Rarities: {stats['rarity_counts']}")

    # Teste Character Info
    print(f"\n🎭 Character Info (Itachi):")
    char_info = system.get_character_encounter_info("itachi")
    if "error" not in char_info:
        print(f"  Rarity: {char_info['rarity']}")
        print(f"  Spawn Rate: {char_info['spawn_rate']}")
        print(f"  Available Locations: {len(char_info['available_locations'])}")
        print(f"  Special Conditions: {char_info['special_conditions']}")

    print("\n✅ === TEST COMPLETE ===")

if __name__ == "__main__":
    test_advanced_encounter_system()