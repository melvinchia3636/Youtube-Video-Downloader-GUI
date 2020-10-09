from tkinter import * #import tkinter for the main GUI design
from tkinter.font import Font #import this to make the font look cooler
import tkinter.messagebox as ms
import tkinter.ttk as ttk #for the progressbar ONLY
from PIL import ImageTk, Image #import this to load the image
from pytube import YouTube #to download Youtube data
import ctypes #to show message box
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests
import threading
from tkinter import * #import tkinter for the main GUI design
from tkinter.font import Font #import this to make the font look cooler
import tkinter.messagebox as ms
import tkinter.ttk as ttk #for the progressbar ONLY
from PIL import ImageTk, Image #import this to load the image
from pytube import YouTube #to download Youtube data
import ctypes #to show message box
from time import sleep
import requests
import threading
import googleapiclient.discovery

#get the videos data from youtube
def SearchVid(search):
    
    global main_data 
    title = []
    vid_id = 0
    vid_uploader = []
    temp_list = []
    upload_date = []
    vid_views = []
    vid_url = []

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAyIDPArq8LQ36l5hRIuhn9n7elVfDr1RI"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q="HermitCraft"
    )
    response = request.execute()

    for i in response['items']:
        if i['id']['kind'] == 'youtube#video':
            vid_url.append(i['id']['videoId'])
            title.append(i['snippet']['title'])
            vid_uploader.append(i['snippet']['channelTitle'])
            upload_date.append(i['snippet']['publishTime'])
    
    temp_main_data =  list(enumerate(list(zip(vid_url, title, vid_uploader, upload_date))))
    for i in range(len(temp_main_data)):
        temp_main_data[i] = list(temp_main_data[i])
        temp_main_data[i][0] += 1
        

    main_data = temp_main_data

#downlaod the video
def download_vid(vidid_to_download, result):
    global file_size
    def progress_Check(stream = None, chunk = None,remaining = None): 
        percent = (100*(file_size-remaining))/file_size
        progressbar['value']=percent
        pw.update()

    #start download
    def start():
        global file_size
        video = YouTube('www.youtube.com?v='+url_to_download, on_progress_callback=progress_Check)
        video_type = video.streams.filter(progressive = True, file_extension = "mp4").last()
        file_size = video_type.filesize
        video_type.download('Downloads')

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
    
    url_to_download = result[vidid_to_download-1][1][0]
    root.destroy()
    pw = Tk()
    titlefont = Font(size=20, family='Gotham')
    buttonfont = Font(size=15, family='Gotham')
    vid_title = YouTube('www.youtube.com?v='+url_to_download).title.encode('utf-8')
    pw.resizable(False, False)
    pw.config(bg="#252525")
    pw.geometry('650x300')
    pw.iconbitmap('icon.ico')
    pw.title('Youtube Video Downloader')
    s = ttk.Style()
    s.theme_use('clam')
    TROUGH_COLOR = '#252525'
    BAR_COLOR = '#00FFFF'
    s.configure("green.flat.Horizontal.TProgressbar", troughcolor=TROUGH_COLOR, bordercolor=BAR_COLOR, background=BAR_COLOR, lightcolor=BAR_COLOR, darkcolor=BAR_COLOR, borderwidth=0)
    title = Label(pw, text=vid_title,wraplength=500, font=titlefont, bg='#252525', fg = 'white')
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
    quitbuttoninputframe = Frame(pw, width=211.45, height=52.45, background='#00FFFF', borderwidth=1.45)
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
    print(search_keyword)
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
                value = id_search_input.get()
                try:
                    int(value)
                except:
                    videoinput_id.set(value[:0])
                if value == 'ID':
                    proceed_btn.place_forget()
                    proceed_btn.config(state=DISABLED)
                    proceed_btn.place(x=361,y=441, width=202, height=50)
                if len(value) < 2:
                    proceed_btn.place_forget()
                    proceed_btn.config(state=DISABLED)
                    proceed_btn.place(x=361,y=441, width=202, height=50)
                    try:
                        int(value)
                    except:
                        videoinput_id.set(value[:0])
                elif len(value) >= 2:
                    videoinput_id.set(value[:2])
                    proceed_btn.place_forget()
                    proceed_btn.config(state=NORMAL)
                    proceed_btn.place(x=361,y=441, width=202, height=50)
                    if len(value) == 2 and value !='ID':
                        try:
                            int(value)
                            videoinput_id.set(str(len(main_data)-1)) if int(value) > len(main_data) else videoinput_id
                        except:
                            videoinput_id.set(value[:1])
                            proceed_btn.place_forget()
                            proceed_btn.config(state=DISABLED)
                            proceed_btn.place(x=361,y=441, width=202, height=50)
                else:
                    proceed_btn.place_forget()
                    proceed_btn.config(state=DISABLED)
                    proceed_btn.place(x=361,y=441, width=202, height=50)

            def pbutton_on_enter(e):
                proceed_btn['background'] = '#565656'
                proceed_btn['fg'] = 'white'

            def pbutton_on_leave(e):
                proceed_btn['background'] = '#252525'
                proceed_btn['fg'] = 'white'

            videoinput_id = StringVar()
            videoinput_id.trace('w', limiturlinput)

            title.place_forget()
            titleicon.place_forget()
            scrollbar = Scrollbar(root)
            titleshowframe = Frame(root, width=876, height=142,background = '#00FFFF', borderwidth = 1, relief = FLAT)
            result_list = Listbox(root, yscrollcommand=scrollbar.set, selectmode=BROWSE, highlightthickness=0, selectbackground='#252525',selectborderwidth=0, width=58, fg='white', relief=FLAT, height=4, font=frameFont, bg='#252525')
            scrollbar.config(command=result_list.yview)
            
            for i in main_data:
                result_list.insert(END, i[0])
                result_list.insert(END, i[1][1])
                result_list.insert(END, i[1][2])
                result_list.insert(END, i[1][3])

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
        root.iconbitmap('icon.ico')

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

        mainicon = ImageTk.PhotoImage(Image.open("mainicon.png"))
        main_menu()
        root.mainloop()
    except:
        raise
        quit()


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

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    current.config(text='Opening Webpage')
    driver.get('https://www.youtube.com/results?search_query='+'+'.join(search.split()))
    current.config(text='Waiting')
    sleep(3)
    for i in driver.find_elements_by_class_name('style-scope ytd-video-renderer'):
        current.config(text='Getting Title')
        title.append(i.find_element_by_id('video-title').find_element_by_tag_name('yt-formatted-string').get_attribute('innerHTML')[:40]+'...')
        current.config(text='Getting Video Length')
        vid_length.append(i.find_element_by_class_name('style-scope ytd-thumbnail').find_element_by_tag_name('span').get_attribute('innerHTML').strip())
        current.config(text='Getting Video Uploader')
        vid_uploader.append(i.find_element_by_class_name('style-scope ytd-channel-name').find_element_by_tag_name('a').get_attribute('innerHTML'))
        current.config(text='Getting Video Metadata')
        for i2 in (i.find_element_by_id('metadata-line').find_elements_by_tag_name('span')):
            temp_list.append(i2.get_attribute('innerHTML'))
        current.config(text='Getting Video Url')
        vid_url.append(i.find_element_by_id('video-title').get_attribute('href'))
    vid_views = temp_list[::2]
    upload_date = temp_list[1::2]
        
    driver.close()
    
    temp_main_data =  list(enumerate(list(zip(vid_url, title, vid_length, vid_uploader, vid_views, upload_date))))
    print(temp_main_data)
    for i in range(len(temp_main_data)):
        temp_main_data[i] = list(temp_main_data[i])
        temp_main_data[i][0] += 1
        

    main_data = [i for i in temp_main_data if ':' in i[1][2]]

#downlaod the video
def download_vid(vidid_to_download, result):
    global file_size
    def progress_Check(stream = None, chunk = None,remaining = None): 
        percent = (100*(file_size-remaining))/file_size
        progressbar['value']=percent
        pw.update()

    #start download
    def start():
        global file_size
        video = YouTube(url_to_download, on_progress_callback=progress_Check)
        video_type = video.streams.filter(progressive = True, file_extension = "mp4").last()
        file_size = video_type.filesize
        video_type.download('Downloads')

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
    
    url_to_download = result[vidid_to_download-1][1][0]
    root.destroy()
    pw = Tk()
    titlefont = Font(size=20, family='Gotham')
    buttonfont = Font(size=15, family='Gotham')
    vid_title = YouTube(url_to_download).title.encode('utf-8')
    pw.resizable(False, False)
    pw.config(bg="#252525")
    pw.geometry('650x300')
    pw.iconbitmap('icon.ico')
    pw.title('Youtube Video Downloader')
    s = ttk.Style()
    s.theme_use('clam')
    print(s.theme_names())
    TROUGH_COLOR = '#252525'
    BAR_COLOR = '#00FFFF'
    s.configure("green.flat.Horizontal.TProgressbar", troughcolor=TROUGH_COLOR, bordercolor=BAR_COLOR, background=BAR_COLOR, lightcolor=BAR_COLOR, darkcolor=BAR_COLOR, borderwidth=0)
    title = Label(pw, text=vid_title,wraplength=500, font=titlefont, bg='#252525', fg = 'white')
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
    quitbuttoninputframe = Frame(pw, width=211.45, height=52.45, background='#00FFFF', borderwidth=1.45)
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
    print(search_keyword)
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
                value = id_search_input.get()
                try:
                    int(value)
                except:
                    videoinput_id.set(value[:0])
                if value == 'ID':
                    proceed_btn.place_forget()
                    proceed_btn.config(state=DISABLED)
                    proceed_btn.place(x=361,y=441, width=202, height=50)
                if len(value) < 2:
                    proceed_btn.place_forget()
                    proceed_btn.config(state=DISABLED)
                    proceed_btn.place(x=361,y=441, width=202, height=50)
                    try:
                        int(value)
                    except:
                        videoinput_id.set(value[:0])
                elif len(value) >= 2:
                    videoinput_id.set(value[:2])
                    proceed_btn.place_forget()
                    proceed_btn.config(state=NORMAL)
                    proceed_btn.place(x=361,y=441, width=202, height=50)
                    if len(value) == 2 and value !='ID':
                        try:
                            int(value)
                            videoinput_id.set(str(len(main_data)-1)) if int(value) > len(main_data) else videoinput_id
                        except:
                            videoinput_id.set(value[:1])
                            proceed_btn.place_forget()
                            proceed_btn.config(state=DISABLED)
                            proceed_btn.place(x=361,y=441, width=202, height=50)
                else:
                    proceed_btn.place_forget()
                    proceed_btn.config(state=DISABLED)
                    proceed_btn.place(x=361,y=441, width=202, height=50)

            def pbutton_on_enter(e):
                proceed_btn['background'] = '#565656'
                proceed_btn['fg'] = 'white'

            def pbutton_on_leave(e):
                proceed_btn['background'] = '#252525'
                proceed_btn['fg'] = 'white'

            videoinput_id = StringVar()
            videoinput_id.trace('w', limiturlinput)

            title.place_forget()
            titleicon.place_forget()
            scrollbar = Scrollbar(root)
            titleshowframe = Frame(root, width=876, height=142,background = '#00FFFF', borderwidth = 1, relief = FLAT)
            result_list = Listbox(root, yscrollcommand=scrollbar.set, selectmode=BROWSE, highlightthickness=0, selectbackground='#252525',selectborderwidth=0, width=58, fg='white', relief=FLAT, height=4, font=frameFont, bg='#252525')
            scrollbar.config(command=result_list.yview)
            
            for i in main_data:
                result_list.insert(END, i[0])
                result_list.insert(END, i[1][1])
                result_list.insert(END, i[1][2])
                result_list.insert(END, i[1][3])

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
        root.iconbitmap('icon.ico')

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

        mainicon = ImageTk.PhotoImage(Image.open("mainicon.png"))
        main_menu()
        root.mainloop()
    except:
        raise
        quit()

