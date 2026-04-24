# -*- coding: utf-8 -*-
"""
⏰ GAME TIME SYSTEM - Separates Zeitsystem für das RPG
NPCs wissen jetzt die Zeit und reagieren darauf!
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random
import json


class TimePeriod(Enum):
    """Tagesperioden"""
    DAWN = "dawn"  # 5:00 - 7:00
    EARLY_MORNING = "early_morning"  # 7:00 - 9:00
    MORNING = "morning"  # 9:00 - 12:00
    MIDDAY = "midday"  # 12:00 - 13:00
    AFTERNOON = "afternoon"  # 13:00 - 17:00
    EVENING = "evening"  # 17:00 - 20:00
    NIGHT = "night"  # 20:00 - 23:00
    LATE_NIGHT = "late_night"  # 23:00 - 5:00


class WeatherType(Enum):
    """Wettertypen"""
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORMY = "stormy"
    SNOWY = "snowy"


@dataclass
class GameTime:
    """Aktueller Zeitpunkt im Spiel"""
    datetime: datetime
    period: TimePeriod
    weather: WeatherType
    season: str

    def to_dict(self) -> Dict:
        """Konvertiert zu Dictionary für Speicherung"""
        return {
            "datetime": self.datetime.isoformat(),
            "period": self.period.value,
            "weather": self.weather.value,
            "season": self.season
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Erstellt GameTime aus Dictionary"""
        return cls(
            datetime=datetime.fromisoformat(data["datetime"]),
            period=TimePeriod(data["period"]),
            weather=WeatherType(data["weather"]),
            season=data["season"]
        )


class GameTimeSystem:
    """⏰ Hauptsystem für Ingame-Zeit"""

    def __init__(self):
        # Startzeitpunkt: Samstag Morgen 7:15 (aus characters.py)
        self.start_time = datetime(2023, 6, 10, 7, 15)  # Samstag
        self.real_start_time = datetime.now()

        # Zeit-Verhältnisse (anpassbar)
        self.time_multiplier = 3  # 1 Real-Minute = 3 Ingame-Minuten

        # Aktuelles Wetter
        self.current_weather = WeatherType.SUNNY
        self.current_season = "Frühling"

        # Zeit-Events
        self.scheduled_events = {}
        self.daily_routines = {}

        print(f"⏰ Game Time System initialisiert")
        print(f"🕐 Start: {self.get_formatted_time()}")

    def get_current_game_time(self) -> datetime:
        """Gibt aktuelle Ingame-Zeit zurück"""
        real_elapsed = datetime.now() - self.real_start_time
        game_elapsed = real_elapsed * self.time_multiplier
        return self.start_time + game_elapsed

    def get_time_period(self) -> TimePeriod:
        """Bestimmt aktuelle Tagesperiode"""
        current = self.get_current_game_time()
        hour = current.hour

        if 5 <= hour < 7:
            return TimePeriod.DAWN
        elif 7 <= hour < 9:
            return TimePeriod.EARLY_MORNING
        elif 9 <= hour < 12:
            return TimePeriod.MORNING
        elif 12 <= hour < 13:
            return TimePeriod.MIDDAY
        elif 13 <= hour < 17:
            return TimePeriod.AFTERNOON
        elif 17 <= hour < 20:
            return TimePeriod.EVENING
        elif 20 <= hour < 23:
            return TimePeriod.NIGHT
        else:
            return TimePeriod.LATE_NIGHT

    def get_current_game_state(self) -> GameTime:
        """Gibt kompletten aktuellen Zeitstatus zurück"""
        return GameTime(
            datetime=self.get_current_game_time(),
            period=self.get_time_period(),
            weather=self.current_weather,
            season=self.current_season
        )

    def get_formatted_time(self) -> str:
        """Formatierte Zeit für Display"""
        current = self.get_current_game_time()
        weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        weekday = weekdays[current.weekday()]

        period_names = {
            TimePeriod.DAWN: "Morgendämmerung",
            TimePeriod.EARLY_MORNING: "Früher Morgen",
            TimePeriod.MORNING: "Vormittag",
            TimePeriod.MIDDAY: "Mittagszeit",
            TimePeriod.AFTERNOON: "Nachmittag",
            TimePeriod.EVENING: "Abend",
            TimePeriod.NIGHT: "Nacht",
            TimePeriod.LATE_NIGHT: "Späte Nacht"
        }

        period_name = period_names.get(self.get_time_period(), "Unbekannt")
        weather_name = {
            WeatherType.SUNNY: "☀️ Sonnig",
            WeatherType.CLOUDY: "☁️ Bewölkt",
            WeatherType.RAINY: "🌧️ Regnerisch",
            WeatherType.STORMY: "⛈️ Stürmisch",
            WeatherType.SNOWY: "❄️ Schnee"
        }.get(self.current_weather, "🌤️")

        return f"🕐 {weekday}, {current.strftime('%H:%M')} Uhr ({period_name})\n🌤️ {weather_name}, {self.current_season}"

    def is_meal_time(self) -> Optional[str]:
        """Prüft ob Essenszeit ist"""
        hour = self.get_current_game_time().hour

        if 7 <= hour <= 9:
            return "Frühstück"
        elif 12 <= hour <= 14:
            return "Mittagessen"
        elif 18 <= hour <= 20:
            return "Abendessen"
        elif 21 <= hour <= 23:
            return "Spätsnack"
        return None

    def is_sleep_time(self) -> bool:
        """Prüft ob Schlafenszeit ist"""
        period = self.get_time_period()
        return period in [TimePeriod.NIGHT, TimePeriod.LATE_NIGHT]

        # Montag-Freitag, 9-15 Uhr
        return weekday < 5 and 9 <= hour < 15

    def is_training_time(self) -> bool:
        """Prüft ob typische Trainingszeit"""
        period = self.get_time_period()
        return period in [TimePeriod.MORNING, TimePeriod.AFTERNOON, TimePeriod.EARLY_MORNING]

    def get_appropriate_activities(self) -> List[str]:
        """Gibt zeitgemäße Aktivitäten zurück"""
        period = self.get_time_period()

        activities = {
            TimePeriod.DAWN: ["meditation", "early_walk", "quiet_activities"],
            TimePeriod.EARLY_MORNING: ["breakfast", "morning_routine", "light_training"],
            TimePeriod.MORNING: ["training", "missions", "work"],
            TimePeriod.MIDDAY: ["lunch", "rest", "indoor_activities"],
            TimePeriod.AFTERNOON: ["training", "missions", "studying", "social_activities"],
            TimePeriod.EVENING: ["dinner", "family_time", "relaxation", "light_activities"],
            TimePeriod.NIGHT: ["dinner", "winding_down", "quiet_talks", "preparation_for_sleep"],
            TimePeriod.LATE_NIGHT: ["sleep", "bedtime_routine", "emergency_only"]
        }

        return activities.get(period, ["general_activities"])

    def get_time_context_for_llm(self) -> str:
        """Gibt Zeit-Kontext für LLM zurück"""
        game_time = self.get_current_game_state()
        activities = self.get_appropriate_activities()
        meal_time = self.is_meal_time()

        context = f"""
⏰ AKTUELLE ZEIT: {self.get_formatted_time()}

🎯 ZEITKONTEXT:
• Tagesperiode: {game_time.period.value}
• Angemessene Aktivitäten: {', '.join(activities)}
"""



        if self.is_sleep_time():
            context += f"• 😴 SCHLAFENSZEIT: NPCs sollten auf Müdigkeit achten\n"

        if self.is_training_time():
            context += f"• 💪 TRAININGSZEIT: Gute Zeit für körperliche Aktivitäten\n"

        context += f"""
🎭 NPCs reagieren auf:
• Tageszeit (müde abends, energisch morgens)
• Wetterlagen ({game_time.weather.value})
• Angemessene Aktivitäten für die Uhrzeit
• Essenszeiten und Schlafenszeiten
"""

        return context

    def advance_time(self, minutes: int):
        """Spult Zeit vorwärts (für Events/Tests)"""
        self.start_time += timedelta(minutes=minutes)
        print(f"⏰ Zeit vorgestellt um {minutes} Minuten: {self.get_formatted_time()}")

    def set_weather(self, weather: WeatherType):
        """Ändert Wetter"""
        self.current_weather = weather
        print(f"🌤️ Wetter geändert zu: {weather.value}")

    def set_season(self, season: str):
        """Ändert Jahreszeit"""
        self.current_season = season
        print(f"🌿 Jahreszeit geändert zu: {season}")

    def schedule_event(self, time: datetime, event_name: str, description: str):
        """Plant zeitbasiertes Event"""
        self.scheduled_events[time] = {
            "name": event_name,
            "description": description,
            "triggered": False
        }
        print(f"📅 Event geplant: {event_name} um {time.strftime('%H:%M')}")

    def check_scheduled_events(self) -> List[Dict]:
        """Prüft ob geplante Events eingetreten sind"""
        current_time = self.get_current_game_time()
        triggered_events = []

        for event_time, event_data in self.scheduled_events.items():
            if not event_data["triggered"] and current_time >= event_time:
                event_data["triggered"] = True
                triggered_events.append({
                    "time": event_time,
                    "name": event_data["name"],
                    "description": event_data["description"]
                })

        return triggered_events

    def get_character_schedule_suggestion(self, character_name: str) -> str:
        """Schlägt character-spezifische Aktivitäten vor"""
        period = self.get_time_period()

        # Character-spezifische Schedules
        character_schedules = {
            "tsunade": {
                TimePeriod.EARLY_MORNING: "Hokage-Büro Vorbereitung oder Sukuna-Care",
                TimePeriod.MORNING: "Hokage-Pflichten oder medizinische Arbeit",
                TimePeriod.AFTERNOON: "Meetings",
                TimePeriod.EVENING: "Familienzeit mit Sukuna",
                TimePeriod.NIGHT: "Sukuna ins Bett bringen",
                TimePeriod.LATE_NIGHT: "Sake trinken oder arbeiten (wenn Sukuna schläft)"
            },

            "naruto": {
                TimePeriod.EARLY_MORNING: "Training oder Ramen essen",
                TimePeriod.MORNING: "Missionen oder Academy (falls noch)",
                TimePeriod.AFTERNOON: "Training mit Team oder Freunde treffen",
                TimePeriod.EVENING: "Ramen essen oder Freunde besuchen",
                TimePeriod.NIGHT: "Entspannen oder früh schlafen",
                TimePeriod.LATE_NIGHT: "Schlafen (früh aufstehen!)"
            },

            "sasuke": {
                TimePeriod.EARLY_MORNING: "Solo Training",
                TimePeriod.MORNING: "Team Training oder Missionen",
                TimePeriod.AFTERNOON: "Intensives Training",
                TimePeriod.EVENING: "Training oder Meditation",
                TimePeriod.NIGHT: "Training oder Planen",
                TimePeriod.LATE_NIGHT: "Training oder Nachdenken"
            },

            "sakura": {
                TimePeriod.EARLY_MORNING: "Medizin-Studium oder Vorbereitung",
                TimePeriod.MORNING: "Hospital-Arbeit oder Training",
                TimePeriod.AFTERNOON: "Training oder medizinische Praxis",
                TimePeriod.EVENING: "Studium oder soziale Zeit",
                TimePeriod.NIGHT: "Entspannung oder Lesen",
                TimePeriod.LATE_NIGHT: "Schlafen"
            }
        }

        if character_name in character_schedules:
            return character_schedules[character_name].get(period, "Allgemeine Aktivitäten")

        # Default Schedule
        return {
            TimePeriod.EARLY_MORNING: "Aufwachen und Morgenroutine",
            TimePeriod.MORNING: "Arbeit/Training/Academy",
            TimePeriod.AFTERNOON: "Fortsetzung der Tagesaktivitäten",
            TimePeriod.EVENING: "Entspannung und soziale Zeit",
            TimePeriod.NIGHT: "Abendessen und Vorbereitung auf Schlaf",
            TimePeriod.LATE_NIGHT: "Schlafen"
        }.get(period, "Ruhen")

    def get_time_summary(self) -> str:
        """Gibt Zeit-System Summary zurück"""
        current = self.get_current_game_state()

        summary = f"""⏰ **GAME TIME SYSTEM STATUS:**

{self.get_formatted_time()}

📅 **Details:**
• Wochentag: {current.datetime.strftime('%A')}
• Kalenderdatum: {current.datetime.strftime('%d.%m.%Y')}
• Tagesperiode: {current.period.value}

🎯 **Aktuelle Situation:**"""


        if self.is_sleep_time():
            summary += f"\n😴 Schlafenszeit - NPCs achten auf Müdigkeit"

        if self.is_training_time():
            summary += f"\n💪 Gute Trainingszeit"

        summary += f"\n\n🎭 **Angemessene Aktivitäten:** {', '.join(self.get_appropriate_activities())}"

        # Nächste wichtige Zeitpunkte
        summary += f"\n\n⏳ **Kommende Zeitpunkte:**"
        current_hour = current.datetime.hour

        if current_hour < 7:
            summary += f"\n• Frühstück in {7 - current_hour} Stunden"
        elif current_hour < 12:
            summary += f"\n• Mittagessen in {12 - current_hour} Stunden"
        elif current_hour < 18:
            summary += f"\n• Abendessen in {18 - current_hour} Stunden"
        elif current_hour < 21:
            summary += f"\n• Schlafenszeit in {21 - current_hour} Stunden"

        return summary


def integrate_time_system(game_data):
    """⏰ Integriert das Time System in GameData"""

    # Erstelle Time System
    time_system = GameTimeSystem()
    game_data.time_system = time_system

    # Erweitere LLM Response für Zeit-Kontext
    if hasattr(game_data, 'family_time_enhanced_llm_response'):
        original_get_llm_response = game_data.get_llm_response

        def time_aware_llm_response(user_input: str) -> str:
            """LLM Response mit Zeit-Kontext"""

            # Normale Response generieren
            base_response = game_data.family_time_enhanced_llm_response(user_input)

            # Zeit-Kontext für NPCs
            time_context = time_system.get_time_context_for_llm()

            # Character-spezifische Schedule-Info
            current_character = getattr(game_data, 'active_character', 'tsunade')
            character_schedule = time_system.get_character_schedule_suggestion(current_character)

            # Events prüfen
            events = time_system.check_scheduled_events()

            # Zeit-sensitive Ergänzungen
            time_additions = []

            # Essenszeit-Reaktionen
            meal_time = time_system.is_meal_time()
            if meal_time and current_character in ["tsunade", "choji", "naruto"] and random.random() < 0.2:
                if current_character == "tsunade":
                    time_additions.append(
                        f"*bemerkt die Uhrzeit* 'Es ist {meal_time}. Hast du schon gegessen?'")
                elif current_character == "naruto":
                    time_additions.append(
                        f"*Magen knurrt* 'Oh! Es ist {meal_time}-Zeit, dattebayo! Lass uns Ramen holen!'")
                elif current_character == "choji":
                    time_additions.append(f"*denkt ans Essen* 'Es ist {meal_time}-Zeit... ich könnte was kochen!'")

            # Schlafenszeit-Reaktionen
            if time_system.is_sleep_time() and current_character in ["tsunade", "sakura", "kakashi"] and random.random() < 0.2:
                if current_character == "tsunade":
                    time_additions.append(f"*schaut auf die Uhr* 'Es wird spät, Sukuna. Zeit fürs Bett, mein Schatz.'")
                elif current_character == "sakura":
                    time_additions.append(
                        f"*gähnt leicht* 'Es ist schon spät... du solltest langsam an den Schlaf denken.'")

            # Kombiniere Response
            final_response = base_response
            if time_additions:
                final_response += f"\n\n{random.choice(time_additions)}"

            return final_response

        # Ersetze LLM Response
        game_data.get_llm_response = time_aware_llm_response

    print("⏰ TIME SYSTEM erfolgreich integriert!")
    print("🕐 Features aktiviert:")
    print("   • Echte Ingame-Zeit mit Tagesperioden")
    print("   • NPCs reagieren auf Tageszeit")
    print("   • Essens- und Schlafzeiten-Erkennung")
    print("   • Character-spezifische Schedules")
    print("   • Wetter- und Jahreszeiten-System")

    return time_system


if __name__ == "__main__":
    print("⏰ GAME TIME SYSTEM")
    print("====================")

    # Test das System
    time_sys = GameTimeSystem()
    print(f"✅ Initialisiert: {time_sys.get_formatted_time()}")
    print(f"✅ Periode: {time_sys.get_time_period().value}")
    print(f"✅ Essenszeit: {time_sys.is_meal_time()}")
    print(f"✅ Aktivitäten: {time_sys.get_appropriate_activities()}")