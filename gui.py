from tkinter import *
from tkinter.ttk import *

from main import Family, Person, Relation,Relationship

class GUI(Tk):
    def __init__(self) :
        super().__init__()

        self.HEIGHT = 400
        self.WIDTH = 600
        self.resizable(0,0)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.set_home_frame()
    

    def set_home_frame(self):
        self.home_frame = Frame(self)
        self.home_frame.place(relx=0,rely=0,relheight=1,relwidth=1)
        Label(self.home_frame, text="Welcome to Family Tree", font=("Arial",30,"bold")).pack()
        Button(self.home_frame, text="Create New Tree", command=lambda :self.set_main_frame(False)).pack()
        Button(self.home_frame, text="Load Tree", command=lambda :self.set_main_frame(True)).pack()


    def set_main_frame(self, load_family=False):
        if load_family:
            self.family = Family.load_family_tree()
        else:
            self.family = Family()

        self.set_treeview()
        self.set_action_frame()
        self.set_family_in_treeview()



    def set_treeview(self):
        self.treeview = Treeview(selectmode="browse", columns=[ "Spouse"])
        self.treeview.heading("#0", text="Name")
        self.treeview.heading("#1", text="Spouse")
        self.treeview.place(relx=0, rely=0,relheight=1,relwidth=0.6)

    def set_family_in_treeview(self):
        head = self.family.get_head()
        if head:
            self.set_family_in_treeview_util(head)
    
    def set_family_in_treeview_util(self,person, parent=None):
        person_relations = self.family.get_relation_of_person(person)
        spouse = self.family.get_spouse(person_relations)
        if not parent:
            new_item = self.treeview.insert("", "end",text=person.name, values=[spouse.name if spouse else ""], iid=person.id)
        else:
            new_item = self.treeview.insert(parent,"end",text=person.name,values=[spouse.name if spouse else ""], iid=person.id )

        for relation in person_relations:
            if relation.relation != Relation.SPOUSE:
                self.set_family_in_treeview_util(relation.person, new_item)
    

    def set_action_frame(self):
        self.action_frame = Frame(self)
        self.action_frame.place(relx=0.6, rely=0, relheight=1, relwidth=0.4)
        self.set_action_form()
        self.set_actions_buttons()

    def set_action_form(self):

        self.name_var = StringVar()
        self.relation_var = StringVar()
        Label(self.action_frame, text="Name").pack()
        Entry(self.action_frame, textvariable=self.name_var).pack()
        Label(self.action_frame, text="Relation").pack()
        Radiobutton(self.action_frame, text='Child', value=1, variable=self.relation_var).pack()
        Radiobutton(self.action_frame, text='Spouse', value=2, variable=self.relation_var).pack()
        Button(self.action_frame, text="Add Relation", command=self.add_member).pack()
        Button(self.action_frame, text="Delete Member", command=self.delete_member).pack()

    def add_member(self):
        if self.treeview.selection():
            relation_with = int(self.treeview.selection()[0])
        else:
            relation_with = ""
        name = self.name_var.get()
        relation = self.relation_var.get()
        person = self.family.add_member(name,relation_with, relation)
        if relation == "1" or not relation:
            self.treeview.insert(str(relation_with), "end", text = name, values=[""], iid=person.id )
            self.treeview.update()

        else:
            self.treeview.set(item=relation_with,column="Spouse", value=name)

    def delete_member(self):
        person_id = int(self.treeview.selection()[0])
        self.family.delete_person(person_id)
        self.treeview.delete(person_id)
        self.treeview.update()
    
    def set_actions_buttons(self):
        self.export_family = Button(self.action_frame, text="Save Family", command= self.family.save_family_tree)
        self.export_family.pack(side="right",fill='x', expand=True)

    

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()