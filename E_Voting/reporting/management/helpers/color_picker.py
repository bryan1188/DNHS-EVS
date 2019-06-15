import random

class ColorPicker():
    # opacity = 1
    COLOR_LIST = [
            'rgba(255, 99, 132, {})',
            'rgba(54, 162, 235, {})',
            'rgba(255, 206, 86, {})',
            'rgba(75, 192, 192, {})',
            'rgba(153, 102, 255, {})',
            'rgba(255, 159, 64, {})',
            'rgba(104, 204, 81, {})',
            'rgba(239, 38, 108, {})',
    ]

    def __init__(self):
        self.opacity = 1
        self.color_list = list(self.COLOR_LIST) #new list instance

    def get_random_color(self):
        '''
            Return random color from the list.
        '''
        if len(self.color_list) > 0:
            random.shuffle(self.color_list)
            color = self.color_list.pop()
            return color.format(self.opacity)
        else:
            # replenesh the list
            self.replenesh_color_list()
            return self.get_random_color()

    def replenesh_color_list(self):
        self.color_list = list(self.COLOR_LIST)
