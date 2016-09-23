import Server
import Parser
import Interpreter
import Store

hostname = "localhost"
port = -1

server = Server()
parser = Parser()
interpreter = Interpreter()
store = Store()

store.init()
interpreter.init(store, server)
parser.init(server)
server.init(hostname, port)
