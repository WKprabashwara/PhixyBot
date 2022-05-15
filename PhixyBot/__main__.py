import importlib
import time
import re
import random
from sys import argv
from typing import Optional
from pyrogram import filters, idle

from PhixyBot import (
    ALLOW_EXCL,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    pbot,
    updater,
)

from PhixyBot.modules import ALL_MODULES
from PhixyBot.modules.helper_funcs.chat_status import is_user_admin
from PhixyBot.modules.helper_funcs.misc import paginate_modules
from PhixyBot.modules.sudoers import bot_sys_stats
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

# ------------------------------------------- pm start text start--------------------------------------------------------------

PM_START_STICKER = "CAACAgUAAx0CZipN1gACCl1hsp4r1lqLvzonDG8lzU3qraOdPgACDQQAAjEpgFUr7pDqDvT2XSME"

PM_START_TEXT = """*Hello There 👋, I'm Phixy 🧚*\n\n*I can help manage your group with useful features, Feel free to add me to your group!📻 I'm made by @TeamPhixY 💸*\n\n*Hit* /help *to find my list of available commands 🔑*"""

buttons = [
    [
        InlineKeyboardButton(text="🔌 Commands Help", callback_data="help_back"),
    ],
    [
        InlineKeyboardButton(text="🧚 Info & About", callback_data="source_"),
        InlineKeyboardButton(text="💻 System Stats", callback_data="stats_callback"),
    ],
    [
        InlineKeyboardButton(text="💬 Support Channel", url=f"https://t.me/TeamPhixY"),
        InlineKeyboardButton(text="📻 Support Group", url=f"https://t.me/PhixYOfficial"),
    ],
    [
        InlineKeyboardButton(text="➕ Add Phixy to your Group ➕", url="t.me/PhixyBot?startgroup=true"),   
    ],
]

# ------------------------------------------- pm start text end--------------------------------------------------------------

# ------------------------------------------- Group start text start--------------------------------------------------------------
GROUP_START_TEXT = """*Heya : )  Phixy in here 🧚\n\nPM me if you have any questions how to use me!📻 I'm made by @TeamPhixY 💸\n\nHit /help to find my list of available commands 🔑*"""

gbuttons = [
        [
        InlineKeyboardButton(text="💻 System Stats", callback_data="stats_callback"),
    ],
]

#------------------------- Group start text end--------------------------------------------------------------

HELP_STRINGS = """
*Phixy's Main Commands :* [🧚](https://telegra.ph/file/6e4cea1a806d58563bd5f.jpg)

*〄* /start*: Starts me! You've probably already used this.*
*〄* /help*: Click this, I'll let you know about myself!*
*〄* /donate*: You can support my creater using this command.*
*〄* /settings*:*
    *〄 in PM: will send you your settings for all supported modules.*
    *〄 in a Group: will redirect you to pm, with all that chat's settings.*
"""

DONATE_STRING = """*💡Join Updates Channel @TeamPhixY | Support Group @PhixYOfficial*"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("PhixyBot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⇦ Back", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)
            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)
           
            else:
                update.effective_message.reply_sticker(
                    PM_START_STICKER,
                )    
        else:
            update.effective_message.reply_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_text(
            GROUP_START_TEXT,
            reply_markup=InlineKeyboardMarkup(gbuttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="⇦ Back", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


@run_async
def phixy_about_callback(update, context):
    query = update.callback_query
    if query.data == "phixy_":
        query.message.edit_text(
            text="""[ • ] My name is *Phixy*, I have been written with Pyrogram and Telethon.. I'm online since 10 June 2021 and is constantly updated!
*Bot Version: 3.0*
\n*Bot Developers:*
-  @dihanrandila
-  @InukaASiTH
\n* Updates Channel:* @SophiaUpdates
* Support Chat:* @SophiaSupport_Official
                 \n\n* And finally special thanks of gratitude to all my users who relied on me for managing their groups, I hope you will always like me; My developers are constantly working to improve me!
                 \n\n *Licensed under the GNU Affero General Public Lisence v3.0*
                 \n© 2020 - 2021 @SophiaSLBot. All Rights Reserved """,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="⇦ Back", callback_data="phixy_back")
                 ]
                ]
            ),
        )
        
    elif query.data == "phixy_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )

        

    elif query.data == "phixy_basichelp":
        query.message.edit_text(
            text=f"*[ • ] Here's basic Help regarding* *How to use Me?*"
            f"\n\n• Firstly Add {dispatcher.bot.first_name} to your group by pressing [here](http://t.me/{dispatcher.bot.username}?startgroup=true)\n"
            f"\n• After adding promote me manually with full rights for faster experience.\n"
            f"\n• Than send `/admincache@PhixyBot` in that chat to refresh admin list in My database.\n"
            f"\n\n*All done now use below given button's to know about use!*\n"
            f"",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="👮‍♂️ Admins", callback_data="phixy_admin"),
                    InlineKeyboardButton(text="📑 Notes", callback_data="phixy_notes"),
                 ],
                 [
                    InlineKeyboardButton(text="🛎 Support", callback_data="phixy_support"),
                    InlineKeyboardButton(text="💟 Credits", callback_data="phixy_credit"),
                 ],
                 [
                    InlineKeyboardButton(text="👑 Owner", callback_data="phixy_owner"),
                 ],
                 [
                    InlineKeyboardButton(text="⇦ Back", callback_data="source_"),
                 
                 ]
                ]
            ),
        )

    elif query.data == "phixy_admin":
        query.message.edit_text(
            text=f"*[ • ] Let's make your group bit effective now*"
            f"\nCongragulations, *Phixy* now ready to manage your group."
            f"\n\n*Admin Tools*"
            f"\nBasic Admin tools help you to protect and powerup your group."
            f"\nYou can ban members, Kick members, Promote someone as admin through commands of bot."
            f"\n\n*Welcome*"
            f"\nLets set a welcome message to welcome new users coming to your group."
            f"send `/setwelcome [message]` to set a welcome message!",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="⇦ Back", callback_data="phixy_basichelp")]]
            ),
        )

    elif query.data == "phixy_owner":
        query.message.edit_text(
            text=f"*[ • ] Owner | Developer of Phixy 🧚*",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                 [
                     [
                    InlineKeyboardButton(text="🗄 Logs", url="https://t.me/ImPrabashwara"),
                    InlineKeyboardButton(text="🌐 Website", url="https://rprabashwara.github.io/Prabashwara.github.io/"),
                 ],
                 [
                    InlineKeyboardButton(text="⇦ Back", callback_data="phixy_basichelp"),
                 ]
                 ]
            ),
        )
        
    elif query.data == "phixy_notes":
        query.message.edit_text(
            text=f"<b>[ • ] Setting up notes</b>"
            f"\nYou can save message/media/audio or anything as notes"
            f"\nto get a note simply use # at the beginning of a word"
            f"\n\nYou can also set buttons for notes and filters (refer help menu)",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="⇦ Back", callback_data="phixy_basichelp")]]
            ),
        )
        
    elif query.data == "phixy_support":
        query.message.edit_text(
            text="*[ • ] Phixy's Updates News & Supports*"
            "\nJoin Support Group & Updates Channel",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="📻 Support Group", url="https://t.me/PhixYOfficial"),
                    InlineKeyboardButton(text="💬 Support Channel", url="https://t.me/TeamPhixY"),
                 ],
                    InlineKeyboardButton(text="🗄 Logs", url="https://t.me/+QXqHhUmXdaoyNGY1"),
                 [
                    InlineKeyboardButton(text="⇦ Back", callback_data="phixy_basichelp"),
                 
                 ]
                ]
            ),
        )
        
    elif query.data == "phixy_credit":
        query.message.edit_text(
            text=f"<b>[ • ] Credit For Phixy's Devs</b>\n"
            f"\nHere Some Developers Helping in Making The Phixy Bot",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="👨‍💻 Developer", url="t.me/ImPrabashwara"),
                    InlineKeyboardButton(text="💟 Contributors", callback_data="contributors_"),
                 ],
                 [
                    InlineKeyboardButton(text="⇦ Back", callback_data="phixy_basichelp"),
                 
                 ]
                ]
            ),
        )


 
@pbot.on_callback_query(filters.regex("stats_callback"))
async def stats_callback(_, CallbackQuery):
    text = await bot_sys_stats()
    await pbot.answer_callback_query(CallbackQuery.id, text, show_alert=True)
        
@run_async
def Source_about_callback(update, context):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text="""*[ • ] Info & About* 
                 \n*Click buttons for help💡*""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="🧚 About Me", callback_data="phixy_"),
                    InlineKeyboardButton(text="❓Basic Help", callback_data="phixy_basichelp"),
                  ],
                  [
                    InlineKeyboardButton(text="💟 Special Credits", url=f"https://telegra.ph/Special-Credits-08-21"),
                    InlineKeyboardButton(text="📄 Terms And Conditions", url=f"https://telegra.ph/Terms-and-Conditions-08-21"),
                  ],
                  [
                    InlineKeyboardButton(text="📜 Source Code", url=f"https://github.com/WKRPrabashwara/Phixy"),
                 ],
                 [
                    InlineKeyboardButton(text="⇦ Back", callback_data="source_back")
                 ]
                ]
            ),
        )

    elif query.data == "source_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )

        # -------------------------------------------------------------------------- contributors --------------------------------------------------------------
        
        
@pbot.on_callback_query(filters.regex("stats_callback"))
async def stats_callback(_, CallbackQuery):
    text = await bot_sys_stats()
    await pbot.answer_callback_query(CallbackQuery.id, text, show_alert=True)
        
@run_async
def Contributors_about_callback(update, context):
    query = update.callback_query
    if query.data == "contributors_":
        query.message.edit_text(
            text="""*[ • ] Info & About* 
                 \n*Click buttons for help💡*""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="🧚 About Me", callback_data="phixy_"),
                    InlineKeyboardButton(text="❓Basic Help", callback_data="phixy_basichelp"),
                  ],
                  [
                    InlineKeyboardButton(text="💟 Special Credits", url=f"https://telegra.ph/Special-Credits-08-21"),
                    InlineKeyboardButton(text="📄 Terms And Conditions", url=f"https://telegra.ph/Terms-and-Conditions-08-21"),
                  ],
                  [
                    InlineKeyboardButton(text="📜 Source Code", url=f"https://github.com/WKRPrabashwara/Phixy"),
                 ],
                 [
                    InlineKeyboardButton(text="⇦ Back", callback_data="contributors_back")
                 ]
                ]
            ),
        )

    elif query.data == "contributors_back":
        query.message.edit_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )
        
@run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton( text="Help", url="t.me/{}?start=ghelp_{}".format(context.bot.username, module),)
                        ],
                        [
                            InlineKeyboardButton( text="🛎 Team Phixy", url="https://t.me/TeamPhixY"),
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "Contact me in PM to get the list of possible commands.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton( text="Help", url="t.me/{}?start=help".format(context.bot.username),
                                            )
                    ],
                    [
                        InlineKeyboardButton( text="🛎 Team Phixy", url="https://t.me/TeamPhixY"),
                    ]
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="⇦ Back", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="⇦ Back",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what"
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what"
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what"
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this Phixy's chat's settings, as well as yours 🧚"
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                        InlineKeyboardButton(text="💻 System Stats", callback_data="stats_callback"),
                        ],
                        [
                        InlineKeyboardButton( text="⚙ Settings", url="t.me/{}?start=stngs_{}".format(context.bot.username, chat.id),)
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings ⚙"

    else:
        send_settings(chat.id, user.id, True)


@run_async
def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 254318997 and DONATION_LINK:
            update.effective_message.reply_text(
                "You can also donate to the person currently running me."
                "[Here]({})".format(DONATION_LINK),
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "I've PM'ed you about donating to my creator!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "Contact me in PM first to get donation information."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", "\n╭━━╮╱╱╱╭╮╱╭━━━╮╭╮╱╱╱╱╱╭╮╱╱╱╱╱╭╮\n┃╭╮┃╱╱╭╯╰╮┃╭━╮┣╯╰╮╱╱╱╭╯╰╮╱╱╱╱┃┃\n┃╰╯╰┳━┻╮╭╯┃╰━━╋╮╭╋━━┳┻╮╭╋━━┳━╯┃\n┃╭━╮┃╭╮┃┃╱╰━━╮┃┃┃┃╭╮┃╭┫┃┃┃━┫╭╮┃\n┃╰━╯┃╰╯┃╰╮┃╰━╯┃┃╰┫╭╮┃┃┃╰┫┃━┫╰╯┃\n╰━━━┻━━┻━╯╰━━━╯╰━┻╯╰┻╯╰━┻━━┻━━╯\n\nI'm Online Now! 🧚💫 | @TeamPhixY")
        except Unauthorized:
            LOGGER.warning(
                """ 
            
╭━━╮╱╱╱╭╮╱╭━━━╮╭╮╱╱╱╱╱╭╮╱╱╱╱╱╭╮
┃╭╮┃╱╱╭╯╰╮┃╭━╮┣╯╰╮╱╱╱╭╯╰╮╱╱╱╱┃┃
┃╰╯╰┳━┻╮╭╯┃╰━━╋╮╭╋━━┳┻╮╭╋━━┳━╯┃
┃╭━╮┃╭╮┃┃╱╰━━╮┃┃┃┃╭╮┃╭┫┃┃┃━┫╭╮┃
┃╰━╯┃╰╯┃╰╮┃╰━╯┃┃╰┫╭╮┃┃┃╰┫┃━┫╰╯┃
╰━━━┻━━┻━╯╰━━━╯╰━┻╯╰┻╯╰━┻━━┻━━╯

- #Independent_Developers

- All Copyright©️ goes to Pʀᴀʙᴀsʜᴡᴀʀᴀ 🇱🇰 #Aғᴋ """
                          )
        except BadRequest as e:
            LOGGER.warning(e.message)

    test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(phixy_about_callback, pattern=r"phixy_")
    source_callback_handler = CallbackQueryHandler(Source_about_callback, pattern=r"source_")
    contributors_callback_handler = CallbackQueryHandler(Contributors_about_callback, pattern=r"contributors_")

    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(source_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
