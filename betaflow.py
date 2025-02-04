import os
import win32api
import win32con
import win32gui
from win32com.shell import shell, shellcon
import ctypes
import ctypes.wintypes

class BetaFlow:
    def __init__(self):
        self.desktop_path = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
        self.icons = self.get_desktop_icons()

    def get_desktop_icons(self):
        """Retrieve a list of icons present on the desktop."""
        icons = []
        for item in os.listdir(self.desktop_path):
            if item.endswith(".lnk") or os.path.isfile(os.path.join(self.desktop_path, item)):
                icons.append(item)
        return icons

    def arrange_icons(self, style='grid'):
        """Arrange desktop icons based on the specified style."""
        if style == 'grid':
            self.arrange_in_grid()
        elif style == 'line':
            self.arrange_in_line()
        else:
            raise ValueError("Unsupported style. Available styles: 'grid', 'line'.")

    def arrange_in_grid(self):
        """Arrange icons in a grid."""
        icon_size = 100
        x, y = 0, 0
        for icon in self.icons:
            self.move_icon(icon, x, y)
            x += icon_size
            if x > 800:  # Assume screen width
                x = 0
                y += icon_size

    def arrange_in_line(self):
        """Arrange icons in a horizontal line."""
        icon_size = 100
        x, y = 0, 0
        for icon in self.icons:
            self.move_icon(icon, x, y)
            x += icon_size

    def move_icon(self, icon_name, x, y):
        """Move an icon to a specified position."""
        full_path = os.path.join(self.desktop_path, icon_name)
        shinfo = win32api.FindExecutable(full_path)
        hwnd = win32gui.FindWindow(None, 'Program Manager')
        icon_position = (x, y)
        win32gui.SendMessage(hwnd, win32con.LVM_SETICONPOSITION, 0, icon_position)

    def refresh_desktop(self):
        """Refresh the desktop to apply changes."""
        win32api.PostMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, "Environment")

if __name__ == "__main__":
    betaflow = BetaFlow()
    betaflow.arrange_icons(style='grid')
    betaflow.refresh_desktop()