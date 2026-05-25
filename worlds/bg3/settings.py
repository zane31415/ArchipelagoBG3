import settings
import os
from typing import Union

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
            return super().browse(**kwargs)

    class UTPackPath(settings.FilePath):
        """
        Path to the BG3 PopTracker pack zip used by Universal Tracker
        for the map tab. Leave blank to be prompted on first launch;
        set to None to disable the UT map tab entirely.
        """
        required = False
        ut_dialog_name = "Select BG3 PopTracker pack (zip)"

    root_directory: RootDirectory = RootDirectory(os.path.join("%LOCALAPPDATA%", "Larian Studios", "Baldur's Gate 3"))
    ut_pack_path: Union[UTPackPath, str] = UTPackPath()
