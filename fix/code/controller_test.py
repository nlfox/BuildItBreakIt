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
    controller.create_principal('bob', 'bob')
except RuntimeError as e:
    print e

print store

try:
    controller.end_transaction()
except RuntimeError as e:
    print e

print store

controller.begin_transaction('alice', 'alice')

controller.set('x', 'this')
controller.set('y', 'that')

controller.set_delegation('all', 'alice', 'read', 'bob')

controller.end_transaction()

controller.begin_transaction('bob', 'bob')

try:
    print controller.get_field('x')
except RuntimeError as e:
    print e

try:
    print controller.get_field('y')
except RuntimeError as e:
    print e

try:
    controller.set('x', 'other')
except RuntimeError as e:
    print e
