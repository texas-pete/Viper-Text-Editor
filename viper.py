from tkinter import Tk, Text, Scrollbar, Menu, messagebox, filedialog, Frame, PhotoImage
import os, subprocess, json, string

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
        self.editor.config( wrap = "word", undo = True, width = 80 )        
        self.editor.focus()
        self.y_scroll_bar.pack(side="right", fill="y")
        self.y_scroll_bar.config(command=self.editor.yview)        
        frame.pack(fill="both", expand=1)

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
    root.mainloop()