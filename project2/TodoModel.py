from datetime import datetime

class Todo:
    id: int
    title: str
    descriptions: str
    is_completed: bool
    priority: int
    created_at: datetime

    def __init__(self, id, title, descriptions, is_completed, priority):
        self.id = id
        self.title = title
        self.descriptions = descriptions
        self.is_completed = is_completed
        self.priority = priority
        self.created_at = datetime.now()