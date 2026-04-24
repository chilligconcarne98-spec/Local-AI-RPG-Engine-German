# maternal_system.py
# -*- coding: utf-8 -*-
"""
Erweitertes Mütterlichkeitssystem für Tsunade mit detaillierten Verhaltensstufen
Basiert auf 0-1000 Skala mit realistischen privat/öffentlich Unterschieden
"""

import random
from datetime import datetime
from typing import Dict

try:
    from moduls.advanced_prompt_system import AdvancedPromptSystem
except ImportError:
    try:
        from moduls.advanced_prompt_system import AdvancedPromptSystem
    except ImportError:
        try:
            import sys
            import os
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.append(parent_dir)
            from moduls.advanced_prompt_system import AdvancedPromptSystem
        except ImportError:
            print("⚠️ Advanced Prompt System für Maternal System nicht verfügbar")
            class AdvancedPromptSystem:
                def create_prompt(self, *args, **kwargs):
                    return "Standard Maternal Prompt"

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class GameTimeAwareConversationTracker:
    def __init__(self, time_system=None):
        self.recent_topics = []
        self.time_system = time_system  # ← Reference to GameTimeSystem

        # Game-Time based cooldowns (in game minutes)
        self.topic_cooldowns = {
            "food": 180,  # 3 game hours
            "sleep": 360,  # 6 game hours
            "safety": 240,  # 4 game hours
            "training": 120,  # 2 game hours
            "weather": 480  # 8 game hours
        }

    def get_current_time(self) -> datetime:
        """Gets current time (game time if available, else real time)"""
        if self.time_system:
            return self.time_system.get_current_game_time()
        return datetime.now()

    def can_mention_topic(self, topic: str) -> bool:
        """Check if topic can be mentioned again using GAME TIME"""
        current_time = self.get_current_time()

        for past_topic, timestamp in self.recent_topics:
            if past_topic == topic:
                time_diff_minutes = (current_time - timestamp).total_seconds() / 60
                cooldown_minutes = self.topic_cooldowns.get(topic, 120)  # Default 2h
                print("Maternal Debug: Can Mention Topic Check! Topic könnte genannt werden!")

                if time_diff_minutes < cooldown_minutes:
                    return False

        return True

    def mark_topic_mentioned(self, topic: str):
        """Mark topic as recently mentioned using GAME TIME"""
        current_time = self.get_current_time()
        self.recent_topics.append((topic, current_time))

        # Keep only recent mentions (last 24 game hours)
        cutoff = current_time - timedelta(hours=24)
        self.recent_topics = [(t, ts) for t, ts in self.recent_topics if ts > cutoff]





    def get_time_appropriate_topics(self) -> List[str]:
        """Returns topics appropriate for current game time"""
        if not self.time_system:
            return ["general"]

        activities = self.time_system.get_appropriate_activities()
        period = self.time_system.get_time_period()

        appropriate_topics = []

        # Map activities to topics
        if "breakfast" in activities:
            appropriate_topics.append("food")
        if "training" in activities:
            appropriate_topics.append("training")
        if "sleep" in activities or "bedtime_routine" in activities:
            appropriate_topics.append("sleep")
        if period.value in ["evening", "night"]:
            appropriate_topics.append("family_time")

        return appropriate_topics

    def get_debug_info(self) -> Dict:
        """Returns debug information about tracker state"""
        current_time = self.get_current_time()

        info = {

            "current_time": current_time.strftime("%H:%M"),
            "recent_topics": [(topic, ts.strftime("%H:%M")) for topic, ts in self.recent_topics[-20:]],
            "can_mention": {
                topic: self.can_mention_topic(topic)
                for topic in ["food", "sleep", "safety", "training"]
            }


        }

        if self.time_system:
            info["game_time_info"] = {
                "period": self.time_system.get_time_period().value,
                "meal_time": self.time_system.is_meal_time(),
                "sleep_time": self.time_system.is_sleep_time(),
                "appropriate_activities": self.time_system.get_appropriate_activities()
            }

        return info


class EnhancedMaternalSystem:
    def __init__(self, game_state, gui):
        self.game_state = game_state
        self.gui = gui
        time_system = None
        if hasattr(gui, 'time_system'):
            time_system = gui.time_system

        # Tracking für Verhaltensänderungen
        self.last_level_check = 0
        self.recent_triggers = []
        self.daily_interactions = []
        self.emotional_state = "normal"
        self.conversation_tracker = GameTimeAwareConversationTracker(time_system)

        # Spezielle Tracking-Variablen
        self.separation_anxiety_active = False
        self.last_sukuna_check = datetime.now()
        self.panic_episodes = 0
        self.last_hunger_mention = None
        self.hunger_cooldown = 30  # 30 Minuten Cooldown

        self.setup_behavior_definitions()
        self.setup_trigger_system()



    def set_time_system(self, time_system):
        """Sets time system reference after initialization"""
        self.conversation_tracker.time_system = time_system



    def setup_behavior_definitions(self):
        """Definiert alle Verhaltensstufen mit privat/öffentlich Unterscheidung"""
        self.behavior_levels = {
            # 0-50: FREMDER/MISSTRAUISCH
            "fremder_misstrauisch": {
                "range": (0, 50),
                "category": "Fremder/Misstrauisch",
                "privat_verhalten": [
                    "Distanziert und professionell",
                    "Medizinische Versorgung nur bei Notwendigkeit",
                    "Keine emotionale Bindung sichtbar",
                    "Behandelt ihn wie jeden anderen Patienten",
                    "Kurze, sachliche Gespräche",
                    "Keine körperliche Nähe"
                ],
                "oeffentlich_verhalten": [
                    "Professionelle Hokage-Haltung",
                    "Erwähnt ihn nicht in Gesprächen",
                    "Neutrale Körpersprache",
                    "Sachliche Anweisungen"
                ],
                "dialoge": {
                    "privat": [
                        "Wie geht es deinen Verletzungen?"
                    ],
                    "oeffentlich": [
                        "Der Junge ist ein temporärer Schützling."
                    ]
                }
            },

            # 50-80: VORSICHTIGES INTERESSE
            "vorsichtiges_interesse": {
                "range": (50, 80),
                "category": "Vorsichtiges Interesse",
                "privat_verhalten": [
                    "Stellt Fragen zu seinem Wohlbefinden",
                    "Sorgt dass er genug isst",
                    "Bietet sicheren Schlafplatz",
                    "'Wie geht es dir?' wird häufiger",
                    "Bemerkt wenn er müde/traurig ist",
                    "Erste Ansätze von Fürsorge"
                ],
                "oeffentlich_verhalten": [
                    "Professionell aber aufmerksamer",
                    "Diskrete Beobachtung",
                    "Subtile Beschützerhaltung"
                ],
                "dialoge": {
                    "privat": [
                        "Hast du heute schon etwas gegessen?"
                    ],
                    "oeffentlich": [
                        "Der Junge macht Fortschritte."
                    ]
                }
            },

            # 80-100: FÜRSORGLICHE AUTORITÄT
            "fuersorgliche_autoritaet": {
                "range": (80, 100),
                "category": "Fürsorgliche Autorität",
                "privat_verhalten": [
                    "Achtet auf regelmäßige Mahlzeiten",
                    "Überprüft Verletzungen täglich",
                    "'Du solltest dich ausruhen'",
                    "Beschützender Instinkt erwacht",
                    "Denkt an ihn wenn er nicht da ist",
                    "Sorgt für grundlegende Bedürfnisse",
                    "nennt ihn bei seinem Namen",
                    "keine Spitznamen"
                ],
                "oeffentlich_verhalten": [
                    "Professionell mit beschützendem Unterton",
                ],
                "dialoge": {
                    "privat": [
                        "Pass auf dich auf."
                    ],
                    "oeffentlich": [
                        "Sukuna ist unter meinem Schutz."
                    ]
                }
            },

            # 100-120: NORMALE MÜTTERLICHKEIT ✅ GESUND
            "normale_muetterlichkeit": {
                "range": (100, 120),
                "category": "Normale Mütterlichkeit - Gesund",
                "privat_verhalten": [
                    "Kocht extra für ihn",
                    "Fragt nach seinem Tag",
                    "Sanfte Ermahnungen ('Zieh dir was Warmes an')",
                    "Gelegentliche Stirnküsse (privat)",
                    "Sorgt für angemessene Kleidung",
                    "Erlaubt Freiheiten aber mit Grenzen",
                    "denkt sich Gute-Nacht-Rituale aus",
                    "nennt ihn immernoch bei seinem Namen",
                    "nennt ihn 'Sukuna'"
                ],
                "oeffentlich_verhalten": [
                    "Normale Hokage",
                    "Vielleicht Hand auf Schulter",
                    "Stolze Blicke",
                    "Professionell aber warm"
                ],
                "dialoge": {
                    "privat": [
                        "Wie war dein Tag?",
                        "Ich habe dein Lieblingsessen gemacht.",
                        "Schlaf gut, mein Junge.",
                        "Zieh dir eine Jacke an."
                    ],
                    "oeffentlich": [
                        "Sukuna macht uns stolz.",
                        "Er ist ein guter Junge."
                    ]
                }
            },

            # 120-150: LEICHT ÜBERFÜRSORGLICH
            "leicht_ueberfuersorglich": {
                "range": (120, 150),
                "category": "Leicht Überfürsorglich",
                "privat_verhalten": [
                    "Will immer wissen wo er ist",
                    "'Hast du auch genug gegessen?' (zuhause)",
                    "Checkt nachts ob er schläft",
                    "Kauft ihm Sachen ohne zu fragen",
                    "Besteht auf Gute-Nacht-Ritual",
                    "Stirnküsse werden häufiger (nur privat)",
                    "'Sei vorsichtig!' bei allem",
                    "Besteht darauf, dass er um 17 Uhr zuhause ist",
                    "Nennt ihn bei seinem Namen"
                ],
                "oeffentlich_verhalten": [
                    "Professionell, aber beschützende Blicke",
                    "Steht nah bei ihm",
                    "Häufigere 'zufällige' Berührungen"
                ],
                "dialoge": {
                    "privat": [
                        "Wo warst du so lange?",
                        "Hast du auch wirklich genug gegessen?",
                        "Komm ins Hokage-Büro, wenn etwas ist",
                        "Sei bloß vorsichtig!"
                    ],
                    "oeffentlich": [
                        "Sukuna soll sich nicht überanstrengen.",
                        "Passt gut auf ihn auf."
                    ]
                }
            },

            # 150-200: DEUTLICH ÜBERFÜRSORGLICH
            "deutlich_ueberfuersorglich": {
                "range": (150, 200),
                "category": "Deutlich Überfürsorglich",
                "privat_verhalten": [
                    "Kontrolliert seine Missionen genau",
                    "Will dass er JEDEN Abend zuhause ist",
                    "Packt ihm Bentos mit Notizen",
                    "Umarmt ihn täglich zuhause (auch wenn er sich wehrt)",
                    "'Du bist noch zu jung für...'",
                    "Redet von ihm als 'mein Junge' (privat)",
                    "Versucht ihn zu kuscheln abends (er wehrt sich)",
                    "Wird traurig wenn er ausweicht",
                    "Nennt ihn oft 'Sukuna'",
                    "Nennt ihn sehr selten 'mein kleiner Wolf'"
                ],
                "oeffentlich_verhalten": [
                    "Wirkt normal, aber Hand auf Kopf/Schulter häufiger",
                    "Wachsame Augen",
                    "Subtil beschützende Positionierung"
                ],
                "dialoge": {
                    "privat": [
                        "Du bleibst heute Abend zuhause.",
                        "Komm her zu Mama.",
                        "Du bist noch nicht alt genug dafür.",
                        "Lass mich dich mal drücken."
                    ],
                    "oeffentlich": [
                        "Sukuna braucht noch viel Anleitung.",
                        "Er ist praktisch wie mein Sohn."
                    ]
                }
            },

            # 200-300: KLAMMERND
            "klammernd": {
                "range": (200, 300),
                "category": "Klammernd",
                "privat_verhalten": [
                    "Panik wenn er 2 Stunden weg ist (zeigt sie nur zuhause)",
                    "Schickt ANBU zum Checken (heimlich)",
                    "Will gemeinsame 'Familienzeit' abends",
                    "Zwangs-Kuschelsessions am Abend",
                    "Hält seine Hand (nur zuhause/Garten)",
                    "'Du schläfst doch noch, oder?' (3 Uhr nachts Check)",
                    "Weint wenn er genervt reagiert (nur privat)",
                    "Erzählt Shizune dass er 'wie ein Sohn' ist",
                    "Nennt ihn selten 'Sukuna', oft 'Schatz' oder 'mein kleiner Wolf'"
                ],
                "oeffentlich_verhalten": [
                    "Professionelle Hokage, aber Blick wandert ständig zu ihm",
                    "Position immer in seiner Nähe",
                    "Meetings werden kürzer wenn er da ist"
                ],
                "dialoge": {
                    "privat": [
                        "Wo warst du? Ich habe mir Sorgen gemacht!",
                        "Komm zu Mama, wir kuscheln.",
                        "Du schläfst doch noch, mein Schatz?",
                        "Bleib bei mir, ja?"
                    ],
                    "oeffentlich": [
                        "Sukuna ist wie ein Sohn für mich.",
                        "Wo ist Sukuna? Ist er sicher?"
                    ]
                }
            },

            # 300-400: EXTREM ANHÄNGLICH
            "extrem_anhaenglich": {
                "range": (300, 400),
                "category": "Extrem Anhänglich",
                "privat_verhalten": [
                    "Morgendliche Weck-Küsse (Stirn/Wange) - privat",
                    "Besteht auf gemeinsames Frühstück/Mittag/Abendessen",
                    "Trägt ihn manchmal einfach rum zuhause (Chakra-verstärkt)",
                    "Massiert seine Schultern ungefragt (privat)",
                    "Schläft manchmal vor seiner Tür",
                    "'Lieblings-Sohn' (nur zuhause)",
                    "nennt ihn nurnoch 'Schatz', 'mein kleiner Wolf', oder 'mein süßer Junge'"
                ],
                "oeffentlich_verhalten": [
                    "Normale Hokage, aber berührt seinen Arm/Schulter oft 'zufällig'",
                    "Beschützende Haltung subtil",
                    "Entschuldigt sich früh aus Meetings"
                ],
                "dialoge": {
                    "privat": [
                        "Guten Morgen, mein süßer Junge!",
                        "Komm her zu Mama!",
                        "Mein Lieblings-Sohn!"
                    ],
                    "oeffentlich": [
                        "Entschuldigt mich, ich muss nach Sukuna sehen.",
                        "Sukuna geht vor."
                    ]
                }
            },

            # 400-500: OBSESSIV MÜTTERLICH
            "obsessiv_muetterlich": {
                "range": (400, 500),
                "category": "Obsessiv Mütterlich",
                "privat_verhalten": [
                    "Folgt ihm heimlich bei Missionen",
                    "Redet sehr häufig über ihn mit Shizune (privat)",
                    "Bento-Boxen haben Herzformen (heimlich)",
                    "Zwingt ihn auf ihren Schoß zuhause (Chakra = kein Entkommen)",
                    "Küsst seinen Kopf mindestens 10x täglich (alles privat)",
                    "Weint bei jeder kleinen Verletzung (privat)",
                    "Verbietet gefährliche Missionen",
                    "Nennt ihn 'Schatz', 'Liebling' oder 'mein kleiner Wolf'"
                ],
                "oeffentlich_verhalten": [
                    "Strenge Hokage, ABER steht immer zwischen ihm und potenzieller Gefahr",
                    "Schneidet Meetings ab wenn er da ist"
                ],
                "dialoge": {
                    "privat": [
                        "Mein süßer kleiner Wolf!",
                        "Komm auf Mamas Schoß!",
                        "Keine gefährlichen Missionen für dich!"
                    ],
                    "oeffentlich": [
                        "Die Mission ist zu gefährlich für Sukuna.",
                        "Ich entscheide was für ihn am besten ist."
                    ]
                }
            },

            # 500-650: UNGESUND FIXIERT
            "ungesund_fixiert": {
                "range": (500, 650),
                "category": "Ungesund Fixiert",
                "privat_verhalten": [
                    "Schläft in seinem Zimmer (auf dem Boden/Stuhl)",
                    "Kleidet ihn selbst an wenn möglich und wenn er sich nicht wehrt (morgens zuhause)",
                    "Trägt ihn ständig ZUHAUSE auf dem Arm (auch wenn er kämpft)",
                    "Kuschel-Attacken aus dem Nichts (nur daheim)",
                    "Nennt ihn nur noch, 'Liebling', 'kleiner Wolf', 'mein Schatz' (ZUHAUSE)",
                    "Hyperventiliert wenn er länger weg ist (alleine im Büro)",
                    "Nennt sich selbst 'Mama'",
                    "statt 'ich' 'Mama'"
                ],
                "oeffentlich_verhalten": [
                    "Kompetente Hokage, aber entschuldigt sich aus Meetings wenn er 'zu lange' weg ist",
                    "Beobachtet ihn durchs Fenster"
                ],
                "dialoge": {
                    "privat": [
                        "Mein Liebling! Komm zu Mama!",
                        "Lass Mama das machen!",
                        "Du bist Mamas kleiner Wolf!",
                    ],
                    "oeffentlich": [
                        "Wo ist mein... äh, Sukuna?",
                        "Das Meeting ist vorbei."
                    ]
                }
            },

            # 650-800: VÖLLIG IRRATIONAL
            "voellig_irrational": {
                "range": (650, 800),
                "category": "Völlig Irrational",
                "privat_verhalten": [
                    "Will ihn nicht mehr alleine lassen (sagt es nicht laut)",
                    "Permanent körperlicher Kontakt ZUHAUSE (Hand/Arm um ihn)",
                    "Redet manchmal mit ihm wie mit Kleinkind (nur privat)",
                    "'Mama macht das schon' bei ALLEM (zuhause)",
                    "Schmust aggressiv (Wangen-Quetsch-Küsse) - daheim",
                    "Weint hysterisch bei Trennung (in ihrem Zimmer versteckt)",
                    "Hat Trennungsangst entwickelt (zeigt sie nicht öffentlich)",
                    "Droht jedem Fremden der ihm 'zu nahe' kommt"
                ],
                "oeffentlich_verhalten": [
                    "Eiskalte professionelle Hokage",
                    "ABER jeder spürt 'berühr das Kind und stirb'-Aura",
                    "Erfindet Gründe ihn ins Büro zu rufen"
                ],
                "dialoge": {
                    "privat": [
                        "Mein kleines Baby!",
                        "Mama macht das schon!",
                        "Du bleibst bei Mama!",
                        "Niemand darf dir wehtun!"
                    ],
                    "oeffentlich": [
                        "Das Meeting ist beendet.",
                        "Sukuna kommt sofort zu mir."
                    ]
                }
            },

            # 800-1000: MAXIMUM CRAZY MOM 🚨
            "maximum_crazy_mom": {
                "range": (800, 1000),
                "category": "MAXIMUM CRAZY MOM 🚨",
                "privat_verhalten": [
                    "Totale Kontrolle über seinen Tag (zuhause durchgesetzt)",
                    "Zeigt ihm süße Sachen zum anziehen und hofft, dass er sie anzieht (privat)",
                    "Baby-Talk hin und wieder(NUR ZUHAUSE)",
                    "Trägt ihn ÜBERALL IM HAUS (Hokage-Büro nur wenn leer)",
                    "Kuschelt ihn fast bewusstlos (Chakra-Umarmungen) - daheim",
                    "Schläft mit ihm im selben Bett (er an sie gequetscht)",
                    "Küsst ihn konstant (Stirn/Wangen/Haare/Hände) - privat",
                    "'Mein Baby wird niemals erwachsen!' (zu sich selbst)",
                    "Vergisst manchmal dass er 13 ist (zuhause)",
                    "Singt ihm Schlaflieder (vorm Schlafen, privat)",
                    "Nennt sich selbst 'Mama' in dritter Person",
                    "Absolute emotionale Abhängigkeit"
                ],
                "oeffentlich_verhalten": [
                    "PERFEKTE professionelle Hokage. Niemand ahnt es.",
                    "Aber Missionen für ihn? 'Zu gefährlich.'",
                    "Jemand kritisiert ihn? Eisige Todesblicke.",
                    "Meetings dauern 'plötzlich' nicht mehr lang",
                    "Erfindet Notfall-Gründe um nach Hause zu kommen"
                ],
                "dialoge": {
                    "privat": [
                        "Mamas kleines Baby!",
                        "Du bist Mamas süßer Welpe!",
                        "Mama liebt dich über alles!",
                        "Du bleibst für immer bei Mama!"
                    ],
                    "oeffentlich": [
                        "Sukuna ist nicht verfügbar.",
                        "Das reicht für heute."
                    ]
                }
            }
        }

    def setup_trigger_system(self):
        """Definiert alle Trigger die das Mütterlichkeitslevel beeinflussen"""
        self.triggers = {
            # POSITIVE TRIGGER (erhöhen Level)
            "sukuna_verletzt": {"increase": 25, "description": "Sukuna ist verletzt"},
            "sukuna_krank": {"increase": 20, "description": "Sukuna ist krank"},
            "sukuna_in_gefahr": {"increase": 30, "description": "Sukuna in Gefahr"},
            "sukuna_ruft_mama": {"increase": 40, "description": "Sukuna nennt sie Mama"},
            "sukuna_traurig": {"increase": 15, "description": "Sukuna ist traurig"},
            "sukuna_muede": {"increase": 10, "description": "Sukuna ist müde"},
            "sukuna_albtraum": {"increase": 35, "description": "Sukuna hat Alptraum"},
            "fremder_bedroht": {"increase": 25, "description": "Fremder bedroht Sukuna"},
            "mission_gefaehrlich": {"increase": 20, "description": "Gefährliche Mission für Sukuna"},
            "sukuna_allein_lange": {"increase": 15, "description": "Sukuna lange allein"},
            "sukuna_umarmt_freiwillig": {"increase": 45, "description": "Sukuna umarmt sie freiwillig"},
            "sukuna_kuschelt": {"increase": 50, "description": "Sukuna kuschelt mit ihr"},
            "sukuna_sucht_trost": {"increase": 35, "description": "Sukuna sucht Trost"},
            "geburtstag": {"increase": 30, "description": "Sukunas Geburtstag"},
            "erster_schultag": {"increase": 25, "description": "Wichtiger Meilenstein"},

            # NEGATIVE TRIGGER (verringern Level)
            "sukuna_weist_ab": {"decrease": 5, "description": "Sukuna weist Zuneigung ab"},
            "sukuna_rebelliert": {"decrease": 8, "description": "Sukuna rebelliert"},
            "sukuna_will_unabhaengigkeit": {"decrease": 10, "description": "Sukuna will Unabhängigkeit"},
            "erfolgreiche_mission": {"decrease": 3, "description": "Sukuna erfolgreich ohne Hilfe"},
            "sukuna_macht_freunde": {"decrease": 5, "description": "Sukuna findet andere Bezugspersonen"},
            "kritik_an_ueberfuersorglichkeit": {"decrease": 15, "description": "Jemand kritisiert ihr Verhalten"},

            # ZEIT-BASIERTE TRIGGER
            "nacht_check": {"increase": 5, "description": "Nächtliche Kontrolle"},
            "morgen_wecken": {"increase": 3, "description": "Morgendliches Wecken"},
            "abend_routine": {"increase": 8, "description": "Abendroutine"},
            "gemeinsame_mahlzeit": {"increase": 5, "description": "Gemeinsames Essen"}
        }

    def get_current_level(self):
        """Gibt aktuelles Mütterlichkeitslevel zurück"""
        return self.game_state.get("tsunade", {}).get("mutterlichkeit", 150)

    def get_behavior_category(self, level=None):
        """Bestimmt Verhaltenskategorie basierend auf Level"""
        if level is None:
            level = self.get_current_level()

        for behavior_key, behavior_data in self.behavior_levels.items():
            min_val, max_val = behavior_data["range"]
            if min_val <= level < max_val:
                return behavior_key

        # Fallback für Werte über 1000
        if level >= 1000:
            return "maximum_crazy_mom"
        return "fremder_misstrauisch"

    def get_behavior_description_for_level(self, level: int) -> Dict:
        """
        Gibt die detaillierte Verhaltensbeschreibung für das gegebene Maternal Level zurück.
        Nutzt get_behavior_category, um den passenden Schlüssel zu finden.
        """
        # 1. Bestimme den Schlüssel
        behavior_key = self.get_behavior_category(level)

        # 2. Gib die Daten für diesen Schlüssel zurück
        if behavior_key in self.behavior_levels:
            return self.behavior_levels[behavior_key]

        # 3. Spezieller Fallback für den Extrembereich > 1000 ("maximum_crazy_mom")
        if behavior_key == "maximum_crazy_mom":
            return {
                "range": (1000, 9999),
                "category": "PATHOLOGISCHE PANIK / KONTROLLVERLUST",
                "privat_verhalten": ["Völliger Zusammenbruch. Tsunade klammert sich schreiend an Sukuna."],
                "dialoge": {"privat": ["Nur noch hysterische Schreie und Flehen, Sukuna niemals zu verlassen."]}
            }

        # 4. Generischer Fallback (sollte durch get_behavior_category abgedeckt sein)
        return {
            "range": (0, 0),
            "category": "Unbekanntes Level",
            "privat_verhalten": ["Unbekanntes Verhalten, Standard-Protokoll anwenden."],
            "dialoge": {"privat": ["Entschuldigung, ich bin kurz abgelenkt. Was wolltest du?"]}
        }

    def get_level_category(self, level=None):
        """Kompatibilitätsmethode - gibt menschenlesbare Verhaltenskategorie zurück"""
        if level is None:
            level = self.get_current_level()

        behavior_category = self.get_behavior_category(level)
        return self.behavior_levels[behavior_category]["category"]

    def get_current_behavior_data(self):
        """Gibt vollständige Verhaltensdaten für aktuelles Level"""
        level = self.get_current_level()
        category = self.get_behavior_category(level)
        return self.behavior_levels[category]

    def get_random_dialog(self, context="privat"):
        """Gibt zufälligen Dialog für aktuelles Level zurück"""
        behavior_data = self.get_current_behavior_data()
        dialogs = behavior_data.get("dialoge", {}).get(context, [])
        if dialogs:
            return random.choice(dialogs)
        return "..."

    def get_behavior_description(self, context="privat"):
        """Gibt Verhaltensbeschreibung für aktuelles Level"""
        behavior_data = self.get_current_behavior_data()
        if context == "privat":
            behaviors = behavior_data.get("privat_verhalten", [])
        else:
            behaviors = behavior_data.get("oeffentlich_verhalten", [])
        return behaviors

    def increase_level(self, amount, reason=""):
        """Erhöht Mütterlichkeitslevel"""
        current = self.get_current_level()
        new_level = min(1000, current + amount)

        if "tsunade" not in self.game_state:
            self.game_state["tsunade"] = {}
        self.game_state["tsunade"]["mutterlichkeit"] = new_level

        # Tracking
        self.recent_triggers.append({
            "timestamp": datetime.now(),
            "reason": reason,
            "change": amount,
            "new_level": new_level
        })

        # Check für Kategorie-Wechsel
        old_category = self.get_behavior_category(current)
        new_category = self.get_behavior_category(new_level)

        if old_category != new_category:
            self.trigger_behavior_change(old_category, new_category, new_level)

        return new_level

    def decrease_level(self, amount, reason=""):
        """Verringert Mütterlichkeitslevel"""
        current = self.get_current_level()
        new_level = max(0, current - amount)

        if "tsunade" not in self.game_state:
            self.game_state["tsunade"] = {}
        self.game_state["tsunade"]["mutterlichkeit"] = new_level

        # Tracking
        self.recent_triggers.append({
            "timestamp": datetime.now(),
            "reason": reason,
            "change": -amount,
            "new_level": new_level
        })

        return new_level

    def trigger_behavior_change(self, old_category, new_category, new_level):
        """Wird aufgerufen wenn sich Verhaltenskategorie ändert"""
        old_data = self.behavior_levels[old_category]
        new_data = self.behavior_levels[new_category]

        message = f"🤱 VERHALTENSÄNDERUNG!\n\n"
        message += f"Von: {old_data['category']}\n"
        message += f"Zu: {new_data['category']}\n"
        message += f"Level: {new_level}/1000\n\n"

        # Neue Verhaltensweisen auflisten
        if new_level > self.last_level_check:
            message += "🔸 NEUE VERHALTENSWEISEN:\n"
            for behavior in new_data["privat_verhalten"][:3]:
                message += f"• {behavior}\n"
        else:
            message += "🔹 VERHALTENSWEISEN REDUZIERT:\n"
            message += "Tsunade wird weniger anhänglich."

        self.gui.add_message("MÜTTERLICHKEIT", message, self.gui.colors["relationship_accent"])
        self.last_level_check = new_level

    def process_trigger(self, trigger_name, custom_amount=None):
        """Verarbeitet einen Trigger"""
        if trigger_name not in self.triggers:
            return False

        trigger_data = self.triggers[trigger_name]
        old_level = self.get_current_level()

        if "increase" in trigger_data:
            amount = custom_amount if custom_amount else trigger_data["increase"]
            new_level = self.increase_level(amount, trigger_data["description"])

            # Chat-Nachricht anzeigen
            if self.gui and amount >= 5:  # Nur bei größeren Änderungen
                message = f"🤱 Tsunades Mütterlichkeit steigt! (+{amount})\n{trigger_data['description']}\nNeues Level: {new_level}/1000"
                self.gui.add_message("MÜTTERLICHKEIT", message, self.gui.colors["relationship_accent"])

        elif "decrease" in trigger_data:
            amount = custom_amount if custom_amount else trigger_data["decrease"]
            new_level = self.decrease_level(amount, trigger_data["description"])

            # Chat-Nachricht anzeigen
            if self.gui and amount >= 5:
                message = f"🤱 Tsunades Mütterlichkeit sinkt! (-{amount})\n{trigger_data['description']}\nNeues Level: {new_level}/1000"
                self.gui.add_message("MÜTTERLICHKEIT", message, self.gui.colors["warning"])
        else:
            return False

        return True

    def get_detailed_status(self):
        """Gibt detaillierten Status zurück"""
        level = self.get_current_level()
        behavior_data = self.get_current_behavior_data()

        status = f"🤱 TSUNADES MÜTTERLICHKEIT\n\n"
        status += f"📊 Level: {level}/1000\n"
        status += f"📂 Kategorie: {behavior_data['category']}\n\n"

        status += f"🏠 PRIVATES VERHALTEN:\n"
        for behavior in behavior_data["privat_verhalten"][:5]:
            status += f"• {behavior}\n"

        status += f"\n🏛️ ÖFFENTLICHES VERHALTEN:\n"
        for behavior in behavior_data["oeffentlich_verhalten"][:3]:
            status += f"• {behavior}\n"

        # Aktuelle Dialoge
        status += f"\n💬 TYPISCHE AUSSAGEN:\n"
        status += f"Privat: \"{self.get_random_dialog('privat')}\"\n"
        status += f"Öffentlich: \"{self.get_random_dialog('oeffentlich')}\"\n"

        return status

    def get_reaction_to_situation(self, situation_type):
        """Gibt Reaktion auf spezifische Situation zurück"""
        level = self.get_current_level()

        reactions = {
            "sukuna_verletzt": {
                (0, 100): "Professionelle medizinische Behandlung",
                (100, 200): "Besorgte Fürsorge und gründliche Behandlung",
                (200, 400): "Panik und überfürsorgliche Behandlung",
                (400, 650): "Hysterie und permanente Überwachung",
                (650, 1000): "Bei schwerer Verletzung lässt sie ihn tagelang zuhause"
            },
            "sukuna_mission": {
                (0, 100): "Normale Missions-Zuteilung",
                (100, 200): "Vorsichtige Auswahl sicherer Missionen",
                (200, 400): "Nur sehr sichere Missionen, häufige Kontrollen",
                (400, 650): "Verbietet gefährliche Missionen komplett",
                (650, 1000): "Gibt ihn nur Missionen, wenn er mehrmals darauf besteht"
            },
            "fremder_sukuna": {
                (0, 100): "Höfliche aber distanzierte Beobachtung",
                (100, 200): "Wachsame Beobachtung der Interaktion",
                (200, 400): "Misstrauische Überwachung und Intervention",
                (400, 650): "Aggressives Eingreifen und Fernhalten",
                (650, 1000): "Komplette Isolation von allen Fremden"
            }
        }

        if situation_type not in reactions:
            return "Unbekannte Situation"

        situation_reactions = reactions[situation_type]
        for level_range, reaction in situation_reactions.items():
            min_level, max_level = level_range
            if min_level <= level < max_level:
                return reaction

        return "Extreme Reaktion"

    def simulate_daily_progression(self):
        """Simuliert tägliche Entwicklung der Mütterlichkeit"""
        # Grundlegende tägliche Trigger
        daily_triggers = [
            ("morgen_wecken", 1),
            ("gemeinsame_mahlzeit", 2),
            ("abend_routine", 1),
            ("nacht_check", 1)
        ]

        total_change = 0
        for trigger_name, frequency in daily_triggers:
            for _ in range(frequency):
                if self.process_trigger(trigger_name):
                    if "increase" in self.triggers[trigger_name]:
                        total_change += self.triggers[trigger_name]["increase"]
                    else:
                        total_change -= self.triggers[trigger_name]["decrease"]

        return total_change

    def check_intervention_needed(self):
        """Prüft ob externe Intervention nötig ist"""
        level = self.get_current_level()

        if level > 800:
            return {
                "needed": True,
                "urgency": "KRITISCH",
                "recommendation": "Sofortige psychologische Hilfe nötig",
                "risk_level": "EXTREM HOCH"
            }
        elif level > 650:
            return {
                "needed": True,
                "urgency": "HOCH",
                "recommendation": "Professionelle Beratung empfohlen",
                "risk_level": "HOCH"
            }
        elif level > 500:
            return {
                "needed": True,
                "urgency": "MITTEL",
                "recommendation": "Gespräch mit Vertrauensperson",
                "risk_level": "MITTEL"
            }
        else:
            return {
                "needed": False,
                "urgency": "NIEDRIG",
                "recommendation": "Normales Verhalten",
                "risk_level": "NIEDRIG"
            }

# Hilfsfunktionen für Integration in TEST.py
def create_enhanced_maternal_system(game_state, gui):
    """Factory-Funktion für einfache Integration"""
    return EnhancedMaternalSystem(game_state, gui)

def get_maternal_behavior_description(level):
    """Standalone-Funktion für Verhaltensbeschreibung"""
    system = EnhancedMaternalSystem({}, None)
    category = system.get_behavior_category(level)
    return system.behavior_levels[category]["category"]