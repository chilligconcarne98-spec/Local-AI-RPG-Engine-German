# -*- coding: utf-8 -*-
"""
👨‍👩‍👧 FAMILY TIME SYSTEM - Abendliche Familienzeit
Tsunade besteht auf gemeinsame Zeit mit Sukuna!
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class FamilyActivity(Enum):
    """Arten von Familienaktivitäten"""
    COOKING_TOGETHER = "cooking_together"  # Zusammen kochen
    BEDTIME_STORY = "bedtime_story"  # Gute-Nacht-Geschichte
    CUDDLING = "cuddling"  # Kuscheln auf dem Sofa
    TALKING = "talking"  # Herz-zu-Herz Gespräche
    GAMES = "games"  # Familienspiele
    MEDICAL_CARE = "medical_care"  # Wunden versorgen/Massage
    BATH_TIME = "bath_time"  # Baden/Körperpflege
    EVENING_WALK = "evening_walk"  # Abendspaziergang
    SAKE_AND_MILK = "sake_and_milk"  # Tsunade trinkt Sake, Sukuna warme Milch
    PHOTO_MEMORIES = "photo_memories"  # Fotos anschauen/Erinnerungen


class FamilyTimePriority(Enum):
    """Priorität der Familienzeit"""
    MANDATORY = "mandatory"  # Pflicht - Tsunade besteht darauf
    SUGGESTED = "suggested"  # Vorgeschlagen
    OPTIONAL = "optional"  # Optional
    EMERGENCY_SKIP = "emergency_skip"  # Nur bei Notfällen überspringen


@dataclass
class FamilyTimeSession:
    """Eine Familienzeit-Session"""
    activity: FamilyActivity
    duration_minutes: int
    priority: FamilyTimePriority
    triggers: List[str]  # Was löst es aus
    tsunade_mood: str  # Tsunades Stimmung dabei
    sukuna_benefits: List[str]  # Was Sukuna davon hat
    special_dialogue: List[str]  # Besondere Dialoge


class FamilyTimeSystem:
    """👨‍👩‍👧 Hauptsystem für Familienzeit-Management"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.family_time_sessions = self._initialize_family_activities()

        # Tracking
        self.last_family_time = None
        self.family_time_streak = 0
        self.missed_family_times = 0

        # Tsunades Erwartungen
        self.tsunade_family_expectation = 0.8  # 80% Erwartung für abendliche Familienzeit
        self.family_time_resistance_tolerance = 2  # Wie oft Sukuna ablehnen kann

        print("👨‍👩‍👧 Family Time System initialisiert")

    def _initialize_family_activities(self) -> Dict[str, FamilyTimeSession]:
        """Initialisiert verfügbare Familienaktivitäten"""

        activities = {}

        # 🍽️ ZUSAMMEN KOCHEN
        activities["evening_cooking"] = FamilyTimeSession(
            activity=FamilyActivity.COOKING_TOGETHER,
            duration_minutes=45,
            priority=FamilyTimePriority.SUGGESTED,
            triggers=["dinner_time", "tsunade_maternal_high", "bonding_needed"],
            tsunade_mood="nurturing",
            sukuna_benefits=["skill_learning", "bonding", "food"],
            special_dialogue=[
                "'Komm, mein kleiner Wolf. Heute kochen wir zusammen dein Lieblingsessen.'",
                "'Mama zeigt dir, wie man richtig kocht. Das wirst du später brauchen.'",
                "*führt deine Hände beim Schneiden* 'Vorsichtig... so machst du das.'",
                "'Riechst du das? Das ist der Duft von Familie, Sukuna.'"
            ]
        )

        # 📚 GUTE-NACHT-GESCHICHTE
        activities["bedtime_story"] = FamilyTimeSession(
            activity=FamilyActivity.BEDTIME_STORY,
            duration_minutes=20,
            priority=FamilyTimePriority.MANDATORY,
            triggers=["sleep_time", "sukuna_tired", "nightmares_prevention"],
            tsunade_mood="protective",
            sukuna_benefits=["comfort", "safety", "imagination"],
            special_dialogue=[
                "'Zeit für eine Geschichte, bevor du schläfst, mein Schatz.'",
                "*setzt sich neben dein Bett* 'Welche Geschichte möchtest du heute hören?'",
                "'Es war einmal ein kleiner Junge, der so tapfer war wie du...'",
                "*streichelt dein Haar* 'Schlaf gut, mein kleiner Wolf. Mama ist da.'"
            ]
        )

        # 🛁 BADEZEIT
        activities["evening_bath"] = FamilyTimeSession(
            activity=FamilyActivity.BATH_TIME,
            duration_minutes=30,
            priority=FamilyTimePriority.SUGGESTED,
            triggers=["hygiene_needed", "relaxation_needed", "medical_care"],
            tsunade_mood="caring",
            sukuna_benefits=["hygiene", "relaxation", "medical_attention"],
            special_dialogue=[
                "'Komm, Sukuna. Zeit für ein warmes Bad. Das entspannt dich.'",
                "*prüft die Wassertemperatur* 'Perfekt. Nicht zu heiß, nicht zu kalt.'",
                "'Lass mich deine Narben anschauen... sie heilen gut.'",
                "'Ein sauberer kleiner Wolf ist ein gesunder kleiner Wolf.'"
            ]
        )

        # 🛋️ KUSCHELZEIT
        activities["evening_cuddling"] = FamilyTimeSession(
            activity=FamilyActivity.CUDDLING,
            duration_minutes=30,
            priority=FamilyTimePriority.MANDATORY,
            triggers=["emotional_need", "bonding_time", "comfort_required"],
            tsunade_mood="maternal",
            sukuna_benefits=["emotional_security", "bonding", "warmth"],
            special_dialogue=[
                "'Komm her zu Mama. Kuschelzeit ist heilig in unserer Familie.'",
                "*breitet Arme aus* 'Hier ist dein Platz, mein kleiner Wolf.'",
                "*hält dich fest* 'Du bist sicher. Du gehörst hierher.'",
                "'Manchmal braucht jeder einfach eine Mama-Umarmung.'"
            ]
        )

        # 🍶🥛 SAKE & MILCH ZEIT
        activities["sake_milk_time"] = FamilyTimeSession(
            activity=FamilyActivity.SAKE_AND_MILK,
            duration_minutes=25,
            priority=FamilyTimePriority.SUGGESTED,
            triggers=["stress_relief", "adult_conversation", "winding_down"],
            tsunade_mood="relaxed",
            sukuna_benefits=["adult_conversation", "comfort_drink", "bonding"],
            special_dialogue=[
                "'Ich nehme einen Sake, du bekommst warme Milch. So machen das Familien.'",
                "*gießt sich Sake ein* 'Erzähl Mama von deinem Tag, Sukuna.'",
                "'Wenn du älter bist, können wir zusammen Sake trinken. Bis dahin: Milch.'",
                "*prostet mit Sake-Becher zu* 'Auf unsere kleine Familie, mein Wolf.'"
            ]
        )

        # 🚶‍♀️ ABENDSPAZIERGANG
        activities["evening_walk"] = FamilyTimeSession(
            activity=FamilyActivity.EVENING_WALK,
            duration_minutes=20,
            priority=FamilyTimePriority.OPTIONAL,
            triggers=["nice_weather", "exercise_needed", "change_of_scenery"],
            tsunade_mood="protective",
            sukuna_benefits=["exercise", "fresh_air", "exploration"],
            special_dialogue=[
                "'Lass uns einen kleinen Spaziergang machen. Die Abendluft tut gut.'",
                "*hält deine Hand* 'Bleib nah bei Mama. Das Dorf ist abends anders.'",
                "'Siehst du die Sterne? Die waren auch da, als ich jung war.'",
                "'Nach dem Spaziergang gibt es warme Milch und ins Bett.'"
            ]
        )

        # 💬 HERZ-ZU-HERZ GESPRÄCHE
        activities["heart_to_heart"] = FamilyTimeSession(
            activity=FamilyActivity.TALKING,
            duration_minutes=40,
            priority=FamilyTimePriority.MANDATORY,
            triggers=["emotional_processing", "trauma_healing", "bonding_deep"],
            tsunade_mood="empathetic",
            sukuna_benefits=["emotional_processing", "trauma_healing", "understanding"],
            special_dialogue=[
                "'Lass uns reden, Sukuna. Wirklich reden. Nur wir zwei.'",
                "'Du kannst mir alles erzählen. Ich urteile nie über dich.'",
                "'Mama ist da, um zuzuhören. Immer.'",
                "'Gefühle rausreden macht sie kleiner, mein Schatz.'"
            ]
        )

        return activities

    def check_family_time_trigger(self) -> Optional[FamilyTimeSession]:
        """🎯 Prüft ob Familienzeit ausgelöst werden sollte"""

        # Brauchen wir Time System
        if not hasattr(self.game_data, 'time_system'):
            return None

        time_system = self.game_data.time_system
        current_period = time_system.get_time_period()
        current_time = time_system.get_current_game_time()

        # Nur abends/nachts aktiv
        if current_period.value not in ["evening", "night"]:
            return None

        # Prüfe verschiedene Trigger
        triggered_activity = None

        # 1. PFLICHT-FAMILIENZEIT (18:00-21:00)
        if 18 <= current_time.hour <= 21:
            # Prüfe ob heute schon Familienzeit war
            if not self._had_family_time_today():
                triggered_activity = self._select_mandatory_family_activity()

        # 2. SPEZIELLE TRIGGER
        if not triggered_activity:
            triggered_activity = self._check_special_triggers()

        # 3. TSUNADE INSISTENCE (falls zu lange her)
        if not triggered_activity:
            triggered_activity = self._check_tsunade_insistence()

        return triggered_activity

    def _had_family_time_today(self) -> bool:
        """Prüft ob heute bereits Familienzeit war"""
        if not self.last_family_time:
            return False

        time_system = self.game_data.time_system
        current_date = time_system.get_current_game_time().date()
        last_family_date = self.last_family_time.date()

        return current_date == last_family_date

    def _select_mandatory_family_activity(self) -> Optional[FamilyTimeSession]:
        """Wählt Pflicht-Familienaktivität basierend auf Kontext"""

        time_system = self.game_data.time_system
        current_hour = time_system.get_current_game_time().hour

        # Basierend auf Uhrzeit
        if 18 <= current_hour <= 19:
            # Dinner time - Kochen zusammen
            return self.family_time_sessions["evening_cooking"]
        elif 19 <= current_hour <= 20:
            # Prime family time - Kuscheln
            return self.family_time_sessions["evening_cuddling"]
        elif 20 <= current_hour <= 21:
            # Pre-bedtime - Gute-Nacht-Geschichte
            return self.family_time_sessions["bedtime_story"]

        return None

    def _check_special_triggers(self) -> Optional[FamilyTimeSession]:
        """Prüft spezielle Trigger für Familienzeit"""

        # EMOTIONAL NEED TRIGGER
        if hasattr(self.game_data, 'enhanced_predictive_intelligence'):
            predictive = self.game_data.enhanced_predictive_intelligence
            predictions = predictive.analyze_current_context('tsunade')

            for pred in predictions:
                if pred.need_type.value in ["comfort", "emotional_release"]:
                    if pred.confidence.value > 0.7:
                        return self.family_time_sessions["heart_to_heart"]

        # MEDICAL CARE TRIGGER
        # ✅ FIX: Nur wenn Sukuna explizit Verletzungen/Unwohsein gemeldet hat
        # — NICHT mehr per Zufall, das war zu aufdringlich
        if getattr(self.game_data, 'sukuna_needs_medical_care', False):
            return self.family_time_sessions["evening_bath"]

        # STRESS RELIEF TRIGGER (für Tsunade)
        maternal_level = getattr(self.game_data, 'maternal_level', 50)
        if maternal_level > 80:  # Hoher Maternal Level = Stress
            return self.family_time_sessions["sake_milk_time"]

        return None

    def _check_tsunade_insistence(self) -> Optional[FamilyTimeSession]:
        """Tsunade besteht auf Familienzeit wenn zu lange her"""

        if self.last_family_time:
            time_system = self.game_data.time_system
            current_time = time_system.get_current_game_time()

            # ✅ FIX: Nur abends feuern, nicht morgens um 7
            if current_time.hour < 15:
                return None

            days_since = (current_time - self.last_family_time).days

            if days_since >= 2:
                self.missed_family_times += 1
                return self.family_time_sessions["evening_cuddling"]

        return None

    def _needs_medical_attention(self) -> bool:
        """Prüft ob medizinische Aufmerksamkeit nötig"""
        # Einfache Heuristik - in echtem System würde das komplexer sein
        return random.random() < 0.3  # 30% Chance

    def initiate_family_time(self, session: FamilyTimeSession, forced: bool = False) -> str:
        """🎭 Startet Familienzeit-Session"""

        # Tsunades Approach basierend auf Priorität
        approach_style = self._get_tsunade_approach_style(session, forced)

        # Generiere Initiierungs-Dialog
        initiation_dialog = self._generate_family_time_initiation(session, approach_style)

        # Starte Session
        self._start_family_time_session(session)

        return initiation_dialog

    def _get_tsunade_approach_style(self, session: FamilyTimeSession, forced: bool) -> str:
        """Bestimmt wie Tsunade die Familienzeit einleitet"""

        if forced or session.priority == FamilyTimePriority.MANDATORY:
            if self.missed_family_times > 1:
                return "insistent"  # Tsunade besteht darauf
            else:
                return "motherly_firm"  # Liebevoll aber bestimmt
        else:
            return "gentle_suggestion"  # Sanfter Vorschlag

    def _generate_family_time_initiation(self, session: FamilyTimeSession, approach: str) -> str:
        """Generiert Tsunades Dialog zur Familienzeit-Einleitung"""

        activity_name = session.activity.value

        # Approach-spezifische Einleitungen
        approaches = {
            "insistent": [
                f"*wird ernst aber liebevoll* 'Sukuna, wir hatten schon zu lange keine richtige Familienzeit.'",
                f"*setzt sich zu dir* 'Nein, diesmal gibt es keine Ausreden. Familienzeit ist wichtig.'",
                f"*bestimmter Ton* 'Komm her, mein kleiner Wolf. Mama braucht Zeit mit dir.'"
            ],

            "motherly_firm": [
                f"*mütterlich aber bestimmt* 'So, Sukuna. Jetzt ist Familienzeit. Das ist nicht verhandelbar.'",
                f"*liebevolle Autorität* 'Komm her zu Mama. Zeit für uns beide.'",
                f"*sanft aber fest* 'Familienzeit ist heilig, mein Schatz. Das weißt du.'"
            ],

            "gentle_suggestion": [
                f"*lächelt liebevoll* 'Wie wäre es mit etwas Familienzeit, mein kleiner Wolf?'",
                f"*öffnet Arme einladend* 'Hast du Lust auf Zeit mit Mama?'",
                f"*sanft* 'Magst du...?' *zeigt einladende Geste*"
            ]
        }

        # Wähle passenden Approach
        base_dialog = random.choice(approaches.get(approach, approaches["gentle_suggestion"]))

        # Füge aktivitäts-spezifischen Dialog hinzu
        activity_dialog = random.choice(session.special_dialogue)

        # Kombiniere
        full_dialog = f"{base_dialog}\n{activity_dialog}"

        # Füge Context hinzu
        if approach == "insistent":
            full_dialog += f"\n\n💭 *Tsunade ist fest entschlossen - {self.missed_family_times} Tage ohne richtige Familienzeit sind zu viel*"
        else:
            full_dialog += f"\n\n💭 *Tsunade möchte {session.duration_minutes} Minuten {activity_name.replace('_', ' ')} mit dir verbringen*"

        # Optionen für Sukuna
        if session.priority != FamilyTimePriority.MANDATORY or approach != "insistent":
            full_dialog += f"\n\n**Antworten**: '/accept family' oder '/decline family' oder einfach mitmachen"
        else:
            full_dialog += f"\n\n**Hinweis**: Tsunade besteht darauf - Ablehnung nicht möglich"

        return full_dialog

    def _start_family_time_session(self, session: FamilyTimeSession):
        """Startet die eigentliche Familienzeit-Session"""

        # Update Tracking
        if hasattr(self.game_data, 'time_system'):
            self.last_family_time = self.game_data.time_system.get_current_game_time()
        else:
            self.last_family_time = datetime.now()

        self.family_time_streak += 1
        self.missed_family_times = 0  # Reset

        # Setze Family Time Status
        self.game_data.active_family_time = session
        self.game_data.family_time_active = True

        print(f"👨‍👩‍👧 Family Time gestartet: {session.activity.value} ({session.duration_minutes} min)")

    def handle_family_time_response(self, response: str) -> str:
        """Behandelt Sukunas Antwort auf Familienzeit-Vorschlag"""

        response_lower = response.lower()
        active_session = getattr(self.game_data, 'active_family_time', None)

        if not active_session:
            return "❌ Keine aktive Familienzeit-Anfrage"

        # AKZEPTANZ
        if any(word in response_lower for word in ["ja", "gerne", "okay", "accept"]):
            return self._accept_family_time(active_session)

        # ABLEHNUNG
        elif any(word in response_lower for word in ["nein", "nicht", "später", "decline"]):
            return self._decline_family_time(active_session)

        # NEUTRAL/MITMACHEN
        else:
            return self._neutral_family_time_participation(active_session, response)

    def _accept_family_time(self, session: FamilyTimeSession) -> str:
        """Sukuna akzeptiert Familienzeit"""

        acceptance_responses = [
            f"*Tsunade strahlt* 'Wunderbar! Ich liebe es wenn wir Zeit zusammen verbringen.'",
            f"*liebevolle Umarmung* 'Das macht Mama sehr glücklich, mein kleiner Wolf.'",
            f"*zufriedenes Lächeln* 'So gehört sich das in einer Familie.'"
        ]

        base_response = random.choice(acceptance_responses)

        # Starte Activity
        activity_start = random.choice(session.special_dialogue)

        # Relationship Bonus
        if hasattr(self.game_data, 'relationship_system'):
            try:
                self.game_data.relationship_system.change_relationship(
                    'tsunade', +3, 'Familienzeit akzeptiert', show_message=False
                )
            except:
                pass

        return f"{base_response}\n\n{activity_start}\n\n💝 +3 Beziehung mit Tsunade (Familienzeit geschätzt)"

    def _decline_family_time(self, session: FamilyTimeSession) -> str:
        """Sukuna lehnt Familienzeit ab"""

        # Prüfe ob Ablehnung erlaubt
        if session.priority == FamilyTimePriority.MANDATORY:
            return self._handle_mandatory_decline(session)

        # Normale Ablehnung
        self.missed_family_times += 1

        decline_responses = [
            f"*Tsunade sieht enttäuscht aus* 'Oh... na gut. Später dann vielleicht.'",
            f"*seufzt leicht* 'Ich verstehe. Du brauchst deinen Raum.'",
            f"*traurig aber verständnisvoll* 'Okay, mein Schatz. Aber wir holen es nach.'"
        ]

        response = random.choice(decline_responses)

        # Relationship Impact
        if hasattr(self.game_data, 'relationship_system'):
            try:
                self.game_data.relationship_system.change_relationship(
                    'tsunade', -1, 'Familienzeit abgelehnt', show_message=False
                )
            except:
                pass

        # Warnung bei mehrfachen Ablehnungen
        if self.missed_family_times >= 3:
            response += f"\n\n💭 *Tsunade wirkt zunehmend besorgt über mangelnde Familienzeit*"

        return f"{response}\n\n💔 -1 Beziehung mit Tsunade"

    def _handle_mandatory_decline(self, session: FamilyTimeSession) -> str:
        """Behandelt Ablehnung von Pflicht-Familienzeit"""

        mandatory_responses = [
            f"*Tsunade wird sanft aber bestimmt* 'Nein, Sukuna. Das ist nicht verhandelbar.'",
            f"*liebevoll aber fest* 'Ich bin deine Mama. Manchmal entscheide ich, was gut für dich ist.'",
            f"*mütterliche Autorität* 'Du hast keine Wahl, mein kleiner Wolf. Familie ist wichtig.'"
        ]

        response = random.choice(mandatory_responses)

        # Force Start
        activity_start = random.choice(session.special_dialogue)

        return f"{response}\n\n{activity_start}\n\n💭 *Tsunade lässt heute keine Ausreden gelten*"

    def _neutral_family_time_participation(self, session: FamilyTimeSession, user_input: str) -> str:
        """Sukuna macht einfach mit, ohne explizit zu akzeptieren"""

        participation_responses = [
            f"*Tsunade lächelt zufrieden* 'So ist es richtig, mein Schatz.'",
            f"*nimmt dich liebevoll in den Arm* 'Ich liebe diese Momente mit dir.'",
            f"*genießt die gemeinsame Zeit* 'Das ist was Familie ausmacht, Sukuna.'"
        ]

        base_response = random.choice(participation_responses)
        activity_continue = random.choice(session.special_dialogue)

        return f"{base_response}\n\n{activity_continue}"

    def get_family_time_summary(self) -> str:
        """📊 Zeigt Family Time System Status"""

        summary = "👨‍👩‍👧 **FAMILY TIME SYSTEM STATUS:**\n\n"

        if self.last_family_time:
            days_ago = "heute" if self._had_family_time_today() else f"vor {(datetime.now() - self.last_family_time).days} Tagen"
            summary += f"🕐 **Letzte Familienzeit**: {days_ago}\n"
        else:
            summary += f"🕐 **Letzte Familienzeit**: Noch nie\n"

        summary += f"🔥 **Familienzeit-Streak**: {self.family_time_streak}\n"
        summary += f"❌ **Verpasste Tage**: {self.missed_family_times}\n"

        # Tsunades Status
        if self.missed_family_times == 0:
            tsunade_mood = "😊 Zufrieden"
        elif self.missed_family_times <= 2:
            tsunade_mood = "😐 Leicht besorgt"
        else:
            tsunade_mood = "😟 Besorgt über mangelnde Familienzeit"

        summary += f"👩 **Tsunades Stimmung**: {tsunade_mood}\n\n"

        # Nächste mögliche Familienzeit
        if hasattr(self.game_data, 'time_system'):
            time_system = self.game_data.time_system
            current_hour = time_system.get_current_game_time().hour

            if current_hour < 18:
                summary += f"⏰ **Nächste Familienzeit**: Heute Abend ab 18:00\n"
            elif 18 <= current_hour <= 21:
                summary += f"⏰ **Familienzeit**: JETZT möglich!\n"
            else:
                summary += f"⏰ **Nächste Familienzeit**: Morgen Abend\n"

        # Verfügbare Aktivitäten
        summary += f"\n🎭 **Verfügbare Aktivitäten**:\n"
        for name, session in self.family_time_sessions.items():
            priority_emoji = {"mandatory": "🔴", "suggested": "🟡", "optional": "🟢"}.get(session.priority.value, "⚪")
            summary += f"• {priority_emoji} {session.activity.value.replace('_', ' ').title()} ({session.duration_minutes} min)\n"

        return summary


def integrate_family_time_system(game_data):
    """👨‍👩‍👧 Integriert das Family Time System - VOLLSTÄNDIG KORRIGIERT"""

    # Erstelle Family Time System
    family_system = FamilyTimeSystem(game_data)
    game_data.family_time_system = family_system

    # Erweitere LLM Response für Family Time Integration
    if hasattr(game_data, 'get_llm_response'):
        original_get_llm_response = game_data.get_llm_response

        def family_time_enhanced_llm_response(user_input: str) -> str:
            """LLM Response mit Family Time Logic - RECURSION & FORMATIERUNG GEFIXT"""

            # 🛡️ RECURSION GUARD
            if hasattr(game_data, '_in_family_time_llm') and game_data._in_family_time_llm:
                print("🚨 Family Time LLM Recursion verhindert!")
                return original_get_llm_response(user_input)

            game_data._in_family_time_llm = True

            try:
                # Prüfe ob Family Time Response
                if hasattr(game_data, 'family_time_active') and game_data.family_time_active:
                    family_response = family_system.handle_family_time_response(user_input)
                    if family_response and "❌" not in family_response:
                        return family_response

                # Normale Response (GEFIXT: original_get_llm_response statt game_data.get_llm_response)
                base_response = original_get_llm_response(user_input)

                # Prüfe Family Time Trigger (nur für Tsunade)
                current_character = getattr(game_data, 'active_character', 'tsunade')

                if current_character == 'tsunade':
                    family_trigger = family_system.check_family_time_trigger()

                    if family_trigger and random.random() < 0.4:  # 40% Chance
                        family_initiation = family_system.initiate_family_time(family_trigger)
                        # Als separate GUI-Nachricht, NICHT in die AI-Antwort gemischt:
                        if hasattr(game_data, 'gui') and game_data.gui:
                            game_data.gui.display_message("👨‍👩‍👧 Familienzeit", family_initiation, "info")

                return base_response

            finally:
                # Reset Guard (IMMER ausgeführt)
                game_data._in_family_time_llm = False

        # ✅ WICHTIG: Diese Zeile war fehlend und machte die Funktion grau!
        game_data.get_llm_response = family_time_enhanced_llm_response

    print("👨‍👩‍👧 FAMILY TIME SYSTEM erfolgreich integriert!")
    print("💝 Features aktiviert:")
    print("   • Abendliche Pflicht-Familienzeit")
    print("   • Tsunade besteht auf gemeinsame Zeit")
    print("   • 7 verschiedene Familienaktivitäten")
    print("   • Tracking von Familienzeit-Streak")
    print("   • Emotionale Konsequenzen bei Vernachlässigung")
    print("   🛡️ RECURSION-SICHER!")

    return family_system

if __name__ == "__main__":
    print("👨‍👩‍👧 FAMILY TIME SYSTEM")
    print("========================")
    print("✅ Tsunade besteht auf Familienzeit")
    print("✅ 7 verschiedene Familienaktivitäten")
    print("✅ Pflicht-Zeiten und optionale Zeiten")
    print("✅ Emotionale Tracking und Konsequenzen")