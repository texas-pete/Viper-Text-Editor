import tkinter as tk
from tkinter import *
from tkinter import Tk, ttk, Text, Scrollbar, Menu, messagebox, filedialog, Frame, PhotoImage, simpledialog, Button
import os, subprocess, json, string
from hashlib import md5
import pyttsx3




current_font = "arial"
current_size = 12


class Document:
    def __init__(self, Frame, TextWidget, FileDir=''):
        self.file_dir = FileDir
        self.file_name = 'Untitled' if not FileDir else os.path.basename(FileDir)
        self.text = TextWidget
        #self.text = CustomText(self)
        #self.custom_text = CustomText(self.text)
        self.status = md5(self.text.get(1.0, 'end').encode('utf-8'))


class TextWindow(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.master.title("Notepad+=1")
        #tk.Frame__init__(self, *args, *kwargs)
        self.frame = tk.Frame(self.master, *args, **kwargs)
        self.frame.pack()


        self.filetypes = (("Normal text file", "*.txt"), ("all files", "*.*"))
        self.init_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

        self.tabs = {}  # { index, text widget }

        # Create Notebook ( for tabs ).
        self.tabControl = ttk.Notebook(master)
        self.tabControl.bind("<Button-2>", self.close_tab)
        self.tabControl.bind("<B1-Motion>", self.move_tab)
        self.tabControl.pack(expand=1, fill="both")
        self.tabControl.enable_traversal()
        # self.tabControl.bind('<<NotebookTabChanged>>', self.tab_change)

        # Override the X button.
        self.master.protocol('WM_DELETE_WINDOW', self.exit)

        # Create Menu Bar
        menu_bar = tk.Menu(self.master)

        # Create File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_as)
        file_menu.add_command(label="Close", command=self.close_tab)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit)

        # Create Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_command(label="Delete", command=self.delete)
        edit_menu.add_command(label="Select All", command=self.select_all)

        # Create Format Menu, with a check button for word wrap.
        format_menu = tk.Menu(menu_bar, tearoff=0)
        self.word_wrap = tk.BooleanVar()
        format_menu.add_checkbutton(label="Word Wrap", onvalue=True, offvalue=False, variable=self.word_wrap,
                                   command=self.wrap)

        # Format menu
        font_type_menu = tk.Menu(format_menu)
        format_menu.add_cascade(label="Font Type", underline=1, menu=font_type_menu)
        font_type_menu.add_command(label="Helvetica", command=self.font_helvetica)
        font_type_menu.add_command(label="Courier New", command=self.font_courier)
        font_type_menu.add_command(label="Times New Roman", command=self.font_times)
        font_type_menu.add_command(label="Cambria", command=self.font_cambria)
        font_type_menu.add_command(label="Calibri", command=self.font_calibri)
        font_type_menu.add_command(label="Verdana", command=self.font_verdana)
        font_type_menu.add_command(label="Papyrus", command=self.font_papyrus)
        font_type_menu.add_command(label="Century Gothic", command=self.font_gothic)
        font_type_menu.add_command(label="Rockwell Nova", command=self.font_rockwell)
        font_type_menu.add_command(label="Corbel", command=self.font_corbel)
        font_type_menu.add_command(label="Georgia", command=self.font_georgia)

        font_color_menu = tk.Menu(format_menu)
        format_menu.add_cascade(label="Font Color", underline=1, menu=font_color_menu)
        font_color_menu.add_command(label="Black", command=self.color_black)
        font_color_menu.add_command(label="White", command=self.color_white)
        font_color_menu.add_command(label="Red", command=self.color_red)
        font_color_menu.add_command(label="Orange", command=self.color_orange)
        font_color_menu.add_command(label="Yellow", command=self.color_yellow)
        font_color_menu.add_command(label="Green", command=self.color_green)
        font_color_menu.add_command(label="Blue", command=self.color_blue)
        font_color_menu.add_command(label="Purple", command=self.color_purple)

        font_size_menu = tk.Menu(format_menu)
        format_menu.add_cascade(label="Font Size", underline=1, menu=font_size_menu)
        font_size_menu.add_command(label="8", command=self.size8)
        font_size_menu.add_command(label="9", command=self.size9)
        font_size_menu.add_command(label="10", command=self.size10)
        font_size_menu.add_command(label="11", command=self.size11)
        font_size_menu.add_command(label="12", command=self.size12)
        font_size_menu.add_command(label="14", command=self.size14)
        font_size_menu.add_command(label="16", command=self.size16)
        font_size_menu.add_command(label="18", command=self.size18)
        font_size_menu.add_command(label="20", command=self.size20)
        font_size_menu.add_command(label="22", command=self.size22)
        font_size_menu.add_command(label="24", command=self.size24)
        font_size_menu.add_command(label="26", command=self.size26)
        font_size_menu.add_command(label="28", command=self.size28)
        font_size_menu.add_command(label="36", command=self.size36)
        font_size_menu.add_command(label="48", command=self.size48)
        font_size_menu.add_command(label="72", command=self.size72)

        theme_menu = tk.Menu(format_menu)
        format_menu.add_cascade(label="Themes", underline=1, menu=theme_menu)
        theme_menu.add_command(label="Day Mode", command=self.theme_day)
        theme_menu.add_command(label="Dark Mode", command=self.theme_dark)

        # Debug menu
        debug_menu = tk.Menu(menu_bar, tearoff=0)
        debug_menu.add_command(label="Debug", underline=1)

        # Help menu
        help_menu = Menu(menu_bar, tearoff=0, )
        help_menu.add_command(label="Help", underline=1, command=self.help_pop)
        help_menu.add_command(label="About", underline=1, command=self.about_pop)

        # Attach to Menu Bar
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        menu_bar.add_cascade(label="Format", underline=1, menu=format_menu)
        menu_bar.add_cascade(label="Debug", underline=1)
        menu_bar.add_cascade(label="Help", underline=1, menu=help_menu)


        self.master.config(menu=menu_bar)

        # Create right-click menu.
        self.right_click_menu = tk.Menu(self.master, tearoff=0)
        self.right_click_menu.add_command(label="Undo", command=self.undo)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Cut", command=self.cut)
        self.right_click_menu.add_command(label="Copy", command=self.copy)
        self.right_click_menu.add_command(label="Paste", command=self.paste)
        self.right_click_menu.add_command(label="Delete", command=self.delete)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Select All", command=self.select_all)

        # Create tab right-click menu
        self.tab_right_click_menu = tk.Menu(self.master, tearoff=0)
        self.tab_right_click_menu.add_command(label="New Tab", command=self.new_file)
        self.tabControl.bind('<Button-3>', self.right_click_tab)

        # Create Initial Tab
        first_tab = ttk.Frame(self.tabControl)
        self.tabs[first_tab] = Document(first_tab, self.create_text_widget(first_tab))
        self.tabControl.add(first_tab, text='Untitled')

        #self.linenumbers = TextLineNumbers(self, width=30)
        #self.linenumbers.attach(self.custom_text)
        #self.linenumbers.pack(side="left", fill="y")

        self._highlight_current_line()
        #self.tabs[self.get_tab()].text.bind('<Up>', self.get_whitespace)
        #self.tabs[self.get_tab()].text.bind('<Down>', self.get_whitespace)
        #self.tabs[self.get_tab()].text.bind('<Return>', self.get_whitespace)
        self.master.bind('<Alt-w>', self.leftclick)
        # if (#args[0] in ("insert", "replace", "delete") or
        #         #args[0:3] == ("mark", "set", "insert") or
        #         args[0:2] == ("yview", "moveto")
        # ):
        #     self.event_generate("<<CursorChange>>", when="tail")
        #     #self.get_whitespace()
        #
        # self.tabs[self.get_tab()].text.bind("<<CursorChange>>", self.get_whitespace())

    def create_text_widget(self, frame, *args, **kwargs):
        # Horizontal Scroll Bar
        xscrollbar = tk.Scrollbar(frame, orient='horizontal')
        xscrollbar.pack(side='bottom', fill='x')

        # Vertical Scroll Bar
        yscrollbar = tk.Scrollbar(frame)
        yscrollbar.pack(side='right', fill='y')

        # Create Text Editor Box
        text = tk.Text(frame, relief='sunken', borderwidth=0, wrap='none')
        text.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, undo=True, autoseparators=True)
        text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        text.tag_configure("current_line", background="#e9e9e9")

        # Keyboard / Click Bindings
        text.bind('<Control-s>', self.save_file)
        text.bind('<Control-o>', self.open_file)
        text.bind('<Control-n>', self.new_file)
        text.bind('<Control-a>', self.select_all)
        text.bind('<Control-w>', self.close_tab)
        text.bind('<Button-3>', self.right_click)

        # Pack the text
        text.pack(fill='both', expand=True)

        # Configure Scrollbars
        xscrollbar.config(command=text.xview)
        yscrollbar.config(command=text.yview)

        # self.linenumbers = TextLineNumbers(self, width=30)
        # self.linenumbers.attach(self.text)
        # self.linenumbers.pack(side="left", fill="y")
        #text.bind("<<CursorChange>>", self.get_whitespace())

        # if (#args[0] in ("insert", "replace", "delete") or
        #         #args[0:3] == ("mark", "set", "insert") or
        #         args[0:2] == ("yview", "moveto")
        # ):
        #     self.event_generate("<<CursorChange>>", when="tail")
        #     #self.get_whitespace()
        #
        # text.bind("<<CursorChange>>", self.get_whitespace())

        return text

    def open_file(self, *args):
        # Open a window to browse to the file you would like to open, returns the directory.
        file_dir = (tkinter
                    .filedialog
                    .askopenfilename(initialdir=self.init_dir, title="Select file", filetypes=self.filetypes))

        # If directory is not the empty string, try to open the file.
        if file_dir:
            try:
                # Open the file.
                file = open(file_dir)

                # Create a new tab.
                new_tab = ttk.Frame(self.tabControl)
                self.tabs[new_tab] = Document(new_tab, self.create_text_widget(new_tab), file_dir)
                self.tabControl.add(new_tab, text=os.path.basename(file_dir))
                self.tabControl.select(new_tab)

                # Puts the contents of the file into the text widget.
                self.tabs[new_tab].text.insert('end', file.read())

                # Update hash
                self.tabs[new_tab].status = md5(tabs[new_tab].text.get(1.0, 'end').encode('utf-8'))
            except:
                return

    def save_as(self):
        curr_tab = self.get_tab()

        # Gets file directory and name of file to save.
        file_dir = (tkinter
                    .filedialog
                    .asksaveasfilename(initialdir=self.init_dir, title="Select file", filetypes=self.filetypes,
                                       defaultextension='.txt'))

        # Return if directory is still empty (user closes window without specifying file name).
        if not file_dir:
            return

        # Adds .txt suffix if not already included.
        if file_dir[-4:] != '.txt':
            file_dir += '.txt'

        self.tabs[curr_tab].file_dir = file_dir
        self.tabs[curr_tab].file_name = os.path.basename(file_dir)
        self.tabControl.tab(curr_tab, text=self.tabs[curr_tab].file_name)

        # Writes text widget's contents to file.
        file = open(file_dir, 'w')
        file.write(self.tabs[curr_tab].text.get(1.0, 'end'))
        file.close()

        # Update hash
        self.tabs[curr_tab].status = md5(self.tabs[curr_tab].text.get(1.0, 'end').encode('utf-8'))

    def save_file(self, *args):
        curr_tab = self.get_tab()

        # If file directory is empty or Untitled, use save_as to get save information from user.
        if not self.tabs[curr_tab].file_dir:
            self.save_as()

        # Otherwise save file to directory, overwriting existing file or creating a new one.
        else:
            with open(self.tabs[curr_tab].file_dir, 'w') as file:
                file.write(self.tabs[curr_tab].text.get(1.0, 'end'))

            # Update hash
            self.tabs[curr_tab].status = md5(self.tabs[curr_tab].text.get(1.0, 'end').encode('utf-8'))

    def new_file(self, *args):
        # Create new tab
        new_tab = ttk.Frame(self.tabControl)
        self.tabs[new_tab] = Document(new_tab, self.create_text_widget(new_tab))
        self.tabs[new_tab].text.config(wrap='word' if self.word_wrap.get() else 'none')
        self.tabControl.add(new_tab, text='Untitled')
        self.tabControl.select(new_tab)

    def copy(self):
        # Clears the clipboard, copies selected contents.
        try:
            sel = self.tabs[self.get_tab()].text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.master.clipboard_clear()
            self.master.clipboard_append(sel)
        # If no text is selected.
        except tk.TclError:
            pass

    def delete(self):
        # Delete the selected text.
        try:
            self.tabs[self.get_tab()].text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        # If no text is selected.
        except tk.TclError:
            pass

    def cut(self):
        # Copies selection to the clipboard, then deletes selection.
        try:
            sel = self.tabs[self.get_tab()].text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.master.clipboard_clear()
            self.master.clipboard_append(sel)
            self.tabs[self.get_tab()].text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        # If no text is selected.
        except tk.TclError:
            pass

    ##########################################################
    #FORMAT MENU FUNCTIONS
    def font_helvetica(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Helvetica", current_size))
        global current_font
        current_font = "Helvetica"
    def font_courier(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Courier", current_size))
        global current_font
        current_font = "Courier"
    def font_times(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Times", current_size))
        global current_font
        current_font = "Times"
    def font_cambria(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Cambria", current_size))
        global current_font
        current_font = "Cambria"
    def font_calibri(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Calibri", current_size))
        global current_font
        current_font = "Calibri"
    def font_verdana(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Verdana", current_size))
        global current_font
        current_font = "Verdana"
    def font_papyrus(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Papyrus", current_size))
        global current_font
        current_font = "Papyrus"
    def font_gothic(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Gothic", current_size))
        global current_font
        current_font = "Gothic"
    def font_rockwell(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Rockwell", current_size))
        global current_font
        current_font = "Rockwell"
    def font_corbel(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Corbel", current_size))
        global current_font
        current_font = "Corbel"
    def font_georgia(self, event=None):
        self.tabs[self.get_tab()].text.config(font=("Georgia", current_size))
        global current_font
        current_font = "Georgia"

    def color_black(self, event=None):
        self.tabs[self.get_tab()].text.config(fg="black")
    def color_white(self, event=None):
        self.tabs[self.get_tab()].text.config(fg="white")
    def color_red(self, event=None):
        self.tabs[self.get_tab()].text.config(fg="red")
    def color_orange(self, event=None):
        self.tabs[self.get_tab()].text.config(fg="orange")
    def color_yellow(self, event=None):
        self.tabs[self.get_tab()].text.config(fg="yellow")
    def color_green(self, event=None):
        self.tabs[self.get_tab()].text.config(fg="green")
    def color_blue(self, event=None):
        self.tabs[self.get_tab()].text.config(fg="blue")
    def color_purple(self, event=None):
        self.tabs[self.get_tab()].text.config(fg="purple")

    def size8(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 8))
        current_size = 8
    def size9(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 9))
        current_size = 9
    def size10(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 10))
        current_size = 10
    def size11(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 11))
        current_size = 11
    def size12(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 12))
        current_size = 12
    def size14(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 14))
        current_size = 14
    def size16(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 16))
        current_size = 16
    def size18(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 18))
        current_size = 18
    def size20(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 20))
        current_size = 20
    def size22(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 22))
        current_size = 22
    def size24(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 24))
        current_size = 24
    def size26(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 26))
        current_size = 26
    def size28(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 28))
        current_size = 28
    def size36(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 36))
        current_size = 36
    def size48(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 48))
        current_size = 48
    def size72(self, event=None):
        global current_font, current_size
        self.tabs[self.get_tab()].text.config(font=(current_font, 72))
        current_size = 72

    def theme_day(self, event=None):
        self.tabs[self.get_tab()].text.config(background="White")
    def theme_dark(self, event=None):
        self.tabs[self.get_tab()].text.config(background="Black")
    ##########################################################

    def wrap(self):
        if self.word_wrap.get() == True:
            for index in self.tabs:
                self.tabs[index].text.config(wrap="word")
        else:
            for index in self.tabs:
                self.tabs[index].text.config(wrap="none")

    def _highlight_current_line(self, interval=100):
        '''Updates the 'current line' highlighting every "interval" milliseconds'''
        self.tabs[self.get_tab()].text.tag_remove("current_line", 1.0, "end")
        self.tabs[self.get_tab()].text.tag_add("current_line", "insert linestart", "insert lineend+1c")
        self.tabs[self.get_tab()].text.after(interval, self._highlight_current_line)

    # def key_listen(self, interval=100, *args, **kwargs):
    #     if (#args[0] in ("insert", "replace", "delete") or
    #             #args[0:3] == ("mark", "set", "insert") or
    #             args[2:3] == ("yview", "moveto")
    #     ):
    #         self.event_generate("<<CursorChange>>", when="tail")
    #         #self.get_whitespace()
    #
    #     self.tabs[self.get_tab()].text.bind("<<CursorChange>>", self.get_whitespace())
    #     self.tabs[self.get_tab()].text.after(interval, self.key_listen)

    def get_whitespace(self):
        line_text = self.tabs[self.get_tab()].text.get("insert linestart", "insert lineend")
        print(line_text)
        count = 0
        for i in line_text:
            if i==" ":
                count = count + 1
            elif i=="\t":
                count = count + 8
            else:
                break
        print(count)
        engine = pyttsx3.init()
        engine.say("White space is " + str(count))
        engine.say(line_text)
        engine.runAndWait()
        engine.stop()

    def leftclick(self, event):
        self.get_whitespace()

    def help_pop(self, event=None):
        messagebox.showinfo("Help","Hotkeys:\n\n Ctrl O: Open file \n\n Ctrl S: Save file \n\n Ctrl Y: Redo \n\n Ctrl Z: Undo \n\n Ctrl W: Say Whitespace")

    def about_pop(self, event=None):
        messagebox.showinfo("About us","Team name: Bits and Pieces \n\n Members: \n Daniel Merlino \n Jose Duarte \n Stephen Lederer \n Travis Pete")


    def paste(self):
        try:
            self.tabs[self.get_tab()].text.insert(tk.INSERT, self.master.clipboard_get())
        except tk.TclError:
            pass

    def select_all(self, *args):
        curr_tab = self.get_tab()

        # Selects / highlights all the text.
        self.tabs[curr_tab].text.tag_add(tk.SEL, "1.0", tk.END)

        # Set mark position to the end and scroll to the end of selection.
        self.tabs[curr_tab].text.mark_set(tk.INSERT, tk.END)
        self.tabs[curr_tab].text.see(tk.INSERT)

    def undo(self):
        self.tabs[self.get_tab()].text.edit_undo()

    def right_click(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)

    def right_click_tab(self, event):
        self.tab_right_click_menu.post(event.x_root, event.y_root)

    def close_tab(self, event=None):
        # Make sure there is at least one tab still open.
        if self.tabControl.index("end") > 1:
            # Close the current tab if close is selected from file menu, or keyboard shortcut.
            if event is None or event.type == str(2):
                selected_tab = self.get_tab()
            # Otherwise close the tab based on coordinates of center-click.
            else:
                try:
                    index = event.widget.index('@%d,%d' % (event.x, event.y))
                    selected_tab = self.tabControl._nametowidget(self.tabControl.tabs()[index])
                except tk.TclError:
                    return

            self.tabControl.forget(selected_tab)
            self.tabs.pop(selected_tab)

    def exit(self):
        # Check if any changes have been made.
        if self.save_changes():
            self.master.destroy()
        else:
            return

    def save_changes(self):
        curr_tab = self.get_tab()
        file_dir = self.tabs[curr_tab].file_dir

        # Check if any changes have been made, returns False if user chooses to cancel rather than select to save or not.
        if md5(self.tabs[curr_tab].text.get(1.0, 'end').encode('utf-8')).digest() != self.tabs[
            curr_tab].status.digest():
            # If changes were made since last save, ask if user wants to save.
            m = messagebox.askyesnocancel('Editor', 'Do you want to save changes to ' + (
                'Untitled' if not file_dir else file_dir) + '?')

            # If None, cancel.
            if m is None:
                return False
            # else if True, save.
            elif m is True:
                self.save_file()
            # else don't save.
            else:
                pass

        return True

    # Get the object of the current tab.
    def get_tab(self):
        return self.tabControl._nametowidget(self.tabControl.select())

    def move_tab(self, event):
        '''
        Check if there is more than one tab.

        Use the y-coordinate of the current tab so that if the user moves the mouse up / down
        out of the range of the tabs, the left / right movement still moves the tab.
        '''
        if self.tabControl.index("end") > 1:
            y = self.get_tab().winfo_y() - 5

            try:
                self.tabControl.insert(event.widget.index('@%d,%d' % (event.x, y)), self.tabControl.select())
            except tk.TclError:
                return

    def _on_change(self, event):
        self.linenumbers.redraw()


# class TextLineNumbers(tk.Canvas):
#     def __init__(self, *args, **kwargs):
#         super(TextLineNumbers, self).tk.Canvas.__init__(self, *args, **kwargs)
#         self.__line_numbers = None
#
#     def attach(self, __line_numbers):
#         self.__line_numbers = __line_numbers
#
#     def redraw(self, *args):
#         # Re-draw line numbers
#         self.delete("all")
#
#         i = self.__line_numbers.index("@0,0")
#         while True:
#             dline = self.__line_numbers.dlineinfo(i)
#             if dline is None: break
#             y = dline[1]
#             line_num = str(i).split(".")[0]
#             self.create_text(2, y, anchor="nw", text=line_num)
#             i = self.__line_numbers.index("%s+1line" % i)
#
#         self.after(30, self.redraw)



# class CustomText(tk.Text):
#     def __init__(self, *args, **kwargs):
#         tk.Text.__init__(self, *args, **kwargs)
#
#         #create a proxy for the underlying widget
#         self._orig = self._w + "_orig"
#         self.tk.call("rename", self._w, self._orig)
#         self.tk.createcommand(self._w, self._proxy)
#
#         def _proxy(self, *args):
#             # let the actual widget perform the requested action
#             cmd = (self._orig,) + args
#             result = self.tk.call(cmd)
#
#             # generate an event if something was added or deleted,
#             # or the cursor position changed
#             if (args[0] in ("insert", "replace", "delete") or
#                     args[0:3] == ("mark", "set", "insert") or
#                     args[0:2] == ("xview", "moveto") or
#                     args[0:2] == ("xview", "scroll") or
#                     args[0:2] == ("yview", "moveto") or
#                     args[0:2] == ("yview", "scroll")
#             ):
#                 self.event_generate("<<Change>>", when="tail")
#
#             # return what the actual widget returned
#             return result

#def main():
#    root = tk.Tk()
#    app = TextWindow(root)
#    root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = TextWindow(root)
    root.wm_state('normal')
    #text = TextWindow(root).pack(side="top", fill="both", expand=True)
    image = PhotoImage(file="viper.png")
    root.tk.call('wm', 'iconphoto', root._w, image)
    root.mainloop()
