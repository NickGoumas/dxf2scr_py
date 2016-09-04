import math
import ezdxf

dwg = ezdxf.readfile("C:\Users\Nick\Desktop\Test Folder\TestPart1.DXF")

file = open('testOutput.scr', 'r+')

gridOutput = 'GRID {};\n'.format('INCH')
print gridOutput,
file.write(gridOutput)

layerOutput = 'LAYER {};\n'.format('20')
print layerOutput,
file.write(layerOutput)

modelspace = dwg.modelspace()

for e in modelspace:
    if e.dxftype() == 'LINE':
        #Eagle Command Syntax
        #WIRE  (Start Point) (End Point)
        lineOutput = ('WIRE ({} {}) ({} {})\n'.format(str(e.dxf.start[0]), str(e.dxf.start[1]), str(e.dxf.end[0]), str(e.dxf.end[1])))
        print lineOutput,
        file.write(lineOutput)

for e in modelspace:
    if e.dxftype() == 'CIRCLE':
        #CIRCLE (Center Point) (Any Point on Circumference)
        circleOutput = ('CIRCLE ({} {}) ({} {})\n'.format(str(e.dxf.center[0]), str(e.dxf.center[1]), str(e.dxf.radius+e.dxf.center[0]), str(e.dxf.center[1])))
        print circleOutput,
        file.write(circleOutput)

for e in modelspace:
    if e.dxftype() == 'ARC':
        #ARC (CW | CCW) (Start Point) (Opposite Point) (End Point)
        #ezdxf reads all arcs as CCW.
        arcStartX = round(e.dxf.center[0] + (e.dxf.radius * math.cos(math.radians(e.dxf.start_angle))), 4) + 0
        arcStartY = round(e.dxf.center[1] + (e.dxf.radius * math.sin(math.radians(e.dxf.start_angle))), 4) + 0
        arcOppX = round(e.dxf.center[0] + (e.dxf.radius * math.cos(math.radians(e.dxf.start_angle))) * -1, 4) + 0
        arcOppY = round(e.dxf.center[1] + (e.dxf.radius * math.sin(math.radians(e.dxf.start_angle))) * -1, 4) + 0
        arcEndX = round(e.dxf.center[0] + (e.dxf.radius * math.cos(math.radians(e.dxf.end_angle))), 4) + 0
        arcEndY = round(e.dxf.center[1] + (e.dxf.radius * math.sin(math.radians(e.dxf.end_angle))), 4) + 0
        arcOutput = ( ('ARC CCW ({} {}) ({} {}) ({} {})\n').format(str(arcStartX), str(arcStartY), str(arcOppX), str(arcOppY), str(arcEndX), str(arcEndY)) )
        print arcOutput,
        file.write(arcOutput)

for e in modelspace:
    if e.dxftype() == 'POLYLINE':
        print e.is_2d_polyline
        print e.__len__()
        
        print list(e.points())[0]
        
        #Round points. Iterate through. If the two points are different create a line between, else skip the step.
        
        #No damn ellipse command in eagle apparently.
        #print 'test'
        #print ('Center Point:{}').format(str(e.dxf.enter))
        #print ('Major Axis:{}').format(str(e.dxf.major_axis))



        

file.close()