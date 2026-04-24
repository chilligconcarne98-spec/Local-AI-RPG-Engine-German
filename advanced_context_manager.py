# -*- coding: utf-8 -*-
"""
ERWEITERTE KONTEXTUALISIERUNG
Tiefe Analyse von Gesprächsverläufen, Emotionen und versteckten Bedeutungen
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics


@dataclass
class ConversationTurn:
    """Einzelner Gesprächszug mit Metadaten"""
    timestamp: datetime
    speaker: str
    message: str
    emotional_tone: str
    topics: List[str]
    intent: str
    subtext: Dict[str, Any]
    response_quality: float = 0.0
    memory_significance: float = 0.0


@dataclass
class EmotionalPattern:
    """Emotionales Muster über Zeit"""
    emotion: str
    intensity: float
    duration: int  # in Turns
    triggers: List[str]
    resolution: Optional[str] = None


@dataclass
class ConversationMemory:
    """Langzeit-Gesprächsgedächtnis"""
    significant_moments: List[ConversationTurn] = field(default_factory=list)
    emotional_history: List[EmotionalPattern] = field(default_factory=list)
    recurring_themes: Dict[str, int] = field(default_factory=dict)
    relationship_milestones: List[Dict] = field(default_factory=list)
    learned_preferences: Dict[str, float] = field(default_factory=dict)


class AdvancedContextManager:
    """
    🧠 Erweiterte Kontextualisierung für tiefere Gesprächsanalyse
    """

    def __init__(self, max_context_turns: int = 50):
        self.max_context_turns = max_context_turns
        self.conversation_history = deque(maxlen=max_context_turns)
        self.memory = ConversationMemory()

        # Analysesysteme
        self.emotion_analyzer = EmotionAnalyzer()
        self.topic_extractor = TopicExtractor()
        self.intent_classifier = IntentClassifier()
        self.subtext_analyzer = SubtextAnalyzer()
        self.pattern_detector = PatternDetector()

        # Kontext-Gewichtungen
        self.context_weights = {
            'recent': 1.0,  # Letzte 3 Turns
            'session': 0.7,  # Aktuelle Session
            'emotional': 0.9,  # Emotionale Momente
            'significant': 0.8,  # Bedeutsame Ereignisse
            'recurring': 0.6  # Wiederkehrende Themen
        }

        print("✅ Erweiterte Kontextualisierung initialisiert")

    def add_conversation_turn(self, speaker: str, message: str,
                              response_quality: float = 0.0) -> ConversationTurn:
        """
        Fügt einen neuen Gesprächszug hinzu und analysiert ihn
        """

        # Analysiere den Turn
        emotional_tone = self.emotion_analyzer.analyze_emotion(message)
        topics = self.topic_extractor.extract_topics(message)
        intent = self.intent_classifier.classify_intent(message, self.conversation_history)
        subtext = self.subtext_analyzer.analyze_subtext(message, self.conversation_history)

        # Erstelle Conversation Turn
        turn = ConversationTurn(
            timestamp=datetime.now(),
            speaker=speaker,
            message=message,
            emotional_tone=emotional_tone,
            topics=topics,
            intent=intent,
            subtext=subtext,
            response_quality=response_quality
        )

        # Berechne Memory Significance
        turn.memory_significance = self._calculate_memory_significance(turn)

        # Füge zu History hinzu
        self.conversation_history.append(turn)

        # Aktualisiere Langzeitgedächtnis wenn signifikant
        if turn.memory_significance > 0.7:
            self._update_longterm_memory(turn)

        # Erkenne Muster
        self._detect_conversation_patterns()

        return turn

    def get_contextual_analysis(self, character: str) -> Dict[str, Any]:
        """
        Liefert umfassende Kontextanalyse für Charakterreaktion
        """

        analysis = {
            'current_context': self._analyze_current_context(),
            'emotional_state': self._analyze_emotional_state(),
            'conversation_flow': self._analyze_conversation_flow(),
            'relationship_dynamics': self._analyze_relationship_dynamics(),
            'memory_relevance': self._get_relevant_memories(),
            'predictive_insights': self._generate_predictive_insights(),
            'character_adaptation': self._suggest_character_adaptation(character)
        }

        return analysis

    def _calculate_memory_significance(self, turn: ConversationTurn) -> float:
        """Berechnet wie bedeutsam ein Turn für das Langzeitgedächtnis ist"""

        significance = 0.1  # Basis-Signifikanz

        # Emotionale Intensität
        emotion_weights = {
            'joy': 0.7, 'sadness': 0.8, 'anger': 0.6, 'fear': 0.8,
            'surprise': 0.5, 'love': 0.9, 'trust': 0.7, 'anxiety': 0.8
        }
        significance += emotion_weights.get(turn.emotional_tone, 0.3)

        # Intent-basierte Signifikanz
        intent_weights = {
            'seeking_comfort': 0.8, 'sharing_vulnerability': 0.9,
            'expressing_gratitude': 0.7, 'asking_guidance': 0.6,
            'sharing_joy': 0.7, 'confessing_feelings': 0.9
        }
        significance += intent_weights.get(turn.intent, 0.2)

        # Subtext-Komplexität
        if turn.subtext.get('hidden_emotions'):
            significance += 0.3
        if turn.subtext.get('relationship_progression'):
            significance += 0.4

        # Themen-Relevanz
        important_topics = ['family', 'medical', 'personal_growth', 'trauma', 'dreams']
        if any(topic in important_topics for topic in turn.topics):
            significance += 0.3

        return min(significance, 1.0)

    def _analyze_current_context(self) -> Dict[str, Any]:
        """Analysiert den aktuellen Gesprächskontext (letzte 3-5 Turns)"""

        if not self.conversation_history:
            return {'status': 'no_context'}

        recent_turns = list(self.conversation_history)[-5:]

        return {
            'dominant_emotion': self._get_dominant_emotion(recent_turns),
            'conversation_momentum': self._calculate_momentum(recent_turns),
            'topic_coherence': self._analyze_topic_coherence(recent_turns),
            'engagement_level': self._measure_engagement_level(recent_turns),
            'emotional_trajectory': self._track_emotional_trajectory(recent_turns),
            'conversation_depth': self._measure_conversation_depth(recent_turns)
        }

    def _get_dominant_emotion(self, turns: List[ConversationTurn]) -> str:
        """Bestimmt dominante Emotion in den letzten Turns"""
        emotions = [turn.emotional_tone for turn in turns if turn.emotional_tone != 'neutral']
        if not emotions:
            return 'neutral'

        # Zähle Emotionen mit Gewichtung (neuere Turns wichtiger)
        emotion_weights = defaultdict(float)
        for i, emotion in enumerate(emotions):
            weight = 1.0 + (i * 0.2)  # Neuere Turns bekommen höheres Gewicht
            emotion_weights[emotion] += weight

        return max(emotion_weights.items(), key=lambda x: x[1])[0] if emotion_weights else 'neutral'

    def _calculate_momentum(self, turns: List[ConversationTurn]) -> str:
        """Berechnet Gesprächsmomentum"""
        if len(turns) < 2:
            return 'initializing'

        # Analysiere Länge und Komplexität der Nachrichten
        lengths = [len(turn.message.split()) for turn in turns]

        if len(lengths) >= 2:
            recent_trend = lengths[-1] - lengths[-2]
            if recent_trend > 5:
                return 'increasing'
            elif recent_trend < -5:
                return 'decreasing'

        return 'stable'

    def _analyze_topic_coherence(self, turns: List[ConversationTurn]) -> float:
        """Analysiert Themenkohärenz"""
        if len(turns) < 2:
            return 1.0

        all_topics = []
        for turn in turns:
            all_topics.extend(turn.topics)

        if not all_topics:
            return 0.5

        # Berechne Wiederholungsrate von Themen
        topic_counts = defaultdict(int)
        for topic in all_topics:
            topic_counts[topic] += 1

        repeated_topics = sum(1 for count in topic_counts.values() if count > 1)
        coherence = repeated_topics / len(set(all_topics)) if all_topics else 0.5

        return min(coherence, 1.0)

    def _measure_engagement_level(self, turns: List[ConversationTurn]) -> str:
        """Misst Engagement-Level"""
        if not turns:
            return 'unknown'

        # Faktoren für Engagement
        avg_length = sum(len(turn.message.split()) for turn in turns) / len(turns)
        question_count = sum(1 for turn in turns if '?' in turn.message)
        emotional_turns = sum(1 for turn in turns if turn.emotional_tone != 'neutral')

        engagement_score = 0
        if avg_length > 15:
            engagement_score += 1
        if question_count > 0:
            engagement_score += 1
        if emotional_turns / len(turns) > 0.3:
            engagement_score += 1

        if engagement_score >= 2:
            return 'high'
        elif engagement_score == 1:
            return 'medium'
        else:
            return 'low'

    def _track_emotional_trajectory(self, turns: List[ConversationTurn]) -> str:
        """Trackt emotionale Entwicklung"""
        emotions = [turn.emotional_tone for turn in turns]

        if len(emotions) < 2:
            return 'stable'

        # Vereinfachte Emotionsgewichtung
        emotion_values = {
            'joy': 3, 'love': 3, 'trust': 2,
            'neutral': 0,
            'sadness': -2, 'anger': -2, 'fear': -3, 'anxiety': -2
        }

        values = [emotion_values.get(emotion, 0) for emotion in emotions]

        if len(values) >= 2:
            trend = values[-1] - values[0]
            if trend > 1:
                return 'improving'
            elif trend < -1:
                return 'declining'

        return 'stable'

    def _measure_conversation_depth(self, turns: List[ConversationTurn]) -> str:
        """Misst Gesprächstiefe"""
        if not turns:
            return 'surface'

        depth_indicators = 0

        for turn in turns:
            # Persönliche Themen
            if any(topic in ['family', 'personal', 'emotional'] for topic in turn.topics):
                depth_indicators += 1

            # Vulnerable Intents
            if turn.intent in ['seeking_comfort', 'sharing_vulnerability']:
                depth_indicators += 1

            # Subtext vorhanden
            if turn.subtext.get('hidden_emotions') or turn.subtext.get('unspoken_needs'):
                depth_indicators += 1

        depth_ratio = depth_indicators / (len(turns) * 3)  # 3 mögliche Indikatoren pro Turn

        if depth_ratio > 0.6:
            return 'deep'
        elif depth_ratio > 0.3:
            return 'moderate'
        else:
            return 'surface'

    def _analyze_emotional_state(self) -> Dict[str, Any]:
        """Tiefe Analyse des emotionalen Zustands"""

        if not self.conversation_history:
            return {'state': 'neutral'}

        recent_turns = list(self.conversation_history)[-10:]

        return {
            'primary_emotion': self._get_dominant_emotion(recent_turns),
            'emotional_stability': self._calculate_emotional_stability(recent_turns),
            'intensity_trend': self._analyze_intensity_trend(recent_turns),
            'emotional_needs': self._identify_emotional_needs(recent_turns),
            'support_requirements': self._assess_support_needs(recent_turns)
        }

    def _calculate_emotional_stability(self, turns: List[ConversationTurn]) -> str:
        """Berechnet emotionale Stabilität"""
        if len(turns) < 3:
            return 'unknown'

        emotions = [turn.emotional_tone for turn in turns]
        unique_emotions = len(set(emotions))

        if unique_emotions <= 2:
            return 'stable'
        elif unique_emotions <= 4:
            return 'moderate'
        else:
            return 'unstable'

    def _analyze_intensity_trend(self, turns: List[ConversationTurn]) -> str:
        """Analysiert Intensitätstrend"""
        if not turns:
            return 'stable'

        # Grobe Intensitätsschätzung basierend auf Satzzeichen und Wortlänge
        intensities = []
        for turn in turns:
            intensity = 0.3  # Basis
            intensity += turn.message.count('!') * 0.2
            intensity += turn.message.count('?') * 0.1
            if any(word in turn.message.lower() for word in ['sehr', 'extrem', 'total']):
                intensity += 0.3
            intensities.append(min(intensity, 1.0))

        if len(intensities) >= 2:
            trend = intensities[-1] - intensities[0]
            if trend > 0.2:
                return 'increasing'
            elif trend < -0.2:
                return 'decreasing'

        return 'stable'

    def _identify_emotional_needs(self, turns: List[ConversationTurn]) -> List[str]:
        """Identifiziert emotionale Bedürfnisse"""
        needs = []

        for turn in turns:
            if turn.intent == 'seeking_comfort':
                needs.append('comfort_and_support')
            elif turn.intent == 'sharing_vulnerability':
                needs.append('emotional_validation')
            elif turn.emotional_tone in ['sadness', 'anxiety']:
                needs.append('reassurance')
            elif turn.emotional_tone == 'joy':
                needs.append('shared_celebration')

        return list(set(needs))

    def _assess_support_needs(self, turns: List[ConversationTurn]) -> str:
        """Bewertet Unterstützungsbedarf"""
        support_indicators = 0

        for turn in turns:
            if turn.emotional_tone in ['sadness', 'anxiety', 'fear']:
                support_indicators += 1
            if turn.intent in ['seeking_comfort', 'asking_guidance']:
                support_indicators += 1

        support_ratio = support_indicators / len(turns) if turns else 0

        if support_ratio > 0.6:
            return 'high'
        elif support_ratio > 0.3:
            return 'moderate'
        else:
            return 'low'

    def _analyze_conversation_flow(self) -> Dict[str, Any]:
        """Analysiert den Gesprächsfluss"""

        turns = list(self.conversation_history)
        if len(turns) < 3:
            return {'flow': 'initializing'}

        return {
            'flow_quality': self._assess_flow_quality(turns),
            'natural_progression': self._check_natural_progression(turns),
            'topic_transitions': self._analyze_topic_transitions(turns),
            'engagement_dynamics': self._detect_engagement_shifts(turns)
        }

    def _assess_flow_quality(self, turns: List[ConversationTurn]) -> str:
        """Bewertet Gesprächsfluss-Qualität"""
        if len(turns) < 3:
            return 'developing'

        # Faktoren für guten Flow
        topic_coherence = self._analyze_topic_coherence(turns[-5:])
        emotional_continuity = self._check_emotional_continuity(turns[-5:])

        flow_score = (topic_coherence + emotional_continuity) / 2

        if flow_score > 0.7:
            return 'smooth'
        elif flow_score > 0.4:
            return 'moderate'
        else:
            return 'choppy'

    def _check_emotional_continuity(self, turns: List[ConversationTurn]) -> float:
        """Prüft emotionale Kontinuität"""
        if len(turns) < 2:
            return 1.0

        emotion_changes = 0
        for i in range(1, len(turns)):
            if turns[i].emotional_tone != turns[i - 1].emotional_tone:
                emotion_changes += 1

        continuity = 1.0 - (emotion_changes / (len(turns) - 1))
        return max(continuity, 0.0)

    def _check_natural_progression(self, turns: List[ConversationTurn]) -> str:
        """Prüft natürliche Gesprächsentwicklung"""
        # Vereinfachte Implementierung
        if len(turns) < 3:
            return 'developing'

        # Prüfe ob sich Themen logisch entwickeln
        recent_topics = []
        for turn in turns[-3:]:
            recent_topics.extend(turn.topics)

        unique_topics = len(set(recent_topics))

        if unique_topics <= 2:
            return 'focused'
        elif unique_topics <= 4:
            return 'natural'
        else:
            return 'scattered'

    def _analyze_topic_transitions(self, turns: List[ConversationTurn]) -> Dict[str, Any]:
        """Analysiert Themenwechsel"""
        if len(turns) < 2:
            return {'transitions': 0, 'smoothness': 'unknown'}

        transitions = 0
        for i in range(1, len(turns)):
            prev_topics = set(turns[i - 1].topics)
            curr_topics = set(turns[i].topics)

            if not prev_topics.intersection(curr_topics) and prev_topics and curr_topics:
                transitions += 1

        smoothness = 'abrupt' if transitions > len(turns) // 2 else 'smooth'

        return {
            'transitions': transitions,
            'smoothness': smoothness,
            'transition_rate': transitions / (len(turns) - 1)
        }

    def _detect_engagement_shifts(self, turns: List[ConversationTurn]) -> Dict[str, Any]:
        """Erkennt Engagement-Veränderungen"""
        if len(turns) < 3:
            return {'shifts': 0, 'trend': 'stable'}

        # Grobe Engagement-Messung basierend auf Nachrichtenlänge
        engagement_levels = []
        for turn in turns:
            length_score = min(len(turn.message.split()) / 20, 1.0)  # Normiert auf 20 Wörter
            emotional_score = 0.5 if turn.emotional_tone != 'neutral' else 0.0
            engagement = (length_score + emotional_score) / 2
            engagement_levels.append(engagement)

        # Erkenne Shifts
        shifts = 0
        for i in range(1, len(engagement_levels)):
            if abs(engagement_levels[i] - engagement_levels[i - 1]) > 0.3:
                shifts += 1

        # Trend
        if len(engagement_levels) >= 3:
            recent_trend = engagement_levels[-1] - engagement_levels[-3]
            if recent_trend > 0.2:
                trend = 'increasing'
            elif recent_trend < -0.2:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'stable'

        return {
            'shifts': shifts,
            'trend': trend,
            'current_level': engagement_levels[-1] if engagement_levels else 0.5
        }

    def _analyze_relationship_dynamics(self) -> Dict[str, Any]:
        """Analysiert Beziehungsdynamiken"""

        return {
            'intimacy_level': self._calculate_intimacy_level(),
            'trust_development': self._assess_trust_development(),
            'communication_style': self._analyze_communication_style(),
            'boundary_dynamics': self._analyze_boundary_dynamics()
        }

    def _calculate_intimacy_level(self) -> float:
        """Berechnet Intimität-Level"""
        if not self.conversation_history:
            return 0.3

        intimacy_score = 0.3  # Basis

        recent_turns = list(self.conversation_history)[-10:]

        for turn in recent_turns:
            # Persönliche Themen erhöhen Intimität
            if any(topic in ['family', 'personal', 'emotional'] for topic in turn.topics):
                intimacy_score += 0.05

            # Vulnerabilität erhöht Intimität
            if turn.intent in ['seeking_comfort', 'sharing_vulnerability']:
                intimacy_score += 0.1

            # Subtext deutet auf tiefere Verbindung hin
            if turn.subtext.get('relationship_signals'):
                intimacy_score += 0.05

        return min(intimacy_score, 1.0)

    def _assess_trust_development(self) -> str:
        """Bewertet Vertrauensentwicklung"""
        if not self.conversation_history:
            return 'unknown'

        trust_indicators = 0
        recent_turns = list(self.conversation_history)[-10:]

        for turn in recent_turns:
            if turn.intent in ['sharing_vulnerability', 'seeking_comfort']:
                trust_indicators += 1
            if 'trust' in turn.subtext.get('relationship_signals', []):
                trust_indicators += 1

        trust_ratio = trust_indicators / len(recent_turns) if recent_turns else 0

        if trust_ratio > 0.4:
            return 'building_strong'
        elif trust_ratio > 0.2:
            return 'developing'
        else:
            return 'cautious'

    def _analyze_communication_style(self) -> Dict[str, float]:
        """Analysiert Kommunikationsstil"""
        if not self.conversation_history:
            return {'directness': 0.5, 'formality': 0.5, 'emotionality': 0.5}

        recent_turns = list(self.conversation_history)[-10:]

        # Berechne verschiedene Stil-Dimensionen
        directness = self._measure_directness(recent_turns)
        formality = self._measure_formality(recent_turns)
        emotionality = self._measure_emotionality(recent_turns)

        return {
            'directness': directness,
            'formality': formality,
            'emotionality': emotionality
        }

    def _measure_directness(self, turns: List[ConversationTurn]) -> float:
        """Misst Direktheit der Kommunikation"""
        if not turns:
            return 0.5

        directness_score = 0.5

        for turn in turns:
            # Kurze Nachrichten tendenziell direkter
            if len(turn.message.split()) < 8:
                directness_score += 0.05

            # Fragen sind oft direkt
            if '?' in turn.message:
                directness_score += 0.05

        return min(directness_score, 1.0)

    def _measure_formality(self, turns: List[ConversationTurn]) -> float:
        """Misst Formalität der Kommunikation"""
        if not turns:
            return 0.5

        formality_score = 0.5

        for turn in turns:
            # Höflichkeitsformen
            if any(word in turn.message.lower() for word in ['bitte', 'danke', 'entschuldigung']):
                formality_score += 0.1

            # Informelle Sprache
            if any(word in turn.message.lower() for word in ['hey', 'hallo', 'cool']):
                formality_score -= 0.05

        return max(0.1, min(formality_score, 1.0))

    def _measure_emotionality(self, turns: List[ConversationTurn]) -> float:
        """Misst Emotionalität der Kommunikation"""
        if not turns:
            return 0.5

        emotional_turns = sum(1 for turn in turns if turn.emotional_tone != 'neutral')
        emotionality = emotional_turns / len(turns) if turns else 0.5

        return min(emotionality, 1.0)

    def _analyze_boundary_dynamics(self) -> Dict[str, str]:
        """Analysiert Grenz-Dynamiken"""

        # Vereinfachte Implementierung
        intimacy = self._calculate_intimacy_level()

        if intimacy > 0.7:
            return {
                'emotional_boundaries': 'low',
                'topic_boundaries': 'flexible',
                'personal_space': 'comfortable'
            }
        elif intimacy > 0.4:
            return {
                'emotional_boundaries': 'moderate',
                'topic_boundaries': 'selective',
                'personal_space': 'respectful'
            }
        else:
            return {
                'emotional_boundaries': 'high',
                'topic_boundaries': 'careful',
                'personal_space': 'formal'
            }

    def _get_relevant_memories(self) -> List[Dict]:
        """Holt relevante Erinnerungen"""
        if not self.memory.significant_moments:
            return []

        # Einfache Relevanz basierend auf aktuellen Themen
        current_topics = []
        if self.conversation_history:
            recent_turns = list(self.conversation_history)[-3:]
            for turn in recent_turns:
                current_topics.extend(turn.topics)

        relevant_memories = []
        for memory in self.memory.significant_moments[-10:]:  # Letzte 10 wichtige Momente
            relevance_score = 0.5

            # Thematische Relevanz
            memory_topics = memory.topics
            common_topics = set(current_topics).intersection(set(memory_topics))
            if common_topics:
                relevance_score += 0.3

            # Emotionale Relevanz
            if self.conversation_history:
                current_emotion = list(self.conversation_history)[-1].emotional_tone
                if memory.emotional_tone == current_emotion:
                    relevance_score += 0.2

            if relevance_score > 0.6:
                relevant_memories.append({
                    'memory': memory,
                    'relevance': relevance_score,
                    'connection_type': 'thematic' if common_topics else 'emotional'
                })

        return sorted(relevant_memories, key=lambda x: x['relevance'], reverse=True)[:5]

    def _generate_predictive_insights(self) -> Dict[str, Any]:
        """Generiert Vorhersagen"""

        return {
            'likely_next_topics': self._predict_next_topics(),
            'emotional_trajectory': self._predict_emotional_development(),
            'conversation_needs': self._predict_conversation_needs()
        }

    def _predict_next_topics(self) -> List[str]:
        """Vorhersage nächster Themen"""
        if not self.conversation_history:
            return ['general']

        # Basiert auf aktuellen Themen und Patterns
        recent_topics = []
        for turn in list(self.conversation_history)[-3:]:
            recent_topics.extend(turn.topics)

        # Häufigste Themen als Vorhersage
        topic_counts = defaultdict(int)
        for topic in recent_topics:
            topic_counts[topic] += 1

        predicted = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        return [topic for topic, count in predicted[:3]]

    def _predict_emotional_development(self) -> str:
        """Vorhersage emotionaler Entwicklung"""
        if len(self.conversation_history) < 3:
            return 'stable'

        recent_emotions = [turn.emotional_tone for turn in list(self.conversation_history)[-3:]]

        # Einfache Trend-Analyse
        emotion_values = {
            'joy': 3, 'love': 3, 'trust': 2, 'neutral': 0,
            'sadness': -2, 'anxiety': -2, 'anger': -2, 'fear': -3
        }

        values = [emotion_values.get(emotion, 0) for emotion in recent_emotions]

        if len(values) >= 2:
            trend = values[-1] - values[0]
            if trend > 0:
                return 'improving'
            elif trend < 0:
                return 'declining'

        return 'stable'

    def _predict_conversation_needs(self) -> List[str]:
        """Vorhersage Gesprächsbedürfnisse"""
        needs = []

        if not self.conversation_history:
            return ['basic_interaction']

        recent_turns = list(self.conversation_history)[-5:]

        # Basiert auf aktuellen emotionalen Zuständen und Intents
        emotional_needs = self._identify_emotional_needs(recent_turns)

        if 'comfort_and_support' in emotional_needs:
            needs.append('empathetic_response')
        if 'emotional_validation' in emotional_needs:
            needs.append('validation_and_understanding')

        # Gesprächsflow-basierte Bedürfnisse
        flow_analysis = self._analyze_conversation_flow()
        if flow_analysis['flow_quality'] == 'choppy':
            needs.append('topic_guidance')

        return needs if needs else ['continued_engagement']

    def _suggest_character_adaptation(self, character: str) -> Dict[str, Any]:
        """Schlägt charakterspezifische Anpassungen vor"""

        current_context = self._analyze_current_context()
        emotional_state = self._analyze_emotional_state()
        relationship_dynamics = self._analyze_relationship_dynamics()

        return {
            'communication_style': self._suggest_communication_style(
                character, emotional_state, relationship_dynamics
            ),
            'empathy_level': self._calculate_needed_empathy_level(emotional_state),
            'response_tone': self._suggest_response_tone(current_context),
            'interaction_depth': self._suggest_interaction_depth(relationship_dynamics),
            'emotional_support': self._assess_needed_emotional_support(emotional_state)
        }

    def _suggest_communication_style(self, character: str, emotional_state: Dict,
                                     relationship_dynamics: Dict) -> Dict[str, float]:
        """Schlägt Kommunikationsstil vor"""

        style = {
            'directness': 0.5,
            'warmth': 0.5,
            'professionalism': 0.5,
            'emotional_expression': 0.5
        }

        # Anpassungen basierend auf emotionalem Zustand
        if emotional_state['support_requirements'] == 'high':
            style['warmth'] += 0.3
            style['emotional_expression'] += 0.2

        # Anpassungen basierend auf Beziehungsdynamik
        intimacy = relationship_dynamics['intimacy_level']
        if intimacy > 0.7:
            style['warmth'] += 0.2
            style['professionalism'] -= 0.2

        # Charakterspezifische Anpassungen
        if character.lower() == 'tsunade':
            style['professionalism'] += 0.1  # Hokage-Aspekt
            style['warmth'] += 0.2  # Mütterliche Seite

        return {k: min(1.0, max(0.1, v)) for k, v in style.items()}

    def _calculate_needed_empathy_level(self, emotional_state: Dict) -> float:
        """Berechnet benötigtes Empathie-Level"""
        base_empathy = 0.6

        # Erhöhe basierend auf Support-Bedarf
        support_level = emotional_state['support_requirements']
        if support_level == 'high':
            base_empathy += 0.3
        elif support_level == 'moderate':
            base_empathy += 0.1

        # Erhöhe bei negativen Emotionen
        primary_emotion = emotional_state['primary_emotion']
        if primary_emotion in ['sadness', 'anxiety', 'fear']:
            base_empathy += 0.2

        return min(base_empathy, 1.0)

    def _suggest_response_tone(self, current_context: Dict) -> str:
        """Schlägt Response-Ton vor"""

        dominant_emotion = current_context['dominant_emotion']

        tone_mapping = {
            'sadness': 'gentle_supportive',
            'anxiety': 'calm_reassuring',
            'joy': 'warm_sharing',
            'anger': 'understanding_firm',
            'neutral': 'naturally_caring'
        }

        return tone_mapping.get(dominant_emotion, 'balanced_caring')

    def _suggest_interaction_depth(self, relationship_dynamics: Dict) -> str:
        """Schlägt Interaktionstiefe vor"""

        intimacy = relationship_dynamics['intimacy_level']

        if intimacy > 0.8:
            return 'deep_personal'
        elif intimacy > 0.5:
            return 'moderate_personal'
        elif intimacy > 0.3:
            return 'light_personal'
        else:
            return 'surface_friendly'

    def _assess_needed_emotional_support(self, emotional_state: Dict) -> Dict[str, bool]:
        """Bewertet benötigte emotionale Unterstützung"""

        primary_emotion = emotional_state['primary_emotion']
        support_requirements = emotional_state['support_requirements']

        return {
            'comfort_needed': primary_emotion in ['sadness', 'anxiety', 'fear'],
            'validation_needed': support_requirements in ['moderate', 'high'],
            'encouragement_needed': emotional_state['intensity_trend'] == 'decreasing',
            'celebration_needed': primary_emotion == 'joy',
            'guidance_needed': support_requirements == 'high'
        }

    def _update_longterm_memory(self, turn: ConversationTurn):
        """Aktualisiert Langzeitgedächtnis"""

        self.memory.significant_moments.append(turn)

        # Begrenze Anzahl gespeicherter Momente
        if len(self.memory.significant_moments) > 50:
            self.memory.significant_moments = self.memory.significant_moments[-50:]

        # Aktualisiere wiederkehrende Themen
        for topic in turn.topics:
            self.memory.recurring_themes[topic] = self.memory.recurring_themes.get(topic, 0) + 1

    def _detect_conversation_patterns(self):
        """Erkennt Gesprächsmuster"""

        if len(self.conversation_history) < 5:
            return

        recent_turns = list(self.conversation_history)[-5:]

        # Erkenne emotionale Muster
        emotions = [turn.emotional_tone for turn in recent_turns]

        # Erkenne Wiederholungen
        if len(set(emotions)) == 1 and emotions[0] != 'neutral':
            # Gleichbleibende Emotion über mehrere Turns
            pattern = EmotionalPattern(
                emotion=emotions[0],
                intensity=0.7,  # Grobe Schätzung
                duration=len(emotions),
                triggers=list(set(topic for turn in recent_turns for topic in turn.topics))
            )
            self.memory.emotional_history.append(pattern)


class EmotionAnalyzer:
    """Analysiert Emotionen in Nachrichten"""

    def __init__(self):
        self.emotion_lexicon = self._build_emotion_lexicon()

    def _build_emotion_lexicon(self) -> Dict[str, List[str]]:
        """Erstellt Emotion-Lexikon für Deutsche Sprache"""
        return {
            'joy': ['glücklich', 'freude', 'fröhlich', 'begeistert', 'toll', 'wunderbar', 'großartig'],
            'sadness': ['traurig', 'deprimiert', 'niedergeschlagen', 'melancholisch', 'betrübt'],
            'anger': ['wütend', 'ärgerlich', 'frustriert', 'sauer', 'zornig', 'empört'],
            'fear': ['angst', 'ängstlich', 'besorgt', 'nervös', 'panisch', 'erschrocken'],
            'surprise': ['überrascht', 'erstaunt', 'verwundert', 'schockiert', 'verblüfft'],
            'love': ['liebe', 'mögen', 'schätzen', 'verehren', 'anbeten'],
            'trust': ['vertrauen', 'glauben', 'sicher', 'geborgen', 'verlassen'],
            'anxiety': ['sorge', 'unruhig', 'gestresst', 'angespannt', 'beunruhigt']
        }

    def analyze_emotion(self, message: str) -> str:
        """Analysiert primäre Emotion einer Nachricht"""
        message_lower = message.lower()
        emotion_scores = defaultdict(int)

        # Zähle Emotionswörter
        for emotion, words in self.emotion_lexicon.items():
            for word in words:
                if word in message_lower:
                    emotion_scores[emotion] += 1

        # Berücksichtige Kontext-Hinweise
        if '?' in message and len(message.split()) < 10:
            emotion_scores['curiosity'] += 1

        if '...' in message:
            emotion_scores['sadness'] += 1
            emotion_scores['uncertainty'] += 1

        # Bestimme dominante Emotion
        if emotion_scores:
            return max(emotion_scores.items(), key=lambda x: x[1])[0]

        return 'neutral'


class TopicExtractor:
    """Extrahiert Gesprächsthemen"""

    def __init__(self):
        self.topic_keywords = self._build_topic_keywords()

    def _build_topic_keywords(self) -> Dict[str, List[str]]:
        """Erstellt Topic-Keyword Mapping"""
        return {
            'medical': ['krank', 'verletzt', 'schmerz', 'heilung', 'medizin', 'behandlung', 'arzt'],
            'family': ['familie', 'eltern', 'geschwister', 'verwandte', 'bruder', 'schwester'],
            'emotional': ['gefühl', 'emotion', 'herz', 'seele', 'empfindung'],
            'training': ['training', 'übung', 'lernen', 'technik', 'ausbildung', 'praxis'],
            'personal': ['persönlich', 'privat', 'geheim', 'intim', 'vergangenheit'],
            'future': ['zukunft', 'pläne', 'träume', 'ziele', 'hoffnung', 'wünsche'],
            'work': ['arbeit', 'job', 'beruf', 'pflicht', 'verantwortung', 'hokage'],
            'friendship': ['freund', 'freundschaft', 'zusammen', 'vertrauen', 'verbindung']
        }

    def extract_topics(self, message: str) -> List[str]:
        """Extrahiert Themen aus einer Nachricht"""
        message_lower = message.lower()
        found_topics = []

        for topic, keywords in self.topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                found_topics.append(topic)

        return found_topics


class IntentClassifier:
    """Klassifiziert Gesprächsabsichten"""

    def __init__(self):
        self.intent_patterns = self._build_intent_patterns()

    def _build_intent_patterns(self) -> Dict[str, List[str]]:
        """Erstellt Intent-Pattern Mapping"""
        return {
            'seeking_comfort': ['hilfe', 'trost', 'allein', 'verstehen', 'sorge'],
            'sharing_joy': ['freue', 'toll', 'geschafft', 'glücklich', 'stolz'],
            'asking_guidance': ['was soll', 'wie kann', 'rat', 'meinung', 'empfehlung'],
            'expressing_gratitude': ['danke', 'dankbar', 'schätze', 'bedeutet mir'],
            'sharing_vulnerability': ['schwach', 'verletzlich', 'verletze', 'angst'],
            'requesting_info': ['was ist', 'wie funktioniert', 'erklär', 'warum'],
            'casual_chat': ['hallo', 'wie geht', 'was machst', 'schöner tag'],
            'seeking_validation': ['richtig', 'okay', 'normal', 'verständlich']
        }

    def classify_intent(self, message: str, context: deque) -> str:
        """Klassifiziert die Absicht einer Nachricht"""
        message_lower = message.lower()
        intent_scores = defaultdict(int)

        # Pattern-basierte Klassifikation
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in message_lower:
                    intent_scores[intent] += 1

        # Kontext-basierte Anpassungen
        if len(context) > 0:
            last_turn = context[-1]
            if last_turn.emotional_tone in ['sadness', 'anxiety']:
                intent_scores['seeking_comfort'] += 1

        # Bestimme primäre Intent
        if intent_scores:
            return max(intent_scores.items(), key=lambda x: x[1])[0]

        return 'general_interaction'


class SubtextAnalyzer:
    """Analysiert Subtext und versteckte Bedeutungen"""

    def analyze_subtext(self, message: str, context: deque) -> Dict[str, Any]:
        """Analysiert Subtext einer Nachricht"""

        subtext = {
            'hidden_emotions': self._detect_hidden_emotions(message),
            'unspoken_needs': self._identify_unspoken_needs(message, context),
            'relationship_signals': self._detect_relationship_signals(message, context)
        }

        return subtext

    def _detect_hidden_emotions(self, message: str) -> List[str]:
        """Erkennt versteckte Emotionen"""
        hidden_emotions = []

        # Kurze "okay" Antworten könnten versteckte Trauer bedeuten
        if re.match(r'^(okay|ok|gut)\.?$', message.lower().strip()):
            hidden_emotions.append('possible_sadness')

        # Punkte/Pausen deuten auf Unsicherheit hin
        if '...' in message or re.search(r'\.{2,}', message):
            hidden_emotions.append('uncertainty_or_sadness')

        return hidden_emotions

    def _identify_unspoken_needs(self, message: str, context: deque) -> List[str]:
        """Identifiziert unausgesprochene Bedürfnisse"""
        needs = []

        # Müdigkeit → Bedürfnis nach Ruhe und Trost
        if any(word in message.lower() for word in ['müde', 'erschöpft', 'kaputt']):
            needs.append('rest_and_comfort')

        # Einsamkeit → Bedürfnis nach Verbindung
        if any(word in message.lower() for word in ['allein', 'einsam', 'niemand']):
            needs.append('connection_and_companionship')

        # Unsicherheit → Bedürfnis nach Bestätigung
        if any(word in message.lower() for word in ['unsicher', 'weiß nicht', 'vielleicht']):
            needs.append('validation_and_guidance')

        return needs

    def _detect_relationship_signals(self, message: str, context: deque) -> List[str]:
        """Erkennt Beziehungssignale"""
        signals = []

        # Verwendung von "du" vs "Sie"
        if 'du' in message.lower() and len(context) > 0:
            signals.append('informal_address_used')

        # Persönliche Informationen teilen
        personal_markers = ['ich fühle', 'meine', 'persönlich', 'privat']
        if any(marker in message.lower() for marker in personal_markers):
            signals.append('personal_sharing')

        # Sorge um andere ausdrücken
        if any(word in message.lower() for word in ['sorge', 'hoffe', 'wünsche']):
            signals.append('caring_expression')

        return signals


class PatternDetector:
    """Erkennt Muster in Gesprächsverläufen"""

    def detect_emotional_patterns(self, history: List[ConversationTurn]) -> List[EmotionalPattern]:
        """Erkennt emotionale Muster über Zeit"""
        patterns = []

        if len(history) < 5:
            return patterns

        # Suche nach emotionalen Zyklen
        emotions = [turn.emotional_tone for turn in history]

        # Erkenne wiederkehrende emotionale Sequenzen
        for i in range(len(emotions) - 3):
            sequence = emotions[i:i + 3]
            if sequence.count(sequence[0]) == 3:  # Gleiche Emotion 3x hintereinander
                pattern = EmotionalPattern(
                    emotion=sequence[0],
                    intensity=0.7,  # Placeholder
                    duration=3,
                    triggers=[]  # Placeholder
                )
                patterns.append(pattern)

        return patterns


# Integration in bestehendes System
def integrate_advanced_context_manager(game_data):
    """
    Integriert erweiterte Kontextualisierung in bestehendes System
    """

    context_manager = AdvancedContextManager()

    # Speichere original get_formatted_response
    if hasattr(game_data, 'get_formatted_response'):
        game_data._original_get_formatted_response = game_data.get_formatted_response

    def enhanced_get_formatted_response(character: str, user_message: str) -> str:
        """
        Erweiterte Response-Generierung mit Kontext-Analyse
        """
        try:
            # Füge User-Turn zum Kontext hinzu
            user_turn = context_manager.add_conversation_turn("Sukuna", user_message)

            # Hole umfassende Kontext-Analyse
            context_analysis = context_manager.get_contextual_analysis(character)

            # Erstelle context-aware Prompt
            enhanced_prompt = _create_context_aware_prompt(
                character, user_message, context_analysis
            )

            # Generiere Response (hier würde LLM-Call stattfinden)
            if hasattr(game_data, '_original_get_formatted_response'):
                base_response = game_data._original_get_formatted_response(character, user_message)
            else:
                base_response = f"*{character} denkt nach* Das ist interessant..."

            # Füge Character-Response zum Kontext hinzu
            context_manager.add_conversation_turn(character, base_response, response_quality=0.8)

            return base_response

        except Exception as e:
            print(f"⚠️ Context Manager Fehler: {e}")
            if hasattr(game_data, '_original_get_formatted_response'):
                return game_data._original_get_formatted_response(character, user_message)
            return f"*{character} lächelt* Erzähl mir mehr davon."

    def _create_context_aware_prompt(character: str, message: str,
                                     context_analysis: Dict) -> str:
        """Erstellt kontext-bewussten Prompt"""

        prompt = f"""
        Du bist {character}. Ein Nutzer sagt: "{message}"

        KONTEXT-ANALYSE:

        Aktuelle Situation:
        - Dominante Emotion: {context_analysis['current_context'].get('dominant_emotion', 'neutral')}
        - Gesprächsmomentum: {context_analysis['current_context'].get('conversation_momentum', 'stable')}
        - Engagement-Level: {context_analysis['current_context'].get('engagement_level', 'medium')}

        Emotionaler Zustand:
        - Primäre Emotion: {context_analysis['emotional_state'].get('primary_emotion', 'neutral')}
        - Emotionale Stabilität: {context_analysis['emotional_state'].get('emotional_stability', 'stable')}
        - Unterstützungsbedarf: {context_analysis['emotional_state'].get('support_requirements', 'normal')}

        Beziehungsdynamik:
        - Intimität-Level: {context_analysis['relationship_dynamics'].get('intimacy_level', 'medium')}
        - Vertrauensentwicklung: {context_analysis['relationship_dynamics'].get('trust_development', 'steady')}

        Anpassungsempfehlungen:
        - Kommunikationsstil: {context_analysis['character_adaptation'].get('communication_style', 'balanced')}
        - Empathie-Level: {context_analysis['character_adaptation'].get('empathy_level', 'medium')}
        - Response-Ton: {context_analysis['character_adaptation'].get('response_tone', 'caring')}

        Reagiere als {character} unter Berücksichtigung dieser Kontext-Informationen.
        """

        return prompt

    # Setze neue Methode
    game_data.get_formatted_response = enhanced_get_formatted_response
    game_data.context_manager = context_manager

    print("✅ Erweiterte Kontextualisierung integriert!")

    return context_manager