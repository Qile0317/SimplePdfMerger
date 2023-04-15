import pytest
from SimplePdfMerger.main_gui import *
from unittest import mock
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from screeninfo import Monitor

# Fixture for the main_gui instance
@pytest.fixture(scope="module")
def gui():
    return main_gui()

# Fixture for the temporary PDF file created during testing
@pytest.fixture(scope="module")
def temp_pdf_file():
    yield "test_output.pdf"
    os.remove("test_output.pdf")

# Test creating the window skeleton
def test_create_window_skeleton(gui):
    gui.create_window_skeleton()
    assert gui.root.title() == "PDF Appender"
    assert gui.root.iconphoto(False) is not None
    assert gui.root.cget("bg") == "#212121"
    assert gui.root.geometry() == "%dx%d" % (Monitor().width//2, Monitor().height//2)

# Test adding a PDF to the list
@mock.patch.object(main_gui, 'update_pdf_list')
def test_open_file_explorer(mock_update_pdf_list, gui):
    gui.open_file_explorer()
    assert gui.pdf_list.length == 0

    with mock.patch.object(filedialog, 'askopenfilename', return_value="file.pdf"):
        gui.open_file_explorer()
        assert gui.pdf_list.length == 1
        assert gui.pdf_list.head.value == "file.pdf"
        mock_update_pdf_list.assert_called_once()

    with mock.patch.object(filedialog, 'askopenfilename', return_value=None):
        gui.open_file_explorer()
        assert gui.pdf_list.length == 1

    with mock.patch.object(filedialog, 'askopenfilename', return_value="file.txt"):
        with mock.patch.object(messagebox, 'showerror') as mock_showerror:
            gui.open_file_explorer()
            assert gui.pdf_list.length == 1
            mock_showerror.assert_called_once()

    with mock.patch.object(filedialog, 'askopenfilename', return_value="file.pdf"):
        with mock.patch.object(gui.pdf_list, '_find_node', return_value=True):
            with mock.patch.object(messagebox, 'showerror') as mock_showerror:
                gui.open_file_explorer()
                assert gui.pdf_list.length == 1
                mock_showerror.assert_called_once()

# Test removing a PDF from the list
@mock.patch.object(main_gui, 'update_pdf_list')
def test_remove_pdf(mock_update_pdf_list, gui):
    gui.pdf_list.append("file1.pdf")
    gui.pdf_list.append("file2.pdf")
    gui.pdf_list.append("file3.pdf")
    assert gui.pdf_list.length == 3

    gui.remove_pdf(gui.pdf_list.head.next_node)
    assert gui.pdf_list.length == 2
    assert gui.pdf_list.head.next_node.value == "file3.pdf"
    mock_update_pdf_list.assert_called_once()

# Test inserting a PDF before another PDF in the list
@mock.patch.object(main_gui, 'update_pdf_list')
def test_add_before_pdf(mock_update_pdf_list, gui):
    gui.pdf_list.append("file1.pdf")
    gui.pdf_list.append("file2.pdf")
    gui.pdf_list.append("file3.pdf")
    assert gui.pdf_list.length == 3

    gui.add_before_pdf(gui.pdf_list.head.next_node)
    assert gui.pdf_list.length == 4
    assert gui.pdf_list.head.next_node.value == "file4.pdf"
    mock_update_pdf_list.assert_called_once()

def test_update_pdf_list():
    gui = main_gui()
    pdf_paths = ["pdf1.pdf", "pdf2.pdf", "pdf3.pdf"]
    for pdf in pdf_paths:
        gui.pdf_list.append(pdf)
    gui.update_pdf_list()
    for pdf, frame in zip(gui.pdf_list, gui.pdf_list_frame.winfo_children()):
        assert isinstance(frame, tk.Frame)
        assert isinstance(frame.winfo_children()[0], tk.Button)  # remove button
        assert isinstance(frame.winfo_children()[1], tk.Button)  # before button
        assert isinstance(frame.winfo_children()[2], tk.Button)  # after button
        assert isinstance(frame.winfo_children()[3], tk.Label)   # pdf label
        assert frame.winfo_children()[3]['text'] == pdf

def test_clear_pdf_list():
    gui = main_gui()
    pdf_paths = ["pdf1.pdf", "pdf2.pdf", "pdf3.pdf"]
    for pdf in pdf_paths:
        gui.pdf_list.append(pdf)
    gui.clear_pdf_list()
    assert gui.pdf_list.length == 0
    assert len(gui.pdf_list_frame.winfo_children()) == 0

# unfinished