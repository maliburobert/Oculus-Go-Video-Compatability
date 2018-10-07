import subprocess
import os
import json
import pprint
import sys

if len(sys.argv)>1:
    myDir = sys.argv[1]
else:
    myDir = "t:\\asdf\\source\\test"
myList = []

for root, dirs, files in os.walk(myDir):
    for name in files:
        myList += [os.path.join(root, name)]
    
for file in myList:
    # print file
    # print os.path.basename(file)[:3]
    if os.path.basename(file)[:3] == "GO_":
        continue
    if file[-4:] in ('.mkv','.avi','.mp4','.mov','.m4a'):
        cmd=["ffprobe","-v","quiet","-print_format","json","-show_format","-show_streams",file]
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        data = json.loads(p.stdout.read())
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data)
        vid = 0
        aud = 0
        try:
            ### pick the right datastreams, logic will take first index of each type
            for i in data["streams"]:
                if i["codec_type"] == "video":  break
                vid+=1
            for i in data["streams"]:
                if i["codec_type"] == "audio":  break
                aud+=1
            fps = round(float(data["streams"][vid]["avg_frame_rate"].split('/')[vid]) / float(data["streams"][vid]["avg_frame_rate"].split('/')[1]),2)
            ### Rename file for Oculus Go Compatibility
            if int(data["streams"][vid]["width"]) <= 4320:
                OGO = "GO"
                if "GO_" != os.path.basename(file)[:3]:
                    newName = "GO_"+os.path.basename(file)[:-4]+"180x180_LR"+os.path.basename(file)[-4:] 
                    newFile = os.path.join(os.path.dirname(file),newName)
                    os.rename(file,newFile)
            else:
                OGO = "NO"
            
            print OGO, data["streams"][vid]["codec_name"],data["streams"][vid]["width"],"x",data["streams"][vid]["height"],"@",fps,"fps",\
            int(data["format"]["bit_rate"])/10**6,"mbps", round(float(data["format"]["size"])/10**9,2),"GB",\
            round(float(data["format"]["duration"])/60,1),"mins",data["streams"][aud]["channel_layout"],file

        except Exception:
            print file, "exception"
            
            
"""
"C:\Program Files\HandBrake\HandBrakeCLI.exe" -i"T:\ASDF\Source\test\source.mkv" -O -o"T:\ASDF\Source\test\test2_180_LR.mp4" -w4320 -l2160 -ex264 -r59.94 -fav_mp4 -E ca_aac -6 stereo
"""