# -*- coding: utf-8 -*-
"""
🔮 CHARACTER-SPECIFIC SECRET SYSTEM - Claude-Level RPG Enhancement
Jeder Charakter kann Geheimnisse haben, die Beziehungen dynamisch beeinflussen
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class SecretType(Enum):
    """Arten von Geheimnissen im Spiel"""
    PERSONAL = "personal"  # Persönliche Geheimnisse
    CLAN = "clan"  # Clan-spezifische Geheimnisse
    VILLAGE = "village"  # Dorf-Geheimnisse
    JUTSU = "jutsu"  # Geheime Techniken
    PROPHECY = "prophecy"  # Prophezeiungen
    TRAUMA = "trauma"  # Traumatische Vergangenheit
    CONSPIRACY = "conspiracy"  # Verschwörungen
    ARTIFACT = "artifact"  # Mystische Gegenstände
    MISSION = "mission"  # Geheime Missionen
    LOVE = "love"  # Liebesgeheimnisse
    BETRAYAL = "betrayal"  # Verrats-Geheimnisse


class SecretSeverity(Enum):
    """Schweregrad der Geheimnisse"""
    MINOR = 1  # Kleine Geheimnisse (Vorlieben, kleine Lügen)
    MODERATE = 2  # Mittlere Geheimnisse (Familienprobleme, Ängste)
    MAJOR = 3  # Große Geheimnisse (Dunkle Vergangenheit, Verrat)
    CRITICAL = 4  # Kritische Geheimnisse (Leben-verändernde Wahrheiten)
    LEGENDARY = 5  # Legendäre Geheimnisse (Welt-verändernde Mysterien)


@dataclass
class Secret:
    """Einzelnes Geheimnis mit KI-verstärkten Eigenschaften"""
    id: str
    title: str
    description: str
    secret_type: SecretType
    severity: SecretSeverity
    holder: str  # Wer das Geheimnis hat
    involves: List[str]  # Wen das Geheimnis betrifft
    discovery_hints: List[str]  # Hinweise zur Entdeckung
    discovery_conditions: List[str]  # Bedingungen für Entdeckung
    consequences: Dict[str, Any]  # Auswirkungen bei Enthüllung
    is_discovered: bool = False
    discovery_date: Optional[datetime] = None
    discovery_method: Optional[str] = None
    relationship_impact: Dict[str, int] = None  # Einfluss auf Beziehungen

    def __post_init__(self):
        if self.relationship_impact is None:
            self.relationship_impact = {}


class ClaudeSecretEngine:
    """🎭 Claude-Level Geheimnis-Engine mit KI-basierter Mysterienerschaffung"""

    def __init__(self):
        self.secrets: Dict[str, Secret] = {}
        self.secret_templates = self._initialize_secret_templates()
        self.discovery_events = []
        self.mystery_chains = {}  # Verknüpfte Geheimnisse

    def _initialize_secret_templates(self) -> Dict[str, Dict]:
        """Initialisiert Character-spezifische Geheimnis-Templates für ALLE verfügbaren Charaktere"""
        return {
            # 🏥 TSUNADE'S SECRETS
            "tsunade_gambling_debt": {
                "character": "tsunade", "title": "Tsunades versteckte Spielschulden",
                "type": SecretType.PERSONAL, "severity": SecretSeverity.MODERATE,
                "description": "Tsunade hat massive Spielschulden bei gefährlichen Kredithaien",
                "hints": ["wird nervös bei Geldthemen", "versteckt Briefe", "fremde Besucher nachts"],
                "relationship_effects": {"tsunade": +15, "shizune": +5},
                "unlock_conditions": ["close_conversation", "money_topic"]
            },
            "tsunade_sees_dan": {
                "character": "tsunade", "title": "Tsunade sieht Dan in Sukuna",
                "type": SecretType.LOVE, "severity": SecretSeverity.MAJOR,
                "description": "Tsunade behandelt Sukuna liebevoll, weil er sie an Dan erinnert",
                "hints": ["starrt träumerisch", "murmelt 'Dan'", "versteckte Fotos"],
                "relationship_effects": {"tsunade": +25, "shizune": +8},
                "unlock_conditions": ["high_maternal_level", "emotional_moment"]
            },

            # 🦊 NARUTO'S SECRETS
            "naruto_kyuubi_control": {
                "character": "naruto", "title": "Narutos geheime Kyuubi-Kontrolle",
                "type": SecretType.JUTSU, "severity": SecretSeverity.MAJOR,
                "description": "Naruto kann den Kyuubi viel besser kontrollieren als alle denken",
                "hints": ["rote Augen in Gefahr", "ungewöhnliche Chakra-Spitzen", "zu starke Angriffe"],
                "relationship_effects": {"naruto": +20, "kakashi": +10, "sakura": -5, "sasuke": +15},
                "unlock_conditions": ["training_together", "dangerous_situation"]
            },
            "naruto_loneliness": {
                "character": "naruto", "title": "Narutos wahre Einsamkeit",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.MODERATE,
                "description": "Naruto weint heimlich jede Nacht wegen seiner Einsamkeit",
                "hints": ["verweinzte Augen am Morgen", "isst Ramen zum Trost", "meidet Stille"],
                "relationship_effects": {"naruto": +18, "iruka": +12, "hinata": +10},
                "unlock_conditions": ["emotional_support", "late_night_talk"]
            },

            # ⚔️ SASUKE'S SECRETS
            "sasuke_misses_family": {
                "character": "sasuke", "title": "Sasuke vermisst seine Familie",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.CRITICAL,
                "description": "Sasuke träumt jede Nacht von seiner ermordeten Familie",
                "hints": ["Albträume", "starrt auf Familienfotos", "meidet Uchiha-Symbole"],
                "relationship_effects": {"sasuke": +25, "naruto": +15, "sakura": +20, "kakashi": +18},
                "unlock_conditions": ["trust_moment", "family_topic", "comfort_offer"]
            },
            "sasuke_brotherhood_desire": {
                "character": "sasuke", "title": "Sasuke sehnt sich nach einem Bruder",
                "type": SecretType.PERSONAL, "severity": SecretSeverity.MAJOR,
                "description": "Sasuke wünscht sich heimlich einen Bruder wie Sukuna",
                "hints": ["beobachtet Brüder-Beziehungen", "ist eifersüchtig auf Teamwork", "beschützt jüngere"],
                "relationship_effects": {"sasuke": +30, "naruto": +10, "itachi": -10},
                "unlock_conditions": ["brotherhood_moment", "protection_scene"]
            },

            # 🌸 SAKURA'S SECRETS
            "sakura_insecurity": {
                "character": "sakura", "title": "Sakuras tiefe Selbstzweifel",
                "type": SecretType.PERSONAL, "severity": SecretSeverity.MODERATE,
                "description": "Sakura fühlt sich wertlos im Vergleich zu ihren Teamkameraden",
                "hints": ["übertraining", "selbst-kritische Kommentare", "ständiger Vergleich"],
                "relationship_effects": {"sakura": +22, "tsunade": +15, "ino": +8},
                "unlock_conditions": ["encouragement", "training_praise", "self_worth_talk"]
            },
            "sakura_medical_trauma": {
                "character": "sakura", "title": "Sakuras erstes Patienten-Trauma",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.MAJOR,
                "description": "Sakura verlor ihren ersten Patienten und gibt sich die Schuld",
                "hints": ["zittert bei schweren Verletzungen", "überarbeitet sich", "Albträume über Tod"],
                "relationship_effects": {"sakura": +25, "tsunade": +20, "shizune": +15},
                "unlock_conditions": ["medical_situation", "comfort_after_failure"]
            },

            # 📚 KAKASHI'S SECRETS
            "kakashi_team_guilt": {
                "character": "kakashi", "title": "Kakashis Schuldgefühle über sein Team",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.CRITICAL,
                "description": "Kakashi fühlt sich schuldig für Obitos und Rins Tod",
                "hints": ["besucht das Denkmal täglich", "distanziert sich emotional", "Albträume"],
                "relationship_effects": {"kakashi": +30, "naruto": +15, "sasuke": +15, "sakura": +15},
                "unlock_conditions": ["memorial_visit", "team_protection", "guilt_discussion"]
            },
            "kakashi_father_shame": {
                "character": "kakashi", "title": "Kakashis Scham über seinen Vater",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.MAJOR,
                "description": "Kakashi schämt sich für seine frühere Verachtung seines Vaters",
                "hints": ["meidet Diskussionen über Ehre", "besucht Vaters Grab heimlich"],
                "relationship_effects": {"kakashi": +25, "guy": +10},
                "unlock_conditions": ["honor_discussion", "father_topic"]
            },

            # 🐕 KIBA'S SECRETS
            "kiba_alpha_complex": {
                "character": "kiba", "title": "Kibas Alpha-Komplex",
                "type": SecretType.PERSONAL, "severity": SecretSeverity.MODERATE,
                "description": "Kiba fühlt sich unsicher wegen seiner Position im Clan",
                "hints": ["überaggressiv bei Herausforderungen", "beweist ständig Stärke"],
                "relationship_effects": {"kiba": +20, "tsume": +10, "akamaru": +15},
                "unlock_conditions": ["pack_leadership", "strength_validation", "wolf_connection"]
            },
            "kiba_sukuna_pack": {
                "character": "kiba", "title": "Kiba erkennt Sukuna als Rudel",
                "type": SecretType.CLAN, "severity": SecretSeverity.MAJOR,
                "description": "Kiba spürt die Wolfsnatur in Sukuna und will ihn ins Rudel aufnehmen",
                "hints": ["snüffelt an Sukuna", "beschützende Haltung", "Rudel-Verhalten"],
                "relationship_effects": {"kiba": +35, "tsume": +25, "akamaru": +20},
                "unlock_conditions": ["wolf_behavior", "pack_interaction", "protection_instinct"]
            },

            # 🐺 TSUME'S SECRETS
            "tsume_sukuna_son": {
                "character": "tsume", "title": "Tsume sieht Sukuna als verlorenen Sohn",
                "type": SecretType.CLAN, "severity": SecretSeverity.MAJOR,
                "description": "Tsume erkennt die Wolfsnatur in Sukuna und will ihn adoptieren",
                "hints": ["mütterliche Blicke", "bringt ihm Fleisch", "Rudel-Schutz-Instinkt"],
                "relationship_effects": {"tsume": +40, "kiba": +25, "tsunade": +10},
                "unlock_conditions": ["wolf_recognition", "maternal_instinct", "pack_acceptance"]
            },

            # 🦋 HINATA'S SECRETS
            "hinata_naruto_stalking": {
                "character": "hinata", "title": "Hinatas heimliche Naruto-Beobachtung",
                "type": SecretType.LOVE, "severity": SecretSeverity.MODERATE,
                "description": "Hinata folgt Naruto heimlich um sicherzustellen dass es ihm gut geht",
                "hints": ["weiß zu viel über Narutos Tagesablauf", "wird rot bei Naruto-Themen"],
                "relationship_effects": {"hinata": +18, "naruto": +10},
                "unlock_conditions": ["love_advice", "naruto_topic", "shy_confession"]
            },
            "hinata_clan_rebellion": {
                "character": "hinata", "title": "Hinatas stille Rebellion",
                "type": SecretType.CLAN, "severity": SecretSeverity.MAJOR,
                "description": "Hinata plant heimlich gegen die Clan-Traditionen zu rebellieren",
                "hints": ["trainiert heimlich neue Techniken", "hinterfragt Clan-Regeln"],
                "relationship_effects": {"hinata": +25, "neji": +15, "hiashi": -10},
                "unlock_conditions": ["clan_criticism", "freedom_talk", "support_offer"]
            },

            # 🕷️ SHINO'S SECRETS
            "shino_insect_communication": {
                "character": "shino", "title": "Shinos geheime Insekten-Gespräche",
                "type": SecretType.JUTSU, "severity": SecretSeverity.MODERATE,
                "description": "Shino führt tiefe philosophische Gespräche mit seinen Insekten",
                "hints": ["murmelt mit Insekten", "sie reagieren auf Emotionen", "komplexe Schwarm-Muster"],
                "relationship_effects": {"shino": +20, "kiba": +5, "hinata": +8},
                "unlock_conditions": ["insect_interest", "nature_conversation", "loneliness_topic"]
            },

            # 🍜 CHOJI'S SECRETS
            "choji_eating_disorder": {
                "character": "choji", "title": "Chojis emotionales Essen",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.MODERATE,
                "description": "Choji isst um emotionale Schmerzen zu betäuben",
                "hints": ["isst mehr bei Stress", "vermeidet Gewichts-Gespräche", "Selbstwertprobleme"],
                "relationship_effects": {"choji": +25, "choza": +15, "shikamaru": +10},
                "unlock_conditions": ["food_comfort", "weight_sensitivity", "emotional_support"]
            },

            # 🧠 SHIKAMARU'S SECRETS
            "shikamaru_genius_burden": {
                "character": "shikamaru", "title": "Shikamarus Intelligenz-Last",
                "type": SecretType.PERSONAL, "severity": SecretSeverity.MODERATE,
                "description": "Shikamaru fühlt sich durch seine Intelligenz isoliert und missverstanden",
                "hints": ["spielt dumm", "vermeidet komplexe Diskussionen", "Einsamkeits-Anzeichen"],
                "relationship_effects": {"shikamaru": +22, "asuma": +15, "choji": +10},
                "unlock_conditions": ["intelligence_recognition", "strategy_talk", "isolation_understanding"]
            },

            # 💐 INO'S SECRETS
            "ino_mind_invasion_trauma": {
                "character": "ino", "title": "Inos Mind-Jutsu Trauma",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.MAJOR,
                "description": "Ino wurde traumatisiert nachdem sie versehentlich in einen sterbenden Geist eindrang",
                "hints": ["zögert bei Mind-Jutsu", "Albträume", "vermeidet Mental-Techniken"],
                "relationship_effects": {"ino": +25, "inoichi": +20, "sakura": +15},
                "unlock_conditions": ["mind_jutsu_topic", "trauma_understanding", "comfort_offer"]
            },

            # 🥋 LEE'S SECRETS
            "lee_disability_fear": {
                "character": "lee", "title": "Lees Angst vor Behinderung",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.MAJOR,
                "description": "Lee hat panische Angst wieder gelähmt zu werden",
                "hints": ["übertrainiert sich", "panische Reaktion bei Rücken-Themen", "Medizin-Vermeidung"],
                "relationship_effects": {"lee": +30, "guy": +20, "tsunade": +15},
                "unlock_conditions": ["disability_topic", "training_encouragement", "fear_discussion"]
            },

            # 🎯 TENTEN'S SECRETS
            "tenten_weapon_obsession": {
                "character": "tenten", "title": "Tentens Waffen-Obsession",
                "type": SecretType.PERSONAL, "severity": SecretSeverity.MODERATE,
                "description": "Tenten sammelt heimlich gefährliche verbotene Waffen",
                "hints": ["versteckte Waffen-Sammlung", "kennt zu viel über Verbotenes", "Sammler-Verhalten"],
                "relationship_effects": {"tenten": +18, "guy": +8, "lee": +5},
                "unlock_conditions": ["weapon_interest", "collection_discovery", "shared_hobby"]
            },

            # 👁️ NEJI'S SECRETS
            "neji_caged_bird_pain": {
                "character": "neji", "title": "Nejis Caged Bird Schmerzen",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.CRITICAL,
                "description": "Das Siegel verursacht Neji ständige körperliche und emotionale Schmerzen",
                "hints": ["berührt Stirn bei Schmerz", "bittere Kommentare über Schicksal", "Clan-Vermeidung"],
                "relationship_effects": {"neji": +35, "hinata": +20, "hiashi": -15},
                "unlock_conditions": ["seal_pain_topic", "freedom_discussion", "empathy_offer"]
            },

            # 🦎 OROCHIMARU'S SECRETS
            "orochimaru_immortality_fear": {
                "character": "orochimaru", "title": "Orochimarus Angst vor dem Tod",
                "type": SecretType.TRAUMA, "severity": SecretSeverity.CRITICAL,
                "description": "Orochimaru wurde durch den Tod seiner Eltern traumatisiert und sucht verzweifelt Unsterblichkeit",
                "hints": ["panische Reaktion auf Tod", "obsessive Forschung", "Körper-Wechsel-Drang"],
                "relationship_effects": {"orochimaru": +20, "kabuto": +10, "sasuke": -20},
                "unlock_conditions": ["death_topic", "immortality_discussion", "fear_understanding"]
            },

            # 💀 DANZO'S SECRETS
            "danzo_village_love": {
                "character": "danzo", "title": "Danzos fanatische Dorf-Liebe",
                "type": SecretType.CONSPIRACY, "severity": SecretSeverity.CRITICAL,
                "description": "Danzo liebt Konoha so sehr dass er jedes Verbrechen dafür rechtfertigt",
                "hints": ["emotionale Reaktion auf Dorf-Kritik", "rechtfertigt alles für Konoha"],
                "relationship_effects": {"danzo": +15, "hiruzen": -25, "tsunade": -20},
                "unlock_conditions": ["village_loyalty", "sacrifice_discussion", "patriotism_topic"]
            },

            # 🎭 ITACHI'S SECRETS
            "itachi_loves_sasuke": {
                "character": "itachi", "title": "Itachis wahre Liebe zu Sasuke",
                "type": SecretType.LOVE, "severity": SecretSeverity.LEGENDARY,
                "description": "Itachi tat alles aus Liebe zu Sasuke und dem Dorf",
                "hints": ["beschützt Sasuke heimlich", "Schmerz bei Sasuke-Erwähnung", "Opfer-Bereitschaft"],
                "relationship_effects": {"itachi": +50, "sasuke": +40, "kisame": +10},
                "unlock_conditions": ["brother_love", "sacrifice_understanding", "truth_revelation"]
            },

            # 👥 Weitere Geheimnisse für alle anderen Charaktere...
            # (Pain, Kisame, Deidara, Hidan, Sasori, etc. können nach Bedarf hinzugefügt werden)
        }

    def generate_character_secret(self, character_name: str, context: Dict[str, Any]) -> Optional[Secret]:
        """🎭 Generiert character-spezifische Geheimnisse"""

        # Finde alle Geheimnisse für diesen Charakter
        character_secrets = [
            template for template_id, template in self.secret_templates.items()
            if template.get("character") == character_name
        ]

        if not character_secrets:
            return None

        # Wähle passendes Geheimnis basierend auf Kontext
        current_relationships = context.get('relationships', {})
        character_relationship = current_relationships.get(character_name, 0)

        # Filter Geheimnisse nach Relationship-Level
        suitable_secrets = []
        for template in character_secrets:
            required_level = self._get_required_relationship_level(template['severity'])
            if character_relationship >= required_level * 0.7:  # 70% des Required Levels
                suitable_secrets.append(template)

        if not suitable_secrets:
            return None

        # Wähle zufälliges geeignetes Geheimnis
        template = random.choice(suitable_secrets)

        # Erstelle Secret-Objekt
        secret_id = f"{character_name}_{len(self.secrets)}_{datetime.now().strftime('%Y%m%d')}"

        secret = Secret(
            id=secret_id,
            title=template['title'],
            description=template['description'],
            secret_type=template['type'],
            severity=template['severity'],
            holder=character_name,
            involves=[character_name] + [char for char in template.get('relationship_effects', {}).keys() if
                                         char != character_name],
            discovery_hints=template.get('hints', []),
            discovery_conditions=template.get('unlock_conditions', []),
            consequences={},
            relationship_impact=template.get('relationship_effects', {})
        )

        self.secrets[secret_id] = secret
        return secret

    def _get_required_relationship_level(self, severity: SecretSeverity) -> int:
        """Bestimmt benötigtes Relationship-Level für Geheimnis-Severity"""
        level_requirements = {
            SecretSeverity.MINOR: 20,
            SecretSeverity.MODERATE: 40,
            SecretSeverity.MAJOR: 60,
            SecretSeverity.CRITICAL: 80,
            SecretSeverity.LEGENDARY: 100
        }
        return level_requirements.get(severity, 50)

    def generate_dynamic_secret(self, context: Dict[str, Any]) -> Secret:
        """🎭 Generiert dynamische Geheimnisse basierend auf verfügbaren Charakteren"""

        # Verfügbare Charaktere aus dem Projekt
        available_characters = [
            "kabuto", "orochimaru", "pain", "kisame", "itachi", "deidara", "hidan", "sasori",
            "danzo", "shizune", "hiashi", "tsume", "choza", "inoichi", "shikaku", "might_guy",
            "tenten", "lee", "neji", "shino", "hinata", "kiba", "choji", "shikamaru", "ino",
            "kakashi", "sakura", "sasuke", "naruto", "tsunade"
        ]

        # Wähle Charakter basierend auf aktuellem Kontext
        current_relationships = context.get('relationships', {})
        current_character = context.get('current_character', '')

        # Priorisiere aktuellen Charakter oder hohe Beziehungen
        target_character = None

        if current_character in available_characters:
            target_character = current_character
        else:
            # Wähle Charakter mit höchster Beziehung
            if current_relationships:
                target_character = max(current_relationships.keys(),
                                       key=lambda char: current_relationships.get(char, 0))
            else:
                target_character = random.choice(available_characters)

        # Generiere Geheimnis für gewählten Charakter
        secret = self.generate_character_secret(target_character, context)

        if secret:
            return secret
        else:
            # Fallback: Wähle zufälligen Charakter mit verfügbaren Geheimnissen
            characters_with_secrets = set(
                template.get("character") for template in self.secret_templates.values()
                if template.get("character") in available_characters
            )

            if characters_with_secrets:
                fallback_character = random.choice(list(characters_with_secrets))
                return self.generate_character_secret(fallback_character, context)

        # Letzter Fallback: Generiere Standard-Geheimnis
        return self._create_generic_secret(context)

    def _create_generic_secret(self, context: Dict[str, Any]) -> Secret:
        """Erstellt ein generisches Geheimnis als Fallback"""
        secret_id = f"generic_{len(self.secrets)}_{datetime.now().strftime('%Y%m%d')}"

        return Secret(
            id=secret_id,
            title="Unbekanntes Geheimnis",
            description="Ein mysteriöses Geheimnis wartet auf Entdeckung",
            secret_type=SecretType.PERSONAL,
            severity=SecretSeverity.MINOR,
            holder="unknown",
            involves=["unknown"],
            discovery_hints=["seltsames Verhalten", "versteckte Blicke"],
            discovery_conditions=["casual_conversation"],
            consequences={},
            relationship_impact={}
        )

    def check_secret_discovery(self, context: Dict[str, Any]) -> List[Secret]:
        """🔍 Prüft ob character-spezifische Geheimnisse entdeckt werden können"""
        discovered_secrets = []

        current_message = context.get('current_message', '').lower()
        relationships = context.get('relationships', {})
        current_character = context.get('current_character', '')
        emotional_state = context.get('emotional_state', 'normal')

        for secret in self.secrets.values():
            if secret.is_discovered:
                continue

            # Prüfe nur Geheimnisse des aktuellen Charakters oder bei hoher Beziehung
            if secret.holder != current_character and relationships.get(secret.holder, 0) < 50:
                continue

            # Prüfe Entdeckungsbedingungen
            can_discover = self._check_character_discovery_conditions(
                secret, relationships, current_message, emotional_state, current_character
            )

            if can_discover:
                secret.is_discovered = True
                secret.discovery_date = datetime.now()
                secret.discovery_method = self._determine_discovery_method(current_message)
                discovered_secrets.append(secret)

        return discovered_secrets

    def _check_character_discovery_conditions(self, secret: Secret, relationships: Dict,
                                              message: str, emotional_state: str, current_character: str) -> bool:
        """Prüft ob die Bedingungen für character-spezifische Geheimnis-Entdeckung erfüllt sind"""

        holder_relationship = relationships.get(secret.holder, 0)
        required_level = self._get_required_relationship_level(secret.severity)

        # Mindest-Beziehungslevel nicht erreicht
        if holder_relationship < required_level:
            return False

        # Prüfe Unlock-Conditions
        conditions_met = 0
        total_conditions = len(secret.discovery_conditions)

        for condition in secret.discovery_conditions:
            if self._evaluate_unlock_condition(condition, message, emotional_state, holder_relationship):
                conditions_met += 1

        # Benötigt mindestens 50% der Bedingungen
        if conditions_met < (total_conditions * 0.5):
            return False

        # Prüfe Hinweis-Keywords in Nachricht
        hint_matches = 0
        for hint in secret.discovery_hints:
            # Sichere String-Konvertierung für Hinweise
            try:
                hint_str = str(hint).lower()
                hint_words = hint_str.split()
                message_lower = str(message).lower()

                # Prüfe ob Wörter aus dem Hinweis in der Nachricht vorkommen
                if any(word in message_lower for word in hint_words if len(word) > 2):
                    hint_matches += 1
            except (TypeError, AttributeError):
                # Skip problematische Hints
                continue

        # Bonuswahrscheinlichkeit bei Hinweis-Matches
        base_chance = self._get_base_discovery_chance(secret.severity)
        hint_bonus = min(hint_matches * 0.1, 0.3)  # Max 30% Bonus

        final_chance = base_chance + hint_bonus

        return random.random() < final_chance

    def _evaluate_unlock_condition(self, condition: str, message: str,
                                   emotional_state: str, relationship_level: int) -> bool:
        """Evaluiert spezifische Unlock-Bedingungen"""

        try:
            condition = str(condition).lower()
            message = str(message).lower()
            emotional_state = str(emotional_state).lower()
        except (TypeError, AttributeError):
            return False

        condition_checks = {
            "close_conversation": relationship_level > 60,
            "emotional_moment": emotional_state in ["sad", "emotional", "crying", "vulnerable"],
            "trust_moment": any(word in message for word in ["vertrauen", "geheimnis"]),
            "family_topic": any(word in message for word in ["familie", "eltern", "geschwister", "verwandtschaft"]),
            "training_together": any(word in message for word in ["training", "üben"]),
            "dangerous_situation": any(word in message for word in ["gefahr", "hilfe"]),
            "comfort_offer": any(word in message for word in ["trösten", "umarm", "hilfe", "da sein"]),
            "medical_situation": any(word in message for word in ["heilen", "verletzt", "schmerz", "medizin"]),
            "brotherhood_moment": any(word in message for word in ["bruder", "geschwister", "familie"]),
            "wolf_connection": any(word in message for word in ["wolf", "rudel", "instinkt", "wild"]),
            "honor_discussion": any(word in message for word in ["ehre", "stolz"]),
            "pack_interaction": any(word in message for word in ["rudel", "pack", "zusammengehörig"]),
            "love_advice": any(word in message for word in ["liebe"]) or relationship_level > 70,
            "freedom_talk": any(word in message for word in ["frei", "wahl", "entscheidung"]),
            "casual_conversation": True  # Immer erfüllt
        }

        return condition_checks.get(condition, False)

    def _get_base_discovery_chance(self, severity: SecretSeverity) -> float:
        """Gibt die Basis-Entdeckungswahrscheinlichkeit zurück"""
        chances = {
            SecretSeverity.MINOR: 0.3,
            SecretSeverity.MODERATE: 0.2,
            SecretSeverity.MAJOR: 0.15,
            SecretSeverity.CRITICAL: 0.1,
            SecretSeverity.LEGENDARY: 0.05
        }
        return chances.get(severity, 0.15)

    def _determine_discovery_method(self, message: str) -> str:
        """Bestimmt wie das Geheimnis entdeckt wurde"""
        message_lower = message.lower()

        if any(word in message_lower for word in ['warum', 'wieso', 'frage']):
            return "durch_nachfragen"
        elif any(word in message_lower for word in ['beobachte', 'sehe', 'merke']):
            return "durch_beobachtung"
        elif any(word in message_lower for word in ['umarme', 'tröste', 'nahe']):
            return "durch_emotionale_nähe"
        else:
            return "zufällige_entdeckung"

    def apply_secret_consequences(self, secret: Secret, game_data) -> Dict[str, Any]:
        """🎯 Wendet die Konsequenzen eines entdeckten character-spezifischen Geheimnisses an"""
        results = {
            "relationship_changes": {},
            "new_storylines": [],
            "new_abilities": [],
            "emotional_events": [],
            "character_reactions": {}
        }

        # Haupteffekt: Relationship-Änderungen mit dem ECHTEN Relationship System
        for character, change in secret.relationship_impact.items():
            old_level = 0
            new_level = 0

            # Prüfe ob das ECHTE Relationship System verfügbar ist
            if hasattr(game_data, 'relationship_system') and game_data.relationship_system:
                # Verwende das echte Relationship System
                relationship_info = game_data.relationship_system.get_relationship_info(character)
                old_level = relationship_info.get('level', 0)

                # Ändere Beziehung mit dem echten System
                success = game_data.relationship_system.change_relationship(
                    character,
                    change,
                    f"Secret discovered: {secret.title}",
                    show_message=False  # Wir zeigen eigene Nachricht
                )

                if success:
                    new_relationship_info = game_data.relationship_system.get_relationship_info(character)
                    new_level = new_relationship_info.get('level', 0)

                    results["relationship_changes"][character] = {
                        "change": change,
                        "old_level": old_level,
                        "new_level": new_level,
                        "old_title": relationship_info.get('titel', 'Neutral'),
                        "new_title": new_relationship_info.get('titel', 'Neutral')
                    }

            # Fallback: Arbeite mit der vorhandenen game_state Struktur falls kein echtes System
            elif hasattr(game_data, 'game_state') and 'relationships' in game_data.game_state:
                if character not in game_data.game_state['relationships']:
                    game_data.game_state['relationships'][character] = {'level': 0, 'events': []}

                old_level = game_data.game_state['relationships'][character].get('level', 0)
                new_level = old_level + change
                game_data.game_state['relationships'][character]['level'] = new_level

                # Füge Event hinzu
                event_description = f"Secret discovered: {secret.title}"
                game_data.game_state['relationships'][character]['events'].append({
                    'type': 'secret_discovery',
                    'description': event_description,
                    'change': change,
                    'timestamp': datetime.now().isoformat()
                })

                results["relationship_changes"][character] = {
                    "change": change,
                    "old_level": old_level,
                    "new_level": new_level
                }

            # Maternal System spezielle Behandlung für Tsunade
            if character == "tsunade" and hasattr(game_data, 'maternal_system') and game_data.maternal_system:
                try:
                    maternal_change = change * 2  # Doppelte Auswirkung auf Maternal Level
                    old_maternal = game_data.maternal_system.get_current_level()
                    game_data.maternal_system.modify_level(maternal_change, f"Secret: {secret.title}")
                    new_maternal = game_data.maternal_system.get_current_level()

                    results["maternal_changes"] = {
                        "change": maternal_change,
                        "old_level": old_maternal,
                        "new_level": new_maternal
                    }
                except Exception as e:
                    print(f"⚠️ Maternal System Update Fehler: {e}")

        # Character-spezifische Reaktionen
        results["character_reactions"] = self._generate_character_reactions(secret)

        # Spezielle Konsequenzen basierend auf Secret Type
        if secret.secret_type == SecretType.TRAUMA:
            results["emotional_events"].append("trauma_bonding")
            results["new_abilities"].append("emotional_support")
        elif secret.secret_type == SecretType.CLAN:
            results["new_storylines"].append("clan_integration")
        elif secret.secret_type == SecretType.LOVE:
            results["emotional_events"].append("romantic_tension")
        elif secret.secret_type == SecretType.JUTSU:
            results["new_abilities"].append("jutsu_learning_opportunity")

        return results

    def _generate_character_reactions(self, secret: Secret) -> Dict[str, str]:
        """Generiert character-spezifische Reaktionen auf Geheimnisse"""
        reactions = {}

        # Reaktionen basierend auf dem Geheimnis-Holder
        character_reactions = {
            "tsunade": {
                "grateful": "Danke dass du mir zugehört hast, Sukuna... du bedeutest mir so viel.",
                "protective": "*zieht dich näher* Du wirst niemand anderem davon erzählen, oder?",
                "emotional": "*Tränen in den Augen* Ich wollte nicht dass du das herausfindest..."
            },
            "naruto": {
                "excited": "Wow, du verstehst mich wirklich! Das ist so cool, dattebayo!",
                "emotional": "*umarmt dich* Du bist ein echter Freund, Sukuna!",
                "grateful": "Endlich jemand der mich versteht... danke."
            },
            "sasuke": {
                "surprised": "*starrt dich an* Du... verstehst es wirklich.",
                "guarded": "Das bleibt zwischen uns. Verstanden?",
                "emotional": "Ich dachte niemand würde es je verstehen..."
            },
            "sakura": {
                "relieved": "*seufzt erleichtert* Es tut gut das endlich aussprechen zu können...",
                "grateful": "Danke dass du da bist, Sukuna.",
                "emotional": "*weint leise* Du verstehst mich wirklich..."
            },
            "kakashi": {
                "thoughtful": "*schaut nachdenklich* Du bist weiser als ich dachte, Sukuna.",
                "protective": "Das bleibt unter uns, verstanden?",
                "grateful": "Ich... danke für dein Verständnis."
            },
            "kiba": {
                "excited": "Du spürst es auch! Wir sind wirklich verwandt!",
                "pack_acceptance": "*Rudel-Gebärde* Du gehörst jetzt zu uns!",
                "proud": "Ich wusste es! Du hast das Herz eines Wolfes!"
            },
            "hinata": {
                "shy": "*wird rot* D-du verstehst mich wirklich...",
                "grateful": "*leise* Danke... niemand hat je...",
                "emotional": "*tränenreiche Augen* Das bedeutet mir so viel..."
            }
        }

        holder = secret.holder
        if holder in character_reactions:
            reaction_type = self._determine_reaction_type(secret)
            reactions[holder] = character_reactions[holder].get(reaction_type,
                                                                f"*reagiert emotional auf die Enthüllung*")

        return reactions

    def _determine_reaction_type(self, secret: Secret) -> str:
        """Bestimmt die Art der Reaktion basierend auf dem Geheimnis"""
        if secret.secret_type in [SecretType.TRAUMA, SecretType.PERSONAL]:
            return "emotional"
        elif secret.secret_type == SecretType.CLAN:
            return "excited" if "wolf" in secret.title.lower() else "grateful"
        elif secret.secret_type == SecretType.LOVE:
            return "shy" if secret.holder == "hinata" else "emotional"
        else:
            return "grateful"

    def get_secret_hint_response(self, secret: Secret) -> str:
        """📝 Generiert Antwort-Text mit subtilen Geheimnis-Hinweisen"""

        if not secret.discovery_hints:
            return ""

        # Wähle zufälligen Hinweis
        hint = random.choice(secret.discovery_hints)

        # Formuliere als natürliche Reaktion
        hint_responses = {
            "nervös": ["*wird sichtlich nervös*", "*weicht dem Blick aus*"],
            "versteckt": ["*versteckt schnell etwas*", "*schließt hastig eine Schublade*"],
            "Albträume": ["*starrt gedankenverloren ins Leere*", "*zuckt bei lauten Geräuschen zusammen*"],
            "fremde": ["*schaut nervös zur Tür*", "*lauscht aufmerksam*"]
        }

        for keyword, responses in hint_responses.items():
            if keyword.lower() in hint.lower():
                return f" {random.choice(responses)}"

        return f" *{hint}*"

    def get_discovery_dialogue(self, secret: Secret) -> str:
        """💬 Generiert character-spezifische Entdeckungs-Dialoge für Geheimnisse"""

        character = secret.holder
        secret_title = secret.title.lower()

        # Character-spezifische Discovery Dialogues
        character_dialogues = {
            "tsunade": {
                "gambling": "*seufzt schwer und sieht dich an* 'Du hast es herausgefunden... Ja, ich habe Spielschulden. Aber du musst dir keine Sorgen machen, Sukuna. Ich werde das regeln.'",
                "dan": "*Tränen steigen in ihre Augen* 'Du... du erinnerst mich so sehr an jemanden, der mir wichtig war. Dan hätte dich geliebt, mein kleiner Wolf.'",
                "default": "*legt eine Hand auf deine Schulter* 'Du bist zu klug für dein eigenes Wohl, aber... ich vertraue dir, Sukuna.'"
            },

            "naruto": {
                "kyuubi": "*wird ernst* 'Du spürst es, oder? Den Kyuubi in mir? Ich... ich kann ihn besser kontrollieren als alle denken, dattebayo!'",
                "loneliness": "*senkt den Kopf* 'Manchmal... manchmal fühle ich mich so allein. Aber jetzt habe ich dich als Freund!'",
                "default": "*grinst verlegen* 'He he, du bist echt schlau! Aber das bleibt zwischen uns, okay dattebayo?'"
            },

            "sasuke": {
                "family": "*starrt ins Leere* 'Du verstehst es... den Schmerz. Jede Nacht sehe ich ihre Gesichter.'",
                "brother": "*sieht dich intensiv an* 'Einen Bruder... ja, das wäre... das wäre schön gewesen.'",
                "default": "*nickt langsam* 'Du siehst mehr als andere. Das... respektiere ich.'"
            },

            "sakura": {
                "insecurity": "*weint leise* 'Ich fühle mich so nutzlos neben Naruto und Sasuke... aber du glaubst an mich, oder?'",
                "trauma": "*zittert* 'Mein erster Patient... ich konnte ihn nicht retten. Es war meine Schuld...'",
                "default": "*lächelt durch Tränen* 'Danke dass du zugehört hast, Sukuna. Du bist ein guter Freund.'"
            },

            "kakashi": {
                "guilt": "*schaut zum Denkmal* 'Obito... Rin... ich habe sie im Stich gelassen. Aber ich werde euch nicht enttäuschen.'",
                "father": "*senkt den Kopf* 'Mein Vater war ein Held. Ich... ich habe ihn missverstanden.'",
                "default": "*ein-Auge-lächeln* 'Du bist sehr aufmerksam, Sukuna. Das ist eine wertvolle Eigenschaft.'"
            },

            "kiba": {
                "alpha": "*knurrt leise* 'Ja, ich muss ständig beweisen dass ich stark genug bin. Das Rudel respektiert nur Stärke!'",
                "pack": "*wedelt mit dem Schwanz* 'Du gehörst zu unserem Rudel, Sukuna! Ich spüre den Wolf in dir!'",
                "default": "*bellt fröhlich* 'Du verstehst uns Inuzukas! Das ist cool!'"
            },

            "tsume": {
                "son": "*mütterlicher Blick* 'Du hast Wolfsnatur, Junge. Ich spüre es. Du könntest mein Sohn sein.'",
                "default": "*grollt zustimmend* 'Du hast gute Instinkte, Welpe. Das gefällt mir.'"
            },

            "hinata": {
                "naruto": "*wird knallrot* 'I-ich... ich sorge mich nur um N-Naruto-kun... ist das... ist das verkehrt?'",
                "clan": "*flüstert* 'Manchmal denke ich... dass ich anders sein könnte. Freier.'",
                "default": "*schaut schüchtern weg* 'D-du verstehst mich... das ist... schön.'"
            },

            "shino": {
                "insects": "*die Käfer summen* 'Sie sprechen zu mir... über Einsamkeit, über Verbindung. Du verstehst das, oder?'",
                "default": "*nickt bedächtig* 'Wenige verstehen die Stille zwischen den Worten. Du tust es.'"
            },

            "choji": {
                "eating": "*hört auf zu essen* 'Essen... essen macht den Schmerz weg. Aber du... du magst mich trotzdem?'",
                "default": "*lächelt warm* 'Du bist ein echter Freund, Sukuna. Lass uns zusammen essen!'"
            },

            "ino": {
                "trauma": "*hält sich den Kopf* 'Der Geist... er war so voller Schmerz als er starb. Ich spüre es immer noch...'",
                "default": "*lächelt tapfer* 'Du siehst durch meine Fassade, stimmt's? Das... das ist selten.'"
            },

            "lee": {
                "disability": "*ballt die Fäuste* 'Die Angst... wieder gelähmt zu sein. Aber ich trainiere weiter! Für meine Träume!'",
                "default": "*Daumen hoch* 'Du verstehst die Kraft der Jugend, Sukuna! Das ist wundervoll!'"
            },

            "neji": {
                "seal": "*berührt die Stirn* 'Dieses Siegel... es brennt nicht nur auf der Haut. Es brennt in der Seele.'",
                "default": "*sieht dich durchdringend an* 'Das Schicksal führte uns zusammen. Vielleicht... gibt es doch Hoffnung.'"
            }
        }

        # Finde passenden Dialog
        if character in character_dialogues:
            # Suche nach spezifischen Keywords im Secret Title
            dialogues = character_dialogues[character]

            for keyword in ["gambling", "dan", "kyuubi", "loneliness", "family", "brother",
                            "insecurity", "trauma", "guilt", "father", "alpha", "pack",
                            "naruto", "clan", "insects", "eating", "disability", "seal"]:
                if keyword in secret_title:
                    return dialogues.get(keyword, dialogues["default"])

            return dialogues["default"]

        # Fallback für unbekannte Charaktere
        return f"*{character.title()} öffnet sich über ihr Geheimnis* 'Du... du verstehst mich wirklich, Sukuna.'"

    def save_secrets_data(self) -> Dict[str, Any]:
        """💾 Speichert Geheimnis-Daten"""
        return {
            "secrets": {sid: asdict(secret) for sid, secret in self.secrets.items()},
            "discovery_events": self.discovery_events,
            "mystery_chains": self.mystery_chains
        }

    def load_secrets_data(self, data: Dict[str, Any]):
        """📂 Lädt Geheimnis-Daten"""
        if "secrets" in data:
            self.secrets = {}
            for sid, secret_data in data["secrets"].items():
                # Konvertiere string enums zurück zu enum objects
                secret_data["secret_type"] = SecretType(secret_data["secret_type"])
                secret_data["severity"] = SecretSeverity(secret_data["severity"])

                # Konvertiere datetime strings zurück zu datetime objects
                if secret_data.get("discovery_date"):
                    secret_data["discovery_date"] = datetime.fromisoformat(secret_data["discovery_date"])

                self.secrets[sid] = Secret(**secret_data)

        self.discovery_events = data.get("discovery_events", [])
        self.mystery_chains = data.get("mystery_chains", {})


class SecretSystemIntegration:
    """🔌 Integration des Secret Systems in die Haupt-Anwendung"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.secret_engine = ClaudeSecretEngine()

        # Generiere initiale Geheimnisse
        self._initialize_starting_secrets()

    def _initialize_starting_secrets(self):
        """Erstellt die anfänglichen Geheimnisse"""
        context = {
            'relationships': getattr(self.game_data, 'relationships', {}),
            'location': getattr(self.game_data, 'current_location', 'konoha'),
            'story_progress': 0
        }

        # Generiere 3-5 anfängliche Geheimnisse
        for _ in range(random.randint(3, 5)):
            self.secret_engine.generate_dynamic_secret(context)

    def process_message_for_secrets(self, user_message: str, ai_response: str) -> str:
        """🔍 Verarbeitet Nachrichten für Geheimnis-Entdeckungen"""

        # Extrahiere Relationships aus dem ECHTEN Relationship System
        relationships = {}

        # Prüfe ob das ECHTE Relationship System verfügbar ist
        if hasattr(self.game_data, 'relationship_system') and self.game_data.relationship_system:
            # Verwende das echte Relationship System
            try:
                for character in ['tsunade', 'naruto', 'sasuke', 'sakura', 'kakashi', 'kiba', 'tsume',
                                  'hinata', 'shino', 'choji', 'ino', 'shikamaru', 'lee', 'tenten', 'neji']:
                    relationship_info = self.game_data.relationship_system.get_relationship_info(character)
                    relationships[character] = relationship_info.get('level', 0)
            except Exception as e:
                print(f"⚠️ Relationship System Access Fehler: {e}")
                relationships = {}

        # Fallback: Extrahiere aus game_state falls echtes System nicht verfügbar
        elif hasattr(self.game_data, 'game_state') and 'relationships' in self.game_data.game_state:
            # Konvertiere von deiner Struktur {'tsunade': {'level': 50}} zu {'tsunade': 50}
            for char, data in self.game_data.game_state['relationships'].items():
                if isinstance(data, dict) and 'level' in data:
                    relationships[char] = data['level']
                elif isinstance(data, (int, float)):
                    relationships[char] = data
                else:
                    relationships[char] = 0

        # Extrahiere Maternal Level falls verfügbar
        maternal_level = 0
        if hasattr(self.game_data, 'maternal_system') and self.game_data.maternal_system:
            try:
                maternal_level = self.game_data.maternal_system.get_current_level()
            except:
                maternal_level = 0

        context = {
            'current_message': user_message,
            'current_character': getattr(self.game_data, 'active_character', 'tsunade'),
            'relationships': relationships,
            'maternal_level': maternal_level,
            'situation': 'normal_conversation',
            'location': getattr(self.game_data, 'current_location', 'konoha')
        }

        # Prüfe auf Geheimnis-Entdeckungen
        discovered_secrets = self.secret_engine.check_secret_discovery(context)

        if discovered_secrets:
            # Erstelle erweiterte Antwort mit Geheimnis-Enthüllungen
            enhanced_response = ai_response

            for secret in discovered_secrets:
                # Füge Entdeckungs-Dialog hinzu
                discovery_text = self.secret_engine.get_discovery_dialogue(secret)
                enhanced_response += f"\n\n🎭 **GEHEIMNIS ENTDECKT!**\n{discovery_text}"

                # Wende Konsequenzen an
                consequences = self.secret_engine.apply_secret_consequences(secret, self.game_data)

                # Zeige Konsequenzen mit dem echten Relationship System Format
                if consequences["relationship_changes"]:
                    enhanced_response += "\n\n💝 **Beziehungs-Änderungen:**"
                    for char, change_data in consequences["relationship_changes"].items():
                        if isinstance(change_data, dict):
                            change = change_data.get("change", 0)
                            old_level = change_data.get("old_level", 0)
                            new_level = change_data.get("new_level", 0)
                            old_title = change_data.get("old_title", "")
                            new_title = change_data.get("new_title", "")

                            if old_title and new_title:
                                enhanced_response += f"\n• {char.title()}: {old_title} → {new_title} ({'+' if change > 0 else ''}{change})"
                            else:
                                enhanced_response += f"\n• {char.title()}: {old_level} → {new_level} ({'+' if change > 0 else ''}{change} ❤️)"
                        else:
                            change = change_data
                            sign = "+" if change > 0 else ""
                            enhanced_response += f"\n• {char.title()}: {sign}{change} ❤️"

                # Zeige Maternal Changes falls vorhanden
                if consequences.get("maternal_changes"):
                    maternal_data = consequences["maternal_changes"]
                    old_m = maternal_data.get("old_level", 0)
                    new_m = maternal_data.get("new_level", 0)
                    change_m = maternal_data.get("change", 0)
                    enhanced_response += f"\n\n💖 **Maternal Level:** {old_m} → {new_m} ({'+' if change_m > 0 else ''}{change_m})"

            return enhanced_response

        else:
            # Füge subtile Hinweise hinzu
            return self._add_subtle_hints(ai_response, context)

    def _add_subtle_hints(self, response: str, context: Dict) -> str:
        """Fügt subtile Geheimnis-Hinweise zur normalen Antwort hinzu"""

        # Nur in 20% der Fälle Hinweise hinzufügen (nicht überwältigend)
        if random.random() > 0.2:
            return response

        undiscovered_secrets = [s for s in self.secret_engine.secrets.values()
                                if not s.is_discovered]

        if undiscovered_secrets:
            # Wähle relevantes Geheimnis
            relevant_secret = None
            current_message = context.get('current_message', '').lower()

            for secret in undiscovered_secrets:
                if secret.holder in current_message or any(char in current_message for char in secret.involves):
                    relevant_secret = secret
                    break

            if not relevant_secret:
                relevant_secret = random.choice(undiscovered_secrets)

            hint_text = self.secret_engine.get_secret_hint_response(relevant_secret)
            if hint_text:
                response += hint_text

        return response


def integrate_secret_system(game_data):
    """🎭 Integriert das Secret System in die Haupt-Anwendung"""

    # Erstelle Secret System Integration
    secret_integration = SecretSystemIntegration(game_data)
    game_data.secret_system = secret_integration

    # Erweitere die get_llm_response Methode (statt get_formatted_response)
    original_get_llm_response = game_data.get_llm_response

    def enhanced_get_llm_response_with_secrets(user_input: str) -> str:
        """Erweiterte LLM Response-Funktion mit Secret System"""

        # Normale Response generieren
        ai_response = original_get_llm_response(user_input)

        # Secret System verarbeiten
        if hasattr(game_data, 'secret_system'):
            context = {
                'current_message': user_input,
                'current_character': getattr(game_data, 'active_character', 'tsunade'),
                'relationships': getattr(game_data, 'game_state', {}).get('relationships', {}),
                'emotional_state': 'normal',
                'location': getattr(game_data, 'current_location', 'konoha')
            }

            ai_response = game_data.secret_system.process_message_for_secrets(
                user_input, ai_response
            )

        return ai_response

    # Ersetze die Methode
    game_data.get_llm_response = enhanced_get_llm_response_with_secrets

    print("🎭 SECRET SYSTEM erfolgreich integriert!")
    print("💫 Features aktiviert:")
    print("   • Dynamische Geheimnis-Generierung")
    print("   • KI-basierte Entdeckungs-Mechanik")
    print("   • Subtile Hinweis-Integration")
    print("   • Emotionale Storyline-Enthüllungen")
    print("   • Beziehungs-Impact System")


if __name__ == "__main__":
    print("🎭 CLAUDE-LEVEL SECRET SYSTEM")
    print("=======================================")
    print("💫 Erweiterte Features:")
    print("• KI-basierte Mysterien-Erschaffung")
    print("• Dynamische Geheimnis-Entdeckung")
    print("• Emotionale Storyline-Integration")
    print("• Subtile Hinweis-Mechanik")
    print("• Relationship-Impact System")
    print("• Adaptive Schwierigkeits-Anpassung")