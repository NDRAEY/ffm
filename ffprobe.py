import subprocess as sp
import os, re

def ffprobe(file):
    proc = sp.Popen(['ffmpeg','-i',file], stderr=sp.PIPE)
    data = proc.stderr.read().decode("utf-8").split("\n")

    if file=="": return {
        "status":"error",
        "description":"No file specified."
    }

    if not os.path.isfile(file): return {
        "status":"error",
        "description":"File not found."
    }
    
    while True:
        k = data[0]
        if k.startswith("Input"): break
        del data[0]

    data = data[:-2]
    for n, i in enumerate(data):
        data[n] = re.sub(' +', ' ', data[n])

    total = {}

    for i in data:
        if i.startswith(" Duration"):
            dat = i.split(" ")[1:]
            total['duration'] = dat[1][:-1]
            total['bitrate'] = ' '.join(dat[-2:])
            break
        if i.startswith(" title"):
            total['title'] = ' '.join(i.split(" ")[3:])
        if i.startswith(" artist"):
            total['artist'] = ' '.join(i.split(" ")[3:])
        if i.startswith(" album"):
            total['album'] = ' '.join(i.split(" ")[3:])
        if i.startswith(" genre"):
            total['genre'] = ' '.join(i.split(" ")[3:])
        if i.startswith(" track"):
            total['track'] = ' '.join(i.split(" ")[3:])
        if i.startswith(" date"):
            total['date'] = ' '.join(i.split(" ")[3:])

    total['status'] = "ok"

    return total

if __name__=="__main__":
    import sys
    print(ffprobe(sys.argv[-1]))
