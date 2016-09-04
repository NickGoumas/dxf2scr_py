# dxf2scr_py
Python program that generates an Eagle-readable script file from a 2D DXF file.

Using python 2.7. Using SolidWorks 2016 to save DXF files in version R12 for testing. 

This is starting off as a simple script. It may grow into a more user friendly GUI as time goes on. The purpose of this project is twofold. To build a usable tool and also get some experience using git. As always, time spent coding python is always welcome.

The output file 'testOutput.scr' is hardcoded, line 7. Just make a blank file it can overwrite for now.

Usage: The first argument after calling the command is the DXF file.

So far it can convert from DXF to scr the following entities: (DXF -> scr)

    LINE -> WIRE
  
    CIRCLE -> CIRCLE
  
    ARC -> ARC

Now working on:

    POLYLINE -> WIRE


