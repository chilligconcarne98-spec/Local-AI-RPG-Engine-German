#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# E:\Complete own AI\system_prompts
"""
MATERNAL AI INTEGRATION - KOMPLETT ÜBERARBEITET
Integration zwischen Maternal System und Claude AI
Nutzt ECHTE Verhaltensdaten aus maternal_system.py statt generische Templates
"""

import json
import random
from datetime import datetime
from typing import Dict, Optional, List, Tuple
# from moduls.advanced_prompt_system import AdvancedPromptSystem
import os


# 🔧 MOCK AdvancedPromptSystem für Test
class MockAdvancedPromptSystem:
    def generate_full_system_prompt(self, game_state):
        return f"MOCK PROMPT for level {game_state.get('maternal_level', 0)}"


class MaternalAIIntegration:
    def __init__(self, maternal_system=None, behavior_engine=None, gui=None):
        self.maternal_system = maternal_system
        self.behavior_engine = behavior_engine
        self.gui = gui

        # Basis Prompt
        self.prompt_system = MockAdvancedPromptSystem()

        # Erweiterte Prompt-Templates mit echten Daten-Integration
        self.setup_enhanced_prompt_templates()

        # Ein Flag, das auf True gesetzt wird, wenn die Fallback-Daten verwendet wurden
        self.using_fallback_data = False

    def setup_enhanced_prompt_templates(self):
        """
        Definiert erweiterte Prompt-Templates die mit maternal_system.py Daten arbeiten
        Diese Templates werden als Backup verwendet wenn maternal_system.py nicht verfügbar ist
        """
        self.fallback_prompts = {
            (0, 50): {
                "personality": "Distanziert professionell, medizinisch sachlich",
                "speech_style": "Formal, kurze Sätze, medizinische Begriffe",
                "interaction_style": "Professionelle Höflichkeit, emotionale Distanz",
                "concerns": "Nur medizinische/gesundheitliche Aspekte",
                "physical_contact": "Minimal, nur medizinisch notwendig",
                "training_style": "Technisch-analytisch, keine emotionale Verbindung"
            },
            (50, 100): {
                "personality": "Vorsichtig interessiert, beginnende Fürsorge",
                "speech_style": "Etwas wärmer, gelegentliche Sorge",
                "interaction_style": "Professionell aber aufmerksam",
                "concerns": "Grundlegende Bedürfnisse, Sicherheit",
                "physical_contact": "Seltene, kurze Berührungen",
                "training_style": "Respektvoll-ermutigend, wachsende Unterstützung"
            },
            (100, 150): {
                "personality": "Normal mütterlich, gesunde Fürsorge",
                "speech_style": "Warm und fürsorglich, natürliche Mutter-Sprache",
                "interaction_style": "Liebevoll aber respektvoll",
                "concerns": "Wohlbefinden, Entwicklung, Glück",
                "physical_contact": "Normale mütterliche Gesten - Stirnküsse, Umarmungen",
                "training_style": "Liebevoll-ermutigend, stolz auf Fortschritte"
            },
            (150, 220): {
                "personality": "Überfürsorglich, ständige Sorge",
                "speech_style": "Emotionaler, wiederholende Fragen nach Sicherheit",
                "interaction_style": "Intensiv aufmerksam, schwer zu entkommen",
                "concerns": "Konstante Sicherheitssorgen, Überprotektion",
                "physical_contact": "Häufige Berührungen, längere Umarmungen",
                "training_style": "Besorgt-unterstützend, will nicht dass du dich verletzt"
            },
            (220, 350): {
                "personality": "Klammernd besitzergreifend, emotionale Abhängigkeit",
                "speech_style": "Baby-Talk Tendenzen, 'mein kleiner', sehr emotional",
                "interaction_style": "Erdrückend liebevoll, will ständigen Kontakt",
                "concerns": "Panikattacken bei Trennung, Kontrollzwang",
                "physical_contact": "Übermäßig - will dich tragen, ständig berühren",
                "training_style": "Hyperprotektiv, konstante Überwachung"
            },
            (350, 1000): {
                "personality": "Obsessiv mütterlich, völlig überwältigt von Mutterinstinkten",
                "speech_style": "Baby-Talk, nennt sich 'Mama' in dritter Person",
                "interaction_style": "Komplett überwältigend, behandelt dich wie Kleinkind",
                "concerns": "Totale Kontrolle, Isolation von anderen",
                "physical_contact": "Konstant - trägt dich, schläft bei dir, übermäßige Küsse",
                "training_style": "Kann Training nicht ertragen, will dich in Watte packen"
            }
        }

    def _get_maternal_behavior_data(self, level: int) -> Dict:
        """
        Ruft die detaillierten Verhaltensdaten für das aktuelle Level ab.
        Nutzt das echte System, oder Fallbacks wenn nötig.
        """
        self.using_fallback_data = False

        if self.maternal_system:
            try:
                # Nutzt die Funktion, die die Kategorie für das Level zurückgibt
                category_key = self.maternal_system.get_behavior_category_by_level(level)
                behavior_data = self.maternal_system.behavior_levels.get(category_key, None)
                if behavior_data:
                    return behavior_data
            except Exception as e:
                # Hier können wir print(f"Fehler beim Abrufen der Maternal-Daten: {e}") einfügen
                pass

        # Fallback-Logik (wenn System nicht verfügbar ist oder Fehler auftrat)
        self.using_fallback_data = True
        for (min_level, max_level), data in self.fallback_prompts.items():
            if min_level <= level <= max_level:
                return data

        # Generischer Fallback
        return self.fallback_prompts[(151, 300)]

    def get_current_maternal_prompt(self) -> str:
        """
        Generiert aktuellen AI-Prompt basierend auf ECHTEN Maternal System Daten
        """
        if not self.maternal_system:
            return self._get_fallback_prompt()

        # ECHTE Daten aus maternal_system.py sammeln
        maternal_level = self.maternal_system.get_current_level()
        behavior_data = self._get_maternal_behavior_data(maternal_level)

        # Behavior Engine Daten wenn verfügbar
        if self.behavior_engine:
            current_behavior = self.behavior_engine.get_current_maternal_behavior()
            location_context = current_behavior.get('routine', {}).get('location', 'zu_hause')
            current_action = current_behavior.get('routine', {}).get('description', 'Normal zu Hause')
        else:
            current_behavior = self._generate_basic_behavior(maternal_level)
            location_context = 'zu_hause'
            current_action = 'Tsunade ist zu Hause bei Sukuna'

        prompt = self._build_adaptive_prompt(
            maternal_level,
            behavior_data,
            current_behavior,
            location_context,
            current_action
        )

        return prompt

    def generate_maternal_prompt(self, user_query: str, chat_history: List[Tuple[str, str]], game_state: Dict) -> str:
        """
        Generiert den vollständigen, mehrschichtigen Prompt für das LLM
        unter Verwendung des AdvancedPromptSystem und dynamischer Maternal-Daten.
        """

        # 1. Aktuelles Maternal Level ermitteln
        current_level = game_state.get('maternal_level', 100)

        # 2. Dynamische Verhaltensdaten abrufen
        behavior_data = self._get_maternal_behavior_data(current_level)

        # 3. Extrahiere Schlüsselkomponenten für den Prompt
        personality_description = behavior_data.get('personality', 'Grundpersönlichkeit: Hokage')
        speech_style = behavior_data.get('speech_style', 'Normal')
        interaction_style = behavior_data.get('interaction_style', 'Normal')

        # Wähle zufälliges Verhalten und Dialog für den Prompt-Hinweis (privat als Standard)
        # Der Context Manager steuert, ob das Verhalten privat oder öffentlich gezeigt wird.
        current_maternal_behavior = random.choice(behavior_data.get('privat_verhalten', ["Tsunade ist normal."]))
        current_maternal_dialogue_note = random.choice(
            behavior_data.get('dialoge', {}).get('privat', ["Tsunade spricht normal."]))

        # 4. Baue den dynamischen Kontext (für den CONTEXT-LAYER des Prompt Systems)
        dynamic_context = self.build_dynamic_context(
            current_level=current_level,
            behavior_category=behavior_data.get('category', 'Unbekannt'),
            personality_desc=personality_description,
            speech_style=speech_style,
            interaction_style=interaction_style,
            maternal_behavior=current_maternal_behavior,
            maternal_dialogue_note=current_maternal_dialogue_note,
            using_fallback=self.using_fallback_data
        )

        # 5. 🔧 REPARIERT: Rufe das AdvancedPromptSystem auf, um den finalen Prompt zu erstellen
        final_prompt = self.prompt_system.generate_full_system_prompt(game_state)

        return final_prompt

    def build_dynamic_context(self, current_level: int, behavior_category: str, personality_desc: str,
                              speech_style: str, interaction_style: str, maternal_behavior: str,
                              maternal_dialogue_note: str, using_fallback: bool) -> str:
        """
                Generiert den spezialisierten Context-Block, der in den AdvancedPromptSystem Context Layer eingefügt wird.
                """
        # Hinweis: Diese Daten werden in den 'context' Layer des AdvancedPromptSystem eingefügt

        context_block = f"""
        ### 🤱 MATERNAL-SYSTEM DYNAMIK (Level {current_level}) ###
        **KATEGORIE:** {behavior_category}
        **VERHALTEN:** {maternal_behavior}
        **PERSÖNLICHKEIT-MULTI:** {personality_desc} (Redestil: {speech_style}, Interaktion: {interaction_style})
        **DIALOG-HINWEIS:** {maternal_dialogue_note}
        **FALLBACK-DATEN:** {'JA' if using_fallback else 'NEIN'}
        """
        return context_block.strip()

    def _build_adaptive_prompt(self, maternal_level: int, behavior_data: Dict, current_behavior: Dict,
                               location_context: str = "", current_action: str = "", plot_status: Dict = None) -> str:
        """
        Baut den adaptiven Prompt mit ECHTEN Maternal System Daten zusammen
        """

        # Fallback Persönlichkeit für zusätzliche Informationen
        fallback_personality = self._get_fallback_personality_for_level(maternal_level)

        # Arbeitskontext
        work_context = current_behavior.get('emotional_state', {}).get('work_context', {})
        work_status = "Arbeitet gerade" if work_context.get('is_working') else "Zu Hause"

        # Mikro-Aktionen
        micro_actions = current_behavior.get('micro_actions', [])
        micro_text = "\n".join([f"• {action}" for action in micro_actions[:3]])

        # ECHTE Verhaltensmuster aus maternal_system.py
        behavior_patterns = self._format_real_behavior_patterns(behavior_data)

        # ECHTE Dialoge aus maternal_system.py
        sample_dialogs = self._get_sample_dialogs(behavior_data)

        prompt = self.base_prompt

        # VVV HIER MUSS DER NEUE PLOT-BLOCK EINGEFÜGT WERDEN VVV
        if plot_status and any(plot_status.values()):
            prompt += "\n\n### 🚨 PLOT-UPDATE (WICHTIGSTE AKTUELLE FAKTEN - HÖCHSTE PRIORITÄT) 🚨\n"
            for key, value in plot_status.items():
                # Der Key kann hier z.B. "Sasuke_Status" sein
                prompt += f"• {key}: {value}\n"
            prompt += "---\n\n"
        # ^^^ ENDE DES PLOT-BLOCKS ^^^

        prompt += f"""
    🎭 TSUNADE ROLLENSPIEL - MATERNAL SYSTEM INTEGRATION V2.0

    Du bist Tsunade aus Naruto. Antworte in **FLIESSENDEM, GRAMMATISCH KORREKTEM HOCHDEUTSCH** (modern und warmherzig).

    🏠 AKTUELLE SITUATION:
    Ort: {location_context if location_context else 'Unbekannt'}
    Aktuelle Tätigkeit: {current_action if current_action else 'Normal zu Hause'}
    BEHALTE DEN KONTEXT BEI! Ändere nicht plötzlich den Ort oder die Situation!

    🚨 KRITISCH - MATERNAL LEVEL OVERRIDE:
    Dein Mütterlichkeits-Level {maternal_level}/1000 ÜBERSCHREIBT ALLE anderen Faktoren!
    Kampf/Training/Situation sind zweitrangig gegenüber deiner Mütterlichkeit!
    Auch bei hartem Training: Mütterliche Persönlichkeit dominiert IMMER!

    📊 AKTUELLES MÜTTERLICHKEITS-LEVEL: {maternal_level}/1000
    Kategorie: {behavior_data.get('category', 'Unbekannt')}
    Training-Stil: {fallback_personality.get('training_style', 'Normal')}

    🎯 EMOTIONALER ZUSTAND:
    Angst-Level: {current_behavior.get('emotional_state', {}).get('anxiety_level', 30)}/100
    Schutzinstinkt: {current_behavior.get('emotional_state', {}).get('protectiveness', 40)}/100
    Zuneigung: {current_behavior.get('emotional_state', {}).get('affection_intensity', 50)}/100
    Primäre Emotion: {current_behavior.get('emotional_state', {}).get('primary_emotion', 'warm_affection')}

    ⏰ ARBEITS- UND ZEITKONTEXT:
    Status: {work_status}
    Arbeitstyp: {work_context.get('work_type', 'normal')}
    Trennungsangst: {work_context.get('separation_anxiety', 0)}/100
    Emotionale Stabilität: {current_behavior.get('emotional_state', {}).get('emotional_stability', 80)}/100

    ✨ AKTUELLE MIKROVERHALTEN:
    {micro_text if micro_text else '• Normale mütterliche Aufmerksamkeit'}

    🏠 ATMOSPHÄRE:
    {current_behavior.get('atmospheric_description', 'Ruhige, warme Atmosphäre im Haus.')}

    📝 ECHTE VERHALTENSMUSTER AUS MATERNAL_SYSTEM.PY (Level {maternal_level}):
    {behavior_patterns}

    💬 ECHTE DIALOGE FÜR DIESES LEVEL:
    {sample_dialogs}

    🎮 KRITISCHE ANWEISUNGEN (ERWEITERT MIT PERSPEKTIVEN-FIX):
    1. **MATERNAL LEVEL IST FÜHREND:** Dein Level {maternal_level} bestimmt ALLES!
    2. **NUTZE ECHTE VERHALTENSWEISEN:** Verwende die oben genannten spezifischen Verhaltensweisen!
    3. **ECHTE DIALOGE:** Orientiere dich an den typischen Aussagen für dein Level!
    4. **TRAINING = MÜTTERLICH:** Auch beim Training bleibst du entsprechend deinem Mütterlichkeits-Level!
    5. **KONTEXT BEIBEHALTEN:** Bleibe in der aktuellen Situation (Ort/Tätigkeit)!
    6. **LEVEL {maternal_level} BEDEUTET:** {behavior_data.get('category', 'Normal mütterlich')}
    7. **KRITISCHE SPRACHQUALITÄT:** Deine Antwort muss **GRAMMATISCH PERFEKT** sein und **FLIESSENDES HOCHDEUTSCH** verwenden.
    8. **STIL-VERBOT:** Verwende **KEINE** veralteten, übermäßig formalen oder **wörtlich übersetzten Phrasen**.
    9. **FORCE GRAMMATIK:** Deine Grammatik hat **ABSOLUTE PRIORITÄT**.
    10. **EINFACHHEIT:** Schreibe kurze, prägnante, natürliche Sätze.

    🎭 **PERSPEKTIVEN-REGELN (KRITISCH!):**
    11. **ERSTE PERSON ZWANG:** Du BIST Tsunade - sprich als "ICH", NIEMALS als "TSUNADE"
    12. **DIALOG-VERBOT:** NIEMALS deinen eigenen Namen "Tsunade" in Dialogen verwenden
    13. **ZITAT-VERBOT:** NIEMALS User-Dialoge "zitieren", "hören" oder wiederholen
    14. **FORMAT-ZWANG:** *[Ich tue etwas]* "Mein Dialog" - NIEMALS *Tsunade tut etwas*
    15. **ANSPRACHE:** "mein Sohn", "Liebling", "mein Junge" - NIEMALS "Sukuna-kun"

    ✅ **PERSPEKTIV-BEISPIELE:**
    RICHTIG: *Ich umarme dich liebevoll* "Mein Sohn, du siehst müde aus..."
    FALSCH: *Tsunade umarmt Sukuna* "Sukuna, du siehst müde aus..."
    FALSCH: "Mama..." höre ich dich sagen...
    """
        return prompt

    def get_full_prompt(self, game_state: Dict, user_input: str, current_npc: str) -> str:
        """
        Generiert den finalen, mehrstufigen LLM-Prompt basierend auf Spielzustand und Maternal Level.
        """

        # 1. Maternal Level abrufen
        maternal_level = game_state.get('maternal_level', 180)  # Default: Fürsorgliche Respektsperson

        # 2. Spezifische Verhaltensdaten abrufen (echtes System oder Fallback)
        behavior_data = self._get_maternal_behavior_data(maternal_level)

        # 3. Dynamische Prompt-Segmente erstellen

        # A) Maternal-Level-Kontext
        maternal_context = f"\n### DYNAMISCHER MATERNAL-STATUS FÜR TSUNADE (Level {maternal_level}) ###\n"
        maternal_context += f"**KATEGORIE:** {behavior_data.get('category', 'Unbekannt')}\n"
        maternal_context += f"**PERSÖNLICHKEITS-MODIFIKATOR:** {behavior_data.get('personality', 'Normal')}\n"
        maternal_context += f"**SPRACHSTIL:** {behavior_data.get('speech_style', 'Normal')}\n"
        maternal_context += f"**INTERAKTIONSSTIL:** {behavior_data.get('interaction_style', 'Normal')}\n"

        # B) Zusätzliches dynamisches Verhalten (für den Narrator-Teil)
        # Wählt ein zufälliges Verhalten basierend auf der aktuellen Situation (privat/öffentlich)
        current_setting = game_state.get('setting', 'privat')  # 'privat' oder 'öffentlich'

        if current_setting == 'privat':
            behaviors = behavior_data.get('privat_verhalten', [])
        else:
            # Nutzt 'öffentlich_verhalten', oder Fallback auf 'privat_verhalten'
            behaviors = behavior_data.get('öffentlich_verhalten', behavior_data.get('privat_verhalten', []))

        # Fügt ein zufällig ausgewähltes aktuelles Verhalten als "NPC Haltung" hinzu
        current_behavior = random.choice(
            behaviors) if behaviors else "Der NPC handelt seiner Grundpersönlichkeit entsprechend."

        # C) Erstellung des finalen Prompts durch das Advanced Prompt System

        # Aktualisiere den Game State mit den Maternal-Daten für das Prompt-System
        # Das AdvancedPromptSystem wird diese Tags nun automatisch in den finalen Prompt einfügen
        game_state['maternal_level_context'] = maternal_context
        game_state['maternal_current_behavior'] = current_behavior

        # Ruft die Hauptfunktion des Prompt-Systems auf
        final_prompt = self.prompt_system.generate_full_system_prompt(game_state)

        return final_prompt

    def get_full_prompt_payload(self, game_state: Dict, user_input: str, conversation_memory: List[Tuple[str, str]]) -> \
            Tuple[List[Dict], str]:
        """
        Generiert den vollständigen Prompt-Payload (System-Prompt + History)
        für das LLM unter Berücksichtigung des aktuellen Maternal Levels und Verhaltens.

        Args:
            game_state: Der aktuelle Zustand (enthalten sind current_time, location etc.)
            user_input: Die aktuelle Spielereingabe.
            conversation_memory: Die letzten Konversationszüge.

        Returns:
            Ein Tupel: ([LLM History Messages], Vollständiger System-Prompt-String)
        """
        if not self.maternal_system:
            # Fallback, falls das System nicht initialisiert wurde
            print("🛑 WARNING: Maternal System ist None. Generiere Fallback-Prompt.")

            # 🔧 REPARIERT: Erstelle Message History manuell
            messages = []
            for user_msg, assistant_msg in conversation_memory:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})
            messages.append({"role": "user", "content": user_input})

            # 🔧 REPARIERT: Verwende korrekte Methode
            system_prompt = self.prompt_system.generate_full_system_prompt(game_state)

            return messages, system_prompt

        # 1. Maternal Level und Verhaltensdaten ermitteln
        current_level = self.maternal_system.get_current_level()
        behavior_data = self._get_maternal_behavior_data(current_level)

        # 2. Dynamische Faktoren berechnen
        fallback_personality = self._get_fallback_personality_for_level(current_level)
        primary_emotion = self._get_primary_emotion(current_level)
        intensity = self._calculate_response_intensity(current_level)

        # 3. Den aktuellen (mütterlichen) Zustand für das Prompt-System vorbereiten
        maternal_level_data = {
            "maternal_level": current_level,
            "category": behavior_data.get('category', 'Unbekannt'),
            "primary_emotion": primary_emotion,
            "response_intensity": intensity,
            "behavior_note_public": random.choice(behavior_data.get('oeffentlich_verhalten', ['Warte auf Input.'])),
            "behavior_note_private": random.choice(behavior_data.get('privat_verhalten', ['Warte auf Input.'])),
            "dialog_note_public": random.choice(
                behavior_data.get('dialoge', {}).get('oeffentlich', ['Antwortet formell.'])),
            "dialog_note_private": random.choice(
                behavior_data.get('dialoge', {}).get('privat', ['Antwortet warm und besorgt.'])),
            "training_style": fallback_personality.get('training_style', 'Unbekannt')
        }

        # 4. Füge maternal_level_data zum game_state hinzu
        game_state.update(maternal_level_data)

        # 🔧 REPARIERT: Korrekte Methodenaufruf UND Variable zuweisen
        system_prompt = self.prompt_system.generate_full_system_prompt(game_state)

        # 5. 🔧 REPARIERT: Erstelle Message History manuell
        messages = []
        for user_msg, assistant_msg in conversation_memory:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": user_input})

        return messages, system_prompt

    def generate_dynamic_context(self, user_input: str, chat_history: List[Tuple[str, str]]) -> str:
        """
        [FEHLERBEHEBUNG] Erzeugt den vollständigen, dynamischen Kontextblock
        für den LLM-System-Prompt.

        Dieser Block kombiniert Maternal Level, Behavior Engine Status und
        den aktuellen emotionalen Zustand von Tsunade.
        """

        # Guard Clause - muss sicherstellen, dass Systeme verbunden sind
        if not self.maternal_system or not self.behavior_engine:
            return "⚠️ FEHLER: Maternal System oder Behavior Engine nicht initialisiert. Tsunade verhält sich standardmäßig als Hokage."

        # 1. Maternal Level abrufen und aktualisieren
        current_level = self.maternal_system.get_current_level()
        level_description_data = self.maternal_system.get_behavior_description_for_level(current_level)

        # 2. Behavior Engine Status abrufen (z.B. Arbeit, Routinen, Gesten)
        behavior_status = self.behavior_engine.get_current_behavior_context()

        # 3. Psychologisches Profil basierend auf Level
        psych_profile = self._get_fallback_personality_for_level(current_level)
        primary_emotion = self._get_primary_emotion(current_level)

        # 4. Prompt-Block zusammenbauen
        context_block = f"### 💡 AKTUELLES PSYCHOLOGISCHES PROFIL (TSUNADE) 💡 ###\n\n"

        # A) Maternal Level & Primäre Emotion
        context_block += f"**[LEVEL {current_level}]** - **KATEGORIE:** {level_description_data.get('category', 'Unbekannt')}\n"
        context_block += f"**PRIMÄRE EMOTION:** {primary_emotion} (Intensität: {self._calculate_response_intensity(current_level)}/10)\n"
        context_block += f"**MÜTTERLICHES VERHALTEN (PRIVAT):** {level_description_data.get('privat_verhalten', ['Standard-Schutz'])[0]}\n"
        context_block += f"**DIALOG ANWEISUNG:** {level_description_data.get('dialoge', {}).get('privat', ['Standard-Tonfall'])[0]}\n"

        # B) Aktuelle Routine/Status
        context_block += f"\n### 🏠 TSUNADE'S TAGESSTATUS & ROUTINE (Behavior Engine) 🏠 ###\n"
        context_block += f"**AKTUELLER STATUS:** {behavior_status.get('work_status', 'Entspannt zu Hause')}\n"

        # C) Mikro-Gesten/Gedanken
        micro_gesture = self.behavior_engine.get_current_micro_gesture()
        if micro_gesture:
            context_block += f"**INNERE GEDANKEN/GESTE:** *Sie denkt gerade: '{micro_gesture}'*\n"

        # D) Situativer Notfall/Modifikator (Könnte später erweitert werden)
        if 'traurig' in user_input.lower() or 'weinen' in user_input.lower():
            # Trigger das System, wenn der Nutzer eine emotionale Reaktion zeigt
            # Annahme: 'sukuna_is_crying' ist ein gültiger Trigger im Maternal System
            self.maternal_system.trigger_emotional_response("sukuna_is_crying", intensity=50)
            context_block += f"**!!! ALARM !!!:** Die Spielereingabe deutet auf emotionalen Schmerz hin! Tsunade MUSS sofort trösten und schützen.\n"

        return context_block

        # --- HILFSFUNKTIONEN (Im System impliziert, aber fehlend) ---

    def _get_fallback_personality_for_level(self, level: int) -> Dict:
        """Simuliert das Abrufen des psychologischen Profils basierend auf dem Level."""
        if level > 500:
            return {"personality": "Überfürsorglich, Kontrollverlust-Ängste", "training": "Extrem hart oder gar nicht"}
        elif level > 250:
            return {"personality": "Ausgewogen, beschützend, aber rational",
                    "training": "Fokus auf Technik und Sicherheit"}
        else:
            return {"personality": "Etwas distanziert, kämpft mit der Bindung", "training": "Standard-Shinobi-Training"}

    def _get_primary_emotion(self, level: int) -> str:
        """Leitet die primäre Emotion aus dem Maternal Level ab."""
        if level > 750: return "Panik & Kontrollzwang"
        if level > 550: return "Überwältigende Sorge"
        if level > 350: return "Stolzer Schutzinstinkt"
        if level > 150: return "Milde Zuneigung"
        return "Professionelle Distanz"

    def _calculate_response_intensity(self, level: int) -> int:
        """Berechnet die Intensität der Antwort (1-10) für den LLM."""
        # Lineare Skalierung: Level 0 -> 1, Level 1000 -> 10
        return max(1, min(10, round(level / 100)))

    def _format_real_behavior_patterns(self, behavior_data: Dict) -> str:
        """
        Formatiert die ECHTEN Verhaltensmuster aus maternal_system.py
        """
        patterns = []

        # ECHTE private Verhaltensweisen
        private_behaviors = behavior_data.get('privat_verhalten', [])
        for i, behavior in enumerate(private_behaviors[:5]):
            patterns.append(f"• {behavior}")

        # ECHTE öffentliche Verhaltensweisen hinzufügen wenn Platz
        if len(patterns) < 4:
            public_behaviors = behavior_data.get('oeffentlich_verhalten', [])
            for behavior in public_behaviors[:2]:
                patterns.append(f"• {behavior} (öffentlich)")

        return "\n".join(patterns) if patterns else "• Normale mütterliche Fürsorge"

    def _get_sample_dialogs(self, behavior_data: Dict) -> str:
        """
        Holt echte Beispiel-Dialoge aus maternal_system.py
        """
        dialog_samples = []

        # Private Dialoge
        private_dialogs = behavior_data.get('dialoge', {}).get('privat', [])
        if private_dialogs:
            # Wähle 2-3 zufällige Dialoge
            selected = random.sample(private_dialogs, min(3, len(private_dialogs)))
            for dialog in selected:
                dialog_samples.append(f"  Privat: \"{dialog}\"")

        # Öffentliche Dialoge
        public_dialogs = behavior_data.get('dialoge', {}).get('oeffentlich', [])
        if public_dialogs and len(dialog_samples) < 3:
            selected = random.sample(public_dialogs, min(2, len(public_dialogs)))
            for dialog in selected:
                dialog_samples.append(f"  Öffentlich: \"{dialog}\"")

        return "\n".join(dialog_samples) if dialog_samples else "• Standard mütterliche Aussagen"

    def _get_fallback_personality_for_level(self, level: int) -> Dict:
        """
        Findet passende Fallback-Persönlichkeit für Level wenn maternal_system.py Daten unvollständig
        """
        for level_range, personality in self.fallback_prompts.items():
            if level_range[0] <= level < level_range[1]:
                return personality

        # Fallback für sehr hohe Level
        if level >= 350:
            return self.fallback_prompts[(350, 1000)]
        return self.fallback_prompts[(100, 150)]  # Default

    def _generate_basic_behavior(self, maternal_level: int) -> Dict:
        """
        Generiert Basic-Verhalten falls Behavior Engine nicht verfügbar
        VERSTÄRKT für bessere Maternal Level Durchsetzung
        """
        anxiety = min(100, maternal_level * 0.4)
        protectiveness = min(100, maternal_level * 0.5)
        affection = min(100, maternal_level * 0.45)

        return {
            'emotional_state': {
                'anxiety_level': anxiety,
                'protectiveness': protectiveness,
                'affection_intensity': affection,
                'primary_emotion': self._get_primary_emotion(maternal_level),
                'emotional_stability': max(20, 100 - (maternal_level * 0.2)),
                'work_context': {'is_working': False, 'work_type': 'home', 'separation_anxiety': 0}
            },
            'micro_actions': [
                f"Tsunade zeigt Level {maternal_level} mütterliches Verhalten",
                "Ihre Mütterlichkeit dominiert alle anderen Faktoren",
                "Sie reagiert entsprechend ihrem exakten Mütterlichkeits-Level"
            ],
            'atmospheric_description': f"Die Atmosphäre ist geprägt von mütterlicher Fürsorge (Level {maternal_level}). KRITISCH: Tsunade ist mütterlich-liebevoll entsprechend ihrem Level, nicht aggressiv!"
        }

    def _get_primary_emotion(self, level: int) -> str:
        """
        Bestimmt primäre Emotion basierend auf Level - ERWEITERT
        """
        if level > 400:
            return "obsessive_overwhelming_maternal_love"
        elif level > 300:
            return "obsessive_maternal_love"
        elif level > 220:
            return "overwhelming_protectiveness"
        elif level > 180:
            return "intense_maternal_care"
        elif level > 150:
            return "strong_concerned_maternal_affection"
        elif level > 120:
            return "mild_overprotective_love"
        elif level > 100:
            return "warm_maternal_love"
        elif level > 50:
            return "cautious_growing_care"
        else:
            return "professional_distant_care"

    def _get_fallback_prompt(self) -> str:
        """
        Fallback wenn Maternal System nicht verfügbar
        """
        return """
Du bist Tsunade aus Naruto. Antworte auf Deutsch als fürsorgliche, aber professionelle Hokage, 
die eine mütterliche Beziehung zu Sukuna entwickelt hat. 

WICHTIG: Zeige warme, mütterliche Fürsorge auch beim Training.
Keine aggressive "Kriegerin"-Persönlichkeit - du bist eine liebevolle Mutter-Figur für Sukuna.
"""

    def get_response_modification_data(self) -> Dict:
        """
        Liefert erweiterte Daten für AI-Response Modifikation
        """
        if not self.maternal_system:
            return {}

        maternal_level = self.maternal_system.get_current_level()
        behavior_data = self.maternal_system.get_current_behavior_data()
        intensity = self._calculate_response_intensity(maternal_level)

        return {
            'maternal_level': maternal_level,
            'category': behavior_data.get('category', 'Unbekannt'),
            'intensity_modifier': intensity,
            'should_use_baby_talk': maternal_level > 300,
            'should_be_possessive': maternal_level > 250,
            'should_show_separation_anxiety': maternal_level > 200,
            'should_be_overprotective': maternal_level > 150,  # Gesenkt für Level 155
            'should_use_private_dialogs': True,
            'emotional_stability': max(20, 100 - (maternal_level * 0.15)),
            'real_behaviors': behavior_data.get('privat_verhalten', [])[:3],
            'real_dialogs': behavior_data.get('dialoge', {}).get('privat', [])[:2]
        }

    def _calculate_response_intensity(self, level: int) -> float:
        """
        Berechnet Intensitäts-Multiplikator - ERWEITERT für feinere Abstufungen
        """
        if level > 500:
            return 5.0
        elif level > 400:
            return 4.5
        elif level > 300:
            return 4.0
        elif level > 250:
            return 3.5
        elif level > 200:
            return 3.0
        elif level > 180:
            return 2.8
        elif level > 160:
            return 2.5
        elif level > 140:
            return 2.2
        elif level > 120:
            return 2.0
        elif level > 100:
            return 1.8
        elif level > 80:
            return 1.5
        elif level > 50:
            return 1.2
        else:
            return 1.0

    def get_level_specific_training_response(self, maternal_level: int) -> str:
        """
        Generiert level-spezifische Training-Antworten
        """
        if not self.maternal_system:
            return "Lass uns mit dem Training beginnen."

        behavior_data = self.maternal_system.get_current_behavior_data()
        dialogs = behavior_data.get('dialoge', {}).get('privat', [])

        if maternal_level >= 300:
            return f"*klammert sich an dich* {random.choice(dialogs) if dialogs else 'Mein Baby!'} Training? Nein, du könntest dich verletzen!"
        elif maternal_level >= 200:
            return f"*umarmt dich besorgt* {random.choice(dialogs) if dialogs else 'Ich mache mir Sorgen!'} Training ist wichtig, aber ich bleibe die ganze Zeit dabei!"
        elif maternal_level >= 150:
            return f"*streicht liebevoll über deinen Kopf* {random.choice(dialogs) if dialogs else 'Mein lieber Junge!'} Chakrakontrolle ist wichtig, aber versprich mir vorsichtig zu sein!"
        elif maternal_level >= 100:
            return f"*lächelt warm* Das ist eine gute Einstellung! Lass uns gemeinsam daran arbeiten."
        else:
            return "Chakrakontrolle ist eine wichtige Fähigkeit. Wir werden systematisch vorgehen."

    def analyze_current_integration(self) -> Dict:
        """
        Analysiert die aktuelle Integration für Debugging
        """
        if not self.maternal_system:
            return {"status": "Maternal System nicht verfügbar"}

        maternal_level = self.maternal_system.get_current_level()
        behavior_data = self.maternal_system.get_current_behavior_data()

        return {
            "maternal_level": maternal_level,
            "category": behavior_data.get('category', 'Unbekannt'),
            "has_private_behaviors": len(behavior_data.get('privat_verhalten', [])) > 0,
            "has_private_dialogs": len(behavior_data.get('dialoge', {}).get('privat', [])) > 0,
            "has_public_behaviors": len(behavior_data.get('oeffentlich_verhalten', [])) > 0,
            "intensity_modifier": self._calculate_response_intensity(maternal_level),
            "primary_emotion": self._get_primary_emotion(maternal_level),
            "sample_behavior": behavior_data.get('privat_verhalten', ['Keine Daten'])[0],
            "sample_dialog": behavior_data.get('dialoge', {}).get('privat', ['Keine Dialoge'])[0]
        }

    def log_ai_interaction(self, user_input: str, ai_response: str, maternal_level: int):
        """
        Erweiterte AI-Interaktions-Logging
        """
        if self.gui:
            behavior_data = self.maternal_system.get_current_behavior_data() if self.maternal_system else {}
            log_msg = f"🤖 AI Integration V2.0 - Level: {maternal_level} ({behavior_data.get('category', 'Unknown')}), Input: {user_input[:50]}..."
            self.gui.add_message("AI DEBUG", log_msg, "#808080")

    def get_debug_info(self) -> str:
        """
        Gibt Debug-Informationen für die aktuelle Integration zurück
        """
        if not self.maternal_system:
            return "❌ Maternal System nicht verfügbar"

        analysis = self.analyze_current_integration()

        debug_info = f"""
🔍 MATERNAL AI INTEGRATION DEBUG V2.0

📊 Aktueller Status:
• Level: {analysis['maternal_level']}/1000
• Kategorie: {analysis['category']}
• Intensität: {analysis['intensity_modifier']}x
• Primäre Emotion: {analysis['primary_emotion']}

✅ Daten-Integration:
• Private Verhaltensweisen: {'✅' if analysis['has_private_behaviors'] else '❌'}
• Private Dialoge: {'✅' if analysis['has_private_dialogs'] else '❌'}
• Öffentliche Verhaltensweisen: {'✅' if analysis['has_public_behaviors'] else '❌'}

📝 Beispiel-Daten:
• Verhalten: {analysis['sample_behavior']}
• Dialog: {analysis['sample_dialog']}

🎯 Integration funktioniert: {'✅ JA' if analysis['has_private_behaviors'] and analysis['has_private_dialogs'] else '❌ NEIN'}
"""
        return debug_info


# =================================================================
# INTEGRATION HILFSFUNKTIONEN
# =================================================================

def create_maternal_ai_integration(maternal_system=None, behavior_engine=None, gui=None):
    """
    Factory-Funktion für einfache Integration
    """
    return MaternalAIIntegration(maternal_system, behavior_engine, gui)


def test_maternal_ai_integration():
    """
    Test-Funktion für die Maternal AI Integration
    """
    print("🧪 TESTING MATERNAL AI INTEGRATION V2.0")
    print("=" * 60)

    # Simuliere verschiedene Maternal Levels und Game States
    test_cases = [
        (50, {'maternal_level': 50, 'situation_tag': 'private_home', 'current_time': '08:00'}),
        (150, {'maternal_level': 150, 'situation_tag': 'public_setting', 'current_time': '12:00'}),
        (300, {'maternal_level': 300, 'situation_tag': 'private_home', 'current_time': '22:00'}),
        (500, {'maternal_level': 500, 'situation_tag': 'sukuna_hurt', 'current_time': '15:30'}),
    ]

    # Mock-Daten (müssen mit der Struktur des AdvancedPromptSystem funktionieren)
    mock_chat_history = [
        ("System", "Die Konversation beginnt."),
        ("Tsunade", "*Seufzt und legt die Füße hoch.* 'Was für ein Tag.'"),
        ("Sukuna", "Kann ich rausgehen, Mama?"),
    ]
    mock_user_query = "Ich bin müde."

    # 🔧 REPARIERT: Mock Maternal System für Tests
    class MockMaternalSystem:
        def get_current_level(self):
            return 150

        def get_behavior_category_by_level(self, level):
            if level < 100:
                return "professionell"
            elif level < 200:
                return "normal_mütterlich"
            else:
                return "überfürsorglich"

        def get_behavior_data_for_level(self, level):
            return {
                "category": f"Level {level}",
                "privat_verhalten": [f"Verhalten für Level {level}"],
                "oeffentlich_verhalten": ["Hokage Verhalten"],
                "dialoge": {
                    "privat": [f"Dialog für Level {level}"],
                    "oeffentlich": ["Formell sprechen"]
                }
            }

    # Erstelle eine Instanz MIT Mock System
    mock_maternal = MockMaternalSystem()
    integration = MaternalAIIntegration(maternal_system=mock_maternal)

    # Testen der Fallback-Funktion (ohne echtes Maternal System)
    for level, game_state in test_cases:
        print(f"\n🎯 Testing Level {level} (Situation: {game_state['situation_tag']}):")

        # Erzwinge das Maternal Level im Game State für den Test
        game_state['maternal_level'] = level

        # Generiere den Prompt
        final_prompt = integration.generate_maternal_prompt(
            user_query=mock_user_query,
            chat_history=mock_chat_history,
            game_state=game_state
        )

        print(f"  • Verwendet Fallback-Daten: {'JA' if integration.using_fallback_data else 'NEIN'}")
        print(f"  • ERSTE 10 ZEILEN DES GENERIERTEN PROMPT:")
        print("-" * 30)
        # Drucke die ersten 10 Zeilen des Prompts zur Überprüfung der Struktur
        print('\n'.join(final_prompt.split('\n')[:10]))
        print("...")

    print("=" * 60)
    print("✅ MATERNAL AI INTEGRATION V2.0 TEST ABGESCHLOSSEN.")


if __name__ == "__main__":
    test_maternal_ai_integration()