from pyrogram import Client, filters
from pyrogram.filters import reply
from pyrogram.types import ForceReply
import config
import base64
import keyboards
import random
import json
from datetime import datetime
from FusionBrain_AI import generate
import pyrogram

API_ID = 24001007
API_HASH = '8f3683b35b54c68d54ff5cff3f2bfcbc'
BOT_TOKEN = '7862997935:AAHwFLqqmMlLzHqP3oiYUvd0fqeI9KpB_lQ'


API_KEY = '025AF61E679527268E0721459F8F2712'
SECRET_KEY = 'C2DEA56133763B0D3C1A6D6991F0A369'

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="MaxVirtualHelper_bot"
)
def button_filter(button):
    async def func(_, __, msg):
        return msg.text == button.text
    return filters.create(func, "ButtonFilter", button=button)


@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("Welcome!", reply_markup=keyboards.kb_main)

    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = 0

    with open("users.json", "w") as file:
        json.dump(users, file)

@bot.on_message(filters.command("Info") | button_filter(keyboards.btn_info))
async def info(bot, message):
    await message.reply("Hello! Here is the description what this bot can do")

@bot.on_message(filters.command("games") | button_filter(keyboards.btn_games))
async def games(bot, message):
    await message.reply("select the game", reply_markup=keyboards.kb_games)

@bot.on_message(filters.command("back") | button_filter(keyboards.btn_back))
async def back(bot, message):
    await message.reply("Back to Menu", reply_markup=keyboards.kb_main)

@bot.on_message(filters.command("time") | button_filter(keyboards.btn_time))
async def time(bot, message):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    await message.reply(f'Actually Time: {current_time}')

@bot.on_message(filters.command("game") | button_filter(keyboards.btn_rps))
async def game(bot, message):
    with open("users.json", "r") as file:
        users = json.load(file)
    if users[str(message.from_user.id)] >= 10:
        await message.reply("Your Way", reply_markup=keyboards.kb_rps)
    else:
        await message.reply(f"Not enough funds. On your Profile are: {users[str(message.from_user.id)]}. Minimum amount for the game is 10")

@bot.on_message(button_filter(keyboards.btn_rock) |
                button_filter(keyboards.btn_scissors) |
                button_filter(keyboards.btn_paper) )
async def choice_rps(bot,message):
    with open ("users.json", "r") as file:
        users = json.load(file)

    rock = keyboards.btn_rock.text
    scissors = keyboards.btn_scissors.text
    paper = keyboards.btn_paper.text
    user = message.text
    pc = random.choice([rock, scissors, paper])

    if user == pc:
        await message.reply("draw")
    elif (user == rock and pc == scissors) or (user == scissors and pc == paper) or (user == paper and pc == rock):
        await message.reply(f"You Won. Bot choice {pc}, you get 1 Coin",
                            reply_markup=keyboards.kb_games)
        users[str(message.from_user.id)] += 1
    else:
        await message.reply(f"You lose. Bot choice {pc}, you lose 1 Coin",
                            reply_markup = keyboards.kb_games)
        users[str(message.from_user.id)] -= 1

    with open("users.json", "w") as file:
        json.dump(users, file)

@bot.on_message(filters.command("313091"))  # Du kannst "geheim123" durch jedes geheime Wort ersetzen
async def coins\
               (bot, message):
    with open("users.json", "r") as file:
        users = json.load(file)

    user_id = str(message.from_user.id)
    if user_id in users:
        users[user_id] += 1
        with open("users.json", "w") as file:
            json.dump(users, file)
        await message.reply("Du hast 1 Coin bekommen!")
    else:
        await message.reply("Du musst zuerst /start benutzen.")

@bot.on_message(filters.command("image"))
async def image(bot, message):
    if len(message.text.split()) > 1:
        query = message.text.replace('/image', '')
        await message.reply_text(f"I generate you by your message '{query}', wait for a few...")
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1,99)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'images/image{img_num}.jpg', reply_to_message_id = message.id)
        else:
            await message.reply_text("An mistake try again", reply_to_message_id = message.id)
    else:
        await message.reply_text("Enter your Question")

query_text = "Enter a question to generate an picture"
@bot.on_message(button_filter(keyboards.btn_generate_image))
async def image_command(bot, message):
    await message.reply("Say anything you want to generate", reply_markup=ForceReply(True))

@bot.on_message(filters.reply)
async def reply(bot, message):
    #if message.reply_to_message.text == query_text:
        query = message.text
        await message.reply_text(f"I generate you by your message **{query}**. wait for a few...")
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'images/image{img_num}.jpg', reply_to_message_id=message.id)
        else:
            await message.reply_text("An mistake try again", reply_to_message_id=message.id)

@bot.on_message(filters.command("quest") | button_filter(keyboards.btn_quest))
async def quest(bot, message):
    await message.reply_text("Do you want to embark on an exciting journey full of adventure and mysteries?",
                             reply_markup=keyboards.inline_kb_start_quest)

@bot.on_message(filters.command("profile") | button_filter(keyboards.btn_profile))
async def profile(bot, message):
    with open("users.json", "r") as file:
        users = json.load(file)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>ID:</b> {message.from_user.id}\n<b>Coins:</b> {users[str(message.from_user.id)]}\n"
    )


@bot.on_message(filters.command("ranking") | button_filter(keyboards.btn_rating))
async def world_rating(bot, message):
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        await message.reply("❌ Keine Benutzerdaten gefunden.")
        return

    # Umwandlung in Liste von Spielern mit id + Coins
    players = [{"id": uid, "Coins": coins} for uid, coins in users.items()]

    # Sortieren nach Coins
    sorted_players = sorted(players, key=lambda x: x["Coins"], reverse=True)

    # Ranking-Text erstellen
    text = "<b>🌍 Global Rank:</b>\n"
    for i, player in enumerate(sorted_players[:20], start=1):
        text += f"{i}. ID: <code>{player['id']}</code> – 💰 {player['Coins']} Coins\n"

    # Eigene Position finden
    user_id = str(message.from_user.id)
    for position, player in enumerate(sorted_players, start=1):
        if player["id"] == user_id:
            text += f"\n🏅 You are on Place <b>{position}</b>"
            break

    await message.reply(text)

@bot.on_callback_query()
async def handle_query(bot, query):
    #await query.message.delete()
    if query.data == 'start_quest':
        await bot.answer_callback_query(query.id,
             text ="Welcome to our quest called 'Find the Treasure'!",
             show_alert=True)
        await query.message.reply_text("You are standing between two doors. Which do you choose?",
                      reply_markup=keyboards.inline_kb_choice_door)
    elif query.data == 'left_door':
        await query.message.reply_text("You enter the room and see an evil dragon! You have two options to choose from.",
                                       reply_markup=keyboards.inline_kb_left_door)
    elif query.data == 'right_door':
        await query.message.reply_text("You're in a room full of treasures! You can only choose one treasure.",
                                       reply_markup=keyboards.inline_kb_right_door)
    elif query.data == 'dragon':
        await bot.answer_callback_query(query.id, text="You fight the dragon, but it is too strong. You die.",
                                        show_alert=True)
    elif query.data == 'run':
        await bot.answer_callback_query(query.id,
                                        text="You try to escape, but the dragon catches up with you and eats you.",
                                        show_alert=True)
    elif query.data == 'gold_crown':
        await bot.answer_callback_query(query.id,
                                        text="You take the golden crown and leave the room. Congratulations! You have won the game.",
                                        show_alert=True)
    elif query.data == 'silver_dagger':
        await bot.answer_callback_query(query.id,
                                        text="You You take the silver dagger and leave the room. Unfortunately, the dagger is worthless.",
                                        show_alert=True)
    elif query.data == 'old_book':
        await bot.answer_callback_query(query.id,
                                        text="You take the old book and leave the room. The book turns out to be magical! You open a page and disappear.",
                                        show_alert=True)


bot.run()