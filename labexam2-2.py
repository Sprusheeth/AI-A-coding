from collections import Counter

class Node:
	def __init__(self, data, next=None): self.data, self.next = data, next

class LinkedList:
	def __init__(self): self.head = None
	def insert(self, x): self.head = Node(x, self.head)
	def to_list(self):
		a = []; t = self.head
		while t: a.append(t.data); t = t.next
		return a
	def search(self, x):
		t = self.head
		while t and t.data != x: t = t.next
		return t is not None
	def freq(self): c = Counter(self.to_list()); m = max(c.values(), default=0); return c, [k for k, v in c.items() if v == m]

if __name__ == "__main__":
	ll = LinkedList()
	for x in [5, 1, 2, 5, 2, 3, 2]: ll.insert(x)
	c, tied = ll.freq()
	print("List:", ll.to_list())
	print("Search 2:", ll.search(2), "| Search 9:", ll.search(9))
	print("Frequency:", dict(c))
	print("Most frequent (tie-aware):", tied)
