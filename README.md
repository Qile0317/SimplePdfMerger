# <img src="pdf_merger_logo.png" width = "17.5%" align = "right" /> SimplePdfMerger

[![MIT license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Qile0317/SimplePdfMerger/LICENSE.md)

A simple, *darkmode* pdf merging windows desktop application written with tkinter. The windowsw executable file is `SimplePdfMerger.exe` and can also be found in the release.

To run the app, simply download the executable from the release page and click on it.

The app GUI houses three buttons on the right side, the topmost one being "Add PDF", to add a pdf to the end of the list of pdfs to merge by opening the file explorer, and allowing the user to select their pdfs. The middle button is "Merge PDFs", which again opens the file explorer and allows the user to name the merged pdf and select the directory. Finally, there is a "clear PDF list" button which empties the existing pdf list.

The absolute file directories of each pdf are shown in a list box on the left hand side of the application when added in order. Each directory is its own widget with three buttons, the "x" to remove the pdf from the list, and two others to add a pdf before or after the selected pdf in the list.

Developer's note: The `main_gui.py` script in `SimplePdfMerger` should ideally be split up but there were difficulties with the import system when using `pyinstaller`