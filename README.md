# FTF-CRTT
This repository provides code and instructions for running the Face-to-Face Competetive Reaction Time Task (FTF-CRTT) first described in our academic article[add hyperlink]. Please cite this paper (and this [repository]([url](https://github.com/AnnahGrace01/FTF-CRTT/blob/main/CITATION.cff))) in any publications including our code or design. In the classic CRTT, a participant plays a game of reaction time against a fictitious opponent they are told is in another room, and each time the participant "wins" a round, they pick some punishment for their "opponent" (and vice versa). Unlike the classical CRTT, ours is designed to be run with two real participants. There are simpler versions of the classic CRTT available elsewhere designed to be run with just a single person (and a fake "opponent"), which are likely a better option if you wish to run an individual CRTT study. For example, available [here](https://www.millisecond.com/download/library/competitivereactiontime). Our code allows the winner of each round to send a "sound blast" to the loser.

## Running the Default Program

### Windows
We have provided an executable version of our experiment with default game settings using [PyInstaller](https://github.com/pyinstaller). You can use this to view our experiment without interfacing with Python. This executable will also allow you to replicate our study. You must calibrate your audio to your specific lab setup. The difference between blasts should be consistent lab to lab, but the base audio output will not be. You can check out our "Configuration in the lab" and "Hardware" sections of this README to understand how we have set up our experiment. If you use inline amplifiers as described in the hardware section, you should be able to get the dB output levels high enough. You can also see our "Standardization of the CRTT" section for details about dB level selection. If you cannot get the audio output to match your wants, you may need to use and modify our code in Python to work for your setup.

If you want to customize our code to extend our research, you will need to modify our script in Python. Instructions to get started are below (Installation section).

### MacOS
We created our program on a PC, but it can be compatible with MacOS. If you wish to see a default program in action without interfacing with Python, you can do so through the terminal. Before you do anything else, you will need to download the script you're trying to run (probably crtt_2023_archive.py) and the radio_static.mp3 to the same folder. Then, you can open the terminal and run the code below one line at a time. If this is your first time installing any of the packages, it can take quite a long time (especially HomeBrew).

```
# Install HomeBrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" 
# This will prompt you to enter your password. Please follow the instructions.

# Install python with tk
brew install python-tk

# Change the working directory to the folder containing the script and the audio file
# This is probably your downloads
cd Downloads


# Create and activate a virtual environment
python3 -m venv env
source env/bin/activate

# Install pydub
pip3 install pydub

# Run script
python3 crtt_2023_archive.py

# Deactivate virtual environment
deactivate
```

## Installation and Set Up for Replication
See requirments.txt for system and package requirements. We created this project in Python 3.11 through PyCharm Community Edition 2023.

### Pydub and SimpleAudio
The code requires you to install [Pydub](https://github.com/jiaaro/pydub) and [SimpleAudio](https://github.com/hamiltron/py-simple-audio). They can be difficult to get working, but with enough trial and error, it will work. You may have to manually import SimpleAudio into your working directory.

### Our audio file
The audio file we used for blasts is available in this repository (radio_static.mp3). If you plan to run our code through Python, you will need to put the audio file the same folder that contains the .py script to utilize relative paths. Otherwise, you can add an absolute file path to the code if you'd prefer.

## Configuration in the lab
Our lab is split into two rooms: the control room (where our computer running the program is) and the experimentation room (where the participants play the CRTT). Participants stand face-to-face, with all equipment in between them (below the eye line) as illustrated [here](https://github.com/AnnahGrace01/FTF-CRTT/blob/main/Arrangment%20of%20participants.pdf). Put simply, our code runs off of one computer and is displayed to both participants on two monitors simultaneously. Both participants see the same thing, and we leverage audio channels to send sound to only one participant at a time (expanded on below).

### Hardware
Our hardware consists of one computer running the code, an AUX. splitter, an HDMI splitter, a USB hub, two monitors, two keyboards, two pairs of headphones, and two big red buttons, as illustrated [here](https://github.com/AnnahGrace01/FTF-CRTT/blob/main/Hardware%20Diagram.pdf). The big red buttons emulate the "1" or "2" key ("1" for Player 1, etc.). We custom-made out beg red buttons with parts like [these]([url](https://learn.browndoggadgets.com/Search?query=Arcade%20Button)).

Player 1's headphones are attached to the right audio channel, and Player 2 gets the left audio channel. **NOTE.** Our code needs to play audio on only one channel at a time. Your Windows computer may try to "make up for" the single-channel audio by mirroring it to the other channel. If this happens (audio comes out of both headphones), you will need to find the setting that controls this and disable it. The setting may be called "audio enhancements".

### Calibrating sound
It is important that you know the volume levels coming out of your experiment at each blast level. The precise volume output will entirely depend on your experimental setup, cable length, etc. This means that you need to calibrate the audio to your exact setup. You can do this by editing the volume modifiers in lines 92 to 99 of the main script. You may have difficulty reaching an output of 110 dBs. This is why we use in-line amplifiers. Note that every time you run the experiment, you will need to have your computer audio set to the same volume (probably 100%).

### Our camera
We recorded participants during the game. To do this, we used an [Insta360 ONE X2](https://www.insta360.com/product/insta360-onex2) placed in between participants. We synced the video to our experiment offline in the original study. We have since improved the code to start and stop recording over wifi and sync the time more precisely. We will include this code once we are ready to publish it in this repository, along with a version without camera integration for those not using the Insta360 ONE X2. If you are looking for a good 360 camera for dyadic research, we have had success with Insta360. You should note, however, that their support for Python integration is almost non-existent.

## Extention, Customization, Standardization, and Analysis
We would love for you to modify our code and produce cool research. If you publish research with a modified version of our code and you are willing to share your modifications, please create a fork for the project and then make a pull request.

### Standardization of the CRTT
Before you design and employ a modification to the CRTT, you should know that there is a lot of debate in the field about standardization. We designed our FTF-CRTT with [Elson et al.'s (2014)](https://doi.org/10.1037/a0035569) recommendations in mind (available for free [here](https://www.researchgate.net/publication/259845770_Press_CRTT_to_Measure_Aggressive_Behavior_The_Unstandardized_Use_of_the_Competitive_Reaction_Time_Task_in_Aggression_Research)). Specifically, we use volume as a measure of aggression only, we did not include duration. As recommended, our blast level input scale is a range from 1-8, we did not include a 0 aggression response. Blast level 1 is 75dB, and each level is 5dB higher than the last (such that 8=110 dB). If you wish, you can change all of this by customizing the code we provide.

### Analysis
There is a lot of debate in the field about the usefulness of the CRTT as a measure of aggression. Some people use only the first blast level selection as a measure of unprovoked aggression (e.g., [here]([url](https://pubmed.ncbi.nlm.nih.gov/9686460/))). Others take a mean of blast selection on every round and consider it a measure of reactive aggression, etc. Because we are interested in reactive aggression, and reactive aggression requires negative emotional arousal, we recorded and affect coded emotion during the game and included only rounds where people were highly negative (details in our article). This is why our code includes time readouts for Time To Button Press (TTBP) and Time To Blast Initiate (TTBI). If you choose not to record affect, you can probably ignore these outputs. If you are interested in other temporal relationships, you can add and modify the time locking. Finally, we are working on producing an end-to-end program to allow researchers to automatically analyze affect data using the Facial Action Coding System ([FACS](https://local.psy.miami.edu/faculty/dmessinger/c_c/rsrcs/rdgs/emot/FACSChapter_SAGEEncyclopedia.pdf)) if they are not certified to use the FACS. This program will provide a frame-by-frame continuous output of basic emotions on a 0-5 scale so that you do not interface with Action Units directly. With that being said, we still recommend that anyone who wants to meaningfully use facial action data to conduct affect research become certified and proficient in the FACS so that you *could* hand-code data intelligently even if you never do.
