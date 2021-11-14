"""Create folder icon for Windows"""
import os
import time

from pathlib import Path
from subprocess import run
from configparser import ConfigParser
import numpy as np
from PIL import Image
import cv2  # opencv-python


class IconCreator:
    """
    Create icon for windows folder
    """

    def __init__(self, debug=False):
        """
        Initialization
        :param bool debug: Debug status
        """
        self.debug = debug

    def create_icon(self, input_file, folder="", placement="", relative=False):
        """
        Generates icons for Windows
        :param str input_file: Input image or text file.
        Image file location is used as folder location
        if not set other vice.
        :param str folder: Folder location. Ignored with text file
        :param str placement: Placement location of the ico file.
        :param bool relative: Path to the placement folder is relative. Ignored with text file
        If Placement folder is on another drive, relative is ignored.
        :param bool debug: display debug info
        :return:
        """
        if (
            placement != ""
            and folder != ""
            and relative
            and os.path.splitdrive(folder.lower())[0]
            != os.path.splitdrive(placement.lower())[0]
        ):
            relative = False

        # check if we have txt file with list or single image
        if os.path.splitext(input_file.lower())[1] == ".txt":
            with open(input_file, "r", encoding="UTF-8") as file:
                while line := file.readline().rstrip():
                    if not os.path.exists(line):
                        continue
                    # we are skipping a line if file is not found
                    folder = str(Path(line).parent)
                    if (
                        placement != ""
                        and relative
                        and os.path.splitdrive(folder.lower())[0]
                        == os.path.splitdrive(placement.lower())[0]
                    ):
                        placement_corrected = os.path.relpath(placement, folder)
                    else:
                        placement_corrected = placement
                    self._create_windows_icon(line, folder, placement_corrected)
        else:
            if folder == "":
                folder = str(Path(input_file).parent)
            if placement != "" and relative:
                placement = os.path.relpath(placement, folder)

            self._create_windows_icon(input_file, folder, placement)
        if self.debug:
            print("creating windows icon")

    def _create_windows_icon(self, image, folder, placement):
        """
        Creates actual icon
        :param str image: path to the image
        :param str folder: path to the folder
        :param str placement: path to the ico file location. can be relative
        :return:
        """
        # Reading an image (you can use PNG or JPG)
        img = cv2.imread(image)

        # Getting the bigger side of the image
        s = max(img.shape[0:2])

        # editing input image top have alpha channel
        alpha = np.full((img.shape[0], img.shape[1]), 255, dtype=np.uint8)
        img = np.dstack((img, alpha))

        # Creating a dark square with NUMPY
        f = np.zeros((s, s, 4), np.uint8)

        # Getting the centering position
        ax, ay = (s - img.shape[1]) // 2, (s - img.shape[0]) // 2

        # Pasting the 'image' in a centering position
        f[ay : img.shape[0] + ay, ax : ax + img.shape[1]] = img

        # Showing results (just in case)
        # cv2.imshow("IMG", f)
        # A pause, waiting for any press in keyboard
        # cv2.waitKey(0)

        # get direct path to the image
        placement_path = folder
        if placement != "":
            placement_path = placement
        # if placement have value and it is a relative path. False if path is relative
        if placement != "" and not os.path.isabs(placement):
            placement_path = folder + os.sep + placement

        # Saving the image
        temp_file = self._append_date(placement_path + os.sep + "_temp_.png")
        cv2.imwrite(temp_file, f)

        # now resizing image

        icon_name = Path(image).stem + ".ico"
        # add individual marker to icon name, if it is not saved locally
        if placement != "":
            icon_name = self._append_date(icon_name)

        img = Image.open(temp_file)
        img = img.resize((256, 256), Image.ANTIALIAS)
        img.save(placement_path + os.sep + icon_name, sizes=[(256, 256)])

        self._generate_desktop_ini(folder, os.path.join(placement, icon_name))
        self._set_attributes(folder)

        os.remove(temp_file)
        if self.debug:
            print("Icon Created for " + folder)

    def _generate_desktop_ini(self, dir_path, icon_path):
        """
        Generates desktop.ini file to display image
        :param str dir_path: path to the folder that will have desktop.ini
        :param str icon_path: path to the icon, can be relative
        :return:
        """
        config = ConfigParser()
        config.read(dir_path + os.sep + "desktop.ini")
        if ".ShellClassInfo" in config:
            if config[".ShellClassInfo"].get("IconResource") is not None:
                if self.debug:
                    print(
                        "Reset origin value: ",
                        config[".ShellClassInfo"]["IconResource"],
                    )
        else:
            config[".ShellClassInfo"] = {}

        config[".ShellClassInfo"]["IconResource"] = icon_path + ",0"

        try:
            if os.path.exists(dir_path + os.sep + "desktop.ini"):
                run(
                    ["attrib", "-a", "-s", "-h", dir_path + os.sep + "desktop.ini"],
                    shell=True,
                )
            with open(dir_path + os.sep + "desktop.ini", "w") as configfile:
                config.write(configfile)
                if self.debug:
                    print("Generated: " + dir_path + os.sep + "desktop.ini")
        except Exception as e:
            print(e)

    def _set_attributes(self, dir_path):
        """
        Set folder attribute to display icon
        :param str dir_path: folder path
        :return:
        """
        ini_path = dir_path + os.sep + "desktop.ini"

        run(["attrib", "+a", "+s", "+h", ini_path], shell=True)
        # run(["attrib", "+a",  ini_path], shell=True)
        if self.debug:
            print("Set attributes: Archive, System, Hidden ->", ini_path)

        run(["attrib", "+r", dir_path], shell=True)
        if self.debug:
            print("Set attribute: Read-only ->", dir_path)
            print()

    def clear_attributes(self, dir_path):
        """
        Clears folder attributes needed for the icon
        :param str dir_path: path to the folder
        :return:
        """
        ini_path = dir_path + os.sep + "desktop.ini"

        if os.path.isfile(ini_path):
            run(["attrib", "-a", "-s", "-h", ini_path], shell=True)
            if self.debug:
                print("Clear attributes: Archive, System, Hidden ->", ini_path)
        else:
            if self.debug:
                print("DO NOT EXIST: ", ini_path)

        run(["attrib", "-r", dir_path], shell=True)
        if self.debug:
            print("Clear attribute: Read-only ->", dir_path)

    def remove_desktop_ini(self, dir_path):
        """
        Removes desktop ini file
        :param str dir_path: path to the folder that holds desktop.ini
        :return:
        """
        ini_path = dir_path + os.sep + "desktop.ini"

        if os.path.isfile(ini_path):
            os.remove(ini_path)
            if self.debug:
                print("Removed: ", ini_path)
        else:
            if self.debug:
                print("DO NOT EXIST: ", ini_path)
                print()

    def _append_date(self, filename):
        """adds date to the end of the filename

        :param str filename: filename
        :return:
        """
        p = Path(filename)
        return "{0}_{2}{1}".format(
            Path.joinpath(p.parent, p.stem), p.suffix, time.strftime("%Y%m%d-%H%M%S")
        )
