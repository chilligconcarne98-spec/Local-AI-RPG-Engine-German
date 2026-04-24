# -*- coding: utf-8 -*-
"""
🔮 ENHANCED PREDICTIVE INTELLIGENCE - Alle 32+ Characters
Arbeitet mit separatem Time System für perfekte Vorhersagen
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class PlayerNeed(Enum):
    """Erweiterte Player-Bedürfnisse"""
    COMFORT = "comfort"
    FOOD = "food"
    REST = "rest"
    SOCIAL = "social"
    SOLITUDE = "solitude"
    VALIDATION = "validation"
    PROTECTION = "protection"
    STIMULATION = "stimulation"
    MEDICAL = "medical"
    EMOTIONAL_RELEASE = "emotional_release"
    WARMTH = "warmth"
    SAFETY = "safety"
    PLAY = "play"
    LEARNING = "learning"


class PredictionConfidence(Enum):
    """Sicherheit der Vorhersage"""
    CERTAIN = 0.9
    LIKELY = 0.7
    POSSIBLE = 0.5
    UNCERTAIN = 0.3


@dataclass
class CharacterPersonality:
    """Charakter-spezifische Persönlichkeit für Predictions"""
    empathy_level: float  # 0-1.0 Wie empathisch
    protective_instinct: float  # 0-1.0 Wie beschützend
    nurturing_tendency: float  # 0-1.0 Wie fürsorglich
    social_sensitivity: float  # 0-1.0 Soziale Aufmerksamkeit

    # Spezielle Sensitivitäten
    physical_need_detection: float  # Hunger, Müdigkeit
    emotional_need_detection: float  # Trauer, Angst
    comfort_offering_style: str  # "maternal", "friendly", "protective", "casual"

    # Aktivitäts-Präferenzen
    preferred_activities: List[str]
    comfort_methods: List[str]


@dataclass
class PredictedNeed:
    """Vorhergesagtes Bedürfnis"""
    need_type: PlayerNeed
    confidence: PredictionConfidence
    reasoning: str
    suggested_actions: List[str]
    urgency_level: int  # 1-5
    character_specific: bool


class EnhancedPredictiveIntelligence:
    """🔮 Enhanced Predictive System für ALLE Characters"""

    def __init__(self, game_data):
        self.game_data = game_data

        # Character Database laden aus characters.py
        self.all_characters = self._load_all_characters()

        # Character Personalities für Predictions
        self.character_personalities = self._initialize_character_personalities()

        # Prediction History
        self.prediction_history = []
        self.learned_patterns = {}

    def _load_all_characters(self) -> List[str]:
        """Lädt alle verfügbaren Charaktere"""
        characters = [
            # Main Characters
            "sukuna", "tsunade",

            # Team 7
            "naruto", "sasuke", "sakura", "kakashi",

            # Rookie 9
            "ino", "shikamaru", "choji", "kiba", "hinata", "shino", "neji", "lee", "tenten",

            # Adults
            "guy", "kurenai", "asuma", "anko", "iruka", "inoichi", "choza", "tsume",
            "hiashi", "shizune",

            # Selected Villains (nur die die nett zu Sukuna sein können)
            "itachi"  # Hat Sukuna geholfen
        ]

        print(f"🎭 Loaded {len(characters)} characters for Predictive Intelligence")
        return characters

    def _initialize_character_personalities(self) -> Dict[str, CharacterPersonality]:
        """Initialisiert Character-spezifische Persönlichkeiten"""
        personalities = {}

        # 🏆 HAUPTCHARAKTERE
        personalities["tsunade"] = CharacterPersonality(
            empathy_level=0.95,
            protective_instinct=1.0,
            nurturing_tendency=1.0,
            social_sensitivity=0.9,
            physical_need_detection=0.95,
            emotional_need_detection=1.0,
            comfort_offering_style="maternal",
            preferred_activities=["medical_care", "cooking", "protecting", "cuddling"],
            comfort_methods=["warm_milk", "hugging", "soothing_voice", "medical_attention"]
        )

        personalities["naruto"] = CharacterPersonality(
            empathy_level=0.8,
            protective_instinct=0.7,
            nurturing_tendency=0.6,
            social_sensitivity=0.85,
            physical_need_detection=0.6,
            emotional_need_detection=0.8,
            comfort_offering_style="friendly",
            preferred_activities=["ramen_eating", "training", "games", "adventures"],
            comfort_methods=["funny_stories", "ramen_sharing", "energy_boost", "friendship"]
        )

        personalities["sasuke"] = CharacterPersonality(
            empathy_level=0.4,
            protective_instinct=0.8,
            nurturing_tendency=0.3,
            social_sensitivity=0.5,
            physical_need_detection=0.5,
            emotional_need_detection=0.6,
            comfort_offering_style="protective",
            preferred_activities=["training", "quiet_time", "strength_building"],
            comfort_methods=["silent_presence", "training_offer", "subtle_protection"]
        )

        personalities["sakura"] = CharacterPersonality(
            empathy_level=0.85,
            protective_instinct=0.7,
            nurturing_tendency=0.8,
            social_sensitivity=0.8,
            physical_need_detection=0.9,
            emotional_need_detection=0.85,
            comfort_offering_style="caring",
            preferred_activities=["medical_help", "studying", "girl_talk", "flower_viewing"],
            comfort_methods=["medical_care", "gentle_words", "healing_touch", "understanding"]
        )

        personalities["kakashi"] = CharacterPersonality(
            empathy_level=0.7,
            protective_instinct=0.9,
            nurturing_tendency=0.5,
            social_sensitivity=0.75,
            physical_need_detection=0.7,
            emotional_need_detection=0.8,
            comfort_offering_style="protective",
            preferred_activities=["reading", "training", "teaching", "observing"],
            comfort_methods=["wisdom_sharing", "patient_listening", "silent_support"]
        )

        # 🎯 ROOKIE 9
        personalities["kiba"] = CharacterPersonality(
            empathy_level=0.6,
            protective_instinct=0.8,
            nurturing_tendency=0.5,
            social_sensitivity=0.7,
            physical_need_detection=0.8,  # Wolfs-Instinkte!
            emotional_need_detection=0.7,
            comfort_offering_style="pack_leader",
            preferred_activities=["outdoor_activities", "running", "pack_bonding"],
            comfort_methods=["pack_protection", "physical_activity", "loyalty_showing"]
        )

        personalities["hinata"] = CharacterPersonality(
            empathy_level=1.0,
            protective_instinct=0.6,
            nurturing_tendency=0.9,
            social_sensitivity=0.95,
            physical_need_detection=0.8,
            emotional_need_detection=1.0,
            comfort_offering_style="gentle",
            preferred_activities=["quiet_activities", "flower_watching", "gentle_care"],
            comfort_methods=["soft_presence", "understanding_silence", "gentle_touch"]
        )

        personalities["shikamaru"] = CharacterPersonality(
            empathy_level=0.65,
            protective_instinct=0.6,
            nurturing_tendency=0.4,
            social_sensitivity=0.8,  # Intelligent observation
            physical_need_detection=0.7,
            emotional_need_detection=0.8,
            comfort_offering_style="analytical",
            preferred_activities=["strategic_games", "cloud_watching", "problem_solving"],
            comfort_methods=["logical_solutions", "calm_presence", "strategic_thinking"]
        )

        personalities["ino"] = CharacterPersonality(
            empathy_level=0.75,
            protective_instinct=0.6,
            nurturing_tendency=0.7,
            social_sensitivity=0.9,
            physical_need_detection=0.7,
            emotional_need_detection=0.85,
            comfort_offering_style="social",
            preferred_activities=["flower_arranging", "gossiping", "beauty_care", "shopping"],
            comfort_methods=["social_distraction", "beauty_tips", "emotional_support"]
        )

        personalities["choji"] = CharacterPersonality(
            empathy_level=0.8,
            protective_instinct=0.7,
            nurturing_tendency=0.8,
            social_sensitivity=0.7,
            physical_need_detection=0.9,  # Food expert!
            emotional_need_detection=0.75,
            comfort_offering_style="nurturing",
            preferred_activities=["eating", "cooking", "food_sharing", "gentle_activities"],
            comfort_methods=["food_offering", "gentle_presence", "comfort_eating"]
        )

        personalities["neji"] = CharacterPersonality(
            empathy_level=0.5,
            protective_instinct=0.7,
            nurturing_tendency=0.4,
            social_sensitivity=0.6,
            physical_need_detection=0.6,
            emotional_need_detection=0.7,
            comfort_offering_style="formal",
            preferred_activities=["training", "meditation", "duty_fulfillment"],
            comfort_methods=["logical_advice", "structured_support", "duty_reminder"]
        )

        personalities["lee"] = CharacterPersonality(
            empathy_level=0.7,
            protective_instinct=0.8,
            nurturing_tendency=0.6,
            social_sensitivity=0.7,
            physical_need_detection=0.8,
            emotional_need_detection=0.7,
            comfort_offering_style="energetic",
            preferred_activities=["training", "youth_activities", "motivation", "exercise"],
            comfort_methods=["training_motivation", "positive_energy", "physical_activity"]
        )

        personalities["tenten"] = CharacterPersonality(
            empathy_level=0.7,
            protective_instinct=0.6,
            nurturing_tendency=0.7,
            social_sensitivity=0.7,
            physical_need_detection=0.7,
            emotional_need_detection=0.7,
            comfort_offering_style="supportive",
            preferred_activities=["weapon_training", "precision_work", "team_support"],
            comfort_methods=["practical_help", "skill_teaching", "reliable_presence"]
        )

        personalities["shino"] = CharacterPersonality(
            empathy_level=0.6,
            protective_instinct=0.7,
            nurturing_tendency=0.5,
            social_sensitivity=0.8,  # Observant
            physical_need_detection=0.7,
            emotional_need_detection=0.8,
            comfort_offering_style="quiet",
            preferred_activities=["observation", "analysis", "quiet_presence"],
            comfort_methods=["silent_support", "analytical_insights", "patient_waiting"]
        )

        # 🎓 ADULTS
        personalities["iruka"] = CharacterPersonality(
            empathy_level=0.9,
            protective_instinct=0.8,
            nurturing_tendency=0.9,
            social_sensitivity=0.85,
            physical_need_detection=0.8,
            emotional_need_detection=0.9,
            comfort_offering_style="teacher",
            preferred_activities=["teaching", "reading", "student_care"],
            comfort_methods=["gentle_teaching", "patient_listening", "educational_support"]
        )

        personalities["guy"] = CharacterPersonality(
            empathy_level=0.7,
            protective_instinct=0.8,
            nurturing_tendency=0.6,
            social_sensitivity=0.6,
            physical_need_detection=0.9,
            emotional_need_detection=0.7,
            comfort_offering_style="energetic",
            preferred_activities=["training", "youth_activities", "motivation"],
            comfort_methods=["training_motivation", "youth_energy", "positive_thinking"]
        )

        personalities["kurenai"] = CharacterPersonality(
            empathy_level=0.85,
            protective_instinct=0.7,
            nurturing_tendency=0.8,
            social_sensitivity=0.9,
            physical_need_detection=0.7,
            emotional_need_detection=0.9,
            comfort_offering_style="gentle",
            preferred_activities=["teaching", "genjutsu_practice", "quiet_support"],
            comfort_methods=["gentle_guidance", "emotional_understanding", "calm_presence"]
        )

        personalities["asuma"] = CharacterPersonality(
            empathy_level=0.7,
            protective_instinct=0.8,
            nurturing_tendency=0.6,
            social_sensitivity=0.7,
            physical_need_detection=0.7,
            emotional_need_detection=0.7,
            comfort_offering_style="mentor",
            preferred_activities=["training", "strategic_games", "mentoring"],
            comfort_methods=["practical_advice", "shared_experience", "mentor_guidance"]
        )

        personalities["shizune"] = CharacterPersonality(
            empathy_level=0.8,
            protective_instinct=0.6,
            nurturing_tendency=0.8,
            social_sensitivity=0.8,
            physical_need_detection=0.9,  # Medical training
            emotional_need_detection=0.8,
            comfort_offering_style="medical",
            preferred_activities=["medical_care", "organization", "support_work"],
            comfort_methods=["medical_attention", "organized_care", "gentle_efficiency"]
        )

        # Fallback für nicht definierte Characters
        default_personality = CharacterPersonality(
            empathy_level=0.6,
            protective_instinct=0.5,
            nurturing_tendency=0.5,
            social_sensitivity=0.6,
            physical_need_detection=0.6,
            emotional_need_detection=0.6,
            comfort_offering_style="neutral",
            preferred_activities=["conversation", "help_offering"],
            comfort_methods=["presence", "listening"]
        )

        # Fülle fehlende Characters mit Default
        for character in self.all_characters:
            if character not in personalities:
                personalities[character] = default_personality

        return personalities

    def analyze_current_context(self, current_character: str) -> List[PredictedNeed]:
        """🎯 Analysiert Kontext für spezifischen Character"""

        if current_character not in self.character_personalities:
            return []

        personality = self.character_personalities[current_character]
        predicted_needs = []

        # 1. TIME-BASED PREDICTIONS (mit Time System)
        time_predictions = self._analyze_time_patterns(personality, current_character)
        predicted_needs.extend(time_predictions)

        # 2. CHARACTER-SPECIFIC SENSITIVITY
        sensitivity_predictions = self._analyze_character_sensitivity(personality, current_character)
        predicted_needs.extend(sensitivity_predictions)

        # 3. TEXT ANALYSIS
        text_predictions = self._analyze_text_patterns(personality)
        predicted_needs.extend(text_predictions)

        # 4. BEHAVIORAL PATTERNS
        behavior_predictions = self._analyze_behavioral_patterns(personality)
        predicted_needs.extend(behavior_predictions)

        # Sortiere und beschränke auf Top 3
        return self._rank_predictions(predicted_needs)[:3]

    def _analyze_time_patterns(self, personality: CharacterPersonality, character_name: str) -> List[PredictedNeed]:
        """⏰ Zeit-basierte Vorhersagen mit Time System"""
        predictions = []

        # Prüfe ob Time System verfügbar
        if not hasattr(self.game_data, 'time_system'):
            return predictions

        time_system = self.game_data.time_system

        # MEAL TIME DETECTION
        meal_time = time_system.is_meal_time()
        if meal_time and personality.physical_need_detection > 0.7:

            # ✅ ADD DAILY COOLDOWN CHECK HERE:
            from moduls.daily_cooldown_system import has_mentioned_today

            if has_mentioned_today("food", character_name):
                print(f"🚫 Überspringt Essensvorschlag von {character_name} an - wurde schon gemacht!")
            else:
                urgency = 4 if personality.nurturing_tendency > 0.8 else 3

                suggestions = []
                if character_name == "naruto":
                    suggestions = ["Schlägt Ramen vor", "Geht zusammen essen", "Teilt Essen"]
                elif character_name == "choji":
                    suggestions = ["Bietet selbstgemachtes Essen", "Kocht zusammen", "Bringt Snacks"]
                elif character_name == "tsunade":
                    pass
                else:
                    suggestions = ["Bietet Essen an", "Erinnert an Essenszeit"]

                # Only add prediction if not already mentioned today
                if suggestions:  # Also check if suggestions exist
                    predictions.append(PredictedNeed(
                        need_type=PlayerNeed.FOOD,
                        confidence=PredictionConfidence.LIKELY,
                        reasoning=f"{meal_time}-Zeit erkannt - {character_name} mit {personality.comfort_offering_style} Stil reagiert",
                        suggested_actions=suggestions,
                        urgency_level=urgency,
                        character_specific=True
                    ))

        # SLEEP TIME DETECTION
        if time_system.is_sleep_time() and personality.protective_instinct > 0.6:

            # ✅ ADD DAILY COOLDOWN CHECK FOR SLEEP:
            from moduls.daily_cooldown_system import has_mentioned_today

            if has_mentioned_today("sleep", character_name):
                print(f"🚫 überspringt Schlafvorhersage für {character_name} - wurde heute schon erwähnt.")
            else:
                suggestions = []
                if character_name == "tsunade":
                    suggestions = ["Bereitet Bett vor", "Bringt warme Milch", "Singt Schlaflied"]
                elif character_name == "sakura":
                    suggestions = ["Erinnert an Schlafenszeit", "Bietet medizinische Entspannung"]
                else:
                    suggestions = ["Schlägt Ruhe vor", "Bereitet ruhige Umgebung"]

                predictions.append(PredictedNeed(
                    need_type=PlayerNeed.REST,
                    confidence=PredictionConfidence.LIKELY,
                    reasoning=f"Schlafenszeit - {character_name} achtet auf Sukuna's Müdigkeit",
                    suggested_actions=suggestions,
                    urgency_level=3,
                    character_specific=True
                ))

        # TRAINING TIME für aktive Characters
        if time_system.is_training_time() and character_name in ["sasuke", "lee", "guy", "kakashi"]:
            if personality.physical_need_detection > 0.6:
                from moduls.daily_cooldown_system import has_mentioned_today

                if has_mentioned_today("training", character_name):
                    print(f"🚫 überspringt Trainingsvorhersage für {character_name} - wurde heute schon erwähnt.")

                predictions.append(PredictedNeed(
                    need_type=PlayerNeed.STIMULATION,
                    confidence=PredictionConfidence.POSSIBLE,
                    reasoning=f"Trainingszeit - {character_name} könnte körperliche Aktivität vorschlagen",
                    suggested_actions=["Schlägt Training vor", "Bietet Übungen an", "Motiviert zur Bewegung"],
                    urgency_level=2,
                    character_specific=True
                ))

        return predictions

    def _analyze_character_sensitivity(self, personality: CharacterPersonality, character_name: str) -> List[
        PredictedNeed]:
        """🎭 Character-spezifische Sensitivitäten"""
        predictions = []

        # TSUNADE: Maternal Instinct Override
        if character_name == "tsunade":
            predictions.append(PredictedNeed(
                need_type=PlayerNeed.PROTECTION,
                confidence=PredictionConfidence.LIKELY,
                reasoning="Tsunades Mutter-Instinkt ist immer aktiv - spürt Schutzbedürfnis",
                suggested_actions=["Wird automatisch beschützend", "Überprüft Umgebung", "Positioniert sich schützend"],
                urgency_level=3,
                character_specific=True
            ))

            # FAMILY TIME NEED (Tsunade-spezifisch)
            if hasattr(self.game_data, 'family_time_system'):
                family_system = self.game_data.family_time_system
                if not family_system._had_family_time_today():
                    urgency = 4 if family_system.missed_family_times > 1 else 3
                    predictions.append(PredictedNeed(
                        need_type=PlayerNeed.SOCIAL,  # Verwende SOCIAL für Familie
                        confidence=PredictionConfidence.CERTAIN,
                        reasoning=f"Tsunade vermisst Familienzeit - {family_system.missed_family_times} Tage ohne",
                        suggested_actions=["Schlägt Familienzeit vor", "Besteht auf gemeinsame Zeit",
                                           "Plant Aktivität"],
                        urgency_level=urgency,
                        character_specific=True
                    ))

        # KIBA: Wolf-Connection mit Sukuna
        elif character_name == "kiba":
            predictions.append(PredictedNeed(
                need_type=PlayerNeed.SOCIAL,
                confidence=PredictionConfidence.POSSIBLE,
                reasoning="Kiba spürt Sukuna's Wolfs-Natur - Pack-Instinkt aktiviert",
                suggested_actions=["Bietet Pack-Zugehörigkeit", "Zeigt Loyalität", "Schlägt Rudel-Aktivitäten vor"],
                urgency_level=2,
                character_specific=True
            ))

        # HINATA: Extreme Empathie
        elif character_name == "hinata":
            if personality.emotional_need_detection == 1.0:
                predictions.append(PredictedNeed(
                    need_type=PlayerNeed.EMOTIONAL_RELEASE,
                    confidence=PredictionConfidence.POSSIBLE,
                    reasoning="Hinatas perfekte Empathie erkennt versteckte emotionale Belastung",
                    suggested_actions=["Bietet sanftes Gespräch", "Schafft sicheren Raum", "Hört geduldig zu"],
                    urgency_level=2,
                    character_specific=True
                ))

        # SAKURA: Medical Awareness
        elif character_name == "sakura":
            if personality.physical_need_detection > 0.8:
                predictions.append(PredictedNeed(
                    need_type=PlayerNeed.MEDICAL,
                    confidence=PredictionConfidence.POSSIBLE,
                    reasoning="Sakuras medizinische Ausbildung erkennt körperliche Beschwerden",
                    suggested_actions=["Bietet med. Untersuchung", "Fragt nach Schmerzen", "Überprüft Gesundheit"],
                    urgency_level=3,
                    character_specific=True
                ))

        return predictions

    def _analyze_text_patterns(self, personality: CharacterPersonality) -> List[PredictedNeed]:
        """📝 Analysiert Text-Patterns in recent messages"""
        predictions = []

        # Hole recent messages falls verfügbar
        recent_messages = self._get_recent_messages()

        for message in recent_messages:
            message_lower = message.lower()

            # MÜDIGKEIT Indikatoren
            if any(ind in message_lower for ind in ["müde", "erschöpft", "schlapp", "gähne"]):
                if personality.physical_need_detection > 0.6:
                    predictions.append(PredictedNeed(
                        need_type=PlayerNeed.REST,
                        confidence=PredictionConfidence.LIKELY,
                        reasoning="Müdigkeits-Indikatoren in Text erkannt",
                        suggested_actions=personality.comfort_methods[:2],
                        urgency_level=3,
                        character_specific=True
                    ))

            # EMOTIONALE BELASTUNG
            if any(ind in message_lower for ind in ["traurig", "einsam", "verletzt", "schmerz"]):
                if personality.emotional_need_detection > 0.7:
                    predictions.append(PredictedNeed(
                        need_type=PlayerNeed.COMFORT,
                        confidence=PredictionConfidence.CERTAIN,
                        reasoning="Emotionale Belastung direkt geäußert",
                        suggested_actions=personality.comfort_methods,
                        urgency_level=5,
                        character_specific=True
                    ))

        return predictions

    def _analyze_behavioral_patterns(self, personality: CharacterPersonality) -> List[PredictedNeed]:
        """🎯 Analysiert Verhaltensmuster"""
        predictions = []

        # SILENCE PATTERN
        if self._detect_recent_silence():
            if personality.social_sensitivity > 0.8:
                predictions.append(PredictedNeed(
                    need_type=PlayerNeed.COMFORT,
                    confidence=PredictionConfidence.LIKELY,
                    reasoning="Schweige-Muster erkannt - meist emotionale Belastung",
                    suggested_actions=["Fragt sanft nach", "Bietet nonverbale Unterstützung", "Bleibt verfügbar"],
                    urgency_level=3,
                    character_specific=True
                ))

        return predictions

    def _get_recent_messages(self, limit: int = 5) -> List[str]:
        """Holt recent chat messages"""
        messages = []

        if hasattr(self.game_data, 'gui') and hasattr(self.game_data.gui, 'chat_messages'):
            recent = self.game_data.gui.chat_messages[-limit:]
            for sender, message in recent:
                if sender.lower() == 'sukuna':  # Nur Player-Messages
                    messages.append(message)

        return messages

    def _detect_recent_silence(self) -> bool:
        """Erkennt ob Player kürzlich schweigsam war"""
        recent_messages = self._get_recent_messages(3)

        silence_indicators = ["...", "*schweigt*", "*sagt nichts*"]
        silent_count = 0

        for message in recent_messages:
            if (len(message.strip()) < 5 or
                    any(ind in message.lower() for ind in silence_indicators)):
                silent_count += 1

        return silent_count >= 2

    def _rank_predictions(self, predictions: List[PredictedNeed]) -> List[PredictedNeed]:
        """Rankt Vorhersagen nach Relevanz"""
        # Sortiere nach Confidence * Urgency
        predictions.sort(key=lambda p: p.confidence.value * p.urgency_level, reverse=True)
        return predictions

    def generate_proactive_response(self, current_character: str, predicted_needs: List[PredictedNeed]) -> str:
        """🎭 Generiert proaktive Character-Reaktion"""

        if not predicted_needs:
            return ""

        top_prediction = predicted_needs[0]
        personality = self.character_personalities.get(current_character)

        if not personality:
            return ""

        # Character-spezifische Reaktionen
        character_responses = self._get_character_responses()

        need_type = top_prediction.need_type
        responses = character_responses.get(current_character, {}).get(need_type, [])

        if responses:
            chosen_response = random.choice(responses)
            reasoning = f"\n💭 *{current_character.title()} spürt: {top_prediction.reasoning}*"
            return chosen_response + reasoning

        return f"*{current_character.title()} bemerkt dass du etwas brauchst und wird aufmerksam*"

    def _get_character_responses(self) -> Dict:
        """Character-spezifische Response-Templates"""
        return {
            "tsunade": {
                PlayerNeed.REST: [
                    "*bemerkt deine Müdigkeit sofort*\n'Du siehst erschöpft aus, mein kleiner Wolf. Zeit fürs Bett.'",
                    "*wird sofort fürsorglich* 'Komm, Mama bringt dich ins Bett. Du brauchst Schlaf.'"
                ],
                PlayerNeed.COMFORT: [
                    "*spürt instinktiv dass du Trost brauchst*\n'Komm her zu Mama. Ich sehe es in deinen Augen.'",
                    "*öffnet ihre Arme* 'Was bedrückt dich, mein Schatz? Erzähl es mir.'"
                ],
                PlayerNeed.FOOD: [
                    "*bemerkt dass du hungrig sein musst*\n'Wann hast du das letzte Mal richtig gegessen?'",
                    "*steht bereits auf* 'Ich mache dir etwas Leckeres. Kein Widerspruch.'"
                ],
                PlayerNeed.SOCIAL: [  # Family Time als SOCIAL
                    "*wird entschlossen* 'Sukuna, wir hatten schon zu lange keine Familienzeit.'",
                    "*liebevoll aber bestimmt* 'Zeit für uns beide. Familienzeit ist wichtig.'",
                    "*öffnet Arme einladend* 'Komm her, mein kleiner Wolf. Mama braucht Zeit mit dir.'"
                ]
            },

            "naruto": {
                PlayerNeed.SOCIAL: [
                    "*merkt dass du Gesellschaft brauchst*\n'Hey, du wirkst einsam, dattebayo! Lass uns was machen!'",
                    "*springt energisch auf* 'Komm schon! Wir können nicht hier rumsitzen!'"
                ],
                PlayerNeed.FOOD: [
                    "*Magen knurrt* 'Oh! Ramen-Zeit, dattebayo! Komm, ich lad dich ein!'",
                    "*wird aufgeregt* 'Ich weiß den perfekten Ramen-Stand! Los geht's!'"
                ]
            },

            "sakura": {
                PlayerNeed.MEDICAL: [
                    "*bemerkt kleine Anzeichen*\n'Ist alles okay? Du siehst blass aus.'",
                    "*wird aufmerksam* 'Lass mich schnell schauen ob alles in Ordnung ist.'"
                ],
                PlayerNeed.COMFORT: [
                    "*erkennt emotionale Belastung*\n'Du hältst etwas zurück, oder? Es ist okay zu reden.'",
                    "*spricht sanft* 'Ich bin hier, wenn du jemanden zum Reden brauchst.'"
                ]
            },

            "hinata": {
                PlayerNeed.COMFORT: [
                    "*spricht sehr sanft*\n'D-du siehst traurig aus... möchtest du darüber reden?'",
                    "*bietet stille Unterstützung* 'I-ich bleibe bei dir... wenn du magst.'"
                ],
                PlayerNeed.SOLITUDE: [
                    "*versteht den Wunsch nach Ruhe*\n'S-soll ich dich allein lassen?'",
                    "*respektiert deinen Raum* 'Ich... ich bin da wenn du mich brauchst.'"
                ]
            },

            "kiba": {
                PlayerNeed.SOCIAL: [
                    "*rudel-Instinkt aktiviert*\n'Hey, Pack-Leader! Du brauchst die Gruppe!'",
                    "*Akamaru bellt zustimmend* 'Wir lassen dich nicht allein, keine Sorge!'"
                ],
                PlayerNeed.STIMULATION: [
                    "*wird wild* 'Komm! Lass uns rennen! Du brauchst Action!'",
                    "*springt auf* 'Akamaru und ich zeigen dir coole Sachen!'"
                ]
            }
        }

    def get_prediction_summary(self, current_character: str) -> str:
        """📊 Zeigt Vorhersage-System Summary"""
        predictions = self.analyze_current_context(current_character)

        summary = f"🔮 **PREDICTIVE INTELLIGENCE** für {current_character.title()}:\n\n"

        if predictions:
            summary += "**AKTUELLE VORHERSAGEN:**\n"
            for i, pred in enumerate(predictions, 1):
                summary += f"{i}. **{pred.need_type.value.title()}** ({pred.confidence.value:.0%} sicher)\n"
                summary += f"   💡 {pred.reasoning}\n"
                summary += f"   🎯 Urgenz: {pred.urgency_level}/5\n\n"
        else:
            summary += "😌 Keine besonderen Bedürfnisse vorhergesagt\n\n"

        personality = self.character_personalities.get(current_character)
        if personality:
            summary += f"🎭 **{current_character.title()}'s Sensitivität:**\n"
            summary += f"• Empathie: {personality.empathy_level:.1f}\n"
            summary += f"• Schutzinstinkt: {personality.protective_instinct:.1f}\n"
            summary += f"• Fürsorglichkeit: {personality.nurturing_tendency:.1f}\n"
            summary += f"• Stil: {personality.comfort_offering_style}\n"

        return summary


def integrate_enhanced_predictive_intelligence(game_data):
    """🔧 Integriert Enhanced Predictive Intelligence"""

    # Erstelle Enhanced Predictive System
    predictive_system = EnhancedPredictiveIntelligence(game_data)
    game_data.enhanced_predictive_intelligence = predictive_system

    # Erweitere get_llm_response
    if hasattr(game_data, 'get_llm_response'):
        original_get_llm_response = game_data.get_llm_response

        def predictive_enhanced_llm_response(user_input: str) -> str:
            """LLM Response mit Enhanced Predictive Intelligence"""

            # Normale Response
            base_response = original_get_llm_response(user_input)

            # Current Character
            current_character = getattr(game_data, 'active_character', 'tsunade')

            # Predictive Analysis (läuft im Hintergrund, zeigt aber nur saubere Outputs)
            try:
                predicted_needs = predictive_system.analyze_current_context(current_character)

                if predicted_needs and random.random() < 0.15:
                    proactive_response = predictive_system.generate_proactive_response(
                        current_character, predicted_needs
                    )

                    if proactive_response:
                        import re

                        # Entferne alle bekannten Corruption-Strings
                        clean = proactive_response
                        clean = re.sub(r'\*öffnet Arme einladend\*.*?(?=\n|$)', '', clean, flags=re.DOTALL)
                        clean = re.sub(r"'Komm her, mein kleiner Wolf[^']*'", '', clean)
                        clean = re.sub(r'Mama braucht Zeit mit dir\.?', '', clean)
                        clean = re.sub(r'💭 \*[^*]+spürt:[^*]*\*', '', clean)
                        clean = re.sub(r'\*wird entschlossen\*.*?(?=\n|$)', '', clean, flags=re.DOTALL)
                        clean = re.sub(r'\*liebevoll aber bestimmt\*.*?(?=\n|$)', '', clean, flags=re.DOTALL)
                        clean = re.sub(r'Sukuna.*?keine Familienzeit.*?(?=\n|$)', '', clean, flags=re.DOTALL)
                        clean = clean.strip()

                        # Nur anzeigen wenn nach Cleaning noch sinnvoller Text übrig
                        if clean and len(clean) > 20 and hasattr(game_data, 'gui') and game_data.gui:
                            game_data.gui.display_message("💭 Vorhersage", clean, "info")

            except Exception as e:
                print(f"⚠️ Predictive Intelligence Fehler: {e}")

            return base_response

        game_data.get_llm_response = predictive_enhanced_llm_response

    print("🔮 ENHANCED PREDICTIVE INTELLIGENCE erfolgreich integriert!")
    print("🎯 Features für ALLE Characters:")
    print(f"   • {len(predictive_system.all_characters)} Characters mit Prediction Support")
    print("   • Zeit-basierte Vorhersagen (mit Time System)")
    print("   • Character-spezifische Sensitivitäten")
    print("   • Proaktive NPC-Reaktionen")
    print("   • Text- und Verhaltens-Analyse")

    return predictive_system


if __name__ == "__main__":
    print("🔮 ENHANCED PREDICTIVE INTELLIGENCE")
    print("===================================")
    print("✅ Alle 32+ Characters unterstützt")
    print("✅ Time System Integration")
    print("✅ Character-spezifische Persönlichkeiten")
    print("✅ Proaktive Bedürfnis-Erkennung")