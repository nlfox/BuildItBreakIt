#include "permissions.h"

#include <string>
#include <queue>
#include <map>
#include <set>

using namespace std;

namespace bibifi {
  Delegation::Delegation(string f, string a, string p, string u) :
    field(f),
    authority(a),
    permission(p),
    user(u) {}

  string Delegation::getString() const {
    return field + authority + permission + user;
  }

  bool Delegation::operator ==(const Delegation &other) const {
    return field == other.field && authority == other.authority && permission == other.permission && user == other.user;
  }

  bool Delegation::operator <(const Delegation &other) const {
    return getString() < other.getString();
  }

  bool Delegation::operator >(const Delegation &other) const {
    return getString() > other.getString();
  }
  
  SecurityState::SecurityState() :
    delegations(),
    defaultDel("anyone"),
    identifiers(),
    delegationsPatch(),
    defaultPatch(""),
    identifiersPatch() {}

  void SecurityState::beginTransaction() {
    defaultPatch = defaultDel;
    identifiersPatch.clear();
  }

  void SecurityState::completeTransaction() {
    delegations.clear();
    delegations = delegationsPatch;
    defaultDel = defaultPatch;
    for (set<string>::iterator i = identifiersPatch.begin(); i != identifiersPatch.end(); i++) {
      identifiers.insert(*i);
    }
    identifiersPatch.clear();
  }

  void SecurityState::discardTransaction() {
    delegationsPatch = delegations;
    identifiersPatch.clear();
  }

  void SecurityState::addUser(string user) {
    if (delegations.find(user) == delegations.end() && delegationsPatch.find(user) == delegationsPatch.end()) {
      delegationsPatch[user] = set<Delegation>();
      for (int i = 0; i < 4; i++) {
	delegationsPatch[user].insert(Delegation("all", defaultPatch, permissions[i], user));
      }
    }
  }

  void SecurityState::own(string user, string field) {
    if (identifiers.find(field) == identifiers.end() && identifiersPatch.find(field) == identifiersPatch.end()) {
      identifiersPatch.insert(field);
    }

    for (int i = 0; i < 4; i++) {
      setDelegation(field, "", permissions[i], user);
    }
  }

  void SecurityState::setDefault(string user) {
    defaultPatch = user;
  }

  void SecurityState::setDelegation(string field, string authority, string permission, string user) {
    if (field == "all") {
      for (set<string>::iterator i = identifiers.begin(); i != identifiers.end(); i++) {
	if (hasPermission(authority, *i, "delegate")) {
	  setDelegation(*i, authority, permission, user);
	}
      }

      for (set<string>::iterator i = identifiersPatch.begin(); i != identifiersPatch.end(); i++) {
	if (hasPermission(authority, *i, "delegate")) {
	  setDelegation(*i, authority, permission, user);
	}
      }
    } else {
      delegationsPatch[user].insert(Delegation(field, authority, permission, user));
    }
  }

  void SecurityState::deleteDelegation(string field, string authority, string permission, string user) {
    if (field == "all") {
      for (set<string>::iterator i = identifiers.begin(); i != identifiers.end(); i++) {
	if (hasPermission(authority, *i, "delegate")) {
	  deleteDelegation(*i, authority, permission, user);
	}
      }

      for (set<string>::iterator i = identifiersPatch.begin(); i != identifiersPatch.end(); i++) {
	if (hasPermission(authority, *i, "delegate")) {
	  deleteDelegation(*i, authority, permission, user);
	}
      }
    } else {
      Delegation d (field, authority, permission, user);
      if (delegationsPatch[user].find(d) != delegationsPatch[user].end()) {
	delegationsPatch[user].erase(d);
      }
    }
  }

  bool SecurityState::hasPermission(string user, string field, string permission) {
    if (user == "admin") return true;
    
    queue<Delegation> tbs;
    for (set<Delegation>::iterator i = delegationsPatch[user].begin(); i != delegationsPatch[user].end(); i++) {
      if (((*i).field == field || (*i).field == "all") && (*i).permission == permission) {
	tbs.push(*i);
      }
    }
    
    for (set<Delegation>::iterator i = delegationsPatch["anyone"].begin(); i != delegationsPatch["anyone"].end(); i++) {
      if (((*i).field == field || (*i).field == "all") && (*i).permission == permission) {
	tbs.push(*i);
      }
    }

    bool foundPermission = false;
    while (!tbs.empty()) {
      Delegation d = tbs.front();
      tbs.pop();
      if (d.authority == "admin" || d.authority == "") {
	foundPermission = true;
	break;
      }

      for (set<Delegation>::iterator i = delegationsPatch[d.authority].begin(); i != delegationsPatch[d.authority].end(); i++) {
	if (((*i).field == field || (*i).field == "all") && (*i).permission == permission) {
	  tbs.push(*i);
	}
      }
    }

    return foundPermission;
  }
};
