# BG_REMOVER
A small desktop GUI based on python tkinter and [rembg](https://github.com/danielgatis/rembg) to provide image background removing 

Current support 
- Select file or directories to remove the background
- All export to .PNG file

## Installation 
- install requirements.txt
```
$ pip install requirements.txt
```
## Usage 
```
$python app.py
```

## Package with pyinstall
```
$pyinstaller app_windows.spec -y --onedir --windowed
```
- Fix the error caused by scipy.libs not found 
    - Copy the `scipy.libs` directory under the envs's `Lib/site-packages` to the `dist/bg_remover`