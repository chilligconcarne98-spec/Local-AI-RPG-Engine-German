# -*- coding: utf-8 -*-
"""
MULTI-CHARACTER ENCOUNTER SYSTEM - SUKUNA ALS SPIELER KORRIGIERT
Ermöglicht Begegnungen mit mehreren NPCs gleichzeitig
WICHTIG: Sukuna ist der SPIELER und spawnt NICHT als NPC
"""

import random
from typing import Dict, List, Optional, Tuple


class MultiCharacterEncounterSystem:
    """
    🎭 MULTI-CHARACTER ENCOUNTERS: NPCs spawnen für den Sukuna-Spieler
    """

    def __init__(self):
        self.character_groups = self._build_character_groups()
        self.location_spawn_rules = self._build_location_rules()
        self.active_characters = []  # Liste der NPCs (OHNE Sukuna)
        self.conversation_mode = "single"  # "single" oder "multi"
        self.player_character = "sukuna"  # Der Spieler ist immer Sukuna

    def _build_character_groups(self) -> Dict:
        """
        Definiert logische NPC-Gruppen (OHNE Sukuna - er ist der Spieler)
        """
        return {
            # TEAMS (ohne Sukuna)
            "team_7": ["naruto", "sasuke", "sakura"],
            "team_8": ["hinata", "kiba", "shino"],
            "team_10": ["shikamaru", "ino", "choji"],
            "team_guy": ["neji", "lee", "tenten"],

            # SENSEI GRUPPEN
            "kakashi_students": ["kakashi", "naruto", "sasuke", "sakura"],
            "guy_students": ["might_guy", "lee", "neji", "tenten"],
            "nara_family": ["shikamaru", "shikaku"],
            "yamanaka_family": ["ino", "inoichi"],
            "akimichi_family": ["choji", "choza"],
            "inuzuka_family": ["kiba", "tsume"],
            "hyuga_family": ["hinata", "neji", "hiashi"],

            # FREUNDSCHAFTEN
            "naruto_friends": ["naruto", "choji", "kiba"],
            "lazy_duo": ["shikamaru", "choji"],
            "girl_friends": ["ino", "sakura", "hinata", "tenten"],
            "shy_pair": ["hinata", "shino"],
            "rivals": ["naruto", "sasuke", "neji", "lee"],
            "training_partners": ["lee", "neji", "might_guy"],

            # ARBEITSGRUPPEN
            "hokage_office": ["tsunade", "shizune"],
            "medical_team": ["tsunade", "sakura", "shizune"],
            "jonin_senseis": ["kakashi", "might_guy"],
            "clan_heads": ["shikaku", "inoichi", "choza", "hiashi", "tsume"],

            # VILLAIN GRUPPEN
            "akatsuki_duo": ["itachi", "kisame"],
            "akatsuki_artists": ["sasori", "deidara"],
            "akatsuki_leaders": ["pain", "itachi"],
            "orochimaru_faction": ["orochimaru", "kabuto"],
            "dangerous_singles": ["danzo", "hidan"],

            # SPEZIELLE KOMBINATIONEN (Gruppen die für Sukuna interessant sind)
            "tsunade_care_team": ["tsunade", "shizune"],  # Für Sukunas Fürsorge
            "wolf_clan_members": ["kiba", "tsume"],  # Reagieren auf Sukunas Wolfsnatur
            "uchiha_brothers": ["sasuke", "itachi"],  # Dramatische Encounters
            "trauma_understanders": ["sasuke", "kakashi"],  # Verstehen Sukunas Trauma

            # ZUFÄLLIGE KOMBINATIONEN
            "random_pairs": [
                ["naruto", "kiba"], ["sasuke", "neji"], ["sakura", "ino"],
                ["shikamaru", "shino"], ["choji", "lee"], ["hinata", "tenten"],
                ["kakashi", "might_guy"], ["tsunade", "shizune"]
            ]
        }

    def _build_location_rules(self) -> Dict:
        """
        Spawn-Regeln für NPCs an verschiedenen Locations
        WICHTIG: Sukuna ist NICHT in den spawn_pools - er ist der Spieler!
        """
        return {
            "tsunades_haus": {
                "name": "Tsunades Haus",
                "description": "Das gemütliche Zuhause der Hokage",
                "max_characters": 3,  # Reduziert da Sukuna schon da ist
                "multi_spawn_chance": 0.6,
                "preferred_groups": ["tsunade_care_team", "hokage_office", "medical_team"],
                "spawn_pools": {
                    "always_available": ["tsunade"],  # Tsunade ist immer zu Hause
                    "very_common": ["shizune"],  # SUKUNA ENTFERNT - er ist der Spieler!
                    "common": ["naruto", "sakura"],
                    "uncommon": ["kakashi"],
                    "rare": ["sasuke", "ino"]
                },
                "emotional_encounters": True,
                "sukuna_home": True  # Markiert als Sukunas Zuhause
            },

            "dorf_zentrum": {
                "name": "Dorfzentrum von Konoha",
                "description": "Geschäftiges Zentrum mit Geschäften und Ständen",
                "max_characters": 4,
                "multi_spawn_chance": 0.7,
                "preferred_groups": ["girl_friends", "naruto_friends", "lazy_duo", "random_pairs"],
                "spawn_pools": {
                    "very_common": ["naruto", "sasuke", "sakura", "ino", "shikamaru", "choji"],
                    "common": ["hinata", "kiba", "shino", "neji", "lee", "tenten"],
                    "uncommon": ["kakashi", "might_guy"],
                    "rare": ["tsunade", "shizune"]
                },
                "civilian_area": True
            },

            "training_area": {
                "name": "Trainingsplatz",
                "description": "Weitläufiger Platz für Ninja-Training",
                "max_characters": 4,
                "multi_spawn_chance": 0.8,
                "preferred_groups": ["team_7", "team_guy", "training_partners", "rivals"],
                "spawn_pools": {
                    "very_common": ["naruto", "sasuke", "sakura", "lee", "neji", "tenten"],
                    "common": ["might_guy", "kakashi", "kiba", "shino"],
                    "uncommon": ["hinata", "ino", "shikamaru", "choji"],
                    "rare": ["tsunade"]
                },
                "training_focus": True
            },

            "ramen_stand": {
                "name": "Ichiraku Ramen",
                "description": "Narutos Lieblings-Ramen-Stand",
                "max_characters": 3,
                "multi_spawn_chance": 0.5,
                "preferred_groups": ["naruto_friends", "team_7", "lazy_duo"],
                "spawn_pools": {
                    "very_common": ["naruto"],
                    "common": ["sakura", "hinata", "choji"],
                    "uncommon": ["sasuke", "kiba", "ino"],
                    "rare": ["kakashi", "shikamaru"]
                },
                "social_hub": True
            },

            "hokage_turm": {
                "name": "Hokage-Turm",
                "description": "Administratives Zentrum des Dorfes",
                "max_characters": 3,
                "multi_spawn_chance": 0.4,
                "preferred_groups": ["hokage_office", "jonin_senseis", "clan_heads"],
                "spawn_pools": {
                    "always_available": ["tsunade"],
                    "very_common": ["shizune"],
                    "common": ["kakashi"],
                    "uncommon": ["might_guy", "inoichi", "shikaku"],
                    "rare": ["naruto", "sakura"]
                },
                "official_business": True
            },

            "wald": {
                "name": "Wald um Konoha",
                "description": "Dichter Wald für Training und Missionen",
                "max_characters": 3,
                "multi_spawn_chance": 0.4,
                "preferred_groups": ["team_8", "wolf_clan_members", "trauma_understanders"],
                "spawn_pools": {
                    "very_common": ["naruto", "sasuke", "kakashi"],
                    "common": ["kiba", "shino", "hinata", "neji"],
                    "uncommon": ["lee", "tenten", "might_guy"],
                    "rare": ["ino", "sakura"]
                },
                "mission_area": True,
                "wolf_friendly": True  # Guter Ort für Sukunas Wolfsnatur
            },

            "onsen": {
                "name": "Heiße Quellen",
                "description": "Entspannende heiße Quellen",
                "max_characters": 4,
                "multi_spawn_chance": 0.6,
                "preferred_groups": ["girl_friends"],
                "spawn_pools": {
                    "female_section": {
                        "very_common": ["tsunade", "sakura", "ino", "hinata"],
                        "common": ["shizune", "tenten", "tsume"],
                        "rare": []
                    },
                    "male_section": {
                        "very_common": ["naruto", "kakashi"],
                        "common": ["might_guy", "shikamaru", "choji"],
                        "uncommon": ["sasuke", "neji", "lee", "kiba"],
                        "rare": ["shino"]
                    }
                },
                "relaxation": True,
                "gender_separated": True
            },

            "hospital": {
                "name": "Konoha-Hospital",
                "description": "Medizinisches Zentrum des Dorfes",
                "max_characters": 3,
                "multi_spawn_chance": 0.3,
                "preferred_groups": ["medical_team"],
                "spawn_pools": {
                    "always_available": ["medical_staff"],
                    "very_common": ["sakura", "tsunade", "shizune"],
                    "common": ["kabuto"],
                    "rare": ["naruto", "kakashi"]
                },
                "medical_focus": True
            },

            "academy": {
                "name": "Ninja-Akademie",
                "description": "Ausbildungsort für junge Ninja",
                "max_characters": 6,
                "multi_spawn_chance": 0.8,
                "preferred_groups": ["team_7", "team_8", "team_10", "team_guy"],
                "spawn_pools": {
                    "very_common": ["naruto", "sasuke", "sakura", "ino", "shikamaru", "choji"],
                    "common": ["hinata", "kiba", "shino", "neji", "lee", "tenten"],
                    "uncommon": ["kakashi", "might_guy"],
                    "rare": []
                },
                "educational": True
            },

            "memorial_stone": {
                "name": "Gedenkstein",
                "description": "Denkmal für gefallene Ninja",
                "max_characters": 2,
                "multi_spawn_chance": 0.3,
                "preferred_groups": ["jonin_senseis", "trauma_understanders"],
                "spawn_pools": {
                    "very_common": ["kakashi"],
                    "common": ["might_guy"],
                    "uncommon": ["neji", "lee"],
                    "rare": ["naruto", "sasuke", "sakura"]
                },
                "memorial": True,
                "emotional_significance": True
            },

            "akatsuki_hideout": {
                "name": "Verlassenes Versteck",
                "description": "Geheimes Akatsuki-Versteck",
                "max_characters": 3,
                "multi_spawn_chance": 0.7,
                "preferred_groups": ["akatsuki_duo", "akatsuki_artists", "akatsuki_leaders"],
                "spawn_pools": {
                    "very_common": ["itachi", "kisame", "pain"],
                    "common": ["sasori", "deidara", "hidan"],
                    "uncommon": ["orochimaru", "kabuto"],
                    "rare": []
                },
                "villain_area": True,
                "dangerous": True
            }
        }

    def attempt_multi_encounter(self, location: str) -> Dict:
        """
        🎯 HAUPTMETHODE: Spawnt NPCs für Multi-Character Encounter mit Sukuna

        Returns:
            Dict mit encounter info oder None falls Single-Encounter
        """

        if location not in self.location_spawn_rules:
            return None

        location_rules = self.location_spawn_rules[location]

        # Prüfe ob Multi-Spawn passiert
        if random.random() > location_rules["multi_spawn_chance"]:
            return None  # Single-Encounter

        # Bestimme Anzahl NPCs (Sukuna ist schon da)
        max_chars = location_rules["max_characters"]
        num_characters = random.randint(1, max_chars)  # 1-3 NPCs + Sukuna

        # Wähle Spawn-Strategie
        if random.random() < 0.6:  # 60% Chance für Gruppen-Spawn
            characters = self._spawn_character_group(location, num_characters)
        else:  # 40% Chance für Random-Spawn
            characters = self._spawn_random_characters(location, num_characters)

        if len(characters) < 1:
            return None  # Mindestens 1 NPC nötig

        # Generiere Encounter-Info mit Sukuna als Spieler
        encounter_info = self._generate_multi_encounter_info(characters, location)

        return encounter_info

    def _spawn_character_group(self, location: str, target_count: int) -> List[str]:
        """
        Spawnt eine logische NPC-Gruppe (ohne Sukuna)
        """
        location_rules = self.location_spawn_rules[location]
        preferred_groups = location_rules.get("preferred_groups", [])
        spawn_pools = location_rules.get("spawn_pools", {})

        # Wähle verfügbare Gruppe
        available_groups = []
        for group_name in preferred_groups:
            if group_name in self.character_groups:
                group = self.character_groups[group_name]
                # Entferne Sukuna falls er versehentlich in einer Gruppe ist
                valid_chars = [char for char in group if
                               char != "sukuna" and self._char_in_spawn_pools(char, spawn_pools)]
                if len(valid_chars) >= 1:
                    available_groups.append((group_name, valid_chars))

        if not available_groups:
            return self._spawn_random_characters(location, target_count)

        # Wähle Gruppe und Charaktere
        chosen_group_name, chosen_chars = random.choice(available_groups)
        selected = random.sample(chosen_chars, min(target_count, len(chosen_chars)))

        print(f"🎭 NPC-Gruppe '{chosen_group_name}' für Sukuna gespawnt: {selected}")
        return selected

    def _spawn_random_characters(self, location: str, target_count: int) -> List[str]:
        """
        Spawnt zufällige NPCs (ohne Sukuna)
        """
        spawn_pools = self.location_spawn_rules[location].get("spawn_pools", {})

        spawned = []
        for _ in range(target_count):
            # Rarity-basierte Auswahl
            rarity = self._determine_character_rarity()

            if rarity in spawn_pools and spawn_pools[rarity]:
                available = [char for char in spawn_pools[rarity] if char not in spawned and char != "sukuna"]
                if available:
                    spawned.append(random.choice(available))

        return spawned

    def _char_in_spawn_pools(self, character: str, spawn_pools: Dict) -> bool:
        """
        Prüft ob NPC in den Spawn-Pools ist (Sukuna wird ignoriert)
        """
        if character == "sukuna":
            return False  # Sukuna spawnt nie als NPC

        for pool_name, pool_chars in spawn_pools.items():
            if isinstance(pool_chars, list) and character in pool_chars:
                return True
            elif isinstance(pool_chars, dict):  # Für geschlechtergetrennte Bereiche
                for sub_pool in pool_chars.values():
                    if isinstance(sub_pool, list) and character in sub_pool:
                        return True
        return False

    def _determine_character_rarity(self) -> str:
        """
        Bestimmt Character Rarity basierend auf Wahrscheinlichkeiten
        """
        roll = random.random()
        if roll < 0.05:  # 5%
            return "always_available"
        elif roll < 0.20:  # 15%
            return "rare"
        elif roll < 0.50:  # 30%
            return "uncommon"
        elif roll < 0.80:  # 30%
            return "common"
        else:  # 20%
            return "very_common"

    def _generate_multi_encounter_info(self, npc_characters: List[str], location: str) -> Dict:
        """
        Generiert Encounter-Info mit Sukuna als Spieler und NPCs
        """

        # Bestimme Haupt-NPC (mit dem primary gesprochen wird)
        primary_npc = npc_characters[0] if npc_characters else None
        secondary_npcs = npc_characters[1:] if len(npc_characters) > 1 else []

        # Bestimme Situation mit Sukuna im Fokus
        situation = self._determine_situation_with_sukuna(npc_characters, location)

        encounter_info = {
            "type": "multi_character",
            "location": location,
            "npc_characters": npc_characters,  # Nur NPCs
            "primary_npc": primary_npc,  # Haupt-NPC
            "secondary_npcs": secondary_npcs,  # Weitere NPCs
            "situation": situation,
            "sukuna_context": self._get_sukuna_context(npc_characters, location),
            "group_dynamic": self._analyze_group_dynamic_with_sukuna(npc_characters),
            "conversation_starters": self._generate_conversation_starters_for_sukuna(npc_characters, situation)
        }

        return encounter_info

    def _determine_situation_with_sukuna(self, npc_characters: List[str], location: str) -> str:
        """
        Bestimmt Situation mit SUKUNA als SPIELER im Fokus
        """

        if not npc_characters:
            return "Solo Exploration"

        # ===== SUKUNA-SPEZIFISCHE SITUATIONEN =====

        # Tsunade + Sukuna = Familie
        if "tsunade" in npc_characters:
            if "shizune" in npc_characters:
                return random.choice([
                    "Mütterliche Fürsorge von Tsunade", "Familiäre Betreuung",
                    "Medizinische Untersuchung durch Familie",
                    "Tsunades Sorge um Sukuna", "Hokage-Großmutter Zeit"
                ])
            else:
                return random.choice([
                    "Tsunade-Sukuna Mutter-Sohn Zeit", "Großmütterliche Liebe", "Familiäre Bindung",
                    "Tsunades Schutzinstinkt", "Emotionale Unterstützung"
                ])

        # Wolf-Clan begegnet Sukuna
        if any(char in npc_characters for char in ["kiba", "tsume"]):
            wolf_chars = [char for char in npc_characters if char in ["kiba", "tsume"]]
            return random.choice([
                f"Wolf-Verbindung mit {', '.join(wolf_chars)}", "Canine Bond Recognition", "Pack Instinct Meeting",
                "Wolfsnatur Erkennung", "Rudel-Akzeptanz", "Wild Nature Connection"
            ])

        # Akatsuki-Trauma Verstehende
        if any(char in npc_characters for char in ["sasuke", "kakashi", "itachi"]):
            trauma_chars = [char for char in npc_characters if char in ["sasuke", "kakashi", "itachi"]]
            return random.choice([
                f"Trauma-Verständnis mit {', '.join(trauma_chars)}", "Shared Pain Recognition",
                "Dark Past Understanding",
                "Survivor Solidarity", "Emotional Healing Session"
            ])

        # Medizinisches Personal
        if any(char in npc_characters for char in ["sakura", "shizune"]):
            return random.choice([
                "Medizinische Untersuchung", "Heilung für Sukuna", "Gesundheitscheck",
                "Wunden-Behandlung", "Recovery Session"
            ])

        # Akatsuki-Begegnung (gefährlich!)
        if any(char in npc_characters for char in ["itachi", "kisame", "pain", "sasori", "hidan", "deidara"]):
            akatsuki_chars = [char for char in npc_characters if
                              char in ["itachi", "kisame", "pain", "sasori", "hidan", "deidara"]]
            if "itachi" in akatsuki_chars:
                return random.choice([
                    "Itachis heimliche Hilfe", "Schutz durch Itachi", "Uchiha-Unterstützung",
                    "Versteckte Allianz", "Itachis wahre Loyalität"
                ])
            else:
                return random.choice([
                    f"Gefährliche Akatsuki-Begegnung", "Villain Konfrontation", "Bedrohliche Situation",
                    "Akatsuki-Spannung", "Dangerous Encounter"
                ])

        # Team 7 (ohne Sukuna)
        if set(npc_characters) == set(["naruto", "sasuke", "sakura"]):
            return random.choice([
                "Team 7 begegnet Sukuna", "Neuer Teamkamerad?", "Team 7 Interesse an Sukuna",
                "Mögliche Team-Erweiterung", "Ninja-Team trifft Wolf-Junge"
            ])

        # Naruto-spezifisch (Jinchuriki-Verbindung)
        if "naruto" in npc_characters:
            return random.choice([
                "Jinchuriki-Verbindung mit Naruto", "Dämon-Träger treffen sich", "Shared Burden Understanding",
                "Beast Spirit Connection", "Fellow Outcast Meeting"
            ])

        # ===== LOCATION-SPEZIFISCHE SITUATIONEN =====

        if location.startswith("tsunades_haus"):
            return random.choice([
                "Zuhause-Atmosphäre", "Sukunas Zuhause-Leben", "Häusliche Begegnung",
                "Family Home Encounter", "Safe Space Meeting"
            ])

        elif location == "training_area":
            return random.choice([
                "Training mit den anderen", "Sukuna zeigt seine Fähigkeiten", "Wolf-Training Session",
                "Combat Skills Demonstration", "Power Sharing"
            ])

        elif location == "dorf_zentrum":
            return random.choice([
                "Sukuna erkundet das Dorf", "Village Life Introduction", "Social Integration",
                "Community Acceptance", "New Life Beginning"
            ])

        elif location == "akatsuki_hideout":
            return random.choice([
                "Rückkehr zum Trauma-Ort", "Confronting the Past", "Dangerous Territory",
                "Facing Old Demons", "Closure Mission"
            ])

        # ===== FALLBACK =====
        return random.choice([
            "NPCs treffen auf Sukuna", "Curious Encounter", "Getting to Know Sukuna",
            "Wolf-Boy Meeting", "New Arrival Interest"
        ])

    def _get_sukuna_context(self, npc_characters: List[str], location: str) -> Dict:
        """
        Gibt Sukuna-spezifischen Kontext zurück
        """
        context = {
            "player_is": "sukuna",
            "wolf_spirit": True,
            "trauma_background": "akatsuki_torture",
            "family": "tsunade_adoptive_mother",
            "home": "tsunades_haus",
            "special_connections": []
        }

        # Spezielle Verbindungen zu NPCs
        if "tsunade" in npc_characters:
            context["special_connections"].append("maternal_bond_with_tsunade")

        if any(char in npc_characters for char in ["kiba", "tsume"]):
            context["special_connections"].append("wolf_clan_recognition")

        if "naruto" in npc_characters:
            context["special_connections"].append("jinchuriki_solidarity")

        if "itachi" in npc_characters:
            context["special_connections"].append("secret_protector")

        return context

    def _analyze_group_dynamic_with_sukuna(self, npc_characters: List[str]) -> Dict:
        """
        Analysiert Gruppendynamik mit SUKUNA als Spieler-Fokus
        """
        dynamics = {
            "sukuna_acceptance": "neutral",
            "protection_level": "none",
            "curiosity_about_sukuna": "medium",
            "wolf_recognition": False,
            "family_feeling": False,
            "danger_level": "safe"
        }

        # Tsunade bringt maximale Familie und Schutz
        if "tsunade" in npc_characters:
            dynamics["sukuna_acceptance"] = "unconditional_love"
            dynamics["protection_level"] = "maximum"
            dynamics["family_feeling"] = True

        # Wolf-Clan erkennt Sukuna
        if any(char in npc_characters for char in ["kiba", "tsume"]):
            dynamics["wolf_recognition"] = True
            dynamics["sukuna_acceptance"] = "pack_acceptance"

        # Naruto versteht als Jinchuriki
        if "naruto" in npc_characters:
            dynamics["sukuna_acceptance"] = "brotherhood"
            dynamics["understanding_level"] = "very_high"

        # Medizinisches Personal sorgt sich
        if any(char in npc_characters for char in ["sakura", "shizune"]):
            dynamics["medical_concern"] = "high"
            dynamics["healing_focus"] = True

        # Akatsuki bringt Gefahr
        akatsuki_members = ["itachi", "kisame", "pain", "sasori", "hidan", "deidara"]
        if any(char in npc_characters for char in akatsuki_members):
            dynamics["danger_level"] = "high"
            if "itachi" in npc_characters:
                dynamics["hidden_protection"] = True
            else:
                dynamics["threat_level"] = "very_high"

        return dynamics

    def _generate_conversation_starters_for_sukuna(self, npc_characters: List[str], situation: str) -> List[str]:
        """
        Generiert Conversation Starter die SUKUNA verwenden kann
        """

        starters = []

        # Allgemeine Starter für Sukuna
        starters.extend([
            "Hallo...",
            "Ich wollte nicht stören...",
            "Was macht ihr hier?",
            "Kann ich... mitmachen?"
        ])

        # Sukuna-spezifische Starter basierend auf NPCs
        if "tsunade" in npc_characters:
            starters.extend([
                "Tsunade-obaa-chan, geht es dir gut?",
                "Ich habe dich vermisst...",
                "Kann ich bei dir bleiben?"
            ])

        if any(char in npc_characters for char in ["kiba", "tsume"]):
            starters.extend([
                "Ihr... spürt es auch, oder? Diese Verbindung?",
                "Mein Wolfsgeist erkennt euch...",
                "Seid ihr... wie ich?"
            ])

        if "naruto" in npc_characters:
            starters.extend([
                "Du hast auch einen Dämon in dir, stimmt's?",
                "Wir sind ähnlich, glaube ich...",
                "Verstehst du, wie es ist?"
            ])

        if any(char in npc_characters for char in ["sakura", "shizune"]):
            starters.extend([
                "Könnt ihr... meine Wunden anschauen?",
                "Tut mir leid, wenn ich Probleme mache...",
                "Ich fühle mich nicht so gut..."
            ])

        # Situations-spezifische Starter
        situation_starters = {
            "Training": [
                "Kann ich auch trainieren?",
                "Zeigt ihr mir, wie es geht?",
                "Ich möchte stärker werden..."
            ],
            "Medical": [
                "Es tut noch weh...",
                "Die Narben brennen manchmal...",
                "Kann ich geheilt werden?"
            ],
            "Family": [
                "Ist das... ein Zuhause?",
                "Gehöre ich auch dazu?",
                "Was ist eine Familie?"
            ]
        }

        # Finde passende Situation
        for key, specific_starters in situation_starters.items():
            if key.lower() in situation.lower():
                starters.extend(specific_starters)

        return starters[:8]  # Maximal 8 Starter


def integrate_multi_encounter_system(encounter_system, game_data):
    """
    🔧 INTEGRATION: Fügt Sukuna-fokussiertes Multi-Character System hinzu
    """

    multi_system = MultiCharacterEncounterSystem()

    def enhanced_check_for_encounter(location_name: str):
        """
        Erweiterte Encounter-Check mit Sukuna als Spieler
        """

        # Prüfe Multi-Character Possibility
        multi_encounter = multi_system.attempt_multi_encounter(location_name)

        if multi_encounter:
            # Multi-Character Encounter mit NPCs für Sukuna!
            setup_multi_character_encounter_for_sukuna(multi_encounter, game_data)
            return multi_encounter
        else:
            # Normal Single-Character Encounter
            return encounter_system.check_for_encounter(location_name)

    def setup_multi_character_encounter_for_sukuna(encounter_info: Dict, game_data):
        """
        Setup für Multi-Character Encounter mit Sukuna als Spieler
        """
        npc_chars = encounter_info["npc_characters"]
        primary_npc = encounter_info["primary_npc"]
        situation = encounter_info["situation"]

        # Setze Multi-Character Modus
        if hasattr(game_data, 'multi_chat'):
            game_data.multi_chat.start_multi_conversation(npc_chars, situation)

        # Formatiere Nachricht für Sukuna
        if len(npc_chars) == 1:
            encounter_msg = f"""🎭 **ENCOUNTER**

📍 **Ort**: {encounter_info['location'].title()}
👤 **Begegnung**: {primary_npc.title()}
📖 **Situation**: {situation}

💭 Du als Sukuna triffst auf {primary_npc.title()}."""
        else:
            npc_list = ", ".join([char.title() for char in npc_chars])
            encounter_msg = f"""🎉 **MULTI-CHARACTER ENCOUNTER**

📍 **Ort**: {encounter_info['location'].title()}
👥 **NPCs**: {npc_list}
🗣️ **Haupt-NPC**: {primary_npc.title()}
📖 **Situation**: {situation}

💭 Du als Sukuna triffst auf mehrere Charaktere! Du kannst mit {primary_npc.title()} sprechen, aber {', '.join([char.title() for char in encounter_info['secondary_npcs']])} ist/sind auch anwesend.

🔄 Verwende '/switch [character]' um den Haupt-Gesprächspartner zu wechseln!"""

        if hasattr(game_data, 'chat_messages'):
            game_data.chat_messages.append(("MULTI-ENCOUNTER", encounter_msg))

        print(f"🎭 Sukuna begegnet: {npc_list if len(npc_chars) > 1 else primary_npc} in {encounter_info['location']}")

    # Integriere Methoden
    encounter_system.multi_encounter_system = multi_system
    encounter_system.enhanced_check_for_encounter = enhanced_check_for_encounter
    encounter_system.setup_multi_character_encounter_for_sukuna = setup_multi_character_encounter_for_sukuna

    print("✅ Sukuna-fokussiertes Multi-Character Encounter System integriert!")
    return multi_system


if __name__ == "__main__":
    # Test des Sukuna-fokussierten Systems
    multi_system = MultiCharacterEncounterSystem()

    print("🎭 SUKUNA-FOKUSSIERTES MULTI-CHARACTER ENCOUNTER SYSTEM TEST")
    print("Der Spieler IST Sukuna - NPCs spawnen für ihn!")

    test_locations = ["tsunades_haus", "training_area", "dorf_zentrum"]

    for location in test_locations:
        print(f"\n📍 Testing {location}:")
        for _ in range(5):
            encounter = multi_system.attempt_multi_encounter(location)
            if encounter:
                npcs = encounter["npc_characters"]
                situation = encounter["situation"]
                print(f"  🎉 NPCs: {npcs} | Situation: {situation}")
            else:
                print(f"  🔘 Single encounter")