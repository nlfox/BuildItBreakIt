#ifndef __PERMISSIONS_H__
#define __PERMISSIONS_H__

#include <string>
#include <vector>
#include <map>
#include <set>

namespace bibifi {
  class Delegation {
  public:
    std::string field;
    std::string authority;
    std::string permission;
    std::string user;

    Delegation(std::string, std::string, std::string, std::string);

    std::string getString() const;

    bool operator ==(const Delegation&) const;
    bool operator <(const Delegation&) const;
    bool operator >(const Delegation&) const;
  };
  
  class SecurityState {
  public:
    SecurityState();
    void beginTransaction();
    void completeTransaction();
    void discardTransaction();
    void addUser(std::string);
    void own(std::string, std::string);
    void setDefault(std::string);
    void setDelegation(std::string, std::string, std::string, std::string);
    void deleteDelegation(std::string, std::string, std::string, std::string);
    bool hasPermission(std::string, std::string, std::string);

  private:
    std::string permissions [4] = {"delegate", "read", "write", "append"};
    
    std::map<std::string, std::set<Delegation> > delegations;
    std::string defaultDel;
    std::set<std::string> identifiers;

    std::map<std::string, std::set<Delegation> > delegationsPatch;
    std::string defaultPatch;
    std::set<std::string> identifiersPatch;
  };
}

#endif
