'''import customtkinter as ctk
from tkinter import Text

def tracnghiem(locde,questions,time,answ,sl):
    #locde.withdraw()
    def countdown(time_left, total_time):
        if time_left >= 0:
            hours, remainder = divmod(time_left, 3600) 
            minutes, seconds = divmod(remainder, 60)  
            tilb.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
            progress.set((total_time - time_left) / total_time)  

            tn.after(1000, countdown, time_left - 1, total_time)  
        else:
            progress.set(1)  
            nop_bai()

    tn = ctk.CTk()
    with open("setting.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        if len(lines) > 1:
            parts = lines[1].strip().split()
            if parts[1] == "1":tn.attributes('-fullscreen', True)
            else: tn.geometry("1000x700")
    tn.configure(fg_color="#E3E8F0")
    tn.minsize(800,500)

    # INFO
    frmif = ctk.CTkFrame(tn, fg_color="#3131AF",corner_radius=0)
    frmif.place(relx=0, rely=0, relwidth=0.8, relheight=0.05)

    # TIME
    frmtime = ctk.CTkFrame(tn, fg_color="#FFFFFF",corner_radius=0)
    frmtime.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.05)

    # TIME LABEL
    tilb = ctk.CTkLabel(frmtime, text="180:00", font=("Segoe UI", 15), text_color="black")
    tilb.place(relx=0.1, rely=0.1, relwidth=0.8)

    # PROGRESS BAR
    progress = ctk.CTkProgressBar(frmtime, corner_radius=0, progress_color="#44A5E1")
    progress.place(relx=0, rely=0.9, relwidth=1, relheight=0.2)
    progress.set(0)  

    # TÊN THÍ SINH
    thisinh = ctk.StringVar(master=frmif)
    with open("userdata.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    thisinh.set(f"Thí sinh: {lines[0]}")
    lbl_ts = ctk.CTkLabel(frmif, textvariable=thisinh, font=("Arial Bold", 15),text_color="white")
    lbl_ts.place(relx=0.1, rely=0.3, relwidth=0.8)

    # Frame danh sách câu hỏi
    frmlc = ctk.CTkFrame(tn, fg_color='white')
    for i in range(5):  
        frmlc.grid_columnconfigure(i, weight=1)
    frmlc.place(relx=0, rely=0, relwidth=0.197, relheight=0.92)

    # Khung câu hỏi chính
    frmcau = ctk.CTkScrollableFrame(tn, fg_color="transparent")
    frmcau.place(relx=0, rely=0.05, relwidth=0.8, relheight=0.95)

    # Danh sách đáp án của người dùng
    #user_answers = [ctk.IntVar(value=-1) for _ in questions]

    # Tạo danh sách câu hỏi động
    frames = []
    for idx, (question, answers) in enumerate(questions):
        frame = ctk.CTkFrame(frmcau, fg_color="white", corner_radius=10, border_width=2, border_color="#D3D3D3")
        frame.pack(pady=15, padx=15, fill="x")  # Increased padding for better spacing
        frame.grid_columnconfigure(0)
        frame.grid_rowconfigure(0)
        
        #SI ZE LA BE
        def update_size(event):
            widget_width = 0
            widget_height = int(lbl.index("end-1c").split('.')[0])  # Calculate number of lines
            for line in lbl.get("1.0", "end-1c").split("\n"):
                if len(line) > widget_width:
                    widget_width = len(line) + 1
            lbl.config(width=widget_width, height=widget_height)
        
        lbl = Text(frame, wrap="word", font=("Arial", 16))
        lbl.insert("1.0", f"Câu {idx+1}: {question}")
        lbl.bind("<Configure>", update_size) 
        lbl.configure(state="normal")  
        lbl.grid(row=0, column=0, ipadx=50, ipady=50, sticky="NW")

        for ans_idx, ans in enumerate(answers):
            ctk.CTkRadioButton(frame, text=ans, variable=user_answers[idx], value=ans_idx, font=("Arial", 14), text_color="black",hover_color="#E0E0E0").grid(row=ans_idx+1, column=0, sticky="we", pady=(0,5), padx=10) 
    
        frames.append(frame)

    # Chuyển đến câu hỏi khi bấm số
    def go_to_question(q):
        frmcau._parent_canvas.yview_moveto(q / len(questions))

    # Tạo bảng danh sách câu hỏi
    frmlc.grid_rowconfigure(0, weight=0)
    lbl_dsch = ctk.CTkLabel(frmlc, text="Danh sách câu hỏi", font=("Arial", 14, "bold"), text_color="black")
    lbl_dsch.grid(row=0, column=0, columnspan=5, pady=10, sticky="ew") 


    for i in range(len(questions)):  
        btn = ctk.CTkButton(frmlc, text=f"{i+1:02d}", width=40, height=40, fg_color="blue",hover_color="darkblue", text_color="white",command=lambda q=i: go_to_question(q))
        row = i // 5
        col = i % 5
    btn.grid(row=row+1, column=col, padx=3, pady=5, sticky="nsew")

    # Nút nộp bài
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

        with open(f"report/BODE{sl+1}.txt", "a", encoding="utf-8") as file:  # Mở file ở chế độ append (a)
            file.write(f"{correct}\n")  # Ghi kết quả vào cuối file

        #locde.deiconify()
        show_result()
        tn.destroy()
    # THÔNG BÁO KẾT QUẢ
    def show_result():
        hkq = ctk.CTkToplevel()
        hkq.title("Kết quả")
        hkq.geometry("550x350")  # Chỉnh sửa kích thước cửa sổ
        hkq.resizable(False, False)
        hkq.configure(fg_color="#43B3AE")
        
        # Ẩn cửa sổ trắc nghiệm (TN)
        tn.withdraw()

        # Phần tiêu đề
        top_frame = ctk.CTkFrame(hkq, fg_color="#FF5733", corner_radius=10)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Đọc tên thí sinh từ tệp userdata.txt
        with open("userdata.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        ths = f"Thí sinh: {lines[0].strip()}"  # Sử dụng strip() để loại bỏ ký tự xuống dòng
        ts = ctk.CTkLabel(top_frame, text=ths, font=("Arial", 16), text_color="white", fg_color="#FF5733", anchor="center")
        ts.pack(side="top", padx=5)

        # Khung chứa thông tin kết quả
        content_frame = ctk.CTkFrame(hkq, fg_color="white", corner_radius=10)
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Phần thông tin "Điểm trắc nghiệm"
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

        # Cập nhật màu sắc cho điểm tự luận
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
            tn.quit()  
        hkq.protocol("WM_DELETE_WINDOW", on_close)
        hkq.mainloop()

    submitbtn = ctk.CTkButton(frmlc, text="Nộp bài", command=nop_bai)
    submitbtn.place(relx = 0, rely = 0.9, relwidth = 1, relheight = 0.1)

    #countdown(time, time)
    tn.mainloop()

tracnghiem(1,2,3,4,5)'''