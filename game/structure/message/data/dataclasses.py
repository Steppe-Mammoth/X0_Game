from dataclasses import dataclass
from typing import Optional


@dataclass
class MessageInfo:
    chat_id: int
    message_id: int


@dataclass
class MessageVoteInfo(MessageInfo):
    choice: Optional[bool] = None
