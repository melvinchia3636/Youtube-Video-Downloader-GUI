from tkinter import * #import tkinter for the main GUI design
from tkinter.font import Font #import this to make the font look cooler
import tkinter.messagebox as ms
import tkinter.ttk as ttk #for the progressbar ONLY
from PIL import ImageTk, Image #import this to load the image
#from custom_pytube import YouTube #to download Youtube data
import ctypes #to show message box
from time import sleep
import requests
import threading
from bs4 import BeautifulSoup
import re
import json
import youtube_dl

#get the videos data from youtube
def SearchVid(search):
    
    global main_data 
    title = []
    vid_id = 0
    vid_length = []
    vid_uploader = []
    temp_list = []
    upload_date = []
    vid_views = []
    vid_url = []
    raw = [i['videoRenderer'] for i in json.loads(re.findall(r'var ytInitialData = (.*?)</script>', str(BeautifulSoup(requests.get('https://www.youtube.com/results?search_query='+'+'.join(search.split())).content.decode('utf-8', 'ignore'), 'lxml')))[0][:-1])['contents']['twoColumnSearchResultsRenderer']["primaryContents"]['sectionListRenderer']['contents'][-2]['itemSectionRenderer']['contents'] if 'videoRenderer' in i]

    for i in raw:
        temp_list.append({
                'id': i["videoId"],
                'title': i['title']['runs'][0]['text'],
                'uploader': i['ownerText']['runs'][0]['text'],
                'description': ''.join(j['text'] for j in i['descriptionSnippet']['runs']) if 'descriptionSnippet' in i else '',
                'length': i['lengthText']['simpleText'] if 'lengthText' in i else '',
                'upload_time': i['publishedTimeText']['simpleText'] if 'publishedTimeText' in i else '',
                'view_count': i['viewCountText']['simpleText'] if 'viewCountText' in i and 'simpleText' in i['viewCountText'] else ''
            })
    main_data = temp_list

#downlaod the video
def download_vid(vidid_to_download, result):
    #start download
    def start():
        global file_size
        try:
            with youtube_dl.YoutubeDL({'include_ads': False, 'format': 'best'}) as ydl:
                ydl.download([url_to_download]) 
        except:
            start()

    global url_to_download
    global filesize
    global progressbar
    global pw

    #quit the app
    def quit_win():
        pw.destroy()
        quit()

    def quitbutton_on_enter(e):
        quit_button['background'] = '#565656'
        quit_button['fg'] = 'white'

    def quitbutton_on_leave(e):
        quit_button['background'] = '#252525'
        quit_button['fg'] = 'white'
    
    url_to_download = 'https://www.youtube.com/watch?v='+main_data[vidid_to_download-1]['id']
    root.destroy()
    pw = Tk()
    titlefont = Font(size=20, family='Gotham')
    buttonfont = Font(size=15, family='Gotham')
    pw.resizable(False, False)
    pw.config(bg="#252525")
    pw.geometry('650x300')
    pw.iconbitmap('assets/icon.ico')
    pw.title('Youtube Video Downloader')
    s = ttk.Style()
    s.theme_use('clam')
    print(s.theme_names())
    TROUGH_COLOR = '#252525'
    BAR_COLOR = '#00FFFF'
    s.configure("green.flat.Horizontal.TProgressbar", troughcolor=TROUGH_COLOR, bordercolor=BAR_COLOR, background=BAR_COLOR, lightcolor=BAR_COLOR, darkcolor=BAR_COLOR, borderwidth=0)
    title = Label(pw, text='', wraplength=500, font=titlefont, bg='#252525', fg = 'white')
    progressbar=ttk.Progressbar(pw, style="green.flat.Horizontal.TProgressbar",orient="horizontal",length=600,mode="determinate")
    title.grid(row=0, column=0)
    progressbar.grid(row=1,column=0, ipady=10, padx=25, pady=20)
    progressbar['value']=0
    progressbar['maximum']=100
    file_size = 0
    pw.update()
    label = Label(pw, text='Downloading', font=titlefont, bg='#252525', fg = 'white')
    label.grid(row=2,column=0)
    start()
    label.grid_forget()
    label = Label(pw, text='Download completed', font=titlefont, bg='#252525', fg = 'white').grid(row=2,column=0)
    quitbuttoninputframe = Frame(pw, width=224, height=50.45, background='#00FFFF', borderwidth=1.45)
    quit_button = Button(
        pw,
        activebackground='#565656',
        activeforeground='white',
        command=quit_win,
        fg='white',
        text='CLOSE',
        font=buttonfont,
        padx=67,
        pady=5,
        bg='#252525',
        relief=FLAT)
    quitbuttoninputframe.grid(row=3, column=0, pady=15)
    quit_button.grid(row=3, column=0, pady=15)
    quit_button.bind("<Enter>", quitbutton_on_enter)
    quit_button.bind("<Leave>", quitbutton_on_leave)

#show the result page
def searchvideo():

    global main_data, current

    main_data = []

    #prepare to downlaod
    def proceed():
        
        proceedid = int(id_search_input.get())
        download_vid(proceedid, main_data)
    
    search_keyword = search_input.get()
    if search_keyword == '' or search_keyword == 'keyword here':
        ms.showwarning('WARNING', 'Don\'t left the search box blank!')
    else:
        try:
            current = Label(root, text='', bg='#252525', fg='white')
            current.place(x=225, y=300, anchor='center')
            x = threading.Thread(target=SearchVid, args=(search_keyword, ))
            x.start()
            while not main_data:
                root.update()
                
            searchframe.place_forget()
            search_input.place_forget()
            submitbuttoninputframe.place_forget()
            submit_button.place_forget()
            quitbuttoninputframe.place_forget()
            quit_button.place_forget()

            root.geometry('920x500')

            def id_on_click(event):
                id_search_input.configure(state=NORMAL)
                id_search_input.delete(0, END)
                id_search_input.unbind('<Button-1>', id_on_click_id)

            def limiturlinput(*args):
                value = videoinput_id.get()
                if value.isdigit() and len(value) == 2 and 1<= int(value) <= len(main_data):
                    proceed_btn.config(state=NORMAL)
                    root.update()
                else:
                    proceed_btn.config(state=DISABLED)
                    root.update()

            def pbutton_on_enter(e):
                proceed_btn['background'] = '#565656'
                proceed_btn['fg'] = 'white'

            def pbutton_on_leave(e):
                proceed_btn['background'] = '#252525'
                proceed_btn['fg'] = 'white'

            videoinput_id = StringVar()
            videoinput_id.trace_add('write', limiturlinput)

            title.place_forget()
            titleicon.place_forget()
            scrollbar = Scrollbar(root)
            titleshowframe = Frame(root, width=876, height=142,background = '#00FFFF', borderwidth = 1, relief = FLAT)
            result_list = Listbox(root, yscrollcommand=scrollbar.set, selectmode=BROWSE, highlightthickness=0, selectbackground='#252525',selectborderwidth=0, width=58, fg='white', relief=FLAT, height=4, font=frameFont, bg='#252525')
            scrollbar.config(command=result_list.yview)
            vid_id = 1 
            for i in main_data:
                result_list.insert(END, 'video ID: '+str(vid_id))
                result_list.insert(END, 'title: '+i['title'])
                result_list.insert(END, 'video length: '+i['length'])
                result_list.insert(END, 'upload time: '+i['upload_time'])
                vid_id+=1

            instrulabel = Label(root, font = instrufont, bg='#252525', fg='white', text='Scroll on the listbox above to explore the search results\nEnter the video id into entry below and press proceed')
            id_searchframe = Frame(root, width=409, height=62,background='#00FFFF', borderwidth=1)
            id_search_input = Entry(root, textvariable=videoinput_id, disabledbackground='#252525', font=inputfont, borderwidth=0, fg='white', bg='#252525', relief=FLAT, justify=CENTER, width=27)
            id_search_input.config(insertbackground='white')
            pbuttoninputframe = Frame(root, width=204.45, height=52.45, background='#00FFFF', borderwidth=1.45)


            proceed_btn = Button(root,
                activebackground='#565656',
                command=proceed,
                activeforeground='white',
                fg='white',
                text='PROCEED',
                state=DISABLED,
                font=buttonfont,
                bg='#252525',
                relief=FLAT)

            titleicon.place(x=245,y=15)
            title.place(x=295,y=20)
            titleshowframe.place(x=20, y=79)
            result_list.place(x=22,y=81)
            instrulabel.place(x=110, y=250)
            id_searchframe.place(x=255,y=340)
            id_search_input.place(x=256,y=341, height=60)
            id_search_input.insert(0, 'ID')
            id_search_input.configure(state=DISABLED)
            id_on_click_id = id_search_input.bind('<Button-1>', id_on_click)
            pbuttoninputframe.place(x=360,y=440)
            proceed_btn.place(x=361,y=441, width=202, height=50)
            proceed_btn.bind("<Enter>", pbutton_on_enter)
            proceed_btn.bind("<Leave>", pbutton_on_leave)
        except:
            raise
            ms.showwarning('KEYWORD ERROR','Invalid Keyword!')

#the main_menu
def main_menu():
    global mainicon
    global search_input
    global searchframe
    global search_input
    global submitbuttoninputframe
    global submit_button
    global quitbuttoninputframe
    global quit_button
    global title
    global titleicon

    def button_on_enter(e):
        submit_button['background'] = '#565656'
        submit_button['fg'] = 'white'

    def button_on_leave(e):
        submit_button['background'] = '#252525'
        submit_button['fg'] = 'white'

    def quitbutton_on_enter(e):
        quit_button['background'] = '#565656'
        quit_button['fg'] = 'white'

    def quitbutton_on_leave(e):
        quit_button['background'] = '#252525'
        quit_button['fg'] = 'white'

    def on_click(event):
        search_input.configure(state=NORMAL)
        search_input.delete(0, END)
        search_input.unbind('<Button-1>', on_click_id)

    def quitmenu():
        root.destroy()
        quit()
    
    titleicon = Label(root, image=mainicon,bg = '#252525')
    title = Label(root, text='Youtube Video Downloader', fg='white', bg='#252525', font=titlefont)
    searchframe = Frame(root, width=409, height=47,background='#00FFFF', borderwidth=1)
    search_input = Entry(root, disabledbackground='#252525', font=inputfont, borderwidth=0, fg='white', bg='#252525', relief=FLAT, justify=CENTER, width=27)
    search_input.config(insertbackground='white')
    submitbuttoninputframe = Frame(root, width=193.45, height=52.45, background='#00FFFF', borderwidth=1.45)
    submit_button = Button(
        root,
        command=searchvideo,
        activebackground='#565656',
        activeforeground='white',
        fg='white',text='SEARCH',
        font=buttonfont,
        bg='#252525',
        relief=FLAT)
    
    quitbuttoninputframe = Frame(root, width=193.45, height=52.45, background='#00FFFF', borderwidth=1.45)
    quit_button = Button(
        root,
        activebackground='#565656',
        activeforeground='white',
        command=quitmenu,
        fg='white',
        text='QUIT',
        font=buttonfont,
        bg='#252525',
        relief=FLAT)

    titleicon.place(x=10,y=15)
    title.place(x=70,y=20)
    searchframe.place(x=20,y=100)
    search_input.place(x=21,y=101, height=45)
    submitbuttoninputframe.place(x=125,y=170)
    submit_button.place(x=126.45,y=171.45, width=191, height=50)
    quitbuttoninputframe.place(x=125,y=230)
    quit_button.place(x=126.45,y=231.45, width=191, height=50)
    submit_button.bind("<Enter>", button_on_enter)
    submit_button.bind("<Leave>", button_on_leave)
    search_input.insert(0, 'keyword here')
    search_input.configure(state=DISABLED)
    on_click_id = search_input.bind('<Button-1>', on_click)
    quit_button.bind("<Enter>", quitbutton_on_enter)
    quit_button.bind("<Leave>", quitbutton_on_leave)

if __name__ == '__main__':
    try:
        requests.get('https://www.youtube.com')
        global root

        root = Tk()
        root.geometry('450x330')
        root.config(bg='#252525')
        root.resizable(False,False)
        root.title('YouTube Video Downloader')
        root.iconbitmap('assets/icon.ico')

        global titlefont
        global inputfont
        global buttonfont
        global framefont
        global instrufont

        frameFont = Font(size=20, family='Bahnschrift Light')
        inputfont = Font(size=20, family='Bahnschrift Light')
        titlefont = Font(size=20, family='Consolas')
        buttonfont = Font(size=15)
        instrufont = Font(size=20, family='Bahnschrift SemiLight')

        mainicon = ImageTk.PhotoImage(Image.open("assets/mainicon.png"))
        main_menu()
        root.mainloop()
    except:
        raise
        quit()

