from typing import Optional

from game.structure.fields.data.dataclasses import TInfo
from game.structure.others.technical import XOTechnic
from game.structure.fields.utils.technical import TableBase

from logger import logger


class TableInfo:
    def __init__(self):
        self.table: Optional[list] = None
        self.unique_id: Optional[str] = None
        self.count_steps: Optional[int] = None

    def new_table_initialization(self):
        self._reset_table()
        self._reset_unique_id()
        self.count_steps = 1
        logger.info('initialization [game_text fields] - DONE'.upper())

    def _reset_unique_id(self):
        unique_id = XOTechnic.get_unique_id()
        self.unique_id = unique_id

    def _reset_table(self):
        clear_table = TableBase.get_clear_table()
        self.table = clear_table

    def edit_table(self, index: int, symbol: str):
        self.table[index] = symbol
        self.count_steps += 1
        logger.info(f'ТАБЛИЦА ИЗМЕНЕННА: {symbol} -> {index}')

    def get_table_info(self) -> TInfo:
        return TInfo(table=self.table, unique_id=self.unique_id)
