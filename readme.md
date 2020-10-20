

## Installation

### 1) Clone the repo
Clone this repo somewhere in your development machine

### 2) Install Python
install python version >= 3.7.*

### 3) install dotenv package
Homepage: https://pypi.org/project/python-dotenv/

    pip install -U python-dotenv
    
### 4) copy `d.cmd` to PATH
update path in `d.cmd` to point `d.py` in this directory.

copy `d.cmd` to a folder within PATH


## Usage

First navigate to a project directory which uses **docker-compose**,
then you can use following commands;

**`d u`** UP: starts the project containers in detached mode

**`d d`** DOWN: stops the project containers and clears volumes

**`d r`** RESTART: runs UP and DOWN routines mentioned above

**`d c [command]`** COMMAND: runs specified command in `web` container

**`d s`** SSH: starts SSH session on `web` container

**`d l [options]`** LOGS: shows `web` container logs. [Options here could be used.][1] Options should be written in single quotes.
Example: `d l '-f'`

[1]:https://docs.docker.com/compose/reference/logs/