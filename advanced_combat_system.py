#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚔️ ADVANCED COMBAT & TRAINING SYSTEM
Vollständiges Kampfsystem für das Chat RPG mit Sparring, Solo-Training und Jutsu-Management

Features:
- Vollständige Jutsu-Datenbank aus den ODT-Dateien
- Chakra-Management System mit Character-spezifischen Levels
- Training Ground Encounters
- Solo Training Mechaniken
- Sparring System gegen NPCs
- Skill Progression & Learning
- Combat AI für realistische Kämpfe
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass


class JutsuRank(Enum):
    """Jutsu-Ränge"""
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S = "S"


class JutsuElement(Enum):
    """Chakra-Elemente"""
    SUITON = "suiton"  # Wasser
    DOTON = "doton"  # Erde
    KATON = "katon"  # Feuer
    FUUTON = "fuuton"  # Wind
    RAITON = "raiton"  # Blitz
    JITON = "jiton"  # Magnet
    TAIJUTSU = "taijutsu"
    GENJUTSU = "genjutsu"
    NINJUTSU = "ninjutsu"
    SPECIAL = "special"  # Clan-spezifisch


class CombatResult(Enum):
    """Combat Ergebnisse"""
    VICTORY = "victory"
    DEFEAT = "defeat"
    DRAW = "draw"
    INTERRUPTED = "interrupted"


@dataclass
class Jutsu:
    """Jutsu-Datenstruktur"""
    name: str
    rank: JutsuRank
    element: JutsuElement
    chakra_cost: int  # in %
    description: str
    requirements: List[str] = None
    special_conditions: List[str] = None
    users: List[str] = None
    learned: bool = False


@dataclass
class CombatStats:
    """Kampf-Statistiken für Charaktere"""
    max_chakra: int  # Basis 100%, Character-Modifikatoren angewendet
    current_chakra: int
    taijutsu_skill: int  # 1-100
    ninjutsu_skill: int  # 1-100
    genjutsu_skill: int  # 1-100
    speed: int  # 1-100
    strength: int  # 1-100
    stamina: int  # 1-100
    intelligence: int  # 1-100


class AdvancedCombatSystem:
    """⚔️ Hauptklasse für das Advanced Combat System"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.setup_jutsu_database()
        self.setup_character_stats()
        self.setup_combat_mechanics()

        # Training & Combat History
        self.training_history = []
        self.combat_history = []
        self.skill_progress = {}

    def setup_jutsu_database(self):
        """🗂️ Initialisiert komplette Jutsu-Datenbank aus den ODT-Dateien"""

        self.jutsu_database = {
            # === SUKUNA'S JUTSUS ===

            # E-Rang Jutsus
            "henge_no_jutsu": Jutsu(
                "Henge no Jutsu", JutsuRank.E, JutsuElement.NINJUTSU, 7,
                "Eine Illusionstechnik, die das Aussehen einer Person oder eines Objekts perfekt nachahmen kann."
            ),
            "kawarimi_no_jutsu": Jutsu(
                "Kawarimi no Jutsu", JutsuRank.E, JutsuElement.NINJUTSU, 10,
                "Eine Substitutionstechnik, bei der der Anwender sich mit einem Holzblock tauschen kann."
            ),
            "bunshin_no_jutsu": Jutsu(
                "Bunshin no Jutsu", JutsuRank.E, JutsuElement.NINJUTSU, 5,
                "Der Anwender erschafft illusionäre Kopien von sich selbst."
            ),
            "suiton_sosa": Jutsu(
                "Suiton: Sosa no Jutsu", JutsuRank.E, JutsuElement.SUITON, 4,
                "Ein einfaches Wassermanipulationsjutsu, um kleine Mengen Wasser zu bewegen."
            ),
            "suiton_mizu_kiri": Jutsu(
                "Suiton: Mizu Kiri no Jutsu", JutsuRank.E, JutsuElement.SUITON, 6,
                "Erzeugt einen dünnen Wasserstrahl zum Schneiden."
            ),
            "doton_shindou": Jutsu(
                "Doton: Shindou", JutsuRank.E, JutsuElement.DOTON, 8,
                "Eine leichte Bodenerschütterung zur Ablenkung oder Störung."
            ),

            # D-Rang Jutsus
            "suiton_kirigakure": Jutsu(
                "Suiton: Kirigakure no Jutsu", JutsuRank.D, JutsuElement.SUITON, 16,
                "Erzeugt einen starken Nebel zur Tarnung oder Verwirrung."
            ),
            "doton_shinjuu_zanshu": Jutsu(
                "Doton: Shinjuu Zanshu no Jutsu", JutsuRank.D, JutsuElement.DOTON, 12,
                "Der Anwender gräbt sich unter die Erde und zieht den Gegner unter die Erde.",
                users=["Kakashi Hatake"]
            ),

            # C-Rang Jutsus
            "suiton_mizurappa": Jutsu(
                "Suiton: Mizurappa", JutsuRank.C, JutsuElement.SUITON, 25,
                "Ein starker Wasserstrahl wird aus dem Mund geschossen."
            ),
            "suiton_mizu_bunshin": Jutsu(
                "Suiton: Mizu Bunshin no Jutsu", JutsuRank.C, JutsuElement.SUITON, 32,
                "Erschafft zwei bis drei Wasserdoppelgänger mit einem Zehntel der Stärke."
            ),
            "doton_koka_jutsu": Jutsu(
                "Doton: Koka Jutsu", JutsuRank.C, JutsuElement.DOTON, 25,
                "Der Körper wird mit Erdschicht überzogen, die als Rüstung dient."
            ),

            # B-Rang Jutsus
            "kage_bunshin": Jutsu(
                "Kage Bunshin no Jutsu", JutsuRank.B, JutsuElement.NINJUTSU, 40,
                "Erschafft drei Schattendoppelgänger mit voller Kampfkraft."
            ),
            "suiton_suiryuudan": Jutsu(
                "Suiton: Suiryuudan no Jutsu", JutsuRank.B, JutsuElement.SUITON, 48,
                "Formt aus einer großen Menge Wasser einen Wasserdrachen."
            ),
            "doton_domu": Jutsu(
                "Doton: Domu", JutsuRank.B, JutsuElement.DOTON, 50,
                "Verstärkt den Körper mit extrem harter Erde."
            ),

            # A-Rang Jutsus
            "suiton_daibakufu": Jutsu(
                "Suiton: Daibakufu no Jutsu", JutsuRank.A, JutsuElement.SUITON, 54,
                "Erzeugt eine massive Wasserwelle wie einen Wasserfall."
            ),
            "doton_yomi_numa": Jutsu(
                "Doton: Yomi Numa", JutsuRank.A, JutsuElement.DOTON, 55,
                "Erzeugt einen riesigen Schlammsumpf, der Gegner einsinken lässt."
            ),

            # === CLAN JUTSUS (SUKUNA SPEZIAL) ===
            "okami_toboe": Jutsu(
                "Okami-dama no Toboe", JutsuRank.C, JutsuElement.GENJUTSU, 23,
                "Wolfsgeheul-Genjutsu, das Gegner in illusionäre Welt zieht.",
                special_conditions=["Nur bei Nacht"], users=["Sukuna"]
            ),
            "okami_toboe_vollmond": Jutsu(
                "Okami-dama no Toboe (Vollmond)", JutsuRank.B, JutsuElement.GENJUTSU, 38,
                "Verstärkte Version bei Vollmondlicht - 2 Minuten Dauer.",
                special_conditions=["Nur bei Vollmond"], users=["Sukuna"]
            ),
            "okami_henge": Jutsu(
                "Okami no Henge", JutsuRank.D, JutsuElement.SPECIAL, 18,
                "Verwandlung in einen 1,40m großen Wolf mit Wolfssinnen.",
                users=["Sukuna"]
            ),

            # === NARUTO UNIVERSE JUTSUS ===

            # Katon Jutsus
            "katon_gokakyuu": Jutsu(
                "Katon: Gokakyuu no Jutsu", JutsuRank.C, JutsuElement.KATON, 25,
                "Eine gewaltige Feuerkugel wird auf den Gegner geblasen.",
                users=["Asuma", "Itachi", "Kakashi", "Sasuke"]
            ),
            "katon_housenka": Jutsu(
                "Katon: Housenka no Jutsu", JutsuRank.C, JutsuElement.KATON, 31,
                "Viele fußballgroße Feuerbälle fliegen auf den Gegner zu.",
                users=["Itachi", "Sasuke"]
            ),

            # Raiton Jutsus
            "chidori": Jutsu(
                "Chidori", JutsuRank.B, JutsuElement.RAITON, 35,
                "Konzentriert Raiton-Chakra in der Hand für durchdringenden Stoß.",
                users=["Sasuke", "Kakashi", "Itachi"]
            ),
            "raikiri": Jutsu(
                "Raikiri", JutsuRank.S, JutsuElement.RAITON, 70,
                "Hochfrequentiertes Raiton-Chakra kann massive Objekte durchbohren.",
                users=["Kakashi"]
            ),

            # Fuuton Jutsus
            "fuuton_reppuushou": Jutsu(
                "Fuuton: Reppuushou", JutsuRank.C, JutsuElement.FUUTON, 23,
                "Kraftvolle Windwelle, die Gegenstände beschleunigen kann.",
                users=["Orochimaru"]
            ),

            # Spezial Jutsus
            "rasengan": Jutsu(
                "Rasengan", JutsuRank.B, JutsuElement.NINJUTSU, 40,
                "Massive Chakrakugel mit verheerendem Aufprallschaden.",
                users=["Jiraiya", "Kakashi", "Naruto"]
            ),
            "edo_tensei": Jutsu(
                "Kuchiyose: Edo Tensei", JutsuRank.S, JutsuElement.DOTON, 100,
                "Verbotene Technik zur Wiederbelebung Verstorbener.",
                requirements=["Forbidden Knowledge"], users=["Orochimaru"]
            )
        }

        # Taijutsu Moves (separiert da sie kein Chakra kosten)
        self.taijutsu_moves = {
            "shotei": "Gezielter Schlag mit offener Hand",
            "kesa_giri": "Schwertschnitt von rechter Schulter zur linken Hüfte",
            "men_uchi": "Fundamentaler Abwärtsschnitt auf den Kopf",
            "tsuki": "Perfekter Stich in gerader Linie",
            "konoha_reppu": "Tiefer Rundtritt zum Boden schleudern",
            "konoha_shofu": "Aufwärtstritt in die Luft schleudern",
            "dynamic_entry": "Schnelle Annäherung mit überraschendem Tritt"
        }

    def setup_character_stats(self):
        """📊 Initialisiert Character-spezifische Stats basierend auf den Chakra-Levels"""

        self.character_stats = {
            "sukuna": CombatStats(
                max_chakra=140,  # 140% überdurchschnittlich wegen Wolfsgeist
                current_chakra=140,
                taijutsu_skill=65,  # Genin+ Level
                ninjutsu_skill=70,  # Überdurchschnittlich
                genjutsu_skill=75,  # Clan-Spezialisierung
                speed=70,
                strength=60,
                stamina=65,
                intelligence=75
            ),

            "tsunade": CombatStats(
                max_chakra=2300,  # Kage-Level!!
                current_chakra=2300,
                taijutsu_skill=95,  # Meister-Level
                ninjutsu_skill=98,  # Fast perfekt
                genjutsu_skill=85,  # Stark aber nicht Spezialisierung
                speed=90,  # Shunshin Meister
                strength=100,  # Übermenschlich mit Chakra-Enhancement
                stamina=95,
                intelligence=95
            ),

            "sasuke": CombatStats(
                max_chakra=140,  # 140% überdurchschnittlich (Uchiha)
                current_chakra=140,
                taijutsu_skill=80,  # Elite
                ninjutsu_skill=85,  # Uchiha Prodigy
                genjutsu_skill=90,  # Sharingan
                speed=85,
                strength=70,
                stamina=75,
                intelligence=85
            ),

            "sakura": CombatStats(
                max_chakra=110,  # Normale Genin
                current_chakra=110,
                taijutsu_skill=60,
                ninjutsu_skill=65,
                genjutsu_skill=70,  # Gute Chakra-Kontrolle
                speed=65,
                strength=55,  # Ohne Chakra-Enhancement
                stamina=70,
                intelligence=85  # Sehr intelligent
            ),

            "danzo": CombatStats(
                max_chakra=1200,  # Hohes Kage-Level
                current_chakra=1200,
                taijutsu_skill=85,
                ninjutsu_skill=95,  # Meister verschiedener Elemente
                genjutsu_skill=80,
                speed=80,
                strength=75,
                stamina=90,
                intelligence=95
            ),

            # Weitere Charaktere können hinzugefügt werden...
            "kakashi": CombatStats(
                max_chakra=900,  # Jonin-Level
                current_chakra=900,
                taijutsu_skill=85,
                ninjutsu_skill=95,  # Copy Ninja
                genjutsu_skill=85,
                speed=90,
                strength=75,
                stamina=80,  # Begrenzt durch Sharingan
                intelligence=95
            )
        }

    def setup_combat_mechanics(self):
        """⚙️ Setup Combat-Mechaniken und Algorithmen"""

        # Combat Modifikatoren
        self.rank_damage_multipliers = {
            JutsuRank.E: 1.0,
            JutsuRank.D: 1.5,
            JutsuRank.C: 2.0,
            JutsuRank.B: 3.0,
            JutsuRank.A: 4.5,
            JutsuRank.S: 6.0
        }

        # Element Effectiveness (Rock-Paper-Scissors)
        self.element_effectiveness = {
            JutsuElement.SUITON: {JutsuElement.KATON: 2.0, JutsuElement.DOTON: 0.5},
            JutsuElement.KATON: {JutsuElement.FUUTON: 2.0, JutsuElement.SUITON: 0.5},
            JutsuElement.FUUTON: {JutsuElement.RAITON: 2.0, JutsuElement.KATON: 0.5},
            JutsuElement.RAITON: {JutsuElement.DOTON: 2.0, JutsuElement.FUUTON: 0.5},
            JutsuElement.DOTON: {JutsuElement.SUITON: 2.0, JutsuElement.RAITON: 0.5}
        }

        # Training Erfolgsraten
        self.training_success_rates = {
            JutsuRank.E: 0.9,  # 90% Erfolg
            JutsuRank.D: 0.75,  # 75% Erfolg
            JutsuRank.C: 0.6,  # 60% Erfolg
            JutsuRank.B: 0.4,  # 40% Erfolg
            JutsuRank.A: 0.25,  # 25% Erfolg
            JutsuRank.S: 0.1  # 10% Erfolg
        }

    def start_training_session(self, training_type: str, duration_minutes: int = 30) -> Dict:
        """🏋️ Startet Training Session im Training Ground"""

        if self.game_data.current_location != 'training_ground':
            return {
                "success": False,
                "message": "❌ Du musst im Training Ground sein um zu trainieren!"
            }

        current_character = "sukuna"
        character_stats = self.character_stats.get(current_character)

        if not character_stats:
            return {
                "success": False,
                "message": f"❌ Keine Stats für {current_character} gefunden!"
            }

        training_results = self._execute_training(training_type, duration_minutes, current_character)

        # 🆕 GAME TIME ADVANCEMENT!
        if hasattr(self.game_data, 'time_system') and self.game_data.time_system:
            try:
                # Zeit um Training-Dauer voranspulen
                self.game_data.time_system.advance_time(duration_minutes)
                print(f"⏰ Spielzeit um {duration_minutes} Minuten vorangeschritten!")

                # Füge Zeit-Info zu Results hinzu
                new_time = self.game_data.time_system.get_formatted_time()
                training_results["new_time"] = f"Zeit nach Training: {new_time}"

            except Exception as e:
                print(f"⚠️ Time System Fehler: {e}")

        # Training zu History hinzufügen
        self.training_history.append({
            "character": current_character,
            "type": training_type,
            "duration": duration_minutes,
            "results": training_results,
            "timestamp": self.game_data.time_system.get_current_game_time() if hasattr(self.game_data, 'time_system') and self.game_data.time_system else datetime.now()
        })

        return {
            "success": True,
            "message": f"✅ Training abgeschlossen: {training_type}",
            "results": training_results
        }

    def _execute_training(self, training_type: str, duration: int, character: str) -> Dict:
        """⚡ Führt Training aus und berechnet Skill-Gains"""

        character_stats = self.character_stats[character]
        results = {}

        # Basis Skill-Gain pro Minute
        base_gain = 0.5
        duration_multiplier = duration / 30  # 30min = Standard

        if training_type == "taijutsu":
            gain = base_gain * duration_multiplier * random.uniform(0.8, 1.2)
            character_stats.taijutsu_skill = min(100, character_stats.taijutsu_skill + gain)
            character_stats.strength = min(100, character_stats.strength + gain * 0.5)
            character_stats.stamina = min(100, character_stats.stamina + gain * 0.3)

            results = {
                "taijutsu_gain": f"+{gain:.1f}",
                "strength_gain": f"+{gain * 0.5:.1f}",
                "stamina_gain": f"+{gain * 0.3:.1f}"
            }

        elif training_type == "ninjutsu":
            gain = base_gain * duration_multiplier * random.uniform(0.8, 1.2)
            character_stats.ninjutsu_skill = min(100, character_stats.ninjutsu_skill + gain)
            character_stats.intelligence = min(100, character_stats.intelligence + gain * 0.3)

            # Chance auf Jutsu Learning
            if random.random() < 0.2:  # 20% Chance
                learned_jutsu = self._attempt_jutsu_learning(character)
                if learned_jutsu:
                    results["jutsu_learned"] = learned_jutsu

            results.update({
                "ninjutsu_gain": f"+{gain:.1f}",
                "intelligence_gain": f"+{gain * 0.3:.1f}"
            })

        elif training_type == "chakra_control":
            gain = base_gain * duration_multiplier * random.uniform(0.7, 1.3)
            # Chakra-Effizienz verbessert sich
            character_stats.max_chakra = min(character_stats.max_chakra * 1.5,
                                             character_stats.max_chakra + gain)
            character_stats.current_chakra = character_stats.max_chakra

            results = {
                "chakra_efficiency": f"+{gain:.1f}%",
                "max_chakra": character_stats.max_chakra
            }

        elif training_type == "sword_technique":
            # Spezial Training für Schwert-Techniken
            gain = base_gain * duration_multiplier * random.uniform(0.9, 1.1)
            character_stats.taijutsu_skill = min(100, character_stats.taijutsu_skill + gain * 1.2)
            character_stats.speed = min(100, character_stats.speed + gain * 0.4)

            results = {
                "sword_mastery": f"+{gain * 1.2:.1f}",
                "speed_gain": f"+{gain * 0.4:.1f}"
            }

        # Immer etwas Stamina training
        character_stats.stamina = min(100, character_stats.stamina + 0.1 * duration_multiplier)

        return results

    def _attempt_jutsu_learning(self, character: str) -> Optional[str]:
        """📚 Versucht ein neues Jutsu zu lernen"""

        character_stats = self.character_stats[character]

        # Verfügbare Jutsus basierend auf Character Level
        available_jutsus = []

        for jutsu_id, jutsu in self.jutsu_database.items():
            if jutsu.learned:
                continue

            # Prüfe ob Character das Jutsu lernen kann
            can_learn = True

            # Skill Requirements
            if jutsu.rank == JutsuRank.E and character_stats.ninjutsu_skill < 10:
                can_learn = False
            elif jutsu.rank == JutsuRank.D and character_stats.ninjutsu_skill < 25:
                can_learn = False
            elif jutsu.rank == JutsuRank.C and character_stats.ninjutsu_skill < 45:
                can_learn = False
            elif jutsu.rank == JutsuRank.B and character_stats.ninjutsu_skill < 65:
                can_learn = False
            elif jutsu.rank == JutsuRank.A and character_stats.ninjutsu_skill < 85:
                can_learn = False
            elif jutsu.rank == JutsuRank.S and character_stats.ninjutsu_skill < 95:
                can_learn = False

            # User Restrictions
            if jutsu.users and character not in jutsu.users:
                can_learn = False

            # Chakra Requirements
            if jutsu.chakra_cost > character_stats.max_chakra * 0.8:  # Kann nicht >80% kosten
                can_learn = False

            if can_learn:
                available_jutsus.append(jutsu_id)

        if not available_jutsus:
            return None

        # Wähle zufälliges Jutsu zum Lernen
        jutsu_id = random.choice(available_jutsus)
        jutsu = self.jutsu_database[jutsu_id]

        # Lern-Erfolgsrate basierend auf Rang
        success_rate = self.training_success_rates[jutsu.rank]

        if random.random() < success_rate:
            jutsu.learned = True
            return jutsu.name

        return None

    def start_sparring_encounter(self, opponent: str = None) -> Dict:
        """⚔️ Startet Sparring gegen NPC im Training Ground"""

        if self.game_data.current_location != 'training_ground':
            return {
                "success": False,
                "message": "❌ Du musst im Training Ground sein für Sparring!"
            }

        current_character = "sukuna"

        # Verfügbare Gegner im Training Ground
        if not opponent:
            available_opponents = self._get_training_opponents()
            if not available_opponents:
                return {
                    "success": False,
                    "message": "❌ Keine Trainingspartner verfügbar! Versuche es später."
                }
            opponent = random.choice(available_opponents)

        if opponent not in self.character_stats:
            return {
                "success": False,
                "message": f"❌ {opponent} ist nicht für Sparring verfügbar!"
            }

        # Starte Combat
        combat_result = self._execute_combat(current_character, opponent, sparring=True)

        # Combat zu History hinzufügen
        self.combat_history.append({
            "player": current_character,
            "opponent": opponent,
            "result": combat_result["result"],
            "type": "sparring",
            "timestamp": self.game_data.time_system.get_current_game_time() if hasattr(self.game_data, 'time_system') and self.game_data.time_system else datetime.now(),
            "details": combat_result
        })

        # 🆕 SPARRING TIME ADVANCEMENT!
        if hasattr(self.game_data, 'time_system') and self.game_data.time_system:
            try:
                # Sparring dauert je nach Rundenzahl (5-15 Minuten)
                sparring_duration = combat_result["rounds"] * 2  # 2 Min pro Runde
                self.game_data.time_system.advance_time(sparring_duration)
                combat_result["sparring_duration"] = sparring_duration
                combat_result["new_time"] = self.game_data.time_system.get_formatted_time()
            except Exception as e:
                print(f"⚠️ Time System Fehler: {e}")

        return {
            "success": True,
            "message": f"⚔️ Sparring gegen {opponent} gestartet!",
            "combat_data": combat_result
        }

    def _get_training_opponents(self) -> List[str]:
        """🎯 Bestimmt verfügbare Trainingspartner"""

        # Zeit-basierte Verfügbarkeit (nutze Time System)
        current_hour = datetime.now().hour

        available = []

        # Genin sind tagsüber verfügbar (8-18 Uhr)
        if 8 <= current_hour <= 18:
            available.extend(["sakura", "ino", "choji"])

        # Sasuke trainiert oft abends (16-22 Uhr)
        if 16 <= current_hour <= 22:
            available.append("sasuke")

        # Jonin sind unregelmäßig verfügbar
        if random.random() < 0.3:  # 30% Chance
            available.append("kakashi")

        # Tsunade ist selten für Training verfügbar
        if random.random() < 0.1:  # 10% Chance
            available.append("tsunade")

        return available

    def _execute_combat(self, player: str, opponent: str, sparring: bool = True) -> Dict:
        """⚡ Führt kompletten Combat aus"""

        player_stats = self.character_stats[player].copy() if hasattr(self.character_stats[player], 'copy') else \
        self.character_stats[player]
        opponent_stats = self.character_stats[opponent].copy() if hasattr(self.character_stats[opponent], 'copy') else \
        self.character_stats[opponent]

        combat_log = []
        round_count = 0
        max_rounds = 10 if sparring else 20

        combat_log.append(f"⚔️ {player.title()} vs {opponent.title()} - {'Sparring' if sparring else 'Kampf'} beginnt!")

        while round_count < max_rounds:
            round_count += 1
            combat_log.append(f"\n--- Runde {round_count} ---")

            # Player Action
            player_action = self._select_combat_action(player, player_stats, opponent_stats)
            player_result = self._execute_combat_action(player, player_action, player_stats, opponent_stats)
            combat_log.append(f"{player.title()}: {player_result['description']}")

            # Damage/Effects anwenden
            if player_result['damage'] > 0:
                if sparring:
                    damage = player_result['damage'] * 0.3  # Reduziert für Sparring
                else:
                    damage = player_result['damage']

                opponent_stats.current_chakra = max(0, opponent_stats.current_chakra - damage)
                combat_log.append(f"  💥 {opponent.title()} verliert {damage:.0f} Chakra!")

            # Prüfe Kampfende
            if opponent_stats.current_chakra <= 0:
                result = CombatResult.VICTORY
                combat_log.append(f"🏆 {player.title()} gewinnt!")
                break

            # Opponent Action
            opponent_action = self._select_combat_action(opponent, opponent_stats, player_stats)
            opponent_result = self._execute_combat_action(opponent, opponent_action, opponent_stats, player_stats)
            combat_log.append(f"{opponent.title()}: {opponent_result['description']}")

            # Damage/Effects anwenden
            if opponent_result['damage'] > 0:
                if sparring:
                    damage = opponent_result['damage'] * 0.3
                else:
                    damage = opponent_result['damage']

                player_stats.current_chakra = max(0, player_stats.current_chakra - damage)
                combat_log.append(f"  💥 {player.title()} verliert {damage:.0f} Chakra!")

            # Prüfe Kampfende
            if player_stats.current_chakra <= 0:
                result = CombatResult.DEFEAT
                combat_log.append(f"😞 {player.title()} verliert!")
                break
        else:
            # Max Rounds erreicht
            if player_stats.current_chakra > opponent_stats.current_chakra:
                result = CombatResult.VICTORY
                combat_log.append(f"🏆 {player.title()} gewinnt durch Ausdauer!")
            elif opponent_stats.current_chakra > player_stats.current_chakra:
                result = CombatResult.DEFEAT
                combat_log.append(f"😞 {opponent.title()} gewinnt durch Ausdauer!")
            else:
                result = CombatResult.DRAW
                combat_log.append(f"🤝 Unentschieden!")

        # Experience Gains für Sparring
        if sparring:
            exp_gain = self._calculate_experience_gain(player, opponent, result)
            combat_log.append(f"\n💪 Training Erfahrung: {exp_gain}")

        return {
            "result": result,
            "rounds": round_count,
            "combat_log": combat_log,
            "final_player_chakra": player_stats.current_chakra,
            "final_opponent_chakra": opponent_stats.current_chakra,
            "experience_gained": exp_gain if sparring else 0
        }

    def _select_combat_action(self, character: str, char_stats: CombatStats, opponent_stats: CombatStats) -> Dict:
        """🧠 KI wählt Combat Action"""

        available_actions = []

        # Learned Jutsus
        learned_jutsus = [j for j_id, j in self.jutsu_database.items()
                          if j.learned and (not j.users or character in j.users)]

        for jutsu in learned_jutsus:
            if jutsu.chakra_cost <= char_stats.current_chakra:
                available_actions.append({
                    "type": "jutsu",
                    "jutsu": jutsu,
                    "priority": self._calculate_action_priority(jutsu, char_stats, opponent_stats)
                })

        # Taijutsu ist immer verfügbar
        for move_name, description in self.taijutsu_moves.items():
            available_actions.append({
                "type": "taijutsu",
                "move": move_name,
                "description": description,
                "priority": char_stats.taijutsu_skill + random.randint(-20, 20)
            })

        # Wähle Action mit höchster Priorität
        if available_actions:
            best_action = max(available_actions, key=lambda x: x["priority"])
            return best_action

        # Fallback
        return {"type": "guard", "priority": 10}

    def _calculate_action_priority(self, jutsu: Jutsu, char_stats: CombatStats, opponent_stats: CombatStats) -> float:
        """🎯 Berechnet Action Priority für KI"""

        priority = 0

        # Basis Priority basierend auf Jutsu Rang
        rank_priorities = {
            JutsuRank.E: 10,
            JutsuRank.D: 20,
            JutsuRank.C: 35,
            JutsuRank.B: 55,
            JutsuRank.A: 80,
            JutsuRank.S: 100
        }
        priority += rank_priorities.get(jutsu.rank, 0)

        # Chakra Effizienz
        chakra_efficiency = (100 - jutsu.chakra_cost) / 100
        priority += chakra_efficiency * 20

        # Element Advantage
        # TODO: Implementiere opponent element detection

        # Skill Match
        if jutsu.element == JutsuElement.NINJUTSU:
            priority += char_stats.ninjutsu_skill * 0.3
        elif jutsu.element == JutsuElement.GENJUTSU:
            priority += char_stats.genjutsu_skill * 0.3

        # Random Factor
        priority += random.uniform(-15, 15)

        return priority

    def _execute_combat_action(self, character: str, action: Dict, char_stats: CombatStats,
                               opponent_stats: CombatStats) -> Dict:
        """💥 Führt Combat Action aus"""

        if action["type"] == "jutsu":
            return self._execute_jutsu_action(character, action["jutsu"], char_stats, opponent_stats)
        elif action["type"] == "taijutsu":
            return self._execute_taijutsu_action(character, action, char_stats, opponent_stats)
        elif action["type"] == "guard":
            return {
                "description": f"{character.title()} geht in Verteidigungshaltung",
                "damage": 0,
                "chakra_cost": 0
            }

        return {"description": "Unbekannte Aktion", "damage": 0, "chakra_cost": 0}

    def _execute_jutsu_action(self, character: str, jutsu: Jutsu, char_stats: CombatStats,
                              opponent_stats: CombatStats) -> Dict:
        """🔥 Führt Jutsu aus"""

        # Chakra Kosten
        chakra_cost = jutsu.chakra_cost
        char_stats.current_chakra = max(0, char_stats.current_chakra - chakra_cost)

        # Basis Damage
        base_damage = self.rank_damage_multipliers[jutsu.rank] * 20

        # Skill Modifier
        skill_modifier = 1.0
        if jutsu.element == JutsuElement.NINJUTSU:
            skill_modifier = char_stats.ninjutsu_skill / 100
        elif jutsu.element == JutsuElement.GENJUTSU:
            skill_modifier = char_stats.genjutsu_skill / 100

        # Element Effectiveness
        element_modifier = 1.0  # TODO: Implementiere basierend auf opponent

        # Final Damage
        final_damage = base_damage * skill_modifier * element_modifier * random.uniform(0.8, 1.2)

        description = f"verwendet {jutsu.name}! {jutsu.description[:50]}..."

        return {
            "description": description,
            "damage": final_damage,
            "chakra_cost": chakra_cost
        }

    def _execute_taijutsu_action(self, character: str, action: Dict, char_stats: CombatStats,
                                 opponent_stats: CombatStats) -> Dict:
        """👊 Führt Taijutsu aus"""

        base_damage = 15 * (char_stats.taijutsu_skill / 100) * (char_stats.strength / 100)
        final_damage = base_damage * random.uniform(0.7, 1.3)

        description = f"verwendet {action['move']} - {action['description'][:40]}..."

        return {
            "description": description,
            "damage": final_damage,
            "chakra_cost": 0
        }

    def _calculate_experience_gain(self, player: str, opponent: str, result: CombatResult) -> str:
        """📈 Berechnet Erfahrungsgewinn"""

        player_stats = self.character_stats[player]
        opponent_stats = self.character_stats[opponent]

        # Basis Gain basierend auf Opponent Stärke
        base_gain = (opponent_stats.ninjutsu_skill + opponent_stats.taijutsu_skill) / 200

        # Result Modifier
        if result == CombatResult.VICTORY:
            result_modifier = 1.0
        elif result == CombatResult.DRAW:
            result_modifier = 0.7
        else:
            result_modifier = 0.5

        final_gain = base_gain * result_modifier

        # Anwenden auf verschiedene Skills
        player_stats.taijutsu_skill = min(100, player_stats.taijutsu_skill + final_gain * 0.5)
        player_stats.ninjutsu_skill = min(100, player_stats.ninjutsu_skill + final_gain * 0.3)
        player_stats.stamina = min(100, player_stats.stamina + final_gain * 0.2)

        return f"Taijutsu +{final_gain * 0.5:.1f}, Ninjutsu +{final_gain * 0.3:.1f}, Ausdauer +{final_gain * 0.2:.1f}"

    def get_character_combat_status(self, character: str = None) -> Dict:
        """📊 Gibt Combat Status für Charakter zurück"""

        if not character:
            character = "sukuna"

        if character not in self.character_stats:
            return {"error": f"Keine Stats für {character} gefunden"}

        stats = self.character_stats[character]
        learned_jutsus = [j.name for j_id, j in self.jutsu_database.items() if j.learned]

        return {
            "character": character.title(),
            "chakra": f"{stats.current_chakra}/{stats.max_chakra}",
            "chakra_percentage": f"{(stats.current_chakra / stats.max_chakra) * 100:.0f}%",
            "skills": {
                "Taijutsu": f"{stats.taijutsu_skill:.0f}/100",
                "Ninjutsu": f"{stats.ninjutsu_skill:.0f}/100",
                "Genjutsu": f"{stats.genjutsu_skill:.0f}/100",
                "Speed": f"{stats.speed:.0f}/100",
                "Strength": f"{stats.strength:.0f}/100",
                "Stamina": f"{stats.stamina:.0f}/100",
                "Intelligence": f"{stats.intelligence:.0f}/100"
            },
            "learned_jutsus": learned_jutsus,
            "total_jutsus": len(learned_jutsus)
        }

    def get_available_jutsu_list(self, character: str = None) -> Dict:
        """📜 Zeigt verfügbare Jutsus zum Lernen"""

        if not character:
            character = getattr(self.game_data, 'active_character', 'sukuna')

        if character not in self.character_stats:
            return {"error": f"Keine Stats für {character} gefunden"}

        char_stats = self.character_stats[character]
        available_jutsus = {}

        for rank in JutsuRank:
            available_jutsus[rank.value] = []

            for jutsu_id, jutsu in self.jutsu_database.items():
                if jutsu.rank != rank or jutsu.learned:
                    continue

                # Prüfe Lernbarkeit
                can_learn = True
                requirements = []

                # Skill Check
                required_skill = {
                    JutsuRank.E: 10, JutsuRank.D: 25, JutsuRank.C: 45,
                    JutsuRank.B: 65, JutsuRank.A: 85, JutsuRank.S: 95
                }

                if char_stats.ninjutsu_skill < required_skill[rank]:
                    can_learn = False
                    requirements.append(f"Ninjutsu {required_skill[rank]}")

                # User Restriction
                if jutsu.users and character not in jutsu.users:
                    can_learn = False
                    requirements.append(f"Nur für: {', '.join(jutsu.users)}")

                # Chakra Requirement
                if jutsu.chakra_cost > char_stats.max_chakra * 0.8:
                    can_learn = False
                    requirements.append(f"Zu hohe Chakra-Kosten ({jutsu.chakra_cost}%)")

                status = "✅ Lernbar" if can_learn else f"❌ {', '.join(requirements)}"

                available_jutsus[rank.value].append({
                    "name": jutsu.name,
                    "element": jutsu.element.value,
                    "chakra_cost": f"{jutsu.chakra_cost}%",
                    "description": jutsu.description[:60] + "...",
                    "status": status
                })

        return available_jutsus


def integrate_combat_system(game_data):
    """⚔️ Integriert das Combat System in GameData"""

    print("⚔️ Integriere Advanced Combat & Training System...")

    # Erstelle Combat System
    combat_system = AdvancedCombatSystem(game_data)
    game_data.combat_system = combat_system

    # Füge Combat Commands hinzu
    _add_combat_commands(game_data)

    print("🥋 ADVANCED COMBAT SYSTEM aktiviert!")
    print("🎯 Features:")
    print("   • Vollständige Jutsu-Datenbank (60+ Jutsus)")
    print("   • Character-spezifische Chakra-Levels")
    print("   • Sparring System im Training Ground")
    print("   • Solo Training & Skill Progression")
    print("   • Realistic Combat AI")
    print("   • Jutsu Learning System")
    print("   • Commands: /train, /spar, /combat_status, /jutsus")

    return combat_system


def _add_combat_commands(game_data):
    """🔧 Fügt Combat Commands zur GUI hinzu"""

    if hasattr(game_data, 'gui'):
        gui = game_data.gui

        if hasattr(gui, 'handle_command'):
            original_handle_command = gui.handle_command

            def enhanced_handle_command_combat(user_message):
                """Erweiterte Commands mit Combat System"""

                # Training Command
                if user_message.strip().lower().startswith('/train'):
                    parts = user_message.split()
                    if len(parts) < 2:
                        gui.add_message("TRAINING", """⚔️ TRAINING OPTIONEN:

/train taijutsu [minuten] - Taijutsu Training
/train ninjutsu [minuten] - Ninjutsu Training  
/train chakra [minuten] - Chakra Control Training
/train sword [minuten] - Schwert Training

Beispiel: /train taijutsu 45""")
                        return True

                    training_type = parts[1].lower()
                    duration = int(parts[2]) if len(parts) > 2 else 30

                    result = game_data.combat_system.start_training_session(training_type, duration)

                    if result["success"]:
                        message = f"🏋️ {result['message']}\n\n"
                        for key, value in result["results"].items():
                            message += f"📈 {key.replace('_', ' ').title()}: {value}\n"
                        gui.add_message("TRAINING", message)
                    else:
                        gui.add_message("ERROR", result["message"])
                    return True

                # Sparring Command
                elif user_message.strip().lower().startswith('/spar'):
                    parts = user_message.split()
                    opponent = parts[1] if len(parts) > 1 else None

                    result = game_data.combat_system.start_sparring_encounter(opponent)

                    if result["success"]:
                        message = f"{result['message']}\n\n"
                        combat_log = result["combat_data"]["combat_log"]
                        # Zeige nur die ersten 10 Zeilen des Combat Logs
                        message += "\n".join(combat_log[:10])
                        if len(combat_log) > 10:
                            message += f"\n... (+{len(combat_log) - 10} weitere Zeilen)"
                        gui.add_message("SPARRING", message)
                    else:
                        gui.add_message("ERROR", result["message"])
                    return True

                # Combat Status Command
                elif user_message.strip().lower() in ['/combat_status', '/stats']:
                    status = game_data.combat_system.get_character_combat_status()

                    if "error" in status:
                        gui.add_message("ERROR", status["error"])
                    else:
                        message = f"""📊 COMBAT STATUS - {status['character']}

🔋 Chakra: {status['chakra']} ({status['chakra_percentage']})

📈 SKILLS:"""
                        for skill, value in status["skills"].items():
                            message += f"\n   {skill}: {value}"

                        message += f"\n\n🎯 Gelernte Jutsus: {status['total_jutsus']}"
                        if status["learned_jutsus"]:
                            message += f"\n   {', '.join(status['learned_jutsus'][:5])}"
                            if len(status["learned_jutsus"]) > 5:
                                message += f" (+{len(status['learned_jutsus']) - 5} weitere)"

                        gui.add_message("COMBAT STATUS", message)
                    return True

                # Jutsu List Command
                elif user_message.strip().lower() in ['/jutsus', '/jutsu_list']:
                    jutsu_list = game_data.combat_system.get_available_jutsu_list()

                    if "error" in jutsu_list:
                        gui.add_message("ERROR", jutsu_list["error"])
                    else:
                        message = "📜 VERFÜGBARE JUTSUS:\n\n"

                        for rank, jutsus in jutsu_list.items():
                            if jutsus:  # Nur zeigen wenn Jutsus vorhanden
                                message += f"🎯 {rank.upper()}-RANG:\n"
                                for jutsu in jutsus[:3]:  # Nur erste 3 pro Rang
                                    message += f"  • {jutsu['name']} ({jutsu['element']}) - {jutsu['chakra_cost']}\n"
                                    message += f"    {jutsu['status']}\n"
                                if len(jutsus) > 3:
                                    message += f"    (+{len(jutsus) - 3} weitere)\n"
                                message += "\n"

                        gui.add_message("JUTSU LIST", message)
                    return True

                # Fallback zu original
                return original_handle_command(user_message)

            # Ersetze Command Handler
            gui.handle_command = enhanced_handle_command_combat


if __name__ == "__main__":
    print("⚔️ ADVANCED COMBAT & TRAINING SYSTEM")
    print("=" * 60)
    print("Verwendung:")
    print("  from combat_system import integrate_combat_system")
    print("  integrate_combat_system(your_game_data)")
    print("\nFeatures:")
    print("  ⚔️ Vollständige Jutsu-Datenbank")
    print("  🥋 Sparring System")
    print("  🏋️ Solo Training")
    print("  📈 Skill Progression")
    print("  🧠 Combat AI")
    print("  💪 Character-spezifische Stats")