from text.utils.emoji import GetEmoji


def get_symbols_line_text():
    emoji = GetEmoji.replay_symbols(11)
    line = "|".join(emoji)
    return line
