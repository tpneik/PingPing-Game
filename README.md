# Pong multiplayer

Pong multiplayer is a Table-Tennis game that supports LAN multiplayer (and singleplayer).

* Written in python with pyglet
* Using socket connections to share data with the server

## TODO
* Game pause
* GUI to define server


--FOR WINDOW--
## PREREQUISITE
* install python3
* install pip
* editor (recommend visual studio code)
## Running

Before running anything, clone the repository:
```bash
git clone https://github.com/longtranv/ping-pong-lan-multiplayer-game
cd ping-pong-lan-multiplayer-game
```

### Running server
```bash
pip install pyglet
code src/lib/settings.py # in order to define the server ip and port
python ./src/server.py
```

Alternatively, with [Nix][nix]:
```bash
code src/lib/settings.py # in order to define the server ip and port
nix-shell --pure --run './src/server.py'
```

### Running client
```bash
code src/lib/settings.py # in order to define server connection ip and port
python src/client.py
```

Alternatively, with [Nix][nix]:
```bash
code src/lib/settings.py # in order to define the server ip and port
nix-shell --pure --run './src/client.py'
```


[nix]: https://nixos.org/nix/
