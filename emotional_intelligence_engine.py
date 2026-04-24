# -*- coding: utf-8 -*-
"""
💭 EMOTIONAL INTELLIGENCE ENGINE - Updated mit vollständiger Emotion-Liste
Claude Ultra Level emotionale Intelligenz für alle NPCs
"""

import random
import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class EmotionalState(Enum):
    """VOLLSTÄNDIGE emotionale Zustände - Updated"""
    # Basis-Emotionen
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    FRUSTRATION = "frustration"

    # Soziale Emotionen
    LOVE = "love"
    AFFECTION = "affection"
    TRUST = "trust"
    GRATITUDE = "gratitude"
    PRIDE = "pride"
    SHAME = "shame"
    GUILT = "guilt"
    JEALOUSY = "jealousy"
    EXCITEMENT = "excitement"

    # Komplexe Emotionen
    NOSTALGIA = "nostalgia"
    MELANCHOLY = "melancholy"
    CONTENTMENT = "contentment"
    ANXIETY = "anxiety"
    RELIEF = "relief"
    HOPE = "hope"
    DESPAIR = "despair"
    LONGING = "longing"
    FOCUS = "focused"
    CONFLICTED = "conflicted"

    # Neutrale Zustände
    CALM = "calm"
    NEUTRAL = "neutral"
    CONFUSED = "confused"

    # Erweiterte Zustände (die vorher gefehlt haben)
    PROTECTIVE = "protective"
    CONCERN = "concern"
    VULNERABLE = "vulnerable"
    CARING = "caring"
    EMPATHETIC = "empathetic"


class EmotionalIntensity(Enum):
    """Intensität von Emotionen"""
    SUBTLE = 1  # Kaum wahrnehmbar
    MILD = 2  # Leicht spürbar
    MODERATE = 3  # Deutlich erkennbar
    STRONG = 4  # Stark ausgeprägt
    INTENSE = 5  # Überwältigend


class EmotionalContext(Enum):
    """Emotionale Kontexte für Situationen"""
    INTIMATE = "intimate"
    SUPPORTIVE = "supportive"
    PLAYFUL = "playful"
    SERIOUS = "serious"
    COMFORTING = "comforting"
    TEACHING = "teaching"
    PROTECTIVE = "protective"
    VULNERABLE = "vulnerable"
    CELEBRATORY = "celebratory"
    CONFLICTED = "conflicted"


@dataclass
class EmotionalAnalysis:
    """Detaillierte emotionale Analyse"""
    primary_emotion: EmotionalState
    secondary_emotions: List[EmotionalState]
    intensity: EmotionalIntensity
    context: EmotionalContext
    confidence: float

    # Erweiterte Analyse
    underlying_needs: List[str]
    triggers: List[str]
    subtext: str
    temporal_aspect: str  # past/present/future focused

    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class EmotionalProfile:
    """Emotionales Profil eines Charakters"""
    character_name: str

    # Empathie-Fähigkeiten
    empathy_level: float = 0.7  # 0-1.0
    emotional_sensitivity: float = 0.7  # 0-1.0
    response_authenticity: float = 0.8  # Wie authentisch reagiert der Character

    # Character-spezifische Emotionale Präferenzen
    dominant_emotions: List[EmotionalState] = None
    comfort_emotions: List[EmotionalState] = None
    stress_emotions: List[EmotionalState] = None

    def __post_init__(self):
        if self.dominant_emotions is None:
            self.dominant_emotions = [EmotionalState.CARING, EmotionalState.PROTECTIVE]
        if self.comfort_emotions is None:
            self.comfort_emotions = [EmotionalState.CALM, EmotionalState.AFFECTION]
        if self.stress_emotions is None:
            self.stress_emotions = [EmotionalState.CONCERN, EmotionalState.ANXIETY]


class AdvancedEmotionalIntelligence:
    """💭 Claude Ultra Level Emotional Intelligence"""

    def __init__(self, game_data):
        self.game_data = game_data

        # Emotionale Profile für alle Characters
        self.character_profiles = self._initialize_character_profiles()

        # Erweiterte Emotions-Erkennung
        self.emotion_patterns = self._initialize_emotion_patterns()
        self.subtext_recognition = self._initialize_subtext_patterns()
        self.trigger_database = self._initialize_trigger_database()

        # Lern-System
        self.interaction_history = []
        self.learned_preferences = {}

        print("💭 Advanced Emotional Intelligence initialisiert")

    def _initialize_character_profiles(self) -> Dict[str, EmotionalProfile]:
        """Initialisiert emotionale Profile für alle Characters"""
        profiles = {}

        # 🏆 HAUPTCHARAKTERE
        profiles["tsunade"] = EmotionalProfile(
            character_name="tsunade",
            empathy_level=0.95,
            emotional_sensitivity=0.9,
            response_authenticity=0.95,
            dominant_emotions=[EmotionalState.PROTECTIVE, EmotionalState.CARING, EmotionalState.LOVE],
            comfort_emotions=[EmotionalState.AFFECTION, EmotionalState.CONTENTMENT],
            stress_emotions=[EmotionalState.CONCERN, EmotionalState.ANXIETY, EmotionalState.PROTECTIVE]
        )

        profiles["naruto"] = EmotionalProfile(
            character_name="naruto",
            empathy_level=0.8,
            emotional_sensitivity=0.85,
            response_authenticity=0.9,
            dominant_emotions=[EmotionalState.EXCITEMENT, EmotionalState.JOY, EmotionalState.CARING],
            comfort_emotions=[EmotionalState.JOY, EmotionalState.EXCITEMENT],
            stress_emotions=[EmotionalState.ANXIETY, EmotionalState.CONFLICTED]
        )

        profiles["sasuke"] = EmotionalProfile(
            character_name="sasuke",
            empathy_level=0.5,
            emotional_sensitivity=0.6,
            response_authenticity=0.7,
            dominant_emotions=[EmotionalState.FOCUS, EmotionalState.CONFLICTED, EmotionalState.PROTECTIVE],
            comfort_emotions=[EmotionalState.CALM, EmotionalState.FOCUS],
            stress_emotions=[EmotionalState.ANGER, EmotionalState.CONFLICTED]
        )

        profiles["sakura"] = EmotionalProfile(
            character_name="sakura",
            empathy_level=0.85,
            emotional_sensitivity=0.8,
            response_authenticity=0.85,
            dominant_emotions=[EmotionalState.CARING, EmotionalState.EMPATHETIC, EmotionalState.CONCERN],
            comfort_emotions=[EmotionalState.CONTENTMENT, EmotionalState.PRIDE],
            stress_emotions=[EmotionalState.ANXIETY, EmotionalState.CONCERN]
        )

        profiles["kakashi"] = EmotionalProfile(
            character_name="kakashi",
            empathy_level=0.75,
            emotional_sensitivity=0.8,
            response_authenticity=0.8,
            dominant_emotions=[EmotionalState.PROTECTIVE, EmotionalState.FOCUS, EmotionalState.CONCERN],
            comfort_emotions=[EmotionalState.CALM, EmotionalState.CONTENTMENT],
            stress_emotions=[EmotionalState.CONCERN, EmotionalState.FOCUS]
        )

        # 🎯 ROOKIE 9
        profiles["hinata"] = EmotionalProfile(
            character_name="hinata",
            empathy_level=1.0,  # Perfekte Empathie
            emotional_sensitivity=0.95,
            response_authenticity=0.9,
            dominant_emotions=[EmotionalState.EMPATHETIC, EmotionalState.CARING, EmotionalState.VULNERABLE],
            comfort_emotions=[EmotionalState.CALM, EmotionalState.AFFECTION],
            stress_emotions=[EmotionalState.ANXIETY, EmotionalState.SHAME]
        )

        profiles["kiba"] = EmotionalProfile(
            character_name="kiba",
            empathy_level=0.7,
            emotional_sensitivity=0.8,  # Wolfs-Instinkte
            response_authenticity=0.85,
            dominant_emotions=[EmotionalState.EXCITEMENT, EmotionalState.PROTECTIVE, EmotionalState.TRUST],
            comfort_emotions=[EmotionalState.EXCITEMENT, EmotionalState.PRIDE],
            stress_emotions=[EmotionalState.ANGER, EmotionalState.PROTECTIVE]
        )

        profiles["shikamaru"] = EmotionalProfile(
            character_name="shikamaru",
            empathy_level=0.65,
            emotional_sensitivity=0.8,  # Intelligent observation
            response_authenticity=0.75,
            dominant_emotions=[EmotionalState.FOCUS, EmotionalState.CALM, EmotionalState.CONCERN],
            comfort_emotions=[EmotionalState.CALM, EmotionalState.CONTENTMENT],
            stress_emotions=[EmotionalState.CONFLICTED, EmotionalState.FOCUS]
        )

        profiles["ino"] = EmotionalProfile(
            character_name="ino",
            empathy_level=0.8,
            emotional_sensitivity=0.85,
            response_authenticity=0.8,
            dominant_emotions=[EmotionalState.EXCITEMENT, EmotionalState.EMPATHETIC, EmotionalState.PRIDE],
            comfort_emotions=[EmotionalState.JOY, EmotionalState.PRIDE],
            stress_emotions=[EmotionalState.JEALOUSY, EmotionalState.ANXIETY]
        )

        profiles["choji"] = EmotionalProfile(
            character_name="choji",
            empathy_level=0.85,
            emotional_sensitivity=0.75,
            response_authenticity=0.9,
            dominant_emotions=[EmotionalState.CARING, EmotionalState.CONTENTMENT, EmotionalState.EMPATHETIC],
            comfort_emotions=[EmotionalState.CONTENTMENT, EmotionalState.JOY],
            stress_emotions=[EmotionalState.SHAME, EmotionalState.SADNESS]
        )

        # 🎓 ADULTS
        profiles["iruka"] = EmotionalProfile(
            character_name="iruka",
            empathy_level=0.9,
            emotional_sensitivity=0.85,
            response_authenticity=0.9,
            dominant_emotions=[EmotionalState.CARING, EmotionalState.PROTECTIVE, EmotionalState.EMPATHETIC],
            comfort_emotions=[EmotionalState.CONTENTMENT, EmotionalState.PRIDE],
            stress_emotions=[EmotionalState.CONCERN, EmotionalState.ANXIETY]
        )

        # Fallback für nicht definierte Characters
        default_profile = EmotionalProfile(
            character_name="default",
            empathy_level=0.6,
            emotional_sensitivity=0.6,
            response_authenticity=0.7
        )

        # Alle Characters mit Profilen versorgen
        all_characters = ["tsunade", "naruto", "sasuke", "sakura", "kakashi", "hinata",
                          "kiba", "shikamaru", "ino", "choji", "neji", "lee", "tenten",
                          "shino", "iruka", "guy", "kurenai", "asuma", "shizune"]

        for char in all_characters:
            if char not in profiles:
                profiles[char] = EmotionalProfile(
                    character_name=char,
                    empathy_level=0.6,
                    emotional_sensitivity=0.6,
                    response_authenticity=0.7
                )

        return profiles

    def _initialize_emotion_patterns(self) -> Dict[str, Dict]:
        """Initialisiert Emotion-Erkennungs-Muster"""
        return {
            # Freude/Glück
            EmotionalState.JOY.value: {
                "keywords": ["freude", "glücklich", "fröhlich", "super", "toll", "wunderbar", "fantastisch"],
                "expressions": ["lacht", "lächelt", "grinst", "strahlt", "jubelt"],
                "subtext_indicators": ["endlich", "perfekt", "genau richtig"],
                "intensity_markers": {"leicht": 2, "sehr": 3, "total": 4, "überwältigend": 5}
            },

            # Trauer
            EmotionalState.SADNESS.value: {
                "keywords": ["traurig", "tränen", "weint", "schlecht", "verletzt", "einsam", "leer"],
                "expressions": ["weint", "seufzt", "schluchzt", "senkt kopf"],
                "subtext_indicators": ["egal", "macht nichts", "ist schon okay"],
                "intensity_markers": {"wenig": 2, "ziemlich": 3, "sehr": 4, "verzweifelt": 5}
            },

            # Angst
            EmotionalState.FEAR.value: {
                "keywords": ["angst", "furcht", "nervös", "sorge", "beunruhigt", "panik", "zittrig"],
                "expressions": ["zittert", "versteckt sich", "klammert", "erstarrt", "zurückweicht"],
                "subtext_indicators": ["...?", "was wenn", "ich kann nicht"],
                "intensity_markers": {"etwas": 2, "ziemlich": 3, "große": 4, "panische": 5}
            },

            # Wut
            EmotionalState.ANGER.value: {
                "keywords": ["wütend", "ärger", "zorn", "sauer", "frustriert", "genervt", "aufgebracht"],
                "expressions": ["schreit", "ballt fäuste", "funkelnde augen", "knurrt"],
                "subtext_indicators": ["reicht", "genug", "nicht fair"],
                "intensity_markers": {"etwas": 2, "ziemlich": 3, "richtig": 4, "rasend": 5}
            },

            # Überraschung
            EmotionalState.SURPRISE.value: {
                "keywords": ["überrascht", "wow", "unerwartet", "plötzlich", "nicht gedacht"],
                "expressions": ["augen weiten sich", "mund öffnet sich", "springt auf"],
                "subtext_indicators": ["wirklich?", "das hätte ich nie", "unglaublich"],
                "intensity_markers": {"etwas": 2, "ziemlich": 3, "total": 4, "völlig": 5}
            },

            # Liebe/Zuneigung
            EmotionalState.LOVE.value: {
                "keywords": ["liebe", "lieb", "herzlich", "innig", "zärtlich", "warm"],
                "expressions": ["umarmt", "streichelt", "liebevoll", "sanft berührt"],
                "subtext_indicators": ["für immer", "bedeutest mir", "nie verlieren"],
                "intensity_markers": {"sehr": 3, "unendlich": 4, "bedingungslos": 5}
            },

            # Schutz/Fürsorge
            EmotionalState.PROTECTIVE.value: {
                "keywords": ["beschützen", "sicher", "aufpassen", "bewachen", "verteidigen"],
                "expressions": ["stellt sich vor", "umhüllt", "wachsam", "kampfbereit"],
                "subtext_indicators": ["pass auf", "nicht zulassen", "über meine leiche"],
                "intensity_markers": {"etwas": 2, "sehr": 3, "extrem": 4, "bedingungslos": 5}
            },

            # Sorge/Besorgnis
            EmotionalState.CONCERN.value: {
                "keywords": ["sorge", "besorgt", "gedanken", "unruhig", "grübelt"],
                "expressions": ["runzelt stirn", "nachdenklich", "unruhig", "seufzt"],
                "subtext_indicators": ["hoffentlich", "wenn nur", "mache mir gedanken"],
                "intensity_markers": {"etwas": 2, "ziemlich": 3, "große": 4, "extreme": 5}
            },

            # Verletzlichkeit
            EmotionalState.VULNERABLE.value: {
                "keywords": ["verletzlich", "schwach", "hilflos", "ungeschützt", "offen"],
                "expressions": ["wird kleiner", "sucht schutz", "zittrig", "unsicher"],
                "subtext_indicators": ["brauche", "hilf mir", "kann nicht allein"],
                "intensity_markers": {"etwas": 2, "sehr": 3, "extrem": 4, "völlig": 5}
            },

            # Empathie
            EmotionalState.EMPATHETIC.value: {
                "keywords": ["verstehe", "fühle mit", "nachvollziehen", "mitfühlen", "spüre"],
                "expressions": ["nickt verständnisvoll", "mitleidend", "teilnehmend"],
                "subtext_indicators": ["ich weiß", "geht mir genauso", "kenne das gefühl"],
                "intensity_markers": {"etwas": 2, "sehr": 3, "tief": 4, "vollkommen": 5}
            }
        }

    def _initialize_subtext_patterns(self) -> Dict[str, str]:
        """Erweiterte Subtext-Erkennung"""
        return {
            # Höfliche Ablehnungen/Versteckte Gefühle
            "ist schon okay": "eigentlich_nicht_okay",
            "macht nichts": "macht_schon_etwas",
            "kein problem": "ist_ein_problem",
            "mir geht es gut": "geht_mir_nicht_gut",
            "bin nicht müde": "bin_müde_will_aber_nicht_zugeben",
            "brauche keine hilfe": "brauche_hilfe_bin_aber_stolz",

            # Emotionale Signale
            "...": "unsicher_oder_nachdenklich",
            "vielleicht": "will_es_aber_unsicher",
            "ich weiß nicht": "weiß_es_aber_unsicher",
            "egal": "ist_nicht_egal",

            # Bindungsangst/Versteckte Wünsche
            "du musst nicht": "bitte_tu_es_trotzdem",
            "wenn du willst": "ich_will_es_sehr",
            "ist mir egal": "ist_mir_nicht_egal",
            "geht schon": "freue_mich_heimlich",

            # Trauma-Reaktionen
            "ist lange her": "beschäftigt_mich_noch",
            "habe vergessen": "kann_nicht_vergessen",
            "war nicht so schlimm": "war_sehr_schlimm",
            "bin darüber hinweg": "bin_nicht_darüber_hinweg",

            # Versteckte Bedürfnisse
            "bin stark genug": "brauche_unterstützung",
            "komme allein klar": "will_nicht_allein_sein",
            "stört mich nicht": "stört_mich_sehr"
        }

    def _initialize_trigger_database(self) -> Dict[str, List[str]]:
        """Datenbank emotionaler Trigger"""
        return {
            "abandonment_triggers": ["verlassen", "weggehen", "allein lassen", "nicht da sein"],
            "pain_triggers": ["schmerz", "verletzt", "weh tun", "leiden"],
            "success_triggers": ["geschafft", "stolz", "gut gemacht", "erfolgreich"],
            "comfort_triggers": ["müde", "traurig", "angst", "unsicher"],
            "protection_triggers": ["gefahr", "bedrohung", "unsicher", "angst"],
            "bonding_triggers": ["zusammen", "familie", "freunde", "vertrauen"],
            "trauma_triggers": ["vergangenheit", "früher", "akatsuki", "folter", "schmerz"]
        }

    def analyze_emotional_state(self, message: str, character_name: str,
                                context: str = "", body_language: str = "") -> EmotionalAnalysis:
        """🎯 Analysiert emotionalen Zustand mit Claude-Ultra Niveau"""

        if character_name not in self.character_profiles:
            character_name = "default"

        profile = self.character_profiles[character_name]

        # Multi-dimensionale Analyse
        detected_emotions = self._detect_emotions_comprehensive(message, body_language)
        subtext = self._analyze_advanced_subtext(message)
        triggers = self._identify_emotional_triggers(message, context)
        underlying_needs = self._extract_psychological_needs(message, detected_emotions)

        # Bestimme primäre Emotion
        primary_emotion = self._determine_primary_emotion(detected_emotions, profile)
        secondary_emotions = self._identify_secondary_emotions(detected_emotions, primary_emotion)

        # Berechne Intensität
        intensity = self._calculate_emotional_intensity(message, body_language, detected_emotions)

        # Bestimme Kontext
        emotional_context = self._determine_emotional_context(primary_emotion, context, triggers)

        # Konfidenz der Analyse
        confidence = self._calculate_analysis_confidence(detected_emotions, triggers, profile)

        # Zeitbezug
        temporal_aspect = self._determine_temporal_focus(message)

        return EmotionalAnalysis(
            primary_emotion=primary_emotion,
            secondary_emotions=secondary_emotions,
            intensity=intensity,
            context=emotional_context,
            confidence=confidence,
            underlying_needs=underlying_needs,
            triggers=triggers,
            subtext=subtext,
            temporal_aspect=temporal_aspect
        )

    def _detect_emotions_comprehensive(self, message: str, body_language: str = "") -> Dict[EmotionalState, float]:
        """Umfassende Emotions-Erkennung"""
        detected = {}
        message_lower = message.lower()
        body_lower = body_language.lower()
        combined_text = f"{message_lower} {body_lower}"

        for emotion_name, pattern_data in self.emotion_patterns.items():
            score = 0

            try:
                emotion_state = EmotionalState(emotion_name)
            except ValueError:
                continue

            # Keyword-Matching
            for keyword in pattern_data.get("keywords", []):
                if keyword in combined_text:
                    score += 1

            # Expression-Matching
            for expression in pattern_data.get("expressions", []):
                if expression in combined_text:
                    score += 1.5

            # Subtext-Indicator-Matching
            for indicator in pattern_data.get("subtext_indicators", []):
                if indicator in combined_text:
                    score += 2  # Subtext ist wichtiger

            # Intensitäts-Marker
            for marker, intensity_boost in pattern_data.get("intensity_markers", {}).items():
                if marker in combined_text:
                    score += intensity_boost * 0.5

            if score > 0:
                detected[emotion_state] = min(5.0, score)

        return detected

    def _analyze_advanced_subtext(self, message: str) -> str:
        """Fortgeschrittene Subtext-Analyse"""
        message_lower = message.lower()

        for phrase, meaning in self.subtext_recognition.items():
            if phrase in message_lower:
                return meaning

        # Pattern-basierte Subtext-Erkennung
        if re.search(r'\.\.\.+', message):
            return "hesitation_or_uncertainty"
        if message.count('?') > 1:
            return "seeking_multiple_reassurances"
        if re.search(r'(ich|mir|mich).*(egal|gleichgültig)', message_lower):
            return "defensive_indifference"
        if re.search(r'(nicht|kein).*(wichtig|schlimm)', message_lower):
            return "minimizing_pain"

        return "surface_level"

    def _identify_emotional_triggers(self, message: str, context: str) -> List[str]:
        """Identifiziert emotionale Auslöser"""
        triggers = []
        combined_text = f"{message.lower()} {context.lower()}"

        for trigger_type, keywords in self.trigger_database.items():
            for keyword in keywords:
                if keyword in combined_text:
                    triggers.append(trigger_type)
                    break

        return triggers

    def _extract_psychological_needs(self, message: str, emotions: Dict[EmotionalState, float]) -> List[str]:
        """Extrahiert psychologische Bedürfnisse"""
        needs = []

        # Emotionsbasierte Bedürfnisse
        for emotion, strength in emotions.items():
            if strength > 2.0:  # Nur starke Emotionen
                if emotion in [EmotionalState.SADNESS, EmotionalState.FEAR]:
                    needs.extend(["comfort", "safety", "understanding"])
                elif emotion in [EmotionalState.ANGER, EmotionalState.FRUSTRATION]:
                    needs.extend(["validation", "justice", "being_heard"])
                elif emotion in [EmotionalState.JOY, EmotionalState.EXCITEMENT]:
                    needs.extend(["sharing", "celebration", "connection"])
                elif emotion in [EmotionalState.VULNERABLE, EmotionalState.ANXIETY]:
                    needs.extend(["protection", "reassurance", "stability"])
                elif emotion in [EmotionalState.LOVE, EmotionalState.AFFECTION]:
                    needs.extend(["closeness", "bonding", "acceptance"])

        return list(set(needs))  # Remove duplicates

    def _determine_primary_emotion(self, detected: Dict[EmotionalState, float],
                                   profile: EmotionalProfile) -> EmotionalState:
        """Bestimmt primäre Emotion unter Berücksichtigung des Character-Profils"""
        if not detected:
            return EmotionalState.NEUTRAL

        # Gewichte Emotionen basierend auf Character-Profil
        weighted_emotions = {}
        for emotion, score in detected.items():
            weight = 1.0

            # Verstärke dominante Emotionen des Characters
            if emotion in profile.dominant_emotions:
                weight += 0.5

            # Verstärke basierend auf Empathie-Level
            if emotion in [EmotionalState.EMPATHETIC, EmotionalState.CARING]:
                weight += profile.empathy_level * 0.3

            weighted_emotions[emotion] = score * weight

        return max(weighted_emotions.items(), key=lambda x: x[1])[0]

    def _identify_secondary_emotions(self, detected: Dict[EmotionalState, float],
                                     primary: EmotionalState) -> List[EmotionalState]:
        """Identifiziert sekundäre Emotionen"""
        secondary = []

        for emotion, score in detected.items():
            if emotion != primary and score > 1.5:
                secondary.append(emotion)

        return sorted(secondary, key=lambda e: detected[e], reverse=True)[:3]

    def _calculate_emotional_intensity(self, message: str, body_language: str,
                                       emotions: Dict[EmotionalState, float]) -> EmotionalIntensity:
        """Berechnet emotionale Intensität"""
        intensity_score = 0

        # Aus Emotionen
        if emotions:
            max_emotion_score = max(emotions.values())
            intensity_score += max_emotion_score

        # Aus Text-Indikatoren
        if re.search(r'[!]{2,}', message):
            intensity_score += 2
        if message.isupper():
            intensity_score += 3
        if re.search(r'(sehr|total|extrem|wahnsinnig|unglaublich)', message.lower()):
            intensity_score += 1

        # Aus Körpersprache
        if body_language:
            intense_indicators = ["zittert", "schluchzt", "schreit", "erstarrt", "zusammenbricht"]
            if any(indicator in body_language.lower() for indicator in intense_indicators):
                intensity_score += 2

        # Map zu Enum
        if intensity_score <= 1:
            return EmotionalIntensity.SUBTLE
        elif intensity_score <= 2.5:
            return EmotionalIntensity.MILD
        elif intensity_score <= 4:
            return EmotionalIntensity.MODERATE
        elif intensity_score <= 6:
            return EmotionalIntensity.STRONG
        else:
            return EmotionalIntensity.INTENSE

    def _determine_emotional_context(self, primary_emotion: EmotionalState,
                                     context: str, triggers: List[str]) -> EmotionalContext:
        """Bestimmt emotionalen Kontext"""

        # Trigger-basierte Kontexte
        if "trauma_triggers" in triggers:
            return EmotionalContext.VULNERABLE
        if "protection_triggers" in triggers:
            return EmotionalContext.PROTECTIVE
        if "bonding_triggers" in triggers:
            return EmotionalContext.INTIMATE
        if "comfort_triggers" in triggers:
            return EmotionalContext.COMFORTING

        # Emotions-basierte Kontexte
        if primary_emotion in [EmotionalState.PROTECTIVE, EmotionalState.CONCERN]:
            return EmotionalContext.PROTECTIVE
        elif primary_emotion in [EmotionalState.VULNERABLE, EmotionalState.FEAR]:
            return EmotionalContext.VULNERABLE
        elif primary_emotion in [EmotionalState.JOY, EmotionalState.EXCITEMENT]:
            return EmotionalContext.CELEBRATORY
        elif primary_emotion in [EmotionalState.CARING, EmotionalState.EMPATHETIC]:
            return EmotionalContext.SUPPORTIVE

        return EmotionalContext.SERIOUS

    def _calculate_analysis_confidence(self, emotions: Dict[EmotionalState, float],
                                       triggers: List[str], profile: EmotionalProfile) -> float:
        """Berechnet Konfidenz der Analyse"""

        confidence = 0.5  # Base confidence

        # Mehr Emotionen = höhere Konfidenz
        if len(emotions) >= 2:
            confidence += 0.2

        # Trigger gefunden = höhere Konfidenz
        if triggers:
            confidence += 0.2

        # Character-Profil Empathie-Level
        confidence += profile.emotional_sensitivity * 0.2

        return min(1.0, confidence)

    def _determine_temporal_focus(self, message: str) -> str:
        """Bestimmt zeitlichen Fokus"""

        past_indicators = ["war", "hatte", "damals", "früher", "erinnerung", "vergangene"]
        future_indicators = ["werde", "will", "später", "morgen", "angst vor", "hoffnung"]
        present_indicators = ["bin", "fühle", "jetzt", "gerade", "momentan"]

        message_lower = message.lower()

        past_count = sum(1 for word in past_indicators if word in message_lower)
        future_count = sum(1 for word in future_indicators if word in message_lower)
        present_count = sum(1 for word in present_indicators if word in message_lower)

        if past_count > max(present_count, future_count):
            return "past_focused"
        elif future_count > max(present_count, past_count):
            return "future_focused"
        else:
            return "present_focused"

    def generate_empathetic_response(self, analysis: EmotionalAnalysis,
                                     character_name: str) -> str:
        """Generiert empathische Antwort basierend auf Analysis"""

        if character_name not in self.character_profiles:
            character_name = "default"

        profile = self.character_profiles[character_name]

        # Character-spezifische Response-Generation
        response_components = []

        # Emotionale Validierung
        validation = self._generate_emotional_validation(analysis, profile)
        if validation:
            response_components.append(validation)

        # Empathische Reaktion
        empathy = self._generate_empathetic_reaction(analysis, profile)
        if empathy:
            response_components.append(empathy)

        # Unterstützung anbieten
        support = self._generate_support_offer(analysis, profile)
        if support:
            response_components.append(support)

        return " ".join(response_components)

    def _generate_emotional_validation(self, analysis: EmotionalAnalysis,
                                       profile: EmotionalProfile) -> str:
        """Generiert emotionale Validierung"""

        emotion = analysis.primary_emotion
        intensity = analysis.intensity

        validation_templates = {
            EmotionalState.SADNESS: [
                "*spürt deinen Schmerz*",
                "*sieht die Trauer in deinen Augen*",
                "*wird sofort aufmerksam bei deiner Traurigkeit*"
            ],
            EmotionalState.FEAR: [
                "*erkennt deine Angst sofort*",
                "*wird beschützend bei deiner Furcht*",
                "*spürt deine Unsicherheit*"
            ],
            EmotionalState.JOY: [
                "*lächelt bei deiner Freude*",
                "*wird warm bei deinem Glück*",
                "*freut sich mit dir*"
            ],
            EmotionalState.ANGER: [
                "*versteht deinen Ärger*",
                "*sieht deine Frustration*",
                "*nimmt deine Wut ernst*"
            ],
            EmotionalState.VULNERABLE: [
                "*erkennt deine Verletzlichkeit*",
                "*wird sanft bei deiner Offenheit*",
                "*spürt dass du Schutz brauchst*"
            ]
        }

        templates = validation_templates.get(emotion, ["*ist aufmerksam*"])

        # Verstärke basierend auf Character Empathie
        if profile.empathy_level > 0.8:
            base_template = random.choice(templates)
            return f"{base_template} mit hoher Empathie"

        return random.choice(templates)

    def _generate_empathetic_reaction(self, analysis: EmotionalAnalysis,
                                      profile: EmotionalProfile) -> str:
        """Generiert empathische Reaktion"""

        emotion = analysis.primary_emotion
        character = profile.character_name

        # Character-spezifische Reaktionen
        if character == "tsunade":
            if emotion in [EmotionalState.SADNESS, EmotionalState.FEAR, EmotionalState.VULNERABLE]:
                return "\"Komm her zu Mama. Ich bin da für dich.\""
            elif emotion == EmotionalState.JOY:
                return "\"Es macht mich so glücklich, dich glücklich zu sehen, mein kleiner Wolf.\""

        elif character == "hinata":
            if emotion in [EmotionalState.SADNESS, EmotionalState.VULNERABLE]:
                return "\"I-ich verstehe wie du dich fühlst... du bist nicht allein.\""

        elif character == "naruto":
            if emotion == EmotionalState.SADNESS:
                return "\"Hey, was ist los? Du weißt, du kannst mir alles erzählen, dattebayo!\""
            elif emotion == EmotionalState.JOY:
                return "\"Yeah! Es ist so cool dich glücklich zu sehen!\""

        # Fallback basierend auf Emotion
        empathy_responses = {
            EmotionalState.SADNESS: "\"Ich verstehe deinen Schmerz.\"",
            EmotionalState.FEAR: "\"Du bist sicher. Ich bin hier.\"",
            EmotionalState.JOY: "\"Deine Freude ist ansteckend.\"",
            EmotionalState.VULNERABLE: "\"Es ist mutig, das zu zeigen.\"",
            EmotionalState.ANGER: "\"Deine Gefühle sind berechtigt.\""
        }

        return empathy_responses.get(emotion, "\"Ich verstehe.\"")

    def _generate_support_offer(self, analysis: EmotionalAnalysis,
                                profile: EmotionalProfile) -> str:
        """Generiert Unterstützungsangebot"""

        needs = analysis.underlying_needs
        character = profile.character_name

        if not needs:
            return ""

        # Character-spezifische Unterstützung
        if character == "tsunade":
            if "comfort" in needs:
                return "*öffnet ihre Arme* \"Lass dich von Mama umarmen.\""
            elif "protection" in needs:
                return "\"Niemand wird dir jemals wieder weh tun. Das verspreche ich.\""

        elif character == "sakura":
            if "comfort" in needs:
                return "\"Möchtest du darüber reden? Ich höre zu.\""
            elif "safety" in needs:
                return "\"Du bist hier sicher. Lass mich dir helfen.\""

        # Allgemeine Unterstützung basierend auf Bedürfnissen
        support_offers = {
            "comfort": "\"Brauchst du eine Umarmung?\"",
            "safety": "\"Du bist hier sicher.\"",
            "understanding": "\"Ich verstehe dich.\"",
            "validation": "\"Deine Gefühle sind wichtig.\"",
            "protection": "\"Ich beschütze dich.\""
        }

        primary_need = needs[0] if needs else "understanding"
        return support_offers.get(primary_need, "\"Wie kann ich dir helfen?\"")

    def get_emotional_intelligence_summary(self, character_name: str) -> str:
        """Zeigt EI-Summary für Character"""

        if character_name not in self.character_profiles:
            return f"❌ Kein emotionales Profil für {character_name} gefunden."

        profile = self.character_profiles[character_name]

        summary = f"""💭 **EMOTIONAL INTELLIGENCE** für {character_name.title()}:

🧠 **Empathie-Fähigkeiten:**
• Empathie-Level: {profile.empathy_level:.1%}
• Emotionale Sensitivität: {profile.emotional_sensitivity:.1%}  
• Response-Authentizität: {profile.response_authenticity:.1%}

🎭 **Emotionale Präferenzen:**
• Dominante Emotionen: {', '.join([e.value for e in profile.dominant_emotions])}
• Komfort-Emotionen: {', '.join([e.value for e in profile.comfort_emotions])}
• Stress-Emotionen: {', '.join([e.value for e in profile.stress_emotions])}

📊 **Erkannte Emotionen**: {len(self.emotion_patterns)} verschiedene Emotionstypen
🔍 **Subtext-Muster**: {len(self.subtext_recognition)} erkannte Subtext-Patterns
⚡ **Trigger-Database**: {len(self.trigger_database)} Trigger-Kategorien"""

        return summary


def integrate_advanced_emotional_intelligence(game_data):
    """🔧 Integriert das Advanced Emotional Intelligence System"""

    # Erstelle Advanced EI System
    emotional_intelligence = AdvancedEmotionalIntelligence(game_data)
    game_data.advanced_emotional_intelligence = emotional_intelligence

    # Erweitere get_llm_response
    if hasattr(game_data, 'get_llm_response'):
        original_get_llm_response = game_data.get_llm_response

        def emotionally_intelligent_llm_response(user_input: str) -> str:
            """LLM Response mit Advanced Emotional Intelligence"""

            # Normale Response
            base_response = original_get_llm_response(user_input)

            # Current Character
            current_character = getattr(game_data, 'active_character', 'tsunade')
            current_location = getattr(game_data, 'current_location', 'konoha')

            # Emotionale Analyse
            emotional_analysis = emotional_intelligence.analyze_emotional_state(
                message=user_input,
                character_name=current_character,
                context=current_location
            )

            # Generiere empathische Response (20% Chance)
            if random.random() < 0.2 and emotional_analysis.confidence > 0.7:
                empathetic_response = emotional_intelligence.generate_empathetic_response(
                    emotional_analysis, current_character
                )

                if empathetic_response:
                    return f"{base_response}\n\n{empathetic_response}"

            return base_response

        game_data.get_llm_response = emotionally_intelligent_llm_response

    print("💭 ADVANCED EMOTIONAL INTELLIGENCE erfolgreich integriert!")
    print("🎯 Features aktiviert:")
    print(f"   • {len(emotional_intelligence.character_profiles)} Characters mit EI-Profilen")
    print(f"   • {len(emotional_intelligence.emotion_patterns)} Emotion-Erkennungspatterns")
    print(f"   • {len(emotional_intelligence.subtext_recognition)} Subtext-Erkennungsmuster")
    print("   • Claude Ultra-Level emotionale Intelligenz")
    print("   • Empathische Response-Generierung")

    return emotional_intelligence


if __name__ == "__main__":
    print("💭 ADVANCED EMOTIONAL INTELLIGENCE ENGINE")
    print("=========================================")
    print("✅ Vollständige Emotion-Liste implementiert")
    print("✅ Claude Ultra-Level emotionale Intelligenz")
    print("✅ Character-spezifische Empathie-Profile")
    print("✅ Erweiterte Subtext- und Trigger-Erkennung")
    print("✅ Empathische Response-Generierung")