import mysql.connector
import pylast
import datetime
import time
import sys
import spotipy
import urllib.request
import os
import tkinter
import pathlib
from spotipy.oauth2 import SpotifyClientCredentials
from mysql.connector import errorcode
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, PhotoImage, font
from PIL import Image, ImageTk, ImageDraw

# ENTER YOUR INFO HERE:
# ***************************************************************************************************************
sqlUser = ''  # YOUR MYSQL USERNAME (root by default)
sqlPwrd = ''  # YOUR MYQL PASSWORD (root by default)
hostname = ''  # YOUR MYSQL HOSTNAME ('localhost' or IP)
db = ''  # YOUR DATABASE NAME
lfmKey = ''  # YOUR LASTFM API KEY
lfmSecret = ''  # YOUR LASTFM API SECRET
lfmUser = ''  # YOUR LASTFM USERNAME
lfmPwrd = ''  # YOUR LASTFM PASSWORD
spotifyKey = ''  # YOUR SPOTIFY API KEY
spotifySecret = ''  # YOUR SPOTIFY API SECRET
name = ''  # Your name
# ***************************************************************************************************************

size = (70, 70)  # Image size for cover art
parent_path = Path(__file__).parent  # File parent directory


# Used to crop a PIL image into the largest possible square about the center, needed for album/artist images
# Partially sourced from:
# https://note.nkmk.me/en/python-pillow-image-crop-trimming/
def crop_square(img):
    img_width, img_height = img.size
    crop_size = min(img.size)
    return img.crop(((img_width - crop_size) // 2, (img_height - crop_size) // 2,
                     (img_width + crop_size) // 2, (img_height + crop_size) // 2))


# (Roughly) adds rounded corners to an image
# Sourced from:
# https://stackoverflow.com/questions/11287402/how-to-round-corner-a-logo-without-white-backgroundtransparent-on-it-using-pi
def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


# Rerun weekly
while True:

    # --------------------------------------------------------------------------------------------------------------
    # MySQL connection
    # --------------------------------------------------------------------------------------------------------------

    # Attempt connection
    try:
        conn = mysql.connector.connect(user=sqlUser, password=sqlPwrd, host=hostname, database=db)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err.msg)
        sys.exit(1)

    # Create the table that all weekly data will be stored in
    cursor = conn.cursor()
    createTable = (
        "CREATE TABLE IF NOT EXISTS ListeningData ("
        "id INT NOT NULL AUTO_INCREMENT,"
        "WeekOf DATE NOT NULL,"
        "TopSong1 VARCHAR(255),"
        "TopSong2 VARCHAR(255),"
        "TopSong3 VARCHAR(255),"
        "TopArtist1 VARCHAR(255),"
        "TopArtist2 VARCHAR(255),"
        "TopArtist3 VARCHAR(255),"
        "PRIMARY KEY (id)"
        ");"
    )
    cursor.execute(createTable)

    # --------------------------------------------------------------------------------------------------------------
    # LastFM & Spotify connections
    # --------------------------------------------------------------------------------------------------------------

    topSongs = []
    topArtists = []
    songImages = []
    artistImages = []
    currentWeek = "'" + str(datetime.datetime.now().date()) + "'"

    # Establish LastFM network connection
    lfmNetwork = pylast.LastFMNetwork(api_key=lfmKey, api_secret=lfmSecret,
                                      username=lfmUser, password_hash=pylast.md5(lfmPwrd))
    user = pylast.User(lfmUser, lfmNetwork)

    # Establish Spotify API connection
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotifyKey, client_secret=spotifySecret))

    # Retrieve and store top 3 tracks
    tracks = user.get_top_tracks(period=pylast.PERIOD_7DAYS, limit=3)
    for track in tracks:
        topSong = "'" + str(track.item.title) + ' - ' + str(track.item.artist) + "'"
        topSongs.append(topSong)
        results = sp.search(q=topSong, limit=1)
        for idx, trackName in enumerate(results['tracks']['items']):
            image = trackName['album']['images'][0]['url']
            songImages.append(image)
    songInfo = [entry.split(' - ') for entry in topSongs]

    # Retrieve and store top 3 artists
    artists = user.get_top_artists(period=pylast.PERIOD_7DAYS, limit=3)
    for artist in artists:
        topArtist = "'" + artist.item.name + "'"
        topArtists.append(topArtist)
        results = sp.search(q='artist:' + topArtist, type='artist')
        artist = results['artists']['items'][0]
        artistImages.append(artist['images'][0]['url'])

    # Download album artwork from the stored URLs
    urllib.request.urlretrieve(f'{artistImages[0]}', 'artist1.png')
    urllib.request.urlretrieve(f'{artistImages[1]}', 'artist2.png')
    urllib.request.urlretrieve(f'{artistImages[2]}', 'artist3.png')
    urllib.request.urlretrieve(f'{songImages[0]}', 'song1.png')
    urllib.request.urlretrieve(f'{songImages[1]}', 'song2.png')
    urllib.request.urlretrieve(f'{songImages[2]}', 'song3.png')

    # Insert data into row in SQL table, identified by the week
    insert_data = (
        "INSERT INTO ListeningData (weekof, topsong1, topsong2, topsong3, topartist1, topartist2, topartist3)"
        f"VALUES (str_to_date({currentWeek}, '%Y-%m-%d'), "
        f"{topSongs[0]}, {topSongs[1]}, {topSongs[2]}, {topArtists[0]}, {topArtists[1]}, {topArtists[2]});"
    )
    cursor.execute(insert_data)

    # Confirm changes & close the connection
    conn.commit()
    conn.close()
    cursor.close()

    # --------------------------------------------------------------------------------------------------------------
    # GUI
    # --------------------------------------------------------------------------------------------------------------

    # Create GUI window
    window = Tk()
    window.geometry("1024x600")
    window.configure(bg="#000000")
    window.config(cursor='none')
    window.attributes('-fullscreen', True)
    canvas = Canvas(window, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=1)
    window.resizable(False, False)

    # Add background, shapes, and designs:
    bg_image = PhotoImage(file=Path(os.path.join(parent_path, "assets", "bg_image.png")))
    bg_image_image = canvas.create_image(512, 300, image=bg_image)
    canvas.create_rectangle(44, 225, 465, 226.75, fill="#FFFFFF", outline="")
    canvas.create_rectangle(555, 225, 978, 226.75, fill="#FFFFFF", outline="")

    # Static text
    canvas.create_text(43, 71, anchor="nw", text=f"You've got some solid music taste, {name}.\n",
                       fill="#FFFFFF", font=("Inter", -43, 'bold', 'italic'))
    canvas.create_text(41, 196, anchor="nw", text="Your top three songs of the last week: ",
                       fill="#FFFFFF", font=("Inter", -23, 'bold'))
    canvas.create_text(552, 196, anchor="nw", text="Your top three artists of the last week: ",
                       fill="#FFFFFF", font=("Inter", -23, 'bold'))

    # Song 1 title
    song_1_title = songInfo[0][0].replace("'", "")
    if len(song_1_title) > 28:
        song_1_title = song_1_title[0:25] + "..."
    canvas.create_text(172, 266, anchor="nw", text=f"{song_1_title}", fill="#FFFFFF", font=("Inter", -19, 'bold'))

    # Song 1 artist
    song_1_artist = songInfo[0][1].replace("'", "")
    if len(song_1_artist) > 28:
        song_1_artist = song_1_artist[0:25] + "..."
    canvas.create_text(172, 288, anchor="nw", text=f"{song_1_artist}", fill="#FFFFFF",
                       font=("Inter", -15, 'italic'))

    # Song 1 cover art
    song_1_img = Image.open("song1.png")
    song_1_img = song_1_img.resize(size)
    song_1_img = add_corners(song_1_img, 7)
    image_image_1 = ImageTk.PhotoImage(song_1_img)
    image_1 = canvas.create_image(104, 287, image=image_image_1)

    # Top artist 1
    artist1 = topArtists[0].replace("'", "")
    if len(artist1) > 28:
        artist1 = artist1[0:25] + "..."
    canvas.create_text(694, 275, anchor="nw", text=f"{artist1}", fill="#FFFFFF", font=("Inter", -19, 'bold'))

    # Top artist 1 image
    artist_1_img = Image.open("artist1.png")
    artist_1_img = crop_square(artist_1_img)
    artist_1_img = artist_1_img.resize(size)
    artist_1_img = add_corners(artist_1_img, 35)
    image_image_4 = ImageTk.PhotoImage(artist_1_img)
    image_4 = canvas.create_image(617, 287, image=image_image_4)

    # Song 2 title
    song_2_title = songInfo[1][0].replace("'", "")
    if len(song_2_title) > 28:
        song_2_title = song_2_title[0:25] + "..."
    canvas.create_text(172, 366, anchor="nw", text=f"{song_2_title}", fill="#FFFFFF", font=("Inter", -19, 'bold'))

    # Song 2 artist
    song_2_artist = songInfo[1][1].replace("'", "")
    if len(song_2_artist) > 28:
        song_2_artist = song_2_artist[0:25] + "..."
    canvas.create_text(172, 388, anchor="nw", text=f"{song_2_artist}", fill="#FFFFFF",
                       font=("Inter", -15, 'italic'))

    # Song 2 cover art
    song_2_img = Image.open("song2.png")
    song_2_img = song_2_img.resize(size)
    song_2_img = add_corners(song_2_img, 7)
    image_image_2 = ImageTk.PhotoImage(song_2_img)
    image_2 = canvas.create_image(104, 387, image=image_image_2)

    # Top artist 2
    artist2 = topArtists[1].replace("'", "")
    if len(artist2) > 28:
        artist2 = artist2[0:25] + "..."
    canvas.create_text(694, 375, anchor="nw", text=f"{artist2}", fill="#FFFFFF", font=("Inter", -19, 'bold'))

    # Top artist 2 image
    img2 = Image.open("artist2.png")
    img2 = crop_square(img2)
    img2 = img2.resize(size)
    img2 = add_corners(img2, 35)
    image_image_5 = ImageTk.PhotoImage(img2)
    image_5 = canvas.create_image(617, 387, image=image_image_5)

    # Song 3 title
    song_3_title = songInfo[2][0].replace("'", "")
    if len(song_3_title) > 28:
        song_3_title = song_3_title[0:25] + "..."
    canvas.create_text(172, 467, anchor="nw", text=f"{song_3_title}", fill="#FFFFFF", font=("Inter", -19, 'bold'))

    # Song 3 artist
    song_3_artist = songInfo[2][1].replace("'", "")
    if len(song_3_artist) > 28:
        song_3_artist = song_3_artist[0:25] + "..."
    canvas.create_text(172, 489, anchor="nw", text=f"{song_3_artist}", fill="#FFFFFF",
                       font=("Inter", -15, 'italic'))

    # Song 3 cover art
    song_3_img = Image.open("song3.png")
    song_3_img = song_3_img.resize(size)
    song_3_img = add_corners(song_3_img, 7)
    image_image_3 = ImageTk.PhotoImage(song_3_img)
    image_3 = canvas.create_image(104, 487, image=image_image_3)

    # Top artist 3
    artist3 = topArtists[2].replace("'", "")
    if len(artist3) > 28:
        artist3 = artist3[0:25] + "..."
    canvas.create_text(694, 475, anchor="nw", text=f"{artist3}", fill="#FFFFFF", font=("Inter", -19, 'bold'))

    # Top artist 3 image
    img3 = Image.open("artist3.png")
    img3 = crop_square(img3)
    img3 = img3.resize(size)
    img3 = add_corners(img3, 35)
    image_image_6 = ImageTk.PhotoImage(img3)
    image_6 = canvas.create_image(617, 487, image=image_image_6)

    # Remove the saved images
    for filename in os.listdir(parent_path):
        if str(filename).endswith(".png"):
            os.remove(filename)

    # Display GUI & destroy after 1 week
    # Millsecond value includes 5 second delay to account for loading
    window.after(604795000, lambda: window.destroy())
    window.mainloop()
