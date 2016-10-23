from permissions import *

S = SecurityState()

S.add_user("alice")
S.add_user("bob")

S.set_delegation("x", "admin", "delegate", "alice")
S.set_delegation("x", "alice", "read", "bob")

print S.has_permission("alice", "x", "read")
print S.has_permission("bob", "x", "read")

S.set_delegation("x", "admin", "read", "alice")

print S.has_permission("alice", "x", "read")
print S.has_permission("bob", "x", "read")

S.delete_delegation("x", "alice", "read", "bob")

print S.has_permission("bob", "x", "read")

S.set_delegation("all", "admin", "read", "anyone")

print S.has_permission("bob", "y", "read")
