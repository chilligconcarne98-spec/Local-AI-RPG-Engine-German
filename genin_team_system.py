#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👥 GENIN TEAM FORMATION SYSTEM
Automatische Team-Zuteilung nach 5 Ingame-Tagen

Features:
- Day 5 Auto-Event: Tsunade ruft Sukuna ins Hokage-Büro
- Intelligente Team-Zuteilung basierend auf Relationships
- Team 7 (Naruto/Sasuke/Sakura), Team 8 (Hinata/Kiba/Shino), Team 10 (Ino/Shikamaru/Choji)
- Permanente Team-Mechaniken nach Zuteilung
- Team-spezifische Missionen & Dynamics
"""

import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass


class GeninTeam(Enum):
    """Verfügbare Genin Teams"""
    TEAM_7 = "team_7"
    TEAM_8 = "team_8"
    TEAM_10 = "team_10"


@dataclass
class TeamInfo:
    """Team Information"""
    team_id: GeninTeam
    name: str
    members: List[str]
    sensei: str
    specialization: str
    description: str


class GeninTeamFormationSystem:
    """👥 Hauptklasse für das Genin Team System"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.setup_teams()
        self.formation_day = 5  # Tag 5 = Team Formation
        self.team_formed = False
        self.current_team = None

        # Status Tracking
        self.hokage_summon_triggered = False
        self.ceremony_completed = False

    def setup_teams(self):
        """🏗️ Definiert alle verfügbaren Teams"""

        self.available_teams = {
            GeninTeam.TEAM_7: TeamInfo(
                team_id=GeninTeam.TEAM_7,
                name="Team 7 - Elite Squad",
                members=["naruto", "sasuke", "sakura"],
                sensei="kakashi",
                specialization="Balanced Combat & Versatility",
                description="Das legendäre Team 7 - bekannt für außergewöhnliche Missionen und starke Bonds."
            ),

            GeninTeam.TEAM_8: TeamInfo(
                team_id=GeninTeam.TEAM_8,
                name="Team 8 - Tracking Specialists",
                members=["hinata", "kiba", "shino"],
                sensei="kurenai",
                specialization="Reconnaissance & Tracking",
                description="Spezialisiert auf Aufkläring, Verfolgung und Genjutsu-Operationen."
            ),

            GeninTeam.TEAM_10: TeamInfo(
                team_id=GeninTeam.TEAM_10,
                name="Team 10 - Strategic Force",
                members=["ino", "shikamaru", "choji"],
                sensei="asuma",
                specialization="Strategy & Formation Combat",
                description="Bekannt für brillante Strategien und perfekte Team-Koordination."
            )
        }

    def check_day_5_event(self) -> Optional[str]:
        """🕐 Prüft ob Day 5 Event getriggert werden soll"""

        current_day = self.game_data.game_state.get('day', 1)

        # Day 5 erreicht und Event noch nicht getriggert
        if current_day >= self.formation_day and not self.hokage_summon_triggered:
            return "hokage_summon"

        return None

    def trigger_hokage_summon(self) -> str:
        """🌅 Tsunade weckt Sukuna am Morgen von Tag 5"""

        self.hokage_summon_triggered = True

        # Speichere Event-Status
        if 'events' not in self.game_data.game_state:
            self.game_data.game_state['events'] = {}
        self.game_data.game_state['events']['hokage_summon_day5'] = True

        # Prüfe ob Sukuna zuhause ist
        current_location = self.game_data.current_location

        if current_location == 'tsunades_haus':
            # PERSÖNLICHES MORNING WAKEUP
            return self._generate_personal_wakeup()
        else:
            # ANBU MESSENGER (wenn er woanders ist)
            return self._generate_anbu_summon()

    def _generate_personal_wakeup(self) -> str:
        """🏠 Tsunade weckt ihn persönlich auf"""

        return """🌅 **TAG 5 - TSUNADES HAUS - FRÜHER MORGEN** 🏠

*Du erwachst durch eine sanfte, vertraute Berührung*

Tsunade: *flüstert liebevoll* "Sukuna... Zeit zum Aufwachen, mein Schatz."

*Du öffnest die Augen. Tsunade sitzt auf deiner Bettkante, bereits in ihrer Hokage-Robe*

"Heute ist der Tag, auf den wir beide gewartet haben." *lächelt warm*

"Nach 5 Tagen... ist es Zeit für deine offizielle Team-Zuteilung."

*ihre Hand ruht beschützend auf deiner Schulter*

"Ich weiß, es fühlt sich überwältigend an. Aber ich glaube an dich, Sukuna. 
Du bist bereit für diesen Schritt."

*steht auf und geht zum Fenster*

"Zieh dich an und frühstücke etwas. In einer Stunde treffen wir uns in meinem Büro."

*dreht sich um, Stolz in ihren Augen*

"Mein kleiner Ninja wird heute erwachsen..." *flüstert mit einem Lächeln*

🍳 **Tsunade macht dir Frühstück und wartet auf dich**
📍 **Bereite dich vor, dann:** /encounter hokage_turm"""

    def _generate_anbu_summon(self) -> str:
        """📜 ANBU Summon falls er nicht zuhause ist"""

        return """🏛️ **ANBU SUMMON - TAG 5** 📜

*Ein ANBU-Ninja erscheint in einer Rauchwolke*

ANBU: "Sukuna, du wirst sofort im Hokage-Büro erwartet. 
Tsunade-sama möchte dich sprechen - es geht um deine Team-Zuteilung."

*verschwindet so schnell wie er kam*

💭 **Tag 5... die Team-Formation beginnt.**

📍 **GEH ZUM HOKAGE-TURM:** /encounter hokage_turm"""

    def handle_hokage_encounter(self) -> str:
        """🏛️ Team Formation Ceremony im Hokage-Turm"""

        if not self.hokage_summon_triggered:
            return "❌ Du solltest noch nicht hier sein. Komm nach Tag 5 wieder."

        if self.ceremony_completed:
            return self._post_ceremony_dialogue()

        # Bestimme Team basierend auf Relationships
        assigned_team = self._determine_team_assignment()
        team_info = self.available_teams[assigned_team]

        # Setze Team-Status
        self.current_team = assigned_team
        self.team_formed = True
        self.ceremony_completed = True

        # Speichere Team-Assignment
        self.game_data.game_state['team'] = {
            'team_id': assigned_team.value,
            'members': team_info.members,
            'sensei': team_info.sensei,
            'formation_day': self.game_data.game_state.get('day', 5),
            'missions_completed': 0
        }

        # Generiere Ceremony Dialogue
        ceremony_text = self._generate_ceremony_dialogue(team_info)

        return ceremony_text

    def _determine_team_assignment(self) -> GeninTeam:
        """🎯 Bestimmt Team basierend auf Relationships & Preferences"""

        team_scores = {}

        for team_id, team_info in self.available_teams.items():
            score = 0

            # Relationship-basierte Scores
            if hasattr(self.game_data, 'relationship_system'):
                for member in team_info.members:
                    rel_level = self._get_relationship_level(member)
                    score += rel_level

            # Team-spezifische Boni
            if team_id == GeninTeam.TEAM_7:
                # Bonus für hohe Combat Skills
                if hasattr(self.game_data, 'combat_system'):
                    sukuna_stats = self.game_data.combat_system.character_stats.get('sukuna')
                    if sukuna_stats:
                        score += (sukuna_stats.ninjutsu_skill + sukuna_stats.taijutsu_skill) * 0.5

            elif team_id == GeninTeam.TEAM_8:
                # Bonus für Genjutsu & Stealth (Clan-Spezialisierung)
                if hasattr(self.game_data, 'combat_system'):
                    sukuna_stats = self.game_data.combat_system.character_stats.get('sukuna')
                    if sukuna_stats:
                        score += sukuna_stats.genjutsu_skill * 1.2  # Wolfs-Clan Genjutsu

            elif team_id == GeninTeam.TEAM_10:
                # Bonus für Intelligence & Strategy
                if hasattr(self.game_data, 'combat_system'):
                    sukuna_stats = self.game_data.combat_system.character_stats.get('sukuna')
                    if sukuna_stats:
                        score += sukuna_stats.intelligence * 0.8

            # Random Factor für Variation
            score += random.uniform(-10, 10)

            team_scores[team_id] = score

        # Wähle Team mit höchstem Score
        best_team = max(team_scores.keys(), key=lambda x: team_scores[x])

        print(f"🎯 Team Assignment Scores: {[(t.value, s) for t, s in team_scores.items()]}")
        print(f"🏆 Assigned to: {best_team.value}")

        return best_team

    def _get_relationship_level(self, character: str) -> float:
        """💕 Holt Relationship Level für Charakter"""

        try:
            if hasattr(self.game_data, 'game_state') and 'relationships' in self.game_data.game_state:
                return self.game_data.game_state['relationships'].get(character, {}).get('level', 0)
        except:
            pass

        return 0

    def _generate_ceremony_dialogue(self, team_info: TeamInfo) -> str:
        """🎭 Generiert die Team Formation Ceremony mit persönlicher Note"""

        ceremony_text = f"""🏛️ **HOKAGE-BÜRO - TEAM FORMATION** 🎌

*Du betrittst Tsunades Büro. Sie sitzt in voller Hokage-Würde hinter ihrem Schreibtisch*

Tsunade: *wechselt zu offiziellem Ton* "Sukuna, nimm Platz."

*ihre Augen zeigen Stolz, aber sie muss professionell sein*

"Nach 5 Tagen sorgfältiger Beobachtung und Bewertung ist deine Team-Zuteilung entschieden."

*nimmt eine versiegelte Schriftrolle*

"Deine Fortschritte waren bemerkenswert. Besonders deine Clan-Fähigkeiten 
haben meine... unsere Aufmerksamkeit erregt."

*ihr Blick wird kurz mütterlich, dann wieder offiziell*

"Du wirst zugeteilt zu: **{team_info.name}**"

📋 **TEAM MITGLIEDER:**
{chr(10).join([f"   • {member.title()}" for member in team_info.members])}
   • Sukuna (Du)

👨‍🏫 **JONIN-SENSEI:** {team_info.sensei.title()}

🎯 **SPEZIALISIERUNG:** {team_info.specialization}

*{team_info.sensei.title()} tritt ein*

{team_info.sensei.title()}: "Ein Wolfs-Clan Ninja... interessant. 
Ich habe viel über deine Fortschritte gehört."

Tsunade: *steht auf, ihre offizielle Maske fällt kurz* "Pass gut auf ihn auf, {team_info.sensei.title()}."

*dann wieder professionell*

"Morgen früh, 6 Uhr, Training Ground 3. Dort lernst du deine Teammates kennen."

*als du dich zum Gehen wendest, flüstert sie*

"Mach mich stolz, mein Lieber..."

🎉 **TEAM FORMATION ABGESCHLOSSEN!**
👨‍👩‍👧 **Tsunade wird immer deine Familie bleiben**
🎯 **Nächster Schritt:** /encounter training_area (morgen früh)
📊 **Team-Status:** /team_status"""

        return ceremony_text

    def handle_morning_breakfast_scene(self) -> str:
        """🍳 Tsunade macht Frühstück für den wichtigen Tag"""

        if (self.hokage_summon_triggered and
                self.game_data.current_location == 'tsunades_haus' and
                not self.ceremony_completed):

            # Maternal Level Bonus für besonderen Moment
            if hasattr(self.game_data, 'maternal_system'):
                try:
                    self.game_data.maternal_system.adjust_level(10, "Besonderer Team-Formation Morgen")
                except:
                    pass

            return """🍳 **TSUNADES HAUS - KÜCHE** 

*Du kommst in die Küche. Tsunade steht am Herd, brät Eier und macht Miso-Suppe*

Tsunade: *ohne sich umzudrehen* "Setz dich, Sukuna. Du brauchst Kraft für heute."

*stellt einen Teller vor dich - dein Lieblings-Frühstück*

"Weißt du... als ich damals meine Team-Zuteilung bekam, war ich so nervös, 
dass ich kein Bissen runterbekommen habe." *lächelt nostalgisch*

*setzt sich dir gegenüber mit einer Tasse Tee*

"Aber du bist stärker als ich es war. Deine Wolfs-Clan Fähigkeiten, 
deine Fortschritte im Training... die anderen Genin werden beeindruckt sein."

*ihre Stimme wird weicher*

"Egal welches Team du bekommst, Sukuna... du wirst immer mein kleiner Ninja bleiben."

*steht auf und küsst deine Stirn*

"Jetzt iss auf. Wir haben einen wichtigen Tag vor uns."

💝 **Maternal Level +10** (besonderer Moment)
🏛️ **Bereit für Hokage-Turm:** /encounter hokage_turm"""

        return "🏠 Normaler Morgen in Tsunades Haus."

    def _post_ceremony_dialogue(self) -> str:
        """💬 Dialog nach der Ceremony"""

        team_info = self.available_teams[self.current_team]

        return f"""🏛️ **HOKAGE-BÜRO** 

Tsunade: "Du bist bereits {team_info.name} zugeteilt worden. 
Dein Training mit {team_info.sensei.title()} sollte bald beginnen."

💡 **Tipp:** Nutze /team_status um deine Team-Info zu sehen!"""

    def get_team_status(self) -> str:
        """📊 Zeigt aktuellen Team-Status"""

        if not self.team_formed:
            current_day = self.game_data.game_state.get('day', 1)
            days_until_formation = max(0, self.formation_day - current_day)

            return f"""👥 **TEAM STATUS**

🕐 **Status:** Noch kein Team
📅 **Team Formation:** Tag {self.formation_day}
⏰ **Verbleibende Tage:** {days_until_formation}

💡 Am Tag {self.formation_day} wirst du zu einem Team zugeteilt!"""

        team_data = self.game_data.game_state.get('team', {})
        team_info = self.available_teams[self.current_team]

        return f"""👥 **TEAM STATUS** 

🏷️ **Team:** {team_info.name}
👨‍🏫 **Sensei:** {team_info.sensei.title()}
🎯 **Spezialisierung:** {team_info.specialization}

👥 **Mitglieder:**
{chr(10).join([f"   • {member.title()}" for member in team_info.members])}
   • Sukuna (Du)

📊 **Stats:**
   • Formation: Tag {team_data.get('formation_day', 5)}
   • Missionen: {team_data.get('missions_completed', 0)}

💡 **Commands:** /call_team, /team_mission"""

    def call_team_to_location(self) -> str:
        """📞 Ruft Team zur aktuellen Location"""

        if not self.team_formed:
            return "❌ Du hast noch kein Team!"

        current_location = self.game_data.current_location
        team_info = self.available_teams[self.current_team]

        # Prüfe ob Location für Team-Meeting geeignet ist
        suitable_locations = ['training_area', 'dorf_zentrum', 'academy', 'hokage_turm']

        if current_location not in suitable_locations:
            return f"❌ {current_location} ist nicht für Team-Meetings geeignet!\n💡 Verfügbare Locations: {', '.join(suitable_locations)}"

        team_members_text = ", ".join([member.title() for member in team_info.members])

        return f"""📞 **TEAM VERSAMMLUNG**

*Du sendest eine Nachricht an deine Teammates*

📍 **Location:** {current_location}
👥 **Team {self.current_team.value.replace('_', ' ').title()}** versammelt sich!

*Nach wenigen Minuten treffen ein:*
   • {team_members_text}

{team_info.sensei.title()}: "Ein Team-Meeting? Gut. Was ist der Plan?"

💡 **Team ist jetzt hier und bereit für Aktionen!**
🎯 **Nutze normale Gespräche oder /team_mission für Aufgaben**"""

    def get_team_missions(self) -> str:
        """🎯 Zeigt verfügbare Team-Missionen"""

        if not self.team_formed:
            return "❌ Du brauchst ein Team für Missionen!"

        team_data = self.game_data.game_state.get('team', {})
        missions_completed = team_data.get('missions_completed', 0)

        # Missions basierend auf Team-Progress
        available_missions = []

        if missions_completed == 0:
            available_missions.append({
                "id": "first_mission",
                "name": "Verschollene Katze finden",
                "rank": "D-Rang",
                "description": "Findet die Katze des Feudalherren - erste echte Teamwork-Probe!",
                "location": "dorf_zentrum"
            })

        if missions_completed >= 1:
            available_missions.append({
                "id": "bandit_patrol",
                "name": "Banditen-Patrouille",
                "rank": "C-Rang",
                "description": "Patrouilliert den Wald und beseitigt Banditenbedrohung",
                "location": "wald"
            })

        missions_text = "🎯 **VERFÜGBARE TEAM-MISSIONEN:**\n\n"

        if available_missions:
            for mission in available_missions:
                missions_text += f"""📋 **{mission['name']}** ({mission['rank']})
   📍 Location: {mission['location']}  
   📝 {mission['description']}
   🎯 Command: /start_mission {mission['id']}

"""
        else:
            missions_text += "🔄 Keine neuen Missionen verfügbar. Kehre später zurück!"

        return missions_text

    def get_save_data(self) -> Dict:
        """💾 Bereitet Team System Daten für Speicherung vor"""
        return {
            'hokage_summon_triggered': self.hokage_summon_triggered,
            'ceremony_completed': self.ceremony_completed,
            'team_formed': self.team_formed,
            'current_team': self.current_team.value if self.current_team else None,
            'formation_day': self.formation_day,
            'training_history': self.training_history if hasattr(self, 'training_history') else [],
            'combat_history': self.combat_history if hasattr(self, 'combat_history') else []
        }

    def load_save_data(self, save_data: Dict):
        """💾 Lädt Team System Daten aus Speicherung"""
        self.hokage_summon_triggered = save_data.get('hokage_summon_triggered', False)
        self.ceremony_completed = save_data.get('ceremony_completed', False)
        self.team_formed = save_data.get('team_formed', False)

        current_team_str = save_data.get('current_team')
        if current_team_str:
            for team in GeninTeam:
                if team.value == current_team_str:
                    self.current_team = team
                    break

        self.formation_day = save_data.get('formation_day', 5)
        self.training_history = save_data.get('training_history', [])
        self.combat_history = save_data.get('combat_history', [])


def integrate_genin_team_system(game_data):
    """👥 Integriert das Genin Team System"""

    print("👥 Integriere Genin Team Formation System...")

    # Erstelle Team System
    team_system = GeninTeamFormationSystem(game_data)
    game_data.genin_team_system = team_system

    # Erweitere Time System für Daily Event Checks
    _integrate_with_time_system(game_data, team_system)

    # Füge Team Commands hinzu
    _add_team_commands(game_data)

    print("🎯 GENIN TEAM SYSTEM aktiviert!")
    print("📅 Features:")
    print("   • Automatisches Day 5 Event (Hokage Summon)")
    print("   • Intelligente Team-Zuteilung")
    print("   • Team 7, 8, 10 verfügbar")
    print("   • Permanente Team-Mechaniken")
    print("   • Commands: /team_status, /call_team")

    return team_system


def _integrate_with_time_system(game_data, team_system):
    """⏰ Integriert mit Time System für Event-Checks"""

    if hasattr(game_data, 'time_system'):
        # Erweitere Time System um Daily Event Check
        original_advance_time = game_data.time_system.advance_time

        def enhanced_advance_time_with_events(minutes):
            old_day = game_data.game_state.get('day', 1)

            # Normale Zeit-Advancement
            result = original_advance_time(minutes)

            new_day = game_data.game_state.get('day', 1)

            # Prüfe auf Day Change Events
            if new_day > old_day:
                event = team_system.check_day_5_event()
                if event == "hokage_summon":
                    # Speichere Event für nächste GUI-Aktualisierung
                    game_data.pending_event = {
                        'type': 'hokage_summon',
                        'message': team_system.trigger_hokage_summon()
                    }

            return result

        game_data.time_system.advance_time = enhanced_advance_time_with_events


def _add_team_commands(game_data):
    """🔧 Fügt Team Commands zur GUI hinzu"""

    if hasattr(game_data, 'gui'):
        gui = game_data.gui

        if hasattr(gui, 'handle_command'):
            original_handle_command = gui.handle_command

            def enhanced_handle_command_team(user_message):
                """Erweiterte Commands mit Team System"""

                parts = user_message[1:].split() if user_message.startswith('/') else []
                command = parts[0].lower() if parts else ""

                # Team Status Command
                if command == "team_status" and hasattr(game_data, 'genin_team_system'):
                    try:
                        status = game_data.genin_team_system.get_team_status()
                        gui.display_message("TEAM STATUS", status, "info")
                    except Exception as e:
                        gui.display_message("ERROR", f"Team Status Fehler: {e}", "danger")
                    return True

                # Call Team Command
                elif command == "call_team" and hasattr(game_data, 'genin_team_system'):
                    try:
                        result = game_data.genin_team_system.call_team_to_location()
                        gui.display_message("TEAM CALL", result, "info")
                    except Exception as e:
                        gui.display_message("ERROR", f"Team Call Fehler: {e}", "danger")
                    return True

                # Team Mission Command
                elif command == "team_mission" and hasattr(game_data, 'genin_team_system'):
                    try:
                        missions = game_data.genin_team_system.get_team_missions()
                        gui.display_message("TEAM MISSIONS", missions, "info")
                    except Exception as e:
                        gui.display_message("ERROR", f"Team Mission Fehler: {e}", "danger")
                    return True

                # Fallback zu original
                return original_handle_command(user_message)

            # Ersetze Command Handler
            gui.handle_command = enhanced_handle_command_team


if __name__ == "__main__":
    print("👥 GENIN TEAM FORMATION SYSTEM")
    print("=" * 60)
    print("Verwendung:")
    print("  from genin_team_system import integrate_genin_team_system")
    print("  integrate_genin_team_system(your_game_data)")
    print("\nFeatures:")
    print("  📅 Automatisches Day 5 Event")
    print("  🎯 Intelligente Team-Zuteilung")
    print("  👥 Team 7, 8, 10 Support")
    print("  ⚔️ Team-basierte Missionen")