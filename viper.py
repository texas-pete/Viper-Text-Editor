from tkinter import Tk, Text, Scrollbar, Menu, messagebox, filedialog, Frame, PhotoImage
import os, subprocess, json, string

current_font = "arial"
current_size = 12

class TextWindow():
    def __init__(self, root):
        self.root = root
        self.TITLE = "Viper"
        self.file_path = None
        self.set_title()

        frame = Frame(root)
        self.y_scroll_bar = Scrollbar(frame, orient="vertical")
        self.editor = Text(frame, yscrollcommand=self.y_scroll_bar.set)
        self.editor.pack(side="left", fill="both", expand=1)
        self.editor.tag_configure("current_line", background="#e9e9e9")

        self.editor.config( wrap = "word", undo = True, width = 80 )        
        self.editor.focus()
        self._highlight_current_line()
        self.y_scroll_bar.pack(side="right", fill="y")
        self.y_scroll_bar.config(command=self.editor.yview)

        frame.pack(fill="both", expand=1)
        #text = Text(root)
        #text.grid()

        root.protocol("WM_DELETE_WINDOW", self.file_quit)

        # Create a top level menu
        self.menu_bar = Menu(root)

        # File menu 
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", underline=1, command=self.file_new, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", underline=1, command=self.file_open, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", underline=1, command=self.file_save, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", underline=5, command=self.file_save_as, accelerator="Ctrl+Alt+S")
        file_menu.add_separator()
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

        #for name in ("Red", "Blue", "Green"):
        #    font_color_menu.add_command(label=name, command=self.font_helvetica)

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
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Help", underline=1)
        self.menu_bar.add_cascade(label="Help", underline=1)

        # Display the menu
        root.config(menu=self.menu_bar)

    def font_helvetica(self, event=None):
        self.editor.config(font=("Helvetica", current_size))
        global current_font
        current_font = "Helvetica"
    def font_courier(self, event=None):
        self.editor.config(font=("Courier", current_size))
        global current_font
        current_font = "Courier"
    def font_times(self, event=None):
        self.editor.config(font=("Times", current_size))
        global current_font
        current_font = "Times"
    def font_cambria(self, event=None):
        self.editor.config(font=("Cambria", current_size))
        global current_font
        current_font = "Cambria"
    def font_calibri(self, event=None):
        self.editor.config(font=("Calibri", current_size))
        global current_font
        current_font = "Calibri"
    def font_verdana(self, event=None):
        self.editor.config(font=("Verdana", current_size))
        global current_font
        current_font = "Verdana"
    def font_papyrus(self, event=None):
        self.editor.config(font=("Papyrus", current_size))
        global current_font
        current_font = "Papyrus"
    def font_gothic(self, event=None):
        self.editor.config(font=("Gothic", current_size))
        global current_font
        current_font = "Gothic"
    def font_rockwell(self, event=None):
        self.editor.config(font=("Rockwell", current_size))
        global current_font
        current_font = "Rockwell"
    def font_corbel(self, event=None):
        self.editor.config(font=("Corbel", current_size))
        global current_font
        current_font = "Corbel"
    def font_georgia(self, event=None):
        self.editor.config(font=("Georgia", current_size))
        global current_font
        current_font = "Georgia"

    def color_black(self, event=None):
        self.editor.config(fg="black")
    def color_white(self, event=None):
        self.editor.config(fg="white")
    def color_red(self, event=None):
        self.editor.config(fg="red")
    def color_orange(self, event=None):
        self.editor.config(fg="orange")
    def color_yellow(self, event=None):
        self.editor.config(fg="yellow")
    def color_green(self, event=None):
        self.editor.config(fg="green")
    def color_blue(self, event=None):
        self.editor.config(fg="blue")
    def color_purple(self, event=None):
        self.editor.config(fg="purple")

    def size8(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 8))
        current_size = 8
    def size9(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 9))
        current_size = 9
    def size10(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 10))
        current_size = 10
    def size11(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 11))
        current_size = 11
    def size12(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 12))
        current_size = 12
    def size14(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 14))
        current_size = 14
    def size16(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 16))
        current_size = 16
    def size18(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 18))
        current_size = 18
    def size20(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 20))
        current_size = 20
    def size22(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 22))
        current_size = 22
    def size24(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 24))
        current_size = 24
    def size26(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 26))
        current_size = 26
    def size28(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 28))
        current_size = 28
    def size36(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 36))
        current_size = 36
    def size48(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 48))
        current_size = 48
    def size72(self, event=None):
        global current_font, current_size
        self.editor.config(font=(current_font, 72))
        current_size = 72

    def theme_day(self, event=None):
        self.editor.config(background="White")
    def theme_dark(self, event=None):
        self.editor.config(background="Black")

    def _highlight_current_line(self, interval=100):
        '''Updates the 'current line' highlighting every "interval" milliseconds'''
        self.editor.tag_remove("current_line", 1.0, "end")
        self.editor.tag_add("current_line", "insert linestart", "insert lineend+1c")
        self.root.after(interval, self._highlight_current_line)

    def save_if_modified(self, event=None):
        if self.editor.edit_modified(): 
            response = messagebox.askyesnocancel("Save?", "This document has been modified. Do you want to save changes?")
            if response: #yes/save
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
            self.editor.delete(1.0, "end")
            self.editor.edit_modified(False)
            self.editor.edit_reset()
            self.file_path = None
            self.set_title()
            

    def file_open(self, event=None, file_path=None):
        result = self.save_if_modified()
        # None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
        if result != None: 
            if file_path == None:
                file_path = filedialog.askopenfilename()
            if file_path != None  and file_path != '':
                with open(file_path, encoding="utf-8") as file:
                    fileContents = file.read()
                # Set current text to file contents
                self.editor.delete(1.0, "end")
                self.editor.insert(1.0, fileContents)
                self.editor.edit_modified(False)
                self.file_path = file_path

    def file_save(self, event=None):
        if self.file_path == None:
            result = self.file_save_as()
        else:
            result = self.file_save_as(file_path=self.file_path)
        return result

    def file_save_as(self, event=None, file_path=None):
        if file_path == None:
            file_path = filedialog.asksaveasfilename(filetypes=(('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*'))) #defaultextension='.txt'
        try:
            with open(file_path, 'wb') as file:
                text = self.editor.get(1.0, "end-1c")
                file.write(bytes(text, 'UTF-8'))
                self.editor.edit_modified(False)
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
            self.editor.edit_undo()
        except:
            print("There is nothing to undo...") 
        
    def redo(self, event=None):
        try:    
            self.editor.edit_redo()   
        except:
            print("There is nothing to redo...")    


    def main(self, event=None):          
        self.editor.bind("<Control-o>", self.file_open)
        self.editor.bind("<Control-O>", self.file_open)
        self.editor.bind("<Control-S>", self.file_save)
        self.editor.bind("<Control-s>", self.file_save)
        self.editor.bind("<Control-y>", self.redo)
        self.editor.bind("<Control-Y>", self.redo)
        self.editor.bind("<Control-Z>", self.undo)
        self.editor.bind("<Control-z>", self.undo)



if __name__ == "__main__":
    root = Tk()
    root.wm_state('normal')
    editor = TextWindow(root)
    editor.main()
    image = PhotoImage(file="viper.png")
    root.tk.call('wm', 'iconphoto', root._w, image)
    text = Text(root)
    #text.tag_configure("current_line", background="#e9e9e9")
    #_highlight_current_line()
    root.mainloop()