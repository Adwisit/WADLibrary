from .Keywords import Keywords
from .Driver import Driver


class WADLibrary(Keywords, Driver):
    def __init__(self, path="http://127.0.0.1:4723", platform="Windows", device_name="my_machine", timeout=30,
                 driver_path="C:/Program Files (x86)/Windows Application Driver/WinAppDriver"):
        Keywords.__init__(self, path, platform, device_name, timeout)
        Driver.__init__(self, driver_path)

    def wadlibrary_set_up(self):
        self.set_up_driver()
        self.set_up()

    def wadlibrary_tear_down(self):
        self.clean_up()
        self.tear_down_driver()
