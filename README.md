
# P2P File Sharing System

A simple peer-to-peer (P2P) file-sharing system implemented in Python. This project allows each peer to act as both a client and a server to share files directly with other peers without relying on a central server.

## Features
- Each peer can act as both a server (to allow others to download files) and a client (to request files from others).
- File transfer is done directly between peers.
- Basic command-line interface for requesting files from other peers.

## Requirements
- Python 3.x

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/p2p-file-sharing.git
cd p2p-file-sharing
```

### 2. Run the Peer Script
Each peer will act as both a server and a client. To start a peer, run:

```bash
python peer.py
```

### 3. Usage

In the terminal, you’ll see a prompt. You can use the following commands to interact with other peers:

#### Commands

1. **Download a File**
   ```
   download <host> <port> <filename>
   ```
   - `<host>`: IP address of the peer you want to download from.
   - `<port>`: The port the peer is listening on (default: `5000`).
   - `<filename>`: Name of the file you want to download.

2. **Exit**
   - Type `exit` to stop the peer.

### Example
Assuming Peer A (server) has a file named `example.txt` that Peer B (client) wants to download:

1. **Start Peer A** on one terminal.
   ```bash
   python peer.py
   ```
   Peer A will be listening on the default port `5000`.

2. **Start Peer B** on another terminal.
   ```bash
   python peer.py
   ```

3. **Request File from Peer A** on Peer B's terminal:
   ```bash
   download <PeerA_IP_Address> 5000 example.txt
   ```

Peer B will download `example.txt` from Peer A.

## Project Structure

```
p2p-file-sharing/
├── peer.py         # The main script for each peer
└── README.md       # Project documentation
```

## Implementation Details

The peer script works in two main modes:
1. **Server Mode**: Each peer starts a server that listens for incoming file requests. If a file exists, the peer sends the file to the requester.
2. **Client Mode**: Each peer can connect to another peer’s server to request a specific file. If the file is found, the peer receives it in chunks and saves it locally.

## Future Enhancements
- Implement file chunking for more efficient downloads.
- Add support for peer discovery in the network.
- Improve error handling and connection stability.
