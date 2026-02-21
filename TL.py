import customtkinter as ctk
import os
import subprocess
import time
import configparser
import sys
import platform
from assets.Codebox import *
from tkinter import messagebox, filedialog
import shutil
import tempfile

version = sys.version.split("\n")[0] 
bit_arch = platform.architecture()[0]
machine = platform.machine()
system = sys.platform  

tl = ctk.CTk()
tl.geometry("800x400")
tl.title("Chấm điểm tự luận")
tl.minsize(600,300)

tl.grid_columnconfigure(1, weight=9)
tl.grid_columnconfigure(0, weight=1)
tl.grid_rowconfigure(1, weight=1)
tl.grid_rowconfigure(0, weight=9)

def flie():
    dan = filedialog.askopenfilename(title = "Chọn tệp chứa code của bạn (C++ / Python)", filetypes=[("Python / Cpp", "*.py;*.cpp"),("Python files", "*.py"), ("C++ files", "*.cpp")])
    if dan:
        return dan


baihs = flie()
problempath = "de/Bộ đề số 1/BAICUDE"
problemname = "CAU3"
dename = "Bộ đề số 1"
ts = "Annsdjf"

testcase = sorted([os.path.join(problempath, d) for d in os.listdir(problempath) if d.startswith("test") and os.path.isdir(os.path.join(problempath, d))])

frmchinh = ctk.CTkFrame(tl, fg_color="#43B3AE", corner_radius=0)
frmchinh.grid(column = 1, row = 0, rowspan=2, sticky = "nsew")
frmtest = ctk.CTkScrollableFrame(tl, corner_radius=0)
frmtest.grid(row = 0,column = 0, sticky = "nsew")
frmbtn = ctk.CTkFrame(tl, corner_radius=0)
frmbtn.grid(row = 1, column = 0, sticky = "nsew")

#Frmtest
def hientest(tentest):
    ht = ctk.CTkToplevel(tl)
    ht.title(f"Test case: {tentest}")
    ht.geometry("600x400")
    ht.resizable(False, False)
    ht.attributes("-topmost", True)
    # Load file
    inputfile = open(os.path.join(tentest, f"{problemname}.inp"), encoding="utf-8").readlines()
    outputfile = open(os.path.join(tentest, f"{problemname}.out"), encoding="utf-8").readlines()

    #MAIN
    main_frame = ctk.CTkFrame(ht)
    main_frame.pack(fill="both", expand=True)

    # Input
    inpla = ctk.CTkLabel(main_frame, text="INPUT:", font=("Consolas", 15, "bold"))
    inpla.grid(row=0, column=0, sticky="w", padx=5, pady=(0, 5))

    inpbox = ctk.CTkTextbox(main_frame, font=("Consolas", 14), height=120)
    inpbox.insert("end", "".join(inputfile))
    inpbox.configure(state="disabled")
    inpbox.grid(row=1, column=0, sticky="nsew", padx=5)

    # Output
    outla = ctk.CTkLabel(main_frame, text="OUTPUT:", font=("Consolas", 15, "bold"))
    outla.grid(row=2, column=0, sticky="w", padx=5, pady=(10, 5))

    outbox = ctk.CTkTextbox(main_frame, font=("Consolas", 14), height=120)
    outbox.insert("end", "".join(outputfile))
    outbox.configure(state="disabled")
    outbox.grid(row=3, column=0, sticky="nsew", padx=5)

    main_frame.rowconfigure(1, weight=1)
    main_frame.rowconfigure(3, weight=1)
    main_frame.columnconfigure(0, weight=1)

buttons = []
for i in range(len(testcase)):
    frame = ctk.CTkFrame(frmtest, fg_color="transparent", corner_radius=0)
    frame.pack(fill = "x", expand = True, pady=5, padx=(10,0))
    buttonfrm = ctk.CTkButton(frame, text=f"TEST{i+1:003}", corner_radius=0, border_color="black", border_width=2, height=50, fg_color="#C5C5C5", text_color="black", font=("consolas", 20), hover_color="#94948F", command=lambda t=testcase[i]: hientest(t))
    buttonfrm.pack(fill = "x", expand = True)

    buttons.append(buttonfrm)

#BTN
probar = ctk.CTkProgressBar(frmbtn, corner_radius=0, progress_color="#FF5733", fg_color="#2C3E50")
probar.set(0)
probar.pack(pady = (20,10), fill="both", padx=10)

chamlai = ctk.CTkButton(frmbtn, corner_radius=0, text="Phúc khảo", command=lambda: chambai(baihs, problempath) if lang == "Python" else chambaicpp(baihs, problempath))
chamlai.pack(pady = (0,5), padx = 10, fill = "both")

nopbai = ctk.CTkButton(frmbtn, corner_radius=0, text="Nộp bài")
nopbai.pack(pady = 5, padx = 10, fill = "both")

rvcode = ctk.CTkButton(frmbtn, corner_radius=0, text="Review code", command=lambda: revicode())
rvcode.pack(pady = 5, padx = 10, fill = "both")

stpt = 1/len(testcase)

if baihs.split(".")[-1] == "py":
    lang = "Python"
elif baihs.split(".")[-1] == "cpp":
    lang = "C++"

def revicode():
    rc = ctk.CTkToplevel(tl)
    rc.title("Review code")
    rc.geometry("400x200")
    rc.attributes("-topmost", True)
    
    try:
        with open(baihs, "r", encoding="utf-8") as file:
            code = file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "Không tìm thấy file code. Thử nhập lại file code của bạn")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return

    cdb = CTkCodeBox(rc, language=lang)

    cdb.insert("end", code)
    cdb.configure(state="disabled")
    lbl = ctk.CTkLabel(rc, text=f"Tên tệp: {baihs}" + "\n" + f"Ngôn ngữ: {lang}" + "\n").pack(pady = (10,0))
    cdb.pack(fill = "both", expand = True, padx = 10, pady = (0,10))

#TT MAIN
st7le = {"font": ("Consolas Bold", 15), "text_color": "#FFFEFE"}
label1 = ctk.CTkLabel(frmchinh, text=f"Tên bài: {problemname.strip()}", **st7le)
label1.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

label2 = ctk.CTkLabel(frmchinh, text=f"Bộ đề: {dename.strip()}", **st7le)
label2.grid(row=1, column=0, sticky="w", padx=10)

label3 = ctk.CTkLabel(frmchinh, text=f"Thí sinh: {ts.strip()}", **st7le)
label3.grid(row=2, column=0, sticky="w", padx=10)

label4 = ctk.CTkLabel(frmchinh, text=f"Số test: {len(testcase)}", **st7le)
label4.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 0))

label5 = ctk.CTkLabel(frmchinh, text=f"INPUT/OUTPUT: STANDARD", **st7le)
label5.grid(row=1, column=1, sticky="w", padx=10)

label6 = ctk.CTkLabel(frmchinh, text=f"Bài thí sinh: {baihs.strip()}", **st7le)
label6.grid(row=2, column=1, sticky="w", padx=10)

frmchinh.grid_rowconfigure(3, weight=1)
frmchinh.grid_columnconfigure(1, weight=1)
log = ctk.CTkTextbox(frmchinh, font=("consolas", 15), corner_radius=0, wrap="word")
log.grid(row=3, column=0, rowspan=4, columnspan=2, sticky="nsew", padx = 5, pady = 5)
if lang == "Python":
    log.insert("end", f"Python {version} [{platform.python_compiler()} {bit_arch} ({machine})] on {system}" + "\n" + "\n")
else:
    try:
        version_info = subprocess.check_output(['g++', '--version'], stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        version_info = f"Error:\n{e}\n"

    try:
        verbose_info = subprocess.check_output(['g++', '-v'], stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        verbose_info = f"Error:\n{e}\n"
    log.insert("end", version_info + verbose_info + '\n')


log.configure(state="disabled")

def chambai(baihs, problempath):
    probar.set(0)
    log.configure(state = "normal")
    config = configparser.ConfigParser()
    config.read(f"{problempath}/Settings.cfg")

    problem_name = config["DEFAULT"].get("problem_name", None)
    student_code = baihs
    timeout_sec = config["DEFAULT"].getint("timeout", 1)
    input_from_file = config["DEFAULT"].getboolean("input_from_file", False)

    problem_path = problempath
    test_dirs = sorted([
        os.path.join(problem_path, d)
        for d in os.listdir(problem_path)
        if d.startswith("test") and os.path.isdir(os.path.join(problem_path, d))
    ])

    total = len(test_dirs)
    passed = 0

    log.insert("end", f"Chấm bài: {student_code} | Bài: {problem_name}" + "\n")
    log.insert("end", f"Giới hạn thời gian: {timeout_sec} giây | Nhập từ file: {input_from_file}" + "\n")
    log.insert("end", f"Số test: {total}\n" + "\n")
    log.update() 

    for index, test_dir in enumerate(test_dirs):
        inp_path = os.path.join(test_dir, f"{problem_name}.inp")
        out_path = os.path.join(test_dir, f"{problem_name}.out")

        try:
            with open(inp_path, "r") as f:
                test_input = f.read()

            with open(out_path, "r") as f:
                expected_output = f.read().strip()

            temp_dir = tempfile.mkdtemp(prefix="test_temp_")

            if input_from_file:
                shutil.copy(inp_path, temp_dir)

            start_time = time.time()

            if input_from_file:
                result = subprocess.run(
                    ["python", os.path.abspath(student_code)],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=timeout_sec
                )

                student_output_path = os.path.join(temp_dir, f"{problem_name}.out")

                if os.path.exists(student_output_path):
                    with open(student_output_path, "r") as f_out:
                        actual_output = f_out.read().strip()
                else:
                    actual_output = ""  

            else:
                result = subprocess.run(
                    ["python", student_code],
                    input=test_input,
                    capture_output=True,
                    text=True,
                    timeout=timeout_sec
                )
                actual_output = result.stdout.strip()

            elapsed = time.time() - start_time
            
            if actual_output == expected_output:
                passed += 1
                log.insert("end", f"✅ {test_dir} - Passed ({round(elapsed, 4)}s)" + "\n")
                buttons[index].configure(fg_color="green")  # Đổi màu button thành xanh
            else:
                log.insert("end", f"❌ {test_dir} - Wrong Answer" + "\n")
                log.insert("end", f"    🟢 Expected: {expected_output}" + "\n")
                log.insert("end", f"    🔴 Got     : {actual_output}" + "\n")
                buttons[index].configure(fg_color="yellow")  
            probar.set(probar.get()+stpt)

        except subprocess.TimeoutExpired:
            log.insert("end", f"❌ {test_dir} - Timeout (> {timeout_sec}s)" + "\n")
            buttons[index].configure(fg_color="yellow")  
            probar.set(probar.get()+stpt)
        except Exception as e:
            log.insert("end", f"❌ {test_dir} - Error: {str(e)}" + "\n")
            buttons[index].configure(fg_color="yellow") 
            probar.set(probar.get()+stpt)
        finally:
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

        log.update()  

    log.insert("end", "\nTổng kết: " + f"{passed}/{total} test đúng"+ "\n"+ "\n")
    log.configure(state="disabled")
    log.update()
    if passed == total: probar.configure(progress_color = "blue")

def chambaicpp(baihs, problempath):
    probar.set(0)
    log.configure(state = "normal")
    mingw_path = r"C:\MinGW\bin\g++.exe"
    config = configparser.ConfigParser()
    config.read(f"{problempath}/Settings.cfg")

    timeout_sec = config["DEFAULT"].getint("timeout", 1)
    input_from_file = config["DEFAULT"].getboolean("input_from_file", False)

    source_cpp = baihs
    output_exe = baihs.split(".")[0] + ".exe"

    problempath = "de/Bộ đề số 1/BAICUDE"

    testcase = sorted([os.path.join(problempath, d) for d in os.listdir(problempath) if d.startswith("test") and os.path.isdir(os.path.join(problempath, d))])

    total = len(testcase)
    passed = 0

    log.insert("end", f"Chấm bài: {source_cpp} | Bài: {problemname}" + "\n")
    log.insert("end", f"Giới hạn thời gian: {timeout_sec} giây | Nhập từ file: {input_from_file}" + "\n")
    log.insert("end", f"Số test: {total}\n" + "\n")
    log.update() 

    # 1. Biên dịch code
    compile_result = subprocess.run(
        [mingw_path, source_cpp, "-o", output_exe],
        capture_output=True,
        text=True,
        timeout=10
    )

    if compile_result.returncode != 0:
        log.insert("end","❌ Compile lỗi:")
        log.insert("end",compile_result.stderr)
        log.update()
    else:
        log.insert("end","✅ Compile thành công." + "\n")
        log.update()

        config = configparser.ConfigParser()
        config.read(f"{problempath}/Settings.cfg")

        problem_name = config["DEFAULT"].get("problem_name", None)
        student_code = baihs
        timeout_sec = config["DEFAULT"].getfloat("timeout", 1)
        input_from_file = config["DEFAULT"].getboolean("input_from_file", False)

        for index, test_dir in enumerate(testcase):
            inp_path = os.path.join(test_dir, f"{problem_name}.inp")
            out_path = os.path.join(test_dir, f"{problem_name}.out")
            
            try:
                with open(inp_path, "r") as f:
                    test_input = f.read()

                with open(out_path, "r") as f:
                    expected_output = f.read().strip()

                temp_dir = tempfile.mkdtemp(prefix="test_temp_")

                if input_from_file:
                    shutil.copy(inp_path, temp_dir)

                start_time = time.time()

                if input_from_file:
                    result = subprocess.run(
                        [output_exe],
                        cwd=temp_dir,
                        capture_output=True,
                        text=True,
                        timeout=timeout_sec
                    )
                
                    student_output_path = os.path.join(temp_dir, f"{problem_name}.out")

                    if os.path.exists(student_output_path):
                        with open(student_output_path, "r") as f_out:
                            actual_output = f_out.read().strip()
                    else:
                        actual_output = ""  
                else:
                    result = subprocess.run(
                        [output_exe],
                        input=test_input,
                        capture_output=True,
                        text=True,
                        timeout=1  # giới hạn thời gian ở đây
                    )
                actual_output = result.stdout.strip()

                elapsed = time.time() - start_time
                if actual_output == expected_output:
                    passed += 1
                    log.insert("end",f"✅ {test_dir} - Passed ({round(elapsed, 4)}s)"+ "\n")
                    log.update()
                    buttons[index].configure(fg_color="green")  
                else:
                    log.insert("end",f"❌ {test_dir} - Wrong Answer"+ "\n")
                    log.insert("end",f"    🟢 Expected: {expected_output}"+ "\n")
                    log.insert("end",f"    🔴 Got     : {actual_output}"+ "\n")
                    log.update()
                    buttons[index].configure(fg_color="yellow")  
                probar.set(probar.get()+stpt)
            except subprocess.TimeoutExpired:
                log.insert("end",f"❌ {test_dir} - Timeout (> {timeout_sec}s)"+ "\n")
                log.update()
                probar.set(probar.get()+stpt)
            except Exception as e:
                log.insert("end",f"❌ {test_dir} - Error:", str(e)+ "\n")
                log.update()
                probar.set(probar.get()+stpt)
            finally:
                if 'temp_dir' in locals() and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)

        # Tổng kết
        log.insert("end", "\nTổng kết: " + f"{passed}/{total} test đúng"+ "\n"+ "\n")
        log.configure(state="disabled")
        log.update()
        if passed == total: probar.configure(progress_color = "blue")

tl.mainloop()
