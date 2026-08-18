class Queue:
    def __init__(self):
        self.items = []

    def insert(self, value):
        self.items.append(value)

    def pop(self):
        if self.is_empty():
            print("Warning: queue is empty")
            return None
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0
# ---------------------------------------------------
print("--- 01 & 02 Build and Try Your Queue ---")
q = Queue()
q.insert(101)
q.insert(102)
q.insert(103)

print(q.pop())
print(q.pop())
print(q.pop())
q.pop()
# ---------------------------------------------------
print("\n--- 03 Add a Name and a Size Limit ---")

class QueueOutOfRangeException(Exception):
    pass

class NamedQueue(Queue):
    registry = {}

    def __init__(self, name, size):
        super().__init__()
        self.name = name
        self.size = size
        NamedQueue.registry[name] = self

    def insert(self, value):
        if len(self.items) >= self.size:
            raise QueueOutOfRangeException(f"queue '{self.name}' is full")
        super().insert(value)
        
    @classmethod
    def get_queue(cls, name):
        return cls.registry.get(name)

try:
    nq = NamedQueue("sensors", 2)
    nq.insert("temp_1")
    nq.insert("temp_2")
    print("Inserted two items successfully.")
    nq.insert("temp_3")
except QueueOutOfRangeException as e:
    print(f"Exception caught: {e}")
# ---------------------------------------------------
print("\n--- 04 Track Every Queue by Name ---")
nq1 = NamedQueue("jobs", 5)
nq2 = NamedQueue("tasks", 3)

fetched_q = NamedQueue.get_queue("jobs")
print(f"Fetched queue name: {fetched_q.name}")
print(f"Is it the exact same object? {fetched_q is nq1}")
