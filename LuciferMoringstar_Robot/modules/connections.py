from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from LuciferMoringstar_Robot import ADMINS
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(bot, update):
    userid = update.from_user.id if update.from_user else None
    if not userid:
        return await update.reply_text(f" ππΎππ π°ππ΄ π°π½πΎπ½ππΌπΎππ π°π³πΌπΈπ½. /connect {update.chat.id} πΈπ½ πΏπΌ")
    chat_type = update.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        try:
            cmd, group_id = update.text.split(" ", 1)
        except:
            await update.reply_text("π΄π½ππ΄π πΈπ½ π²πΎπππ΄π²π π΅πΎππΌπ°π..!\n<code>/connect groupid</code>\nπΆπ΄π ππΎππ πΆππΎππΏ πΈπ³ π±π π°π³π³πΈπ½πΆ ππ·πΈπ π±πΎπ ππΎ ππΎππ πΆππΎππΏ π°πΌπ³ πππ΄ <code>/id</code>""", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = update.chat.id

    try:
        member = await bot.get_chat_member(group_id, userid)
        if (
                member.status != enums.ChatMemberStatus.ADMINISTRATOR
                and member.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await update.reply_text("ππΎπ ππ·πΎππ»π³ π±π΄ π°π½ π°π³πΌπΈπ½ πΈπ½ πΆπΈππ΄π½ πΆππΎππΏ..!", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await update.reply_text(f"{e}")
        await update.reply_text("πΈπ½ππ°π»πΈπ³ πΆππΎππΏ πΈπ³..!\n\n    πΈπ΅ π²πΎπππ΄π²π πΌπ°πΊπ΄ ππππ΄ πΈ'πΌ πΏππ΄ππ΄π½π πΈπ½ ππΎππ πΆππΎππΏ...!", quote=True)
        return
    try:
        st = await bot.get_chat_member(group_id, "me")
        if st.status == enums.ChatMemberStatus.ADMINISTRATOR:
            mrkyt = await bot.get_chat(group_id)
            title = mrkyt.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await update.reply_text(text=f"πππ²π²π΄πππ΅ππ»π»π π²πΎπ½π½π΄π²ππ΄π³ ππΎ **{title}**\n    π½πΎπ πΌπ°π½π°πΆπ΄ ππΎππ πΆππΎππΏ π΅ππΎπΌ πΌπ πΏπΌ..!", quote=True)
                
                if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    await bot.send_message(chat_id=userid, text=f"π²πΎπ½π½π΄π²ππ΄π³ ππΎ **{title}** !")
            else:
                await update.reply_text(text="ππΎπ'ππ΄ π°π»ππ΄π°π³π π²πΎπ½π½π΄π²ππ΄π³ ππΎ ππ·πΈπ π²π·π°π..!", quote=True)               
        else:
            await update.reply_text(text="π°π³π³ πΌπ΄ π°π π°π½ π°π³πΌπΈπ½ πΈπ½ πΆππΎππΏ..!", quote=True)
    except Exception as e:
        logger.exception(e)
        await update.reply_text(f"{e}")
        await update.reply_text('ππΎπΌπ΄ π΄πππΎπ πΎπ²π²ππππ΄π³..!\n   πππ π°πΆπ°πΈπ½ π»π°ππ΄π.', quote=True)
        return

@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def delete_connections_cmd(bot, update):
    
    if update.chat.type == enums.ChatType.PRIVATE:
        await update.reply_text("__Run /connections to view or disconnect from groups..!__", quote=True)
        return

    elif update.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = update.chat.id
        user_id = update.from_user.id
        st = await bot.get_chat_member(update.chat.id, update.from_user.id)
        if (st.status != enums.ChatMemberStatus.ADMINISTRATOR and st.status != enums.ChatMemberStatus.OWNER and update.from_user.id not in ADMINS):
            return

        delcon = await delete_connection(str(user_id), str(group_id))
        if delcon:
            await update.reply_text("__Successfully disconnected from this chat__")
        else:
            await update.reply_text("__This chat isn't connected to me!\nDo /connect to connect.__")


@Client.on_message(filters.private & filters.command("connections"))
async def all_connections_cmd(bot, update):

    userid = update.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        text = "__**There Are No Active Connections..! Connect To Some Groups First**__"
        await update.reply_text(text)
        return

    buttons = []
    for groupid in groupids:
        try:
            ttl = await bot.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            buttons.append( [ InlineKeyboardButton(f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}") ] )            
        except:
            pass

    if buttons:
        text = "**Your Connected Group Details :**\n\n"
        await update.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))        
    else:
        text = "__**There Are No Active Connections..! Connect To Some Groups First**__"
        await update.reply_text(text)
