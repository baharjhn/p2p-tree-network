"""

    This is the format of packets in our network:
    


                                                **  NEW Packet Format  **
     __________________________________________________________________________________________________________________
    |           Version(2 Bytes)         |         Type(2 Bytes)         |           Length(Long int/4 Bytes)          |
    |------------------------------------------------------------------------------------------------------------------|
    |                                            Source Server IP(8 Bytes)                                             |
    |------------------------------------------------------------------------------------------------------------------|
    |                                           Source Server Port(4 Bytes)                                            |
    |------------------------------------------------------------------------------------------------------------------|
    |                                                    ..........                                                    |
    |                                                       BODY                                                       |
    |                                                    ..........                                                    |
    |__________________________________________________________________________________________________________________|

    Version:
        For now version is 1
    
    Type:
        1: Register
        2: Advertise
        3: Join
        4: Message
        5: Reunion
                e.g: type = '2' => Advertise packet.
    Length:
        This field shows the character numbers for Body of the packet.

    Server IP/Port:
        We need this field for response packet in non-blocking mode.



    ***** For example: ******

    version = 1                 b'\x00\x01'
    type = 4                    b'\x00\x04'
    length = 12                 b'\x00\x00\x00\x0c'
    ip = '192.168.001.001'      b'\x00\xc0\x00\xa8\x00\x01\x00\x01'
    port = '65000'              b'\x00\x00\\xfd\xe8'
    Body = 'Hello World!'       b'Hello World!'

    Bytes = b'\x00\x01\x00\x04\x00\x00\x00\x0c\x00\xc0\x00\xa8\x00\x01\x00\x01\x00\x00\xfd\xe8Hello World!'




    Packet descriptions:
    
        Register:
            Request:
        
                                 ** Body Format **
                 ________________________________________________
                |                  REQ (3 Chars)                 |
                |------------------------------------------------|
                |                  IP (15 Chars)                 |
                |------------------------------------------------|
                |                 Port (5 Chars)                 |
                |________________________________________________|
                
                For sending IP/Port of the current node to the root to ask if it can register to network or not.

            Response:
        
                                 ** Body Format **
                 _________________________________________________
                |                  RES (3 Chars)                  |
                |-------------------------------------------------|
                |                  ACK (3 Chars)                  |
                |_________________________________________________|
                
                For now only should just send an 'ACK' from the root to inform a node that it
                has been registered in the root if the 'Register Request' was successful.
                
        Advertise:
            Request:
            
                                ** Body Format **
                 ________________________________________________
                |                  REQ (3 Chars)                 |
                |________________________________________________|
                
                Nodes for finding the IP/Port of their neighbour peer must send this packet to the root.

            Response:

                                ** Packet Format **
                 ________________________________________________
                |                RES(3 Chars)                    |
                |------------------------------------------------|
                |              Server IP (15 Chars)              |
                |------------------------------------------------|
                |             Server Port (5 Chars)              |
                |________________________________________________|
                
                Root will response Advertise Request packet with sending IP/Port of the requester peer in this packet.
                
        Join:

                                ** Body Format **
                 ________________________________________________
                |                 JOIN (4 Chars)                 |
                |________________________________________________|
            
            New node after getting Advertise Response from root must send this packet to the specified peer
            to tell him that they should connect together; When receiving this packet we should update our
            Client Dictionary in the Stream object.


            
        Message:
                                ** Body Format **
                 ________________________________________________
                |             Message (#Length Chars)            |
                |________________________________________________|

            The message that want to broadcast to hole network. Right now this type only includes a plain text.
        
        Reunion:
            Hello:
        
                                ** Body Format **
                 ________________________________________________
                |                  REQ (3 Chars)                 |
                |------------------------------------------------|
                |           Number of Entries (2 Chars)          |
                |------------------------------------------------|
                |                 IP0 (15 Chars)                 |
                |------------------------------------------------|
                |                Port0 (5 Chars)                 |
                |------------------------------------------------|
                |                 IP1 (15 Chars)                 |
                |------------------------------------------------|
                |                Port1 (5 Chars)                 |
                |------------------------------------------------|
                |                     ...                        |
                |------------------------------------------------|
                |                 IPN (15 Chars)                 |
                |------------------------------------------------|
                |                PortN (5 Chars)                 |
                |________________________________________________|
                
                In every interval (for now 20 seconds) peers must send this message to the root.
                Every other peer that received this packet should append their (IP, port) to
                the packet and update Length.

            Hello Back:
        
                                    ** Body Format **
                 ________________________________________________
                |                  REQ (3 Chars)                 |
                |------------------------------------------------|
                |           Number of Entries (2 Chars)          |
                |------------------------------------------------|
                |                 IPN (15 Chars)                 |
                |------------------------------------------------|
                |                PortN (5 Chars)                 |
                |------------------------------------------------|
                |                     ...                        |
                |------------------------------------------------|
                |                 IP1 (15 Chars)                 |
                |------------------------------------------------|
                |                Port1 (5 Chars)                 |
                |------------------------------------------------|
                |                 IP0 (15 Chars)                 |
                |------------------------------------------------|
                |                Port0 (5 Chars)                 |
                |________________________________________________|

                Root in an answer to the Reunion Hello message will send this packet to the target node.
                In this packet, all the nodes (IP, port) exist in order by path traversal to target.
            
    
"""
import struct
from struct import *
from src.tools.Node import Node


class Packet:
    def __init__(self, buf):
        self.buf = buf
        self.header = self.buf[:20]

        """
        The decoded buffer should convert to a new packet.

        :param buf: Input buffer was just decoded.
        :type buf: bytearray
        """
        pass

    def get_header(self):
        return self.header
        """

        :return: Packet header
        :rtype: str
        """
        pass

    def get_version(self):
        return int.from_bytes(self.header[:2], byteorder='big')

        """

        :return: Packet Version
        :rtype: int
        """
        pass

    def get_type(self):
        return int.from_bytes(self.header[2:4], byteorder='big')

        """

        :return: Packet type
        :rtype: int
        """
        pass

    def get_length(self):
        return int.from_bytes(self.header[4:8], byteorder='big')
        """

        :return: Packet length
        :rtype: int
        """
        pass

    def get_body(self):
        return "".join(map(chr, self.buf[20:]))

        """

        :return: Packet body
        :rtype: str
        """
        pass

    def get_buf(self):
        return self.buf
        """
        In this function, we will make our final buffer that represents the Packet with the Struct class methods.

        :return The parsed packet to the network format.
        :rtype: bytearray
        """
        pass

    def get_source_server_ip(self):
        a = list()
        a.append(0)
        a.append(0)
        a.append(0)
        a.append(0)
        a[0], a[1], a[2], a[3] = struct.unpack_from(">HHHH", self.header[8:16])
        for i in range(4):
            if(a[i] < 10):
                a[i] = "0" + "0" + str(a[i])
            elif(a[i] < 100):
                a[i] = "0" + str(a[i])
            else:
                a[i] = str(a[i])
        source_ip = a[0] + a[1] + a[2] + a[3]
        #source_ip = int.from_bytes(self.header[8:16], byteorder='big')  # formate asli
        #source_ip = str(source_ip)
        return Node.parse_ip(source_ip)
        """
        :return: Server IP address for the sender of the packet.
        :rtype: str
        """
        pass

    def get_source_server_port(self):
        return int.from_bytes(self.header[16:20], byteorder='big')
        """

        :return: Server Port address for the sender of the packet.
        :rtype: str
        """
        pass

    def get_source_server_address(self):
        address_tuple = (self.get_source_server_ip(), self.get_source_server_port())
        return address_tuple
        """

        :return: Server address; The format is like ('192.168.001.001', '05335').
        :rtype: tuple
        """
        pass


class PacketFactory:
    """
    This class is only for making Packet objects.
    """

    @staticmethod
    def parse_buffer(buffer):

        return Packet(buffer)
        """
        In this function we will make a new Packet from input buffer with struct class methods.

        :param buffer: The buffer that should be parse to a validate packet format

        :return new packet
        :rtype: Packet

        """
        pass

    @staticmethod
    def new_reunion_packet(type, source_address, nodes_array_str, is_root = False):
        version = 1
        msg_type = 5
        packet_bytearray = version.to_bytes(2, byteorder='big')
        packet_bytearray += msg_type.to_bytes(2, byteorder='big')
        ip, port = source_address
        header_port = int(port)
        #header_ip = Node.reverse_parse_ip(ip)
        if(is_root == False):
            if type == "request":
                length = 3 + 2 + len(nodes_array_str) + 20  # 3req/2NoE/lenNodes/20source
                packet_bytearray += length.to_bytes(4, byteorder='big')
                bodip = ip
                ip = tuple([int(i) for i in ip.split(".")])
                packet_bytearray += ip[0].to_bytes(2, byteorder='big')
                packet_bytearray += ip[1].to_bytes(2, byteorder='big')
                packet_bytearray += ip[2].to_bytes(2, byteorder='big')
                packet_bytearray += ip[3].to_bytes(2, byteorder='big')
                packet_bytearray += header_port.to_bytes(4, byteorder='big')
                packet_bytearray += bytearray(b'REQ')
                NoE = len(nodes_array_str) // 20 + 1
                NoE = "0" + str(NoE)
                packet_bytearray += bytearray(NoE.encode())

                port = Node.parse_port(str(port))
                temp =  bodip + Node.parse_port(str(port)) + nodes_array_str
                body = bytearray(temp.encode())
                packet_bytearray += body
            else:
                length = 3 + 2 + len(nodes_array_str) - 20
                packet_bytearray += length.to_bytes(4, byteorder='big')
                ip = tuple([int(i) for i in ip.split(".")])
                packet_bytearray += ip[0].to_bytes(2, byteorder='big')
                packet_bytearray += ip[1].to_bytes(2, byteorder='big')
                packet_bytearray += ip[2].to_bytes(2, byteorder='big')
                packet_bytearray += ip[3].to_bytes(2, byteorder='big')
                packet_bytearray += header_port.to_bytes(4, byteorder='big')
                packet_bytearray += bytearray(b'RES')
                NoE = len(nodes_array_str) // 20 - 1
                NoE = "0" + str(NoE)
                packet_bytearray += bytearray(NoE.encode())

                temp = nodes_array_str[20:]  ####?
                body = bytearray(temp.encode())
                packet_bytearray += body
        else:
            length = 3 + 2 + len(nodes_array_str)
            packet_bytearray += length.to_bytes(4, byteorder='big')
            ip = tuple([int(i) for i in ip.split(".")])
            packet_bytearray += ip[0].to_bytes(2, byteorder='big')
            packet_bytearray += ip[1].to_bytes(2, byteorder='big')
            packet_bytearray += ip[2].to_bytes(2, byteorder='big')
            packet_bytearray += ip[3].to_bytes(2, byteorder='big')
            packet_bytearray += header_port.to_bytes(4, byteorder='big')
            packet_bytearray += bytearray(b'RES')
            NoE = len(nodes_array_str) // 20
            NoE = "0" + str(NoE)
            packet_bytearray += bytearray(NoE.encode())

            temp = nodes_array_str
            body = bytearray(temp.encode())
            packet_bytearray += body
        print(packet_bytearray)
        return (packet_bytearray)
        """
        :param type: Reunion Hello (REQ) or Reunion Hello Back (RES)
        :param source_address: IP/Port address of the packet sender.
        :param nodes_array: [(ip0, port0), (ip1, port1), ...] It is the path to the 'destination'.

        :type type: str
        :type source_address: tuple
        :type nodes_array: list

        :return New reunion packet.
        :rtype Packet
        """
        pass

    @staticmethod
    def new_advertise_packet(type, source_server_address, neighbour=None):
        version = 1
        msg_type = 2
        packet_bytearray = version.to_bytes(2, byteorder='big')
        packet_bytearray += msg_type.to_bytes(2, byteorder='big')
        ip, port = source_server_address
        ip = tuple([int(i) for i in ip.split(".")])
        port = int(port)
        if type == "request":
            length = 3
            packet_bytearray += length.to_bytes(4, byteorder='big')
            packet_bytearray += ip[0].to_bytes(2, byteorder='big')
            packet_bytearray += ip[1].to_bytes(2, byteorder='big')
            packet_bytearray += ip[2].to_bytes(2, byteorder='big')
            packet_bytearray += ip[3].to_bytes(2, byteorder='big')
            packet_bytearray += port.to_bytes(4, byteorder='big')
            body = bytearray(b'REQ')
            packet_bytearray += body
        else:
            length = 23
            packet_bytearray += length.to_bytes(4, byteorder='big')
            packet_bytearray += ip[0].to_bytes(2, byteorder='big')
            packet_bytearray += ip[1].to_bytes(2, byteorder='big')
            packet_bytearray += ip[2].to_bytes(2, byteorder='big')
            packet_bytearray += ip[3].to_bytes(2, byteorder='big')
            packet_bytearray += port.to_bytes(4, byteorder='big')
            neighbour_ip, neighbour_port = neighbour
            temp = "RES" + neighbour_ip + str(neighbour_port)
            body = bytearray(temp.encode())
            packet_bytearray += body
        print(packet_bytearray)
        return (packet_bytearray)
        """
        :param type: Type of Advertise packet
        :param source_server_address Server address of the packet sender.
        :param neighbour: The neighbour for advertise response packet; The format is like ('192.168.001.001', '05335').

        :type type: str
        :type source_server_address: tuple
        :type neighbour: tuple

        :return New advertise packet.
        :rtype Packet

        """
        pass

    @staticmethod
    def new_join_packet(source_server_address):
        version = 1
        type = 3
        length = 4
        packet_bytearray = version.to_bytes(2, byteorder='big')
        packet_bytearray += type.to_bytes(2, byteorder='big')
        packet_bytearray += length.to_bytes(4, byteorder='big')
        ip, port = source_server_address
        ip = tuple([int(i) for i in ip.split(".")])
        packet_bytearray += ip[0].to_bytes(2, byteorder='big')
        packet_bytearray += ip[1].to_bytes(2, byteorder='big')
        packet_bytearray += ip[2].to_bytes(2, byteorder='big')
        packet_bytearray += ip[3].to_bytes(2, byteorder='big')
        packet_bytearray += port.to_bytes(4, byteorder='big')
        body = bytearray(b'JOIN')
        packet_bytearray += body
        print(packet_bytearray)
        return (packet_bytearray)
        """
        :param source_server_address: Server address of the packet sender.

        :type source_server_address: tuple

        :return New join packet.
        :rtype Packet

        """
        pass

    @staticmethod
    def new_register_packet(type, source_server_address, address=(None, None)):
        version = 1
        msg_type = 1
        packet_bytearray = version.to_bytes(2, byteorder='big')
        packet_bytearray += msg_type.to_bytes(2, byteorder='big')
        ip, port = source_server_address
        ip = tuple([int(i) for i in ip.split(".")])
        port = int(port)
        #ip = Node.reverse_parse_ip(ip)
        if type == "response":
            length = 6
            packet_bytearray += length.to_bytes(4, byteorder='big')
            #ip_int = int(ip)
            #packet_bytearray += ip_int.to_bytes(8, byteorder='big')
            packet_bytearray += ip[0].to_bytes(2, byteorder='big')
            packet_bytearray += ip[1].to_bytes(2, byteorder='big')
            packet_bytearray += ip[2].to_bytes(2, byteorder='big')
            packet_bytearray += ip[3].to_bytes(2, byteorder='big')
            packet_bytearray += port.to_bytes(4, byteorder='big')
            temp = "RES"
            packet_bytearray += bytearray(temp.encode())
            temp = "ACK"
            packet_bytearray += bytearray(temp.encode())
        else:
            length = 23
            packet_bytearray += length.to_bytes(4, byteorder='big')
            #ip_int = int(ip)
            #packet_bytearray += ip_int.to_bytes(8, byteorder ='big')
            packet_bytearray += ip[0].to_bytes(2, byteorder='big')
            packet_bytearray += ip[1].to_bytes(2, byteorder='big')
            packet_bytearray += ip[2].to_bytes(2, byteorder='big')
            packet_bytearray += ip[3].to_bytes(2, byteorder='big')
            packet_bytearray += port.to_bytes(4, byteorder='big')
            address_ip, address_port = address
            temp = "REQ" + address_ip + Node.parse_port(str(address_port))
            body = bytearray(temp.encode())
            packet_bytearray += body

        print(packet_bytearray)
        return packet_bytearray

        """
        :param type: Type of Register packet
        :param source_server_address: Server address of the packet sender.
        :param address: If 'type' is 'request' we need an address; The format is like ('192.168.001.001', '05335').

        :type type: str
        :type source_server_address: tuple
        :type address: tuple

        :return New Register packet.
        :rtype Packet

        """
        pass

    @staticmethod
    def new_message_packet(message, source_server_address):
        version = 1
        type = 4
        message = str(message)
        body = message.encode()
        length = len(body)
        packet_bytearray = version.to_bytes(2, byteorder='big')
        packet_bytearray += type.to_bytes(2, byteorder='big')
        packet_bytearray += length.to_bytes(4, byteorder='big')
        ip, port = source_server_address
        ip = tuple([int(i) for i in ip.split(".")])
        packet_bytearray += ip[0].to_bytes(2, byteorder='big')
        packet_bytearray += ip[1].to_bytes(2, byteorder='big')
        packet_bytearray += ip[2].to_bytes(2, byteorder='big')
        packet_bytearray += ip[3].to_bytes(2, byteorder='big')
        packet_bytearray += port.to_bytes(4, byteorder='big')
        port = int(port)
        packet_bytearray += port.to_bytes(4, byteorder='big')
        packet_bytearray += body
        print(packet_bytearray)
        return packet_bytearray
        """
        Packet for sending a broadcast message to the whole network.

        :param message: Our message
        :param source_server_address: Server address of the packet sender.

        :type message: str
        :type source_server_address: tuple

        :return: New Message packet.
        :rtype: Packet
        """
        pass
