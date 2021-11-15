# f-icon

Set Folder Icons.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install f-icon
```

## Usage

### Parameters

f-icon [OPTIONS] [--] IMAGE

## Options:
    -h, --help                       Print this help text and exit
    -f, --folder                     Path to the folder that will have its icon changed. 
                                     It is ignored if the input is a text file.
    -p, --placement                  Path to the folder where to keep generated icons. 
                                     By default, they are stored inside the folder with a changed icon.
                                     Used only on Windows.
    -r, --relative                   If the icon is located in another folder, 
                                     it forces the path to be relative, 
                                     and it gets ignored if the drive for both locations is different.
                                     USed only on windows
    -v, --verbose                    Print various debugging information

### Direct

```python
import f_icon

# generate icon

image = "Path to the image."
folder = "Path to the folder" # is optional if the image is already in the folder that will use it
placement = "Path to the ico file" # is optional if icon stays in the folder. Ignored on macOS
relative = True # is placement set as relative path to the folder or direct path. Ignored on macOS
debug = False # display print() messages during work
f_icon.create_icon(image, folder, placement, relative, debug
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)