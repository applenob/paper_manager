# coding=utf-8

paper_item_list = ['paper_name', 'importance',
                   'urgency', 'tags', 'path',
                   'read', 'date', 'id']


class Paper:
    def __init__(self, importance, urgency, tags, name, path, read, date):
        self.importance = importance
        self.urgency = urgency
        self.tags = tags
        self.name = name
        self.path = path
        self.read = read
        self.date = date

