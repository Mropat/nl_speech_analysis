import pydub
from pydub import AudioSegment

sound = AudioSegment.from_mp3("/home/maria/Documents/NLstat/dumps/The Binding of Isaac - AFTERBIRTH+ - Northernlion Plays - Episode 272 [Compromise] (Daily)-Hb6fkOt3sNo.mp3")

# len() and slicing are in milliseconds
sound = sound[:59000]
first_half = sound

first_half.export("/home/maria/Documents/NLstat/dumps/The Binding of Isaac - AFTERBIRTH+ - Northernlion Plays - Episode 272 [Compromise] (Daily)-Hb6fkOt3sNo_cropped.flac", format="flac")