class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.__colleague_set = set()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self) -> str:
        return f"<Actor {self.actor_full_name}>"

    def __eq__(self, other: 'Actor') -> bool:
        if type(self) == type(other) and self.actor_full_name == other.actor_full_name:
            return True
        return False

    def __lt__(self, other: 'Actor') -> bool:
        if type(self) == type(other) and self.actor_full_name < other.actor_full_name:
            return True
        if type(self) != type(other):
            raise TypeError(f"Cannot compare Actor instance with {type(other)}")
        return False

    def __hash__(self):
        return hash(self.actor_full_name)

    def add_actor_colleague(self, colleague: 'Actor'):
        if type(self) != type(colleague):
            raise TypeError(f"Expect colleague to be Actor type, instead {type(colleague)} found")
        self.__colleague_set.add(colleague)

    def check_if_this_actor_worked_with(self, colleague: 'Actor') -> bool:
        return colleague in self.__colleague_set
