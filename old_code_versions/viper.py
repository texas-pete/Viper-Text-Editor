import tkinter as tk
from tkinter import *
from tkinter import Tk, ttk, Text, Scrollbar, Menu, messagebox, filedialog, Frame, PhotoImage
import os, subprocess, json, string

class TextWindow(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self.root = root        
        self.TITLE = "Viper"
        self.file_path = None
        tk.Frame.__init__(self, *args, **kwargs)    
        self.set_title()

        

        # Frame for the Text Window
        frame = Frame(root)
        #self.text = CustomText(self)
        self.text = TextLineNumbers(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)
        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        self.tabs = {'ky':0}
        self.tab_list = []
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Bindings and Hot Key Bindings
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        # Closes the application
        root.protocol("WM_DELETE_WINDOW", self.file_quit) 

        # Create a top level menu
        self.menu_bar = Menu(root)

        # File menu 
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New File", underline=1, command=self.generate_tab, accelerator="Ctrl+N")
        file_menu.add_command(label="Open File", underline=1, command=self.file_open, accelerator="Ctrl+O")
        file_menu.add_command(label="Open Project", underline=1, command=self.project_open)
        file_menu.add_command(label="Save File", underline=1, command=self.file_save, accelerator="Ctrl+S")
        file_menu.add_command(label="Save File As...", underline=5, command=self.file_save_as, accelerator="Ctrl+Alt+S")
        file_menu.add_command(label="Save Project", underline=1, command=self.project_save)
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
        format_menu.add_command(label="Font Color", underline=1)
        self.menu_bar.add_cascade(label="Format", underline=1)

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

    def save_if_modified(self, event=None):
        if self.text.edit_modified(): 
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
            self.text.delete(1.0, "end")
            self.text.edit_modified(False)
            self.text.edit_reset()
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
            if file_path != None  and file_path != '':
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
            file_path = filedialog.asksaveasfilename(filetypes=(('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*'))) #defaultextension='.txt'
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

    def add_tab(self, name):
        tab = Tab(self.notebook, name)
        print(name)
        self.notebook.add(tab, text=name)
        self.tab_list.append(tab) 

    def get_tab(self):
        print(self.notebook.index('current'))
        #Get the tab object from the tab_list based on the index of the currently selected tab
        tab = self.tab_list[self.notebook.index('current')]
        return tab

    def generate_tab(self):
        if self.tabs['ky'] < 20:
            self.tabs['ky'] += 1
            self.add_tab('Document ' + str(self.tabs['ky']))

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


class Tab(tk.Frame):

    def __init__(self, root, name):
        Frame.__init__(self, root)

        self.root = root
        self.name = name

        self.textWidget = Text(self)
        self.textWidget.pack(expand=True, fill='both')

    def save_tab(self):
        print(self.textWidget.get("1.0", 'end-1c'))
        file = open(filedialog.asksaveasfilename() + '.txt', 'w+')
        file.write(self.textWidget.get("1.0", 'end-1c'))
        print(os.path.basename(file.name))
        #title = os.path.basename(file.name)
        file.close()


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
        while True :
            dline= self.__line_numbers.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            line_num = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=line_num)
            i = self.__line_numbers.index("%s+1line" % i)

        
# class CustomText(tk.Text):
#     def __init__(self, *args, **kwargs):
#         tk.Text.__init__(self, *args, **kwargs)

#         # create a proxy for the underlying widget
#         self._orig = self._w + "_orig"
#         self.tk.call("rename", self._w, self._orig)
#         self.tk.createcommand(self._w, self._proxy)

#     def _proxy(self, *args):
#         # let the actual widget perform the requested action
#         cmd = (self._orig,) + args
#         result = self.tk.call(cmd)

#         # generate an event if something was added or deleted,
#         # or the cursor position changed
#         if (args[0] in ("insert", "replace", "delete") or 
#             args[0:3] == ("mark", "set", "insert") or
#             args[0:2] == ("xview", "moveto") or
#             args[0:2] == ("xview", "scroll") or
#             args[0:2] == ("yview", "moveto") or
#             args[0:2] == ("yview", "scroll")
#         ):
#             self.event_generate("<<Change>>", when="tail")

#         # return what the actual widget returned
#         return result  


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_state('normal')
    text = TextWindow(root).pack(side="top", fill="both", expand=True)
    #text.main()
    image = PhotoImage(file="viper.png")
    root.tk.call('wm', 'iconphoto', root._w, image) 
    root.mainloop()