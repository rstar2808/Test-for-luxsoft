#!/usr/bin/env python

# Задача 1.
class Node(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return 'Node({})'.format(self.val)

    def serialize(self):
        components = []

        def incorporate(self, components):
            components.append(str(self.val))
            if self.left:
                components.append('L')
                incorporate(self.left, components)
            if self.right:
                components.append('R')
                incorporate(self.right, components)
            components.append('U')
            return ''.join(components)

        incorporate(self, components)
        components.pop()
        return ''.join(components)

def deserialize(string):
    chars = ''
    nodes = []
    next_child = None
    for i, char in enumerate(string):
        if char not in ('L', 'R', 'U'):
            chars += char
        else:
            if not nodes:
                nodes.append(Node(int(chars)))
            elif next_child == 'left':
                nodes[-1].left = Node(int(chars))
                nodes.append(nodes[-1].left)
            elif next_child == 'right':
                nodes[-1].right = Node(int(chars))
                nodes.append(nodes[-1].right)
            elif next_child == 'up':
                nodes.pop()
            if char == 'L':
                next_child = 'left'
            elif char == 'R':
                next_child = 'right'
            elif char == 'U':
                next_child = 'up'
            chars = ''
    return nodes[0]

"""
My BT
          1
         / \
        2   3
       / \   \
      4   5   6

"""

BT = Node(1)
BT.left = Node(2)
BT.left.left = Node(4)
BT.right = Node(3)
BT.left.right = Node(5)
BT.right.right = Node(6)

# Сериализуем в строку.
print BT.serialize()  # '1L2L4UR5UUR3R6UU'
# В обратную сторону.
print deserialize('1L2L4UR5UUR3R6UU')  # 'Node(1)'

# P.S. Вообще не сталкивался со структурой данных такой как бинарное не сбалансированое дерево. Из за этого пришлось поискать ответ в интернете.
# Нашел этот код. Признаюсь честно просмотрел и немного изменил. Но вывод можно сделать что Google пользоватся могу. Поэтому если что то будет встречатся не понятное буду искать сам а не дергать по 100 раз.


# Задача 1. (SQL)
SELECT * FROM Users GROUP BY Name HAVING COUNT(Name) > 2;
# Задача 2. (SQL)
SELECT * FROM Users WHERE Users.Id NOT IN (SELECT Data.User_id FROM Users LEFT JOIN Data on (Users.Id = Data.User_id) WHERE Data.Data IS NOT NULL);
# P.S. Последний раз работал с мускулем 2 года назад не судите строго. :-)