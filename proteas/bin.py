
class Bin():
    def __init__(self):
        self.storage= []
        self.questinables=[]

    def add(self, thing):
        self.storage.append(thing)

    def reset(self):
        self.storage = []

    def bring(self, name):

        for p in self.storage:
            pass

        for idx, p in enumerate(self.storage):
            if  p.name == name:
                return p

    def bring_by_category(self, cat):
        selections=[]
        for idx, p in enumerate(self.storage):
            if p.category == cat:
                selections.append(p)
        return  selections
    def find_questionable_prompts(self):
        questinables=[]
        for idx, p in enumerate(self.storage):
            if p.category=="context_prompts":
               # question = p
                questinables.append(p)

        self.questinables= questinables