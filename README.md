# SuperSimpleMH
### Diablo 2 Resurrected map directions. A tool which direct to key points in the game map.
#### SuperSimpleMH is intended for informational and educational purposes only. By using this tool online you take the risk of being banned.

## Requirements
* Diablo 2 lod version 1.13c
* python 3.11 32-bit version
* python 3.11 64-bit version
* pyMeow module - https://github.com/qb-0/pyMeow

## Setup
* install python 3.11 32-bit version
* install python 3.11 64-bit version
* download diablo 2 lod version 1.13c, you can download from here https://www.mediafire.com/file/3x7g0nuph242mu1/game.zip/file
* download SuperSimpleMH.zip from the releases
* download pyMeow module (from releases) to the project folder
* open settings.toml (in rpyc-d2-map-api folder), write the absolute path of diablo 2 lod folder that you've just downloaded
<<<<<<< HEAD
* from rpyc-d2-map-api directory open command shell prompt and run the commands:
  * py -3.11-32 -m venv venv
  * .\venv\Scripts\activate"
  * pip install .
* from the project directory (SuperSimpleMH folder) open a command shell prompt and run the commands:
  * py -3.11-64 -m venv venv
  * .\venv\Scripts\activate
  * pip install .

## Usage
* to use SuperSimpleMH take the following steps:
  * start D2R
  * from the project directory (SuperSimpleMH folder) open a command shell prompt and run the commands:
    * .\venv\Scripts\activate
    * super_simple_mh
=======
* from the project directory open a command shell prompt and run "python tools\build.py"
* run "\venv\Scripts\activate"
* run "super_simple_mh"
>>>>>>> e7cff1c89a5c16b4e3742397a620d157b0a78821

## Features
* map directions to adjacent levels and mazes.
* map overlay
* drawing monster and their immunities
* drawing super uniques, uniques and champions
* drawing merc and player minions
* drawing hostile players and their life
* display other players stats
* display other players inventory

## SuperSimpleMH Features Usage
* display other players inventory - hover over a player and press insert. press pgup to view items on switch
* display other players stats - hover over a player and press pgdn.

## Credits
* [mapview](https://github.com/joffreybesos/d2r-mapview) @joffreybesos for rustdecrypt and many more.
* MapAssit @OneXDeveloper @ItzRabbs
* [d2mapapi](https://github.com/jcageman/d2mapapi)


LowerKurast                |  Catacombs
:-------------------------:|:-------------------------:
![plot](./LowerKurast.png)  |  ![plot](Catacombs.png)

Show Inventory             |  Show Stats
:-------------------------:|:-------------------------:
![plot](./ShowInventory.png)  |  ![plot](./ShowStats.png)
