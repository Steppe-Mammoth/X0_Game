from text.utils.emoji import GetEmoji


class MenuText:

    @staticmethod
    def start_menu(name_user: str):
        emoji = GetEmoji.smile(2)

        text = f"""
    {emoji[0]} <b>Welcome {name_user}</b> {emoji[1]}
        <i>CHOICE MODE</i>"""
        return text

    @staticmethod
    def select_opponent():
        emoji = GetEmoji.silent(11)
        text = f"<i>* LIST OF <b>YOUR OPPONENTS</b></i>\n" \
               f"{' '.join(emoji)}"
        return text

    @staticmethod
    def select_rounds():
        emoji = GetEmoji.sport(11)
        text = f"<b>How many <u><i>ROUNDS</i></u> do you choose</b> \n" \
               f"<i>For a <b><u>DUEL</u></b>:</i>\n" \
               f"{' '.join(emoji)}"
        return text

    @staticmethod
    def show_game_description(opponent_name: str, count_rounds: int):
        crayfish = GetEmoji.crayfish(1)
        fight = GetEmoji.duel_fight(1)
        envelope = GetEmoji.envelope(2)

        text = f"""
    <i>* Your rival:</i> <b>{opponent_name}</b> {crayfish[0]}
    <i>** Game for</i> <b>{count_rounds} games</b> {fight[0]}

{envelope[0]} <i>Send an invite to a game?</i> {envelope[1]}"""
        return text