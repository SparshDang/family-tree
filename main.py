from enum import Enum
import pickle

class Relation(Enum):
    CHILD = 1
    SPOUSE = 2
    SIBLING = 3

class Person:
    def __init__(self,name,parent, id):
        self.id = id
        self.parent=parent
        self.name = name

class Relationship:
    def __init__(self, person, relation_with, relation):
        self.person = person
        self.relation_with = relation_with
        self.relation = relation


class Family:
    def __init__(self):
        self.family_head = None
        self.number_of_members = 0 
        self.members = []
        self.relations = []


    def add_head(self,name):
        self.family_head = Person(name, 0, self.number_of_members)
        self.number_of_members+=1
        self.members.append(self.family_head)
        return self.family_head
    
    def add_member(self, name, relation_with_id, relation):
        if  relation_with_id == "":
            return self.add_head(name)
        relation_with = [person for person in self.members if person.id == relation_with_id][0]
        relation = int(relation)
        if relation == 2 or relation == 3:
            parent = relation_with.parent
        else:
            parent = relation_with
        
        new_member = Person(name, parent, self.number_of_members)
        self.members.append(new_member)
        self.number_of_members+=1

        if int(relation) == 1:
            relation = Relation.CHILD
        else:
            relation = Relation.SPOUSE

        self.add_relation(new_member, relation_with, relation)
        return new_member

    def add_relation(self,person, relation_with, relation):
        if relation == Relation.SPOUSE:
            print("Hello")
            for relation_ in self.relations:
                if relation_.relation_with == relation_with and relation_.relation == Relation.SPOUSE:
                    self.relations.remove(relation_)
                    break

        new_relation = Relationship(person, relation_with,relation)
        self.relations.append(new_relation)

    def get_relation_of_person(self,person):
        return  [relation for relation in self.relations if person == relation.relation_with]
      
    def get_spouse(self,relations):
        for relation in relations:
            if relation.relation ==   Relation.SPOUSE:
                return relation.person
            
    def delete_person(self, person_id):
        person = [person for person in self.members if person.id == person_id][0]

        person_relations = self.get_relation_of_person(person)
        for relation in person_relations:
            self.relations.remove(relation)
            self.delete_person(relation.person.id)

    def get_head(self):
        return self.family_head
    
    def save_family_tree(self):
        with open("family.txt", "wb") as fileHandler:
                pickle.dump(self,fileHandler)

    @staticmethod
    def load_family_tree():
        with open("family.txt", "rb") as fileHandler:
            return pickle.loads(fileHandler.read())