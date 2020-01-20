# WADLibrary

WADLibrary is a Application testing library for Robot Framework that utilizes [Win App Driver](https://github.com/Microsoft/WinAppDriver).

This library was created to be able to work with multi-window use cases compared to Appium.

---

## Getting Started

### System Requirements

- Windows 10 PC
- Python 3
- Robot Framework

### Install the package

```
pip install robotframework-wadlibrary
```

### Setting up WinAppDriver

1. Download Windows Application Driver installer from <https://github.com/Microsoft/WinAppDriver/releases>
2. Run the installer on a **Windows 10** machine where your application under test is installed and will be tested
3. Run `WinAppDriver.exe` from the installation directory (E.g. `C:\Program Files (x86)\Windows Application Driver`)

Windows Application Driver will then be running on the test machine listening to requests on the default IP address and port (`127.0.0.1:4723`). `WinAppDriver.exe` can be configured to listen to a different IP address and port as follows:

```
WinAppDriver.exe 4727
WinAppDriver.exe 10.0.0.10 4725
WinAppDriver.exe 10.0.0.10 4723/wd/hub
```

> **Note**: You must run `WinAppDriver.exe` as **administrator** to listen to a different IP address and port.

### Running the Demo

This repo includes a demo that runs a automated script with Windows 10s included calculator and paint app. To run the demo you don't need to start up WinAppDriver beforehand since the test will do it on its own. Note that if you have installed the driver in a non-default path you have to submitt the driver path with the *driver_path* variable in the import.

You can also start the driver manually for debugging or just to see the driver output. Follow the intructions inside the test file and start the driver manually before running any tests.

```
path_to_repo/Demo robot wadlibrary_demo.robot
```

## Useful tools

- Inspection Tool , Part of Windows 10 SDK that can be found [here](https://developer.microsoft.com/en-US/windows/downloads/windows-10-sdk) (I recommomend to check [this](https://stackoverflow.com/questions/34760513/how-to-install-the-inspect-tool-on-windows-10) question on StackOverflow for instructions on how to install it if you dont want to install the whole SDK)

- WinAppDriver UI Recorder , [*UI Recorder tracks both keyboard and mouse interactions against an application interface—representing a UI action.*](https://github.com/microsoft/WinAppDriver/wiki/WinAppDriver-UI-Recorder), You can find it in the same place as the driver. [Download Link](https://github.com/Microsoft/WinAppDriver/releases)

---

This is my first python package so many things are not fixed yet, such as requirements. 

Looking for Keyword Documentation? There is none! (Yet) For now you'll have to simply look in the keyword file.

I've included a simple demo that shows how to use the main feature (compared to appium), i.e. switching between windows.