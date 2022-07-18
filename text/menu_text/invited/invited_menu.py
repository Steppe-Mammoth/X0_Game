from text.utils.emoji import GetEmoji


class InviteText:
    @staticmethod
    def notification_invitation(name: str, count_rounds: int):
        people = GetEmoji.people(1)
        envelope = GetEmoji.envelope(11)
        sport = GetEmoji.sport(11)

        text = f'''
    {' '.join(envelope)}
        
* <b>{name.upper()}</b> {people[0]}:
    ** <i><b>Invites you to play</b>
    *** <b>{count_rounds}</b> <u>round game</u></i>

{' '.join(sport)}
'''
        return text

    @staticmethod
    def about_canceling_invitation(name: str):
        people = GetEmoji.people(1)
        envelope = GetEmoji.envelope(11)

        text = f"""
    <i>{name.upper()} {people[0]}
<b>Canceled your invitation to play</b></i>

{' '.join(envelope)}"""
        return text

    @staticmethod
    def sender_invitation():
        people = GetEmoji.people(1)
        text = f'''
    <i>An <b>invitation has been sent</b> to the <b>player</b></i> {people[0]}
    
<i>He has <b><u>45 seconds</u> to accept</b></i>'''
        return text

    @staticmethod
    def watch_wait_time(seconds: int):
        text = f"""
You have already sent an invitation
Wait until it expires

    ** Left: 00:00:{seconds} seconds"""
        return text
