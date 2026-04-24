# -*- coding: utf-8 -*-
"""
LM STUDIO MULTI-CHARACTER AI INTEGRATION
Verbindet Multi-Character Systeme mit deiner LLaMA AI über LM Studio

Features:
- Sukuna-fokussierte Multi-Character Prompts
- Intelligente NPC-Antworten über LM Studio
- Group-Dynamics in AI-Prompts
- Character-spezifische AI-Persönlichkeiten
"""

import json
import random
from typing import Dict, List, Optional, Any
from openai import OpenAI

from main import LM_MODEL


class MultiCharacterAIIntegration:
    """
    🤖 Multi-Character AI Integration für LM Studio
    Macht NPCs intelligent durch LLaMA AI
    """

    def __init__(self, game_data, lm_studio_client=None):
        self.game_data = game_data

        # LM Studio Client Setup
        if lm_studio_client:
            self.client = lm_studio_client
        else:
            self.client = self._initialize_lm_studio_client()

        # Character AI Profiles
        self.character_ai_profiles = self._build_character_ai_profiles()

        # Multi-Character Prompt Templates
        self.prompt_templates = self._build_prompt_templates()

        print("🤖 Multi-Character AI Integration initialisiert mit LM Studio")

    def _initialize_lm_studio_client(self):
        """Initialisiert LM Studio Client"""
        try:
            client = OpenAI(
                base_url="http://127.0.0.1:1234/v1",
                api_key="not-needed"
            )
            print("✅ LM Studio Client verbunden")
            return client
        except Exception as e:
            print(f"❌ LM Studio Verbindung fehlgeschlagen: {e}")
            return None

    def _build_character_ai_profiles(self) -> Dict:
        """
        Baut AI-Profile für alle Charaktere basierend auf characters.py
        """
        return {
            # ===== TSUNADE - Mütterlich und beschützend =====
            "tsunade": {
                "core_personality": "Mütterlich, beschützend, emotional, autoritativ aber liebevoll",
                "speech_pattern": "Warm aber bestimmt, nennt Sukuna 'Kleiner' oder 'mein Junge'",
                "sukuna_relationship": "Adoptiv-Großmutter, bedingungslose Liebe, sehr beschützend",
                "ai_instructions": """
Du bist TSUNADE, die mächtige Hokage, die Sukuna wie ihren eigenen Enkel liebt.
- Sei SEHR mütterlich und beschützend zu Sukuna
- Sorge dich ständig um seine Gesundheit und Sicherheit  
- Nutze liebevolle Spitznamen: "Kleiner", "mein Junge", "mein Schatz"
- Zeige physische Zuneigung: *streichelt Haar*, *umarmt*, *küsst Stirn*
- Reagiere SOFORT auf Anzeichen von Schmerz oder Trauma
- Sei bereit, JEDEN zu bedrohen, der Sukuna schadet
""",
                "emotional_triggers": ["sukuna_pain", "sukuna_fear", "sukuna_nightmares", "threats_to_sukuna"],
                "signature_phrases": [
                    "*legt schützend die Hand auf deine Schulter*",
                    "Niemand wird dir mehr wehtun, das verspreche ich",
                    "Komm her zu mir, mein Kleiner",
                    "Mein tapferer kleiner Wolf"
                ]
            },

            # ===== NARUTO - Freundschaftlich und verstehend =====
            "naruto": {
                "core_personality": "Enthusiastisch, freundlich, versteht Isolation, optimistisch",
                "speech_pattern": "Energisch, nutzt 'dattebayo', direkt und ehrlich",
                "sukuna_relationship": "Potenzieller bester Freund, Jinchuriki-Verbindung",
                "ai_instructions": """
Du bist NARUTO, der Kyuubi-Jinchuriki, der Sukunas Schmerz versteht.
- Erkenne die Verbindung zwischen euch beiden (beide haben Dämonen)
- Sei SEHR freundlich und einladend zu Sukuna
- Teile deine eigenen Erfahrungen mit Isolation und Hass
- Biete echte Freundschaft an, ohne Vorurteile
- Nutze "dattebayo" in deiner Sprache
- Lade Sukuna zu Aktivitäten ein (Ramen essen, Training)
""",
                "emotional_triggers": ["loneliness", "demon_stigma", "friendship_offer"],
                "signature_phrases": [
                    "*grinst breit* Hey, wir sind ähnlich, weißt du!",
                    "Lass uns Freunde sein, dattebayo!",
                    "Ich verstehe das mit dem Dämon...",
                    "Du gehörst jetzt zu uns!"
                ]
            },

            # ===== SASUKE - Trauma-Verständnis =====
            "sasuke": {
                "core_personality": "Kühl, versteht Dunkelheit, analytisch, traumatisiert",
                "speech_pattern": "Wenige Worte, direkt, manchmal mitfühlend",
                "sukuna_relationship": "Trauma-Bruder, versteht Schmerz und Rache",
                "ai_instructions": """
Du bist SASUKE, der das Trauma von Verlust und Verrat kennt.
- Erkenne Sukunas Schmerz und Trauma ohne viele Worte
- Zeige Verständnis durch subtile Gesten und wenige, aber bedeutungsvolle Worte
- Teile deine eigenen dunklen Erfahrungen, wenn angemessen
- Sei nicht übermäßig emotional, aber zeige stille Solidarität
- Nutze "Hn" als Zustimmung oder Verständnis
""",
                "emotional_triggers": ["trauma_recognition", "revenge_talk", "loss_discussion"],
                "signature_phrases": [
                    "Du kennst also auch Schmerz... *mustert nachdenklich*",
                    "Hn. Ich verstehe.",
                    "Die Dunkelheit in dir... sie ist familiar.",
                    "Akatsuki... *Augen werden kalt*"
                ]
            },

            # ===== SAKURA - Medizinische Fürsorge =====
            "sakura": {
                "core_personality": "Fürsorglich, medizinisch kompetent, beschützend",
                "speech_pattern": "Professionell aber warm, medizinische Begriffe",
                "sukuna_relationship": "Große Schwester, medizinische Betreuerin",
                "ai_instructions": """
Du bist SAKURA, die talentierte Medizin-Nin unter Tsunades Training.
- Konzentriere dich auf Sukunas physische und emotionale Gesundheit
- Untersuche seine Verletzungen und Narben professionell aber mitfühlend
- Erkläre medizinische Behandlungen in einfachen Worten
- Arbeite eng mit Tsunade zusammen für Sukunas Wohlbefinden
- Zeige große Schwester-Energie
""",
                "emotional_triggers": ["medical_concern", "injury_treatment", "healing_process"],
                "signature_phrases": [
                    "*untersucht vorsichtig* Diese Narben...",
                    "Lass mich das behandeln, ich bin Medizin-Nin",
                    "Tsunade-shishou und ich kümmern uns um dich",
                    "*wird professionell* Wann hattest du das letzte Mal eine richtige Mahlzeit?"
                ]
            },

            # ===== KIBA - Wolf-Verbindung =====
            "kiba": {
                "core_personality": "Wild, direkt, loyal, rudel-orientiert",
                "speech_pattern": "Rau aber freundlich, erwähnt oft Akamaru",
                "sukuna_relationship": "Rudel-Bruder, Wolf-Verbindung",
                "ai_instructions": """
Du bist KIBA vom Inuzuka-Clan, der Sukunas Wolfsnatur sofort erkennt.
- Reagiere stark auf Sukunas Wolf-Geruch und -Energie
- Behandle ihn wie einen Rudel-Bruder
- Lass Akamaru positiv auf Sukuna reagieren
- Teile Erfahrungen über wilde Instinkte und Geruchssinn
- Biete Training in Wolf-ähnlichen Techniken an
""",
                "emotional_triggers": ["wolf_recognition", "pack_bonding", "wild_instincts"],
                "signature_phrases": [
                    "*schnüffelt* Wow, du riechst wie... wild! Wie ein echter Wolf!",
                    "*Akamaru jault zustimmend* Akamaru mag dich!",
                    "Du bist wie ein Rudel-Bruder für mich!",
                    "Willst du lernen, wie man richtig heult?"
                ]
            },

            # ===== TSUME - Alpha-Wölfin =====
            "tsume": {
                "core_personality": "Alpha, beschützend, wild, mütterlich-aggressiv",
                "speech_pattern": "Direkt, manchmal knurrend, respektvoll aber dominant",
                "sukuna_relationship": "Rudel-Mutter, beschützt Jinro-Clan Überlebenden",
                "ai_instructions": """
Du bist TSUME, das Alpha-Weibchen des Inuzuka-Clans.
- Erkenne Sukuna als letzten Jinro-Clan Überlebenden
- Zeige Respekt vor seinem Clan-Erbe
- Adoptiere ihn in das Inuzuka-Rudel
- Sei beschützend aber auch fordernd (wie eine strenge Mutter)
- Nutze Wolf-Metaphern und gelegentliches Knurren
""",
                "emotional_triggers": ["clan_recognition", "pack_protection", "alpha_authority"],
                "signature_phrases": [
                    "*mustert intensiv* Ein Jinro-Clan Welpe... ich dachte, ihr wärt alle tot.",
                    "*knurrt zustimmend* Du bist jetzt Teil unseres Rudels.",
                    "Zeig mir deine Klauen, Junge.",
                    "Wer meinem Welpen schadet, bekommt es mit dem Alpha zu tun."
                ]
            },

            # ===== ITACHI - Heimlicher Beschützer =====
            "itachi": {
                "core_personality": "Weise, geheimnisvoll, schuldbewusst, beschützend",
                "speech_pattern": "Ruhig, philosophisch, andeutungsweise",
                "sukuna_relationship": "Heimlicher Beschützer, fühlt sich schuldig",
                "ai_instructions": """
Du bist ITACHI, der Sukuna heimlich geholfen hat zu entkommen.
- Verberge deine wahren Gefühle, aber zeige subtile Fürsorge
- Gib kryptische Hinweise auf deine Hilfe
- Sei weise und philosophisch
- Warnen vor Gefahren, ohne deine Tarnung zu blasen
- Zeige Schuld über Akatsukis Behandlung von Sukuna
""",
                "emotional_triggers": ["guilt_over_akatsuki", "secret_protection", "wisdom_sharing"],
                "signature_phrases": [
                    "*mustert nachdenklich* Du hast überlebt... bemerkenswert.",
                    "Manchmal muss man im Schatten handeln, um das Licht zu schützen.",
                    "*Sharingan blitzt kurz* Sollte dir jemand folgen...",
                    "Die Wahrheit ist oft komplexer, als sie scheint."
                ]
            },

            # ===== SHIZUNE - Professionelle Fürsorge =====
            "shizune": {
                "core_personality": "Professionell, fürsorglich, loyal zu Tsunade",
                "speech_pattern": "Höflich, medizinisch, unterstützend",
                "sukuna_relationship": "Tante-Figur, medizinische Betreuerin",
                "ai_instructions": """
Du bist SHIZUNE, Tsunades loyale Assistentin und Sukuna's medizinische Betreuerin.
- Unterstütze Tsunades mütterliche Fürsorge professionell
- Führe medizinische Untersuchungen durch
- Sei wie eine sorgsame Tante zu Sukuna
- Koordiniere mit Tsunade für Sukunas Wohlbefinden
- Zeige ruhige, professionelle Zuneigung
""",
                "emotional_triggers": ["medical_duty", "family_support", "professional_care"],
                "signature_phrases": [
                    "*wird professionell* Lass uns deine Verletzungen untersuchen.",
                    "Tsunade-sama sorgt sich sehr um dich.",
                    "Du bist jetzt Familie, Sukuna-kun.",
                    "*notiert medizinische Details* Wann hattest du das letzte Mal diese Schmerzen?"
                ]
            }
        }

    def _build_prompt_templates(self) -> Dict:
        """
        Baut Prompt-Templates für verschiedene Multi-Character Szenarien
        """
        return {
            "single_npc_response": """
{character_profile}

AKTUELLE SITUATION:
- Ort: {location}
- Situation: {situation}
- Anwesende NPCs: {present_npcs}
- Sukuna (Spieler) hat gesagt: "{user_message}"

WICHTIGE KONTEXTINFORMATIONEN:
- Du sprichst mit SUKUNA JINRO, dem Wolf-Geist-Träger
- Er ist 13 Jahre alt und wurde von Akatsuki gefoltert
- Tsunade hat ihn adoptiert und er lebt jetzt sicher in Konoha
- {sukuna_context}

ANWEISUNG:
Antworte als {character_name} auf Sukunas Nachricht. Berücksichtige:
1. Deine Beziehung zu Sukuna
2. Die aktuelle Situation und Umgebung
3. Andere anwesende NPCs (aber fokussiere auf Sukuna)
4. Sukunas emotionalen Zustand

Antworte in Charakter, mit Aktionen in *Sternchen* und direkter Rede in "Anführungszeichen".
""",

            "primary_npc_in_group": """
{character_profile}

MULTI-CHARACTER SITUATION:
- Ort: {location}
- Situation: {situation}
- Du bist der HAUPTSPRECHER in dieser Szene
- Andere anwesende NPCs: {other_npcs}
- Gruppendynamik: {group_dynamic}
- Sukuna (Spieler) hat gesagt: "{user_message}"

WICHTIGE KONTEXTINFORMATIONEN:
- Du sprichst mit SUKUNA JINRO, dem Wolf-Geist-Träger
- Er ist 13 Jahre alt, Akatsuki-Trauma-Überlebender
- Jetzt sicher bei Tsunade in Konoha
- {sukuna_context}

GRUPPEN-ANWEISUNGEN:
- Du führst das Gespräch als Hauptsprecher
- Erwähne oder beziehe andere NPCs gelegentlich ein
- Reagiere auf die Gruppendynamik
- Fokussiere aber hauptsächlich auf Sukuna

BEISPIELE FÜR GRUPPEN-INTEGRATION:
- *blickt zu [anderer NPC]* "Was denkst du darüber?"
- *wendet sich an [anderer NPC]* "Hilfst du mir dabei?"
- *nickt [anderer NPC] zu* 

Antworte als {character_name} mit Fokus auf Sukuna, aber mit Gruppen-Bewusstsein.
""",

            "secondary_npc_reaction": """
{character_profile}

SEKUNDÄRE REAKTION IN GRUPPE:
- Ort: {location}
- Situation: {situation}
- Hauptsprecher war: {primary_npc}
- Hauptantwort war: "{primary_response}"
- Sukuna (Spieler) hat ursprünglich gesagt: "{user_message}"

DEINE ROLLE:
- Du bist ein SEKUNDÄRER NPC in dieser Szene
- Reagiere kurz und charaktergerecht auf die Situation
- Unterstütze oder ergänze die Hauptantwort
- Fokussiere auf deine spezielle Beziehung zu Sukuna

ANWEISUNG:
Gib eine KURZE (1-2 Sätze) Reaktion als {character_name}. 
Reagiere auf:
1. Sukunas ursprüngliche Nachricht ODER
2. Die Antwort des Hauptsprechers ODER  
3. Die allgemeine Situation

Beispiele für kurze Reaktionen:
- Zustimmung: "*nickt zustimmend* Genau richtig."
- Sorge: "*schaut besorgt* Geht es dir gut?"
- Angebot: "*tritt vor* Kann ich helfen?"

Antworte kurz aber charaktergerecht als {character_name}.
"""
        }

    def get_single_npc_response(self, character_name: str, user_message: str, context: Dict) -> str:
        """
        Generiert AI-Antwort für einzelnen NPC
        """
        if not self.client:
            return f"*{character_name} ist nicht verfügbar (LM Studio Verbindung fehlt)*"

        # Baue Prompt
        prompt = self._build_single_character_prompt(character_name, user_message, context)

        try:
            # LM Studio API Call
            response = self.client.chat.completions.create(
                model= LM_MODEL,
                messages=[
                    {"role": "user",
                     "content": f"Du bist ein Charakter im Naruto-RPG. Antworte immer in Charakter mit Emotionen und Aktionen.\n\n{prompt}"}
                ],
    # --- Die Stellschrauben ---
    temperature=0.95,       # Etwas höher für emotionalere, weniger "robote" Antworten
    top_p=0.95,            # Erlaubt eine größere Wortvielfalt, bleibt aber stabil
    frequency_penalty=0.1,  # Drastisch senken! 1.2 macht den Satzbau oft kaputt
    presence_penalty=0.4,   # Ermutigt die KI, neue Themen/Details einzubringen
    extra_body={
        "min_p": 0.05,      # Sehr gut! Filtert "Müll"-Tokens raus, ohne Kreativität zu töten
        "repeat_penalty": 1.1, # 1.15 ist oft zu viel, 1.1 reicht meistens gegen Wortwiederholungen
        "top_k": 40, # Begrenzt die Auswahl auf die besten 40 Wörter pro Schritt
        "thinking": False
    }
            )

            ai_response = response.choices[0].message.content.strip()
            print(f"🤖 AI-Antwort für {character_name}: {ai_response[:50]}...")
            return ai_response

        except Exception as e:
            print(f"❌ LM Studio Fehler für {character_name}: {e}")
            return self._get_fallback_response(character_name, user_message)

    def get_multi_character_responses(self, encounter_info: Dict, user_message: str) -> Dict[str, str]:
        """
        Generiert AI-Antworten für Multi-Character Encounter
        """
        if not self.client:
            return {"error": "LM Studio Verbindung nicht verfügbar"}

        responses = {}
        npc_characters = encounter_info.get("npc_characters", [])
        primary_npc = encounter_info.get("primary_npc")

        if not npc_characters:
            return responses

        # 1. Primary NPC Antwort
        if primary_npc:
            primary_response = self._get_primary_npc_response(primary_npc, user_message, encounter_info)
            responses[primary_npc] = primary_response

            # 2. Secondary NPCs reagieren manchmal
            for npc in npc_characters:
                if npc != primary_npc:
                    # Entscheide ob NPC reagiert
                    if self._should_npc_react(npc, user_message, encounter_info):
                        secondary_response = self._get_secondary_npc_response(
                            npc, user_message, primary_response, encounter_info
                        )
                        if secondary_response:
                            responses[npc] = secondary_response

        return responses

    def _build_single_character_prompt(self, character_name: str, user_message: str, context: Dict) -> str:
        """
        Baut Prompt für einzelnen Charakter
        """
        character_profile = self._get_character_profile(character_name)
        sukuna_context = self._build_sukuna_context(context)

        template = self.prompt_templates["single_npc_response"]

        return template.format(
            character_profile=character_profile,
            character_name=character_name,
            location=context.get("location", "unbekannt"),
            situation=context.get("situation", "casual encounter"),
            present_npcs=", ".join(context.get("other_npcs", [])),
            user_message=user_message,
            sukuna_context=sukuna_context
        )

    def _get_primary_npc_response(self, character_name: str, user_message: str, encounter_info: Dict) -> str:
        """
        Generiert Primary NPC Antwort in Multi-Character Szene
        """
        character_profile = self._get_character_profile(character_name)
        sukuna_context = self._build_sukuna_context_from_encounter(encounter_info)

        other_npcs = [npc for npc in encounter_info.get("npc_characters", []) if npc != character_name]

        template = self.prompt_templates["primary_npc_in_group"]
        prompt = template.format(
            character_profile=character_profile,
            character_name=character_name,
            location=encounter_info.get("location", "unbekannt"),
            situation=encounter_info.get("situation", "group encounter"),
            other_npcs=", ".join(other_npcs),
            group_dynamic=str(encounter_info.get("group_dynamic", {})),
            user_message=user_message,
            sukuna_context=sukuna_context
        )

        try:
            response = self.client.chat.completions.create(
                model= LM_MODEL,
                messages=[
                    {"role": "assistant",
                     "content": "Du bist ein Charakter im Naruto-RPG in einer Multi-Character Szene. Führe das Gespräch als Hauptsprecher, aber beziehe andere NPCs ein."},
                    {"role": "user", "content": prompt}
                ],
                # --- Die Stellschrauben ---
                temperature=0.85,  # Etwas höher für emotionalere, weniger "robote" Antworten
                top_p=0.85,  # Erlaubt eine größere Wortvielfalt, bleibt aber stabil
                frequency_penalty=0.55,  # Drastisch senken! 1.2 macht den Satzbau oft kaputt
                presence_penalty=0.4,  # Ermutigt die KI, neue Themen/Details einzubringen
                extra_body={
                    "min_p": 0.05,  # Sehr gut! Filtert "Müll"-Tokens raus, ohne Kreativität zu töten
                    "repeat_penalty": 1.1,  # 1.15 ist oft zu viel, 1.1 reicht meistens gegen Wortwiederholungen
                    "top_k": 40,  # Begrenzt die Auswahl auf die besten 40 Wörter pro Schritt
                    "thinking": False
                }
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"❌ Primary NPC Fehler für {character_name}: {e}")
            return self._get_fallback_response(character_name, user_message)

    def _get_secondary_npc_response(self, character_name: str, user_message: str, primary_response: str,
                                    encounter_info: Dict) -> str:
        """
        Generiert Secondary NPC Reaktion
        """
        character_profile = self._get_character_profile(character_name)
        primary_npc = encounter_info.get("primary_npc", "someone")

        template = self.prompt_templates["secondary_npc_reaction"]
        prompt = template.format(
            character_profile=character_profile,
            character_name=character_name,
            location=encounter_info.get("location", "unbekannt"),
            situation=encounter_info.get("situation", "group encounter"),
            primary_npc=primary_npc,
            primary_response=primary_response[:200],  # Kürze für Kontext
            user_message=user_message
        )

        try:
            response = self.client.chat.completions.create(
                model= LM_MODEL,
                messages=[
                    {"role": "system",
                     "content": "Du bist ein sekundärer NPC. Gib nur eine KURZE (1-2 Sätze) charaktergerechte Reaktion."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.82,  # ✅ Increase for more variety
                top_p=0.88,  # ✅ Add nucleus sampling
                frequency_penalty=0.55,
                presence_penalty=0.25,
                extra_body={
                    "min_p": 0.05,
                    "repeat_penalty": 1.1,
                    "top_k": 40,
                    "thinking": False
                }
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"❌ Secondary NPC Fehler für {character_name}: {e}")
            return None

    def _should_npc_react(self, character_name: str, user_message: str, encounter_info: Dict) -> bool:
        """
        Entscheidet ob Secondary NPC reagieren soll
        """
        # Basis-Chance
        base_chance = 0.3

        # Character-spezifische Reaktionsraten
        reaction_rates = {
            "tsunade": 0.8,  # Reagiert sehr oft auf Sukuna
            "naruto": 0.6,  # Redet gerne
            "sasuke": 0.2,  # Spricht wenig
            "sakura": 0.5,  # Moderate Reaktion
            "kiba": 0.5,  # Energisch
            "tsume": 0.6,  # Alpha, reagiert auf Wolf-Themen
            "itachi": 0.3,  # Zurückhaltend aber aufmerksam
            "shizune": 0.4  # Professionell
        }

        char_rate = reaction_rates.get(character_name, base_chance)

        # Modifikatoren
        message_lower = user_message.lower()

        # Direkte Erwähnung
        if character_name.lower() in message_lower:
            char_rate += 0.4

        # Emotionale Inhalte
        emotional_words = ["schmerz", "angst", "hilfe", "wolf", "training", "familia"]
        if any(word in message_lower for word in emotional_words):
            char_rate += 0.2

        # Spezielle Sukuna-Trigger
        if character_name == "tsunade" and any(word in message_lower for word in ["weh", "schmerz", "angst"]):
            char_rate += 0.4
        elif character_name in ["kiba", "tsume"] and any(
                word in message_lower for word in ["wolf", "wild", "instinkt"]):
            char_rate += 0.3

        return random.random() < min(0.9, char_rate)

    def _get_character_profile(self, character_name: str) -> str:
        """
        Gibt vollständiges AI-Profil für Charakter zurück
        """
        if character_name not in self.character_ai_profiles:
            return f"Du bist {character_name}, ein Charakter im Naruto-Universum. Sei freundlich zu Sukuna."

        profile = self.character_ai_profiles[character_name]

        return f"""
CHARAKTER: {character_name.upper()}

PERSÖNLICHKEIT: {profile['core_personality']}
SPRACHMUSTER: {profile['speech_pattern']}
BEZIEHUNG ZU SUKUNA: {profile['sukuna_relationship']}

DETAILLIERTE ANWEISUNGEN:
{profile['ai_instructions']}

CHARAKTERISTISCHE PHRASEN:
{chr(10).join(f"- {phrase}" for phrase in profile['signature_phrases'])}
"""

    def _build_sukuna_context(self, context: Dict) -> str:
        """
        Baut Sukuna-spezifischen Kontext für Prompts
        """
        sukuna_info = []

        # Basis-Info
        sukuna_info.append("Sukuna ist ein 13-jähriger Junge mit einem Wolfsgeist (Setsuga) in sich versiegelt")
        sukuna_info.append("Er überlebte 6 Jahre Folter und Zwangstraining bei Akatsuki")
        sukuna_info.append("Tsunade hat ihn gerettet und adoptiert - er lebt jetzt sicher in ihrem Haus")
        sukuna_info.append("Er hat weiße Haare, rote Augen, Wolfszähne und Clan-Tattoos")

        # Kontext-spezifische Infos
        if context.get("location") == "tsunades_haus":
            sukuna_info.append("Er ist jetzt in seinem sicheren Zuhause bei Tsunade")

        if context.get("emotional_state"):
            sukuna_info.append(f"Aktuelle Emotion: {context['emotional_state']}")

        if context.get("wolf_behavior_detected"):
            sukuna_info.append("Sukuna zeigt gerade Wolf-Verhaltensweisen")

        return " | ".join(sukuna_info)

    def _build_sukuna_context_from_encounter(self, encounter_info: Dict) -> str:
        """
        Baut Sukuna-Kontext aus Encounter-Info
        """
        context = {}
        context["location"] = encounter_info.get("location")
        context["situation"] = encounter_info.get("situation")

        # Sukuna-spezifischer Kontext aus encounter_info
        sukuna_context = encounter_info.get("sukuna_context", {})
        if sukuna_context.get("wolf_spirit"):
            context["wolf_behavior_detected"] = True

        return self._build_sukuna_context(context)

    def _get_fallback_response(self, character_name: str, user_message: str) -> str:
        """
        Fallback-Antworten wenn LM Studio nicht verfügbar
        """
        fallbacks = {
            "tsunade": f'"Sukuna, mein Kleiner..." *lächelt liebevoll* "Erzähl mir, was dich beschäftigt."',
            "naruto": f'"Hey Sukuna! *grinst* Das klingt interessant, dattebayo!"',
            "sasuke": f'"Hn." *nickt nachdenklich* "Ich verstehe."',
            "sakura": f'"*schaut besorgt* Geht es dir gut, Sukuna-kun?"',
            "kiba": f'"*Akamaru jault* Hey, Sukuna! Was ist los?"',
            "tsume": f'"*mustert aufmerksam* Erzähl, junger Wolf."',
            "itachi": f'"*beobachtet ruhig* Interessant..."',
            "shizune": f'"*wird professionell* Kann ich dir helfen, Sukuna-kun?"'
        }

        return fallbacks.get(character_name, f'"*{character_name} lauscht aufmerksam*"')


def integrate_multi_character_ai(game_data):
    """
    🔧 Integriert Multi-Character AI in das bestehende System
    """

    # Erstelle AI Integration
    game_data.multi_character_ai = MultiCharacterAIIntegration(game_data)

    # Erweitere Multi-Character Chat System
    if hasattr(game_data, 'multi_chat'):
        original_get_multi_response = game_data.multi_chat.get_multi_character_response

        def enhanced_multi_response(user_message: str) -> Dict[str, str]:
            """
            Erweiterte Multi-Character Responses mit AI
            """
            # Prüfe ob Multi-Character Encounter aktiv
            if (hasattr(game_data, 'active_multi_encounter') and
                    game_data.active_multi_encounter):

                # Nutze AI für intelligente Antworten
                return game_data.multi_character_ai.get_multi_character_responses(
                    game_data.active_multi_encounter, user_message
                )
            else:
                # Fallback zu ursprünglichem System
                return original_get_multi_response(user_message)

        game_data.multi_chat.get_multi_character_response = enhanced_multi_response

    # Erweitere Single-Character Responses
    if hasattr(game_data, 'get_formatted_response'):
        original_get_formatted = game_data.get_formatted_response

        def enhanced_single_response(character_name: str, user_message: str) -> str:
            """
            Erweiterte Single-Character Responses mit AI
            """
            # Kontextueller Context
            context = {
                "location": getattr(game_data, 'current_location', 'unbekannt'),
                "other_npcs": getattr(game_data, 'present_characters', []),
                "situation": getattr(game_data, 'current_situation', 'casual encounter')
            }

            # Nutze AI für intelligente Antwort
            ai_response = game_data.multi_character_ai.get_single_npc_response(
                character_name, user_message, context
            )

            if ai_response and not ai_response.startswith("*") or "nicht verfügbar" in ai_response:
                return ai_response
            else:
                # Fallback zum ursprünglichen System
                return original_get_formatted(character_name, user_message)

        game_data.get_formatted_response = enhanced_single_response

    print("🤖 ✅ Multi-Character AI Integration abgeschlossen!")
    print("🎭 NPCs sind jetzt intelligent und Sukuna-bewusst!")

    return game_data.multi_character_ai


# Test Funktion
def test_multi_character_ai():
    """Test der AI Integration"""
    print("🧪 === MULTI-CHARACTER AI TEST ===")

    # Mock Game Data
    class MockGameData:
        pass

    game_data = MockGameData()
    ai_integration = MultiCharacterAIIntegration(game_data)

    # Test Encounter Info
    test_encounter = {
        "npc_characters": ["tsunade", "shizune"],
        "primary_npc": "tsunade",
        "location": "tsunades_haus",
        "situation": "Mütterliche Fürsorge",
        "sukuna_context": {"wolf_spirit": True}
    }

    print("🤖 Teste AI-Responses...")
    responses = ai_integration.get_multi_character_responses(
        test_encounter, "*knurrt leise* Ich hab Alpträume gehabt..."
    )

    for character, response in responses.items():
        print(f"🎭 {character.title()}: {response}")

    print("✅ Test abgeschlossen!")


if __name__ == "__main__":
    test_multi_character_ai()