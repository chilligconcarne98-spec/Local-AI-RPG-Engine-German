# -*- coding: utf-8 -*-
"""
🗓️ DAILY COOLDOWN SYSTEM EXTENSION für backstory.py
Verhindert dass Topics mehrfach am Tag erwähnt werden
"""

from datetime import datetime, timedelta
import json
import os

# DAILY MENTIONS TRACKING
DAILY_MENTIONS = {}
LAST_RESET_DATE = None


def get_current_game_day():
    """Gibt aktuellen Game-Tag als String zurück (YYYY-MM-DD)"""
    from backstory import get_current_game_time
    current_time = get_current_game_time()
    return current_time.strftime('%Y-%m-%d')


def get_current_game_hour():
    """Gibt aktuelle Game-Stunde zurück (0-23)"""
    from backstory import get_current_game_time
    current_time = get_current_game_time()
    return current_time.hour


def reset_daily_mentions_if_new_day():
    """Reset daily mentions wenn neuer Tag"""
    global DAILY_MENTIONS, LAST_RESET_DATE

    current_day = get_current_game_day()

    if LAST_RESET_DATE != current_day:
        DAILY_MENTIONS = {}
        LAST_RESET_DATE = current_day
        print(f"🗓️ Daily mentions reset für neuen Tag: {current_day}")


def has_mentioned_today(topic, character="tsunade"):
    """Check ob Topic heute schon erwähnt wurde"""
    reset_daily_mentions_if_new_day()

    current_day = get_current_game_day()
    key = f"{character}_{topic}_{current_day}"

    return key in DAILY_MENTIONS


def mark_mentioned_today(topic, character="tsunade"):
    """Markiert Topic als heute erwähnt"""
    reset_daily_mentions_if_new_day()

    current_day = get_current_game_day()
    key = f"{character}_{topic}_{current_day}"

    DAILY_MENTIONS[key] = {
        "mentioned_at": datetime.now().isoformat(),
        "game_day": current_day,
        "character": character,
        "topic": topic
    }

    print(f"📝 Marked as mentioned today: {character} -> {topic}")


def can_mention_topic_today(topic, character="tsunade", force_allow_hours=None):
    """
    Prüft ob Topic heute erwähnt werden darf

    Args:
        topic: Das Topic (z.B. "food", "training", "safety")
        character: Character der erwähnt (default: tsunade)
        force_allow_hours: List von Stunden wo Topic trotzdem erlaubt ist (z.B. [7,12,18] für Mahlzeiten)
    """
    reset_daily_mentions_if_new_day()

    # Check if already mentioned today
    if has_mentioned_today(topic, character):
        # Check force allow hours
        if force_allow_hours:
            current_hour = get_current_game_hour()
            if current_hour in force_allow_hours:
                return True, f"force_allowed_hour_{current_hour}"

        return False, "already_mentioned_today"

    return True, "first_mention_today"


def get_daily_mentions_status(character="tsunade"):
    """Gibt Status aller heutigen Mentions zurück"""
    reset_daily_mentions_if_new_day()

    current_day = get_current_game_day()
    today_mentions = {}

    for key, data in DAILY_MENTIONS.items():
        if data["game_day"] == current_day and data["character"] == character:
            today_mentions[data["topic"]] = data

    return today_mentions


def save_daily_mentions_to_autosave():
    """Speichert daily mentions ins autosave"""
    try:
        from backstory import AUTOSAVE_PATH, _load_full_state

        # Load existing autosave
        existing_state = _load_full_state(AUTOSAVE_PATH) or {}

        # Add daily mentions data
        existing_state["daily_mentions"] = DAILY_MENTIONS
        existing_state["last_reset_date"] = LAST_RESET_DATE

        # Save back
        os.makedirs(os.path.dirname(AUTOSAVE_PATH), exist_ok=True)
        with open(AUTOSAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(existing_state, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"⚠️ Daily mentions save error: {e}")
        return False


def load_daily_mentions_from_autosave():
    """Lädt daily mentions aus autosave"""
    global DAILY_MENTIONS, LAST_RESET_DATE

    try:
        from backstory import AUTOSAVE_PATH, _load_full_state

        state = _load_full_state(AUTOSAVE_PATH)
        if state:
            DAILY_MENTIONS = state.get("daily_mentions", {})
            LAST_RESET_DATE = state.get("last_reset_date", None)

            print(f"✅ Daily mentions loaded: {len(DAILY_MENTIONS)} entries")

    except Exception as e:
        print(f"⚠️ Daily mentions load error: {e}")
        DAILY_MENTIONS = {}
        LAST_RESET_DATE = None


def get_daily_cooldown_context_for_prompt(character="tsunade"):
    """Erstellt Context für Prompt mit daily mention rules"""
    reset_daily_mentions_if_new_day()

    current_day = get_current_game_day()
    current_hour = get_current_game_hour()
    today_mentions = get_daily_mentions_status(character)

    context = f"""
🗓️ DAILY MENTION RULES - Heute: {current_day}, {current_hour}:00 Uhr

BEREITS HEUTE ERWÄHNT:
"""

    if today_mentions:
        for topic, data in today_mentions.items():
            context += f"- {topic.upper()}: ❌ Bereits erwähnt\n"
    else:
        context += "- Noch nichts erwähnt heute\n"

    context += """
⚠️ WICHTIGE REGEL:
- Themen die heute bereits erwähnt wurden NICHT nochmal erwähnen
- Ausnahme: Mahlzeiten zu Essenszeiten (7-9, 12-14, 18-20 Uhr)
- Fokussiere auf andere Gesprächsthemen
"""

    # Special meal time allowance
    if 7 <= current_hour <= 9 or 12 <= current_hour <= 14 or 18 <= current_hour <= 20:
        if "food" in today_mentions:
            context += f"\n🍽️ ESSENSZEIT ({current_hour}:00): Essen erwähnen trotz heute schon erwähnt OK"

    return context


# USAGE EXAMPLES FOR MATERNAL SYSTEM:
def maternal_daily_check(topic):
    """Helper für maternal system daily checks"""
    can_mention, reason = can_mention_topic_today(
        topic,
        character="tsunade",
        force_allow_hours=[7, 8, 9, 12, 13, 14, 18, 19, 20] if topic == "food" else None
    )

    if can_mention:
        mark_mentioned_today(topic, "tsunade")
        return True

    print(f"🚫 Daily cooldown: {topic} blocked - {reason}")
    return False


def detect_and_mark_mentioned_topics(response_text, character="tsunade"):
    """Auto-detects topics mentioned in AI response and marks them as mentioned today"""

    response_lower = response_text.lower()

    # FOOD DETECTION
    food_keywords = [
        "frühstück", "essen", "onigiri", "früchte", "lecker", "hungrig",
        "kochen", "zubereitet", "mahlzeit", "brot", "reis", "suppe",
        "mittagessen", "abendessen", "snack", "trinken"
    ]
    if any(keyword in response_lower for keyword in food_keywords):
        mark_mentioned_today("food", character)
        print(f"📝 Auto-detected: FOOD mentioned by {character}")

    # SLEEP DETECTION
    sleep_keywords = [
        "schlafen", "müde", "geschlafen", "aufgewacht", "träumen",
        "bett", "ausgeruht", "schlafzeit", "gute nacht", "aufstehen"
    ]
    if any(keyword in response_lower for keyword in sleep_keywords):
        mark_mentioned_today("sleep", character)
        print(f"📝 Auto-detected: SLEEP mentioned by {character}")

    # TRAINING DETECTION
    training_keywords = [
        "training", "üben", "trainieren", "jutsu", "kämpfen",
        "mission", "ninja", "fähigkeiten", "chakra", "kampf"
    ]
    if any(keyword in response_lower for keyword in training_keywords):
        mark_mentioned_today("training", character)
        print(f"📝 Auto-detected: TRAINING mentioned by {character}")

    # SAFETY/PROTECTION DETECTION
    safety_keywords = [
        "sicher", "schutz", "gefahr", "vorsichtig", "aufpassen",
        "verletzt", "sorge", "angst", "beschützen"
    ]
    if any(keyword in response_lower for keyword in safety_keywords):
        mark_mentioned_today("safety", character)
        print(f"📝 Auto-detected: SAFETY mentioned by {character}")

    # WEATHER DETECTION
    weather_keywords = [
        "wetter", "sonnig", "regen", "warm", "kalt", "wind",
        "schnee", "wolken", "himmel"
    ]
    if any(keyword in response_lower for keyword in weather_keywords):
        mark_mentioned_today("weather", character)
        print(f"📝 Auto-detected: WEATHER mentioned by {character}")

    # VILLAGE/SOCIAL DETECTION
    village_keywords = [
        "dorf", "konoha", "leute", "nachbarn", "hokage",
        "andere ninja", "bewohner", "freunde"
    ]
    if any(keyword in response_lower for keyword in village_keywords):
        mark_mentioned_today("village", character)
        print(f"📝 Auto-detected: VILLAGE mentioned by {character}")

    # Save updated mentions
    save_daily_mentions_to_autosave()


# Initialize on import
load_daily_mentions_from_autosave()