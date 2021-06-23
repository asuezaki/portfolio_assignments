# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        for i in range(len(self._buckets)):
            if self._buckets[i].head is not None:
                self._buckets[i] = LinkedList()
        self.size = 0

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        index = self._hash_function(key) % self.capacity           # variable to find bucket index
        if self._buckets[index].contains(key) is not None:         # checking if key is present
            return self._buckets[index].contains(key).value
        else:                                                       # if link isn't found, returns None
            return None

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        buckets = []        # lists to store buckets, keys, and values
        keys = []
        vals = []
        for i in range(capacity):           # initializing new hash table with buckets with linked lists
            buckets.append(LinkedList())
        for p in range(0, len(self._buckets)):      # iterating through buckets to gather keys and values
            curr = self._buckets[p].head
            while curr is not None:                 # checking each bucket
                keys.append(curr.key)               # saving current keys and values to list
                vals.append(curr.value)
                curr = curr.next                    # iterating through linked lists in each bucket
            self._buckets[p] = LinkedList()         # clearing each bucket after saving keys and values
        self._buckets = buckets                     # set bucket list to new bucket list
        self.capacity = capacity                    # set capacity to new capacity
        self.size = 0                               # reset size
        for q in range(0, len(keys)):               # rehash keys and values stored in the lists
            self.put(keys[q], vals[q])

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        index = self._hash_function(key) % self.capacity           # variable to find bucket index
        if self._buckets[index].contains(key) is not None:                 # checking if key already exists
            self._buckets[index].contains(key).value = value               # updates value if key exists
        else:
            self._buckets[index].add_front(key, value)       # adds new link it key doesn't exist
            self.size += 1

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        index = self._hash_function(key) % self.capacity           # variable to find bucket index
        if self._buckets[index].contains(key) is None:             # returns if link doesn't exist
            return
        else:
            self._buckets[index].remove(key)                       # removes link containing the inputted key
            self.size -= 1

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        index = self._hash_function(key) % self.capacity           # variable to find bucket index
        if self._buckets[index].contains(key) is not None:
            return True                                            # returns True if key exists
        else:
            return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        counter = 0     # counter for empty buckets
        for i in self._buckets:     # iterating through buckets
            if i.head is None:      # adding to counter for each empty bucket
                counter += 1
        return counter              # returns count of empty buckets

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        return self.size / self.capacity

    def get_data(self):
        """Function that returns all of the stored keys and values in a list of tuples"""
        data = []        # list to store tuples
        for i in range(0, len(self._buckets)):          # iterating through buckets
            curr = self._buckets[i].head
            while curr is not None:                     # checking each bucket
                data.append((curr.key, curr.value))   # adding each key and value to the list paired as a tuple
                curr = curr.next                        # iterating through links in buckets
        return data                                     # returns the list

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
