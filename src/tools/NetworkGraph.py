import time


class GraphNode:
    def __init__(self, address, father_address):
        """

        :param address: (ip, port)
        :type address: tuple

        """
        self.on = False
        self.father_address = father_address
        self.childs = []
        self.address = address
        #self.on = False
        self.lastunion = 0
        pass

    def set_parent(self, parent):
        pass

    def set_address(self, new_address):
        pass

    def __reset(self):
        pass

    def add_child(self, child):
        pass

    def set_time(self, time):
        self.time = time


class NetworkGraph:
    def __init__(self, root):
        self.root = root
        root.alive = True
        self.nodes = [root]

    def find_live_node(self, sender):
        for i in range(len(self.nodes)):
            if sender == self.nodes[i].address and self.nodes[i].on == True:
                return None
        father = self.BFS(self.root)
        self.add_node(sender, father.address)
        return father.address

    def turnoff(self, Node):

        """
        Here we should find a neighbour for the sender.
        Best neighbour is the node who is nearest the root and has not more than one child.

        Code design suggestion:
            1. Do a BFS algorithm to find the target.

        Warnings:
            1. Check whether there is sender node in our NetworkGraph or not; if exist do not return sender node or
               any other nodes in it's sub-tree.

        :param sender: The node address we want to find best neighbour for it.
        :type sender: tuple

        :return: Best neighbour for sender.
        :rtype: GraphNode
        """
        pass

    def find_node(self, ip, port):
        pass

    def turn_on_node(self, node_address):
        pass

    def turn_off_node(self, address):
        for i in range(len(self.nodes)):
            if(self.nodes[i].address == address):
                x = self.nodes.pop(i)
        for i in range(len(self.nodes)):
            if(x.father_address == self.nodes[i].address):
                self.nodes[i].childs.remove(x)

        pass

    def remove_node(self, node_address):
        pass

    def add_node(self, address, father_address):
        x = GraphNode(address, father_address)
        x.on = True
        x.lastunion = time.time()
        for i in range(len(self.nodes)):
            if(father_address == self.nodes[i].address):
                self.nodes[i].childs += [x]
        self.nodes += [x]

        """
        Add a new node with node_address if it does not exist in our NetworkGraph and set its father.

        Warnings:
            1. Don't forget to set the new node as one of the father_address children.
            2. Before using this function make sure that there is a node which has father_address.

        :param ip: IP address of the new node.
        :param port: Port of the new node.
        :param father_address: Father address of the new node

        :type ip: str
        :type port: int
        :type father_address: tuple


        :return:
        """
        pass

    def BFS(self, root):
        queue = [root]
        while True:
            node = queue.pop(0)
            if len(node.childs) >= 2:
                for i in range(len(node.childs)):
                    queue += [node.childs[i]]
            else:
                break
        return node