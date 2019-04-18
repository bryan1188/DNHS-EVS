
class NoDupList:

    def __init__(self):
        self.list_data_ = list()

    def append(self, data):
        if not data in self.list_data_:
            self.list_data_.append(data)

    @property
    def list_data(self):
        return self.list_data_
