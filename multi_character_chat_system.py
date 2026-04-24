# -*- coding: utf-8 -*-
"""
MULTI-CHARACTER CHAT SYSTEM - KORRIGIERT FÜR SUKUNA ALS SPIELER
System für Gespräche mit mehreren Charakteren gleichzeitig
WICHTIG: Der Spieler IST Sukuna, andere Charaktere reagieren auf IHN
"""

from typing import Dict, List, Optional
import random


class MultiCharacterChat:
    """
    💬 MULTI-CHARACTER CHAT: Gespräche als Sukuna mit mehreren Charakteren
    """

    def __init__(self, game_data):
        self.game_data = game_data
        self.active_characters = []  # NPCs die anwesend sind (OHNE Sukuna)
        self.primary_speaker = None  # Haupt-NPC der antwortet
        self.conversation_mode = "single"  # "single" oder "multi"
        self.group_context = {}
        self.character_responses = {}
        self.player_character = "sukuna"  # Der Spieler ist immer Sukuna

    def start_multi_conversation(self, characters: List[str], situation: str):
        """
        🎯 Startet eine Multi-Character Unterhaltung
        characters: Liste der NPCs (ohne Sukuna - der ist der Spieler)
        """
        # Entferne Sukuna aus der Liste falls er versehentlich drin ist
        self.active_characters = [char for char in characters if char != "sukuna"]

        if self.active_characters:
            self.primary_speaker = self.active_characters[0]  # Erste NPC spricht hauptsächlich
            self.conversation_mode = "multi"
            self.group_context = {
                "situation": situation,
                "group_dynamic": self._analyze_group_dynamic(self.active_characters),
                "conversation_history": []
            }

            print(f"💬 Multi-Chat gestartet: Sukuna mit {', '.join(self.active_characters)} - {situation}")

    def get_multi_character_response(self, user_message: str) -> Dict[str, str]:
        """
        🔥 HAUPTMETHODE: Generiert Antworten von NPCs auf Sukunas Nachricht
        """
        responses = {}

        if self.conversation_mode != "multi" or not self.active_characters:
            # Fallback auf Single-Character
            return {
                self.game_data.active_character: self.game_data.get_formatted_response(
                    self.game_data.active_character, user_message)
            }

        # 1. Primary Character antwortet hauptsächlich
        primary_response = self._generate_primary_response(user_message)
        responses[self.primary_speaker] = primary_response

        # 2. Secondary Characters reagieren manchmal auf Sukuna
        for char in self.active_characters:
            if char != self.primary_speaker:
                secondary_response = self._generate_secondary_response(char, user_message, primary_response)
                if secondary_response:
                    responses[char] = secondary_response

        # 3. Aktualisiere Conversation History
        self.group_context["conversation_history"].append({
            "sukuna_message": user_message,
            "npc_responses": responses
        })

        return responses

    def _generate_primary_response(self, user_message: str) -> str:
        """
        Generiert die Haupt-Antwort vom Primary Speaker auf Sukunas Nachricht
        """
        # Verwende das normale Response-System aber mit Sukuna-Kontext
        if hasattr(self.game_data, 'get_claude_level_response'):
            detailed_response = self.game_data.get_claude_level_response(self.primary_speaker, user_message)
            base_response = detailed_response['response']
        else:
            base_response = self.game_data.get_formatted_response(self.primary_speaker, user_message)

        # Erweitere mit Group-Awareness (andere NPCs sind auch da)
        enhanced_response = self._add_group_awareness(base_response, self.primary_speaker)

        return enhanced_response

    def _generate_secondary_response(self, character: str, user_message: str, primary_response: str) -> Optional[str]:
        """
        Generiert optionale Reaktionen von Secondary Characters auf Sukuna
        """
        # Bestimme ob Character auf Sukuna reagiert
        reaction_chance = self._calculate_reaction_chance_to_sukuna(character, user_message, primary_response)

        if random.random() > reaction_chance:
            return None  # Character reagiert nicht

        # Generiere Reaktion auf Sukuna
        reaction_type = self._determine_reaction_type(character, user_message, primary_response)
        reaction = self._generate_character_reaction_to_sukuna(character, reaction_type, user_message, primary_response)

        return reaction

    def _calculate_reaction_chance_to_sukuna(self, character: str, user_message: str, primary_response: str) -> float:
        """
        Berechnet die Wahrscheinlichkeit dass ein NPC auf SUKUNA reagiert
        """
        base_chance = 0.3  # 30% Basis-Chance

        # Charakter-spezifische Reaktionsraten ZU SUKUNA
        character_reaction_rates = {
            # TSUNADE reagiert SEHR oft auf Sukuna (Mutter-Sohn Beziehung)
            "tsunade": 0.8,  # Sehr aufmerksam zu Sukuna

            # TEAM 7 - unterschiedlich
            "naruto": 0.7,  # Redet viel, auch zu Sukuna
            "sasuke": 0.3,  # Spricht wenig, aber interessiert an Sukuna
            "sakura": 0.5,  # Moderate Aufmerksamkeit
            "kakashi": 0.4,  # Beobachtet Sukuna aufmerksam

            # ROOKIE 9
            "ino": 0.6,  # Neugierig auf Sukuna
            "shikamaru": 0.2,  # Zu faul, aber analytisch interessiert
            "choji": 0.4,  # Freundlich zu Sukuna
            "kiba": 0.5,  # Kann Sukunas Wolfsnatur spüren
            "hinata": 0.3,  # Schüchtern aber aufmerksam
            "shino": 0.2,  # Zurückhaltend aber beobachtend
            "neji": 0.3,  # Stolz aber respektvoll
            "lee": 0.6,  # Enthusiastisch und freundlich
            "tenten": 0.4,  # Praktisches Interesse

            # ERWACHSENE/CLAN-OBERHÄUPTER
            "might_guy": 0.5,  # Jugendlicher Enthusiasmus
            "shikaku": 0.3,  # Strategisch interessiert an Sukuna
            "inoichi": 0.6,  # Psychologisch fasziniert von Sukuna
            "choza": 0.4,  # Väterlich fürsorglich
            "tsume": 0.7,  # SEHR interessiert - spürt Wolfsnatur!
            "hiashi": 0.3,  # Formal aber wachsam
            "shizune": 0.6,  # Medizinisches Interesse + Tsunades Einfluss

            # AKATSUKI/VILLAINS - verschiedene Interesse an Sukuna
            "itachi": 0.4,  # Strategisch interessiert, hat geholfen
            "kisame": 0.3,  # Respektiert Stärke
            "pain": 0.3,  # Philosophisch interessiert
            "sasori": 0.1,  # Wenig Emotion
            "hidan": 0.4,  # Chaotisch interessiert
            "deidara": 0.3,  # Künstlerisches Interesse
            "orochimaru": 0.5,  # SEHR interessiert an Sukunas Fähigkeiten
            "kabuto": 0.4,  # Wissenschaftlich neugierig
            "danzo": 0.6  # Misstrauisch und wachsam gegenüber Sukuna
        }

        char_modifier = character_reaction_rates.get(character, 0.3)

        # SUKUNA-SPEZIFISCHE Kontext-Modifikatoren
        message_lower = user_message.lower()

        # Wolf-bezogene Themen - Tsume und Kiba reagieren mehr
        wolf_keywords = ["wolf", "instinkt", "wild", "jagd", "rudel", "knurren"]
        if any(word in message_lower for word in wolf_keywords):
            if character in ["tsume", "kiba"]:
                char_modifier += 0.4  # Große Reaktion auf Wolf-Themen

        # Emotional geladene Nachrichten
        emotional_keywords = ["schmerz", "angst", "wut", "traurig", "verletzt", "akatsuki", "folter"]
        if any(word in message_lower for word in emotional_keywords):
            if character == "tsunade":
                char_modifier += 0.5  # Tsunade reagiert stark auf Sukunas Emotionen
            elif character in ["sakura", "shizune"]:
                char_modifier += 0.3  # Medizinisches Personal reagiert auf Trauma
            else:
                char_modifier += 0.2

        # Kampf/Training Themen
        combat_keywords = ["training", "kampf", "technik", "jutsu", "stärke"]
        if any(word in message_lower for word in combat_keywords):
            if character in ["kakashi", "might_guy", "lee", "sasuke"]:
                char_modifier += 0.3

        # Familie/Schutz Themen
        family_keywords = ["familie", "schutz", "zuhause", "sicher"]
        if any(word in message_lower for word in family_keywords):
            if character == "tsunade":
                char_modifier += 0.4

        return min(0.95, base_chance + char_modifier)

    def _determine_reaction_type(self, character: str, user_message: str, primary_response: str) -> str:
        """
        Bestimmt die Art der Reaktion auf SUKUNA
        """
        reaction_types = ["concern", "curiosity", "protective", "friendly", "analytical", "suspicious", "supportive"]

        # Charakter-spezifische Reaktions-Präferenzen ZU SUKUNA
        character_preferences = {
            # TSUNADE - sehr mütterlich und beschützend
            "tsunade": ["concern", "protective", "supportive"],

            # TEAM 7
            "naruto": ["friendly", "curiosity", "supportive"],  # Will Freund sein
            "sasuke": ["curiosity", "analytical"],  # Versteht Sukunas Dunkelheit
            "sakura": ["concern", "supportive"],  # Medizinisch interessiert
            "kakashi": ["analytical", "protective", "concern"],  # Sensei-Instinkt

            # ROOKIE 9
            "ino": ["curiosity", "friendly"],  # Neugierig
            "shikamaru": ["analytical", "curiosity"],  # Strategisch interessiert
            "choji": ["friendly", "supportive"],  # Gutherzig
            "kiba": ["curiosity", "friendly"],  # Wolf-Verbindung
            "hinata": ["concern", "supportive"],  # Empathisch
            "shino": ["analytical", "curiosity"],  # Beobachtend
            "neji": ["analytical", "curiosity"],  # Stolz aber interessiert
            "lee": ["friendly", "supportive"],  # Enthusiastisch positiv
            "tenten": ["curiosity", "supportive"],  # Praktisch hilfreich

            # ERWACHSENE
            "might_guy": ["friendly", "supportive"],  # Jugendlicher Optimismus
            "shikaku": ["analytical", "curiosity"],  # Strategische Einschätzung
            "inoichi": ["curiosity", "concern"],  # Psychologisch interessiert
            "choza": ["supportive", "protective"],  # Väterlich
            "tsume": ["curiosity", "protective"],  # Wolf-Mutter Instinkt
            "hiashi": ["analytical", "suspicious"],  # Clan-Schutz
            "shizune": ["concern", "supportive"],  # Medizinisch + Tsunades Einfluss

            # AKATSUKI/VILLAINS
            "itachi": ["analytical", "protective"],  # Heimlich hilfreich
            "kisame": ["curiosity", "analytical"],  # Respektiert Stärke
            "pain": ["analytical", "curiosity"],  # Philosophisch interessiert
            "sasori": ["analytical"],  # Emotionslos analytisch
            "hidan": ["curiosity"],  # Chaotisch neugierig
            "deidara": ["curiosity", "analytical"],  # Künstlerisch interessiert
            "orochimaru": ["curiosity", "analytical"],  # Wissenschaftlich gierig
            "kabuto": ["curiosity", "analytical"],  # Forschungsinteresse
            "danzo": ["suspicious", "analytical"]  # Misstrauisch und berechnend
        }

        preferred = character_preferences.get(character, ["curiosity", "analytical"])
        return random.choice(preferred)

    def _generate_character_reaction_to_sukuna(self, character: str, reaction_type: str, user_message: str,
                                               primary_response: str) -> str:
        """
        Generiert Charakter-Reaktionen speziell AUF SUKUNA
        """
        # SUKUNA-SPEZIFISCHE Reaktions-Templates
        sukuna_reaction_templates = {

            # ===== TSUNADE - Mütterliche Fürsorge =====
            "tsunade": {
                "concern": [
                    '"Sukuna, Kleiner, geht es dir gut?" *legt besorgt die Hand auf deine Schulter*',
                    '"Du siehst müde aus... hast du wieder Alpträume?" *schaut mütterlich besorgt*',
                    '"Erzähl deiner Oma, was dich beschäftigt." *zieht dich sanft zu sich*'
                ],
                "protective": [
                    '"Niemand wird dir mehr wehtun, das verspreche ich dir." *umfasst dich schützend*',
                    '"Du bist jetzt sicher bei mir, mein Junge." *streichelt beruhigend dein Haar*',
                    '"Wer auch immer dir das angetan hat..." *Augen blitzen gefährlich* "...wird es bereuen."*'
                ],
                "supportive": [
                    '"Du bist stärker als du denkst, Sukuna." *lächelt stolz*',
                    '"Mein tapferer kleiner Wolf." *küsst deine Stirn*',
                    '"Was auch immer du brauchst, ich bin für dich da." *hält deine Hand*'
                ]
            },

            # ===== NARUTO - Freundschaft =====
            "naruto": {
                "friendly": [
                    '"Hey Sukuna! Willst du mit mir Ramen essen gehen?" *grinst breit*',
                    '"Du bist cool, weißt du das? Lass uns Freunde sein!" *streckt die Hand aus*',
                    '"Ich verstehe das mit dem Dämon in dir... bei mir ist es ähnlich." *wird ernster*'
                ],
                "curiosity": [
                    '"Wow, du hast einen Wolfsgeist? Das ist so cool!" *Augen leuchten*',
                    '"Kannst du wirklich Gerüche so gut riechen wie Kiba?" *ist fasziniert*',
                    '"Zeigst du mir mal deine Wolfsklauen?" *springt aufgeregt herum*'
                ],
                "supportive": [
                    '"Du gehörst jetzt zu uns! Familie lässt Familie nicht im Stich!" *nickt entschlossen*',
                    '"Wir werden beide stärker, dattebayo!" *macht Faust-Bump*'
                ]
            },

            # ===== SASUKE - Verständnis für Dunkelheit =====
            "sasuke": {
                "curiosity": [
                    '"Du kennst also auch Schmerz..." *mustert dich nachdenklich*',
                    '"Dieser Wolfsgeist... ist er wie mein Fluchsiegel?" *berührt seinen Nacken*',
                    '"Akatsuki hat dich auch gequält?" *Augen werden kalt*'
                ],
                "analytical": [
                    '"Deine Kraft ist interessant... anders als meine." *aktiviert Sharingan kurz*',
                    '"Du verstehst Rache, nicht wahr?" *schaut durchdringend*'
                ]
            },

            # ===== SAKURA - Medizinische Sorge =====
            "sakura": {
                "concern": [
                    '"Deine Narben... wer hat dir das angetan?" *untersucht vorsichtig*',
                    '"Lass mich das behandeln. Ich bin Medizin-Nin!" *wird professionell*',
                    '"Du bist unterernährt. Wann hast du das letzte Mal richtig gegessen?" *wird fürsorglich*'
                ],
                "supportive": [
                    '"Tsunade-shishou und ich werden gut auf dich aufpassen." *lächelt beruhigend*',
                    '"Du bist nicht allein, Sukuna-kun." *reicht dir Wasser*'
                ]
            },

            # ===== KAKASHI - Sensei-Instinkt =====
            "kakashi": {
                "analytical": [
                    '"Hmm... du erinnerst mich an mich selbst in dem Alter." *schaut nachdenklich*',
                    '"Akatsuki-Training... das erklärt deine Kampfhaltung." *beobachtet aufmerksam*'
                ],
                "protective": [
                    '"Du bist unter Tsunades und meinem Schutz. Niemand wird dir hier schaden." *wird ernst*',
                    '"Wenn du reden willst... ich verstehe Trauma." *legt Hand auf deine Schulter*'
                ],
                "concern": [
                    '"Du trägst zu viel für dein Alter..." *seufzt mitfühlend*',
                    '"Kinder sollten nicht solche Augen haben." *wird traurig*'
                ]
            },

            # ===== KIBA & TSUME - Wolf-Verbindung =====
            "kiba": {
                "curiosity": [
                    '"Wow, du riechst wie... wild? Wie ein echter Wolf!" *schnüffelt interessiert*',
                    '"Akamaru mag dich! Das passiert selten!" *Akamaru jault zustimmend*',
                    '"Zeig mal deine Wolfszähne! Sind sie schärfer als meine?" *grinst*'
                ],
                "friendly": [
                    '"Du bist wie ein Rudel-Bruder für mich!" *schlägt kameradschaftlich auf den Rücken*',
                    '"Wollen wir zusammen jagen gehen... äh, trainieren?" *wird verlegen*'
                ]
            },

            "tsume": {
                "curiosity": [
                    '"Ein Jinro-Clan Welpe... ich dachte, ihr wärt alle tot." *mustert dich intensiv*',
                    '"Dein Wolfsgeist ist stark. Ich kann ihn riechen." *schnüffelt prüfend*',
                    '"Zeig mir deine Klauen, Junge." *fordert respektvoll*'
                ],
                "protective": [
                    '"Du bist jetzt Teil unseres Rudels. Inuzuka beschützen ihre eigenen." *knurrt zustimmend*',
                    '"Wer meinem Welpen schadet, bekommt es mit dem Alpha-Wolf zu tun." *wird gefährlich*'
                ]
            },

            # ===== SHIZUNE - Medizinisch + Tsunades Einfluss =====
            "shizune": {
                "concern": [
                    '"Tsunade-sama sorgt sich sehr um dich. Lass uns deine Verletzungen untersuchen." *wird professionell*',
                    '"Diese Folternarben... wir sollten sie behandeln." *wird mitfühlend*'
                ],
                "supportive": [
                    '"Du bist jetzt Familie, Sukuna-kun. Wir lassen dich nicht fallen." *lächelt warm*',
                    '"Tsunade-sama redet ständig über dich. Du bedeutest ihr sehr viel." *wird vertraulich*'
                ]
            },

            # ===== ITACHI - Heimliche Hilfsbereitschaft =====
            "itachi": {
                "analytical": [
                    '"Du hast Akatsukis Folter überlebt... bemerkenswert." *mustert respektvoll*',
                    '"Dein Hass macht dich stark, aber lass ihn nicht dein Herz vergiften." *wird weise*'
                ],
                "protective": [
                    '"Sollte Akatsuki dich wieder jagen... sie werden es bereuen." *Sharingan blitzt kurz*',
                    '"Du bist nicht der einzige, der unter falschen Anschuldigungen leidet." *wird nachdenklich*'
                ]
            },

            # ===== OROCHIMARU - Wissenschaftliches Interesse =====
            "orochimaru": {
                "curiosity": [
                    '"Kukukuku... ein Jinro-Clan Überlebender. Wie faszinierend..." *leckt sich die Lippen*',
                    '"Dein Wolfsgeist interessiert mich. Zeig mir seine Macht." *wird gierig*',
                    '"Akatsukis Training war grausam, aber effektiv... du bist ein Kunstwerk." *mustert dich wie ein Experiment*'
                ],
                "analytical": [
                    '"Die Versiegelung in dir ist... ungewöhnlich. Wer war dein Versieglungsmeister?" *wird neugierig*',
                    '"Du könntest ein mächtiger Verbündeter werden... oder ein interessantes Forschungsobjekt." *grinst schlangenhaft*'
                ]
            },

            # ===== DANZO - Misstrauen =====
            "danzo": {
                "suspicious": [
                    '"Ein Akatsuki-Trainierter... du bist eine Bedrohung für Konoha." *mustert misstrauisch*',
                    '"Root wird dich beobachten, Junge." *wird bedrohlich*',
                    '"Tsunade ist zu vertrauensselig. Du bist ein Risiko." *verschränkt die Arme*'
                ],
                "analytical": [
                    '"Deine Fähigkeiten könnten Root nützlich sein..." *wird berechnend*',
                    '"Akatsuki hat dich gut trainiert. Schade, dass du nicht loyal bist." *seufzt*'
                ]
            }
        }

        # Wähle Template für Charakter und Reaktionstyp
        if character in sukuna_reaction_templates and reaction_type in sukuna_reaction_templates[character]:
            templates = sukuna_reaction_templates[character][reaction_type]
            return random.choice(templates)

        # Fallback: Generische Reaktion auf Sukuna
        generic_sukuna_reactions = {
            "concern": '"Geht es dir gut, Sukuna?" *schaut besorgt*',
            "curiosity": '"Du bist interessant... erzähl mehr." *mustert neugierig*',
            "protective": '"Niemand wird dir hier schaden." *wird beschützend*',
            "friendly": '"Du scheinst nett zu sein, Sukuna." *lächelt*',
            "analytical": '"Faszinierend... du bist anders." *beobachtet aufmerksam*',
            "suspicious": '"Ich behalte dich im Auge..." *mustert misstrauisch*',
            "supportive": '"Du kannst auf mich zählen." *nickt ermutigend*'
        }

        return generic_sukuna_reactions.get(reaction_type, '"..." *beobachtet dich aufmerksam*')

    def _add_group_awareness(self, base_response: str, character: str) -> str:
        """
        Fügt Group-Awareness zur Basis-Antwort hinzu (andere NPCs sind auch da)
        """
        # 30% Chance für Group-Interaction zwischen NPCs
        if random.random() < 0.3 and len(self.active_characters) > 1:
            other_chars = [char for char in self.active_characters if char != character]
            chosen_char = random.choice(other_chars)

            # Spezielle NPC-zu-NPC Interaktionen in Sukunas Gegenwart
            if character == "tsunade" and "shizune" in other_chars:
                group_additions = [
                    f' *wendet sich an Shizune* "Bereite eine medizinische Untersuchung vor."',
                    f' *nickt Shizune zu* "Kümmere dich um Sukunas Wunden."'
                ]
            elif character == "naruto" and "sasuke" in other_chars:
                group_additions = [
                    f' *schaut zu Sasuke* "Findest du Sukuna nicht auch cool?"',
                    f' *wendet sich an Sasuke* "Du verstehst ihn doch auch, oder?"'
                ]
            elif character == "kakashi" and any(char in other_chars for char in ["naruto", "sasuke", "sakura"]):
                team_member = next((char for char in ["naruto", "sasuke", "sakura"] if char in other_chars), None)
                if team_member:
                    group_additions = [
                        f' *blickt zu {team_member.title()}* "Sukuna könnte euer neuer Teamkamerad werden."',
                        f' *wendet sich an {team_member.title()}* "Zeigt ihm, wie wir als Team funktionieren."'
                    ]
                else:
                    group_additions = [f' *blickt zu {chosen_char.title()}*']
            else:
                group_additions = [
                    f' *blickt zu {chosen_char.title()}*',
                    f' *wendet sich an {chosen_char.title()}*'
                ]

            addition = random.choice(group_additions)
            base_response += addition

        return base_response

    def _analyze_group_dynamic(self, characters: List[str]) -> Dict:
        """
        Analysiert die Gruppendynamik MIT SUKUNA als Fokus
        """
        dynamics = {
            "energy": "medium",
            "sukuna_acceptance": "neutral",
            "protection_level": "low",
            "curiosity_level": "medium",
            "family_feeling": "none"
        }

        # Tsunade bringt automatisch Familie-Gefühl und Schutz
        if "tsunade" in characters:
            dynamics["family_feeling"] = "very_high"
            dynamics["protection_level"] = "maximum"
            dynamics["sukuna_acceptance"] = "very_high"

        # Team 7 bringt verschiedene Dynamiken
        if "naruto" in characters:
            dynamics["energy"] = "high"
            dynamics["sukuna_acceptance"] = "high"

        if "sasuke" in characters:
            dynamics["understanding_darkness"] = "high"

        if "sakura" in characters:
            dynamics["medical_concern"] = "high"

        # Wolf-Verbindung
        if any(char in characters for char in ["kiba", "tsume"]):
            dynamics["wolf_connection"] = "strong"
            dynamics["pack_mentality"] = True

        # Akatsuki bringt Spannung
        akatsuki_members = ["itachi", "kisame", "pain", "sasori", "hidan", "deidara", "orochimaru"]
        if any(char in characters for char in akatsuki_members):
            dynamics["danger_level"] = "high"
            dynamics["tension"] = "very_high"
            if "itachi" in characters:
                dynamics["hidden_protection"] = "high"  # Itachi hilft heimlich

        # Danzo bringt Misstrauen
        if "danzo" in characters:
            dynamics["mistrust_level"] = "very_high"
            dynamics["political_tension"] = "high"

        return dynamics

    def switch_primary_speaker(self, new_speaker: str) -> bool:
        """
        Wechselt den Haupt-NPC-Gesprächspartner
        """
        if new_speaker in self.active_characters:
            old_speaker = self.primary_speaker
            self.primary_speaker = new_speaker
            # NICHT den active_character ändern - Sukuna bleibt der Spieler!

            print(f"🔄 Haupt-Gesprächspartner gewechselt: {old_speaker} → {new_speaker}")
            return True

        return False


def integrate_multi_chat_system(game_data):
    """
    🔧 INTEGRATION: Fügt Multi-Chat System zur GameData hinzu
    """

    # Erstelle Multi-Chat System
    game_data.multi_chat = MultiCharacterChat(game_data)

    # Erweitere get_formatted_response für Multi-Character Support
    original_get_formatted_response = game_data.get_formatted_response

    def enhanced_get_formatted_response(character_name: str, user_message: str) -> str:
        """
        Erweiterte get_formatted_response mit Multi-Character Support für Sukuna
        """

        # Prüfe ob Multi-Character Modus aktiv
        if (hasattr(game_data, 'multi_chat') and
                game_data.multi_chat.conversation_mode == "multi" and
                len(game_data.multi_chat.active_characters) > 0):

            # Multi-Character Response (NPCs antworten auf Sukuna)
            responses = game_data.multi_chat.get_multi_character_response(user_message)

            # Formatiere für Chat-Display
            formatted_responses = []
            for char, response in responses.items():
                formatted_responses.append(f"**{char.title()}**: {response}")

            return "\n\n".join(formatted_responses)

        else:
            # Standard Single-Character Response
            return original_get_formatted_response(character_name, user_message)

    # Ersetze Methode
    game_data.get_formatted_response = enhanced_get_formatted_response

    print("✅ Multi-Character Chat System für Sukuna-Spieler integriert!")


if __name__ == "__main__":
    print("💬 SUKUNA-FOKUSSIERTES MULTI-CHARACTER CHAT SYSTEM")
    print("Der Spieler IST Sukuna - NPCs reagieren auf ihn!")
    print("Besondere Features:")
    print("- Tsunades mütterliche Fürsorge")
    print("- Wolf-Verbindungen mit Inuzuka-Clan")
    print("- Akatsuki-Trauma-Verständnis")
    print("- Medizinische Sorge von Sakura/Shizune")