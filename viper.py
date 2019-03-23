import tkinter as tk
from tkinter import *
from tkinter import Tk, ttk, Text, Scrollbar, Menu, messagebox, filedialog, Frame, PhotoImage
import os, subprocess, json, string

current_font = "arial"
current_size = 12

class TextWindow(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.TITLE = "Viper"
        self.file_path = None
        tk.Frame.__init__(self, *args, **kwargs)
        self.set_title()
        self.tabControl = ttk.Notebook(root)

        # Frame for the Text Window
        frame = Frame(root)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.text.tag_configure("current_line", background="#e9e9e9")
        self._highlight_current_line()
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)
        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        self.tabControl.pack(anchor='nw', expand=1, fill="both")



        # Bindings and Hot Key Bindings
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        # Closes the application
        root.protocol("WM_DELETE_WINDOW", self.file_quit)

        # Create a top level menu
        self.menu_bar = Menu(root)

        # File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New File", underline=1, command=self.file_new, accelerator="Ctrl+N")
        file_menu.add_command(label="Open File", underline=1, command=self.file_open, accelerator="Ctrl+O")
        file_menu.add_command(label="Open Project", underline=1, command=self.project_open)
        file_menu.add_command(label="Save File", underline=1, command=self.file_save, accelerator="Ctrl+S")
        file_menu.add_command(label="Save File As...", underline=5, command=self.file_save_as, accelerator="Ctrl+Alt+S")
        file_menu.add_command(label="Save Project", underline=1, command=self.project_save)
        file_menu.add_separator()
        file_menu.add_command(label="Close Current Tab", underline=1, command=self.close_tab)
        file_menu.add_command(label="Exit", underline=2, command=self.file_quit, accelerator="Alt+F4")
        self.menu_bar.add_cascade(label="File", underline=0, menu=file_menu)

        # Edit menu
        edit_menu = Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", underline=1, command=self.undo, accelerator="Ctrl+z")
        edit_menu.add_command(label="Redo", underline=1, command=self.redo, accelerator="Ctrl+y")
        self.menu_bar.add_cascade(label="Edit", underline=0, menu=edit_menu)

        # Format menu
        format_menu = Menu(self.menu_bar, tearoff=0)
        font_type_menu = Menu(format_menu)
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

        font_color_menu = Menu(format_menu)
        format_menu.add_cascade(label="Font Color", underline=1, menu=font_color_menu)
        font_color_menu.add_command(label="Black", command=self.color_black)
        font_color_menu.add_command(label="White", command=self.color_white)
        font_color_menu.add_command(label="Red", command=self.color_red)
        font_color_menu.add_command(label="Orange", command=self.color_orange)
        font_color_menu.add_command(label="Yellow", command=self.color_yellow)
        font_color_menu.add_command(label="Green", command=self.color_green)
        font_color_menu.add_command(label="Blue", command=self.color_blue)
        font_color_menu.add_command(label="Purple", command=self.color_purple)

        font_size_menu = Menu(format_menu)
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

        theme_menu = Menu(format_menu)
        format_menu.add_cascade(label="Themes", underline=1, menu=theme_menu)
        theme_menu.add_command(label="Day Mode", command=self.theme_day)
        theme_menu.add_command(label="Dark Mode", command=self.theme_dark)

        self.menu_bar.add_cascade(label="Format", underline=1, menu=format_menu)

        # Debug menu
        debug_menu = Menu(self.menu_bar, tearoff=0)
        debug_menu.add_command(label="Debug", underline=1)
        self.menu_bar.add_cascade(label="Debug", underline=1)

        # Go To menu
        go_to_menu = Menu(self.menu_bar, tearoff=0)
        go_to_menu.add_command(label="Go To", underline=1)
        self.menu_bar.add_cascade(label="Go To", underline=1)

        # Help menu
        help_menu = Menu(self.menu_bar, tearoff=0, )
        help_menu.add_command(label="Help", underline=1, command=self.help_pop)
        help_menu.add_command(label="About", underline=1, command=self.about_pop)
        self.menu_bar.add_cascade(label="Help", underline=1, menu=help_menu)

        # Display the menu
        root.config(menu=self.menu_bar)

    def help_pop(self, event=None):
        messagebox.showinfo("Help","Hotkeys:\n\n Ctrl O: Open file \n\n Ctrl S: Save file \n\n Ctrl Y: Redo \n\n Ctrl Z: Undo ")

    def about_pop(self, event=None):
        messagebox.showinfo("About us","Team name: Bits and Pieces \n\n Members: \n Daniel Merlino \n Jose Duarte \n Stephen Lederer \n Travis Pete")

    def font_helvetica(self, event=None):
        self.text.config(font=("Helvetica", current_size))
        global current_font
        current_font = "Helvetica"
    def font_courier(self, event=None):
        self.text.config(font=("Courier", current_size))
        global current_font
        current_font = "Courier"
    def font_times(self, event=None):
        self.text.config(font=("Times", current_size))
        global current_font
        current_font = "Times"
    def font_cambria(self, event=None):
        self.text.config(font=("Cambria", current_size))
        global current_font
        current_font = "Cambria"
    def font_calibri(self, event=None):
        self.text.config(font=("Calibri", current_size))
        global current_font
        current_font = "Calibri"
    def font_verdana(self, event=None):
        self.text.config(font=("Verdana", current_size))
        global current_font
        current_font = "Verdana"
    def font_papyrus(self, event=None):
        self.text.config(font=("Papyrus", current_size))
        global current_font
        current_font = "Papyrus"
    def font_gothic(self, event=None):
        self.text.config(font=("Gothic", current_size))
        global current_font
        current_font = "Gothic"
    def font_rockwell(self, event=None):
        self.text.config(font=("Rockwell", current_size))
        global current_font
        current_font = "Rockwell"
    def font_corbel(self, event=None):
        self.text.config(font=("Corbel", current_size))
        global current_font
        current_font = "Corbel"
    def font_georgia(self, event=None):
        self.text.config(font=("Georgia", current_size))
        global current_font
        current_font = "Georgia"

    def color_black(self, event=None):
        self.text.config(fg="black")
    def color_white(self, event=None):
        self.text.config(fg="white")
    def color_red(self, event=None):
        self.text.config(fg="red")
    def color_orange(self, event=None):
        self.text.config(fg="orange")
    def color_yellow(self, event=None):
        self.text.config(fg="yellow")
    def color_green(self, event=None):
        self.text.config(fg="green")
    def color_blue(self, event=None):
        self.text.config(fg="blue")
    def color_purple(self, event=None):
        self.text.config(fg="purple")

    def size8(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 8))
        current_size = 8
    def size9(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 9))
        current_size = 9
    def size10(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 10))
        current_size = 10
    def size11(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 11))
        current_size = 11
    def size12(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 12))
        current_size = 12
    def size14(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 14))
        current_size = 14
    def size16(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 16))
        current_size = 16
    def size18(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 18))
        current_size = 18
    def size20(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 20))
        current_size = 20
    def size22(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 22))
        current_size = 22
    def size24(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 24))
        current_size = 24
    def size26(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 26))
        current_size = 26
    def size28(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 28))
        current_size = 28
    def size36(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 36))
        current_size = 36
    def size48(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 48))
        current_size = 48
    def size72(self, event=None):
        global current_font, current_size
        self.text.config(font=(current_font, 72))
        current_size = 72

    def theme_day(self, event=None):
        self.text.config(background="White")
    def theme_dark(self, event=None):
        self.text.config(background="Black")

    def _highlight_current_line(self, interval=100):
        '''Updates the 'current line' highlighting every "interval" milliseconds'''
        self.text.tag_remove("current_line", 1.0, "end")
        self.text.tag_add("current_line", "insert linestart", "insert lineend+1c")
        self.root.after(interval, self._highlight_current_line)

    def save_if_modified(self, event=None):
        if self.text.edit_modified():
            response = messagebox.askyesnocancel("Save?",
                                                 "This document has been modified. Do you want to save changes?")
            if response:  # yes/save
                result = self.file_save()
                if result == "saved":
                    return True
                # Save cancelled
                else:
                    return None
            else:
                return response
                # Not modified
        else:
            return True

    def file_new(self, event=None):
        result = self.save_if_modified()
        # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
        if result != None:
            self.text.delete(1.0, "end")
            self.text.edit_modified(False)
            self.text.edit_reset()
            self.file_path = None
            self.set_title()
            tab1 = ttk.Frame(self.tabControl)  # Create a tab
            self.tabControl.add(tab1, text='New Tab')  # Add the tab
            return tab1


    def file_open(self, event=None, file_path=None):
        result = self.save_if_modified()
        # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
        if result != None:
            if file_path == None:
                file_path = filedialog.askopenfilename()
            if file_path != None and file_path != '':
                with open(file_path, encoding="utf-8") as file:
                    fileContents = file.read()
                # Set current text to file contents
                self.text.delete(1.0, "end")
                self.text.insert(1.0, fileContents)
                self.text.edit_modified(False)
                self.file_path = file_path

    def project_open(self, event=None, file_path=None):
        result = self.save_if_modified()
        # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
        if result != None:
            if file_path == None:
                file_path = filedialog.askopenfilename()
            if file_path != None and file_path != '':
                with open(file_path, encoding="utf-8") as file:
                    fileContents = file.read()
                # Set current text to file contents
                self.text.delete(1.0, "end")
                self.text.insert(1.0, fileContents)
                self.text.edit_modified(False)
                self.file_path = file_path

    def file_save(self, event=None):
        if self.file_path == None:
            result = self.file_save_as()
        else:
            result = self.file_save_as(file_path=self.file_path)
        return result

    def project_save(self, event=None):
        if self.file_path == None:
            result = self.file_save_as()
        else:
            result = self.file_save_as(file_path=self.file_path)
        return result

    def file_save_as(self, event=None, file_path=None):
        if file_path == None:
            file_path = filedialog.asksaveasfilename(filetypes=(
            ('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*')))  # defaultextension='.txt'
        try:
            with open(file_path, 'wb') as file:
                text = self.text.get(1.0, "end-1c")
                file.write(bytes(text, 'UTF-8'))
                self.text.edit_modified(False)
                self.file_path = file_path
                self.set_title()
                return "saved"
        except FileNotFoundError:
            print('FileNotFoundError')
            return "cancelled"

    def file_quit(self, event=None):
        result = self.save_if_modified()
        # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
        if result != None:
            self.root.destroy()

    def set_title(self, event=None):
        if self.file_path != None:
            title = os.path.basename(self.file_path)
        else:
            title = "Untitled"
        self.root.title(title + " - " + self.TITLE)

    def undo(self, event=None):
        try:
            self.text.edit_undo()
        except:
            print("There is nothing to undo...")

    def redo(self, event=None):
        try:
            self.text.edit_redo()
        except:
            print("There is nothing to redo...")

    def close_tab(self):
        self.tabControl.destroy()

            # def main(self, event=None):
        # self.text.bind("<Control-o>", self.file_open)
        # self.text.bind("<Control-O>", self.file_open)
        # self.text.bind("<Control-S>", self.file_save)
        # self.text.bind("<Control-s>", self.file_save)
        # self.text.bind("<Control-y>", self.redo)
        # self.text.bind("<Control-Y>", self.redo)
        # self.text.bind("<Control-Z>", self.undo)
        # self.text.bind("<Control-z>", self.undo)

    def _on_change(self, event):
        self.linenumbers.redraw()


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.__line_numbers = None

    def attach(self, __line_numbers):
        self.__line_numbers = __line_numbers

    def redraw(self, *args):
        # Re-draw line numbers
        self.delete("all")

        i = self.__line_numbers.index("@0,0")
        while True:
            dline = self.__line_numbers.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            line_num = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=line_num)
            i = self.__line_numbers.index("%s+1line" % i)


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_state('normal')
    text = TextWindow(root).pack(side="top", fill="both", expand=True)
    # text.main()
    image = PhotoImage(file="viper.png")
    root.tk.call('wm', 'iconphoto', root._w, image)
    #text = Text(root)
    root.mainloop()