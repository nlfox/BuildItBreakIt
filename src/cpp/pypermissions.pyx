from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "permissions.h" namespace "bibifi":
    cdef cppclass SecurityState:
        SecurityState() except +
        void beginTransaction()
        void completeTransaction()
        void discardTransaction()
        void addUser(string)
        void own(string, string)
        void setDefault(string)
        void setDelegation(string, string, string, string)
        void deleteDelegation(string, string, string, string)
        bool hasPermission(string, string, string)


cdef class PySecurityState:
    cdef SecurityState S

    def __cinit__(self):
        self.S = SecurityState()

    def begin_transaction(self):
        self.S.beginTransaction()

    def complete_transaction(self):
        self.S.completeTransaction()

    def discard_transaction(self):
        self.S.discardTransaction()

    def add_user(self, str user):
        self.S.addUser(user)

    def set_default(self, str default):
        self.S.setDefault(default)

    def set_delegation(self, str field, str authority, str permission, str user):
        self.S.setDelegation(field, authority, permission, user)

    def delete_delegation(self, str field, str authority, str permission, str user):
        self.S.deleteDelegation(field, authority, permission, user)

    def has_permission(self, str user, str field, str permission):
        return self.S.hasPermission(user, field, permission)
