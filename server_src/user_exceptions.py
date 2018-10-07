class UserExceptions(Exception):
    def __init__(self, contact_name):
        self.name = contact_name


class UserNotExisting(UserExceptions):
    def __str__(self):
        return 'User "{}" not existing'.format(self.name)


class UserAlreadyExists(UserExceptions):
    def __str__(self):
        return 'User "{}" already exists'.format(self.name)


class ContactAlreadyInList(UserExceptions):
    def __str__(self):
        return '"{}" already in contacts list'.format(self.name)


class ContactNotInList(UserExceptions):
    def __str__(self):
        return '"{}" not in contacts list'.format(self.name)


class SelfAdding(UserExceptions):
    def __str__(self):
        return '"{}" trying to add self to contact list'.format(self.name)
