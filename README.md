# hamlogger
Amateur radio contact logger

This is inteded to be a python based console logger for ham radio contacts.
I haven't been able to find a console logger that I actually liked, so
I started this one for myself.

## Current Status

This is in the very early stages. There is still a great deal of work that
needs to be done. Right now the interface is very simple. I am not sure if
I will leave it this way or move to some sort of curses interface. I want it to
be quick and easy to interact with so it can be used remotely over for example
ssh, but powerful enough to do everything I need for logging contacts. Right
now all testing is being done on OSX and Linux. Windows may have to wait a
while... Though anyone else is welcome to see if they can get it working there!

Additionally, this is a bit of side project, so I don't know how much time
I will actually devote to it, but hopefully I can get some of the desired
features added over time.

## TODO:
Just about everything

* Autofill RSTs
    - SSB vs CW etc
* More error checking
* frequency parsing of some kind
* fill band based on frequency
* Additional inline history reporting for logged contacts
* Possible webscraper for contact information (?)
* Add logfile converter
* sqlite vs json (?)
* set up config file
* auto build config file and directories
* other...
