import Server from server
import Parser from parser
import Interpreter from interpreter
import Store from store

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
