class DoublyLinkedList:
    class Node:
        def __init__(self, data=None):
            self.data = data
            self.prev = None
            self.next = None

        def __repr__(self):
            return f"Node({self.data})"

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
        self.node_dict = {}

    def __len__(self):
        return self.length
    
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.data
            node = node.next
    
    def __repr__(self):
        if len(self) == 0:
            return "Empty DoublyLinkedList"
        
        current = self.head
        linked_list_str = f"DoublyLinkedList of length {self.length}:\n    "
        while current is not None:
            linked_list_str += f"{current.data}"
            if current.next is not None:
                linked_list_str += " <-> "
            current = current.next
        return linked_list_str
    
    def _find_node(self, data):
        if data in self.node_dict:
            return self.node_dict[data]
        return None

    def append(self, data):
        new_node = self.Node(data)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.node_dict[data] = new_node
        self.length += 1

    def prepend(self, data):
        new_node = self.Node(data)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.node_dict[data] = new_node
        self.length += 1

    def insert_after(self, prev_node_data, data):
        new_node = self.Node(data)
        prev_node = self._find_node(prev_node_data)
        if prev_node is None:
            raise ValueError(f"Node with data '{prev_node_data}' not found.")
        if prev_node is self.tail:
            self.tail = new_node
        new_node.next = prev_node.next
        new_node.prev = prev_node
        if prev_node.next is not None:
            prev_node.next.prev = new_node
        prev_node.next = new_node
        self.node_dict[data] = new_node
        self.length += 1

    def insert_before(self, next_node_data, data):
        new_node = self.Node(data)
        next_node = self._find_node(next_node_data)
        if next_node is None:
            raise ValueError(f"Node with data '{next_node_data}' not found.")
        if next_node is self.head:
            self.head = new_node
        new_node.prev = next_node.prev
        new_node.next = next_node
        if next_node.prev is not None:
            next_node.prev.next = new_node
        next_node.prev = new_node
        self.node_dict[data] = new_node
        self.length += 1

    def remove(self, data):
        node = self._find_node(data)
        if node is None:
            raise ValueError(f"Node with data '{data}' not found.")
        if node is self.head:
            self.head = node.next
        if node is self.tail:
            self.tail = node.prev
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        del self.node_dict[data]
        self.length -= 1

    def append_vector(self, vec):
        for element in vec:
            self.append(element)
            self.node_dict[element] = self._find_node(element)
    
    def clear(self):
        self.head = None
        self.tail = None
        self.length = 0
        self.node_dict = {}