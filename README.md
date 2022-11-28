# PiTunes :saxophone:
PiTunes is Raspberry Pi interface to display data on your Spotify listening.  
  
The GUI displays your top three artists and top three songs of the last week (refreshing weekly). The data is then stored in a MySQL database (of your configuration) to store listening statistics over time. LastFM and Spotify APIs are used in tandem to retrieve the necessary info.  

## :high_brightness: Images

### Implementation

<img width="500" alt="interface" src="https://user-images.githubusercontent.com/41372799/204268602-99e240a8-bf9b-480f-8997-af0d93ca844d.jpg">

### GUI

![newgui](https://user-images.githubusercontent.com/41372799/200444761-5a4ea4de-d721-4417-aa74-f063b46428aa.JPG)

### Refresh screen

![2img](https://user-images.githubusercontent.com/41372799/199851064-65ebe811-c634-46af-9b97-28cf13776e50.jpg)



## :cyclone: Requirements
The following are needed to set up the project as shown:
* Raspberry Pi
* **1024x600 screen**
  * GUI is only fit for the 1024x600 screen I have with my Raspberry Pi. However, this resolution is fairly standard for aftermarket RPi displays.
* [Spotify web API keys](https://developer.spotify.com/documentation/web-api/)
* [LastFM web API keys](https://www.last.fm/api)
* (OPTIONAL): MySQL installation with a database created to store weekly data in
  * If you wish to store your weekly data in a MySQL database, the code is implemented
  * Otherwise, it can be commented out

Once you have these, you will need to enter your unique keys / account passwords in the corresponding variables in the code. These are clearly labelled. 

## :snake: Setup 
The project is two scripts (Tkinter windows) that run simultaneously. This is so that when the GUI closes to refresh weekly, the refresh screen will already be running and displayed in the window underneath. There is most definitely a better way to do this, but I couldn't get it to work the way I wanted.

1. Enter your keys/passwords/database info into the code
2. Ensure your file path is correctly setup - `PiTunes.py` and `refresh.py` should be contained within the main folder, along with an 'assets' folder containing the necessary images
3. Open a terminal from the folder and run:
    * `python refresh.py`
4. Tab out and open a separate terminal to run:
    * `python PiTunes.py`
5. Tab the windows such that gui is laid over the refresh window 


## :rocket: Future improvements
Some things I'd like to add to what I have so far:
* Compatability with different resolutions
* A more interactive interface 
  * A button to see statistics over time 
  * Scrolling text / an updating feed 
* A better way to deal with the refresh screen
* Different ways of storing data over time
* Need to implement better error catching, if connection errors occur
