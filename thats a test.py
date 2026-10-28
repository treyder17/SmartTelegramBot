import random

# Brawler emojis by difficulty


# Score by difficulty
score_map = {"easy": 1, "mid": 5, "hard": 25, "unreal": 50, "impossible": 100}

# Just outputting structure to check
total_brawlers = sum(len(brawlers[level]) for level in brawlers)
total_points = sum(score_map[level] * len(brawlers[level]) for level in brawlers)
total_brawlers, total_points
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import json
import random

bot = Client("my_bot", api_id=123456, api_hash="your_api_hash", bot_token="your_bot_token")

# Pfad zur Nutzerdaten-Datei
USER_FILE = "users.json"

# Beispiel-Datenstruktur: {user_id: {"points": 0}}
def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

# Schwierigkeitsgrade
difficulty_levels = {
    "easy": {"points": 1},
    "mid": {"points": 5},
    "hard": {"points": 25},
    "unreal": {"points": 50},
    "impossible": {"points": 100}
}

# Liste aller Brawler mit Schwierigkeitsgrad und Emojis
brawlers = {
    "easy": {
        "Shelly": "💥🔫👩‍🌾", "Bull": "🐃💥😠", "Colt": "🤠🔫😎", "Brock": "🚀🔥🕶️",
        "Poco": "🎸💀🎶", "Nita": "🐻👧🔥", "El Primo": "🤼‍♂️🔥💪", "Dynamike": "🧨👴💣",
        "Jessie": "🔧🐶📡", "Barley": "🍺🤖🧪", "Rosa": "🥊🌹🌱", "8-Bit": "🕹️👾💥",
        "Piper": "🎯💋☂️", "Bea": "🐝🎯😇", "Frank": "🔨🧟‍♂️😤", "Bo": "🏹🦅🌲", "Pam": "💉🔧🤱"
    },
    "mid": {
        "Penny": "🏴‍☠️💰🔫", "Darryl": "🛢️🔫🤖", "Carl": "⛏️🚋👷", "Rico": "🤖🔫💎",
        "Jacky": "👷‍♀️🔨💥", "Bibi": "⚾🦹‍♀️🍬", "Max": "⚡🏃‍♀️💨", "Edgar": "🧣💀🦇",
        "Emz": "🧴💀📱", "Lou": "🍦🤖❄️", "Stu": "🤹‍♂️🔥🏍️", "Fang": "🥋👟💥",
        "Tara": "🃏👁️💫", "Gene": "🧞‍♂️👐💨", "Mortis": "🧛‍♂️⚰️🔮", "Sprout": "🌱📦🧠",
        "Squeak": "🧼🐶💥", "Crow": "🐦☠️🗡️", "Spike": "🌵💣😄", "Leon": "🦎🌀🧢"
    },
    "hard": {
        "Grom": "📦💣😱", "Belle": "👵🔫💰", "Byron": "💉📚🧙‍♂️", "Buzz": "🕶️🦈🔫",
        "Janet": "🎤🎶🛩️", "Gray": "🧔🪄🚪", "Ruffs": "🐶👮‍♂️📦", "Otis": "🐙🎨🔇",
        "Colette": "📓💘🔫", "Sandy": "😴🌪️✨", "Meg": "👩‍🔧🤖⚡", "Amber": "🔥👩‍🦰🧴",
        "Chester": "🤡🎁🎲", "Mr. P": "🐧📦🎩", "Ash": "🧹🤖😡", "Gale": "❄️👴🔧",
        "Lola": "🎬💄📸", "Buster": "📽️🛡️🎞️", "Nani": "🤖📸🧠"
    },
    "unreal": {
        "Melodie": "🎵🎤😄", "Eve": "🐞👶🚀", "Chuck": "🚂🧙‍♂️📞", "Mico": "🪩🐵🎧",
        "Cordelius": "🍄🧠🌀", "Lumi": "💡🧝‍♀️🌌", "Doug": "💀👻🍔", "Clancy": "🦐🧨😠",
        "Willow": "🐸🧠🌀", "Jae-Yong": "🦾💿🎧", "Sam": "👊🧥⚡", "Pearl": "🔥🍳😄",
        "Mandy": "🍬💥👸", "Maisie": "🛡️📡🧠", "Bonny": "🧨💣🦜", "Hank": "🦀💪🔫", "Gus": "👻🧒🎈"
    },
    "impossible": {
        "Larry & Lawrie": "🕴️🤖🔫", "Shade": "🕶️🌀👤", "Charlie": "🪱🪄🧪", "Juju": "🦴👻🎭",
        "Lily": "🌸🗡️👘", "Angelo": "🏹🐟🌊", "Kenji": "🦾🗡️⚙️", "Draco": "🐉🔥⚔️",
        "Kaze": "🌪️🗡️😄", "Finx": "🦊🎭💥", "Kit": "🐱🎯😄", "Moe": "🎩💣🐀", "Meeple": "🎲🧠🌀"
    }
}

@bot.on_message(filters.command("brawlerquiz"))
async def brawler_quiz(client, message: Message):
    user_id = str(message.from_user.id)
    users.setdefault(user_id, {"points": 0})

    brawler = random.choice(brawlers)
    emojis = brawler["emojis"]
    name = brawler["name"].lower()
    difficulty = brawler["difficulty"]
    points = difficulty_levels[difficulty]["points"]

    msg = await message.reply_text(
        f"🧠 Rate den Brawler!\nSchwierigkeitsgrad: **{difficulty.upper()}**\nEmojis: {emojis}\n⏳ Du hast 5 Sekunden!"
    )

    try:
        response = await bot.listen(message.chat.id, timeout=5)
        if response.text.lower() == name:
            users[user_id]["points"] += points
            save_users(users)
            await response.reply_text(f"✅ Richtig! Du bekommst {points} Punkte.\n📊 Gesamtpunkte: {users[user_id]['points']}")
        else:
            await response.reply_text("❌ Falsch! Versuch es nochmal mit /brawlerquiz.")
    except asyncio.TimeoutError:
        await msg.delete()
        await message.reply_text("⌛ Zeit abgelaufen! 😢 Versuche es erneut mit /brawlerquiz.")

# Punkteabfrage
@bot.on_message(filters.command("mypoints"))
async def my_points(client, message: Message):
    user_id = str(message.from_user.id)
    points = users.get(user_id, {}).get("points", 0)
    await message.reply_text(f"📊 Deine Punkte: {points}")

bot.run()
