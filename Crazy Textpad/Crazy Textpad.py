from tkinter import *
from tkinter import ttk, messagebox, font, filedialog
from PIL import Image,ImageTk
import time, win32api
import mysql.connector as db
from fpdf import FPDF

class TextPad:
    def __init__(self, root):
        self.window = root
        self.window.title(f"Crazy TextPad        New Document")
        mainframe = Frame(self.window, bg="white")
        mainframe.pack(pady=56)



        self.permission_to_update = 0
        #self.main_writing_space = None

        self.db_pwd_store = None
        self.record_no = -1
        self.record_status = "Yes"
        self.acc_name = None
        self.pwd_acc = None
        self.total_word = 0
        self.total_line = 0
        self.saved_file_name = "New Document"
        self.searching_things_in_google = "Nothing To Show"
        self.send_msg_to_wp = "Nothing To Show"
        self.pdf_saved_file_name = "Nothing To Show"
        self.saved_file_name_in_google_drive = "Nothing To Show"

        self.font_tag_name_store = []
        self.font_tag_counter = 0

        self.current_font_size = 20
        self.current_font = "Arial"

        self.font_family = StringVar()

        self.get_time = -1
        self.curr_acc_pwd = None

        # Some basic function call
        self.__header()
        self.__writing_area()
        self.__footer()
        self.__menu_decor()


    def __menu_decor(self):# Menu decorating function
        global file_new_img, file_open_img, file_save_img, file_pdf_img, file_print_img, file_exit_img, edit_undo_img, edit_redo_img, edit_cut_img, edit_copy_img, edit_paste_img, edit_clear_img, view_find_img, view_replace_img, view_dark_img, view_light_img, customization_bold_img, customization_italic_img, customization_underline_img, customization_foreground_color_img, customization_background_color_img
        menu_control = Menu(self.window)
        self.window.config(menu=menu_control)

        # Image bringing for menu
        file_new_img = ImageTk.PhotoImage(Image.open("sketch_images/new_img.jpg").resize((30,30),Image.ANTIALIAS))
        file_open_img = ImageTk.PhotoImage(Image.open("sketch_images/open_img.jpg").resize((30,30),Image.ANTIALIAS))
        file_save_img = ImageTk.PhotoImage(Image.open("sketch_images/save_img.png").resize((30,30),Image.ANTIALIAS))
        file_pdf_img = ImageTk.PhotoImage(Image.open("TextPad_Images/pdf_text.jpg").resize((30, 30), Image.ANTIALIAS))
        file_print_img = ImageTk.PhotoImage(Image.open("TextPad_Images/print_img.png").resize((30, 30), Image.ANTIALIAS))
        file_exit_img = ImageTk.PhotoImage(Image.open("sketch_images/exit_img.png").resize((30,30),Image.ANTIALIAS))

        edit_undo_img = ImageTk.PhotoImage(Image.open("sketch_images/undo_img.jpg").resize((30,30),Image.ANTIALIAS))
        edit_redo_img = ImageTk.PhotoImage(Image.open("TextPad_Images/redo_icon.png").resize((30, 30), Image.ANTIALIAS))
        edit_cut_img = ImageTk.PhotoImage(Image.open("sketch_images/cut_img.png").resize((30, 30), Image.ANTIALIAS))
        edit_copy_img = ImageTk.PhotoImage(Image.open("sketch_images/copy_img.jpg").resize((30, 30), Image.ANTIALIAS))
        edit_paste_img = ImageTk.PhotoImage(Image.open("sketch_images/paste_img.jpg").resize((30, 30), Image.ANTIALIAS))
        edit_clear_img = ImageTk.PhotoImage(Image.open("sketch_images/clear_img.png").resize((30, 30), Image.ANTIALIAS))

        view_find_img =  ImageTk.PhotoImage(Image.open("sketch_images/magnifier.jpg").resize((30, 30), Image.ANTIALIAS))
        view_replace_img = ImageTk.PhotoImage(Image.open("TextPad_Images/replace_icon.png").resize((30, 30), Image.ANTIALIAS))
        view_dark_img = ImageTk.PhotoImage(Image.open("TextPad_Images/dark_mode_img.png").resize((30, 30), Image.ANTIALIAS))
        view_light_img = ImageTk.PhotoImage(Image.open("TextPad_Images/bulb_img.jpg").resize((30, 30), Image.ANTIALIAS))

        customization_bold_img = ImageTk.PhotoImage(Image.open("TextPad_Images/bold_img.jpg").resize((30, 30), Image.ANTIALIAS))
        customization_italic_img = ImageTk.PhotoImage(Image.open("TextPad_Images/italic_img.png").resize((30, 30), Image.ANTIALIAS))
        customization_underline_img = ImageTk.PhotoImage(Image.open("TextPad_Images/underline_img.png").resize((30, 30), Image.ANTIALIAS))
        customization_foreground_color_img = ImageTk.PhotoImage(Image.open("TextPad_Images/font_color.png").resize((30, 30), Image.ANTIALIAS))
        customization_background_color_img = ImageTk.PhotoImage(Image.open("TextPad_Images/background_color.png").resize((30, 30), Image.ANTIALIAS))

        # Menu Make
        self.file_menu = Menu(menu_control,tearoff=False)
        menu_control.add_cascade(label="File",menu=self.file_menu)
        self.file_menu.add_command(label="New", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial",10,"bold","italic"), accelerator="(Ctrl+N)", compound=LEFT, image=file_new_img, command=self.new_window)
        self.file_menu.add_command(label="Open", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial",10,"bold","italic"), accelerator="(Ctrl+O)", compound=LEFT, image=file_open_img, command=self.open_another_file)
        self.file_menu.add_separator(background="green")
        self.file_menu.add_command(label="Save", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), compound=LEFT, image=file_save_img, command=self.save)
        self.file_menu.add_command(label="Save As", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial",10,"bold","italic"), accelerator="(Ctrl+S)", compound=LEFT, image=file_save_img, command=self.save_as)
        self.file_menu.add_command(label="Save File as PDF", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial",10,"bold","italic"), accelerator="(Alt+P)", compound=LEFT, image=file_pdf_img, command=self.save_file_as_pdf)
        self.file_menu.add_separator(background="green")
        self.file_menu.add_command(label="Print", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial",10,"bold","italic"), accelerator="(Ctrl+P)", compound=LEFT, image=file_print_img, command=self.print_a_file)
        self.file_menu.add_command(label="Exit", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial",10,"bold","italic"), accelerator="ESC", compound=LEFT, image=file_exit_img, command=self.take_exit)
        self.window.bind('<Control-Key-n>', self.new_window)
        self.window.bind('<Control-Key-o>', self.open_another_file)
        self.window.bind('<Control-Key-s>', self.save_as)
        self.window.bind('<Alt-p>', self.save_file_as_pdf)
        self.window.bind('<Control-Key-p>', self.print_a_file)
        self.window.bind('<Escape>', self.take_exit)


        self.edit_menu = Menu(menu_control,tearoff=False)
        menu_control.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+Z)", compound=LEFT, image=edit_undo_img, command=self.undo)
        self.edit_menu.add_command(label="Redo", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+Y)", compound=LEFT, image=edit_redo_img, command=self.redo)
        self.edit_menu.add_separator(background="green")
        self.edit_menu.add_command(label="Cut", background="green", foreground="Yellow", activebackground="yellow",                 activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+X)", compound=LEFT, image=edit_cut_img, command=self.cut)
        self.edit_menu.add_command(label="Copy", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+C)", compound=LEFT, image=edit_copy_img)
        self.edit_menu.add_command(label="Paste", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+V)", compound=LEFT, image=edit_paste_img, command=self.paste)
        self.edit_menu.add_separator(background="green")
        self.edit_menu.add_command(label="Clear", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), compound=LEFT, image=edit_clear_img, command=self.clear)


        self.view_menu = Menu(menu_control,tearoff=False)
        menu_control.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Find", background="green", foreground="Yellow", activebackground="yellow",    activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+F)", compound=LEFT, image=view_find_img, command=self.find_UI)
        self.view_menu.add_command(label="Replace", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+R)", compound=LEFT, image=view_replace_img, command=self.replace_UI)
        self.view_menu.add_separator(background="green")
        self.view_menu.add_command(label="Dark Mode", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), compound=LEFT, image=view_dark_img, command=self.dark_mode)
        self.view_menu.add_command(label="Light Mode", background="green", foreground="Yellow", activebackground="yellow",       activeforeground="green", font=("Arial", 10, "bold", "italic"), compound=LEFT, image=view_light_img, command=self.light_mode)

        self.customization_menu = Menu(menu_control, tearoff=False)
        menu_control.add_cascade(label="Customization", menu=self.customization_menu)
        self.customization_menu.add_command(label="Bold", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+B)", compound=LEFT, image=customization_bold_img)
        self.customization_menu.add_command(label="Italics", background="green", foreground="Yellow", activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+I)", compound=LEFT, image=customization_italic_img)
        self.customization_menu.add_command(label="Underline", background="green", foreground="Yellow",                     activebackground="yellow", activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Ctrl+U)", compound=LEFT, image=customization_underline_img)
        self.customization_menu.add_separator(background="green")
        self.customization_menu.add_command(label="Foreground-Color", background="green", foreground="Yellow", activebackground="yellow",     activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Shift+F)", compound=LEFT, image=customization_foreground_color_img)
        self.customization_menu.add_command(label="Background-Color", background="green", foreground="Yellow", activebackground="yellow",      activeforeground="green", font=("Arial", 10, "bold", "italic"), accelerator="(Shift+B)", compound=LEFT, image=customization_background_color_img)


    def __header(self):# Header container make
        self.header_1 = Frame(self.window, bg="orange", relief=RAISED, bd=3, width=325, height=90)
        self.header_1.place(x=0, y=0)

        self.header_2 = Frame(self.window, bg="orange", relief=RAISED, bd=3, width=260, height=90)
        self.header_2.place(x=325, y=0)

        self.header_3 = Frame(self.window, bg="orange", relief=RAISED, bd=3, width=325, height=90)
        self.header_3.place(x=325*2-65, y=0)

        self.header_4 = Frame(self.window, bg="orange", relief=RAISED, bd=3, width=305, height=90)
        self.header_4.place(x=325*3-65, y=0)

        self.acc = Frame(self.window, bg="orange", relief=RAISED, bd=3, width=50+85, height=90)
        self.acc.place(x=325*4-85, y=0)

        # Store instructional buttons
        self.__header_1_decoration()
        self.__header_2_decoration()
        self.__header_3_decoration()
        self.__header_4_decoration()
        self.__acc_decoration()

    def __footer(self):# Footer Container make
        self.status_components = []

        self.footer_1 = Label(self.window, text="Total Word: 0", font=("Arial",10,"bold"), bg="gold", fg="brown", relief=RIDGE, bd=3, width=40, height=1)
        self.footer_1.place(x=0, y=90)

        self.footer_2 = Label(self.window, text="Total Line: 0", font=("Arial",10,"bold"), bg="gold", fg="brown", relief=RIDGE, bd=3, width=46, height=1)
        self.footer_2.place(x=325, y=90)

        self.footer_3 = Label(self.window, text=f"Working Time: 00:00:00", font=("Arial",10,"bold"), bg="gold", fg="brown", relief=RIDGE, bd=3, width=46, height=1)
        self.footer_3.place(x=(325+325)+3, y=90)

        self.footer_4 = Label(self.window, text="Account holder_name: Sam", font=("Arial", 10, "bold"), bg="gold", fg="brown", relief=RIDGE, bd=3, width=41, height=1)
        self.footer_4.place(x=(325 + 325 + 325+53), y=90)

        self.status_components.append(self.footer_1)
        self.status_components.append(self.footer_2)
        self.status_components.append(self.footer_3)
        self.status_components.append(self.footer_4)

    def __writing_area(self):
        make_scroll_vertical= Scrollbar(self.window)
        make_scroll_vertical.pack(side=RIGHT, fill=Y)

        self.main_writing_space = Text(self.window, font=(self.current_font, self.current_font_size), relief=RAISED, bd=10, yscrollcommand=make_scroll_vertical.set, undo=True)
        self.main_writing_space.pack(fill=BOTH, expand=1, anchor=W)
        self.main_writing_space.focus()

        make_scroll_vertical.config(command=self.main_writing_space.yview)

    def __header_1_decoration(self):
        global l_img,m_img,r_img

        # Image bringing
        l_img = ImageTk.PhotoImage(Image.open("TextPad_Images/l_align.png").resize((50,50),Image.ANTIALIAS))
        m_img = ImageTk.PhotoImage(Image.open("TextPad_Images/m_align.png").resize((50, 50), Image.ANTIALIAS))
        r_img = ImageTk.PhotoImage(Image.open("TextPad_Images/r_align.png").resize((50, 50), Image.ANTIALIAS))

        self.header_1_components = []

        font_size_controller = Scale(self.header_1, font=("Arial",10,"bold"), width=15, orient=HORIZONTAL, background="green", foreground="gold", from_=1, to=100, activebackground="red", relief=RAISED, bd=2, command=self.change_font_size)
        font_size_controller.place(x=0,y=0)
        font_size_controller.set(self.current_font_size)

        # Make buttons
        l_align = Button(self.header_1, width=30, height=30, image=l_img, bg="black", relief=RAISED, bd=3, command=self.make_align_left)
        l_align.place(x=110+20, y=2)

        m_align = Button(self.header_1, width=30, height=30, image=m_img, bg="black", relief=RAISED, bd=3, command=self.make_align_center)
        m_align.place(x=110+90, y=2)

        r_align = Button(self.header_1, width=30, height=30, image=r_img, bg="black", relief=RAISED, bd=3, command=self.make_align_right)
        r_align.place(x=280-10, y=2)

        self.font_size_label = Label(self.header_1, text="Font Size", font=("Arial",15,"bold"), bg="orange", fg="brown")
        self.font_size_label.place(x=5,y=50)
        self.alignment_label = Label(self.header_1, text="Alignment", font=("Arial",15,"bold"), bg="orange", fg="brown")
        self.alignment_label.place(x=150+20, y=50)

        # Store instructional buttons
        self.header_1_components.append(font_size_controller)
        self.header_1_components.append(l_align)
        self.header_1_components.append(m_align)
        self.header_1_components.append(r_align)
        # self.header_1_components.append(font_size_label)
        # self.header_1_components.append(alignment_label)

    def __header_2_decoration(self):
        self.header_2_components = []

        # Font Collection
        font_combobox = ttk.Combobox(self.header_2, width=30, values=font.families(), foreground="blue", font=("Arial",10,"bold"), state="readonly", textvariable=self.font_family)
        font_combobox.place(x=5+5,y=0)
        font_combobox.set("Arial")
        print(font_combobox.get())

        font_combobox.bind("<<ComboboxSelected>>", self.change_font_manually)

        # Background Color list
        select_bg_color = [1,2,3,4,5,6]
        bg_color_combobox = ttk.Combobox(self.header_2, width=30, values=select_bg_color, foreground="red", font=("Arial",10,"bold"), state="readonly")
        bg_color_combobox.place(x=5+5, y=30)
        bg_color_combobox.current(0)

        bg_color_combobox.bind("<<ComboboxSelected>>", lambda e: self.change_line_space_to_selected_text(int(bg_color_combobox.get())))

        # Bullets list
        total_bullets = ["1   2   3", "#   #   #", "!   !   !", ">    >    >", "o   o   o"]
        bullet = ttk.Combobox(self.header_2, width=30, values=total_bullets, foreground="brown", font=("Arial",10,"bold"), state="readonly", background="black")
        bullet.place(x=5+5, y=60)
        bullet.current(0)

        bullet.bind("<<ComboboxSelected>>", lambda e: self.add_bullet_in_selected_text(bullet.get()))

        # Store instructional buttons
        self.header_2_components.append(font_combobox)
        self.header_2_components.append(bg_color_combobox)
        self.header_2_components.append(bullet)

    def __header_3_decoration(self):
        global ts_img,u_img,lc_img,w_mark_image,gs_image,wm_image

        # Image bringing
        ts_img = ImageTk.PhotoImage(Image.open("TextPad_Images/TS.png").resize((50,50), Image.ANTIALIAS))
        u_img = ImageTk.PhotoImage(Image.open("TextPad_Images/U.png").resize((50, 50), Image.ANTIALIAS))
        lc_img = ImageTk.PhotoImage(Image.open("TextPad_Images/L.png").resize((50, 50), Image.ANTIALIAS))
        w_mark_image = ImageTk.PhotoImage(Image.open("TextPad_Images/w_mark_img.png").resize((50, 50), Image.ANTIALIAS))
        gs_image = ImageTk.PhotoImage(Image.open("TextPad_Images/magnifier.jpg").resize((50, 30), Image.ANTIALIAS))
        wm_image = ImageTk.PhotoImage(Image.open("TextPad_Images/WM_img.png").resize((50, 30), Image.ANTIALIAS))

        self.header_3_components = []

        # Instructional Buttons
        u_case = Button(self.header_3, width=35, height=30, image=u_img, bg="#00FF00", relief=RAISED, bd=3)
        u_case.place(x=25, y=0)

        l_case = Button(self.header_3, width=35, height=30, image=lc_img, bg="#00FF00", relief=RAISED, bd=3)
        l_case.place(x=140, y=0)

        ts = Button(self.header_3, width=35, height=30, image=ts_img, bg="#00FF00", relief=RAISED, bd=3)
        ts.place(x=250, y=0)

        w_mark = Button(self.header_3, width=35, height=30, image=w_mark_image, bg="#00FF00", relief=RAISED, bd=3)
        w_mark.place(x=25, y=45)

        g_search = Button(self.header_3, width=35, height=30, image=gs_image, bg="#00FF00", relief=RAISED, bd=3)
        g_search.place(x=140, y=45)

        w_meaning = Button(self.header_3, width=35, height=30, image=wm_image, bg="#00FF00", relief=RAISED, bd=3)
        w_meaning.place(x=250, y=45)

        # Store instructional buttons
        self.header_3_components.append(u_case)
        self.header_3_components.append(l_case)
        self.header_3_components.append(ts)
        self.header_3_components.append(w_mark)
        self.header_3_components.append(g_search)
        self.header_3_components.append(w_meaning)

    def __header_4_decoration(self):
        global pdf_txt_img, g_drive_img, wp_logo_img, wiki_img, screenshot_image, paint_image
        self.header_4_components = []

        # Image Bringing
        pdf_txt_img = ImageTk.PhotoImage(Image.open("TextPad_Images/pdf_text_btn.jpg").resize((50, 50), Image.ANTIALIAS))
        g_drive_img = ImageTk.PhotoImage(Image.open("TextPad_Images/g_drive.jpg").resize((50, 50), Image.ANTIALIAS))
        wp_logo_img = ImageTk.PhotoImage(Image.open("TextPad_Images/wp_logo.jpg").resize((50, 50), Image.ANTIALIAS))
        wiki_img = ImageTk.PhotoImage(Image.open("TextPad_Images/wiki.png").resize((50, 50), Image.ANTIALIAS))
        screenshot_image = ImageTk.PhotoImage(Image.open("sketch_images/screenshot_img.jpg").resize((50, 50), Image.ANTIALIAS))
        paint_image = ImageTk.PhotoImage(Image.open("sketch_images/pencil.png").resize((30, 30), Image.ANTIALIAS))

        # Instructional buttons
        pdf_txt = Button(self.header_4, width=35, height=30, image=pdf_txt_img, font=("Arial", 11, "bold"), bg="#00FF00", relief=RAISED, bd=3)
        pdf_txt.place(x=25, y=0)

        sg = Button(self.header_4, width=35, height=30, image=g_drive_img, font=("Arial", 2, "bold"), bg="#00FF00", relief=RAISED, bd=3)
        sg.place(x=125, y=0)

        g = Button(self.header_4, width=35, height=30, image=wp_logo_img, bg="green", relief=RAISED, bd=3)
        g.place(x=230, y=0)

        w = Button(self.header_4, width=35, height=30, image=wiki_img, font=("Arial", 11, "bold"), bg="#00FF00", relief=RAISED, bd=3)
        w.place(x=25, y=45)

        ts = Button(self.header_4, width=35, height=30, image=screenshot_image, bg="#00FF00", relief=RAISED, bd=3)
        ts.place(x=125, y=45)

        op = Button(self.header_4, width=35, height=30, image=paint_image, font=("Arial", 11, "bold"), bg="#00FF00", relief=RAISED, bd=3)
        op.place(x=230, y=45)

        # Store instructional buttons
        self.header_4_components.append(pdf_txt)
        self.header_4_components.append(sg)
        self.header_4_components.append(g)
        self.header_4_components.append(w)
        self.header_4_components.append(ts)
        self.header_4_components.append(op)

    def __acc_decoration(self):
        global log_img, sign_up_img, history_img, log_out_img
        self.acc_components = []

        # Image Bringing
        log_img = ImageTk.PhotoImage(Image.open("TextPad_Images/login_image.png").resize((50, 50), Image.ANTIALIAS))
        sign_up_img = ImageTk.PhotoImage(Image.open("TextPad_Images/sign_up_image.png").resize((50, 50), Image.ANTIALIAS))
        history_img = ImageTk.PhotoImage(Image.open("TextPad_Images/history_check.png").resize((35, 35), Image.ANTIALIAS))
        log_out_img =  ImageTk.PhotoImage(Image.open("TextPad_Images/log_out_img.png").resize((35, 35), Image.ANTIALIAS))

        # Instructional buttons
        log_in_btn = Button(self.acc, width=35, height=30, image=log_img, bg="#008080", relief=RAISED, bd=3, command=self.__log_in)
        log_in_btn.place(x=10, y=0)

        sign_up_btn = Button(self.acc, width=35, height=30, image=sign_up_img, bg="#008080", relief=RAISED, bd=3, command=self.__sign_up)
        sign_up_btn.place(x=10, y=45)

        history_btn = Button(self.acc, width=35, height=30, image=history_img, bg="#008080", relief=RAISED, bd=3,   command=self.__history_check_options, state=DISABLED)
        history_btn.place(x=80, y=0)

        log_out_btn = Button(self.acc, width=35, height=30, image=log_out_img, bg="#008080", relief=RAISED, bd=3, command=self.__log_out, state=DISABLED)
        log_out_btn.place(x=80, y=45)

        self.acc_components.append(log_in_btn)
        self.acc_components.append(sign_up_btn)
        self.acc_components.append(history_btn)
        self.acc_components.append(log_out_btn)

    # Account Management
    def __sign_up(self):
        top = Toplevel()
        top.geometry("800x600")
        top.maxsize(800, 600)
        top.minsize(800, 600)
        top.config(bg="#262626")

        Label(top, text="Sign-Up", font=("Arial", 30, "bold", "italic", "underline"), bg="#262626").place(x=300, y=8)

        Label(top, text="-:Enter the Storage Password to Unlock:-", font=("Arial", 25, "bold", "italic"), bg="#262626", fg="gold").place(x=100, y=100)
        db_pwd_take = Entry(top, width=26, font=("Arial", 18, "bold", "italic"), bg="#262626", fg="#d6b575", relief=SUNKEN, bd=5, show="*")
        db_pwd_take.place(x=220, y=160)
        db_pwd_take.focus()

        def change_visibility_db_pwd():# Password visible and invisible controller
            if db_pwd_take['show'] == '*':
                db_pwd_take['show'] = ''
                visibility['text'] = "Hide"
            else:
                db_pwd_take['show'] = '*'
                visibility['text'] = "Show"

        visibility = Button(top, text="Show", font=("Arial", 18, "bold", "italic"), bg="#262626", fg="#FF4500", relief=RAISED, bd=1, command=change_visibility_db_pwd)
        visibility.place(x=580, y=160)

        Label(top, text="-:Enter New Account name:-", font=("Arial", 25, "bold", "italic"), bg="#262626", fg="gold").place(x=160, y=80+150)
        acc_name_take = Entry(top, width=23, font=("Arial", 25, "bold", "italic"), bg="#262626", fg="#d6b575", relief=SUNKEN, bd=5)
        acc_name_take.place(x=180, y=140+150)

        Label(top, text="-:Enter Password:-", font=("Arial", 25, "bold", "italic"), bg="#262626", fg="gold").place(x=240, y=220+150)
        pwd_entry = Entry(top, width=16, font=("Arial", 25, "bold", "italic"), bg="#262626", fg="#d6b575", relief=SUNKEN, bd=5, show="*")
        pwd_entry.place(x=240, y=270+150)


        def change_visibility_acc_pwd():
            if pwd_entry['show'] == '*':
                pwd_entry['show'] = ''
                visibility_other['text'] = "Hide"
            else:
                pwd_entry['show'] = '*'
                visibility_other['text'] = "Show"


        visibility_other = Button(top, text="Show", font=("Arial", 18, "bold", "italic"), bg="#262626", fg="#00FF00", relief=RAISED, bd=2, command=change_visibility_acc_pwd)
        visibility_other.place(x=550, y=270+150)

        conform_btn = Button(top, text="Make Account", font=("Arial", 15, "bold", "italic"), bg="#262626", fg="#FF0000", relief=RAISED, bd=5, command=lambda: self.__mysql_entry_for_sign_up(top, db_pwd_take.get(), acc_name_take.get(), pwd_entry.get()))
        conform_btn.place(x=300,y=340+180)

        top.mainloop()

    def __mysql_entry_for_sign_up(self, input_window, db_pwd, acc_name, acc_pwd):
        try:
            input_window.destroy()
            # Underscore joining in account_name
            acc_name = ("_".join(list(acc_name.split(" ")))).lower()

            # MySQL database access
            # Database Connect
            access_old = db.connect(host="localhost", user="root", password=db_pwd)
            switch_cur = access_old.cursor() # Cursor control take

            return_take = self.db_checking(switch_cur)# Checking if database is presnt or not

            def make_account_containing_database():# Database make if not present
                db_command = "CREATE DATABASE __modern_textpad_sam_account_container;"
                switch_cur.execute(db_command)

            if return_take == -1:# Indicating that name db not present
                make_account_containing_database()

            # Fetching all tables name
            switch_cur.execute("USE __modern_textpad_sam_account_container;")
            switch_cur.execute("SHOW TABLES;")
            all_result = switch_cur.fetchall()

            # If no table present pass it, else integrity check for same account_name table
            if len(all_result) == 0:
                pass
            else:
                return_take = self.__table_checking(all_result, acc_name)
                if return_take:# If same name table exist, warning show and process back
                    messagebox.showwarning("Name Conflict", "Same Account name present here! Please try other name")
                    return

            # Otherwise proceed
            take_input = f"CREATE TABLE {acc_name}(Record_no BIGINT, Account_pwd varchar(100) DEFAULT '{acc_pwd}' NOT NULL, Date varchar(12), Working_time varchar(10), Total_words BIGINT, Total_lines BIGINT, Saved_file_name varchar(100), Searching_things_in_google varchar(640), Send_message_to_whatsapp varchar(1000), PDF_saved_file_name varchar(100), Saved_file_name_in_google_drive varchar(100));"
            switch_cur.execute(take_input)
            access_old.commit()

            take_input = f"INSERT INTO {acc_name} VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            take_values = (1, acc_pwd, "Nothing To Show", "Nothing To Show", 0, 0, "Nothing To Show", "Nothing To Show", "Nothing To Show","Nothing To Show","Nothing To Show")
            switch_cur.execute(take_input, take_values)
            access_old.commit()

            self.record_no = 1
            self.record_status = "No"

            messagebox.showinfo("Complete", "Congratulation! Your Account Sign-up Complete")
        except:
            messagebox.showerror("Password Error", "Storage Passsword not match")

    def __log_in(self):
        top = Toplevel()
        top.geometry("800x600")
        top.maxsize(800, 600)
        top.minsize(800, 600)
        top.config(bg="#141414")

        Label(top, text="Log-in", font=("Arial", 30, "bold", "italic", "underline"), bg="#141414").place(x=300, y=8)
        Label(top, text="-:Enter the Storage Password to Unlock:-", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="gold").place(x=80, y=100)

        db_pwd_take = Entry(top, width=26, font=("Arial", 18, "bold", "italic"), bg="#141414", fg="#d6b575", relief=SUNKEN, bd=5, show="*")
        db_pwd_take.place(x=220, y=160)
        db_pwd_take.focus()

        def change_visibility_db_pwd():
            if db_pwd_take['show'] == '*':
                db_pwd_take['show'] = ''
                visibility['text'] = "Hide"
            else:
                db_pwd_take['show'] = '*'
                visibility['text'] = "Show"

        visibility = Button(top, text="Show", font=("Arial", 18, "bold", "italic"), bg="#141414", fg="#FF4500", relief=RAISED, bd=1, command=change_visibility_db_pwd)
        visibility.place(x=580, y=160)

        Label(top, text="-:Enter Existing Account name:-", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="gold").place(x=140, y=80 + 150)
        acc_name_take = Entry(top, width=23, font=("Arial", 25, "bold", "italic"), bg="#141414", fg="#d6b575", relief=SUNKEN, bd=5)
        acc_name_take.place(x=180, y=140 + 150)

        Label(top, text="-:Enter Account Password:-", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="gold").place(x=160, y=220 + 150)
        pwd_entry = Entry(top, width=16, font=("Arial", 25, "bold", "italic"), bg="#141414", fg="#d6b575", relief=SUNKEN, bd=5, show="*")
        pwd_entry.place(x=220, y=270 + 150)

        def change_visibility_acc_pwd():
            if pwd_entry['show'] == '*':
                pwd_entry['show'] = ''
                visibility_other['text'] = "Hide"
            else:
                pwd_entry['show'] = '*'
                visibility_other['text'] = "Show"

        visibility_other = Button(top, text="Show", font=("Arial", 18, "bold", "italic"), bg="#141414", fg="#00FF00", relief=RAISED, bd=2, command=change_visibility_acc_pwd)
        visibility_other.place(x=550, y=270 + 150)

        conform_btn = Button(top, text="Activate Account", font=("Arial", 15, "bold", "italic"), bg="#262626", fg="#FF0000",relief=RAISED, bd=5, command=lambda: self.__mysql_entry_for_log_in(top, db_pwd_take.get(), acc_name_take.get(), pwd_entry.get()))
        conform_btn.place(x=300, y=340 + 180)

        top.mainloop()

    def __mysql_entry_for_log_in(self, input_window, db_pwd, acc_name, acc_pwd):
        try:
            input_window.destroy()
            # Underscore joining in account_name
            real_acc_name = acc_name
            acc_name = ("_".join(list(acc_name.split(" ")))).lower()

            # MySQL database access
            # Database Connect
            access_old = db.connect(host="localhost", user="root", password=db_pwd)
            switch_cur = access_old.cursor()  # Cursor control take

            return_take = self.db_checking(switch_cur)# Database checking

            if return_take == -1:
                messagebox.showerror("Not Found"," Account not found, please sign-up at first then log-in")
                return
            else:
                switch_cur.execute("USE __modern_textpad_sam_account_container;")
                switch_cur.execute("SHOW TABLES;")
                all_result = switch_cur.fetchall()

                if len(all_result) == 0:
                    messagebox.showerror("Not Found", " Account not found, please sign-up at first then log-in")
                    return
                else:
                    return_take = self.__table_checking(all_result, acc_name)
                    if return_take:# If same name table exist, check acc_pwd
                        result = self.__acc_pwd_checking(switch_cur, access_old, acc_name, acc_pwd)
                        if result:
                            self.main_writing_space.delete(1.0, END)
                            self.status_components[0]['text'] = "Total Word: 0"
                            self.status_components[1]['text'] = "Total Line: 0"
                            self.status_components[2]['text'] = f"Working Time: 00:00:00"
                            self.status_components[3]['text'] = f"Account holder_name: {real_acc_name}"
                            self.get_time = -1
                            self.__time_counter()

                            self.db_pwd_store = db_pwd
                            self.acc_name = acc_name
                            self.pwd_acc = acc_pwd

                            self.main_writing_space.bind('<KeyRelease>',self.total_word_and_line_counter)
                            self.permission_to_update = 1

                            self.acc_components[0]['state'] = DISABLED
                            self.acc_components[1]['state'] = DISABLED
                            self.acc_components[2]['state'] = NORMAL
                            self.acc_components[3]['state'] = NORMAL
                        else:
                            messagebox.showerror("Password", "Password not match")
                    else:
                        messagebox.showwarning("Not Found", " Account not found, please sign-up at first then log-in")
                        return
        except:
            messagebox.showerror("Password Error", "Storage Passsword not match")

    def __acc_pwd_checking(self, switch_cur, access_old, acc_name, acc_pwd):
        take_input = f"Select Account_pwd from {acc_name} WHERE Record_no=1;"
        switch_cur.execute(take_input)

        self.curr_acc_pwd = switch_cur.fetchall()[0][0]
        access_old.commit()

        if self.curr_acc_pwd == acc_pwd:
            print(self.curr_acc_pwd)
            return True
        else:
            return False

    def db_checking(self, switch_cur):
        switch_cur.execute("SHOW DATABASES")  # All database list view
        db_chart = switch_cur.fetchall()  # Fetch database list
        take = []
        for x in db_chart:
            take.append(x[0])
        take.sort()

        # Database name used here: '__modern_textpad_sam_account_container'.
        # If this named database not present in your database, here the code present to make it
        # in your database automatically.

        def binary_search_db_check(take_it, start, end, find_it):  # Particular db name check
            while start <= end:
                mid = int((start + end) / 2)
                if take_it[mid] == find_it:
                    return take_it[mid]
                elif find_it > take[mid]:
                    start = mid + 1
                else:
                    end = mid - 1
            return -1

        return binary_search_db_check(take, 0, len(take) - 1, "__modern_textpad_sam_account_container")

    def __table_checking(self, all_result, acc_name):
        take = []
        for x in all_result:
            take.append(x[0])
        take.sort()

        # Checking account named table present or not
        def binary_search_table_check(take_it, start, end, find_it):
            while start <= end:
                mid = int((start + end) / 2)
                if take_it[mid] == find_it:
                    return True
                elif find_it > take[mid]:
                    start = mid + 1
                else:
                    end = mid - 1
            return False

        return binary_search_table_check(take, 0, len(take) - 1, acc_name)

    def __history_check_options(self):
        top = Toplevel(relief=RAISED, bd=10)
        top.title("History Checking Topics")
        top.geometry("800x600")
        top.maxsize(800, 600)
        top.minsize(800, 600)
        top.config(bg="#141414")

        general_information = Button(top, text="General Information", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="#FF0000", relief=RAISED, bd=5, activebackground="green", activeforeground="gold", command=lambda :self.__history_viewer(1))
        general_information.pack(pady=20)

        searching_google = Button(top, text="Google Search History", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="yellow", relief=RAISED, bd=5, activebackground="green", activeforeground="gold", command=lambda :self.__history_viewer(2))
        searching_google.pack(pady=20)

        send_msg_to_wp = Button(top, text="Whatsapp Messages", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="#00FF00", relief=RAISED, bd=5, activebackground="green", activeforeground="gold", command=lambda :self.__history_viewer(3))
        send_msg_to_wp.pack(pady=20)

        pdf_saved_file_name = Button(top, text="Saved PDF file names", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="magenta", relief=RAISED, bd=5, activebackground="green", activeforeground="gold", command=lambda :self.__history_viewer(4))
        pdf_saved_file_name.pack(pady=20)

        file_save_in_google_drive = Button(top, text="Saved file names in google drive", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="chocolate", relief=RAISED, bd=5, activebackground="green", activeforeground="gold", command=lambda :self.__history_viewer(5))
        file_save_in_google_drive.pack(pady=20)

        top.mainloop()

    def __history_viewer(self, instruction_no):
        root = Toplevel()

        # Frame make
        main_frame = Frame(root, bg="#141414")
        main_frame.pack(fill=BOTH, expand=1)

        # Canvas make
        my_canvas = Canvas(main_frame, bg="#141414")
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add a scrollbar to canvas
        my_scroll = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scroll.pack(side=RIGHT, fill=Y)

        # Configure the canvas
        my_canvas.config(yscrollcommand=my_scroll.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # Make second frame
        second_frame = Frame(my_canvas, bg="#141414")

        # Add that new frame to a window in the canvas
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        access_old = db.connect(host="localhost", user="root", password=self.db_pwd_store)
        switch_cur = access_old.cursor()  # Cursor control take

        switch_cur.execute("USE __modern_textpad_sam_account_container;")
        access_old.commit()

        if instruction_no == 1:
            root.title("General Information")
            root.geometry("1350x300")
            switch_cur.execute(f"SELECT Record_no,Account_pwd,Date,Working_time,Total_words,Total_lines,Saved_file_name FROM {self.acc_name};")
            result_take = switch_cur.fetchall()

            heading_names = ["Entry no","Account password","Date","Working Time","Total word","Total line","Saved file name"]

            col=0
            for every in heading_names:
                Label(second_frame, text=every, font=("Arial", 20, "bold", "italic", "underline"), bg="#141414", fg="gold").grid(row=0, column=col, padx=12)
                col+=1

            h_x = 1
            for every in result_take:
                v_y = 0
                for every_person in every:
                    Label(second_frame, text=every_person, font=("Arial",15,"bold"), bg="#141414", fg="green").grid(row=h_x, column=v_y, padx=15, pady=17)
                    print(every_person)
                    v_y+=1
                h_x+=1

        elif instruction_no == 2:
            root.title("Google Search History")
            root.geometry("700x500")
            switch_cur.execute(f"SELECT Record_no,Searching_things_in_google FROM {self.acc_name};")
            result_take = switch_cur.fetchall()

            heading_names = ["Entry no", "Google Search History"]

            col = 0
            for every in heading_names:
                Label(second_frame, text=every, font=("Arial", 20, "bold", "italic", "underline"), bg="#141414", fg="gold").grid(row=0, column=col, padx=12)
                col += 1

            h_x = 1
            for every in result_take:
                v_y = 0
                for every_person in every:
                    Label(second_frame, text=every_person, font=("Arial", 15, "bold"), bg="#141414", fg="green").grid(row=h_x, column=v_y, padx=15, pady=17)
                    print(every_person)
                    v_y += 1
                h_x += 1

        elif instruction_no == 3:
            root.title("Whatsapp messages")
            root.geometry("700x500")
            switch_cur.execute(f"SELECT Record_no,Send_message_to_whatsapp FROM {self.acc_name};")
            result_take = switch_cur.fetchall()

            heading_names = ["Entry no", "Whatsapp Message Record"]

            col = 0
            for every in heading_names:
                Label(second_frame, text=every, font=("Arial", 20, "bold", "italic", "underline"), bg="#141414", fg="gold").grid(row=0, column=col, padx=12)
                col += 1

            h_x = 1
            for every in result_take:
                v_y = 0
                for every_person in every:
                    Label(second_frame, text=every_person, font=("Arial", 15, "bold"), bg="#141414", fg="green").grid(row=h_x, column=v_y, padx=15, pady=17)
                    print(every_person)
                    v_y += 1
                h_x += 1

        elif instruction_no == 4:
            root.title("Files saved as PDF")
            root.geometry("700x500")
            switch_cur.execute(f"SELECT Record_no,PDF_saved_file_name FROM {self.acc_name};")
            result_take = switch_cur.fetchall()

            heading_names = ["Entry no", "PDF Converted File Name"]

            col = 0
            for every in heading_names:
                Label(second_frame, text=every, font=("Arial", 20, "bold", "italic", "underline"), bg="#141414", fg="gold").grid(row=0, column=col, padx=12)
                col += 1

            h_x = 1
            for every in result_take:
                v_y = 0
                for every_person in every:
                    Label(second_frame, text=every_person, font=("Arial", 15, "bold"), bg="#141414", fg="green").grid(row=h_x, column=v_y, padx=15, pady=17)
                    print(every_person)
                    v_y += 1
                h_x += 1

        elif instruction_no == 5:
            root.title("Saved file name in google drive")
            root.geometry("700x500")
            switch_cur.execute(f"SELECT Record_no,Saved_file_name_in_google_drive FROM {self.acc_name};")
            result_take = switch_cur.fetchall()

            heading_names = ["Entry no", "Saved File in Google Drive"]

            col = 0
            for every in heading_names:
                Label(second_frame, text=every, font=("Arial", 20, "bold", "italic", "underline"), bg="#141414", fg="gold").grid(row=0, column=col, padx=12)
                col += 1

            h_x = 1
            for every in result_take:
                v_y = 0
                for every_person in every:
                    Label(second_frame, text=every_person, font=("Arial", 15, "bold"), bg="#141414", fg="green").grid(row=h_x, column=v_y, padx=15, pady=17)
                    print(every_person)
                    v_y += 1
                h_x += 1

        root.mainloop()

    def __log_out(self):
        # Underscore joining in account_name
        self.acc_name = ("_".join(list(self.acc_name.split(" ")))).lower()

        # MySQL database access
        # Database Connect
        access_old = db.connect(host="localhost", user="root", password=self.db_pwd_store)
        switch_cur = access_old.cursor()  # Cursor control take

        switch_cur.execute("USE __modern_textpad_sam_account_container;")
        access_old.commit()

        if self.record_status == "No":
            take_input = f"DELETE FROM {self.acc_name} WHERE Record_no={self.record_no};"
            switch_cur.execute(take_input)
            access_old.commit()
            self.record_status = "Yes"
        else:
            take_input = f"SELECT COUNT(Record_no) from {self.acc_name};"
            switch_cur.execute(take_input)
            self.record_no = switch_cur.fetchall()[0][0]
            self.record_no+=1

        self.save()
        working_time_is = time.strftime("%H:%M:%S", time.gmtime(self.get_time))
        d = time.strftime("%d")
        m = time.strftime("%m")
        y = time.strftime("%Y")

        if self.saved_file_name == "New Document":
            saved_file_name = "Nothing To Show"
        else:
            saved_file_name = self.saved_file_name.split("/")
            saved_file_name = saved_file_name[len(saved_file_name)-1]

        take_input = f"INSERT INTO {self.acc_name} VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        take_values = (self.record_no, self.pwd_acc, f"{d}/{m}/{y}", working_time_is, self.total_word, self.total_line, saved_file_name, self.searching_things_in_google, self.send_msg_to_wp, self.pdf_saved_file_name, self.saved_file_name_in_google_drive)
        switch_cur.execute(take_input, take_values)
        access_old.commit()

        self.total_word = 0
        self.total_line = 0
        self.saved_file_name = "New Document"
        self.searching_things_in_google = "Nothing To Show"
        self.send_msg_to_wp = "Nothing To Show"
        self.pdf_saved_file_name = "Nothing To Show"
        self.saved_file_name_in_google_drive = "Nothing To Show"

        self.font_tag_name_store.clear()
        self.font_tag_counter = 0

        self.main_writing_space.unbind('<KeyRelease>')
        self.permission_to_update = 0

        self.get_time = -2
        self.main_writing_space.delete(1.0, END)
        self.saved_file_name = "New Document"
        self.window.title(f"Crazy TextPad          {self.saved_file_name}")

        self.status_components[0]['text'] = "Total Word: 0"
        self.status_components[1]['text'] = "Total Line: 0"
        self.status_components[2]['text'] = "Working Time: 00:00:00"
        self.status_components[3]['text'] = "Account holder name:"

        self.acc_components[0]['state'] = NORMAL
        self.acc_components[1]['state'] = NORMAL
        self.acc_components[2]['state'] = DISABLED
        self.acc_components[3]['state'] = DISABLED

        messagebox.showinfo("Log-Out", "You are log out from your current account")


    # New Menu Configuration
    def new_window(self, e=None):
        take_response = messagebox.askyesno("New Window Conformation","Do you want to open new Window?")
        if take_response:
            self.main_writing_space.delete(1.0,END)
            self.saved_file_name = "New Document"
            self.window.title(f"Crazy TextPad          {self.saved_file_name}")

    def open_another_file(self, e=None):
        file_name = filedialog.askopenfilename(initialdir="\Desktop", title="Select a file",filetypes=(("Text Files", "*.txt"), ("C Files", "*.c"), ("CPP Files", "*.cpp"), ("Python Files", "*.py"), ("HTML Files","*.html"), ("CSS Files","*.css"), ("JavaScript Files","*.js")))
        if file_name:
            self.main_writing_space.delete(1.0, END)
            self.saved_file_name = file_name
            self.window.title(f"Crazy TextPad         {self.saved_file_name}")
            get_file = open(file_name, "r")
            get_text = get_file.read()
            self.main_writing_space.insert(END,get_text)
            get_file.close()
            if self.permission_to_update == 1:
                self.total_word_and_line_counter(None)

    def save(self, e=None):
        if self.saved_file_name == "New Document":
            self.save_as()
        else:
            take_file = open(self.saved_file_name, "w")
            take_text = self.main_writing_space.get(1.0, END)
            take_file.write(take_text)
            take_file.close()
            messagebox.showinfo("Saved", "Your file saved securely")

    def save_as(self, e=None):
        take_file_name = filedialog.asksaveasfilename(initialdir="\Desktop", title="Save As", defaultextension=".txt", filetypes=(("Text Files", "*.txt"), ("C Files", "*.c"), ("CPP Files", "*.cpp"), ("Python Files", "*.py"), ("HTML Files","*.html"), ("CSS Files","*.css"), ("JavaScript Files","*.js")))
        if take_file_name:
            self.saved_file_name = take_file_name
            self.window.title(f"Crazy TextPad         {self.saved_file_name}")
            take_file = open(take_file_name,"w")
            take_text = self.main_writing_space.get(1.0, END)
            take_file.write(take_text)
            take_file.close()
            messagebox.showinfo("Successfully Saved", "Your file saved successfully")

    def save_file_as_pdf(self, e=None):
        self.main_writing_space.clipboard_clear()
        take_file_name = filedialog.asksaveasfilename(initialdir="\Desktop", title="Select location and name to save that file as PDF", defaultextension=".pdf")
        if take_file_name:
            self.pdf_saved_file_name = take_file_name.split("/")
            self.pdf_saved_file_name = self.pdf_saved_file_name[len(self.pdf_saved_file_name)-1]
            self.window.title(f"Crazy TextPad         {take_file_name}")
            pdf_control = FPDF()
            pdf_control.add_page()
            pdf_control.set_font(family="Arial", size=10)
            take_input = self.main_writing_space.get(1.0,END).split("\n")
            print(take_input)
            for i in take_input:
                pdf_control.cell(1000, 5, txt=i, ln=1, align="L")
            pdf_control.output(take_file_name)

            messagebox.showinfo("Saved as PDF", "The Current File Saved as PDF")

    def print_a_file(self, e=None):
        self.save()
        ask_pls = messagebox.askyesno("Conformation of printing", "Are you ready to print the file?")
        if ask_pls:
            win32api.ShellExecute(0, "print", self.saved_file_name, None, ".", 0)

    def take_exit(self, e=None):
        conform = messagebox.askyesno("Exit Conformation", "Are you sure to exit?")
        if conform:
            self.window.destroy()

    # Edit menu Configuration
    def undo(self):
        try:
            self.edit_menu.entryconfigure(0,command=self.main_writing_space.edit_undo)
        except:
            messagebox.showinfo("Container Empty", "No action to perform")

    def redo(self):
        try:
            self.edit_menu.entryconfigure(1,command=self.main_writing_space.edit_redo)
        except:
            messagebox.showinfo("Container Empty", "No action to perform")


    def cut(self):
        get_text = self.main_writing_space.get("sel.first", "sel.last")
        self.main_writing_space.delete("sel.first", "sel.last")
        print(get_text)
        self.main_writing_space.clipboard_clear()
        self.main_writing_space.clipboard_append(get_text)

    def copy(self):
        get_text = self.main_writing_space.get("sel.first", "sel.last")
        print(get_text)
        self.main_writing_space.clipboard_clear()
        self.main_writing_space.clipboard_append(get_text)

    def paste(self):
        self.main_writing_space.insert(INSERT,self.main_writing_space.clipboard_get())

    def clear(self):
        conform = messagebox.askyesno("Conformation to clean", "Do you want to clean the writing space?")
        if conform:
            self.main_writing_space.delete(1.0, END)

    def find_UI(self):
        top = Toplevel()
        top.title("Finding")
        top.geometry("600x300")
        top.maxsize(600, 300)
        top.minsize(600, 300)
        top.config(bg="#141414")

        Label(top, text="Enter a text to search", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="gold").place(x=135, y=50)
        take_entry = Entry(top, font=("Arial", 20, "bold", "italic"), bg="#141400", fg="#d6b575", insertbackground="#d6b575", relief=SUNKEN, bd=5)
        take_entry.place(x=150, y=120)
        take_entry.focus()

        def find_pattern(search_it):
            if self.main_writing_space.get(1.0, END):
                if search_it:
                    remove_highlight()
                    start_index = "1.0"
                    self.main_writing_space.tag_configure("highlight", background="red")
                    match_pattern = 0
                    while True:
                        # print("Start index: ", start_index)
                        start_index = self.main_writing_space.search(search_it, start_index, stopindex=END)
                        if not start_index:
                            break
                        # print(start_index)
                        end_pos = f"{start_index}+{len(search_it)}c"
                        match_pattern+=1
                        self.main_writing_space.tag_add("highlight", start_index, end_pos)
                        # print("end position: ", end_pos)
                        start_index = end_pos
                    messagebox.showinfo("Finding result", f"Total finding result: {match_pattern}")
                else:
                    messagebox.showinfo("Input Error", "Nothing to find")
            else:
                messagebox.showinfo("Text absent", "No text present")

        def remove_highlight():
            try:
                self.main_writing_space.tag_remove("highlight",1.0,END)
            except:
                print("Tag not found error")

        ok_btn = Button(top, text="Ok", width=5, font=("Arial", 18, "bold", "italic"), bg="#262626", fg="#FF0000", activebackground="#262626", activeforeground="#FF0000", command=lambda :find_pattern(take_entry.get()))
        ok_btn.place(x=100, y=200)

        remove_tag = Button(top, text="Remove Highlight", font=("Arial", 18, "bold", "italic"), bg="#262626", fg="#FF0000", activebackground="#262626", activeforeground="#FF0000", command=remove_highlight)
        remove_tag.place(x=300, y=200)

        top.mainloop()

    def replace_UI(self):
        top = Toplevel()
        top.title("Replacing")
        top.geometry("600x400")
        top.maxsize(600, 400)
        top.minsize(600, 400)
        top.config(bg="#141414")

        Label(top, text="Enter a text to search", font=("Arial", 25, "bold", "italic"), bg="#141414", fg="gold").place(x=135, y=50)
        Label(top, text="Find", font=("Arial", 17, "bold", "italic"), bg="#141414", fg="#00FF00").place(x=50, y=125)
        Label(top, text="Replace", font=("Arial", 17, "bold", "italic"), bg="#141414", fg="#00FF00").place(x=50, y=205)

        take_entry = Entry(top, font=("Arial", 20, "bold", "italic"), bg="#141400", fg="#d6b575", insertbackground="#d6b575", relief=SUNKEN, bd=5)
        take_entry.place(x=150, y=120)

        replacing_word = Entry(top, font=("Arial", 20, "bold", "italic"), bg="#141400", fg="#d6b575", insertbackground="#d6b575", relief=SUNKEN, bd=5)
        replacing_word.place(x=150, y=200)

        take_entry.focus()

        def replace_pattern(search_it, replaced_by):
            if self.main_writing_space.get(1.0, END):
                if search_it and replaced_by:
                    start_index = "1.0"
                    match_pattern = 0
                    while True:
                        start_index = self.main_writing_space.search(search_it, start_index, stopindex=END)
                        if not start_index:
                            break
                        end_pos = f"{start_index}+{len(search_it)}c"
                        match_pattern += 1
                        self.main_writing_space.replace(start_index, end_pos, replaced_by)
                        start_index = end_pos
                    messagebox.showinfo("Replacing result", f"Total replacing result: {match_pattern}")
                else:
                    messagebox.showinfo("Input Error", "Nothing to replace")
            else:
                messagebox.showinfo("Text absent", "No text present")

        ok_btn = Button(top, text="Ok", width=5, font=("Arial", 18, "bold", "italic"), bg="#262626", fg="#FF0000",        activebackground="#262626", activeforeground="#FF0000",         command=lambda: replace_pattern(take_entry.get(), replacing_word.get()))
        ok_btn.place(x=270, y=280)

        top.mainloop()











    # View menu Configuration
    def dark_mode(self):
        self.main_writing_space.config(bg="#0d0d0d", fg="#00FF00", insertbackground="green", selectbackground="#8989ff")

        self.header_1.config(bg="#474747")
        self.font_size_label.config(bg="#474747", fg="gold")
        self.alignment_label.config(bg="#474747", fg="gold")
        self.header_1_components[0].config(bg="#6c6c93")

        self.header_2.config(bg="#474747")
        self.header_3.config(bg="#474747")
        self.header_4.config(bg="#474747")
        self.acc.config(bg="#474747")

        for every in self.status_components:
            every.config(bg="#474747", fg="#00e600")

        self.file_menu.entryconfig("New",background="#474747")
        self.file_menu.entryconfig("Open", background="#474747")
        self.file_menu.entryconfig("Save", background="#474747")
        self.file_menu.entryconfig("Save As", background="#474747")
        self.file_menu.entryconfig("Save File as PDF", background="#474747")
        self.file_menu.entryconfig("Print", background="#474747")
        self.file_menu.entryconfig("Exit", background="#474747")
        self.file_menu.delete(2)
        self.file_menu.delete(5)
        self.file_menu.insert_separator(2, background="#474747")
        self.file_menu.insert_separator(6, background="#474747")

        self.edit_menu.entryconfig("Undo", background="#474747")
        self.edit_menu.entryconfig("Redo", background="#474747")
        self.edit_menu.entryconfig("Cut", background="#474747")
        self.edit_menu.entryconfig("Copy", background="#474747")
        self.edit_menu.entryconfig("Paste", background="#474747")
        self.edit_menu.entryconfig("Clear", background="#474747")
        self.edit_menu.delete(2)
        self.edit_menu.delete(5)
        self.edit_menu.insert_separator(2, background="#474747")
        self.edit_menu.insert_separator(6, background="#474747")


        self.view_menu.entryconfig("Find", background="#474747")
        self.view_menu.entryconfig("Replace", background="#474747")
        self.view_menu.entryconfig("Dark Mode", background="#474747")
        self.view_menu.entryconfig("Light Mode", background="#474747")
        self.view_menu.delete(2)
        self.view_menu.insert_separator(2, background="#474747")

        self.customization_menu.entryconfig("Bold", background="#474747")
        self.customization_menu.entryconfig("Italics", background="#474747")
        self.customization_menu.entryconfig("Underline", background="#474747")
        self.customization_menu.entryconfig("Foreground-Color", background="#474747")
        self.customization_menu.entryconfig("Background-Color", background="#474747", state=DISABLED)
        self.customization_menu.delete(3)
        self.customization_menu.insert_separator(3, background="#474747")

    def light_mode(self):
        self.main_writing_space.config(bg="white", fg="black", insertbackground="black", selectbackground="blue")

        self.header_1.config(bg="orange")
        self.font_size_label.config(bg="orange", fg="brown")
        self.alignment_label.config(bg="orange", fg="brown")
        self.header_1_components[0].config(bg="green")

        self.header_2.config(bg="orange")
        self.header_3.config(bg="orange")
        self.header_4.config(bg="orange")
        self.acc.config(bg="orange")

        for every in self.status_components:
            every.config(bg="orange", fg="brown")

        self.file_menu.entryconfig("New", background="green", foreground="Yellow")
        self.file_menu.entryconfig("Open", background="green", foreground="Yellow")
        self.file_menu.entryconfig("Save", background="green", foreground="Yellow")
        self.file_menu.entryconfig("Save As", background="green", foreground="Yellow")
        self.file_menu.entryconfig("Save File as PDF", background="green", foreground="Yellow")
        self.file_menu.entryconfig("Print", background="green", foreground="Yellow")
        self.file_menu.entryconfig("Exit", background="green", foreground="Yellow")
        self.file_menu.delete(2)
        self.file_menu.delete(5)
        self.file_menu.insert_separator(2, background="green")
        self.file_menu.insert_separator(6, background="green")

        self.edit_menu.entryconfig("Undo", background="green", foreground="Yellow")
        self.edit_menu.entryconfig("Redo", background="green", foreground="Yellow")
        self.edit_menu.entryconfig("Cut", background="green", foreground="Yellow")
        self.edit_menu.entryconfig("Copy", background="green", foreground="Yellow")
        self.edit_menu.entryconfig("Paste", background="green", foreground="Yellow")
        self.edit_menu.entryconfig("Clear", background="green", foreground="Yellow")
        self.edit_menu.delete(2)
        self.edit_menu.delete(5)
        self.edit_menu.insert_separator(2, background="green")
        self.edit_menu.insert_separator(6, background="green")

        self.view_menu.entryconfig("Find", background="green", foreground="Yellow")
        self.view_menu.entryconfig("Replace", background="green", foreground="Yellow")
        self.view_menu.entryconfig("Dark Mode", background="green", foreground="Yellow")
        self.view_menu.entryconfig("Light Mode", background="green", foreground="Yellow")
        self.view_menu.delete(2)
        self.view_menu.insert_separator(2, background="green")

        self.customization_menu.entryconfig("Bold", background="green", foreground="Yellow")
        self.customization_menu.entryconfig("Italics", background="green", foreground="Yellow")
        self.customization_menu.entryconfig("Underline", background="green", foreground="Yellow")
        self.customization_menu.entryconfig("Foreground-Color", background="green", foreground="Yellow")
        self.customization_menu.entryconfig("Background-Color", background="green", foreground="Yellow", state=NORMAL)
        self.customization_menu.delete(3)
        self.customization_menu.insert_separator(3, background="green")

    # Header Configuration
    def change_font_size(self, e):
        self.current_font_size = int(e)
        self.main_writing_space['font'] = (self.font_family.get(), self.current_font_size)

    def make_align_left(self):
        try:
            store_selection_start_position = list(self.main_writing_space.index(INSERT))
            checking_if_empty_space_present = list(self.main_writing_space.get(int(store_selection_start_position[0])*1.0, "sel.first"))

            if len(checking_if_empty_space_present) == 0 or checking_if_empty_space_present[0] == '\t' or checking_if_empty_space_present[0] == ' ':
                get_all_text = self.main_writing_space.get("sel.first", "sel.last")
                self.main_writing_space.tag_configure("left", justify=LEFT)
                self.main_writing_space.delete("sel.first", "sel.last")
                self.main_writing_space.insert(int(store_selection_start_position[0]) * 1.0, get_all_text, "left")
            else:
                messagebox.showerror("Not allowed","Not allowed to make selected text left aligned!! text present in left side")
        except:
            messagebox.showerror("Selection Error","Please select a text to make left aligned")

    def make_align_center(self):
        try:
            store = list(self.main_writing_space.index("sel.first"))
            store = int(store[0]) * 1.0
            checking_if_empty_space_present = list(self.main_writing_space.get("sel.last", "current lineend"))

            if len(checking_if_empty_space_present) == 0 or checking_if_empty_space_present[len(checking_if_empty_space_present)-1] == '\t' or checking_if_empty_space_present[len(checking_if_empty_space_present)-1] == ' ':
                get_all_text = self.main_writing_space.get(store, "sel.last")
                self.main_writing_space.tag_configure("middle", justify=CENTER)
                self.main_writing_space.delete(store, "sel.last")
                self.main_writing_space.insert(INSERT, get_all_text, "middle")
            else:
                messagebox.showerror("Not empty","Right side not empty")
        except:
            messagebox.showerror("Selection Error","Nothing selected here")

    def make_align_right(self):
        try:
            store = list(self.main_writing_space.index("sel.first"))
            store = int(store[0]) * 1.0
            checking_if_empty_space_present = list(self.main_writing_space.get("sel.last", "current lineend"))

            if len(checking_if_empty_space_present) == 0 or checking_if_empty_space_present[len(checking_if_empty_space_present) - 1] == '\t' or checking_if_empty_space_present[len(checking_if_empty_space_present) - 1] == ' ':
                get_all_text = self.main_writing_space.get(store, "sel.last")
                self.main_writing_space.tag_configure("right", justify=RIGHT)
                self.main_writing_space.delete(store, "sel.last")
                self.main_writing_space.insert(INSERT, get_all_text, "right")
            else:
                messagebox.showerror("Not empty", "Right side not empty")
        except:
            messagebox.showerror("Selection Error", "Nothing selected here")

    def change_font_manually(self, e):
        try:
            font_change = font.Font(self.main_writing_space, self.main_writing_space.cget("font"))
            font_change.configure(family=self.font_family.get())

            if len(self.font_tag_name_store) == 0:
                temp_store = [self.font_tag_counter, self.main_writing_space.index("sel.first"), self.main_writing_space.index("sel.last")]
                self.font_tag_name_store.append(temp_store)
                temp = self.font_tag_name_store[0][0]
                self.font_tag_counter+=1
            else:
                def search_it():
                    start = self.main_writing_space.index("sel.first")
                    end = self.main_writing_space.index("sel.last")
                    for take in self.font_tag_name_store:
                        if take[1] == start and take[2] == end:
                            temp = take[0]
                            return temp
                    return -1

                temp = search_it()

                if temp == -1:
                    temp_store = [self.font_tag_counter, self.main_writing_space.index("sel.first"), self.main_writing_space.index("sel.last")]
                    self.font_tag_name_store.append(temp_store)
                    temp = self.font_tag_name_store[self.font_tag_counter][0]
                    self.font_tag_counter += 1

            self.main_writing_space.tag_configure(temp, font=font_change)
            self.main_writing_space.tag_add(temp, "sel.first", "sel.last")
        except:
            messagebox.showerror("Selection Error","Select select a text to change font")

    def change_line_space_to_selected_text(self, take):
        try:
            starting_index = int(list(self.main_writing_space.index("sel.first").split("."))[0])

            get_text = self.main_writing_space.get(starting_index * 1.0, "sel.last").split("\n")
            self.main_writing_space.delete(starting_index * 1.0, "sel.last")
            print("Before: ",get_text)

            for modified_element in get_text:
                if modified_element == '':
                    pass
                else:
                    self.main_writing_space.insert(starting_index * 1.0, modified_element)
                    for lines in range(take):
                        self.main_writing_space.insert((starting_index+1) * 1.0, '\n')
                        starting_index += 1

            print("After: ",get_text)
        except:
            messagebox.showerror("Selection Error", "Nothing Selected to change line space")

        if self.permission_to_update == 1:
            self.total_word_and_line_counter(None)

    def add_bullet_in_selected_text(self, bullet_is):
        try:
            if int(self.header_2_components[1].get()) > 1:
                messagebox.showwarning("Restriction", "Bullet add can happen only for line spacing: 1")
                return

            bullet_is = list(bullet_is)[0]
            if bullet_is == '1':
                bullet_is = 1

            starting_index = int(list(self.main_writing_space.index("sel.first").split("."))[0])

            get_text = self.main_writing_space.get(starting_index*1.0, "sel.last").split("\n")
            self.main_writing_space.delete(starting_index*1.0, "sel.last")

            print("Before get_text: ",get_text)

            for element in get_text:
                element_index_finder = get_text.index(element)
                element = list(element)
                print("Element is: ",element)

                while True:
                    print("Element is in loop: ", element)

                    if element:
                        if element[0] == '' or element[0] == ' ' or element[0] == '\t' or element[0] == '\n' or element[0] == '#' or element[0] == '!' or element[0] == '>' or element[0] == 'o' or element[0] == '.':
                            element.remove(element[0])

                        elif len(element) >= 5 and (element[3] == '.' and element[4] == ' '):
                            count_delete = 5
                            while count_delete:
                                element.remove(element[0])
                                count_delete-=1

                        elif len(element) >= 4 and (element[2] == '.' and element[3] == ' '):
                            count_delete = 4
                            while count_delete:
                                element.remove(element[0])
                                count_delete-=1

                        elif len(element) >= 3 and (element[1] == '.' and element[2] == ' '):
                            count_delete = 3
                            while count_delete:
                                element.remove(element[0])
                                count_delete-=1
                        else:
                            break

                    else:
                        break

                element = "".join(element)

                if type(bullet_is) == int:
                    element=f"{bullet_is}. {element}"
                else:
                    element = f"{bullet_is} {element}"
                if element_index_finder < len(get_text)-1:
                    element+='\n'

                get_text[element_index_finder] = element

                if type(bullet_is) == int:
                    bullet_is+=1
            print(get_text)

            for modified_element in get_text:
                self.main_writing_space.insert(starting_index*1.0,modified_element)
                starting_index+=1

            print(get_text)
        except:
            messagebox.showerror("Selection Error", "Nothing Selected to make bullet before it")

        if self.permission_to_update == 1:
            self.total_word_and_line_counter(None)

    def total_word_and_line_counter(self, e = None):
        total_take = list(self.main_writing_space.get(1.0, END).split("\n"))

        self.total_line = len(total_take)-1
        self.status_components[1]['text'] = "Total Line: " + str(len(total_take)-1)

        count = 0
        for element in total_take:
            temp=list(element)
            if temp and (temp[0] == "#" or temp[0] == ">" or temp[0] == "o" or temp[0] == "" or temp[0] == "!"):
                temp.remove(temp[0])

            if temp.count('\t')>0:
                temp[temp.index('\t')] = " "
                while temp.count('\t')>0:
                    temp.remove('\t')

            while temp.count('.')>0:
                index = temp.index('.')
                if (index+1<len(temp) and temp[index+1] == ' ') and (index-1>=0):
                    temp.remove(temp[index])
                else:
                    break

            element="".join(temp)
            store = list(element.split(" "))

            while store.count('')>0:
                store.remove('')

            count += len(store)

        self.total_word = count
        self.status_components[0]['text'] = "Total Word: " + str(count)

    def __time_counter(self):
        self.get_time+=1
        if self.get_time>-1:
            self.status_components[2].after(1000, self.__time_counter)  # Recursive function call after 1 sec
            converted_time = time.strftime("%H:%M:%S", time.gmtime(self.get_time))
            self.status_components[2]['text'] = f"Working Time: {converted_time}"
        else:
            self.status_components[2]['text'] = "Working Time: 00:00:00"


if __name__ == '__main__':
    window = Tk()
    window.geometry("1350x715")
    window.maxsize(1350, 715)
    window.minsize(500, 500)
    window.config(bg="black")
    TextPad(window)
    window.mainloop()