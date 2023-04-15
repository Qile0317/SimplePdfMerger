#from SimplePdfMerger.doublinklist import *
from SimplePdfMerger.main_gui import * #doesnt work when using pyinstaller

if __name__ == '__main__':
    app = main_gui()
    app.run()