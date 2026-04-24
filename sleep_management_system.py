# -*- coding: utf-8 -*-
"""
🌙 SLEEP MANAGEMENT SYSTEM
Verwaltet Sukuna's Schlaf-Zyklen mit Zeit-basierter Kontrolle
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple


class SleepManagementSystem:
    """🛏️ System für Schlaf-Management mit realistischen Zeiten"""

    def __init__(self, game_data):
        self.game_data = game_data
        self.is_sleeping = False
        self.sleep_start_time = None
        self.wake_up_time = None

        # Schlaf-Einstellungen
        self.earliest_bedtime = 20  # 20:00 Uhr
        self.latest_bedtime = 23  # 23:00 Uhr
        self.wake_up_hour = 7  # 07:00 Uhr
        self.minimum_sleep_hours = 8

        print("🌙 Sleep Management System initialisiert!")

    def can_sleep(self) -> Tuple[bool, str]:
        """🛏️ Prüft ob Sukuna schlafen gehen kann"""

        # 1. Prüfe Location
        current_location = getattr(self.game_data, 'current_location', '')
        if current_location != 'sukunas_zimmer':
            return False, "❌ Du musst in deinem Zimmer sein um schlafen zu gehen!"

        # 2. Prüfe ob bereits schlafend
        if self.is_sleeping:
            return False, "💤 Du schläfst bereits!"

        # 3. Prüfe Uhrzeit
        current_time = self.get_current_game_time()

        if current_time.hour < self.earliest_bedtime and current_time.hour >= self.wake_up_hour:
            return False, f"⏰ Es ist erst {current_time.hour:02d}:{current_time.minute:02d} Uhr! Du kannst erst ab {self.earliest_bedtime}:00 Uhr schlafen gehen."

        return True, "✅ Du kannst schlafen gehen!"

    def go_to_sleep(self) -> Tuple[bool, str]:
        """🛏️ Sukuna geht schlafen"""

        can_sleep, message = self.can_sleep()
        if not can_sleep:
            return False, message

        # Schlaf initialisieren
        current_time = self.get_current_game_time()
        self.sleep_start_time = current_time
        self.is_sleeping = True

        # Berechne Aufwachzeit (nächster Tag 07:00)
        next_day = current_time.date() + timedelta(days=1)
        self.wake_up_time = datetime.combine(next_day, datetime.min.time()) + timedelta(hours=self.wake_up_hour)

        # Zeit vorspulen bis Aufwachen
        self.advance_time_to_wake_up()

        sleep_duration = (self.wake_up_time - self.sleep_start_time).total_seconds() / 3600

        sleep_message = f"""🌙 **GUTE NACHT, SUKUNA!**

🛏️ Du legst dich in dein Bett und schließt die Augen...

⏰ **Schlafzeit**: {self.sleep_start_time.strftime('%H:%M')} Uhr
🌅 **Aufwachen**: {self.wake_up_time.strftime('%H:%M')} Uhr  
⌛ **Schlafdauer**: {sleep_duration:.1f} Stunden

💤 Du schläfst tief und fest... Die Zeit vergeht...

🌅 **GUTEN MORGEN!** 
Es ist {self.wake_up_time.strftime('%H:%M')} Uhr am nächsten Tag.
Du fühlst dich ausgeruht und bereit für neue Abenteuer!"""

        # Schlaf beenden
        self.wake_up()

        return True, sleep_message

    def wake_up(self):
        """🌅 Sukuna wacht auf"""
        self.is_sleeping = False
        self.sleep_start_time = None
        self.wake_up_time = None

        # Update Game State für neuen Tag
        if hasattr(self.game_data, 'game_state'):
            current_day = self.game_data.game_state.get('day', 1)
            self.game_data.game_state['day'] = current_day + 1

        print(f"🌅 Sukuna ist aufgewacht! Neuer Tag: {self.game_data.game_state.get('day', 1)}")

    def advance_time_to_wake_up(self):
        """⏰ Spult Zeit bis zum Aufwachen vor"""

        if not hasattr(self.game_data, 'time_system') or not self.game_data.time_system:
            return

        try:
            # Berechne Zeitunterschied in Minuten
            time_diff = self.wake_up_time - self.sleep_start_time
            minutes_to_advance = int(time_diff.total_seconds() / 60)

            # Advance Game Time
            self.game_data.time_system.advance_time(minutes_to_advance)

            print(f"⏰ Zeit vorgerückt um {minutes_to_advance} Minuten (Schlaf)")

        except Exception as e:
            print(f"⚠️ Fehler beim Vorspulen der Zeit: {e}")

    def get_current_game_time(self) -> datetime:
        """🕐 Holt aktuelle Spielzeit"""

        # Versuche Game Time System
        if hasattr(self.game_data, 'time_system') and self.game_data.time_system:
            try:
                return self.game_data.time_system.get_current_game_time()
            except:
                pass

        # Fallback zu Real Time
        return datetime.now()

    def get_sleep_status(self) -> str:
        """🛏️ Status des Schlaf-Systems"""

        current_time = self.get_current_game_time()

        if self.is_sleeping:
            return f"💤 **SCHLAFEND** (seit {self.sleep_start_time.strftime('%H:%M')})"

        can_sleep, reason = self.can_sleep()

        status = f"""🌙 **SCHLAF-STATUS**

⏰ **Aktuelle Zeit**: {current_time.strftime('%H:%M')} Uhr
📍 **Location**: {getattr(self.game_data, 'current_location', 'Unbekannt')}
🛏️ **Schlafbereit**: {'✅ Ja' if can_sleep else '❌ Nein'}

🔄 **Bedingungen:**
📍 Im Zimmer: {'✅' if getattr(self.game_data, 'current_location', '') == 'sukunas_zimmer' else '❌'}
⏰ Nach 20:00: {'✅' if current_time.hour >= self.earliest_bedtime or current_time.hour < self.wake_up_hour else '❌'}

💡 **Verfügbare Commands:**
• /schlafen_gehen - Ins Bett gehen (nur im Zimmer, 20:00-23:00)
• /schlaf_status - Aktueller Status
"""

        if not can_sleep:
            status += f"\n⚠️ **Hinweis**: {reason}"

        return status


def integrate_sleep_system(game_data):
    """🌙 Integriert das Sleep System in die Hauptanwendung"""

    # Erstelle Sleep System
    game_data.sleep_system = SleepManagementSystem(game_data)

    print("🌙 SLEEP MANAGEMENT SYSTEM erfolgreich integriert!")
    print("💡 Verfügbare Commands:")
    print("   • /schlafen_gehen - Schlafen (nur im Zimmer ab 20:00)")
    print("   • /schlaf_status - Sleep System Status")

    return game_data.sleep_system


if __name__ == "__main__":
    print("🌙 SLEEP MANAGEMENT SYSTEM")
    print("=" * 50)
    print("✨ Features:")
    print("• Zeit-basierte Schlaf-Kontrolle (20:00-23:00)")
    print("• Location-Requirement (nur im Zimmer)")
    print("• Automatisches Aufwachen (07:00)")
    print("• Game-Time Integration")
    print("• Tag-Progression System")