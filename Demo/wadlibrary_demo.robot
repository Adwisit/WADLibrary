*** Settings ***
Library  WADLibrary
Library  Common.py

# Starts up and teardowns the driver. Exclude these and start the driver manually if you want to log the driver output
Suite Setup  set up driver
Suite Teardown  tear down driver

# Sets up and clears the sessions inbetween tests (each attached window gets its own session)
Test Setup  set up
Test Teardown  clean up

*** Test Cases ***
Paint
    cmd run  mspaint.exe
    sleep  1    
    attach to window  Untitled - Paint  Paint
    sleep  1
    close window

Calculator
    cmd run  calc.exe
    sleep  1
    attach to window  Calculator  Calculator
    click element  One
    click element  Plus
    click element  Two
    click element  Equals
    sleep  1
    close window

Switch window
    cmd run  calc.exe
    sleep  1
    attach to window  Calculator  Calculator
    sleep  1
    set current session  Root
    cmd run  mspaint.exe
    sleep  1
    attach to window  Untitled - Paint  Paint
    set current session  Calculator
    set focus
    click element  One
    click element  Plus
    click element  Two
    click element  Equals
    sleep  1
    close window
    set current session  Root
    set current session  Paint
    set focus
    close window
