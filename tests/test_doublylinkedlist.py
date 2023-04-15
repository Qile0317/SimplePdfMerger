import pytest
from SimplePdfMerger.doublinklist import *

def test_empty_list():
    dll = DoublyLinkedList()
    assert len(dll) == 0
    assert list(dll) == []
    assert str(dll) == "Empty DoublyLinkedList"

def test_append():
    dll = DoublyLinkedList()
    dll.append(1)
    assert len(dll) == 1
    assert list(dll) == [1]
    assert str(dll) == "DoublyLinkedList of length 1:\n    1"
    dll.append(2)
    assert len(dll) == 2
    assert list(dll) == [1, 2]
    assert str(dll) == "DoublyLinkedList of length 2:\n    1 <-> 2"
    
def test_prepend():
    dll = DoublyLinkedList()
    dll.prepend(1)
    assert len(dll) == 1
    assert list(dll) == [1]
    assert str(dll) == "DoublyLinkedList of length 1:\n    1"
    dll.prepend(2)
    assert len(dll) == 2
    assert list(dll) == [2, 1]
    assert str(dll) == "DoublyLinkedList of length 2:\n    2 <-> 1"

def test_insert_after():
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.append(4)
    dll.insert_after(1, 3)
    assert len(dll) == 4
    assert list(dll) == [1, 3, 2, 4]
    assert str(dll) == "DoublyLinkedList of length 4:\n    1 <-> 3 <-> 2 <-> 4"
    with pytest.raises(ValueError):
        dll.insert_after(5, 3)

def test_insert_before():
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.append(4)
    dll.insert_before(4, 3)
    assert len(dll) == 4
    assert list(dll) == [1, 2, 3, 4]
    assert str(dll) == "DoublyLinkedList of length 4:\n    1 <-> 2 <-> 3 <-> 4"
    with pytest.raises(ValueError):
        dll.insert_before(5, 3)

def test_remove():
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.append(3)
    dll.append(4)
    dll.remove(2)
    assert len(dll) == 3
    assert list(dll) == [1, 3, 4]
    assert str(dll) == "DoublyLinkedList of length 3:\n    1 <-> 3 <-> 4"
    with pytest.raises(ValueError):
        dll.remove(5)

def test_append_vector():
    dll = DoublyLinkedList()
    vec = [1, 2, 3, 4]
    dll.append_vector(vec)
    assert len(dll) == 4
    assert list(dll) == vec
    assert str(dll) == "DoublyLinkedList of length 4:\n    1 <-> 2 <-> 3 <-> 4"
    
def test_clear():
    linked_list = DoublyLinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.clear()
    assert len(linked_list) == 0
    assert linked_list.head is None
    assert linked_list.tail is None