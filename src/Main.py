"""Start one peer of the network. Run each peer in its own terminal.

Examples (from the repository root):
    python -m src.Main --root --port 5356
    python -m src.Main --port 31318 --root-port 5356
"""
import argparse

from src.Peer import Peer


def main():
    parser = argparse.ArgumentParser(description="Start a peer in the P2P tree network.")
    parser.add_argument("--ip", default="127.000.000.001", help="IP of this peer, in 15-character format")
    parser.add_argument("--port", type=int, required=True, help="Server port of this peer")
    parser.add_argument("--root", action="store_true", help="Start this peer as the root of the network")
    parser.add_argument("--root-ip", default="127.000.000.001", help="IP of the root peer (clients only)")
    parser.add_argument("--root-port", type=int, default=5356, help="Port of the root peer (clients only)")
    args = parser.parse_args()

    if args.root:
        Peer(args.ip, args.port, is_root=True)
    else:
        Peer(args.ip, args.port, is_root=False, root_address=(args.root_ip, args.root_port))


if __name__ == "__main__":
    main()
