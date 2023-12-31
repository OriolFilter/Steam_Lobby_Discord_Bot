from aiohttp import web
from Classes import HealthCheckConf

from CustomBot import CustomBot


class HealthcheckHandler:
    __discord_bot: CustomBot
    __configuration: HealthCheckConf

    def __init__(self, configuration, discord_bot):
        self.__configuration: HealthCheckConf = configuration
        self.__discord_bot: CustomBot = discord_bot

    @property
    def is_bot_connected(self) -> bool:
        return self.__discord_bot.is_connected

    async def handle_healthcheck(self, request):
        status_code = [503, 200][self.is_bot_connected]
        data = {'status_code': status_code}
        return web.json_response(data, status=status_code)

    @property
    def configuration(self):
        return self.__configuration

    async def start_web(self):
        app = web.Application()
        app.add_routes([web.get('/healthz', self.handle_healthcheck)])
        runner = web.AppRunner(app)
        await runner.setup()
        webserver = web.TCPSite(runner, port=self.configuration.port)
        await webserver.start()
