import os
import threading
import time
from tkinter import *
from tkinter import filedialog, messagebox
from pygame import mixer
from mutagen.mp3 import MP3


class YMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("YMUSIC PLAYER")
        self.root.geometry("750x450")

        # Initialize mixer and playlists
        mixer.init()
        self.playlist = []
        self.paused = False
        self.muted = False

        # Setup GUI components
        self.create_menu()
        self.create_widgets()

        # Initialize status bar and default volume
        self.statusbar = Label(self.root, text="Welcome to YMUSIC PLAYER", relief=GROOVE, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)
        self.volume_scale.set(70)

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.browse_file)
        file_menu.add_command(label="Exit", command=self.on_closing)

        # Help Menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About Us", command=self.about_us)

    def create_widgets(self):
        # Left frame for playlist
        left_frame = Frame(self.root)
        left_frame.pack(side=LEFT, padx=30)

        self.playlist_box = Listbox(left_frame)
        self.playlist_box.pack()

        add_button = Button(left_frame, text="Add+", command=self.browse_file)
        add_button.pack(side=LEFT, padx=10)

        delete_button = Button(left_frame, text="Del-", command=self.delete_song)
        delete_button.pack(side=LEFT)

        # Right frame for controls
        right_frame = Frame(self.root)
        right_frame.pack(pady=30)

        # Playback controls
        controls_frame = Frame(right_frame)
        controls_frame.grid(row=0, column=0, padx=10)

        # Store image references as instance variables
        self.play_img = PhotoImage(file= r"C:\Users\himan\Downloads\play.png")
        self.pause_img = PhotoImage(file= r"C:\Users\himan\Downloads\pause-button.png")
        self.stop_img = PhotoImage(file= r"C:\Users\himan\Downloads\stop.png")
        self.rewind_img = PhotoImage(file= r"C:\Users\himan\Downloads\rewind-button.png")
        self.mute_img = PhotoImage(file= r"C:\Users\himan\Downloads\volume-off.png")
        self.unmute_img = PhotoImage(file= r"C:\Users\himan\Downloads\volume-on.png")

        # Use the images for buttons
        play_button = Button(controls_frame, image=self.play_img, command=self.play_song)
        pause_button = Button(controls_frame, image=self.pause_img, command=self.pause_song)
        stop_button = Button(controls_frame, image=self.stop_img, command=self.stop_song)
        rewind_button = Button(controls_frame, image=self.rewind_img, command=self.rewind_song)
        self.mute_button = Button(controls_frame, image=self.mute_img, command=self.mute_song)

        # Place buttons
        play_button.grid(row=0, column=0)
        pause_button.grid(row=0, column=1)
        stop_button.grid(row=0, column=2)
        rewind_button.grid(row=0, column=3)
        self.mute_button.grid(row=0, column=4)

        # Volume control
        self.volume_scale = Scale(right_frame, from_=0, to=100, orient=HORIZONTAL, command=self.set_volume)
        self.volume_scale.grid(row=1, column=0, pady=10)

        # Time labels
        self.total_length_label = Label(right_frame, text="Total Length: --:--")
        self.total_length_label.grid(row=2, column=0)

        self.current_time_label = Label(right_frame, text="Current Time: --:--")
        self.current_time_label.grid(row=3, column=0)

    def browse_file(self):
        self.filename = filedialog.askopenfilename()
        if self.filename:
            self.add_to_playlist(self.filename)

    def add_to_playlist(self, filename):
        basename = os.path.basename(filename)
        self.playlist.append(filename)
        self.playlist_box.insert(END, basename)

    def delete_song(self):
        selected_song = self.playlist_box.curselection()
        if selected_song:
            index = selected_song[0]
            self.playlist_box.delete(index)
            self.playlist.pop(index)

    def about_us(self):
        messagebox.showinfo("About YMUSIC PLAYER", "This is a Music Player built using Python Tkinter.")

    def show_details(self, play_song):
        file_data = os.path.splitext(play_song)

        if file_data[1] == ".mp3":
            audio = MP3(play_song)
            total_length = audio.info.length
        else:
            audio = mixer.Sound(play_song)
            total_length = audio.get_length()

        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.total_length_label['text'] = f"Total Length: {time_format}"

        t1 = threading.Thread(target=self.start_count, args=(total_length,))
        t1.start()

    def start_count(self, total_length):
        current_time = 0
        while current_time <= total_length and mixer.music.get_busy():
            if self.paused:
                continue
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                time_format = '{:02d}:{:02d}'.format(mins, secs)
                self.current_time_label['text'] = f"Current Time: {time_format}"
                time.sleep(1)
                current_time += 1

    def set_volume(self, vol):
        volume = int(vol) / 100
        mixer.music.set_volume(volume)

    def play_song(self):
        if self.paused:
            mixer.music.unpause()
            self.paused = False
        else:
            try:
                selected_song = self.playlist_box.curselection()[0]
                play_it = self.playlist[selected_song]
                mixer.music.load(play_it)
                mixer.music.play()
                self.statusbar['text'] = "Playing Music: " + os.path.basename(play_it)
                self.show_details(play_it)
            except IndexError:
                messagebox.showerror("File not found", "YMUSIC PLAYER couldn't find the file, please try again.")

    def pause_song(self):
        self.paused = True
        mixer.music.pause()
        self.statusbar['text'] = "Music Paused"

    def stop_song(self):
        mixer.music.stop()
        self.statusbar['text'] = "Music Stopped"

    def rewind_song(self):
        self.play_song()
        self.statusbar['text'] = "Music Rewinded"

    def mute_song(self):
        if self.muted:
            mixer.music.set_volume(0.7)
            self.mute_button.config(image=self.mute_button.unmute_img)
            self.volume_scale.set(70)
            self.muted = False
        else:
            mixer.music.set_volume(0)
            self.mute_button.config(image=self.mute_button.mute_img)
            self.volume_scale.set(0)
            self.muted = True

    def on_closing(self):
        # Stop the music if it's playing
        self.stop_song()
        # Ask for confirmation
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


# Initialize Tkinter root window
root = Tk()
ymusic_player = YMusicPlayer(root)
root.mainloop()
