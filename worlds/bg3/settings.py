import settings
import os

class BG3Settings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """
        Locates the BG3 root directory on your system.
        This is used by the BG3 client, so it knows where to send communication files to.
        """
        description = "BG3 root directory"

        def browse(self, **kwargs):
            from Utils import messagebox
            messagebox("BG3 folder not found",
                       "BG3Client couldn't detect a path to the BG3 folder.\n"
                       "Please select the BG3 install folder. It should look something like AppData/Local/Larian Studios/Baldur's Gate 3/.")
            super().browse(**kwargs)

    root_directory: RootDirectory = RootDirectory(os.path.join("%LOCALAPPDATA%", "Larian Studios", "Baldur's Gate 3"))
