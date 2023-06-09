# <img src="images/pdf_merger_logo.png" width = "17.5%" align = "right" /> SimplePdfMerger

[![Latest Release](https://img.shields.io/github/release/Qile0317/SimplePdfMerger.svg)](https://github.com/Qile0317/SimplePdfMerger/releases/latest)
[![MIT license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Qile0317/SimplePdfMerger/LICENSE.md)

Worried about online pdf merger tools keeping your persnoal information or being needlessly overcomplicated to use? `SimplePdfMerger` solves this issue: a simple, opensource, *darkmode* pdf merging windows desktop application written in less than 400 lines. The windows executable file `SimplePdfMerger.exe` and can also be found in the latest releases page.

## Installation
To run the app, simply download the executable `SimplePdfMerger.exe` from the latest release page (https://github.com/Qile0317/SimplePdfMerger/releases/download/v0.2.1/SimplePdfMerger.exe) and click on it when downloaded. The executable works on windows and the code hasn't been tested on other systems yet.

If one is worried about the executable being malicious, the app can also be compiled from scratch by cloning the repository and built with pyinstaller from the command line with the following code:
```
git clone https://github.com/Qile0317/SimplePdfMerger.git
cd SimplePdfMerger
pyinstaller --onefile -w -F main_gui.pyw
```

## Usage
PDFs, JPEGS, and PNGs can all be merged in any order into a pdf file within the following user GUI:

<img src="images/GUI_example.png" width = "70%" align = "center" />

On the right hand side, the first button "Add file(s)" opens the file explorer when clicked, allowing the user to select one or more files through the file explorer to add to the end of the file list that can be merged into a pdf on the left hand side. The file can be a `.pdf`, `.png`, or `.jpg` file. The second button "Merge files" will attempt to convert all files in the filelist into pdfs and merge them into an output location chosen by the user in the file explorer. If (un)successful, a popup will be shown informing the user. The third button "Clear list" will simply clear the pdf list.

In the filelist, for each file, the filename will be shown in the right. On the left for each file, there are again three buttons. The first red x will remove the corresponding file from the filelist. The second button will open the file explorer to add a file before (above) the current file, while the second button will do the reverse.

*Developer's note: The `main_gui.pyw` script in `SimplePdfMerger` should ideally be split up but there were difficulties with the import system when using `pyinstaller`. Also, in the future the files in the filelsit should be made draggable should the user wants to reorder them.*