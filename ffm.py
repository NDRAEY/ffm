import subprocess as sp
import time
import re
import ffprobe as ffp

def calculate_duration(time):
    hrs, mn, sec, ms = re.split('\:|\.', time)
    hrs, mn, sec, ms = list(map(int, [hrs, mn, sec, ms]))

    calc = 0
    calc += (hrs*3600)
    calc += (mn*60)
    calc += sec
    calc += ms/100
    return calc

def run(inp: str = None,
        out: str = None,
        params: str = "",
        before_params: str = "",
        param=None):
    par = []
    pos = 0
    pmax = 5
    showprc = True
    if param is not None:
        par.append("ffmpeg")
        par.extend(param.split(" "))
    else:
        par.append("ffmpeg")
        par.extend(before_params)
        par.append("-i")
        par.append(inp)
        par.extend(params)
        par.append(out)
    
    while "" in par:
        par.remove("")

    fname = param.split(" ")
    if '-i' in fname:
        fname = fname[fname.index("-i")+1]
        if not fname: print("File not found."); return
        print("File: "+fname)
    else:
        print("File or stream is not present.")
        return

    dat = ffp.ffprobe(fname)

    if 'duration' in dat:
        tm = calculate_duration(dat['duration'])
    else:
        showprc = False
        
    prc = sp.Popen(par, stderr=sp.PIPE, universal_newlines=True)
    while True:
        cm = prc.stderr.readline()
        if not cm: print(""); break
        if cm.startswith("size="):
            data = cm.split(" ")
            if data[-1]=="\n": del data[-1]
            for i in data:
                data[data.index(i)] = i.split("=")[-1]
            while "" in data:
                data.remove("")
            size, time, bitrate, speed = data

            percent = "%.2f"%((calculate_duration(time)/tm)*100) if showprc else "--.-"
            print("\r%s%% <%s> [%s] [%s]"%(percent,
                                        size+"@"+speed,
                                        time,
                                        bitrate)
                ,end='\033[K',flush=True)
        else: pass
    return True

if __name__=="__main__":
    import sys
    nargs = ' '.join(sys.argv[1:])
    run(param=nargs)
