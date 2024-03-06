import whisper
import time
import os

model = whisper.load_model("base")  # base, tiny, medium, large
result = model.transcribe("/Users/raymondwang/Downloads/deepblue.mp4")
print(result["text"])

# while(True):
#     i = []

dirname = os.path.dirname(__file__)
og = os.path.dirname(__file__)

# print(dirname)

os.chdir(dirname + "/vids/")

vidlist = os.listdir()

os.chdir(og)

# print(vidlist)

converttracks = False

start_time = time.time()
if converttracks:
    for vid in vidlist:
        if vid[0] != ".":
            filename = os.path.join(og + "/vids", vid)
            print(filename)

            my_clip = mp.VideoFileClip(filename)
            trackname = os.path.join(og + "/tracks/" + vid[:-4] + ".mp3")
            my_clip.audio.write_audiofile(trackname)
    print(
        "\n\n\n Completed audio extraction in ---%s seconds"
        % (time.time() - start_time)
    )

# print(os.listdir())

os.chdir(og + "/tracks/")

# print(os.path.dirname())

tracklist = os.listdir()

tracklist.sort()

print(tracklist)

transcribe = True

os.chdir(og)

counter = 0

if transcribe:
    for track in tracklist:
        if track[0] != ".":
            print("\n\n\n")
            start_time = time.time()
            filename = os.path.join(og + "/tracks", track)
            print(filename)
            print("WhisperAI – Begin processing.")
            model = whisper.load_model("base")  # base, tiny, medium, large
            result = model.transcribe(filename)
            print(result["text"])

            with open("transcript_base.txt", "a") as myfile:
                myfile.write("\f***TRANSCRIPT FOR " + track + " ***\n\n")
                myfile.write(result["text"] + "\n\n\n")

            print("WhisperAI – Done.")
            print("Completed in ---%s seconds" % (time.time() - start_time))
            counter += 1
            print(
                "Processed "
                + str(counter)
                + " out of "
                + str((len(tracklist) - 1))
                + " files."
            )
            print("\n\n\n")
