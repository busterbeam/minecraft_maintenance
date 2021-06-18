# Minecraft Maintenance 
This will manage updating, backups, archiving and prompting your server.

[**`AGPL License`**](LICENSE)
**`INCOMPLETE`**

## Updating
Updating at the present time only utalizes papermc, as this was built for a papermc server.  I do plan to add other server software support, but don't intend to test each.  It has access to a restore function and temporary backuping so if an update doesn't work it will promptly revert the server.  It will also start and stop the server for you when needed, even if the server wasn't running in the first place
 - [ ] **`Mojang`**
 - [ ] **`Spigot`**
 - [ ] **`Bukkit`**
 - [x] **`PaperMC`**
 - [ ] **`Frabic`**
 - [ ] **`Forge`**

## Plugin, Datapack & Resource Specific Updating (maybe Java update)
I imagine some of these things could be completed by some other system, but by integrating it all into this one program it can probably reduce that number of server "restarts", and for things not covered by some other system.  Java updating, minecraft runs on Java why not make sure Java is up to date? and as this system is written in python it is not affected by Java.

## Backuping
This system has a smart backup system at it's core that allows you to make snapshot backups without using huge amounts of permanent storage space, but also faster backing up.  The system relies symbolic links (shortcuts) to help maintain sanity when trying to restore files. I have plans to add byte differencing comparing files changes at a binary level, but I imagine not much will be yielded from this

## Archiving
Archiving with this system allows you to produce more solid backups or easier world downloads.  Seperate to the backup system, you can make it send your world to a webpage
for your players to download, but also remove sensitive files from the system before archiving.  Archiving may be helpful if you want to build a tertiary backup system that sits off your computer, especially if you have tape drives and the such

## Prompting
Prompting is essentialy all these process sending messages into the game server so when players are online they can know there is a backup in progress or an update may be installed soon.  It will utalize the Boss Bar, title's, and actionbar when prompting instead of flooding the user chat window.

## Configuration
This system utalizes an ini file for user prefernces, this is found in `minecraft_maintanence/config.ini`

## Usage
Usage would simply be `python3 minecraft_maintanence` which could be placed inside crontab (linux) `@reboot python3 path_to_server/minecraft_maintanence`.  But you also want to add how often you want the script to run as minecraft_maintanence stops once it's finished updating, backing up etc... so your config.ini might state backup every hour but if it runs once a day it won't do anything so you must schedule it to run once an hour at least and it will maintain the rest.  partially setup like this because if you want to restore you would do `python3 minecraft_maintanence latest`.  Also to ensure low power/performance requirements

## Discord Bot
Minecraft Servers usually have discord servers, maybe make the maintenance software perpetually alive and if players request for update_checks, world_restore and anything else through the relevant discord channel then the it will happen.  Too make this happen I will need to change how the server is initiated, probably use `subprocess.Popen()`.  This will also be helpful to allow other server operators, to add more functionality from inside the game, as I might be able to add download requests to plugins, datapacks, resourece packs etc...




