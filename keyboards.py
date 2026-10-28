from pyrogram.types import KeyboardButton
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import emoji

btn_info =  KeyboardButton(f'{emoji.INFORMATION} Info')
btn_games = KeyboardButton(f'{emoji.VIDEO_GAME} Games')
btn_profile = KeyboardButton(f'{emoji.PERSON} Profile')
btn_rps = KeyboardButton(f'{emoji.PLAY_BUTTON} Rock Paper Scissors')
btn_quest = KeyboardButton(f'{emoji.CITYSCAPE_AT_DUSK} Quest')
btn_back = KeyboardButton(f'{emoji.BACK_ARROW} Back')
btn_time = KeyboardButton(f'{emoji.TIMER_CLOCK} Time')
btn_rock = KeyboardButton(f'{emoji.ROCK} Rock')
btn_scissors = KeyboardButton(f'{emoji.SCISSORS} Scissors')
btn_paper = KeyboardButton(f'{emoji.NOTEBOOK} Paper')
btn_generate_image = KeyboardButton(f'{emoji.FRAMED_PICTURE} Generate Picture')
btn_rating = KeyboardButton(f'{emoji.GLOBE_WITH_MERIDIANS} World Rating')
btn_free_coins = KeyboardButton(f'{emoji.COIN} Free Coins!!!')

inline_kb_start_quest = InlineKeyboardMarkup([
    [InlineKeyboardButton('go through quest', callback_data='start_quest')] ])
inline_kb_choice_door = InlineKeyboardMarkup([
    [InlineKeyboardButton("🚪⬅️  Left door", callback_data='left_door')],
    [InlineKeyboardButton("🚪➡️  Right door", callback_data='right_door')]
    ])
inline_kb_left_door = InlineKeyboardMarkup([
    [InlineKeyboardButton("🗡️ Fight the dragon", callback_data='dragon')],
    [InlineKeyboardButton("🏃‍♂️ Trying to escape", callback_data='escape')]
])

inline_kb_right_door = InlineKeyboardMarkup([
    [InlineKeyboardButton("👑 golden crown", callback_data='gold_crown')],
    [InlineKeyboardButton("🗡️ Silver dagger", callback_data='silver_dagger')],
    [InlineKeyboardButton("📜 Old book", callback_data='old_book')]
])
kb_games = ReplyKeyboardMarkup (
    keyboard=[
        [btn_rps],
        [btn_quest, btn_back]

    ], resize_keyboard=True
)

kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [btn_info, btn_games, btn_time, btn_generate_image,],
        [btn_rating, btn_profile, btn_free_coins]
    ],
    resize_keyboard=True
)
kb_rps = ReplyKeyboardMarkup (
    keyboard=[
        [btn_rock, btn_scissors, btn_paper]
    ],
    resize_keyboard=True
)