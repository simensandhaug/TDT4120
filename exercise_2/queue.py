# 1037
class Queue:
    def __init__(self, max_size):
        self.head = self.tail = 0
        self.val = [None] * max_size

    def enqueue(self, value):
        try:
            self.val[self.tail] = value
            self.tail += 1
            return
        except:
            self.val[0] = value
            self.tail = 1

    def dequeue(self):
        try:
            value = self.val[self.head]
            self.head += 1
            return value
        except:
            value = self.val[0]
            self.head = 1
            return value
highscore = True