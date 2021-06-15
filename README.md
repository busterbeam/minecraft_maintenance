# Minecraft Maintenance
This will manage updating, backups, archiving and prompting your server.

## Updating
Updating at the present time only utalizes papermc, as this was built for a papermc server.  I do plan to add other server software support, but don't intend to test each.  It has access to a restore function and temporary backuping so if an update doesn't work it will promptly revert the server.  It will also start and stop the server for you when needed, even if the server wasn't running in the first place

## Backuping
This system has a smart backup system at it's core that allows you to make snapshot backups without using huge amounts of permanent storage space, but also faster backing up.  The system relies symbolic links (shortcuts) to help maintain sanity when trying to restore files.

## Archiving
Archiving with this system allows you to produce more solid backups or easier world downloads.  Seperate to the backup system, you can make it send your world to a webpage
for your players to download, but also remove sensitive files from the system before archiving.  Archiving may be helpful if you want to build a tertiary backup system that sits off your computer, especially if you have tape drives and the such

## Prompting
Prompting is essentialy all these process sending messages into the game server so when players are online they can know there is a backup in progress or an update may be installed soon.  It will utalize the Boss Bar, title's, and actionbar when prompting instead of flooding the user chat window.

This system utalizes an ini file for user prefernces, this is found in minecraft_maintanence/config.ini

Usage would simply be `python3 minecraft_maintanence` which could be placed inside crontab (linux) `@reboot python3 path_to_server/minecraft_maintanence`.
