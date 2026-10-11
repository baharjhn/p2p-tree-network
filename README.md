# P2P Tree Network

A peer-to-peer messaging network in Python, built for the **Computer Networks** course at **Sharif University of Technology** (Fall 2018). Peers join through a root node, organize themselves into a **binary tree** and broadcast messages across it. A custom **binary packet protocol** runs over TCP sockets, and a **heartbeat ("Reunion") mechanism** detects failed nodes so the network can heal itself.

## How it works

```
                 root (5356)
                /            \
        peer (31318)      peer (31319)
          /      \            /     \
        ...      ...        ...     ...
```

1. **Register:** a new peer sends a Register request to the root, which records it.
2. **Advertise (peer discovery):** the peer asks the root for a place in the tree. The root runs a breadth-first search over its `NetworkGraph` to find the first live node with fewer than 2 children, and returns that node as the new parent.
3. **Join:** the peer connects to its new parent.
4. **Message:** a message is broadcast to all tree neighbours, and each peer forwards it to everyone except the sender. Messages never go over the register connection to the root.
5. **Reunion (heartbeat):** every peer periodically sends a Reunion "Hello" up the tree to the root, which replies with a "Hello Back" down the same path.
   - **Root side:** if the root hears nothing from a node for 36 seconds, it turns that node off and stops advertising it as a parent.
   - **Peer side:** if a peer gets no reply in time, it drops its parent and sends a new Advertise request to rejoin the tree.

## Packet format

Every packet has a 20-byte header followed by a body:

| Field | Size | Notes |
|---|---|---|
| Version | 2 bytes | Always 1 |
| Type | 2 bytes | 1 Register, 2 Advertise, 3 Join, 4 Message, 5 Reunion |
| Length | 4 bytes | Body length |
| Source server IP | 8 bytes | 4 × 2-byte parts |
| Source server port | 4 bytes | |
| Body | variable | Type-specific (e.g. `REQ`/`RES` + addresses, or the message text) |

The full specification is in the docstring at the top of [`src/Packet.py`](src/Packet.py).

## Project structure

```
src/
├── Main.py            # Entry point: start a root or client peer
├── Peer.py            # Peer logic: command handling, packet handlers, Reunion daemon
├── Packet.py          # Packet class and PacketFactory (binary encoding/decoding)
├── Stream.py          # TCP server and outgoing connections for a peer
├── UserInterface.py   # Thread that reads user commands
└── tools/
    ├── NetworkGraph.py   # Root's view of the tree (BFS parent selection, node on/off)
    ├── Node.py           # A connection to another peer with its outgoing buffer
    ├── SemiNode.py       # IP/port formatting helpers
    └── simpletcp/        # Small TCP socket library (provided with the course, lightly modified)
```

## Running it

Requirements: Python 3.6+ (no external packages).

Start each peer in its own terminal, from the repository root:

```bash
# Terminal 1: the root
python -m src.Main --root --port 5356

# Terminal 2 and 3: two clients
python -m src.Main --port 31318 --root-port 5356
python -m src.Main --port 31319 --root-port 5356
```

Then type these commands in a client terminal:

| Command | What it does |
|---|---|
| `Register` | Register with the root |
| `Advertise` | Ask the root for a parent and join the tree |
| `Sendmessage <text>` | Broadcast a message through the network |

I tested this setup locally with one root and two clients: both clients registered, joined the tree under the root, exchanged Reunion heartbeats, and a broadcast message reached the root.

## Team

Group project by **Bahar Jahani** and **Amirreza Kazemi**, Computer Networks course, Sharif University of Technology, Fall 2018.

## About this project

The course staff provided the project skeleton: class and method signatures, with docstrings describing the expected behaviour and the packet format. The implementation of the peer logic, packet encoding and decoding, the network graph and the Reunion mechanism is ours.

Before publishing, I:

- removed IDE files and compiled caches;
- recovered `UserInterface.py` and `tools/SemiNode.py` from their compiled bytecode, because the source files were damaged in the archive;
- replaced the original `Main.py`, which created two peers in one process, with a command-line entry point;
- translated two code comments into English.

This is course code, kept close to the original submission.
