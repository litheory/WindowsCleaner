# Windows Cleaner

**Windows Cleaner**, an Windows optimize scripts, which can scan and delete rubbish files or serach big files. This scirpts was an improvements veision of the **PyOptimize** in the ***Python Treasured Book***[Edit by Yang peilu and Song qiang, etc].

## Requirements

In `Python 2.7`. The  modules used are as follows:

- Tkinter
- tkMessageBox
- tkSimpleDialog
- os
- os.path
- threading

## Installation

- Command-line tools

  Clone this repo and run the WindowsCleaner.py

  ```
  $ git clone git@github.com:vanyoung/WindowwsCleaner.git
  $ python WindowsCleaner.py
  # command 'sudo' may be needed 
  ```

- Download on website

  Visit https://github.com/Vanyoung/WindowsCleaner and download the ZIP, unzip the file and run the WindowsCleaner.py

## Usage

- Delete rubbish files

  - Choose the ‘Clean up’ menu

    - Click the 'Scan rubbish' button to scan rubbish files
    - Click the 'Del rubbish' button to delete rubbish files

- Search big files

  - Choose the 'Search file' menu

    - Click the 'Scan big file' button and set the file size to be scanned to scan big files
    - Click the 'Search file by name' button and set the file name to be searched to search the file you want


## Scannig area
The GetDirvers() function will scan all the Drives in Windows
	def GetDrives():
		drives = []
		for i in range(65,91):
			vol = chr(i) + ':/'
			if os.path.isdir(vol):
				drives.append(vol)
		return tuple(drives)
## Customization

- You can set your own rubbish-file list by modifying ***rubbishExt*** on the 10 line of the source code

  `rubbishExt = ['.tmp','.bak','.old','.wbk','.xlk','._mp','.gid','.chk','.syd','.$$$','.@@@','.~*']`

  **DO NOT ADD SYSTEM-CRITICAL FILES**

## TODOs

- [ ] Set your own rubbish-file list.

- [ ] ~~Add system-critical files~into ***rubbishExt***~~. (It's a dangerous and most of the time the system does not allow this.)


## Precautions

If the file name is in CJK will lead to the output file name garbled.

## License

MIT. See `LICENSE` file.
