# -*- coding: utf-8 -*-
"""
🧠 ADVANCED MEMORY & LEARNING SYSTEM - Claude Ultra Level
NPCs erinnern sich an ALLES und lernen aus jeder Interaktion
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import re


class MemoryType(Enum):
    """Arten von Erinnerungen"""
    CONVERSATION = "conversation"  # Gesprächs-Erinnerungen
    EMOTIONAL = "emotional"  # Emotionale Momente
    BEHAVIORAL = "behavioral"  # Verhaltens-Beobachtungen
    PREFERENCE = "preference"  # Vorlieben-Erkenntnisse
    ROUTINE = "routine"  # Gewohnheits-Muster
    RELATIONSHIP = "relationship"  # Beziehungs-Entwicklung
    TRAUMA = "trauma"  # Traumatische/wichtige Events
    ACHIEVEMENT = "achievement"  # Erfolge und Fortschritte


class EmotionalIntensity(Enum):
    """Intensität emotionaler Erinnerungen"""
    SUBTLE = 1  # Kaum merklich
    MILD = 2  # Leicht spürbar
    MODERATE = 3  # Deutlich erkennbar
    STRONG = 4  # Stark ausgeprägt
    INTENSE = 5  # Überwältigend


@dataclass
class Memory:
    """Eine einzelne Erinnerung mit emotionalem Kontext"""
    id: str
    character: str  # Wer erinnert sich
    memory_type: MemoryType
    content: str  # Was passiert ist
    emotional_context: str  # Emotionaler Zustand
    intensity: EmotionalIntensity  # Wie stark die Erinnerung ist
    participants: List[str]  # Wer war dabei
    location: str  # Wo es passiert ist
    timestamp: datetime

    # Lern-Aspekte
    learned_insights: List[str] = field(default_factory=list)  # Was gelernt wurde
    behavioral_changes: List[str] = field(default_factory=list)  # Verhaltensänderungen
    tags: List[str] = field(default_factory=list)  # Kategorisierung

    # Emotionale Metadaten
    sukuna_mood: str = "neutral"  # Sukunas Stimmung damals
    character_reaction: str = ""  # Wie der Charakter reagiert hat
    relationship_impact: int = 0  # Auswirkung auf Beziehung

    # Wiedererinnerung
    recall_count: int = 0  # Wie oft erinnert
    last_recalled: Optional[datetime] = None
    importance_score: float = 1.0  # Wie wichtig die Erinnerung ist


class EmotionalPattern:
    """Erkannte emotionale Muster über Zeit"""

    def __init__(self, pattern_name: str, triggers: List[str], responses: List[str]):
        self.pattern_name = pattern_name
        self.triggers = triggers  # Was löst das Muster aus
        self.responses = responses  # Wie reagiert Sukuna
        self.confidence = 0.0  # Wie sicher ist das Muster
        self.occurrences = 0  # Wie oft beobachtet
        self.last_seen = None  # Wann zuletzt gesehen


class AdvancedMemorySystem:
    """🧠 Hauptsystem für Advanced Memory & Learning"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.character_memories: Dict[str, List[Memory]] = {}
        self.emotional_patterns: Dict[str, List[EmotionalPattern]] = {}
        self.learning_insights: Dict[str, Dict[str, Any]] = {}

        # Memory-Einstellungen
        self.max_memories_per_character = 500
        self.memory_decay_days = 30
        self.importance_threshold = 2.0

        # Initialisiere für alle Charaktere
        self._initialize_character_memory_systems()

        # Lade emotionale Erkennungs-Muster
        self._initialize_emotional_recognition()

    def _initialize_character_memory_systems(self):
        """Initialisiert Memory-Systeme für alle Charaktere"""

        # Hole verfügbare Charaktere
        characters = self._get_available_characters()

        for character in characters:
            self.character_memories[character] = []
            self.emotional_patterns[character] = []
            self.learning_insights[character] = {
                "sukuna_preferences": {},
                "emotional_triggers": {},
                "behavior_patterns": {},
                "communication_style": {},
                "comfort_methods": [],
                "stress_indicators": [],
                "happiness_sources": []
            }

        print(f"🧠 Advanced Memory System initialisiert für {len(characters)} Charaktere")

    def _get_available_characters(self) -> List[str]:
        """Holt verfügbare Charaktere aus dem System"""
        characters = []

        if hasattr(self.game_data, 'relationship_system'):
            try:
                relationships = self.game_data.relationship_system.get_all_relationships()
                characters = list(relationships.keys())
            except:
                pass

        # Fallback
        if not characters:
            characters = ["tsunade", "naruto", "sasuke", "sakura", "kakashi", "kiba", "hinata",
                          "shino", "choji", "ino", "shikamaru", "lee", "tenten", "neji"]

        return characters

    def _initialize_emotional_recognition(self):
        """Initialisiert emotionale Erkennungs-Muster"""

        # Basis emotionale Muster für Erkennung
        self.emotional_keywords = {
            "happy": ["freut", "lacht", "fröhlich", "gut", "toll", "super", "yeah", "haha"],
            "sad": ["traurig", "schlecht", "weine", "weinen", "tränen", "schmerz", "verletzt"],
            "angry": ["wütend", "ärger", "sauer", "nervig", "dumm", "hasse", "schlecht"],
            "anxious": ["angst", "nervös", "sorge", "befürchte", "unsicher", "ängstlich"],
            "excited": ["aufgeregt", "kann nicht warten", "endlich", "yeah", "wow", "cool"],
            "lonely": ["allein", "einsam", "niemand", "verlassen", "isoliert"],
            "grateful": ["danke", "dankbar", "schätze", "toll von dir", "lieb"],
            "confused": ["verstehe nicht", "was", "wie", "warum", "verwirrt", "???"],
            "tired": ["müde", "erschöpft", "schlafen", "kaputt", "ausgeruht"],
            "stressed": ["stress", "zu viel", "überwältigt", "kann nicht", "hilfe"]
        }

        # Verhaltensmuster-Erkennungs-Templates
        self.behavior_patterns = {
            "affection_seeking": {
                "keywords": ["umarm", "kuschel", "nähe", "bei dir bleiben", "nicht allein"],
                "indicators": ["seeks_physical_comfort", "wants_attention", "needs_reassurance"]
            },
            "independence_asserting": {
                "keywords": ["allein machen", "selbst", "nicht helfen", "kann das", "will nicht"],
                "indicators": ["growing_confidence", "boundary_setting", "self_reliance"]
            },
            "curiosity_expressing": {
                "keywords": ["warum", "wie", "was ist", "erzähl", "erklär", "zeig"],
                "indicators": ["learning_mindset", "trust_building", "intellectual_growth"]
            }
        }

    def store_memory(self, character: str, user_message: str, ai_response: str,
                     context: Dict[str, Any]) -> Memory:
        """🧠 Speichert eine neue Erinnerung mit emotionalem Kontext"""

        if character not in self.character_memories:
            self.character_memories[character] = []

        # Analysiere emotionalen Kontext
        emotional_analysis = self._analyze_emotional_context(user_message, ai_response)

        # Erkenne Verhaltensmuster
        behavioral_insights = self._recognize_behavioral_patterns(user_message)

        # Bestimme Memory-Type
        memory_type = self._classify_memory_type(user_message, ai_response, emotional_analysis)

        # Bestimme Intensität
        intensity = self._calculate_emotional_intensity(emotional_analysis, user_message)

        # Erstelle Memory
        memory_id = f"{character}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        memory = Memory(
            id=memory_id,
            character=character,
            memory_type=memory_type,
            content=self._create_memory_summary(user_message, ai_response),
            emotional_context=emotional_analysis["primary_emotion"],
            intensity=intensity,
            participants=["sukuna", character],
            location=context.get("location", "unknown"),
            timestamp=datetime.now(),
            sukuna_mood=emotional_analysis["sukuna_mood"],
            character_reaction=ai_response[:100] + "..." if len(ai_response) > 100 else ai_response,
            relationship_impact=self._calculate_relationship_impact(emotional_analysis),
            tags=self._generate_memory_tags(user_message, ai_response, emotional_analysis)
        )

        # Füge Lern-Insights hinzu
        memory.learned_insights = self._extract_learning_insights(
            user_message, ai_response, emotional_analysis, behavioral_insights
        )

        # Speichere Memory
        self.character_memories[character].append(memory)

        # Update Emotional Patterns
        self._update_emotional_patterns(character, emotional_analysis, user_message)

        # Update Learning Insights
        self._update_learning_insights(character, memory)

        # Memory-Management (begrenze Anzahl)
        self._manage_memory_storage(character)

        print(f"🧠 Memory gespeichert für {character}: {memory_type.value} ({intensity.name})")
        return memory

    def _analyze_emotional_context(self, user_message: str, ai_response: str) -> Dict[str, Any]:
        """💭 Analysiert emotionalen Kontext einer Interaktion"""

        message_lower = user_message.lower()
        analysis = {
            "primary_emotion": "neutral",
            "secondary_emotions": [],
            "emotional_intensity": 0.0,
            "sukuna_mood": "neutral",
            "emotional_needs": [],
            "triggers_detected": []
        }

        # Erkenne Emotionen aus Keywords
        emotion_scores = {}
        for emotion, keywords in self.emotional_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                emotion_scores[emotion] = score

        if emotion_scores:
            # Primäre Emotion
            analysis["primary_emotion"] = max(emotion_scores, key=emotion_scores.get)
            analysis["emotional_intensity"] = max(emotion_scores.values()) / 3  # Normalisiere

            # Sekundäre Emotionen
            sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
            analysis["secondary_emotions"] = [emo for emo, score in sorted_emotions[1:3] if score > 0]

        # Sukuna's Stimmung basierend auf Message-Stil
        analysis["sukuna_mood"] = self._detect_sukuna_mood(user_message)

        # Emotionale Bedürfnisse erkennen
        analysis["emotional_needs"] = self._detect_emotional_needs(user_message)

        # Trigger-Worte
        analysis["triggers_detected"] = self._detect_emotional_triggers(user_message)

        return analysis

    def _detect_sukuna_mood(self, message: str) -> str:
        """Erkennt Sukunas Stimmung aus seiner Nachricht"""
        message_lower = message.lower()

        mood_indicators = {
            "excited": ["!", "wow", "cool", "yeah", "super", "toll"],
            "sad": ["...", "traurig", "schlecht", "nicht gut", "weine"],
            "angry": ["ärgerlich", "sauer", "nervig", "dumm", "hasse"],
            "curious": ["?", "warum", "wie", "was", "erzähl"],
            "affectionate": ["lieb", "danke", "schätze", "umarm", "kuschel"],
            "tired": ["müde", "schlafen", "kaputt", "ruhe"],
            "playful": ["hehe", "haha", "spaß", "spiel", "lustig"],
            "vulnerable": ["hilfe", "angst", "unsicher", "allein", "verloren"]
        }

        for mood, indicators in mood_indicators.items():
            if any(indicator in message_lower for indicator in indicators):
                return mood

        return "neutral"

    def _detect_emotional_needs(self, message: str) -> List[str]:
        """Erkennt emotionale Bedürfnisse aus der Nachricht"""
        message_lower = message.lower()
        needs = []

        need_patterns = {
            "comfort": ["tröst", "umarm", "bei dir", "allein", "angst"],
            "validation": ["bin ich", "was denkst", "meinung", "richtig", "gut gemacht"],
            "attention": ["schau", "hör zu", "wichtig", "beachte mich"],
            "understanding": ["versteh", "fühl mich", "niemand versteht"],
            "guidance": ["was soll", "hilf mir", "weiß nicht", "rat"],
            "connection": ["zusammen", "mit dir", "freunde", "verbindung"],
            "safety": ["sicher", "schutz", "gefahr", "beschütze"],
            "independence": ["allein", "selbst", "kann das", "will nicht hilfe", "du nervst"]
        }

        for need, patterns in need_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                needs.append(need)

        return needs

    def _detect_emotional_triggers(self, message: str) -> List[str]:
        """Erkennt emotionale Trigger in der Nachricht"""
        message_lower = message.lower()
        triggers = []

        trigger_patterns = {
            "abandonment": ["verlassen", "weggehen", "allein lassen", "nicht da"],
            "rejection": ["mag mich nicht", "will mich nicht", "ablehnung"],
            "criticism": ["falsch", "schlecht gemacht", "dumm", "versagt"],
            "past_trauma": ["damals", "früher", "erinnert mich", "wie damals"],
            "authority": ["muss ich", "befehl", "gehorchen", "folgen"],
            "intimacy": ["nähe", "vertrauen", "geheimnis", "privat"],
            "change": ["anders", "verändert", "nicht mehr", "früher war"]
        }

        for trigger, patterns in trigger_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                triggers.append(trigger)

        return triggers

    def _recognize_behavioral_patterns(self, message: str) -> Dict[str, Any]:
        """Erkennt Verhaltensmuster in der Nachricht"""
        message_lower = message.lower()
        patterns = {}

        for pattern_name, pattern_data in self.behavior_patterns.items():
            score = 0
            matched_keywords = []

            for keyword in pattern_data["keywords"]:
                if keyword in message_lower:
                    score += 1
                    matched_keywords.append(keyword)

            if score > 0:
                patterns[pattern_name] = {
                    "score": score,
                    "matched_keywords": matched_keywords,
                    "indicators": pattern_data["indicators"]
                }

        return patterns

    def _classify_memory_type(self, user_message: str, ai_response: str,
                              emotional_analysis: Dict) -> MemoryType:
        """Klassifiziert den Typ der Erinnerung"""

        message_lower = user_message.lower()
        intensity = emotional_analysis.get("emotional_intensity", 0)

        # Hohe emotionale Intensität = Trauma/Emotional Memory
        if intensity > 2.0:
            return MemoryType.EMOTIONAL

        # Verhaltensmuster-Keywords
        if any(word in message_lower for word in ["immer", "nie", "mag", "hasse", "liebe"]):
            return MemoryType.PREFERENCE

        # Routine-Keywords
        if any(word in message_lower for word in ["jeden tag", "immer wenn", "normalerweise"]):
            return MemoryType.ROUTINE

        # Beziehungs-Keywords
        if any(word in message_lower for word in ["freund", "familie", "beziehung", "vertrauen"]):
            return MemoryType.RELATIONSHIP

        # Achievement-Keywords
        if any(word in message_lower for word in ["geschafft", "stolz", "gelernt", "besser"]):
            return MemoryType.ACHIEVEMENT

        # Behavioral-Keywords
        if any(word in message_lower for word in ["verhalte", "mache", "tue", "gewohnheit"]):
            return MemoryType.BEHAVIORAL

        # Fallback
        return MemoryType.CONVERSATION

    def _calculate_emotional_intensity(self, emotional_analysis: Dict,
                                       message: str) -> EmotionalIntensity:
        """Berechnet emotionale Intensität"""

        base_intensity = emotional_analysis.get("emotional_intensity", 0)

        # Intensitäts-Indikatoren
        intensity_boosters = ["!!!", "sehr", "total", "komplett", "extrem", "richtig"]
        message_lower = message.lower()

        boosters = sum(1 for booster in intensity_boosters if booster in message_lower)
        final_intensity = base_intensity + (boosters * 0.5)

        if final_intensity >= 4.0:
            return EmotionalIntensity.INTENSE
        elif final_intensity >= 3.0:
            return EmotionalIntensity.STRONG
        elif final_intensity >= 2.0:
            return EmotionalIntensity.MODERATE
        elif final_intensity >= 1.0:
            return EmotionalIntensity.MILD
        else:
            return EmotionalIntensity.SUBTLE

    def _create_memory_summary(self, user_message: str, ai_response: str) -> str:
        """Erstellt eine Zusammenfassung der Interaktion"""
        return f"Sukuna: {user_message[:100]}{'...' if len(user_message) > 100 else ''}"

    def _calculate_relationship_impact(self, emotional_analysis: Dict) -> int:
        """Berechnet Auswirkung auf Beziehung"""
        primary_emotion = emotional_analysis.get("primary_emotion", "neutral")
        intensity = emotional_analysis.get("emotional_intensity", 0)

        emotion_impacts = {
            "happy": 2, "grateful": 3, "excited": 1, "affectionate": 3,
            "sad": 1, "angry": -2, "anxious": 1, "confused": 0,
            "lonely": 2, "tired": 0, "stressed": 1
        }

        base_impact = emotion_impacts.get(primary_emotion, 0)
        return int(base_impact * (1 + intensity))

    def _generate_memory_tags(self, user_message: str, ai_response: str,
                              emotional_analysis: Dict) -> List[str]:
        """Generiert Tags für die Erinnerung"""
        tags = []

        # Emotionale Tags
        tags.append(f"emotion:{emotional_analysis.get('primary_emotion', 'neutral')}")

        # Content Tags
        message_lower = user_message.lower()
        tag_keywords = {
            "food": ["essen", "hunger", "restaurant", "kochen"],
            "training": ["training", "stark", "kämpfen", "übung"],
            "family": ["familie", "mutter", "vater", "geschwister"],
            "friends": ["freund", "zusammen", "team", "gruppe"],
            "comfort": ["umarm", "tröst", "kuschel", "beruhig"],
            "questions": ["warum", "wie", "was", "?"],
            "activities": ["gehen", "machen", "spielen", "besuchen"]
        }

        for tag, keywords in tag_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                tags.append(f"topic:{tag}")

        # Beziehungs-Tags
        if emotional_analysis.get("emotional_intensity", 0) > 1.5:
            tags.append("important")

        return tags

    def _extract_learning_insights(self, user_message: str, ai_response: str,
                                   emotional_analysis: Dict, behavioral_insights: Dict) -> List[str]:
        """Extrahiert Lern-Insights aus der Interaktion"""
        insights = []

        message_lower = user_message.lower()
        primary_emotion = emotional_analysis.get("primary_emotion", "neutral")

        # Präferenz-Insights
        if "mag" in message_lower or "liebe" in message_lower:
            insights.append(f"sukuna_likes: {self._extract_preference(user_message, True)}")
        elif "mag nicht" in message_lower or "hasse" in message_lower:
            insights.append(f"sukuna_dislikes: {self._extract_preference(user_message, False)}")

        # Emotionale Trigger-Insights
        if primary_emotion in ["sad", "angry", "anxious"]:
            trigger_context = self._extract_trigger_context(user_message)
            if trigger_context:
                insights.append(f"emotional_trigger: {trigger_context}")

        # Comfort-Method-Insights
        if primary_emotion in ["sad", "anxious", "stressed"]:
            comfort_response = self._analyze_comfort_effectiveness(ai_response)
            if comfort_response:
                insights.append(f"effective_comfort: {comfort_response}")

        # Verhaltensmuster-Insights
        for pattern_name, pattern_data in behavioral_insights.items():
            insights.append(f"behavior_pattern: {pattern_name} - {pattern_data['score']} intensity")

        return insights

    def _extract_preference(self, message: str, is_positive: bool) -> str:
        """Extrahiert Präferenz aus Nachricht"""
        # Vereinfachte Extraktion - könnte mit NLP verbessert werden
        words = message.split()
        preference_words = []

        trigger_words = ["mag", "liebe", "hasse", "mag nicht"] if is_positive else ["hasse", "mag nicht"]

        for i, word in enumerate(words):
            if any(trigger in word.lower() for trigger in trigger_words):
                # Nehme die nächsten 2-3 Worte als Präferenz
                preference_words = words[i + 1:i + 4]
                break

        return " ".join(preference_words) if preference_words else "unknown"

    def _extract_trigger_context(self, message: str) -> str:
        """Extrahiert Kontext eines emotionalen Triggers"""
        # Vereinfachte Kontextextraktion
        return message[:50] + "..." if len(message) > 50 else message

    def _analyze_comfort_effectiveness(self, ai_response: str) -> str:
        """Analysiert Effektivität einer Trost-Antwort"""
        response_lower = ai_response.lower()

        comfort_methods = {
            "physical": ["umarm", "streichel", "hand", "nah", "kuschel"],
            "verbal": ["verstehe", "okay", "da", "höre", "reden"],
            "protective": ["schutz", "sicher", "beschütze", "nichts passiert"],
            "validating": ["recht", "normal", "verstehen", "okay"],
            "distracting": ["machen wir", "gehen", "spiel", "anders"]
        }

        detected_methods = []
        for method, keywords in comfort_methods.items():
            if any(keyword in response_lower for keyword in keywords):
                detected_methods.append(method)

        return ", ".join(detected_methods) if detected_methods else "general_support"

    def _update_emotional_patterns(self, character: str, emotional_analysis: Dict,
                                   user_message: str):
        """Updated emotionale Muster für Charakter"""

        primary_emotion = emotional_analysis.get("primary_emotion", "neutral")
        triggers = emotional_analysis.get("triggers_detected", [])

        if character not in self.emotional_patterns:
            self.emotional_patterns[character] = []

        # Suche oder erstelle Muster
        for trigger in triggers:
            pattern = self._find_or_create_pattern(character, trigger, primary_emotion)
            pattern.occurrences += 1
            pattern.last_seen = datetime.now()
            pattern.confidence = min(1.0, pattern.occurrences / 10)  # Max confidence bei 10 occurrences

    def _find_or_create_pattern(self, character: str, trigger: str,
                                emotion: str) -> EmotionalPattern:
        """Findet oder erstellt emotionales Muster"""

        for pattern in self.emotional_patterns[character]:
            if pattern.pattern_name == f"{trigger}_to_{emotion}":
                return pattern

        # Erstelle neues Muster
        new_pattern = EmotionalPattern(
            pattern_name=f"{trigger}_to_{emotion}",
            triggers=[trigger],
            responses=[emotion],
        )

        self.emotional_patterns[character].append(new_pattern)
        return new_pattern

    def _update_learning_insights(self, character: str, memory: Memory):
        """Aktualisiert Lern-Insights für Charakter"""

        if character not in self.learning_insights:
            return

        insights = self.learning_insights[character]

        # Update basierend auf Memory-Insights
        for insight in memory.learned_insights:
            if insight.startswith("sukuna_likes:"):
                preference = insight.split(":")[1].strip()
                insights["sukuna_preferences"][preference] = "positive"
            elif insight.startswith("sukuna_dislikes:"):
                preference = insight.split(":")[1].strip()
                insights["sukuna_preferences"][preference] = "negative"
            elif insight.startswith("emotional_trigger:"):
                trigger = insight.split(":")[1].strip()
                insights["emotional_triggers"][trigger] = insights["emotional_triggers"].get(trigger, 0) + 1
            elif insight.startswith("effective_comfort:"):
                method = insight.split(":")[1].strip()
                insights["comfort_methods"].append(method)

    def _manage_memory_storage(self, character: str):
        """Verwaltet Memory-Speicher (entfernt alte/unwichtige Memories)"""

        if len(self.character_memories[character]) <= self.max_memories_per_character:
            return

        memories = self.character_memories[character]

        # Sortiere nach Wichtigkeit (Intensität + Häufigkeit der Erinnerung)
        memories.sort(key=lambda m: (m.intensity.value + m.recall_count), reverse=True)

        # Behalte die wichtigsten Memories
        self.character_memories[character] = memories[:self.max_memories_per_character]

        print(f"🧠 Memory-Management für {character}: {len(memories)} → {self.max_memories_per_character}")

    def recall_relevant_memories(self, character: str, current_context: str,
                                 limit: int = 5) -> List[Memory]:
        """🧠 Ruft relevante Erinnerungen für aktuellen Kontext ab"""

        if character not in self.character_memories:
            return []

        memories = self.character_memories[character]
        current_context_lower = current_context.lower()

        # Bewerte Relevanz jeder Erinnerung
        memory_scores = []
        for memory in memories:
            score = self._calculate_memory_relevance(memory, current_context_lower)
            if score > 0:
                memory_scores.append((memory, score))

        # Sortiere nach Relevanz
        memory_scores.sort(key=lambda x: x[1], reverse=True)

        # Aktualisiere Recall-Statistiken
        relevant_memories = []
        for memory, score in memory_scores[:limit]:
            memory.recall_count += 1
            memory.last_recalled = datetime.now()
            relevant_memories.append(memory)

        return relevant_memories

    def _calculate_memory_relevance(self, memory: Memory, current_context: str) -> float:
        """Berechnet Relevanz einer Erinnerung für aktuellen Kontext"""

        score = 0.0
        memory_content_lower = memory.content.lower()

        # Keyword-Übereinstimmung
        context_words = current_context.split()
        memory_words = memory_content_lower.split()

        common_words = set(context_words) & set(memory_words)
        score += len(common_words) * 0.5

        # Tag-Übereinstimmung
        for tag in memory.tags:
            if any(word in current_context for word in tag.split(":")):
                score += 1.0

        # Emotionale Ähnlichkeit
        current_emotion = self._detect_sukuna_mood(current_context)
        if current_emotion == memory.sukuna_mood:
            score += 2.0

        # Intensitäts-Bonus (wichtige Memories sind relevanter)
        score += memory.intensity.value * 0.3

        # Zeitlicher Decay (neuere Memories relevanter)
        days_ago = (datetime.now() - memory.timestamp).days
        decay_factor = max(0.1, 1.0 - (days_ago / self.memory_decay_days))
        score *= decay_factor

        return score

    def generate_memory_enhanced_response(self, character: str, user_message: str,
                                          base_response: str) -> str:
        """🧠 Generiert Memory-enhanced Antwort"""

        # Hole relevante Erinnerungen
        relevant_memories = self.recall_relevant_memories(character, user_message, limit=3)

        if not relevant_memories:
            return base_response

        # Analysiere Lern-Insights für den Charakter
        insights = self.learning_insights.get(character, {})

        # Generiere Memory-Referenzen
        memory_additions = []

        for memory in relevant_memories:
            if memory.memory_type == MemoryType.EMOTIONAL and memory.intensity.value >= 3:
                # Starke emotionale Erinnerung
                memory_additions.append(self._create_emotional_memory_reference(memory))

            elif memory.memory_type == MemoryType.PREFERENCE:
                # Präferenz-Erinnerung
                memory_additions.append(self._create_preference_memory_reference(memory, insights))

            elif memory.memory_type == MemoryType.BEHAVIORAL:
                # Verhaltens-Erinnerung
                memory_additions.append(self._create_behavioral_memory_reference(memory))

        # Kombiniere mit base response
        if memory_additions:
            enhanced_response = base_response

            # Füge Memory-Referenz subtil hinzu
            memory_text = random.choice(memory_additions)
            enhanced_response += f"\n\n{memory_text}"

            return enhanced_response

        return base_response

    def _create_emotional_memory_reference(self, memory: Memory) -> str:
        """Erstellt Referenz auf emotionale Erinnerung"""

        references = [
            f"*erinnert sich* Letztes Mal warst du auch {memory.sukuna_mood}...",
            f"*nachdenklich* Das erinnert mich an neulich, als du...",
            f"Ich merke, dass du dich genauso fühlst wie {self._format_memory_time(memory.timestamp)}."
        ]

        return random.choice(references)

    def _create_preference_memory_reference(self, memory: Memory,
                                            insights: Dict[str, Any]) -> str:
        """Erstellt Referenz auf Präferenz-Erinnerung"""

        preferences = insights.get("sukuna_preferences", {})

        if preferences:
            positive_prefs = [k for k, v in preferences.items() if v == "positive"]
            negative_prefs = [k for k, v in preferences.items() if v == "negative"]

            references = []

            if positive_prefs:
                pref = random.choice(positive_prefs)
                references.append(f"*lächelt wissend* Du magst {pref}, das habe ich mir gemerkt.")

            if negative_prefs:
                pref = random.choice(negative_prefs)
                references.append(f"Ich weiß, du magst {pref} nicht. Keine Sorge.")

            if references:
                return random.choice(references)

        return "*hat sich deine Vorlieben gemerkt*"

    def _create_behavioral_memory_reference(self, memory: Memory) -> str:
        """Erstellt Referenz auf Verhaltens-Erinnerung"""

        references = [
            f"*bemerkt dein Verhalten* Du machst das immer, wenn...",
            f"*verständnisvoll* Ich kenne diesen Blick schon...",
            f"*aufmerksam* Das ist typisch für dich, nicht wahr?"
        ]

        return random.choice(references)

    def _format_memory_time(self, timestamp: datetime) -> str:
        """Formatiert Zeitangabe für Memory-Referenz"""

        days_ago = (datetime.now() - timestamp).days

        if days_ago == 0:
            return "heute"
        elif days_ago == 1:
            return "gestern"
        elif days_ago < 7:
            return f"vor {days_ago} Tagen"
        elif days_ago < 30:
            weeks = days_ago // 7
            return f"vor {weeks} Woche{'n' if weeks > 1 else ''}"
        else:
            return "neulich"

    def get_character_insights_summary(self, character: str) -> str:
        """📊 Gibt Zusammenfassung der Charakter-Insights zurück"""

        if character not in self.learning_insights:
            return f"❌ Keine Insights für {character} verfügbar."

        insights = self.learning_insights[character]
        memory_count = len(self.character_memories.get(character, []))

        summary = f"🧠 **MEMORY INSIGHTS: {character.title()}**\n\n"
        summary += f"📚 **Erinnerungen**: {memory_count}\n\n"

        # Sukuna's Präferenzen
        preferences = insights.get("sukuna_preferences", {})
        if preferences:
            positive = [k for k, v in preferences.items() if v == "positive"]
            negative = [k for k, v in preferences.items() if v == "negative"]

            if positive:
                summary += f"✅ **Sukuna mag**: {', '.join(positive[:5])}\n"
            if negative:
                summary += f"❌ **Sukuna mag nicht**: {', '.join(negative[:3])}\n"

        # Emotionale Trigger
        triggers = insights.get("emotional_triggers", {})
        if triggers:
            top_triggers = sorted(triggers.items(), key=lambda x: x[1], reverse=True)[:3]
            summary += f"⚡ **Emotionale Trigger**: {', '.join([t[0] for t in top_triggers])}\n"

        # Comfort-Methods
        comfort_methods = insights.get("comfort_methods", [])
        if comfort_methods:
            unique_methods = list(set(comfort_methods))[:3]
            summary += f"💝 **Effektive Trost-Methoden**: {', '.join(unique_methods)}\n"

        return summary

    def save_memory_data(self) -> Dict[str, Any]:
        """💾 Speichert Memory-System Daten"""

        # Konvertiere Memories zu Dict
        memories_data = {}
        for character, memories in self.character_memories.items():
            memories_data[character] = [asdict(memory) for memory in memories]

        # Konvertiere Emotional Patterns
        patterns_data = {}
        for character, patterns in self.emotional_patterns.items():
            patterns_data[character] = [asdict(pattern) for pattern in patterns]

        return {
            "character_memories": memories_data,
            "emotional_patterns": patterns_data,
            "learning_insights": self.learning_insights,
            "system_settings": {
                "max_memories_per_character": self.max_memories_per_character,
                "memory_decay_days": self.memory_decay_days,
                "importance_threshold": self.importance_threshold
            }
        }

    def load_memory_data(self, data: Dict[str, Any]):
        """📂 Lädt Memory-System Daten"""

        # Lade Memories
        if "character_memories" in data:
            for character, memories_data in data["character_memories"].items():
                memories = []
                for memory_data in memories_data:
                    # Konvertiere Enums zurück
                    memory_data["memory_type"] = MemoryType(memory_data["memory_type"])
                    memory_data["intensity"] = EmotionalIntensity(memory_data["intensity"])

                    # Konvertiere Timestamps
                    memory_data["timestamp"] = datetime.fromisoformat(memory_data["timestamp"])
                    if memory_data.get("last_recalled"):
                        memory_data["last_recalled"] = datetime.fromisoformat(memory_data["last_recalled"])

                    memories.append(Memory(**memory_data))

                self.character_memories[character] = memories

        # Lade Insights
        if "learning_insights" in data:
            self.learning_insights = data["learning_insights"]

        # Lade Settings
        if "system_settings" in data:
            settings = data["system_settings"]
            self.max_memories_per_character = settings.get("max_memories_per_character", 500)
            self.memory_decay_days = settings.get("memory_decay_days", 30)
            self.importance_threshold = settings.get("importance_threshold", 2.0)


def integrate_advanced_memory_system(game_data):
    """🧠 Integriert das Advanced Memory System"""

    # Erstelle Advanced Memory System
    memory_system = AdvancedMemorySystem(game_data)
    game_data.advanced_memory_system = memory_system

    # Erweitere get_llm_response für Memory-Integration
    if hasattr(game_data, 'get_llm_response'):
        original_get_llm_response = game_data.get_llm_response

        def memory_enhanced_llm_response(user_input: str) -> str:
            """LLM Response mit Memory-Enhancement"""

            # Normale Response generieren
            base_response = original_get_llm_response(user_input)

            # Current character bestimmen
            current_character = getattr(game_data, 'active_character', 'tsunade')

            # Memory-Context für Response
            context = {
                'location': getattr(game_data, 'current_location', 'konoha'),
                'current_character': current_character
            }

            # Speichere Memory
            memory_system.store_memory(current_character, user_input, base_response, context)

            # Generiere Memory-enhanced Response
            enhanced_response = memory_system.generate_memory_enhanced_response(
                current_character, user_input, base_response
            )

            return enhanced_response

        # Ersetze Methode
        game_data.get_llm_response = memory_enhanced_llm_response

    print("🧠 ADVANCED MEMORY SYSTEM erfolgreich integriert!")
    print("🎯 Features aktiviert:")
    print("   • Alle Interaktionen werden erinnert")
    print("   • Emotionale Kontexte werden analysiert")
    print("   • Verhaltensmuster werden erkannt")
    print("   • NPCs lernen Sukunas Präferenzen")
    print("   • Memory-basierte Antworten")

    return memory_system


if __name__ == "__main__":
    print("🧠 ADVANCED MEMORY & LEARNING SYSTEM")
    print("=============================================")
    print("✅ Totale Erinnerungs-Persistenz")
    print("✅ Emotionale Kontext-Analyse")
    print("✅ Verhaltens-Muster-Erkennung")
    print("✅ Adaptive Lern-Algorithmen")
    print("✅ Memory-enhanced AI-Antworten")