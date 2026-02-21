from TN import *
import customtkinter as ctk
from CTkListbox import *
from PIL import Image
import os
from showkq import xemkq
import webbrowser
import requests
from assets.Codebox import *
from CTkTable import *
from CTkToolTip import *
from tkinter import messagebox

ltime = 60*10 # 10 phút

def hsg(main = None, mainloop = False):
    dan = os.path.dirname(os.path.abspath(__file__))
    filedan = os.path.join(dan, "setting.txt")

    try:
        with open(filedan, "r", encoding="utf-8") as file:
            settingfile = file.readlines()
            print(settingfile)
    except FileNotFoundError:
        messagebox.showerror("Error", "Phát hiện thiếu tệp chương trình, cài đặt lại chương trình có thể giải quyết")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return
    
    filedan = os.path.join(dan, "userdata.txt")
    try:
        with open(filedan, "r", encoding="utf-8") as file:
            userdatafile = file.readlines()
    except FileNotFoundError:
        messagebox.showerror("Error", "Phát hiện thiếu tệp chương trình, cài đặt lại chương trình có thể giải quyết")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    if main:
        main.destroy()
    def capnhat_userdata():
        if tende.get() in bode:
            index = list(bode.keys()).index(tende.get())
            ldl = userdatafile[index+1].strip().split()
            dulienbai = str(f"{ldl[0]} với số điểm {ldl[1]}")
            if solanlam.get() != f"Số lần làm đề: {dulienbai}":
                solanlam.set(f"Số lần làm đề: {dulienbai}")

        locde.after(1000, capnhat_userdata)  
    
    #LAYDE
    if settingfile[3].strip().split()[1] == "1":
        def layde(event):
            nonlocal tende, solanlam
            selected = de.get()  # Lấy giá trị của phần tử được chọn
            if selected:
                tende.set(selected)  
                index = list(bode.keys()).index(selected) 
                ldl = userdatafile[index+1].strip().split() 
                dulienbai = str(f"{ldl[0]} với số điểm {ldl[1]}")
                try:
                    with open(f"de/{selected}/info.txt", "r", encoding="utf-8") as file:
                        nine = file.readlines()
                except FileNotFoundError:
                    messagebox.showerror("Error", "Phát hiện thiếu tệp chương trình, cài đặt lại chương trình có thể giải quyết")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")
                    
                solanlam.set(f"Số lần làm đề: {dulienbai}")
                scautn.set(f"Số câu trắc nghiệm: {nine[0].strip()}")
                scautl.set(f"Số câu tự luận: {nine[1].strip()}")
                sctg.set(f"Thời gian làm đề: {nine[2].strip()}")
                rate.set(f"Độ khó: {nine[3].strip()}")

                #lamde.grid(row = 9, column = 0, sticky = "w e", padx = 10, pady = (5,10))
                #kqd.grid(row = 10, column = 0, sticky = "w e", padx = 10, pady = (5,10))
                homerfs.grid(row = 11, column = 0, sticky = "w e", padx = 10, pady = (5,10))

                return index
            else:
                tende.set("Vui lòng chọn 1 đề")
    
    bode = {entry.name: index + 1 for index, entry in enumerate(os.scandir("de")) if entry.is_dir()}
    
    #INIT 
    locde = ctk.CTk()
    locde.title("Ôn học sinh giỏi THPT")
    locde.geometry("800x450")
    locde.minsize(600,400)

    # GRCF
    locde.grid_rowconfigure(0, weight=1)
    locde.grid_columnconfigure(1, weight=1)

    # IMGP
    image_path = os.path.join(os.path.dirname(__file__), "assets")

    # INIT
    logo_img = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
    home_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                            dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(24, 24))
    add_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                           dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(24, 24))
    tg_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "author_light.png")),
                            dark_image = Image.open(os.path.join(image_path, "author_dark.png")), size=(24, 24))
    setting_img = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "setting_light.png")),
                            dark_image = Image.open(os.path.join(image_path, "setting_dark.png")), size=(24, 24))

    # Tạo thanh điều hướng
    nav_frame = ctk.CTkFrame(locde, corner_radius=0)
    nav_frame.grid(row=0, column=0, sticky="nsew")
    nav_frame.grid_rowconfigure(5, weight=1)

    nav_label = ctk.CTkLabel(nav_frame, text="  Canfendania Helper", image=logo_img, compound="left",wraplength=600, font=("Arial", 16, "bold"))
    nav_label.grid(row=0, column=0, padx=20, pady=20)

    button_style = {"anchor": "w", "height": 40, "border_spacing": 12, "font": ("Arial", 14), "hover_color": ("gray70", "gray30"),"text_color": ("black", "white")}
    
    btn_home = ctk.CTkButton(nav_frame, text="Trang chủ", image=home_img, fg_color="transparent", corner_radius=0, **button_style)
    btn_home.grid(row=1, column=0, sticky="nsew")

    btn_add = ctk.CTkButton(nav_frame, text="Thư viện đề", image=add_img, fg_color="transparent", corner_radius=0, **button_style)
    btn_add.grid(row=2, column=0, sticky="nsew")

    btn_tg = ctk.CTkButton(nav_frame, text="Thông tin tác giả", image=tg_img, fg_color = "transparent", corner_radius = 0, **button_style)
    btn_tg.grid(row=3, column=0, sticky = "nsew")

    btn_st = ctk.CTkButton(nav_frame, text="Cài đặt", image=setting_img, fg_color = "transparent", corner_radius = 0, **button_style)
    btn_st.grid(row=4, column=0, sticky = "nsew")

    # Tạo các frame
    home_frame = ctk.CTkFrame(locde, corner_radius=0, fg_color="transparent")
    add_frame = ctk.CTkFrame(locde, corner_radius=0, fg_color="transparent")
    tg_frame = ctk.CTkFrame(locde, corner_radius=0, fg_color="transparent")
    st_frame = ctk.CTkFrame(locde, corner_radius=0, fg_color="transparent")

    #APP MODE
    default_mode = "System" 
    ctk.set_appearance_mode(default_mode)

    appearance_menu = ctk.CTkOptionMenu(nav_frame, values=["Light", "Dark", "System"], command=lambda mode: ctk.set_appearance_mode(mode))
    appearance_menu.set(default_mode) 
    appearance_menu.grid(row=6, column=0, padx=20, pady=5, sticky="s")

    versionapp = ctk.CTkLabel(nav_frame, text="pre-release 0.7.3", font=("Arial", 10),wraplength=600)
    versionapp.grid(row=7, column=0, padx=20, sticky="s")

    # Cấu hình cột lưới của các frame
    home_frame.grid_columnconfigure(0, weight=1)
    tg_frame.grid_columnconfigure(0, weight=1)
    st_frame.grid_columnconfigure(0, weight=1)

    # TRANG ADD
    home_frame.grid(row=0, column=1, sticky="nsew")
    homelbl = ctk.CTkLabel(add_frame, text="TESTING ONLY!", font=("Arial", 16),wraplength=600)
    homelbl.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    #TẢI ĐỀ
    def taide(file_url):
        import zipfile

        url = file_url
        dzip = "temp_download.zip"
        ezip = "de"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            with open(dzip, "wb") as f:
                f.write(response.content)

            if not os.path.exists(ezip):
                os.makedirs(ezip)

            with zipfile.ZipFile(dzip, "r") as zip_ref:
                zip_ref.extractall(ezip)

            os.remove(dzip)
            messagebox.showinfo("Success", "Download successfully! Click Refresh in home page")

        except requests.Timeout:
            messagebox.showerror("Timeout", "Timeout!")
        except Exception as e: 
            messagebox.showerror("Error", f"Unknown error: {str(e)}")
    
    from requests.exceptions import MissingSchema  # Import MissingSchema từ requests.exceptions

    def load_text():
        global file_content
        load_button.configure(state="disabled", text="Loading...")
        try:
            if len(settingfile) > 2:
                parts = settingfile[2].strip().split()
                if len(parts) > 1:
                    slink = parts[1]
                else:
                    raise ValueError("Invalid format in setting.txt: Missing server URL.")
            else:
                raise ValueError("Invalid format in setting.txt: Not enough lines.")

            response = requests.get(slink, timeout=5)
            response.raise_for_status()
            file_content = response.text  
            cacde()  
            load_button.configure(state="normal", text="Refresh data")  

        except requests.Timeout:
            messagebox.showerror("Timeout Error", "The request took too long to complete.")
            load_button.configure(state="normal", text="Refresh data")
        except MissingSchema: 
            messagebox.showerror("Invalid URL", "No scheme supplied. Please check the server URL in Setting => server \n If you don't know what's wrong. Change the server to default")
            load_button.configure(state="normal", text="Refresh data")
        except requests.RequestException as e:
            messagebox.showerror("Request Error", f"Error loading file: {e}")
            load_button.configure(state="normal", text="Refresh data")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
            load_button.configure(state="normal", text="Refresh data")

    def cacde():
        for widget in add_frame.winfo_children():
            if widget != load_button:  
                widget.destroy()
        # Tiêu đề
        title_label = ctk.CTkLabel(add_frame, text="Danh sách bộ đề thi", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")
        # Thanh tìm kiếm
        def search_items():
            keyword = search_entry.get().lower()
            update_display(keyword)
    
        search_entry = ctk.CTkEntry(add_frame, placeholder_text="Tìm kiếm đề thi...")
        search_entry.grid(row=1, column=0, padx=(15,2), pady=(5,0), sticky="ew")
    
        search_button = ctk.CTkButton(add_frame, text="Tìm", command=search_items, width=80)
        search_button.grid(row=1, column=1, padx=(2,15), pady=(5,0), sticky="e")
    
        # Khung cuộn chứa các đề
        scrollable_frame = ctk.CTkScrollableFrame(add_frame, fg_color="transparent")
        scrollable_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=0, sticky="nsew")

        # Configure grid weights for proper resizing
        add_frame.grid_rowconfigure(2, weight=1)
        add_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(0, weight=1)  # Đảm bảo cột trong scrollable_frame giãn đều

        lines = file_content.splitlines()
        all_frames = [] 
        for i in range(0, len(lines), 3):
            if i + 2 >= len(lines):
                break
            title = lines[i].strip()
            link = lines[i + 1].strip()
            details = lines[i + 2].strip().split()
    
            # Tạo frame cho từng đề thi
            cacde_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10, fg_color="#f2f2f2")
            cacde_frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew")  # Đặt sticky="ew" để giãn theo chiều ngang
            cacde_frame.grid_columnconfigure(0, weight=1)  # Đảm bảo nội dung bên trong giãn đều
    
            # Nhãn tiêu đề đề thi
            title_label = ctk.CTkLabel(cacde_frame, text=title, font=("Arial", 14, "bold"), text_color="black")
            title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    
            # Nút mở đề
            open_button = ctk.CTkButton(cacde_frame, text="Thêm đề", command=lambda l=link: taide(l),font=("Arial", 12), fg_color="#3b8ed0", hover_color="#36719F", width=80)
            open_button.grid(row=0, column=1, padx=10, pady=5, sticky="e")
    
            # Thông tin đề
            info_labels = [f"Số câu trắc nghiệm: {details[0]}",f"Số câu tự luận: {details[1]}",f"Thời gian: {details[2]} phút",f"Độ khó: {details[3]}"]

            for idx, text in enumerate(info_labels):
                label = ctk.CTkLabel(cacde_frame, text=text, font=("Arial", 12), text_color="gray30")
                label.grid(row=idx+1, column=0, padx=10, pady=0, sticky="w")
    
            # Lưu frame vào danh sách
            all_frames.append((title.lower(), cacde_frame))
    
        # Hàm để cập nhật hiển thị danh sách đề
        def update_display(keyword=""):
            # Ẩn tất cả các frame
            for _, frame in all_frames:
                frame.grid_forget()

            row = 0
            for title, frame in all_frames:
                if keyword in title:
                    frame.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
                    row += 1
    
        # Hiển thị tất cả các đề lần đầu
        update_display()

    text_box = ctk.CTkLabel(add_frame, width=480, height=250, anchor="nw", wraplength=460, justify="left", text = "No loaded data, Please click the button to load data", font=("Arial", 12), text_color="gray30")
    text_box.place(relx=0.5, rely=0.5, anchor="center")  # Center the label in the frame
    text_box.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="nsew")

    load_button = ctk.CTkButton(add_frame, text="Khởi động marketplace", command=load_text, fg_color="#3b8ed0", hover_color="#36719F")
    load_button.grid(row=3, column=0, columnspan=2, padx=10, pady=(0,2), sticky="ew")


    # LỆNH SWICH FRAME
    def switch_frame(name):
        btn_home.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        btn_add.configure(fg_color=("gray75", "gray25") if name == "add" else "transparent")
        btn_tg.configure(fg_color=("gray75", "gray25") if name == "tg" else "transparent")
        btn_st.configure(fg_color=("gray75", "gray25") if name == "st" else "transparent")

        home_frame.grid_forget()
        add_frame.grid_forget()
        tg_frame.grid_forget()
        st_frame.grid_forget()

        if name == "home":
            home_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "add":
            add_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "tg":
            tg_frame.grid(row=0, column = 1, sticky = "nsew")
        elif name == "st":
            st_frame.grid(row=0, column = 1, sticky = "nsew")

    btn_home.configure(command=lambda: switch_frame("home"))
    btn_add.configure(command=lambda: switch_frame("add"))
    btn_tg.configure(command=lambda: switch_frame("tg"))
    btn_st.configure(command=lambda: switch_frame("st"))    


    





    if settingfile[3].strip().split()[1] == "0":
        frmde = ctk.CTkFrame(home_frame, fg_color="transparent")
        frmde.place(relx=0, rely=0, relwidth=1, relheight=1)

        # LISTBOX 
        thumbpa = os.path.join(os.path.dirname(__file__), "assets", "thumb.png")
        thumb = ctk.CTkImage(Image.open(thumbpa), size=(150, 200))

        for widget in frmde.winfo_children():
                if widget != load_button:  
                    widget.destroy()

        title_label = ctk.CTkLabel(frmde, text="Danh sách bộ đề thi", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")

        def search_items():
            keyword = search_entry.get().lower()
            update_display(keyword)
        
        search_entry = ctk.CTkEntry(frmde, placeholder_text="Tìm kiếm đề thi...")
        search_entry.grid(row=1, column=0, padx=(15,2), pady=(5,0), sticky="ew")

        search_button = ctk.CTkButton(frmde, text="Tìm", command=search_items, width=80)
        search_button.grid(row=1, column=1, padx=(2,15), pady=(5,0), sticky="e")

        scrollable_frame = ctk.CTkScrollableFrame(frmde, fg_color="transparent")
        scrollable_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=0, sticky="nsew")

        frmde.grid_rowconfigure(2, weight=1)
        frmde.grid_columnconfigure(0, weight=1)

        scrollable_frame.grid_columnconfigure(0, weight=1)  
        depackpath = "de/depack.txt"
        with open(depackpath, "r", encoding="utf-8") as file:
            lines = file.readlines()

        all_frames = [] 

        for i in range(0, len(lines), 6):
            if i + 5 >= len(lines):
                break
            title = lines[i].strip()
            socautn = lines[i + 1].strip()
            socautl = lines[i + 2].strip()
            thoigian = lines[i + 3].strip()
            dokho = lines[i + 4].strip()
            dscr = lines[i + 5].strip()

            cacde_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10, fg_color="#f2f2f2")
            cacde_frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew") 
            cacde_frame.grid_columnconfigure(1, weight=1)  

            title_label = ctk.CTkLabel(cacde_frame, text=title, font=("Arial", 14, "bold"), text_color="black")
            title_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            thumba = ctk.CTkLabel(cacde_frame,text = None, image=thumb, compound="left")
            thumba.grid(row=0,rowspan = 10, column=0, padx=0, pady=0, sticky="w")

            # Nút mở đề
            open_button = ctk.CTkButton(cacde_frame, text="Bắt đầu làm bài", font=("Arial", 12), fg_color="#3b8ed0", hover_color="#36719F", width=80)
            open_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

            # Thông tin đề
            info_labels = [f"Số câu trắc nghiệm: {socautn}",f"Số câu tự luận: {socautl}",f"Thời gian: {thoigian}",f"Độ khó: {dokho}", f"Mô tả: {dscr}"]
            for idx, text in enumerate(info_labels):
                label = ctk.CTkLabel(cacde_frame, text=text, font=("Arial", 12), text_color="gray30")
                label.grid(row=idx+1, column=1, padx=10, pady=0, sticky="w")

            all_frames.append((title.lower(), cacde_frame))

        def update_display(keyword=""):
            # Ẩn tất cả các frame
            for _, frame in all_frames:
                frame.grid_forget()
            row = 0
            for title, frame in all_frames:
                if keyword in title:
                    frame.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
                    row += 1

        update_display()

    else:    
        frmde = ctk.CTkFrame(home_frame, fg_color="transparent")
        frmde.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # FRAME ĐỀ
        frmbai = ctk.CTkFrame(home_frame, fg_color="transparent")
        frmbai.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        de = CTkListbox(frmde, font=("Arial", 11), command=layde)
        de.bind("<Button-1>", layde)
        de.place(relx=0.03, rely=0.03, relwidth=0.95, relheight=0.95)

        for key, value in bode.items():
            de.insert(ctk.END, key)

        # REFRESH
        def refreshome():
            de.delete("all")
            bode = {entry.name: index + 1 for index, entry in enumerate(os.scandir("de")) if entry.is_dir()}
            for key, value in bode.items():
                de.insert(ctk.END, key)

        frmbai.grid_columnconfigure(0, weight=1)
        frmbai.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6,7,8,9,10,11,12), weight=0)

        homerfs = ctk.CTkButton(master=frmbai,text="Refresh",font=("Arial", 12)) #command=refreshome
        homerfstp = CTkToolTip(homerfs, message = "Làm mới danh sách bộ đề", delay = 1)

        tende = ctk.StringVar(master=frmbai)
        tende.set("Vui lòng chọn 1 đề")

        solanlam = ctk.StringVar(master=frmbai)
        solanlam.set("")

        scautn = ctk.StringVar(master=frmbai)
        scautn.set("")

        scautl = ctk.StringVar(master=frmbai)
        scautl.set("")

        sctg= ctk.StringVar(master=frmbai)
        sctg.set("")

        rate = ctk.StringVar(master=frmbai)
        rate.set("")

        lbl_tende = ctk.CTkLabel(frmbai, textvariable=tende, font=("Arial", 15),wraplength=600)
        lbl_tende.grid(row=0, column=0, padx=20, pady=50, sticky="w e")

        lbl_slm = ctk.CTkLabel(frmbai, textvariable=solanlam, font=("Arial", 15),wraplength=600)
        lbl_slm.grid(row=1, column=0, padx=20, pady=0, sticky="w")

        lbl_scautn = ctk.CTkLabel(frmbai, textvariable=scautn, font=("Arial", 15), anchor="w",wraplength=600)
        lbl_scautn.grid(row=2, column=0, padx=20, pady=0, sticky="w")

        lbl_scautl = ctk.CTkLabel(frmbai, textvariable=scautl, font=("Arial", 15), anchor="w",wraplength=600)
        lbl_scautl.grid(row=3, column=0, padx=20, pady=0, sticky="w")

        lbl_sctg = ctk.CTkLabel(frmbai, textvariable=sctg, font=("Arial", 15), anchor="w",wraplength=600)
        lbl_sctg.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        lbl_rate = ctk.CTkLabel(frmbai, textvariable=rate, font=("Arial", 15), anchor="w",wraplength=600)
        lbl_rate.grid(row=5, column=0, padx=20, pady=0, sticky="w")

    questions_data = []
    answers = [] 

    def stn():
        global questions_data, answers
        '''sel = de.get()
        idx = list(bode.keys()).index(sel)'''

        ccau = 5
        answ = [0, 2, 3, 3, 1]  
        sl = 0
        name = 'sel'
        total_seconds = 5000000

        locde.deiconify()
        tracnghiem(ccau,answ,sl,name,total_seconds)
        # LÀM ĐỀ
    '''lamde = ctk.CTkButton(master=frmbai, text="Bắt đầu làm bài", font=("Arial", 12), fg_color="#3b8ed0",hover_color = "#36719F")
    lamde.bind("<Button-1>", lambda event:stn())'''

    # KẾT QUẢ ĐỀ
    '''def lkq():
        sel= de.get()
        idx = list(bode.keys()).index(sel)
        bode_path = os.path.join(os.path.dirname(__file__), f"de/{sel}")
        db_path = os.path.join(bode_path, f"BODE.db")
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT question, a, b, c, d, correct FROM BODE")
        rows = cursor.fetchall()
        questions_data = [(row[0], [row[1], row[2], row[3], row[4]]) for row in rows]
        answers = [row[5] for row in rows]
        conn.close()
        xemkq(questions_data,answers)
    kqd = ctk.CTkButton(master=frmbai, text="Xem kết quả", font=("Arial", 12), fg_color="#3b8ed0",hover_color = "#36719F", command=lkq)'''
    
    if settingfile[3].split()[1] == "1": capnhat_userdata()

    # ========================= SETTING ==========================
    tab = ctk.CTkTabview(st_frame)
    tab.pack(expand=True, fill="both", padx=10, pady=10)

    gn = tab.add("General")
    sv = tab.add("Server")
    qlde = tab.add("Manager")

    sv.grid_rowconfigure(2, weight = 1)
    sv.grid_columnconfigure(1, weight=1)
    sv.grid_columnconfigure((2,3), weight=0)
    sv.grid_rowconfigure(3, weight=1)  

    gn.grid_rowconfigure(2)
    gn.grid_columnconfigure((0,1),weight=1)

    # GENERAL
    def savest(x,ln,note = None):
        state = x.get()  
        parts = settingfile[ln].strip().split()
        if parts:
            if state == 1:
                parts[1] = "1"
            else:
                parts[1] = "0"
            settingfile[ln] = " ".join(parts) + "\n"
        with open("setting.txt", "w", encoding= "utf-8") as file:
            file.writelines(settingfile)
        if note:
            messagebox.showinfo("Old GUI", note) 

    fsw = ctk.CTkSwitch(gn, text="Toàn màn hình")
    fsw.configure(command = lambda: savest(fsw,1))
    fsw.grid(row = 0, column = 0,padx= 20, sticky="nsew")
    
    fswtp = CTkToolTip(fsw, message ="Thay đổi việc có toàn màn hình không trong phần thi trắc nghiệm", delay=1)

    #Giao dien de
    guidw = ctk.CTkSwitch(gn, text="Sử dụng giao diện chọn đề cũ")
    guidw.configure(command = lambda: savest(guidw,3,"Để áp dụng giao diện mới, bạn vui lòng khởi động lại ứng dụng"))
    guidw.grid(row = 0, column = 1,padx= 20, sticky="nsew")

    guidwtp = CTkToolTip(guidw, message="Sử dụng giao diện classic cho trang chọn và làm đề thi (Yêu cầu khởi động lại)", delay=1)

    if len(settingfile) > 3:
        parts = settingfile[1].strip().split()
        if parts[1] == "1": fsw.select()
        else: fsw.deselect()
        parts = settingfile[3].strip().split()
        if parts[1] == "1": guidw.select()
        else: guidw.deselect()

    # SERVER
    def svcof():
        esv = svip.get()
        if esv:
            if len(settingfile) > 2:
                parts = settingfile[2].strip().split()
                parts[1] = esv
                settingfile[2] = " ".join(parts) + "\n"
            with open("setting.txt", "w", encoding = "utf-8") as file:
                file.writelines(settingfile)
            messagebox.showinfo("Successfully", "Server changed successfully.")
        else:
            messagebox.showerror("Error", "Do not leave the entry empty.")
    if len(settingfile) > 2:
        parts = settingfile[2].strip().split()
        slink = parts[1]

    svip = ctk.CTkEntry(sv, placeholder_text="Enter server IP (default: https://raw.githubusercontent.com/nbao210/spst-cdn/refs/heads/main/index.txt)")
    svip.grid(row=1, column=1, padx=(20,0), sticky="nsew")
    svip.insert(0, slink)
    sviptp = CTkToolTip(svip, message = "Chỉnh sửa máy chủ của marketplace. Cần là một link TXT hợp lệ",delay=1)

    svcf = ctk.CTkButton(sv, text="Xác nhận", command=svcof)  # Remove parentheses
    svcf.grid(row=1, column=3, padx = (5,20), sticky="nsew")

    svinfo = ctk.CTkTextbox(sv, fg_color="transparent", text_color="white")
    svinfo.insert("end", "Mặc định: https://raw.githubusercontent.com/nbao210/spst-cdn/refs/heads/main/index.txt\n", "default")
    svinfo.insert("end", "⚠️ Đây là máy chủ mặc định của Marketplace. Chỉ thay đổi khi bạn biết mình đang làm gì", "warning")
    svinfo.tag_config("default", foreground="white")  # màu chữ mặc định
    svinfo.tag_config("warning", foreground="yellow")  # màu chữ cảnh báo
    svinfo.configure(state="disabled", wrap="word")
    svinfo.grid(row=2, column=1, columnspan=3, padx=5, sticky="nsew")

    # MANAGER
    #AUTHOR
    tg_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)  
    tg_frame.grid_columnconfigure(0, weight=1)

    # Hiển thị ảnh đại diện
    avt = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "auth.png")), size=(200, 200))
    avp = ctk.CTkLabel(tg_frame, image=avt, text="")  # Không có text để tránh khoảng trắng
    avp.grid(row=1, column=0, pady=(30, 2), sticky="n")

    # Hiển thị tên ngay dưới ảnh
    name = ctk.CTkLabel(tg_frame, text="Nguyễn Gia Bảo", font=("Arial", 18, "bold"),wraplength=600)
    name.grid(row=2, column=0, pady=0, sticky="n")

    dvl = ctk.CTkLabel(tg_frame,wraplength=600, text = "<a> Python, C++, C#, web developer </a>", font=("SegoeUI",12), text_color="gray")
    dvl.grid(row=3, column = 0, pady=0, sticky = "n")

    dt = ctk.CTkLabel(tg_frame, text ="From THCS Nguyễn Trãi", font=("Arial", 12), text_color="gray",wraplength=600)
    dt.grid(row=4, column=0, pady=0, sticky ="n")

    # Tạo frame chứa các nút và căn giữa
    buttons_frame = ctk.CTkFrame(tg_frame, fg_color="transparent")
    buttons_frame.grid(row=5, column=0, pady=(5, 0), sticky="n")
    buttons_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    # Tạo hình ảnh cho các nút
    face = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "facebook.png")), size=(35, 35))
    you = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "youtube.png")), size=(40, 30))
    dis = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "discord.png")), size=(45, 25))
    wb = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "web.png")), size=(35, 35))
    git = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "github.png")), size=(35, 35))

    # Tạo các nút hình ảnh
    fb = ctk.CTkButton(buttons_frame, image=face, width=70, height=70, text="", fg_color="transparent", command=lambda:webbrowser.open("https://www.facebook.com/daisuh2cl/"))
    yt = ctk.CTkButton(buttons_frame, image=you, width=70, height=70, text="", fg_color="transparent", command=lambda: webbrowser.open("https://www.youtube.com/@wonggrow"))
    dc = ctk.CTkButton(buttons_frame, image=dis, width=70, height=70, text="", fg_color="transparent", command=lambda: webbrowser.open("http://discordapp.com/users/1003997661361356810"))
    web = ctk.CTkButton(buttons_frame, image=wb, width=70, height=70, text="", fg_color="transparent", command=lambda: webbrowser.open("https://nbaowebpro.web.app"))
    gh = ctk.CTkButton(buttons_frame, image=git, width=70, height=70, text="", fg_color="transparent", command=lambda: webbrowser.open("https://github.com/nbao210/spst-cdn"))

    # Căn giữa các nút trong frame
    fb.grid(row=0, column=0, padx=5, pady=5)
    yt.grid(row=0, column=1, padx=5, pady=5)
    dc.grid(row=0, column=2, padx=5, pady=5)
    web.grid(row=0, column=3, padx=5, pady=5)
    gh.grid(row=0, column=4, padx=5, pady=5)
    if mainloop:
        locde.mainloop()
    return locde

def ganmain(ot):
    ot.destroy()
    def tents():
        text = entry.get()
        with open("userdata.txt", "r+", encoding="utf-8") as file:
            lines = file.readlines()  
            if lines:
                lines[0] = text + "\n"  
            else:
                lines.append(text + "\n")  
            file.seek(0)  
            file.writelines(lines)  
            file.truncate() 
    def reset():
        with open("userdata.txt", "w") as file:
            default = ["Annonymous"] + ["0 0"] * 5
            file.write("\n".join(default))
        main.destroy()
    main = ctk.CTk()
    main.resizable(False, False)
    main.geometry("800x400+50+50")
    main.title("Canfendania Helper - Phần mềm bổ trợ tin học THPT")
    welcome = ctk.CTkLabel(master=main, text="Chào mừng đến với phần mềm hỗ trợ ôn tin học THPT - Cafendania Helper", font=("Monospace", 12),wraplength=600)
    onhsgbutton = ctk.CTkButton(master=main, text="Ôn tin học sinh giỏi", font=("Arial", 12), fg_color="#3b8ed0",hover_color = "#36719F")
    onhsgbutton.bind("<Button-1>", lambda event: hsg(main, True))
    welcome.pack(pady=20)
    onhsgbutton.pack(padx=0, pady=50)
    entry = ctk.CTkEntry(main, placeholder_text="Nhập tên thí sinh")
    entry.pack(pady=5)
    button = ctk.CTkButton(main, text="Xác nhận tên thí sinh", command=tents)
    button.pack(pady=0)
    resetbutton = ctk.CTkButton(main, text="Reset", font=("Arial", 12), fg_color="#3b8ed0",hover_color = "#36719F")
    resetbutton.bind("<Button-1>", lambda event: reset())
    resetbutton.pack(padx=0, pady=20)
    main.configure(fg_color="#43B3AE")
    main.mainloop()

def root():
    # GN
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # WH
    WIDTH, HEIGHT = 600, 350
    BORDER   = 3
    TITLE_H  = 30

    #OUT
    outer = ctk.CTk()
    outer.overrideredirect(True)
    outer.attributes("-topmost", True)
    outer.configure(fg_color="#818181")
    screen_w = outer.winfo_screenwidth()
    screen_h = outer.winfo_screenheight()
    x = (screen_w - WIDTH)//2 - BORDER
    y = (screen_h - HEIGHT)//2 - BORDER
    outer.geometry(f"{WIDTH+BORDER*2}x{HEIGHT+BORDER*2}+{x}+{y}")

    #MAIN
    main_frame = ctk.CTkFrame(
        outer,
        corner_radius=8,
        fg_color="#FFFFFF",
        width=WIDTH,
        height=HEIGHT
    )
    main_frame.place(relx = 0.01, rely = 0.01, relwidth = 0.98, relheight = 0.98)

    # TTB
    title_bar = ctk.CTkFrame(
        main_frame,
        fg_color="#E1F3E1",
        height=TITLE_H,
        corner_radius=0
    )
    title_bar.pack(fill="x", side="top")

    lbl_ms = ctk.CTkLabel(
        title_bar,
        text=" Nguyễn Gia Bảo",
        font=("Segoe UI", 12, "bold"),
        text_color="#217346",
        anchor="w"
    )
    lbl_ms.place(x=10, y=5, relwidth=0.9)

    def close_splash():
        outer.destroy()

    btn_close = ctk.CTkButton(
        title_bar,
        text="✕",
        width=30, height=TITLE_H-10,
        fg_color="transparent",
        hover_color="#B61818",
        text_color="#000000",
        command=close_splash
    )
    btn_close.place(relx=1.0, x=-35, y=5, anchor="ne")

    # ND
    content = ctk.CTkFrame(
        main_frame,
        fg_color="#FFFFFF",
        corner_radius=0
    )
    content.pack(expand=True, fill="both", pady=(TITLE_H,0))

    # LG
    try:
        logo_img = ctk.CTkImage(
            light_image=Image.open("assets/CustomTkinter_logo_single.png"),
            size=(120,120)
        )
    except:
        logo_img = None

    lbl_logo = ctk.CTkLabel(content, image=logo_img, text="")
    lbl_logo.pack(pady=(20,10))

    #APP
    lbl_app = ctk.CTkLabel(
        content,
        text="Canfendania Helper",
        font=("Segoe UI", 24, "bold"),
        text_color="#222"
    )
    lbl_app.pack()

    lbl_slg = ctk.CTkLabel(
        content,
        text="Phần mềm luyện thi tin học cho cấp THPT",
        font=("Segoe UI", 15),
        text_color="#5E5E5E"
    )
    lbl_slg.pack()

    # STT
    lbl_stat = ctk.CTkLabel(
        content,
        text="Chào mừng đến với phần mềm luyện thi tin học cho cấp THPT",
        font=("Segoe UI", 12),
        text_color="#5E5E5E"
    )
    lbl_stat.place(rely = 0.9, relx = 0.01)

    def text():
        status_texts = [
            "Chào mừng đến với phần mềm luyện thi tin học cho cấp THPT",
            "Kiểm tra phần cứng",
            "Kiểm tra runtime",
            "Kiểm tra tệp tin ứng dụng",
            "Chuẩn bị phiên hoạt động mới",
            "Đang tải dữ liệu người dùng",
            "Đang thiết lập giao diện",
            "Đang khởi động giao diện"
        ]

        times = [
            1500,
            200,  
            200,  
            200,  
            200,  
            200,  
            200,  
            1000   
        ]
        def upt(index=0):
            if index < len(status_texts):
                lbl_stat.configure(text=status_texts[index])
                outer.after(times[index], upt, index + 1)  
        upt()
    text()

    outer.after(3700, ganmain, outer)
    outer.mainloop()

if __name__ == "__main__":
    root()