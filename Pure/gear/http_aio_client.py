#  http_aio_client.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import aiohttp


# 기본값 100 커넥션이다. 이 정도면 차고 넘친다.
# 런루프 종료 시에는 반드시 닫아줘야 한다.
# https://docs.aiohttp.org/en/stable/client_advanced.html
class HttpAioClient:
    SESSION: aiohttp.ClientSession | None = None

    @staticmethod
    def __bootup__():
        if not HttpAioClient.SESSION or HttpAioClient.SESSION.closed:
            HttpAioClient.SESSION = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    @staticmethod
    async def __shutdown__():
        if HttpAioClient.SESSION and not HttpAioClient.SESSION.closed:
            await HttpAioClient.SESSION.close()
