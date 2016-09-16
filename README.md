# dxf2scr_py
Python program that generates an Eagle-readable script file from a 2D DXF file.

Using python v2.7. Requires the ezdxf package, currently using v0.7.6. Using SolidWorks 2016 to save DXF files in version R12 for testing. 

Usage: The first argument after calling the command is the DXF file.
Example: $ python dxf2scr.py ExamplePart.DXF

So far it can convert from DXF to scr the following entities: (DXF -> scr)

    LINE -> WIRE
    CIRCLE -> CIRCLE
    ARC -> ARC
    POLYLINE -> WIRE
    
Things to know:
    
    The output file takes the name of the input file.
    WIRE entities in eagle default to width 0.
    CIRCLE entities in eagle default to width 1mil.
    There is a debug flag to print the output to the shell.
    Entities in eagle default to layer 20 right now.
    CIRCLE entities <= 0.25 (drillThreshold) become drill holes in eagle