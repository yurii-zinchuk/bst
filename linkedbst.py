"""
File: linkedbst.py
Author: Ken Lambert
"""

from platform import node
from time import perf_counter
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedqueue import LinkedQueue
from linkedstack import LinkedStack
from math import log
import random


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                # yield node.data
                yield node
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)

        # return recurse(self._root)

        # elements = set([elem.data for elem in self])
        # if item not in elements:
        #     return None
        
        try:
            node = self._root
            while True:
                if item == node.data:
                    return node.data
                elif item < node.data:
                    node = node.left
                else:
                    node = node.right
        except ValueError:
            return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # # Helper function to search for item's position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left == None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right == None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # # Tree is empty, so new item goes at the root
        # if self.isEmpty():
        #     self._root = BSTNode(item)
        # # Otherwise, search for the item's spot
        # else:
        #     recurse(self._root)
        # self._size += 1

        if self._root is not None:
            node = self._root
        else:
            self._root = BSTNode(item)
            return
        while True:
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                    break
                else:
                    node = node.left
            else:
                if node.right is None:
                    node.right = BSTNode(item)
                    break
                else:
                    node = node.right
            self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        leaves = []
        for node in self:
            if self.is_leaf(node):
                leaves.append(node)

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            Переробити нормально
            '''
            cur_comp = self._root
            height = 0
            while cur_comp.data != top.data:
                if top.data < cur_comp.data:
                    # go left
                    cur_comp = cur_comp.left
                    height += 1
                else:
                    # go right
                    cur_comp = cur_comp.right
                    height += 1
            return height

        height = 0
        for leaf in leaves:
            height = max(height, height1(leaf))

        return height

    @staticmethod
    def is_leaf(node):
        return True if node.right is None and node.left is None else False

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return True if self.height() < 2*log(self._size+1, 2)-1 else False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        range_items = [node.data for node in self if (
            low <= node.data <= high)]
        return range_items

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        tree_cp = [node.data for node in self]
        self.clear()
        tree_cp.sort(key=lambda x: x)
        while tree_cp:
            middle = tree_cp.pop((len(tree_cp))//2)
            self.add(middle)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        tree_cp = [node.data for node in self]
        try:
            successor = min([val for val in tree_cp if val > item])
            return successor
        except ValueError:
            pass

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        tree_cp = [node.data for node in self]
        try:
            preccessor = max([val for val in tree_cp if val < item])
            return preccessor
        except ValueError:
            pass

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, "r") as file:
            vocabulary = [line[:-1] for line in file]
        random_10000 = random.sample(vocabulary, 10000)


        start = perf_counter()
        for word in random_10000:
            vocabulary.index(word)
        end = perf_counter()
        taken1 = end-start
        print(f"Time to find in list: {taken1}")


        for word in vocabulary:
            self.add(word)
        start = perf_counter()
        for word in random_10000:
            self.find(word)
        end = perf_counter()
        taken2 = end = start
        print(f"Time to find in alpahbetic tree: {taken2}")

        random.shuffle(vocabulary)
        for word in vocabulary:
            self.add(word)
        start = perf_counter()
        for word in random_10000:
            self.find(word)
        end = perf_counter()
        taken3 = end - start
        print(f"Time to find in random tree: {taken3}")


if __name__ == "__main__":
    tree = LinkedBST()
    tree.demo_bst("words.txt")
