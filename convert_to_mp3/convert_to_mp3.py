import glob
import os
import subprocess

path = './bgm_album_files'
dir_list = os.listdir(path)
album = [f for f in dir_list if os.path.isdir(os.path.join(path, f))]
for i in album:
    os.makedirs('mp3/' + i)

source_list = []
ext_list = ["wav", "aif"]

#ffmpeg -i input -b:a 128k output.mp3
#ffmpeg -i '02 ipm020_02 Strolling to Summer.aif' -b:a 128k '02 ipm020_02 Strolling to Summer.mp3'
def convert_to_mp3(dir, file_name):
    output = file_name.replace('.wav','')
    output = output.replace('.aif','')
    print(dir, file_name, output)
    subprocess.call(
            [
                    "ffmpeg",
                    "-i",
                    path + "/" + dir + "/" + file_name,
                    "-b:a",
                    "128k",
                    "mp3/" + dir + "/" + output + ".mp3"
            ]
    )



for i in album:
        for j in ext_list:
                path_album = path + '/' + i + '/*.' + j
                flist = glob.glob(path_album)
                for j in flist:
                    dirname = os.path.basename(os.path.dirname(j))
                    basename = os.path.basename(j)
                    source = [dirname, basename]
                    source_list.append(source)

for i in source_list:
    convert_to_mp3(i[0], i[1])

