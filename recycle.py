# coding:utf-8
import os
os.environ['KIVY_AUDIO'] = 'ffpyplayer'

import sqlite3
import re
import glob
import csv
import shutil
import time as delay
from functools import partial

import soundfile as sf

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.core.text import Label as CoreLabel
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

resource_add_path("./font")
LabelBase.register(DEFAULT_FONT, "NotoSansJP-Regular.otf")



# conenct DB
conn = sqlite3.connect('data.db')
c = conn.cursor()

# create table if not exist
c.execute('''
CREATE TABLE IF NOT EXISTS filename({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12})
'''.format('file_name', 'album', 'artist','file_pass','file_pass_sub','tag_genre','tag_brightness','tag_strength','tag_inst','rate','end_time','end_time_raw','tag_us'))

'''
#(start point to add quatation when reading new wav and aif)
#open csv
csv_rlist = []    #csvリスト
with open('./music.csv') as f:
    reader = csv.reader(f)

    #delete first line
    for i in reader:
        csv_rlist.append(i)
    csv_rlist.pop(0)

def get_song_time(filepass_sub):
    data, samplerate = sf.read(filepass_sub)
    data_time = data.shape[0]/samplerate
    end_m, end_s = map(int, divmod(data_time, 60))
    end_s = str(end_s).zfill(2)
    song_time = f'{end_m}:{end_s}'
    return song_time, data_time


# when change music.csv other than file_name update DB
for i in csv_rlist:
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
                                                                                #/変える '変える isub
conn.commit()'''
#(end point to add quatation when reading new wav and aif)

# for UI
# get record
files = []
for row in c.execute('SELECT * FROM filename'):
    files.append(row)

Window.size = (1280,900)

items_checked = [] #checkbox
items_0 = [] #file_name
items_1 = [] #rate
items_2 = [] #time
items_3 = [] #file_pass
items_4 = [] #copy
items_5 = [] #tag_genre
items_6 = [] #tag_brightness
items_7 = [] #tag_strength
items_8 = [] #tag_instruments
items_9 = [] #album
items_10 = [] #artist
items_11 = [] #end_time_raw
items_12 = [] #file_pass_sub
items_13 = [] #tag_us
for row in c.execute('SELECT * FROM filename'):
    items_checked.append(False)
    items_0.append(row[0])
    items_1.append(row[9])
    items_2.append(row[10])
    items_3.append(row[3])
    items_4.append('C')
    items_5.append(row[5])
    items_6.append(row[6])
    items_7.append(row[7])
    items_8.append(row[8])
    items_9.append(row[1])
    items_10.append(row[2])
    items_11.append(row[11])
    items_12.append(row[4])
    items_13.append(row[12])

KV = '''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: 1935, 25
    button_name_text: 'button name text'
    file_pass_text: 'file_pass text'
    button_rate_text: 'button rate text'
    label_us_text: 'button us text'
    label_time_text: 'label time text'
    slider_value: 0
    slider_max: 100
    button_copy_text: 'button copy text'
    label_genre_text: 'label genre text'
    label_brightness_text: 'label brightness text'
    label_strength_text: 'label strength text'
    label_inst_text: 'label inst text'
    label_album_text: 'label album text'
    label_artist_text: 'label artist text'
    pos: self.pos
    size: self.size
    CheckBox:
        active: root.is_checked
        group: 'g1'
        size_hint_x: None
        width: 35
        on_press: root.on_press_checkbox()
    Button:
        id: id_button_name
        text: root.button_name_text
        font_size: 12
        size_hint_x: None
        width: 300
        on_press: root.on_play_button(root.file_pass_sub)
    Button:
        id: id_button_rate
        text: root.button_rate_text
        font_size: 12
        size_hint_x: None
        width: 35
        on_press: root.on_press_rate(root.button_rate)
    Label:
        id: id_label_us
        text: root.label_us_text
        font_size: 12
        size_hint_x: None
        width: 35
    Label:
        id: id_label_time
        text: root.label_time_text
        font_size: 12
        size_hint_x: None
        width: 80
    Slider:
        id: id_slider_seek
        min: 0
        max: root.slider_max
        value: root.slider_value
        cursor_width: 25
        cursor_height: 25
        size_hint_x: None
        width: 150
        on_touch_up: root.slider_touch(root.button_name, self.value, root.label_time)
        on_touch_move: root.slider_move(root.file_pass_sub, self.value, root.label_time)
    Button:
        id: id_button_copy
        text: root.button_copy_text
        font_size: 12
        size_hint_x: None
        width: 35
        on_press: root.on_press_copy(root)
    Label:
        id: id_label_genre
        text: root.label_genre_text
        font_size: 12
        size_hint_x: None
        width: 50
    Label:
        id: id_label_brightness
        text: root.label_brightness_text
        font_size: 12
        size_hint_x: None
        width: 150
    Label:
        id: id_label_strength
        text: root.label_strength_text
        font_size: 12
        size_hint_x: None
        width: 50
    Label:
        id: id_label_inst
        text: root.label_inst_text
        font_size: 12
        size_hint_x: None
        width: 450
    Label:
        id: id_label_album
        text: root.label_album_text
        font_size: 12
        size_hint_x: None
        width: 300
    Label:
        id: id_label_artist
        text: root.label_artist_text
        font_size: 12
        size_hint_x: None
        width: 300

RecycleView:
    id: rv
    viewclass: 'SelectableLabel'
    data: []
    scroll_type: ['bars', 'content']
    scroll_wheel_distance: sp(60) #スクロール速度
    SelectableRecycleBoxLayout:
        default_size: None, dp(25)
        size_hint_x: 1
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: True
        key_selection: 'selectable'
'''

playing_index = ['index'] #再生中のインデックスを入れる配列
playing_pass = [] #再生中のパスを入れる
play_button = ['off'] #再生ボタンを押す概念
is_playing = ['stop'] #再生中かどうか
now_str_box = [] #now_strを入れる配列
volume_value = [1] #volumeのvaluemを入れる配列
sound_box = [] #volumeを制御するためにself.soundを入れる配列
playing_name = [] #再生中の楽曲名を入れる配列
playing_lbl = [] #再生中の表示のためのラベルwidgetを入れる配列
footer_lbl = [] #曲情報のためのラベルwidgetを入れる配列
footer_lbl_data = [] #曲情報のための曲数を入れる配列
footer_lbl_albums = [] #曲情報のためのアルバム数を入れる配列
footer_lbl_genres = [] #曲情報のためのジャンル数を入れる配列
footer_rightlbl = [] #タグが外れたときのためのラベルwidgetを入れる配列
pre_playing = ['pre_playing']

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    def get_nodes(self):
        nodes = self.get_selectable_nodes()
        print(nodes)
        if self.nodes_order_reversed:
            nodes = nodes[::-1]
        if not nodes:
            return None, None


class SelectableLabel(RecycleDataViewBehavior, GridLayout):
    ''' 1行ずつ変数が定義されているよう '''
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    cols = 13
    button_name_text = StringProperty()
    label_time_text = StringProperty()
    is_checked = BooleanProperty(False)
    sound_play = [] #再生中または直前に再生されたボタンwidgetを入れる配列
    pause_box = [0] #停止した時の時間を入れる配列
    now_str = '0:00' #曲の再生中の時間を入れる
    seek_pos = 0 #再生のseekタイムを入れる
    clock_event_box = [] #実行されているclockオブジェクトと入れる配列
    self_box = [] #ラジオボタンが点灯しているselfオブジェクトを入れる配列
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.button_name_text = data['button_name']['text']
        self.file_pass_text = data['file_pass']['text']
        self.button_rate_text = data['button_rate']['text']
        self.label_us_text = data['label_us']['text']
        self.end_time = data['label_time']['text']
        self.label_time_text = self.now_str + '/' + data['label_time']['text']
        self.slider_value = 0
        self.slider_max = data['slider']['max']
        self.button_copy_text = data['button_copy']['text']
        self.label_genre_text = data['label_genre']['text']
        self.label_brightness_text = data['label_brightness']['text']
        self.label_strength_text = data['label_strength']['text']
        self.label_inst_text = data['label_instruments']['text']
        self.label_album_text = data['album']['text']
        self.label_artist_text = data['artist']['text']
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            #return True
            return self.parent.select_with_touch(self.index, touch)
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        #ボタン押した時
        self.self_box.clear()
        self.self_box.append(self)
        footer_rightlbl[0].text = ''
        if is_playing == ['stop'] and is_selected and play_button == ['on']:
            playing_index.clear()
            playing_index.append(index)
            playing_name.clear()
            playing_name.append(self.button_name_text)
            playing_lbl[0].text = 'Playing... ' + playing_name[0]
            footer_lbl[0].text = str(index + 1) + ' / ' + str(footer_lbl_data[0]) + '曲' + \
            ' / ' + str(footer_lbl_albums[0]) + 'アルバム' + ' / ' + str(footer_lbl_genres[0]) + 'ジャンル'
            #立ち上げ直後か直前に再生した曲と同じ場合
            if playing_pass == [] or playing_pass == [rv.data[index]['file_pass_sub']['text']]:
                self.seek_pos = self.pause_box[0]
            #直前に再生した曲と違う場合
            elif playing_pass != [rv.data[index]['file_pass_sub']['text']]:
                self.return_zero()
            is_playing.clear()
            playing_pass.clear()
            is_playing.append('play')
            playing_pass.append(rv.data[index]['file_pass_sub']['text'])
            self.on_press_checkbox2()
            self.on_sound_play(rv.data[index]['file_pass_sub']['text'])
            self.sound_play.append(self.sound)
            self.sound_play[0].seek(self.seek_pos)
            self.pause_box.clear()
            now_str_box.clear()
            now_str_box.append(self)
            now_str_box.append(rv.data[index]['label_time'])
            self.clock_event_box.clear()
            self.now_str_timer(rv.data[index]['label_time']['text'])
        elif is_playing == ['play'] and is_selected and playing_index[0] == index:
            #再生中のボタンが画面から消えたあと再表示された時
            if play_button == ['on']:
                self.is_checked = True
                playing_index.clear()
                playing_index.append(index)
                if r"'" in rv.data[index]['button_name']['text']:
                    name = rv.data[index]['button_name']['text'].replace(r"'", r"''")
                else:
                    name = rv.data[index]['button_name']['text']
                brightness, strength, inst = c.execute("SELECT tag_brightness, tag_strength, tag_inst FROM filename WHERE file_name = '{}'".format(name)).fetchone()
                self.label_brightness_text = brightness
                self.label_strength_text = strength
                self.label_inst_text = inst
            #再生中のボタンを押して停止した時
            else:
                playing_lbl[0].text = 'Pausing... ' + playing_name[0]
                self.on_press_checkbox3()
                now_str_box[0].clock_event_box[0].cancel()
                self.on_sound_stop()
        #multiselect: Falseによって生じる1回目のapply_selectionを打ち消す
        elif is_selected == False and playing_index[0] == index:
            pass
        #連続再生または再生中に他のシークスライダーかrateボタン押した時
        elif is_playing == ['play'] and is_selected and playing_index[0] != index and play_button == ['on']:
            footer_lbl[0].text = str(index + 1) + ' / ' + str(footer_lbl_data[0]) + '曲' + \
            ' / ' + str(footer_lbl_albums[0]) + 'アルバム' + ' / ' + str(footer_lbl_genres[0]) + 'ジャンル'
            self.on_press_checkbox2()
            playing_index.clear()
            playing_index.append(index)
            playing_name.clear()
            playing_name.append(self.button_name_text)
            playing_lbl[0].text = 'Playing... ' + playing_name[0]
            self.seek_pos = 0
            playing_pass.clear()
            playing_pass.append(rv.data[index]['file_pass_sub']['text'])
            self.clock_event_box[0].cancel()
            self.return_zero()
            self.sound_play[0].stop()
            delay.sleep(0.1)
            self.sound_play[0].unload()
            self.sound_play.clear()
            self.on_sound_play(rv.data[index]['file_pass_sub']['text'])
            self.sound_play.append(self.sound)
            self.sound_play[0].seek(self.seek_pos)
            self.pause_box.clear()
            now_str_box.clear()
            now_str_box.append(self)
            now_str_box.append(rv.data[index]['label_time'])
            self.clock_event_box.clear()
            self.now_str_timer(rv.data[index]['label_time']['text'])
        #作動していないボタンが画面に表示された時
        else:
            #セレクトされていない曲
            if playing_index[0] != self.index:
                self.now_str = '0:00'
                self.label_time_text = self.now_str + '/' + rv.data[index]['label_time']['text']
                if r"'" in rv.data[index]['button_name']['text']:
                    name = rv.data[index]['button_name']['text'].replace(r"'", r"''")
                else:
                    name = rv.data[index]['button_name']['text']
                brightness, strength, inst = c.execute("SELECT tag_brightness, tag_strength, tag_inst FROM filename WHERE file_name = '{}'".format(name)).fetchone()
                rv.data[index]['label_brightness']['text'] = brightness
                rv.data[index]['label_strength']['text'] = strength
                rv.data[index]['label_instruments']['text'] = inst
            #セレクトされている曲
            else:
                self.now_str = round(self.pause_box[0])
                now_m, now_s = map(int, divmod(self.now_str, 60))
                now_s = str(now_s).zfill(2)
                self.now_str = f'{now_m}:{now_s}'
                self.label_time_text = self.now_str + '/' + rv.data[index]['label_time']['text']
    def on_sound_play(self, sound_pass, *args):
        try:
            self.sound = SoundLoader.load(sound_pass)
            sound_box.clear()
            sound_box.append(self.sound)
            self.sound.play()
            self.sound.volume = volume_value[0]
        except Exception as e:
            print('play error')
    def on_sound_stop(self, *args):
        self.pause_box.append(self.sound_play[0].get_pos())
        self.sound_play[0].stop()
        self.sound_play[0].unload()
        self.sound_play.clear()
        is_playing.clear()
        is_playing.append('stop')
        delay.sleep(0.1)
    def count(self, time, *args):
        if sound_box[0].state == 'play':
            self.now_str = self.sound_play[0].get_pos()
            self.now_str = round(self.now_str)
            now_m, now_s = map(int, divmod(self.now_str, 60))
            now_s = str(now_s).zfill(2)
            self.now_str = f'{now_m}:{now_s}'
            if playing_index[0] == self.index:
                playing_lbl[0].text = 'Playing... ' + playing_name[0]
                self.label_time_text = self.now_str + '/' + time
                self.slider_value = self.sound_play[0].get_pos()
            else: #再生中にスクロールして別の曲の表示がキャッチされても上書き?
                playing_lbl[0].text = '[ref=Caution : Out of operation][color=ff0000]Caution : Out of operation[/color][/ref]   Playing... ' + playing_name[0]
                pass
                #self.label_time_text = '0:00' + '/' + self.end_time
                #self.slider_value = 0
        elif sound_box[0].state == 'stop': #再生が最後まで行われた時に停止する用
            playing_lbl[0].text = 'Not Playing'
            play_button.clear()
            play_button.append('off')
            self.clock_event_box[0].cancel()
            self.return_zero()
            self.on_sound_stop()
            self.on_press_checkbox3()
    def now_str_timer(self, time, *args):
        self.clock_event = Clock.schedule_interval(partial(self.count, f'{time}'), 0.1)
        self.clock_event_box.append(self.clock_event)
    def return_zero(self, *args):
        change_label = now_str_box[0]
        change_label.label_time_text = '0:00/' + now_str_box[1]['text']
        change_label.slider_value = 0
        self.pause_box.clear()
        self.pause_box.append(0)
    def on_play_button(self, file_pass_sub, *args):
        #曲が停止中の場合
        if play_button == ['off']:
            play_button.clear()
            play_button.append('on')
        #再生中の曲ボタンを再度押す場合
        elif (play_button == ['on']) and (playing_pass == [file_pass_sub['text']]):
            play_button.clear()
            play_button.append('off')
        #再生中とは違う曲ボタンを押す場合
        else:
            pass
    def on_press_checkbox(self, **kwargs):
        self.self_box.clear()
        self.self_box.append(self)
    def on_press_checkbox2(self, **kwargs):
        if self.self_box != []:
            self.self_box[0].is_checked = False
        else:
            pass
        self.is_checked = True
    def on_press_checkbox3(self, **kwargs):
        self.is_checked = False
    def on_press_rate(self, rv, **kwargs):
        if self.button_rate_text == '':
            self.button_rate_text = '1'
            rv['text'] = '1'
        elif self.button_rate_text == '1':
            self.button_rate_text = '2'
            rv['text'] = '2'
        elif self.button_rate_text == '2':
            self.button_rate_text = '3'
            rv['text'] = '3'
        elif self.button_rate_text == '3':
            self.button_rate_text = '4'
            rv['text'] = '4'
        elif self.button_rate_text == '4':
            self.button_rate_text = '5'
            rv['text'] = '5'
        elif self.button_rate_text == '5':
            self.button_rate_text = ''
            rv['text'] = ''
        else:
            print('rate error')
        c.execute("update filename set rate=? where file_name=?", (self.button_rate_text, self.button_name_text))
        conn.commit()
    def on_press_copy(self, root, *args):
        source = root.file_pass_sub['text']
        copy = './copy/' + root.button_name['text']
        shutil.copyfile(source, copy)
    def change_now_str(self, value, time, *args):
        now_m, now_s = map(int, divmod(value, 60))
        now_s = str(now_s).zfill(2)
        now_str = f'{now_m}:{now_s}'
        self.label_time_text = now_str + '/' + time['text']
    def slider_move(self, file_pass, value, time, *args):
        if playing_pass == []:
            pass
        elif is_playing == ['play'] and playing_pass[0] == file_pass['text']:
            self.sound_play[0].seek(value)
            self.change_now_str(value, time)
        elif is_playing == ['stop'] and playing_pass[0] == file_pass['text']:
            self.pause_box[0] = value
            self.change_now_str(value, time)
        elif is_playing == ['play'] and playing_pass[0] != file_pass['text']:
            pass
        else:
            self.seek_pos = value
            self.change_now_str(value, time)
    def tag_brightness_update(self, tag, *args):
        if playing_index[0] == self.self_box[0].index:
            pass
        else:
            footer_rightlbl[0].text = '[ref=No match! : Press the play button again!][color=00ff00]No match! : Press the play button again![/color][/ref]'
            return
        if self.self_box == []:
            return
        elif self.self_box[0].label_brightness_text == '':
            self.self_box[0].label_brightness_text = tag
            c.execute("update filename set tag_brightness=? where file_name=?", (tag, self.self_box[0].button_name_text))
        elif self.self_box[0].label_brightness_text == tag:
            self.self_box[0].label_brightness_text = ''
            c.execute("update filename set tag_brightness=? where file_name=?", ('', self.self_box[0].button_name_text))
        elif self.self_box[0].label_brightness_text != tag:
            self.self_box[0].label_brightness_text = tag
            c.execute("update filename set tag_brightness=? where file_name=?", (tag, self.self_box[0].button_name_text))
        conn.commit()
    def tag_strength_update(self, tag, *args):
        if playing_index[0] == self.self_box[0].index:
            pass
        else:
            footer_rightlbl[0].text = '[ref=No match! : Press the play button again!][color=00ff00]No match! : Press the play button again![/color][/ref]'
            return
        if self.self_box == []:
            return
        elif self.self_box[0].label_strength_text == '':
            self.self_box[0].label_strength_text = tag
            c.execute("update filename set tag_strength=? where file_name=?", (tag, self.self_box[0].button_name_text))
        elif self.self_box[0].label_strength_text == tag:
            self.self_box[0].label_strength_text = ''
            c.execute("update filename set tag_strength=? where file_name=?", ('', self.self_box[0].button_name_text))
        elif self.self_box[0].label_strength_text != tag:
            self.self_box[0].label_strength_text = tag
            c.execute("update filename set tag_strength=? where file_name=?", (tag, self.self_box[0].button_name_text))
        conn.commit()
    def tag_inst_update(self, tag, *args):
        if playing_index[0] == self.self_box[0].index:
            pass
        else:
            footer_rightlbl[0].text = '[ref=No match! : Press the play button again!][color=00ff00]No match! : Press the play button again![/color][/ref]'
            return
        if self.self_box == []:
            return
        elif self.self_box[0].label_inst_text == '':
            self.self_box[0].label_inst_text = tag
            c.execute("update filename set tag_inst=? where file_name=?", (tag, self.self_box[0].button_name_text))
        elif tag in self.self_box[0].label_inst_text:
            self.self_box[0].label_inst_text = self.self_box[0].label_inst_text.replace(tag, '')
            c.execute("update filename set tag_inst=? where file_name=?", (self.self_box[0].label_inst_text, self.self_box[0].button_name_text))
        else:
            self.self_box[0].label_inst_text += tag
            c.execute("update filename set tag_inst=? where file_name=?", (self.self_box[0].label_inst_text, self.self_box[0].button_name_text))
        conn.commit()
    def tag_us_update(self, tag, *args):
        if playing_index[0] == self.self_box[0].index:
            pass
        else:
            footer_rightlbl[0].text = '[ref=No match! : Press the play button again!][color=00ff00]No match! : Press the play button again![/color][/ref]'
            return
        if self.self_box == []:
            return
        elif self.self_box[0].label_us_text == '':
            self.self_box[0].label_us_text = tag
            c.execute("update filename set tag_us=? where file_name=?", (tag, self.self_box[0].button_name_text))
        elif self.self_box[0].label_us_text == tag:
            self.self_box[0].label_us_text = ''
            c.execute("update filename set tag_us=? where file_name=?", ('', self.self_box[0].button_name_text))
        elif self.self_box[0].label_us_text != tag:
            self.self_box[0].label_us_text = tag
            c.execute("update filename set tag_us=? where file_name=?", (tag, self.self_box[0].button_name_text))
        conn.commit()
    def slider_touch(self, button_name, value, time, *args):
        if not self.sound_play:
            if value != 0:
                self.pause_box.clear()
                self.pause_box.append(value)
                self.now_str = round(value)
                now_m, now_s = map(int, divmod(self.now_str, 60))
                now_s = str(now_s).zfill(2)
                self.now_str = f'{now_m}:{now_s}'
                self.label_time_text = self.now_str + '/' + time['text']
            else:
                return
        else:
            if value != 0:
                if pre_playing[0] != button_name:
                    if value < 0.2:
                        return
                    else:
                        delay.sleep(0.1)
                        self.sound_play[0].seek(value)
                        pre_playing.clear()
                        pre_playing.append(button_name)
                else:
                    if abs(self.sound_play[0].get_pos() - value) > 1:
                        delay.sleep(0.1)
                        self.sound_play[0].seek(value)
                    else:
                        return
            else:
                return

class MainScreen(App, SelectableLabel):
    #set initial
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.focus_genre_word = ''
        self.focus_brightness_word = ''
        self.focus_strength_word = ''
        self.focus_inst_word = ''
        self.focus_search_word = ''
        self.time_sort_rev = False

    def rv_update_brightness(self, word, *args):
        if playing_index == ['index']:
            return
        else:
            pass
        if playing_index[0] == self.self_box[0].index:
            pass
        else:
            return
        rv_tag = self.display_recycle.data[playing_index[0]]['label_brightness']['text']
        if rv_tag != word:
            self.display_recycle.data[playing_index[0]]['label_brightness']['text'] = word
        else:
            self.display_recycle.data[playing_index[0]]['label_brightness']['text'] = ''

    def tag_pressed_bright(self, *args):
        word = '明るめ'
        self.tag_brightness_update(word)
        self.rv_update_brightness(word)

    def tag_pressed_either(self, *args):
        word = 'どちらとも言えない'
        self.tag_brightness_update(word)
        self.rv_update_brightness(word)

    def tag_pressed_dark(self, *args):
        word = '暗め'
        self.tag_brightness_update(word)
        self.rv_update_brightness(word)

    def rv_update_strength(self, word, *args):
        if playing_index == ['index']:
            return
        else:
            pass
        if playing_index[0] == self.self_box[0].index:
            pass
        else:
            return
        rv_tag = self.display_recycle.data[playing_index[0]]['label_strength']['text']
        if rv_tag != word:
            self.display_recycle.data[playing_index[0]]['label_strength']['text'] = word
        else:
            self.display_recycle.data[playing_index[0]]['label_strength']['text'] = ''

    def tag_pressed_strong(self, *args):
        word = '強い'
        self.tag_strength_update(word)
        self.rv_update_strength(word)

    def tag_pressed_light(self, *args):
        word = '少し強い'
        self.tag_strength_update(word)
        self.rv_update_strength(word)

    def tag_pressed_upturn(self, *args):
        word = '起伏系'
        self.tag_strength_update(word)
        self.rv_update_strength(word)

    def tag_pressed_week(self, *args):
        word = '弱い'
        self.tag_strength_update(word)
        self.rv_update_strength(word)

    def rv_update_inst(self, word, *args):
        if playing_index == ['index']:
            return
        else:
            pass
        if playing_index[0] == self.self_box[0].index:
            pass
        else:
            return
        rv_tag = self.display_recycle.data[playing_index[0]]['label_instruments']['text']
        if word in rv_tag:
            self.display_recycle.data[playing_index[0]]['label_instruments']['text'].replace(word, '')
        else:
            self.display_recycle.data[playing_index[0]]['label_instruments']['text'] += word

    def tag_pressed_per(self, *args):
        word = 'パーカッション '
        self.tag_inst_update(word)
        self.rv_update_inst(word)

    def tag_pressed_piano(self, *args):
        word = 'ピアノ '
        self.tag_inst_update(word)
        self.rv_update_inst(word)

    def tag_pressed_guitar(self, *args):
        word = 'ギター '
        self.tag_inst_update(word)
        self.rv_update_inst(word)

    def tag_pressed_electric(self, *args):
        word = '電子系 '
        self.tag_inst_update(word)
        self.rv_update_inst(word)

    def tag_pressed_orche(self, *args):
        word = 'オーケストラ大編成 '
        self.tag_inst_update(word)
        self.rv_update_inst(word)

    def tag_pressed_ensemble(self, *args):
        word = 'オーケストラ小編成 '
        self.tag_inst_update(word)
        self.rv_update_inst(word)

    def tag_pressed_ethnic(self, *args):
        word = '民族系 '
        self.tag_inst_update(word)
        self.rv_update_inst(word)

    def tag_pressed_other(self, *args):
        word = 'その他 '
        self.tag_inst_update(word)
        self.rv_update_inst(word)

    def rv_update_us(self, word, *args):
        if playing_index == ['index']:
            return
        else:
            pass
        if playing_index[0] == self.self_box[0].index:
            pass
        else:
            return
        rv_tag = self.display_recycle.data[playing_index[0]]['label_us']['text']
        if rv_tag != word:
            self.display_recycle.data[playing_index[0]]['label_us']['text'] = word
        else:
            self.display_recycle.data[playing_index[0]]['label_us']['text'] = ''

    def tag_pressed_us(self, *args):
        word = 'U'
        self.tag_us_update(word)
        self.rv_update_us(word)

    def display_count_songs(self, data, *args):
        songs = len(data)
        albums = [data[i]['album']['text'] for i in range(len(data))]
        albums = len(set(albums))
        genres = [data[i]['label_genre']['text'] for i in range(len(data))]
        genres = len(set(genres))
        footer_lbl_data.clear()
        footer_lbl_data.append(songs)
        footer_lbl_albums.clear()
        footer_lbl_albums.append(albums)
        footer_lbl_genres.clear()
        footer_lbl_genres.append(genres)
        footer_lbl[0].text = '0 / ' + str(songs) + '曲' + ' / ' + str(albums) + 'アルバム' + ' / ' + str(genres) + 'ジャンル'

    #display_areaをkivyファイルで読み込み
    def display(self, *args):
        self.display_area = BoxLayout(size_hint=(1.6, 1))
        self.display_area.orientation = "vertical"
        self.display_area.bind(minimum_height=self.display_area.setter('height'))
        self.display_area.bind(minimum_width=self.display_area.setter('width'))
        row_height = 35
        display_width = 1935
        display_area_row_head = BoxLayout(height=row_height, width=display_width, size_hint=(None, None))
        display_area_row_head.orientation = "horizontal"
        display_area_row_check_head = Label(text='', font_size = 12, height=row_height, width=row_height, size_hint=(None, None))
        self.display_area_row_name_head = Label(text='[ref=file name]file name  ↓[/ref]', font_size = 12, height=row_height, \
            width=300, size_hint=(None, None), markup=True, on_ref_press=self.name_sort)
        display_area_row_rate_head= Label(text='rate', font_size = 12, height=row_height, width=row_height, size_hint=(None, None))
        self.display_area_row_time_head = Label(text='[ref=time]time  ⇅[/ref]', font_size=12, height=row_height, \
            width=80, size_hint=(None, None), markup=True, on_ref_press=self.time_sort)
        display_area_row_head_tag_us  = Label(text='U/S', font_size=12, height=row_height, width=35, size_hint=(None, None))
        display_area_row_posi_head = Label(text='seek bar', font_size=12, height=row_height, width=150, size_hint=(None, None))
        display_area_row_copy_head= Label(text='copy', font_size = 12, height=row_height, width=row_height, size_hint=(None, None))
        display_area_row_head_tag0  = Label(text='Gen', font_size=12, height=row_height, width=50, size_hint=(None, None))
        display_area_row_head_tag1  = Label(text='Brt', font_size=12, height=row_height, width=150, size_hint=(None, None))
        display_area_row_head_tag2  = Label(text='Str', font_size=12, height=row_height, width=50, size_hint=(None, None))
        display_area_row_head_tag3  = Label(text='Ins', font_size=12, height=row_height, width=450, size_hint=(None, None))
        display_area_row_album_head = Label(text='album', font_size = 12, height=row_height, width=300, size_hint=(None, None))
        display_area_row_artist_head = Label(text='artist', font_size = 12, height=row_height, width=300, size_hint=(None, None))
        display_area_row_head.add_widget(display_area_row_check_head)
        display_area_row_head.add_widget(self.display_area_row_name_head)
        display_area_row_head.add_widget(display_area_row_rate_head)
        display_area_row_head.add_widget(display_area_row_head_tag_us)
        display_area_row_head.add_widget(self.display_area_row_time_head)
        display_area_row_head.add_widget(display_area_row_posi_head)
        display_area_row_head.add_widget(display_area_row_copy_head)
        display_area_row_head.add_widget(display_area_row_head_tag0)
        display_area_row_head.add_widget(display_area_row_head_tag1)
        display_area_row_head.add_widget(display_area_row_head_tag2)
        display_area_row_head.add_widget(display_area_row_head_tag3)
        display_area_row_head.add_widget(display_area_row_album_head)
        display_area_row_head.add_widget(display_area_row_artist_head)
        self.display_area.add_widget(display_area_row_head)
        self.display_recycle = Builder.load_string(KV)
        paired_iter = zip(items_checked, items_0, items_1, items_2, items_3, items_4, items_5 \
        , items_6, items_7, items_8, items_9, items_10, items_11, items_12, items_13)
        for ichecked, i0, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10 , i11, i12 , i13 in paired_iter:
            d = {'is_checked': ichecked, 'button_name': {'text': i0}, 'button_rate': {'text': i1}, \
            'label_time': {'text': i2}, 'file_pass': {'text': i3}, 'button_copy': {'text': i4}, \
            'label_genre': {'text': i5}, 'label_brightness': {'text': i6}, 'label_strength': {'text': i7}, \
            'label_instruments': {'text': i8}, 'album': {'text': i9}, \
            'artist': {'text': i10}, 'slider': {'max': i11}, 'file_pass_sub': {'text': i12}, 'label_us': {'text': i13}}
            self.display_recycle.data.append(d)
        self.display_area.add_widget(self.display_recycle)
        conn.commit()

    def stop_for_switching(self, *args):
        if now_str_box == []:
            pass
        else:
            if now_str_box[0].pause_box == []:
                now_str_box[0].pause_box.append(0)
            else:
                now_str_box[0].pause_box[0] = 0
            now_str_box[0].now_str = '0:00'
            now_str_box[0].clock_event_box[0].cancel()
            sound_box[0].stop()
            delay.sleep(0.1)
            play_button.clear()
            play_button.append('off')
            sound_box[0].unload()
            delay.sleep(0.1)
            now_str_box[0].label_time_text = '0:00/' + now_str_box[1]['text']
            now_str_box[0].slider_value = 0
            now_str_box[0].seek_pos = 0

    def focus_display(self, *args):
        self.stop_for_switching()
        self.display_area_row_name_head.color = [1, 1, 1, 1]
        self.display_area_row_time_head.color = [1, 1, 1, 1]
        focus_data = []
        if self.focus_genre_word == '' and \
           self.focus_brightness_word == '' and \
           self.focus_strength_word == '' and \
           self.focus_inst_word == '' and \
           self.focus_search_word == '':
            for row in c.execute('SELECT * FROM filename'):
                d = {'is_checked': False, 'button_name': {'text': row[0]}, 'button_rate': {'text': row[9]}, \
                'label_time': {'text': row[10]}, 'file_pass': {'text': row[3]}, 'button_copy': {'text': 'C'}, \
                'label_genre': {'text': row[5]}, 'label_brightness': {'text': row[6]}, 'label_strength': {'text': row[7]}, \
                'label_instruments': {'text': row[8]}, 'album': {'text': row[1]}, 'artist': {'text': row[2]}, \
                'slider': {'max': row[11]}, 'file_pass_sub': {'text': row[4]}, 'label_us': {'text': row[12]}}
                focus_data.append(d)
        else:
            for i in c.execute('SELECT * FROM filename'):
                if self.focus_genre_word != '' and self.focus_genre_word != i[5]:
                    continue
                elif self.focus_brightness_word != '' and self.focus_brightness_word != i[6]:
                    continue
                elif self.focus_strength_word != '' and self.focus_strength_word != i[7]:
                    continue
                elif self.focus_inst_word != '' and self.focus_inst_word not in i[8]:
                    continue
                elif self.focus_search_word != '' and self.focus_search_word not in i[0]:
                    continue
                else:
                    d = {'is_checked': False, 'button_name': {'text': i[0]}, 'button_rate': {'text': i[9]}, \
                    'label_time': {'text': i[10]}, 'file_pass': {'text': i[3]}, 'button_copy': {'text': 'C'}, \
                    'label_genre': {'text': i[5]}, 'label_brightness': {'text': i[6]}, 'label_strength': {'text': i[7]}, \
                    'label_instruments': {'text': i[8]}, 'album': {'text': i[1]}, 'artist': {'text': i[2]}, \
                    'slider': {'max': i[11]}, 'file_pass_sub': {'text': i[4]}, 'label_us': {'text': i[12]}}
                focus_data.append(d)
        self.display_recycle.data = focus_data
        self.display_recycle.data = sorted(self.display_recycle.data, key=lambda n: n['button_name']['text'])
        self.display_count_songs(self.display_recycle.data)

    def name_sort(self, *args):
        self.stop_for_switching()
        self.display_area_row_time_head.text = '[ref=time]time  ⇅[/ref]'
        self.display_area_row_time_head.color = [1, 1, 1, 1]
        if self.display_area_row_name_head.color == [1, 1, 1, 1]:
            self.display_area_row_name_head.color = [0, 1, 0, 1]
            self.display_area_row_name_head.text = '[ref=file name]file name  ↑[/ref]'
            self.display_recycle.data = sorted(self.display_recycle.data, key=lambda n: n['button_name']['text'], reverse=True)
        elif self.display_area_row_name_head.color != [1, 1, 1, 1]:
            self.display_area_row_name_head.color = [1, 1, 1, 1]
            self.display_area_row_name_head.text = '[ref=file name]file name  ↓[/ref]'
            self.display_recycle.data = sorted(self.display_recycle.data, key=lambda n: n['button_name']['text'])
        else:
            pass
            #self.display_area_row_name_head.color = [1, 1, 1, 1]
            #self.display_area_row_name_head.text = '[ref=file name]file name  ⇅[/ref]'
            #self.display_recycle.data = sorted(self.display_recycle.data, key=lambda n: n['button_name']['text'])

    def time_sort(self, *args):
        self.stop_for_switching()
        self.display_area_row_name_head.color = [1, 1, 1, 1]
        self.display_area_row_name_head.text = '[ref=file name]file name  ⇅[/ref]'
        if self.display_area_row_time_head.color == [1, 1, 1, 1]:
            self.display_area_row_time_head.color = [0, 1, 0, 1]
            self.display_area_row_time_head.text = '[ref=time]time  ↑[/ref]'
            self.time_sort_rev = True
            self.display_recycle.data = sorted(self.display_recycle.data, key=lambda n: n['label_time']['text'], reverse=True)
        else:
            if self.time_sort_rev == True:
                #self.display_area_row_time_head.color = [0, 1, 0, 1]
                self.display_area_row_time_head.text = '[ref=time]time  ↓[/ref]'
                self.time_sort_rev = False
                self.display_recycle.data = sorted(self.display_recycle.data, key=lambda n: n['label_time']['text'])
            else:
                self.display_area_row_time_head.text = '[ref=time]time  ↑[/ref]'
                self.time_sort_rev = True
                self.display_recycle.data = sorted(self.display_recycle.data, key=lambda n: n['label_time']['text'], reverse=True)

    def pressed_search(self, *args):
        self.focus_search_word = self.focus_area_top_input.text
        self.focus_display()

    def btn_genre_lighting(self, select, o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, o11, *args):
        if select.color == [0, 1, 0, 1]:
            select.color = [1, 1, 1, 1]
        else:
            select.color = [0, 1, 0, 1]
            o1.color = [1, 1, 1, 1]
            o2.color = [1, 1, 1, 1]
            o3.color = [1, 1, 1, 1]
            o4.color = [1, 1, 1, 1]
            o5.color = [1, 1, 1, 1]
            o6.color = [1, 1, 1, 1]
            o7.color = [1, 1, 1, 1]
            o8.color = [1, 1, 1, 1]
            o9.color = [1, 1, 1, 1]
            o10.color = [1, 1, 1, 1]
            o11.color = [1, 1, 1, 1]
            
    def genre_word(self, word, *args):
        if self.focus_genre_word == word:
            self.focus_genre_word = ''
        else:
            self.focus_genre_word = word

    def focus_2020_01(self, *args):
        word = '2020-01'
        self.genre_word(word)
        select = self.focus_genre_btn_2020_01
        other1 = self.focus_genre_btn_2019_02
        other2 = self.focus_genre_btn_2019_01
        other3 = self.focus_genre_btn_2018_02
        other4 = self.focus_genre_btn_2018_01
        other5 = self.focus_genre_btn_2017_02
        other6 = self.focus_genre_btn_2017_01
        other7 = self.focus_genre_btn_2016_02
        other8 = self.focus_genre_btn_2016_01
        other9 = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2019_02(self, *args):
        word = '2019-02'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        select = self.focus_genre_btn_2019_02
        other2 = self.focus_genre_btn_2019_01
        other3 = self.focus_genre_btn_2018_02
        other4 = self.focus_genre_btn_2018_01
        other5 = self.focus_genre_btn_2017_02
        other6 = self.focus_genre_btn_2017_01
        other7 = self.focus_genre_btn_2016_02
        other8 = self.focus_genre_btn_2016_01
        other9 = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2019_01(self, *args):
        word = '2019-01'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        select = self.focus_genre_btn_2019_01
        other3 = self.focus_genre_btn_2018_02
        other4 = self.focus_genre_btn_2018_01
        other5 = self.focus_genre_btn_2017_02
        other6 = self.focus_genre_btn_2017_01
        other7 = self.focus_genre_btn_2016_02
        other8 = self.focus_genre_btn_2016_01
        other9 = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2018_02(self, *args):
        word = '2018-02'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        other3 = self.focus_genre_btn_2019_01
        select = self.focus_genre_btn_2018_02
        other4 = self.focus_genre_btn_2018_01
        other5 = self.focus_genre_btn_2017_02
        other6 = self.focus_genre_btn_2017_01
        other7 = self.focus_genre_btn_2016_02
        other8 = self.focus_genre_btn_2016_01
        other9 = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2018_01(self, *args):
        word = '2018-01'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        other3 = self.focus_genre_btn_2019_01
        other4 = self.focus_genre_btn_2018_02
        select = self.focus_genre_btn_2018_01
        other5 = self.focus_genre_btn_2017_02
        other6 = self.focus_genre_btn_2017_01
        other7 = self.focus_genre_btn_2016_02
        other8 = self.focus_genre_btn_2016_01
        other9 = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2017_02(self, *args):
        word = '2017-02'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        other3 = self.focus_genre_btn_2019_01
        other4 = self.focus_genre_btn_2018_02
        other5 = self.focus_genre_btn_2018_01
        select = self.focus_genre_btn_2017_02
        other6 = self.focus_genre_btn_2017_01
        other7 = self.focus_genre_btn_2016_02
        other8 = self.focus_genre_btn_2016_01
        other9 = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2017_01(self, *args):
        word = '2017-01'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        other3 = self.focus_genre_btn_2019_01
        other4 = self.focus_genre_btn_2018_02
        other5 = self.focus_genre_btn_2018_01
        other6 = self.focus_genre_btn_2017_02
        select = self.focus_genre_btn_2017_01
        other7 = self.focus_genre_btn_2016_02
        other8 = self.focus_genre_btn_2016_01
        other9 = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2016_02(self, *args):
        word = '2016-02'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        other3 = self.focus_genre_btn_2019_01
        other4 = self.focus_genre_btn_2018_02
        other5 = self.focus_genre_btn_2018_01
        other6 = self.focus_genre_btn_2017_02
        other7 = self.focus_genre_btn_2017_01
        select = self.focus_genre_btn_2016_02
        other8 = self.focus_genre_btn_2016_01
        other9 = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2016_01(self, *args):
        word = '2016-01'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        other3 = self.focus_genre_btn_2019_01
        other4 = self.focus_genre_btn_2018_02
        other5 = self.focus_genre_btn_2018_01
        other6 = self.focus_genre_btn_2017_02
        other7 = self.focus_genre_btn_2017_01
        other8 = self.focus_genre_btn_2016_02
        select = self.focus_genre_btn_2016_01
        other9 = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2015(self, *args):
        word = '2015'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        other3 = self.focus_genre_btn_2019_01
        other4 = self.focus_genre_btn_2018_02
        other5 = self.focus_genre_btn_2018_01
        other6 = self.focus_genre_btn_2017_02
        other7 = self.focus_genre_btn_2017_01
        other8 = self.focus_genre_btn_2016_02
        other9 = self.focus_genre_btn_2016_01
        select = self.focus_genre_btn_2015
        other10 = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2014(self, *args):
        word = '2014'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        other3 = self.focus_genre_btn_2019_01
        other4 = self.focus_genre_btn_2018_02
        other5 = self.focus_genre_btn_2018_01
        other6 = self.focus_genre_btn_2017_02
        other7 = self.focus_genre_btn_2017_01
        other8 = self.focus_genre_btn_2016_02
        other9 = self.focus_genre_btn_2016_01
        other10 = self.focus_genre_btn_2015
        select = self.focus_genre_btn_2014
        other11 = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def focus_2012(self, *args):
        word = '2014'
        self.genre_word(word)
        other1 = self.focus_genre_btn_2020_01
        other2 = self.focus_genre_btn_2019_02
        other3 = self.focus_genre_btn_2019_01
        other4 = self.focus_genre_btn_2018_02
        other5 = self.focus_genre_btn_2018_01
        other6 = self.focus_genre_btn_2017_02
        other7 = self.focus_genre_btn_2017_01
        other8 = self.focus_genre_btn_2016_02
        other9 = self.focus_genre_btn_2016_01
        other10 = self.focus_genre_btn_2015
        other11 = self.focus_genre_btn_2014
        select = self.focus_genre_btn_2012
        self.focus_display()
        self.btn_genre_lighting(select, other1, other2, other3, other4, other5,\
             other6, other7, other8, other9, other10, other11)

    def btn_brightness_lighting(self, select, o1, o2, *args):
        if select.color == [0, 1, 0, 1]:
            select.color = [1, 1, 1, 1]
        else:
            select.color = [0, 1, 0, 1]
            o1.color = [1, 1, 1, 1]
            o2.color = [1, 1, 1, 1]

    def brightness_word(self, word, *args):
        if self.focus_brightness_word == word:
            self.focus_brightness_word = ''
        else:
            self.focus_brightness_word = word

    def focus_bright(self, *args):
        word = '明るめ'
        self.brightness_word(word)
        select = self.focus_brightness_btn_bright
        other1 = self.focus_brightness_btn_either
        other2 = self.focus_brightness_btn_dark
        self.focus_display()
        self.btn_brightness_lighting(select, other1, other2)

    def focus_either(self, *args):
        word = 'どちらとも言えない'
        self.brightness_word(word)
        other1 = self.focus_brightness_btn_bright
        select = self.focus_brightness_btn_either
        other2 = self.focus_brightness_btn_dark
        self.focus_display()
        self.btn_brightness_lighting(select, other1, other2)

    def focus_dark(self, *args):
        word = '暗め'
        self.brightness_word(word)
        other1 = self.focus_brightness_btn_bright
        other2 = self.focus_brightness_btn_either
        select = self.focus_brightness_btn_dark
        self.focus_display()
        self.btn_brightness_lighting(select, other1, other2)

    def btn_strength_lighting(self, select, o1, o2, o3, *args):
        if select.color == [0, 1, 0, 1]:
            select.color = [1, 1, 1, 1]
        else:
            select.color = [0, 1, 0, 1]
            o1.color = [1, 1, 1, 1]
            o2.color = [1, 1, 1, 1]
            o3.color = [1, 1, 1, 1]

    def strength_word(self, word, *args):
        if self.focus_strength_word == word:
            self.focus_strength_word = ''
        else:
            self.focus_strength_word = word

    def focus_strong(self, *args):
        word = '強い'
        self.strength_word(word)
        select = self.focus_strength_btn_strong
        other1 = self.focus_strength_btn_light
        other2 = self.focus_strength_btn_week
        other3 = self.focus_strength_btn_upturn
        self.focus_display()
        self.btn_strength_lighting(select, other1, other2, other3)

    def focus_light(self, *args):
        word = '少し強い'
        self.strength_word(word)
        other1 = self.focus_strength_btn_strong
        select = self.focus_strength_btn_light
        other2 = self.focus_strength_btn_week
        other3 = self.focus_strength_btn_upturn
        self.focus_display()
        self.btn_strength_lighting(select, other1, other2, other3)

    def focus_week(self, *args):
        word = '弱い'
        self.strength_word(word)
        other1 = self.focus_strength_btn_strong
        other2 = self.focus_strength_btn_light
        select = self.focus_strength_btn_week
        other3 = self.focus_strength_btn_upturn
        self.focus_display()
        self.btn_strength_lighting(select, other1, other2, other3)

    def focus_upturn(self, *args):
        word = '起伏系'
        self.strength_word(word)
        other1 = self.focus_strength_btn_strong
        other2 = self.focus_strength_btn_light
        other3 = self.focus_strength_btn_week
        select = self.focus_strength_btn_upturn
        self.focus_display()
        self.btn_strength_lighting(select, other1, other2, other3)

    def btn_inst_lighting(self, select, o1, o2, o3, o4, o5, o6, o7, *args):
        if select.color == [0, 1, 0, 1]:
            select.color = [1, 1, 1, 1]
        else:
            select.color = [0, 1, 0, 1]
            o1.color = [1, 1, 1, 1]
            o2.color = [1, 1, 1, 1]
            o3.color = [1, 1, 1, 1]
            o4.color = [1, 1, 1, 1]
            o5.color = [1, 1, 1, 1]
            o6.color = [1, 1, 1, 1]
            o7.color = [1, 1, 1, 1]

    def inst_word(self, word, *args):
        if self.focus_inst_word == word:
            self.focus_inst_word = ''
        else:
            self.focus_inst_word = word

    def focus_per(self, *args):
        word = 'パーカッション'
        self.inst_word(word)
        select = self.focus_inst_btn_per
        other1 = self.focus_inst_btn_piano
        other2 = self.focus_inst_btn_guitar
        other3 = self.focus_inst_btn_electric
        other4 = self.focus_inst_btn_orch
        other5 = self.focus_inst_btn_ensemble
        other6 = self.focus_inst_btn_ethnic
        other7 = self.focus_inst_btn_other
        self.focus_display()
        self.btn_inst_lighting(select, other1, other2, other3, other4, \
            other5, other6, other7)

    def focus_piano(self, *args):
        word = 'ピアノ'
        self.inst_word(word)
        other1 = self.focus_inst_btn_per
        select = self.focus_inst_btn_piano
        other2 = self.focus_inst_btn_guitar
        other3 = self.focus_inst_btn_electric
        other4 = self.focus_inst_btn_orch
        other5 = self.focus_inst_btn_ensemble
        other6 = self.focus_inst_btn_ethnic
        other7 = self.focus_inst_btn_other
        self.focus_display()
        self.btn_inst_lighting(select, other1, other2, other3, other4, \
            other5, other6, other7)

    def focus_guitar(self, *args):
        word = 'ギター'
        self.inst_word(word)
        other1 = self.focus_inst_btn_per
        other2 = self.focus_inst_btn_piano
        select = self.focus_inst_btn_guitar
        other3 = self.focus_inst_btn_electric
        other4 = self.focus_inst_btn_orch
        other5 = self.focus_inst_btn_ensemble
        other6 = self.focus_inst_btn_ethnic
        other7 = self.focus_inst_btn_other
        self.focus_display()
        self.btn_inst_lighting(select, other1, other2, other3, other4, \
            other5, other6, other7)

    def focus_electric(self, *args):
        word = '電子系'
        self.inst_word(word)
        other1 = self.focus_inst_btn_per
        other2 = self.focus_inst_btn_piano
        other3 = self.focus_inst_btn_guitar
        select = self.focus_inst_btn_electric
        other4 = self.focus_inst_btn_orch
        other5 = self.focus_inst_btn_ensemble
        other6 = self.focus_inst_btn_ethnic
        other7 = self.focus_inst_btn_other
        self.focus_display()
        self.btn_inst_lighting(select, other1, other2, other3, other4, \
            other5, other6, other7)

    def focus_orche(self, *args):
        word = 'オーケストラ大編成'
        self.inst_word(word)
        other1 = self.focus_inst_btn_per
        other2 = self.focus_inst_btn_piano
        other3 = self.focus_inst_btn_guitar
        other4 = self.focus_inst_btn_electric
        select = self.focus_inst_btn_orch
        other5 = self.focus_inst_btn_ensemble
        other6 = self.focus_inst_btn_ethnic
        other7 = self.focus_inst_btn_other
        self.focus_display()
        self.btn_inst_lighting(select, other1, other2, other3, other4, \
            other5, other6, other7)

    def focus_ensemble(self, *args):
        word = 'オーケストラ小編成'
        self.inst_word(word)
        other1 = self.focus_inst_btn_per
        other2 = self.focus_inst_btn_piano
        other3 = self.focus_inst_btn_guitar
        other4 = self.focus_inst_btn_electric
        other5 = self.focus_inst_btn_orch
        select = self.focus_inst_btn_ensemble
        other6 = self.focus_inst_btn_ethnic
        other7 = self.focus_inst_btn_other
        self.focus_display()
        self.btn_inst_lighting(select, other1, other2, other3, other4, \
            other5, other6, other7)

    def focus_ethnic(self, *args):
        word = '民族系'
        self.inst_word(word)
        other1 = self.focus_inst_btn_per
        other2 = self.focus_inst_btn_piano
        other3 = self.focus_inst_btn_guitar
        other4 = self.focus_inst_btn_electric
        other5 = self.focus_inst_btn_orch
        other6 = self.focus_inst_btn_ensemble
        select = self.focus_inst_btn_ethnic
        other7 = self.focus_inst_btn_other
        self.focus_display()
        self.btn_inst_lighting(select, other1, other2, other3, other4, \
            other5, other6, other7)

    def focus_other(self, *args):
        word = 'その他'
        self.inst_word(word)
        other1 = self.focus_inst_btn_per
        other2 = self.focus_inst_btn_piano
        other3 = self.focus_inst_btn_guitar
        other4 = self.focus_inst_btn_electric
        other5 = self.focus_inst_btn_orch
        other6 = self.focus_inst_btn_ensemble
        other7 = self.focus_inst_btn_ethnic
        select = self.focus_inst_btn_other
        self.focus_display()
        self.btn_inst_lighting(select, other1, other2, other3, other4, \
            other5, other6, other7)

    def volume_change(self, *args):
        if playing_pass:
            sound_box[0].volume = self.volume_bar.value
            volume_value[0] = self.volume_bar.value
        else:
            volume_value[0] = self.volume_bar.value

###ここからbuid
    def build(self):
        root = BoxLayout()
        root.orientation = "horizontal"

###focus+displayのselect_zoneエリアを用意
        select_zone = BoxLayout(size_hint=(0.9, 1))
        select_zone.orientation = "vertical"

###focusエリア
        focus_area = BoxLayout(size_hint=(1, .29))
        focus_area.orientation = "vertical"

        focus_area_top = BoxLayout(size_hint=(1, .2))
        focus_area_top.orientation = "horizontal"
        focus_area_top_spc = Label(text="", font_size = 12, size_hint=(.16, 1))
        focus_area_top_lbl = Label(text="Not Playing", font_size = 12, size_hint=(.68, 1), markup=True)
        playing_lbl.append(focus_area_top_lbl)
        focus_area_top_search_parent = BoxLayout(size_hint=(.16, 1))
        focus_area_top_search_parent.orientation = "vertical"
        focus_area_top_input_over = BoxLayout(size_hint=(1, .1))
        focus_area_top_search_middle = BoxLayout(size_hint=(1, .8))
        focus_area_top_search_middle.orientation = "horizontal"
        self.focus_area_top_input = TextInput(text="", font_size = 12, size_hint=(.75, 1))
        focus_area_top_btn = Button(text="search", font_size = 12, size_hint=(.25, 1), on_press=self.pressed_search)
        focus_area_top_search_middle.add_widget(self.focus_area_top_input)
        focus_area_top_search_middle.add_widget(focus_area_top_btn)
        focus_area_top_input_under = BoxLayout(size_hint=(1, .1))
        focus_area_top_search_parent.add_widget(focus_area_top_input_over)
        focus_area_top_search_parent.add_widget(focus_area_top_search_middle)
        focus_area_top_search_parent.add_widget(focus_area_top_input_under)
        focus_area_top.add_widget(focus_area_top_spc)
        focus_area_top.add_widget(focus_area_top_lbl)
        focus_area_top.add_widget(focus_area_top_search_parent)
        #focus_area_top.add_widget(focus_area_top_btn)

        focus_area_bottom = BoxLayout(size_hint=(1, .8))
        focus_area_bottom.orientation = "horizontal"

        focus_btn_height = 30

        ###focus_genre
        focus_genre_box = BoxLayout(size_hint=(.25, 1))
        focus_genre_box.orientation = "vertical"

        focus_genre_title = BoxLayout(size_hint=(1, .12))
        focus_genre_title_lbl = Label(text="ジャンル", font_size = 12, height=30, size_hint=(1, None))
        focus_genre_title.add_widget(focus_genre_title_lbl)

        sv_focus_genre = ScrollView(size_hint=(1, .88))
        focus_genre = BoxLayout(size_hint=(1, None))
        focus_genre.orientation = "vertical"
        focus_genre.bind(minimum_height=focus_genre.setter('height'))

        self.focus_genre_btn_2020_01 = Button(text='2020-01', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2020_01)
        self.focus_genre_btn_2019_02 = Button(text='2019-02', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2019_02)
        self.focus_genre_btn_2019_01 = Button(text='2019-01', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2019_01)
        self.focus_genre_btn_2018_02 = Button(text='2018-02', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2018_02)
        self.focus_genre_btn_2018_01 = Button(text='2018-01', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2018_01)
        self.focus_genre_btn_2017_02 = Button(text='2017-02', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2017_02)
        self.focus_genre_btn_2017_01 = Button(text='2017-01', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2017_01)
        self.focus_genre_btn_2016_02 = Button(text='2016-02', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2016_02)
        self.focus_genre_btn_2016_01 = Button(text='2016-01', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2016_01)
        self.focus_genre_btn_2015 = Button(text='2015', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2015)
        self.focus_genre_btn_2014 = Button(text='2014', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2014)
        self.focus_genre_btn_2012 = Button(text='2012', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_2012)

        focus_genre.add_widget(self.focus_genre_btn_2020_01)
        focus_genre.add_widget(self.focus_genre_btn_2019_02)
        focus_genre.add_widget(self.focus_genre_btn_2019_01)
        focus_genre.add_widget(self.focus_genre_btn_2018_02)
        focus_genre.add_widget(self.focus_genre_btn_2018_01)
        focus_genre.add_widget(self.focus_genre_btn_2017_02)
        focus_genre.add_widget(self.focus_genre_btn_2017_01)
        focus_genre.add_widget(self.focus_genre_btn_2016_02)
        focus_genre.add_widget(self.focus_genre_btn_2016_01)
        focus_genre.add_widget(self.focus_genre_btn_2015)
        focus_genre.add_widget(self.focus_genre_btn_2014)
        focus_genre.add_widget(self.focus_genre_btn_2012)

        focus_genre_box.add_widget(focus_genre_title)
        sv_focus_genre.add_widget(focus_genre)
        focus_genre_box.add_widget(sv_focus_genre)

        focus_area_bottom.add_widget(focus_genre_box)

        ###focus_brightness
        focus_brightness_box = BoxLayout(size_hint=(.25, 1))
        focus_brightness_box.orientation = "vertical"

        focus_brightness_title = BoxLayout(size_hint=(1, .12))
        focus_brightness_title_lbl = Label(text="明るさの印象", font_size = 12, height=30, size_hint=(1, None))
        focus_brightness_title.add_widget(focus_brightness_title_lbl)

        sv_focus_brightness = ScrollView(size_hint=(1, .88))
        focus_brightness = BoxLayout(size_hint=(1, None))
        focus_brightness.orientation = "vertical"
        focus_brightness.bind(minimum_height=focus_brightness.setter('height'))

        self.focus_brightness_btn_bright = Button(text='明るめ', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_bright)
        self.focus_brightness_btn_either = Button(text='どちらとも言えない', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_either)
        self.focus_brightness_btn_dark = Button(text='暗め', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_dark)

        focus_brightness.add_widget(self.focus_brightness_btn_bright)
        focus_brightness.add_widget(self.focus_brightness_btn_either)
        focus_brightness.add_widget(self.focus_brightness_btn_dark)

        focus_brightness_box.add_widget(focus_brightness_title)
        sv_focus_brightness.add_widget(focus_brightness)
        focus_brightness_box.add_widget(sv_focus_brightness)

        focus_area_bottom.add_widget(focus_brightness_box)

        ###focus_strength
        focus_strength_box = BoxLayout(size_hint=(.25, 1))
        focus_strength_box.orientation = "vertical"

        focus_strength_title = BoxLayout(size_hint=(1, .12))
        focus_strength_title_lbl = Label(text="強さの印象", font_size = 12, height=30, size_hint=(1, None))
        focus_strength_title.add_widget(focus_strength_title_lbl)

        sv_focus_strength = ScrollView(size_hint=(1, .88))
        focus_strength = BoxLayout(size_hint=(1, None))
        focus_strength.orientation = "vertical"
        focus_strength.bind(minimum_height=focus_strength.setter('height'))

        self.focus_strength_btn_strong = Button(text='強い', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_strong)
        self.focus_strength_btn_light = Button(text='少し強い', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_light)
        self.focus_strength_btn_week = Button(text='弱い', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_week)
        self.focus_strength_btn_upturn = Button(text='起伏系', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_upturn)

        focus_strength.add_widget(self.focus_strength_btn_strong)
        focus_strength.add_widget(self.focus_strength_btn_light)
        focus_strength.add_widget(self.focus_strength_btn_week)
        focus_strength.add_widget(self.focus_strength_btn_upturn)

        focus_strength_box.add_widget(focus_strength_title)
        sv_focus_strength.add_widget(focus_strength)
        focus_strength_box.add_widget(sv_focus_strength)

        focus_area_bottom.add_widget(focus_strength_box)

        ###focus_instrument
        focus_inst_box = BoxLayout(size_hint=(.25, 1))
        focus_inst_box.orientation = "vertical"

        focus_inst_title = BoxLayout(size_hint=(1, .12))
        focus_inst_title_lbl = Label(text="主な楽器", font_size = 12, height=30, size_hint=(1, None))
        focus_inst_title.add_widget(focus_inst_title_lbl)

        sv_focus_inst = ScrollView(size_hint=(1, .88))
        focus_inst = BoxLayout(size_hint=(1, None))
        focus_inst.orientation = "vertical"
        focus_inst.bind(minimum_height=focus_inst.setter('height'))

        self.focus_inst_btn_per = Button(text='パーカッション', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_per)
        self.focus_inst_btn_piano = Button(text='ピアノ', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_piano)
        self.focus_inst_btn_guitar = Button(text='ギター', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_guitar)
        self.focus_inst_btn_electric = Button(text='電子系', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_electric)
        self.focus_inst_btn_orch = Button(text='オーケストラ大編成', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_orche)
        self.focus_inst_btn_ensemble = Button(text='オーケストラ小編成', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_ensemble)
        self.focus_inst_btn_ethnic = Button(text='民族系', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_ethnic)
        self.focus_inst_btn_other = Button(text='その他', font_size = 12, height=focus_btn_height, size_hint=(1, None), on_press=self.focus_other)

        focus_inst.add_widget(self.focus_inst_btn_per)
        focus_inst.add_widget(self.focus_inst_btn_piano)
        focus_inst.add_widget(self.focus_inst_btn_guitar)
        focus_inst.add_widget(self.focus_inst_btn_electric)
        focus_inst.add_widget(self.focus_inst_btn_orch)
        focus_inst.add_widget(self.focus_inst_btn_ensemble)
        focus_inst.add_widget(self.focus_inst_btn_ethnic)
        focus_inst.add_widget(self.focus_inst_btn_other)

        focus_inst_box.add_widget(focus_inst_title)
        sv_focus_inst.add_widget(focus_inst)
        focus_inst_box.add_widget(sv_focus_inst)

        focus_area_bottom.add_widget(focus_inst_box)

        focus_area.add_widget(focus_area_top)
        focus_area.add_widget(focus_area_bottom)

###displayエリア
        sv_display_area = ScrollView(size_hint=(1, .69))

        self.display()

        sv_display_area.add_widget(self.display_area)

###footerエリア
        display_area_footer = BoxLayout(size_hint=(1, .02))
        display_area_footer.orientation = "horizontal"
        display_area_footer_leftspc = BoxLayout(size_hint=(.3, 1))
        self.display_area_footer_label = Label(text='', font_size = 10, size_hint=(.4, 1))
        footer_lbl.append(self.display_area_footer_label)
        self.display_area_footer_rightlabel = Label(text='', font_size = 10, size_hint=(.3, 1), markup=True)
        footer_rightlbl.append(self.display_area_footer_rightlabel)
        display_area_footer.add_widget(display_area_footer_leftspc)
        display_area_footer.add_widget(self.display_area_footer_label)
        display_area_footer.add_widget(self.display_area_footer_rightlabel)
        self.display_count_songs(self.display_recycle.data)

        select_zone.add_widget(focus_area)
        select_zone.add_widget(sv_display_area)
        select_zone.add_widget(display_area_footer)

###volume+tagのpanel_zoneエリアを用意
        panel_zone = BoxLayout(size_hint=(0.1, 1))
        panel_zone.orientation = "vertical"
        panel_zone.bind(minimum_height=panel_zone.setter('height'))

###volumeエリアを用意
        volume_area = BoxLayout(size_hint=(1, .1))
        volume_area.orientation = "vertical"
        volume_area.bind(minimum_height=volume_area.setter('height'))
        lbl_volume = Label(text='ボリューム', font_size = 12, size_hint =(1, .5))
        self.volume_bar = Slider(min=0, max=1, value=1, cursor_width=25, cursor_height=25, size_hint =(1, .5))
        self.volume_bar.bind(value=self.volume_change)
        volume_area.add_widget(lbl_volume)
        volume_area.add_widget(self.volume_bar)

###tagエリアを用意
        tag_area = BoxLayout(size_hint=(1, .9))
        tag_area.orientation = "vertical"

        tag_btn_height = 30

        #tag_brightness
        sv_tag_area_brightness = ScrollView(size_hint=(1, .20))
        tag_area_brightness = BoxLayout(size_hint =(1, None))
        tag_area_brightness.orientation = "vertical"
        tag_area_brightness.bind(minimum_height=tag_area_brightness.setter('height'))
        tag_area_brightness_lbl = Label(text="明るさの印象", font_size=12, height=tag_btn_height, size_hint=(1, None))
        self.tag_brightness_btn0 = Button(text="明るめ", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_bright)
        self.tag_brightness_btn1 = Button(text="どちらとも言えない", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_either)
        self.tag_brightness_btn2 = Button(text="暗め", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_dark)

        tag_area_brightness.add_widget(tag_area_brightness_lbl)
        tag_area_brightness.add_widget(self.tag_brightness_btn0)
        tag_area_brightness.add_widget(self.tag_brightness_btn1)
        tag_area_brightness.add_widget(self.tag_brightness_btn2)

        sv_tag_area_brightness.add_widget(tag_area_brightness)

        #tag_strength
        sv_tag_area_strength = ScrollView(size_hint=(1, .25))
        tag_area_strength = BoxLayout(size_hint =(1, None))
        tag_area_strength.orientation = "vertical"
        tag_area_strength.bind(minimum_height=tag_area_strength.setter('height'))
        tag_area_strength_lbl = Label(text="強さの印象", font_size=12, height=tag_btn_height, size_hint=(1, None))
        self.tag_strength_btn0 = Button(text="強い", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_strong)
        self.tag_strength_btn1 = Button(text="少し強い", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_light)
        self.tag_strength_btn2 = Button(text="弱い", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_week)
        self.tag_strength_btn3 = Button(text="起伏系", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_upturn)

        tag_area_strength.add_widget(tag_area_strength_lbl)
        tag_area_strength.add_widget(self.tag_strength_btn0)
        tag_area_strength.add_widget(self.tag_strength_btn1)
        tag_area_strength.add_widget(self.tag_strength_btn2)
        tag_area_strength.add_widget(self.tag_strength_btn3)

        sv_tag_area_strength.add_widget(tag_area_strength)

        #tag_instrument
        sv_tag_area_inst = ScrollView(size_hint=(1, .5))
        tag_area_inst = BoxLayout(size_hint =(1, None))
        tag_area_inst.orientation = "vertical"
        tag_area_inst.bind(minimum_height=tag_area_inst.setter('height'))
        tag_area_inst_lbl = Label(text="主な楽器(複数選択可)", font_size=12, height=tag_btn_height, size_hint=(1, None))
        self.tag_inst_btn_per = Button(text="パーカッション", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_per)
        self.tag_inst_btn_piano = Button(text="ピアノ", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_piano)
        self.tag_inst_btn_guitar = Button(text="ギター", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_guitar)
        self.tag_inst_btn_electric = Button(text="電子系", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_electric)
        self.tag_inst_btn_orch = Button(text="オーケストラ大編成", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_orche)
        self.tag_inst_btn_ensemble = Button(text="オーケストラ小編成", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_ensemble)
        self.tag_inst_btn_ethnic = Button(text="民族系", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_ethnic)
        self.tag_inst_btn_other = Button(text="その他", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_other)

        tag_area_inst.add_widget(tag_area_inst_lbl)
        tag_area_inst.add_widget(self.tag_inst_btn_per)
        tag_area_inst.add_widget(self.tag_inst_btn_piano)
        tag_area_inst.add_widget(self.tag_inst_btn_guitar)
        tag_area_inst.add_widget(self.tag_inst_btn_electric)
        tag_area_inst.add_widget(self.tag_inst_btn_orch)
        tag_area_inst.add_widget(self.tag_inst_btn_ensemble)
        tag_area_inst.add_widget(self.tag_inst_btn_ethnic)
        tag_area_inst.add_widget(self.tag_inst_btn_other)

        sv_tag_area_inst.add_widget(tag_area_inst)

        #tag_US
        tag_area_us = BoxLayout(size_hint =(1, .05))
        tag_area_us.orientation = "vertical"
        tag_area_us.bind(minimum_height=tag_area_us.setter('height'))
        tag_area_us_lbl = Label(text="Under Score", font_size=12, height=tag_btn_height, size_hint=(1, None))
        self.tag_us_btn = Button(text="Under Score", font_size=12, height=tag_btn_height, size_hint=(1, None), on_press=self.tag_pressed_us)

        tag_area_us.add_widget(tag_area_us_lbl)
        tag_area_us.add_widget(self.tag_us_btn)


        tag_area.add_widget(sv_tag_area_brightness)
        tag_area.add_widget(sv_tag_area_strength)
        tag_area.add_widget(sv_tag_area_inst)
        tag_area.add_widget(tag_area_us)

        panel_zone.add_widget(volume_area)
        panel_zone.add_widget(tag_area)


        root.add_widget(select_zone)
        root.add_widget(panel_zone)

#        print('list of read_error is')
#        print(self.read_error)

        return root


if __name__=="__main__":
    MainScreen().run()



# データベースへのアクセスが終わったら close する
conn.close()