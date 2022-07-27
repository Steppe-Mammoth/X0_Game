from typing import NamedTuple


class ExpandableMessage(NamedTuple):
    short: str
    full: str


class FriendsText:
    @staticmethod
    def add_friends(my_id: int, bot_username: str) -> ExpandableMessage:
        link = f"https://t.me/{bot_username}?start={my_id}_add_friend"

        base_method_text = f"""
<b>To add as a friend:</b>
* <b>1</b>) <i>Send your friend an invitation link:</i> \n
<b>-></b> <code>{link}</code>"""

        more_methods_text = f"""\n\n    <i>{'*' * 15} OR {'*' * 15}</i>\n
    ** <b>2</b>) <i>Send me a friend's contact</i>
    ** <b>3</b>) <i>Send me a friend's forwarded message</i>\n
<b>Note</b>: <i>For 2 and 3 steps - Your friend must at least once send <code>/start</code> to the bot</i>
 """
        full_methods_text = base_method_text + more_methods_text
        return ExpandableMessage(short=base_method_text, full=full_methods_text)

    @staticmethod
    def fail_add_friend():
        text = """
        <b>The Bot does not have access to your friend</b>\n
<i>Ask a friend to send <code>/start</code> to the bot
Or send him an <u>invitation link</u></i> 📬"""
        return text

    @staticmethod
    def already_friends(friend_name: str) -> str:
        text = f"<i><b>{friend_name}</b>: 🫂\n👉 <u>Is already your friend</u></i>"
        return text

    @staticmethod
    def notify_me_add_friend(friend_name: str) -> str:
        text = f'<i><b>👤 {friend_name} added</b></i>\n <i>You friends list is refreshed 🫂</i>'
        return text

    @staticmethod
    def notify_friend_add_friend(friend_name: str) -> str:
        text = f'<i><b>You have been added as a friend 🫂\n 👤 {friend_name}</b></i>'
        return text

    @staticmethod
    def get_error_format_msg() -> str:
        text = '''<b>Wrong message format</b>\n🔽<i>Choose one of the supported methods</i>🔽'''
        return text

    @staticmethod
    def error_added() -> str:
        text = '<b><i>ERROR. UNABLE TO ADD FRIEND</i></b>'
        return text
