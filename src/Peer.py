from src.Stream import Stream
from src.Packet import Packet, PacketFactory
from src.UserInterface import UserInterface
from src.tools.Node import Node
from src.tools.NetworkGraph import NetworkGraph, GraphNode
import time
import threading

"""
    Peer is our main object in this project.
    In this network Peers will connect together to make a tree graph.
    This network is not completely decentralised but will show you some real-world challenges in Peer to Peer networks.
    
"""


class Peer:
    def __init__(self, server_ip, server_port, is_root=False, root_address=None):
        self.server_ip = server_ip
        self.server_port = server_port
        self.is_root = is_root
        self.is_registered = False
        self.stream_object = Stream(self.server_ip, self.server_port)
        self.packetFactory_object = PacketFactory()
        self.interface_object = UserInterface()
        self.start_user_interface()
        self.father_address = (None,None)
        self.a = threading.Thread(target=self.run_reunion_daemon)
        self.tuple = (self.server_ip, self.server_port)
        self.condition = True
        self.is_first_advertised = False
        if(is_root == True):
            root = GraphNode(self.tuple, None)
            self.networkgraph_object = NetworkGraph(root)
            self.a.start()
            self.condition = True
        else:
            self.root_address = root_address
            self.lastuninonback = 0
            self.mode = -1
            self.waiting = 36
        self.run()

        """
        The Peer object constructor.

        Code design suggestions:
            1. Initialise a Stream object for our Peer.
            2. Initialise a PacketFactory object.
            3. Initialise our UserInterface for interactioisn with user commandline.
            4. Initialise a Thread for handling reunion daemon.

        Warnings:
            1. For root Peer, we need a NetworkGraph object.
            2. In root Peer, start reunion daemon as soon as possible.
           // 3. In client Peer, we need to connect to the root of the network, Don't forget to set this connection
               as a register_connection.


        :param server_ip: Server IP address for this Peer that should be pass to Stream.
        :param server_port: Server Port address for this Peer that should be pass to Stream.
        :param is_root: Specify that is this Peer root or not.
        :param root_address: Root IP/Port address if we are a client.

        :type server_ip: str
        :type server_port: int
        :type is_root: bool
        :type root_address: tuple
        """
        pass

    def start_user_interface(self):
        self.interface_object.start()
        """
        For starting UserInterface thread.

        :return:
        """
        pass

    def handle_user_interface_buffer(self):
        length = len(self.interface_object.buffer)
        for i in range(length):
            x = self.interface_object.buffer[i]
            str = x.split(" ")
            if(str[0] == "Register"):
                if(self.is_root == False):
                    if(self.is_registered == False):
                        print("register message sent")
                        self.stream_object.add_node(self.root_address, True)
                        packet = self.packetFactory_object.new_register_packet("request", self.tuple, self.tuple)
                        self.stream_object.add_message_to_out_buff(self.root_address, packet, True )
                    else:
                        print("already registered")
                else:
                    print("not valid command for root")
            elif(str[0] == "Advertise"):
                if(self.is_root == False):
                    node = self.stream_object.get_node_by_server(self.root_address)
                    if node is not None and self.is_registered == True:
                        print("advertise message sent")
                        packet = self.packetFactory_object.new_advertise_packet("request", self.tuple, None)
                        self.stream_object.add_message_to_out_buff(self.root_address, packet, True)

                else:
                    print("not valid command")

            elif(str[0] == "Sendmessage"):
                message = x[12:]
                packet = self.packetFactory_object.new_message_packet(message, self.tuple)
                for i in range(len(self.stream_object.Nodes)):
                    if(self.stream_object.Nodes[i].is_register_connection == False):
                        self.stream_object.add_message_to_out_buff(self.stream_object.Nodes[i].get_server_address(), packet,False)
            else:
                print("Invalid")
        self.interface_object.buffer.clear()
        """
        In every interval, we should parse user command that buffered from our UserInterface.
        All of the valid commands are listed below:
            1. Register:  With this command, the client send a Register Request packet to the root of the network.
            2. Advertise: Send an Advertise Request to the root of the network for finding first hope.
            3. SendMessage: The following string will be added to a new Message packet and broadcast through the network.

        Warnings:
            1. Ignore irregular commands from the user.
            2. Don't forget to clear our UserInterface buffer.
        :return:
        """
        pass

    def run(self):

        while True:
            for i in range(len(self.stream_object._server_in_buf)):
                packet = self.packetFactory_object.parse_buffer(self.stream_object._server_in_buf[i])
                self.handle_packet(packet)
            self.stream_object.clear_in_buff()
            if (self.condition == True):
                self.handle_user_interface_buffer()
                self.stream_object.send_out_buf_messages()
            time.sleep(2)
        """
        The main loop of the program.
        
        Code design suggestions:
            1. Parse server in_buf of the stream.
            2. Handle all packets were received from our Stream server.
            3. Parse user_interface_buffer to make message packets.
           // 4. Send packets stored in nodes buffer of our Stream object.
            5. ** sleep the current thread for 2 seconds **

       // Warnings:
            1. At first check reunion daemon condition; Maybe we have a problem in this time
               and so we should hold any actions until Reunion acceptance.
            2. In every situation checkout Advertise Response packets; even is Reunion in failure mode or not

        :return:
        """
        pass

    def run_reunion_daemon(self):
        while True:
            if(self.is_root == False and self.condition == True):

                if(time.time() - self.lastuninonback < 4):

                    pass
                if(time.time() - self.lastuninonback >= 4 and self.mode == 0 and self.is_first_advertised == True):

                    print("reunion packet sent")
                    packet = self.packetFactory_object.new_reunion_packet("request", (self.server_ip, self.server_port), "")
                    self.stream_object.add_message_to_out_buff(self.father_address, packet, False)
                    self.mode = 1
                if(time.time() - self.lastuninonback > 4 and time.time()- self.lastuninonback <= 36 and self.mode == 1):
                    pass
                if(time.time() - self.lastuninonback > 36 and self.is_first_advertised == True):
                    self.condition = False
                    print("ooops ! reunion failed so advertise packet should be sent")
                    father_node = self.stream_object.get_node_by_server(self.father_address)
                    self.stream_object.remove_node(father_node)
                    self.father_address = (None, None)
                    packet = self.packetFactory_object.new_advertise_packet("request", self.tuple, None)
                    self.stream_object.add_message_to_out_buff(self.root_address, packet,True)
                    self.stream_object.send_out_buf_messages()
                    self.mode = 0
            elif(self.is_root == False and self.condition == False):

                time.sleep(2)
                packet = self.packetFactory_object.new_advertise_packet("request", self.tuple, None)
                self.stream_object.add_message_to_out_buff(self.root_address, packet, True)
                self.stream_object.send_out_buf_messages()
            elif(self.is_root == True):
                for i in range(1, len(self.networkgraph_object.nodes)):
                    if(time.time() - self.networkgraph_object.nodes[i].lastunion >= 36):
                        print("node" + str(self.networkgraph_object.nodes[i].address) + "should be removed")
                        self.networkgraph_object.turn_off_node(self.networkgraph_object.nodes[i].address)

        """

        In this function, we will handle all Reunion actions.

        Code design suggestions:
            1. Check if we are the network root or not; The actions are identical.
            2. If it's the root Peer, in every interval check the latest Reunion packet arrival time from every node;
               If time is over for the node turn it off (Maybe you need to remove it from our NetworkGraph).
            3. If it's a non-root peer split the actions by considering whether we are waiting for Reunion Hello Back
               Packet or it's the time to send new Reunion Hello packet.

        Warnings:
            1. If we are the root of the network in the situation that we want to turn a node off, make sure that you will not
               advertise the nodes sub-tree in our GraphNode.
            2. If we are a non-root Peer, save the time when you have sent your last Reunion Hello packet; You need this
               time for checking whether the Reunion was failed or not.
            3. For choosing time intervals you should wait until Reunion Hello or Reunion Hello Back arrival,
               pay attention that our NetworkGraph depth will not be bigger than 8. (Do not forget main loop sleep time)
            4. Suppose that you are a non-root Peer and Reunion was failed, In this time you should make a new Advertise
               Request packet and send it through your register_connection to the root; Don't forget to send this packet
               here, because in the Reunion Failure mode our main loop will not work properly and everything will be got stock!

        :return:
        """
        pass
# Broadcasting is implemented directly in handle_user_interface_buffer (SendMessage command).
    def send_broadcast_packet(self, broadcast_packet):
        """

        For setting broadcast packets buffer into Nodes out_buff.

        Warnings:
            1. Don't send Message packets through register_connections.

        :param broadcast_packet: The packet that should be broadcast through the network.
        :type broadcast_packet: Packet

        :return:
        """
        pass

    def handle_packet(self, packet):
        type = int(packet.get_type())
        if (type == 1 and self.condition == True):
            self.__handle_register_packet(packet)
        if (type == 2):
            self.__handle_advertise_packet(packet)
        if (type == 3 and self.condition == True):
            self.__handle_join_packet(packet)
        if (type == 4) and self.condition == True:
            self.__handle_message_packet(packet)
        if (type == 5 and self.condition == True):
            self.__handle_reunion_packet(packet)
        type = 0
        """

        This function act as a wrapper for other handle_###_packet methods to handle the packet.

        Code design suggestion:
         //   1. It's better to check packet validation right now; For example Validation of the packet length.

        :param packet: The arrived packet that should be handled.

        :type packet Packet

        """
        pass

    def __check_registered(self, source_address):
        bool = False
        if self.is_root == True:
            for i in range(len(self.stream_object.Nodes)):
                if self.stream_object.Nodes[i].get_server_address() == source_address:
                    bool = True

                    return True
            if(bool == False):
                return False

        """
        If the Peer is the root of the network we need to find that is a node registered or not.

        :param source_address: Unknown IP/Port address.
        :type source_address: tuple

        :return:
        """
        pass

    def __handle_advertise_packet(self, packet):
        body = packet.get_body()
        res = body[:3]
        if self.is_root == False:
            if res == "RES":
                print("we got a response advertise so we should join to the address given , we make a join packet")
                jointuple = (body[3:18], int(body[18:23]))
                self.stream_object.add_node(jointuple, False)
                self.father_address = jointuple
                packet = self.packetFactory_object.new_join_packet(self.tuple)
                self.stream_object.add_message_to_out_buff(jointuple, packet, False)
                self.lastuninonback = time.time()
                self.condition = True
                self.mode = 0
                self.is_first_advertised = True
        else:
            if res == "REQ":
                tuple = packet.get_source_server_address()
                if(self.__check_registered(tuple) == True):
                    father = self.networkgraph_object.find_live_node(tuple)
                    if(father is not None):
                        print("we find a live node " + "the father is " + str(father) + " the child is " + str(tuple))
                        packet = PacketFactory.new_advertise_packet("response", (self.server_ip, self.server_port), father)
                        self.stream_object.add_message_to_out_buff(tuple, packet,True)


        """
        For advertising peers in the network, It is peer discovery message.

        Request:
            We should act as the root of the network and reply with a neighbour address in a new Advertise Response packet.

        Response:
            When an Advertise Response packet type arrived we should update our parent peer and send a Join packet to the
            new parent.

        Code design suggestion:
            1. Start the Reunion daemon thread when the first Advertise Response packet received.
            2. When an Advertise Response message arrived, make a new Join packet immediately for the advertised address.

        Warnings:
            1. Don't forget to ignore Advertise Request packets when you are a non-root peer.
            2. The addresses which still haven't registered to the network can not request any peer discovery message.
            3. Maybe it's not the first time that the source of the packet sends Advertise Request message. This will happen
               in rare situations like Reunion Failure. Pay attention, don't advertise the address to the packet sender
               sub-tree.
            4. When an Advertise Response packet arrived update our Peer parent for sending Reunion Packets.

        :param packet: Arrived register packet

        :type packet Packet

        :return:
        """
        pass

    def __handle_register_packet(self, packet):
        server_tuple = packet.get_source_server_address()
        if self.is_root == True:
            if(self.__check_registered(server_tuple) == False):
                self.stream_object.add_node(server_tuple, True)
                reg_res = self.packetFactory_object.new_register_packet("response",self.tuple)
                self.stream_object.add_message_to_out_buff(server_tuple,reg_res,True)
                print("node " + str(server_tuple) + " is registered")
        else:
            if(server_tuple == self.root_address):
                body = packet.get_body()
                ack = body[3:6]
                if(ack == "ACK"):
                    self.is_registered = True
                    self.a.start()
                    print("we are registered")


        """
        For registration a new node to the network at first we should make a Node with stream.add_node for'sender' and
        save it.

        Code design suggestion:
            1.For checking whether an address is registered since now or not you can use SemiNode object except Node.

        Warnings:
            1. Don't forget to ignore Register Request packets when you are a non-root peer.

        :param packet: Arrived register packet
        :type packet Packet
        :return:
        """
        pass

    def __check_neighbour(self, address):
        """
        It checks is the address in our neighbours array or not.

        :param address: Unknown address

        :type address: tuple

        :return: Whether is address in our neighbours or not.
        :rtype: bool
        """
        pass

    def __handle_message_packet(self, packet):
        src = packet.get_source_server_address()
        packet = self.packetFactory_object.new_message_packet(packet.get_body(), self.tuple)
        packett = Packet(packet)
        print("message : " + packett.get_body() + self.server_ip + str(self.server_port))
        for i in range(len(self.stream_object.Nodes)):
            if(src != self.stream_object.Nodes[i].get_server_address() and self.stream_object.Nodes[i].is_register_connection == False):
                self.stream_object.add_message_to_out_buff(self.stream_object.Nodes[i].get_server_address(), packet,False)

            '''
            ted = 0
            for i in range(len(self.stream_object.Nodes)):
                if self.stream_object.Nodes[i].get_server_address == self.root_address:
                    ted += 1
            if(ted == 1):
                for i in range(len(self.stream_object.Nodes)):
                    if (src != self.stream_object.Nodes[i].get_server_address and self.root_address != self.stream_object.Nodes[i].get_server_address):
                        self.stream_object.add_message_to_out_buff(self.stream_object.Nodes[i].get_server_address, packet)
            else:
                for i in range(len(self.stream_object.Nodes)):
                    if(src != self.stream_object.Nodes[i].get_server_address and self.stream_object.Nodes[i].is_register_connection == False):
                        self.stream_object.add_message_to_out_buff(self.stream_object.Nodes[i].get_server_address, packet)
            '''




        """
        Only broadcast message to the other nodes.

        Warnings:
           /// 1. Do not forget to ignore messages from unknown sources.
            2. Make sure that you are not sending a message to a register_connection.

        :param packet: Arrived message packet

        :type packet Packet

        :return:
        """
        pass

    def __handle_reunion_packet(self, packet):
        body = packet.get_body()
        res = body[:3]
        if(self.is_root == False):
            if(res == "REQ"):
                path = body[5:]
                packet = PacketFactory.new_reunion_packet("request", self.tuple, path, False)
                self.stream_object.add_message_to_out_buff(self.father_address, packet,False)
            else:
                if(len(body) == 25):
                    if(body[5:20] == self.server_ip and int(body[20:25]) == self.server_port):
                        self.lastuninonback = time.time()
                        self.mode = 0
                else:
                    path = body[5:]
                    packet = PacketFactory.new_reunion_packet("response", self.tuple, path, False)
                    packett = Packet(packet)
                    new_body = packett.get_body()
                    tuple = (new_body[5:20], int(new_body[20:25]))
                    self.stream_object.add_message_to_out_buff(tuple, packet,False)
        else:
            if(res == "REQ"):
                path = body[5:]
                tuple = packet.get_source_server_address()
                leng = packet.get_length()
                packet = PacketFactory.new_reunion_packet("response", self.tuple, path, True)
                src = (body[leng - 20: leng - 5], int(body[leng - 5:]))
                #print(new_body)

                for i in range(len(self.networkgraph_object.nodes)):
                    if(src == self.networkgraph_object.nodes[i].address):
                        self.networkgraph_object.nodes[i].lastunion = time.time()
                        break
                print("node " + str(src) + " is in the network")
                self.stream_object.add_message_to_out_buff(tuple, packet,False)






        """
        In this function we should handle Reunion packet was just arrived.

        Reunion Hello:
            If you are root Peer you should answer with a new Reunion Hello Back packet.
            At first extract all addresses in the packet body and append them in descending order to the new packet.
            You should send the new packet to the first address in the arrived packet.
            If you are a non-root Peer append your IP/Port address to the end of the packet and send it to your parent.

        Reunion Hello Back:
            Check that you are the end node or not; If not only remove your IP/Port address and send the packet to the next
            address, otherwise you received your response from the root and everything is fine.

        Warnings:
            1. Every time adding or removing an address from packet don't forget to update Entity Number field.
            2. If you are the root, update last Reunion Hello arrival packet from the sender node and turn it on.
            3. If you are the end node, update your Reunion mode from pending to acceptance.


        :param packet: Arrived reunion packet
        :return:
        """
        pass

    def __handle_join_packet(self, packet):
        src = packet.get_source_server_address()
        self.stream_object.add_node(src, False)
        print(" we add this node ")
        """
        When a Join packet received we should add a new node to our nodes array.
        In reality, there is a security level that forbids joining every node to our network.

        :param packet: Arrived register packet.
        :type packet Packet

        :return:
        """
        pass


# Not needed: neighbour selection happens in __handle_advertise_packet when the root receives an Advertise request.



    def __get_neighbour(self, sender):
        """
        Finds the best neighbour for the 'sender' from the network_nodes array.
        This function only will call when you are a root peer.

        Code design suggestion:
            1. Use your NetworkGraph find_live_node to find the best neighbour.

        :param sender: Sender of the packet
        :return: The specified neighbour for the sender; The format is like ('192.168.001.001', '05335').
        """
        pass
    def parse_port(self, port):
        return str(int(port)).zfill(5)