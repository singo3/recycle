# coding:utf-8
import os
import sqlite3

# conenct DB
conn = sqlite3.connect('data.db')
c = conn.cursor()

# get record
files = []
for row in c.execute('SELECT * FROM filename'):
    files.append(row)

for i in files:
    if r"'" in i[0]:
        idb0 = i[0].replace(r"'", r"''")
    else:
        idb0 = i[0]
    extension = os.path.splitext(i[0])[1]
    if extension == '.aif':
        #for j in c.execute(f"SELECT file_name FROM filename WHERE file_name = '{idb0}'"):
        #    print(j)
        c.execute(f"DELETE FROM filename WHERE file_name = '{idb0}'")
    else:
        pass

conn.commit()




'''
    if r"'" in i[0]:
        idb0 = i[0].replace(r"'", r"''")
    else:
        idb0 = i[0]
    if r"'" in i[1]:
        idb1 = i[1].replace(r"'", r"''")
    else:
        idb1 = i[1]
    if r"/" in i[0]:
        i0 = i[0].replace(r"/", r":")
        isub0 = idb0.replace(r"/", r":")
    else:
        i0  = i[0]
        isub0 = idb0
    if r"/" in i[1]:
        i1 = i[1].replace(r"/", r":")
        isub1 = idb1.replace(r"/", r":")
    else:
        i1 = i[1]
        isub1 = idb1
    filepass = "./music/" + i[3] + "/" + idb1 + "/" + idb0 #button_name表示用
    filepass_sub = "./music/" + i[3] + "/" + isub1 + "/" + isub0 #SoundLoader読み込み用
    filepass_sub2 = "./music/" + i[3] + "/" + i1 + "/" + i0 #soundfile読み込み用
        # insert data if not duplicate
    check = c.execute("SELECT file_name FROM filename WHERE file_name = '{}'".format(idb0)).fetchall()
    dup_check = c.execute("SELECT file_name, album, artist, tag_genre FROM filename WHERE file_name = '{}'".format(idb0)).fetchone() #/そのまま '変える idb
    if len(check):
        if dup_check[1] == i[1] and dup_check[2] == i[2] and dup_check[3] == i[3]:
            continue
        else: #music.csvのgenreと、genreフォルダを更新した時用
            song_time, data_time = get_song_time(filepass_sub2)
            print('updating...' + i[0])
            c.execute(f"UPDATE filename SET album = '{idb1}', artist = '{i[2]}', tag_genre = '{i[3]}', file_pass = '{filepass}', file_pass_sub = '{filepass_sub}', end_time = '{song_time}', end_time_raw = '{data_time}' WHERE file_name = '{i[0]}'")
    else:
        song_time, data_time = get_song_time(filepass_sub2) #/変える 'そのまま i
        print('reading...' + i[0])
        c.execute(f"INSERT INTO filename VALUES ('{idb0}', '{idb1}', '{i[2]}', '{filepass}', '{filepass_sub}', '{i[3]}', '', '', '', '', '{song_time}', '{data_time}', '')")
'''