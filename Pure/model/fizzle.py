#  fizzle.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from typing import final
__all__ = ['Fizzle', 'FileFizzle', 'WebFizzle', 'DBFizzle']


class Fizzle(Exception):
    def __init__(self, msg="An unknown error has occurred.", code=0xFF):
        self.code = code
        self.msg = msg


@final
class FileFizzle(Fizzle):
    def __init__(self, msg="HTTP Error"):
        super().__init__(msg, 0b_1000_0000)

    @classmethod
    def not_found(cls):
        return cls("Oops! The file was not found.")


@final
class DBFizzle(Fizzle):
    def __init__(self, msg="DB Error"):
        super().__init__(msg, 0b_0100_0000)

    @classmethod
    def operation_error(cls):
        return cls("Database operation failed")

    @classmethod
    def db_fail(cls):
        return cls("Database is damaged")


@final
class WebFizzle(Fizzle):
    def __init__(self, msg="Web Error"):
        super().__init__(msg, 0b_0010_0000)

    @classmethod
    def connection_error(cls):
        return cls("Cannot connect to server.")

    @classmethod
    def server_fail(cls):
        return cls("Server is not responding.")

