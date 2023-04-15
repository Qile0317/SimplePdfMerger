import tkinter as tk
from tkinter import filedialog, messagebox
from screeninfo import get_monitors
from doublylinkedlist import DoublyLinkedList
from pypdf import PdfWriter

class main_gui:
    def __init__(self):
        self.pdf_list = DoublyLinkedList()
        self.background_color = "#212121"
        self.root = tk.Tk()

        self.pdf_list_frame = tk.Frame(self.root, bg = self.background_color)
        self.pdf_list_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        self.button_frame = tk.Frame(self.root, bg = self.background_color)
        self.button_frame.pack(side = tk.RIGHT, fill = tk.Y)

        self.create_window_skeleton()
        self.add_all_buttons()
    
    def create_window_skeleton(self):
        self.root.title("PDF Appender")
        self.root.iconphoto(False, tk.PhotoImage(file = "pdf_merger_logo.png"))
        self.root.configure(bg = self.background_color)

        main_monitor = get_monitors()[0]
        self.root.geometry("%dx%d" % (main_monitor.width//2, main_monitor.height//2))

    def add_all_buttons(self):
        self.insert_button("Add PDF",
            command = self.open_file_explorer)
        self.insert_button("Merge PDFs",
            command = self.pdf_merger)
        self.insert_button("Clear PDF list",
            command = self.clear_pdf_list)

    def run(self):
        self.root.mainloop()
    
    # functions for the buttons - i couldnt make it in another script :/
    def open_file_explorer(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if self.pdf_list._find_node(file_path):
                messagebox.showerror(title="Error", message = "This PDF is already in the list!")
            elif file_path[-3:] != "pdf":
                messagebox.showerror(title="Error", message = "Selected file is not a PDF!")
            else:
                self.pdf_list.append(file_path)
                self.update_pdf_list()

    # Remove the selected PDF from the list
    def remove_pdf(self, pdf_node):
        self.pdf_list.remove(pdf_node)
        self.update_pdf_list()

    # Add a PDF before the selected PDF
    def add_before_pdf(self, pdf_node):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.pdf_list.insert_before(pdf_node, file_path)
            self.update_pdf_list()

    # Add a PDF after the selected PDF
    def add_after_pdf(self, pdf_node):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.pdf_list.insert_after(pdf_node, file_path)
            self.update_pdf_list()

    # Update the display of the PDF list box
    def update_pdf_list(self):
        # Clear the existing list
        for widget in self.pdf_list_frame.winfo_children():
            widget.destroy()

        # Create a frame for each PDF in the list
        for pdf_node in self.pdf_list:
            pdf_frame = tk.Frame(self.pdf_list_frame, bg = self.background_color)
            pdf_frame.pack(fill = tk.X, padx = 5, pady = 5)

            # Add a button to remove the PDF from the list
            remove_button = tk.Button(
                pdf_frame,
                text = "×",
                fg = "white",
                bg = "red",
                command = lambda node = pdf_node: self.remove_pdf(node))
            remove_button.pack(side = tk.LEFT, padx = 5)

            # Add a button to add a PDF before the current one
            before_button = tk.Button(
                pdf_frame,
                text = "+ Before",
                fg = "white",
                bg = "orange",
                command = lambda node = pdf_node: self.add_before_pdf(node))
            before_button.pack(side = tk.LEFT, padx = 5)

            # Add a button to add a PDF after the current one
            after_button = tk.Button(
                pdf_frame,
                text = "+ After",
                fg = "white",
                bg = "orange",
                command = lambda node = pdf_node: self.add_after_pdf(node))
            after_button.pack(side = tk.LEFT, padx = 5)

            # Add the PDF filename to the frame
            pdf_label = tk.Label(
                pdf_frame,
                text = pdf_node,
                bg = self.background_color,
                fg = 'white',
                wraplength = 500,
                justify=tk.LEFT)
            pdf_label.pack(side = tk.LEFT, fill = tk.X, expand = True)

    def clear_pdf_list(self):
        self.pdf_list.clear()
        self.update_pdf_list()

    def merge_pdfs(self, output_file):
        merger = PdfWriter()
        for pdf in self.pdf_list:
            merger.append(pdf)
        merger.write(output_file)
        merger.close()

    def pdf_merger(self):
        if self.pdf_list.length == 0:
            messagebox.showerror(
                title = "Error",
                message = "Please add some PDFs to the list first!")
            return
        output_file = filedialog.asksaveasfilename(
            initialdir = "~/Documents",
            defaultextension = ".pdf")
        if output_file:
            try:
                merge_pdfs(self.pdf_list, output_file)
                tk.messagebox.showinfo(
                    title = "Success",
                    message = "PDFs merged successfully at " + output_file)
            except Exception as e:
                tk.messagebox.showerror(
                    title = "Error",
                    message = str(e))

    # button creation:
    def create_button(self, text, command,
                  bg = "gray",
                  fg = "white",
                  activebackground = "gray",
                  activeforeground = "white",
                  bd = 0,
                  padx = 10,
                  pady = 5,
                  font = ("Helvetica", 15),
                  width = 20,
                  height = 3):
        button = tk.Button(
            self.button_frame, text = text, command = command,
            bg=bg,fg=fg, activebackground=activebackground, activeforeground=activeforeground, bd=bd, padx=padx, pady=pady, font=font, width=width, height=height)
        button.pack(pady = 15, fill = tk.X)

    def add_separator_line(self):
        separator_line = tk.Frame(
            self.button_frame,
            height = 2,
            bg = "white",
            bd = 0)
        separator_line.pack(fill = tk.X)

    def insert_button(self, text, command):
        self.create_button(text, command)
        self.add_separator_line()