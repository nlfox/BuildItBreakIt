#include "permissions.h"

#include <algorithm>
#include <string>
#include <stack>
#include <map>
#include <set>

using namespace std;

namespace bibifi {
  Delegation::Delegation(string f, string a, string p, string u) :
    field(f),
    authority(a),
    permission(p),
    user(u) {}

  bool Delegation::operator ==(const Delegation &other) const {
    return field == other.field && authority == other.authority && permission == other.permission && user == other.user;
  }
  
  SecurityState::SecurityState() :
    delegations(),
    defaultDel("anyone"),
    identifiers(),
    delegationsPatch(),
    defaultPatch(""),
    identifiersPatch(),
    cache() {}

  void SecurityState::beginTransaction() {
    defaultPatch = defaultDel;
    identifiersPatch.clear();
    cache.clear();
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
      delegationsPatch[user] = vector<Delegation>();
      for (int i = 0; i < 4; i++) {
	delegationsPatch[user].push_back(Delegation("all", defaultPatch, permissions[i], user));
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
      Delegation d (field, authority, permission, user);
      auto i = find(delegationsPatch[user].begin(), delegationsPatch[user].end(), d);
      if (i == delegationsPatch[user].end()) {
	delegationsPatch[user].push_back(d);
      }
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
      auto i = find(delegationsPatch[user].begin(), delegationsPatch[user].end(), d);
      if (i != delegationsPatch[user].end()) {
	cache.clear();
	delegationsPatch[user].erase(i);
      }
    }
  }

  bool SecurityState::hasPermission(string user, string field, string permission) {
    if (user == "admin") return true;
    string id = user + field + permission;
    if (cache.find(id) != cache.end()) {
      return cache[id];
    }
    
    stack<string> tbs;
    set<string> visited;
    visited.insert(user);
    for (vector<Delegation>::iterator i = delegationsPatch[user].begin(); i != delegationsPatch[user].end(); i++) {
      if (((*i).field == field || (*i).field == "all") && (*i).permission == permission) {
	tbs.push((*i).authority);
      }
    }
    
    for (vector<Delegation>::iterator i = delegationsPatch["anyone"].begin(); i != delegationsPatch["anyone"].end(); i++) {
      if (((*i).field == field || (*i).field == "all") && (*i).permission == permission) {
	tbs.push((*i).authority);
      }
    }

    bool foundPermission = false;
    while (!tbs.empty()) {
      string authority = tbs.top();
      tbs.pop();
      if (authority == "admin" || authority == "") {
	foundPermission = true;
	break;
      }

      for (int i = 0; i < delegationsPatch[authority].size(); i++) {
	Delegation d = delegationsPatch[authority][i];
	if ((d.field == field || d.field == "all") && d.permission == permission && visited.find(d.authority) == visited.end()) {
	  tbs.push(d.authority);
	  visited.insert(d.authority);
	}
      }
    }

    cache[id] = foundPermission;
    return foundPermission;
  }
};
