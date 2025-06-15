import customtkinter as ctk
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os
import time
import threading
from tkinter import Text

class PDFViewer(ctk.CTkFrame):
    def __init__(self, parent, path, **kwargs):
        super().__init__(parent, **kwargs)
        self.doc = fitz.open(path)
        self.current_page = 0
        self.zoom_factor = 1.5
        self.image_id = None
        self.image_obj = None

        self.configure(fg_color="#AAD3DE", corner_radius=0, border_width=0)

        self.canvas = ctk.CTkCanvas(self, bg="white", highlightthickness=0)
        self.h_scroll = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.v_scroll = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        # Bố trí với grid, để canvas có thể giãn nở
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.controls = ctk.CTkFrame(self)
        self.controls.configure(fg_color="transparent", corner_radius=0, border_width=0)
        self.controls.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.page_info = ctk.CTkLabel(self.controls, text="", text_color="black")
        self.page_info.grid(row=0, column=4, padx=5, sticky="e")  # Align to the right
        
        ctk.CTkButton(self.controls, text="<< Trang trước", command=self.prev_page, width=100).grid(row=0, column=0, padx=5, sticky="w")
        ctk.CTkButton(self.controls, text="Trang sau >>", command=self.next_page, width=100).grid(row=0, column=1, padx=5, sticky="w")
        ctk.CTkButton(self.controls, text="Zoom +", command=self.zoom_in, width=100).grid(row=0, column=2, padx=5, sticky="w")
        ctk.CTkButton(self.controls, text="Zoom -", command=self.zoom_out, width=100).grid(row=0, column=3, padx=5, sticky="w")
        
        self.page_entry = ctk.CTkEntry(self.controls, width=60, placeholder_text="Số trang")
        self.page_entry.grid(row=0, column=5, padx=10, sticky="w")
        ctk.CTkButton(self.controls, text="Đi đến", command=self.go_to_page).grid(row=0, column=6, padx=5, sticky="w")

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Configure>", self.on_canvas_ready)

        self.canvas.configure(bg = "#AAD3DE")

        self.canvas.bind("<MouseWheel>", self.on_mouse_scroll)
        self.canvas.bind("<Shift-MouseWheel>", self.on_shift_mouse_scroll)

    def show_page(self, page_num):
        page = self.doc.load_page(page_num)
        mat = fitz.Matrix(self.zoom_factor, self.zoom_factor)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.image_obj = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, pix.width, pix.height))
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0)


        canvas_width = self.canvas.winfo_width()
        x_center = max((canvas_width - pix.width) // 2, 0)
        self.image_id = self.canvas.create_image(x_center, 0, image=self.image_obj, anchor="nw")
        self.page_info.configure(text=f"Trang {page_num + 1} / {len(self.doc)}")

    def zoom_in(self):
        self.zoom_factor += 0.2
        self.show_page(self.current_page)

    def zoom_out(self):
        if self.zoom_factor > 0.4:
            self.zoom_factor -= 0.2
            self.show_page(self.current_page)

    def on_mouse_wheel(self, event):
        if event.state & 0x0004:  # Ctrl
            if event.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()

    def next_page(self):
        if self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def go_to_page(self):
        try:
            page_num = int(self.page_entry.get()) - 1
            if 0 <= page_num < len(self.doc):
                self.current_page = page_num
                self.show_page(self.current_page)
        except ValueError:
            pass

    def on_canvas_ready(self, event):
        self.canvas.unbind("<Configure>")
        self.show_page(self.current_page)

    def on_mouse_scroll(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_shift_mouse_scroll(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

def tracnghiem(ccau, answ, sl, name, total_seconds):
    tn = ctk.CTk()
    #main.destroy()
    with open("setting.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        if len(lines) > 1:
            parts = lines[1].strip().split()
            if parts[1] == "1":
                tn.attributes('-fullscreen', True)  # Nếu fullscreen
            else:
                tn.geometry("1000x700")  
    tn.configure(fg_color="#E3E8F0")
    tn.minsize(800, 500)
    
    tn.grid_columnconfigure(0, weight=1)
    tn.grid_columnconfigure(1, weight=9)
    tn.grid_rowconfigure(0, weight=1)

    # Frame cho câu hỏi
    frmcau = ctk.CTkScrollableFrame(tn, fg_color="#F2F8FF", scrollbar_button_color="#F2F8FF", scrollbar_button_hover_color="#F2F8FF", scrollbar_fg_color="#F2F8FF")
    frmcau.grid(row = 0, column = 0, sticky = "nsew")

    '''frmcau.grid_columnconfigure(0, weight=1)
    frmcau.grid_rowconfigure(5, weight=1)'''

    # Frame cho đề bài
    frmde = ctk.CTkFrame(tn, fg_color="transparent")
    frmde.grid(row = 0, column = 1, sticky = "nsew")
    frmde.grid_rowconfigure(0, weight=1)
    frmde.grid_columnconfigure(0, weight=1)

    viewer = PDFViewer(frmde, f"de/{name}/main.pdf")
    viewer.grid(row=0, column=0, sticky="nsew")
    
    image_path = os.path.join(os.path.dirname(__file__), "assets", "CustomTkinter_logo_single.png")
    tn.logo_img = ctk.CTkImage(Image.open(image_path), size=(30, 30))
    dd = ctk.CTkLabel(frmcau, text="  Canfendania Helper", image=tn.logo_img, compound="left", wraplength=600, font=("Arial Bold", 15), text_color="black")

    dd.pack()

    slg = ctk.CTkLabel(frmcau, text="Phần mềm ôn tin học", compound="left", font=("Arial", 15), text_color="#808080")
    slg.pack()
    def start_countdown():
        def countdown():
            nonlocal total_seconds
            if total_seconds >= 0:
                hrs = total_seconds // 3600
                mins = (total_seconds % 3600) // 60
                secs = total_seconds % 60

                label_hour.after(0, lambda: label_hour.configure(text=f"{hrs:02d}"))
                label_min.after(0, lambda: label_min.configure(text=f"{mins:02d}"))
                label_sec.after(0, lambda: label_sec.configure(text=f"{secs:02d}"))

                total_seconds -= 1
                label_hour.after(1000, countdown) 
            else:
                nop_bai()

        countdown()  

    cdf = ctk.CTkFrame(frmcau, fg_color="transparent")
    cdf.pack(pady = 20)
    label_hour = ctk.CTkLabel(cdf, text="00", font=("Arial", 25), text_color="white", fg_color="#E56425", width=50, corner_radius=5)
    label_hour.grid(row=0, column=0, padx=(0, 2))

    colon1 = ctk.CTkLabel(cdf, text=":", font=("Arial", 25), text_color="black")
    colon1.grid(row=0, column=1, padx=(0, 2))

    label_min = ctk.CTkLabel(cdf, text="00", font=("Arial", 25), text_color="white", fg_color="#E56425", width=50, corner_radius=5)
    label_min.grid(row=0, column=2, padx=(0, 2))

    colon2 = ctk.CTkLabel(cdf, text=":", font=("Arial", 25), text_color="black")
    colon2.grid(row=0, column=3, padx=(0, 2))

    label_sec = ctk.CTkLabel(cdf, text="00", font=("Arial", 25), text_color="white", fg_color="#E56425", width=50, corner_radius=5)
    label_sec.grid(row=0, column=4, padx=(0, 2))

    start_countdown()
    user_answers = [ctk.IntVar(value=-1) for _ in range(ccau)]

    with open("userdata.txt", "r", encoding="utf-8") as file:
        usdl = file.readlines()

    text = Text(frmcau, font=("Arial", 12), bg="#F2F8FF", height=4, bd=0, padx = 15, spacing3=20, spacing1=0, spacing2=0)
    text.tag_config("bold", font=("Arial Bold", 12))
    text.insert("end", "Thí sinh: ")
    text.insert("end", usdl[0].strip() + "\n", "bold")

    text.insert("end", "Bộ đề: ")
    text.insert("end", name + "\n", "bold")

    text.insert("end", "Thời gian: ")
    text.insert("end", f"{int(total_seconds / 60)} phút\n", "bold")

    text.insert("end", "Số câu: ")
    text.insert("end", str(ccau), "bold")  

    text.configure(state="disabled")

    text.pack()
    # Frame danh sách câu hỏ 

    '''tnf = ctk.CTkFrame(frmcau, fg_color="transparent")
    tnf.pack(pady=10, padx = 0, fill="both", expand=True)
        
    tnf.grid_columnconfigure((0, 1, 2, 3), weight=0)

    abcd = ctk.CTkFrame(frmcau, fg_color="transparent")
    abcd.pack(pady=0, padx=45, fill="x")
    
    ctk.CTkLabel(abcd, font=("Arial", 20), text_color="black", text="A").grid(row=0, column=0, padx=15,  sticky="w")
    ctk.CTkLabel(abcd, font=("Arial", 20), text_color="black", text="B").grid(row=0, column=1, padx=15,  sticky="w")
    ctk.CTkLabel(abcd, font=("Arial", 20), text_color="black", text="C").grid(row=0, column=2, padx=15,  sticky="w")
    ctk.CTkLabel(abcd, font=("Arial", 20), text_color="black", text="D").grid(row=0, column=3, padx=15,  sticky="w")'''

    frmccau = ctk.CTkScrollableFrame(frmcau, fg_color="transparent", height=400)
    frmccau.pack(fill="both", expand=True)

    frames = []
    for i in range(ccau):
        frame = ctk.CTkFrame(frmccau, fg_color="transparent", corner_radius=10, border_width=2, border_color="#F2F8FF")
        frame.pack(pady=(0,20), padx=5, fill = "x")
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0)

        nhcau = ctk.CTkLabel(frame, text=None, font=("Arial", 20), text_color="black")
        if len(str(i+1)+".") == 2:
            nhcau.configure(text=" "+str(i+1)+".")
            nhcau.grid(row=0, column=0, sticky="s", padx=(5,15), pady=0)
        elif len(str(i+1)+".") == 3:
            nhcau.configure(text=str(i+1)+".")
            nhcau.grid(row=0, column=0, sticky="s", padx=(0,15), pady=0)

        tnf = ctk.CTkFrame(frame, fg_color="transparent")
        tnf.grid(row=0, column=1, sticky="ew")
        
        frame.grid_columnconfigure(1, weight=1)
        tnf.grid_columnconfigure((0, 1, 2, 3), weight=1)

        for j in range(4): 
            radio = ctk.CTkRadioButton(
                tnf,
                text="",
                border_width_checked = 5,
                variable=user_answers[i],
                value=j,
                width=0,  
                height=0,
                border_width_unchecked=3,
                radiobutton_width = 27,
                radiobutton_height = 27)  
            radio.grid(row=1, column=j+1, sticky="w", padx=0, pady=0) 
        frames.append(frame)

    def nop_bai():
        result = [var.get() for var in user_answers]
        correct = sum(1 for i in range(len(result)) if result[i] == answ[i])
        with open("userdata.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        if len(lines) > 1:
            parts = lines[sl+1].strip().split()
            if parts:
                parts[0] = str(int(parts[0]) + 1)
                parts[1] = str(correct) if len(parts) > 1 else str(correct)
                lines[sl+1] = " ".join(parts) + "\n"
        with open("userdata.txt", "w") as file:
            file.writelines(lines)
        with open(f"report/{name}.txt", "a", encoding="utf-8") as file: 
            file.write(f"{correct}\n")  
        res()
        tn.destroy()

    def res():
        hkq = ctk.CTkToplevel()
        hkq.title("Kết quả")
        hkq.geometry("550x350") 
        hkq.resizable(False, False)
        hkq.configure(fg_color="#43B3AE")

        tn.withdraw()

        #TOP
        top_frame = ctk.CTkFrame(hkq, fg_color="#FF5733", corner_radius=10)
        top_frame.pack(fill="x", padx=10, pady=10)

        #NAME
        with open("userdata.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        ths = f"Thí sinh: {lines[0].strip()}"  
        ts = ctk.CTkLabel(top_frame, text=ths, font=("Arial", 16), text_color="white", fg_color="#FF5733", anchor="center")
        ts.pack(side="top", padx=5)

        #TL
        content_frame = ctk.CTkFrame(hkq, fg_color="white", corner_radius=10)
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        #TN
        with open(f"report/BODE{sl+1}.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        #Test score sẽ là số ở dòng cuối cùng của file
        test_score = int(lines[-1].strip())
        test_score_frame = ctk.CTkFrame(content_frame, fg_color="#44A5E1", corner_radius=10)
        test_score_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        test_label = ctk.CTkLabel(test_score_frame, text="Điểm trách nghiệm", font=("Arial", 16), text_color="black", anchor="center")
        test_label.pack(pady=10)
        
        # Cập nhật màu sắc cho điểm trắc nghiệm
        if test_score < 4:
            test_score_color = "red"  
        elif test_score < 6:
            test_score_color = "yellow"   
        else:
            test_score_color = "green" 

        test_score_label = ctk.CTkLabel(test_score_frame, text=f"{test_score}/7", font=("Arial", 24, "bold"), text_color=test_score_color, anchor="center")
        test_score_label.pack(pady=5)

        # Phần thông tin "Điểm tự luận"
        diemtl = 0
        diemtl_frame = ctk.CTkFrame(content_frame, fg_color="#FFBD39", corner_radius=10)
        diemtl_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        tl_label = ctk.CTkLabel(diemtl_frame, text="Điểm tự luận", font=("Arial", 16), text_color="black", anchor="center")
        tl_label.pack(pady=10)

        if diemtl < 6:
            diemtl_color = "red"  
        elif diemtl < 9:
            diemtl_color = "yellow"  
        elif diemtl < 11:
            diemtl_color = "lightgreen"  
        else:
            diemtl_color = "green"  

        diemtl_label = ctk.CTkLabel(diemtl_frame, text=f"COMMING SOON", font=("Arial", 24, "bold"), anchor="center")
        diemtl_label.pack(pady=5)

        # Cấu hình grid cho content_frame
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        def on_close():
            hkq.destroy()
            tn.destroy()
            hsg(mainloop = True)

        hkq.protocol("WM_DELETE_WINDOW", on_close)
        hkq.mainloop()

    submitbtn = ctk.CTkButton(frmcau, text="Nộp bài", command=nop_bai)
    submitbtn.pack(pady= 20)

    tn.mainloop()
ccau = 45
answ = [0, 2, 3, 3, 1]  
sl = 0
name = "Bộ đề số 1"
total_seconds = 180
tracnghiem(ccau, answ, sl, name, total_seconds)