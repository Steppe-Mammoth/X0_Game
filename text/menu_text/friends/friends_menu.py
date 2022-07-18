class FriendsText:
    @staticmethod
    def add_friends():
        text = """
        <b>To add as a friend, do one of the options in the list:</b>
        
 * <i>send his contact</i>
 * <i>send me his forwarded message</i>
        
<b>Note</b>: <i>A friend will not be found if he has never sent <code>/start</code> to the bot_utils</i>
"""
        return text

    @staticmethod
    def fail_add_friend():
        text = """
        <b>The bot_utils did not find your friend</b>
<i>Make sure that the added user sent <code>/start</code> to the bot_utils</i>"""
        return text

    @staticmethod
    def added_friend(name: str):
        text = f'''
        <b>{name.upper()}
<u>Added successfully</u></b>
        
<i>Shared friends list updated</i>'''
        return text

    @staticmethod
    def get_error_format_msg():
        text = '''<b>Wrong message format</b>
        
Accepted only:
    <i>* Contact
    * Forwarded message</i>
    
Note: Send /<u>cancel</u> to cancel adding friends'''
        return text
