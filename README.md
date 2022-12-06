# PiTunes :saxophone:
PiTunes is Raspberry Pi interface to display data on your Spotify listening.  
  
The software displays your top three artists and top three songs of the last week, refreshing weekly. The data is then stored in a MySQL database (of your configuration) to store listening statistics over time. LastFM and Spotify APIs are used in tandem to retrieve the necessary info.  

## :high_brightness: Images

### Implementation

<img width="600" alt="interface" src="https://user-images.githubusercontent.com/41372799/204268602-99e240a8-bf9b-480f-8997-af0d93ca844d.jpg"> <img width="600" alt="interface" src="https://user-images.githubusercontent.com/41372799/204269091-bd15431c-787f-4078-8942-9dc08c8101f5.jpg">

### GUI

<img width="700" alt="interface" src="https://user-images.githubusercontent.com/41372799/204553427-38bc9abc-2863-4291-9397-f3e7b2acc661.JPG">

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
3. Install all the necessary packages
4. Open a terminal from the folder and run:
    * `python refresh.py`
5. Tab out and open a separate terminal to run:
    * `python PiTunes.py`
6. Tab the windows such that gui is laid over the refresh window 

## :anger: Challenges
* I honestly don't remember how I got this idea, nor how I figured it would be possible. Every step of the way was just constant challenges, so I won't list all them here. For every one thing I figured out, two more problems came up. That being said, it was a lot of fun
* Designing the interface was painstaking. Actually creating something that looked aesthetically pleasing took long enough, and then making pixel-by-pixel adjustments to each and every widget was the nail in the coffin
* Originally I intended to only use the Pylast package to get Spotify listening data, but later found out it doesn't really support fetching album/cover art for songs. Luckily I found Spotipy, a package that works with the Spotify API. That meant I was able to take the info from LastFM and run it through a search function with the Spotify artwork to find the corresponding cover art for the song or artist
* That being said, both these packages had little to no useful documentation which meant I had to scroll through a ton of old forum posts and sometimes even the source code to try and figure out which functions do what and what parameters they take. The same was true for the package I used to get a MySQL database connection working to my PC
* If there was a better/simple way to round image corners, I couldn't find it
* I won't even talk about the refresh screen. It felt like I spent forever and still couldn't figure out a way to get it to work the way it should. Eventually I settled on the shoddy implementation of making it it's own program that runs in the background, so it'll automatically come up when the main script does its automatic close-and-refresh.
* Finally, I had the code working the way I wanted on my PC. Putting it on the Raspberry Pi was a totally different game. Once I actually saw the way it was going to be physically implemented, I had to make so many changes for things I just hadn't accounted for when it was only something I was programming in a terminal on my laptop


## :rocket: Future improvements
Some things I'd like to add to what I have so far:
* Compatability with different resolutions
* A more interactive interface 
  * A button to see statistics over time 
  * Scrolling text / an updating feed 
* A better way to deal with the refresh screen
* Different ways of storing data over time
* Need to implement better error catching, if connection errors occur
* UPDATE: there is an error with song names that contain certain special characters. This won't take long to fix, I just have to add some special cases
