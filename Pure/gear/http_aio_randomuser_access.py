#  http_aio_randomuser_access.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from typing import NamedTuple
import aiohttp
from gear.http_aio_client import HttpAioClient

_BASE_URL = "https://randomuser.me/api/"


class HttpAioRandomuserAccess(HttpAioClient):
    async def get_all_user(self, count=100) -> list['WEB.User'] | None:
        async with self.SESSION.get(_BASE_URL, params={"results": count}) as resp:
            if 200 <= resp.status < 300:
                json = await resp.json()
                return [WEB.User.new(d) for d in json['results']]
            return None

    async def get_picture(self, url) -> bytes:
        url = _BASE_URL + url
        async with self.SESSION.get(url) as resp:
            if 200 <= resp.status < 300:
                if resp.headers['Content-Type'] != 'image/jpeg':
                    raise aiohttp.ClientError("Not JPG")
                return await resp.read()


class WEB:
    class User(NamedTuple):
        gender: str
        name: 'WEB.Name'
        email: str
        login: 'WEB.Login'
        dob: 'WEB.Dob'
        cell: str
        picture: 'WEB.Picture'
        nat: str

        @staticmethod
        def new(data: dict) -> 'WEB.User':
            return WEB.User(
                gender=data['gender'],
                name=WEB.Name.new(data['name']),
                email=data['email'],
                login=WEB.Login.new(data['login']),
                dob=WEB.Dob.new(data['dob']),
                cell=data['cell'],
                picture=WEB.Picture.new(data['picture']),
                nat=data['nat']
            )

    class Name(NamedTuple):
        first: str
        last: str

        @staticmethod
        def new(data: dict) -> 'WEB.Name':
            return WEB.Name(
                first=data['first'],
                last=data['last']
            )

    class Login(NamedTuple):
        uuid: str
        username: str

        @staticmethod
        def new(data: dict) -> 'WEB.Login':
            return WEB.Login(
                uuid=data['uuid'],
                username=data['username']
            )

    class Dob(NamedTuple):
        date: str
        age: int

        @staticmethod
        def new(data: dict) -> 'WEB.Dob':
            return WEB.Dob(
                date=data['date'],
                age=data['age']
            )

    class Picture(NamedTuple):
        large: str

        @staticmethod
        def new(data: dict) -> 'WEB.Picture':
            return WEB.Picture(
                large=data['large'].replace(_BASE_URL, "")
            )
