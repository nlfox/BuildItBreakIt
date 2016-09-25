from store import Store

store = Store()

store.begin_transaction()

print store

store.modify_principal("admin", "password")

print store

store.set_field('x', {'f1': "this", "f2": "that"})

print store

print store.field_type('x')
print store.field_type('x.f1')
print store.field_exists('x.f3')
print store.field_exists('x.f1')

store.set_local('y', "hello")

print store

print store.field_exists('y')
print store.field_type('y')
print store.get_field('x.f2')
print store.get_field('y')

store.complete_transaction()

print store

