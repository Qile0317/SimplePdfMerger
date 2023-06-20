import tkinter as tk
from tkinter import filedialog, messagebox
from screeninfo import get_monitors
from pypdf import PdfWriter
from PIL import Image
from img2pdf import convert
import tempfile
import os

# the doubly linked list with quite some overhead but O(1) insertion
class DoublyLinkedList:
    class Node:
        def __init__(self, data=None):
            self.data = data
            self.prev = None
            self.next = None

        def __repr__(self):
            return f"Node({self.data})"

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
        self.node_dict = {}

    def __len__(self):
        return self.length
    
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.data
            node = node.next
    
    def __repr__(self):
        if len(self) == 0:
            return "Empty DoublyLinkedList"
        
        current = self.head
        linked_list_str = f"DoublyLinkedList of length {self.length}:\n    "
        while current is not None:
            linked_list_str += f"{current.data}"
            if current.next is not None:
                linked_list_str += " <-> "
            current = current.next
        return linked_list_str
    
    def _find_node(self, data):
        if data in self.node_dict:
            return self.node_dict[data]
        return None

    def append(self, data):
        new_node = self.Node(data)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.node_dict[data] = new_node
        self.length += 1

    def prepend(self, data):
        new_node = self.Node(data)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.node_dict[data] = new_node
        self.length += 1

    def insert_after(self, prev_node_data, data):
        new_node = self.Node(data)
        prev_node = self._find_node(prev_node_data)
        if prev_node is None:
            raise ValueError(f"Node with data '{prev_node_data}' not found.")
        if prev_node is self.tail:
            self.tail = new_node
        new_node.next = prev_node.next
        new_node.prev = prev_node
        if prev_node.next is not None:
            prev_node.next.prev = new_node
        prev_node.next = new_node
        self.node_dict[data] = new_node
        self.length += 1

    def insert_before(self, next_node_data, data):
        new_node = self.Node(data)
        next_node = self._find_node(next_node_data)
        if next_node is None:
            raise ValueError(f"Node with data '{next_node_data}' not found.")
        if next_node is self.head:
            self.head = new_node
        new_node.prev = next_node.prev
        new_node.next = next_node
        if next_node.prev is not None:
            next_node.prev.next = new_node
        next_node.prev = new_node
        self.node_dict[data] = new_node
        self.length += 1

    def remove(self, data):
        node = self._find_node(data)
        if node is None:
            raise ValueError(f"Node with data '{data}' not found.")
        if node is self.head:
            self.head = node.next
        if node is self.tail:
            self.tail = node.prev
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        del self.node_dict[data]
        self.length -= 1

    def append_vector(self, vec):
        for element in vec:
            self.append(element)
            self.node_dict[element] = self._find_node(element)
    
    def clear(self):
        self.head = None
        self.tail = None
        self.length = 0
        self.node_dict = {}

# main GUI
class main_gui:
    def __init__(self):
        self.pdf_list = DoublyLinkedList()
        self.temp_directory = None
        self.background_color = "#212121"
        self.root = tk.Tk()

        # pdf list
        self.pdf_list_frame = tk.Frame(self.root, bg = self.background_color)
        self.pdf_list_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        # buttons
        self.button_frame = tk.Frame(self.root, bg = self.background_color)
        self.button_frame.pack(side = tk.RIGHT, fill = tk.Y)
        
        # initializing functions
        self.create_window_skeleton()
        self.add_all_buttons()
    
    # temporary directory creator and clearer for storing pdfs
    def create_temp_directory(self):
        self.temp_directory = tempfile.TemporaryDirectory()

    def clear_temp_directory(self):
        if self.temp_directory is not None:
            self.temp_directory.cleanup()

    # window creator
    def create_window_skeleton(self):
        self.root.title("Simple PDF file merger")
        # self.root.iconphoto(False, tk.PhotoImage(file = "pdf_merger_logo_base64.txt"))
        #self.root.wm_iconphoto(False, tk.PhotoImage(file = 'pdf_merger_logo_base64.txt'))
        self.root.configure(bg = self.background_color)

        main_monitor = get_monitors()[0]
        self.root.geometry("%dx%d" % (main_monitor.width//2, main_monitor.height//2))

    def add_all_buttons(self):
        self.insert_button("Add file",
            command = self.open_file_explorer)
        self.insert_button("Merge files",
            command = self.pdf_merger)
        self.insert_button("Clear list",
            command = self.clear_pdf_list)

    def run(self):
        self.root.mainloop()
    
    # functions for the buttons - i couldnt make it in another script :/
    def open_file_explorer(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if self.pdf_list._find_node(file_path):
                messagebox.showerror(title="Error", message = "This file is already in the list!")
            elif (file_path[-3:] != "pdf") and (file_path[-3:] != "png") and (file_path[-3:] != "jpg"):
                messagebox.showerror(title="Error", message = "Selected file is not a PDF or image!")
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
            if pdf.endswith(".pdf"):
                merger.append(pdf)
                continue
            # assume is png/jpg
            elif self.temp_directory == None:
                self.create_temp_directory()

            # convert png to pdf and store in the temporary directory - works
            curr_img = Image.open(pdf)
            pdf_bytes = convert(curr_img.filename)
            temp_pdf_path = os.path.join(self.temp_directory.name, "tempfile.pdf")
            file = open(temp_pdf_path, "wb")
            file.write(pdf_bytes)
            file.close()
            curr_img.close()
            pdf_bytes = None # save a teeny bit of memory            
            merger.append(temp_pdf_path)

        merger.write(output_file)
        merger.close()
        self.clear_temp_directory()

    def pdf_merger(self):
        if self.pdf_list.length == 0:
            messagebox.showerror(
                title = "Error",
                message = "Please add some files to the list first!")
            return
        output_file = filedialog.asksaveasfilename(
            initialdir = "~/Documents",
            defaultextension = ".pdf")
        if output_file:
            try:
                self.merge_pdfs(output_file)
                tk.messagebox.showinfo(
                    title = "Success",
                    message = "files merged successfully at " + output_file)
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

# app runner
if __name__ == '__main__':
    app = main_gui()
    app.run()

# pyinstaller input:
# pyinstaller --onefile -w -F --add-binary "pdf_merger_logo_base64.txt;." SimplePdfMerger/main_gui.pyw
