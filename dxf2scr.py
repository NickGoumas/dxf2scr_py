import sys
import math
import ezdxf

dwg = ezdxf.readfile(str(sys.argv[1]))

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
        '''
        Eagle defines a a WIRE with a start and end point.
        WIRE  (Start Point) (End Point)
        '''
        lineOutput = ('WIRE ({} {}) ({} {})\n'.format(str(e.dxf.start[0]), str(e.dxf.start[1]), str(e.dxf.end[0]), str(e.dxf.end[1])))
        print lineOutput,
        file.write(lineOutput)

for e in modelspace:
    if e.dxftype() == 'CIRCLE':
        '''
        Eagle defines a circle with a center point and a point anywhere
        on the circumference.
        #CIRCLE (Center Point) (Any Point on Circumference)
        ''' 
        circleOutput = ('CIRCLE ({} {}) ({} {})\n'.format(str(e.dxf.center[0]), str(e.dxf.center[1]), str(e.dxf.radius+e.dxf.center[0]), str(e.dxf.center[1])))
        print circleOutput,
        file.write(circleOutput)

for e in modelspace:
    if e.dxftype() == 'ARC':
        '''
        Eagle defines an arc with three points. The first point is the 
        start of the arc. The second point is opposite the start point
        if the arc were a circle. The third point is the end of the 
        arc. The ezdxf library always reads arcs as CCW.
        #ARC (CW | CCW) (Start Point) (Opposite Point) (End Point)
        '''
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
        '''
        ezdxf renderes ellipses as polylines. The polyline is broken up
        into it's individual points and lines are drawn from point to 
        point. If by rounding the two sets of points making the next 
        line are the same, the line is skipped. 
        '''
        #print e.is_2d_polyline
        for i in range(1,e.__len__()):
            polyStartX = round(list(e.points())[i-1][0], 4)
            polyStartY = round(list(e.points())[i-1][1], 4)
            polyEndX = round(list(e.points())[i][0], 4)
            polyEndY = round(list(e.points())[i][1], 4)
            if polyStartX != polyEndX or polyStartY != polyEndY:
                polyOutput = ('WIRE ({} {}) ({} {})\n').format(polyStartX, polyStartY, polyEndX, polyEndY)
                print polyOutput,
                file.write(polyOutput)        
        #Round points. Iterate through. If the two points are different create a line between, else skip the step.

file.close()
