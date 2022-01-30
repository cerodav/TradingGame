from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from monie.logger.logger import logger
from monie.util.envUtil import EnvUtil
from monie.util.configUtil import ConfigUtil
from monie.service.handler.gameRoomHandler import GameRoomHandler

define('port', default=ConfigUtil().getConfig(['service', 'port']), help='Port to listen on')

app = Application([
    ('/api/tradergame/([^/]+)', GameRoomHandler),
])

http_server = HTTPServer(app)
http_server.listen(options.port)
logger.info('[{}] Dashboard service listening on http://localhost:{}'.format(EnvUtil.getEnv().upper(), options.port))
IOLoop.current().start()
