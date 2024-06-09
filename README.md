# FTF-CRTT
This repository provides code and instructions for running the Face-to-Face Competetive Reaction Time Task (FTF-CRTT) first described in our academic article[add hyperlink]. Please cite this paper in any publications including our code or design. Unlike the classical CRTT, ours is designed to be run with two people. There are simpler versions of the CRTT available elsewhere designed to be run with just a single person (and a fake "opponent"), which are likey a better option if you wish to run an individual CRTT study. For example, available [here](https://www.millisecond.com/download/library/competitivereactiontime). 

## Installation
### Pydub and SimpleAudio
### Our audio file

## Configuration in the lab
### Hardwear
### Calibrating sound
### Our camera

## Extention, Customization, Standardization, and Analysis
We would love for you to modify our code and produce cool research. If you publish research with a modified version of our code and you are willing to share your modifications, please get in touch so we can either add your code to this repository or add a link to your own repository.

### Standardization of the CRTT
Before you design and employ a modification to the CRTT, you should know that there is a lot of debate in the field about standardization. We designed our FTF-CRTT with [Elson et al.'s (2014)](https://doi.org/10.1037/a0035569) recommendations in mind (available for free [here](https://www.researchgate.net/publication/259845770_Press_CRTT_to_Measure_Aggressive_Behavior_The_Unstandardized_Use_of_the_Competitive_Reaction_Time_Task_in_Aggression_Research)). Specifically, we use volume as a measure of aggression only, we did not include duration. As recommended, our blast level input scale is a range from 1-8, we did not include a 0 aggression response. Blast level 1 is 75dB, and each level is 5dB higher than the last (such that 8=110 dB). If you wish, you can change all of this by customizing our provided code.

### Analysis
There is a lot of debate in the field about the usefulness of the CRTT as a measure of aggression. Some people use only the first blast level selection and call it "unprovoked aggression", and then ignore the rest of the data they collected. Others take a mean of blast selection on every round and consider it a measure of reactive aggression, etc. Because we are interested in reactive aggression, and reactive aggression requires negative emotional arousal, we recorded and affect coded emotion during the game and included only rounds where people were highly negative (details in our article). This is why our code includes time readouts for Time To Button Press (TTBP) and Time To Blast Initiate (TTBI). If you choose not to record affect, you can probably ignore these outputs. If you are interested in other temporal relationships, you can add and modify the time locking. Finally, we are working on producing an end-to-end program to allow researchers to automatically analyze affect data using the Facial Action Coding System ([FACS](https://local.psy.miami.edu/faculty/dmessinger/c_c/rsrcs/rdgs/emot/FACSChapter_SAGEEncyclopedia.pdf)) if they are not certified to use the FACS. This program will provide a frame-by-frame continuous output of basic emotions on a 0-5 scale so that you do not interface with Action Units directly. With that being said, we still recommend that anyone who wants to meaningfully use facial action data to conduct affect research become certified and proficient in the FACS so that you *could* hand-code data intelligently even if you never do. While the FACS is a feat of behavioural science, it also has many pitfalls and quirks that effect analysis and interpretation, and you can only fully understand these limitations and oddities if you know the system inside and out.
