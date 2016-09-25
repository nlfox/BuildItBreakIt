from store import Store
from controller import Controller

store = Store()
controller = Controller(store, None)

store.users = {'admin': 'admin'}

try:
    controller.begin_transaction('admin', 'password')
except RuntimeError as e:
    print e

try:
    controller.begin_transaction('admin', 'admin')
except RuntimeError as e:
    print e

try:
    controller.create_principal('alice', 'alice')
except RuntimeError as e:
    print e

print store

try:
    controller.end_transaction()
except RuntimeError as e:
    print e

print store
