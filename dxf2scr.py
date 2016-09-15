import sys
import math
import ezdxf

outputFilename = str(sys.argv[1]).split('.')[0]
outputFilename = outputFilename + '.scr'
file = open(outputFilename, 'w')

dwg = ezdxf.readfile(str(sys.argv[1]))

''' Will add a switch flag for INCH or MM later '''
gridOutput = 'GRID {};\n'.format('INCH')
print gridOutput,
file.write(gridOutput)

''' Layer 20 is the dimension layer in Eagle '''
layerOutput = 'LAYER {};\n'.format('20')
print layerOutput,
file.write(layerOutput)

modelspace = dwg.modelspace()

def makeLine(e):
    lineOutput = ('WIRE ({} {}) ({} {})\n'.format(str(e.dxf.start[0]), str(e.dxf.start[1]), str(e.dxf.end[0]), str(e.dxf.end[1])))
    print lineOutput,
    file.write(lineOutput)
    '''
    Eagle defines a a WIRE with a start and end point.
    WIRE  (Start Point) (End Point)
    '''
    
def makeCircle(e):
    circleOutput = ('CIRCLE ({} {}) ({} {})\n'.format(str(e.dxf.center[0]), str(e.dxf.center[1]), str(e.dxf.radius+e.dxf.center[0]), str(e.dxf.center[1])))
    print circleOutput,
    file.write(circleOutput)
    '''
    Eagle defines a circle with a center point and a point anywhere
    on the circumference.
    #CIRCLE (Center Point) (Any Point on Circumference)
    '''
    
def makeArc(e):
    arcStartX = round(e.dxf.center[0] + (e.dxf.radius * math.cos(math.radians(e.dxf.start_angle))), 3) + 0
    arcStartY = round(e.dxf.center[1] + (e.dxf.radius * math.sin(math.radians(e.dxf.start_angle))), 3) + 0
    arcOppX = round(e.dxf.center[0] + (e.dxf.radius * math.cos(math.radians(e.dxf.start_angle))) * -1, 3) + 0
    arcOppY = round(e.dxf.center[1] + (e.dxf.radius * math.sin(math.radians(e.dxf.start_angle))) * -1, 3) + 0
    arcEndX = round(e.dxf.center[0] + (e.dxf.radius * math.cos(math.radians(e.dxf.end_angle))), 3) + 0
    arcEndY = round(e.dxf.center[1] + (e.dxf.radius * math.sin(math.radians(e.dxf.end_angle))), 3) + 0
    arcOutput = ( ('ARC CCW ({} {}) ({} {}) ({} {})\n').format(str(arcStartX), str(arcStartY), str(arcOppX), str(arcOppY), str(arcEndX), str(arcEndY)) )
    print arcOutput,
    file.write(arcOutput)
    '''
    Eagle defines an arc with three points. The first point is the 
    start of the arc. The second point is opposite the start point
    if the arc were a circle. The third point is the end of the 
    arc. The ezdxf library always reads arcs as CCW.
    #ARC (CW | CCW) (Start Point) (Opposite Point) (End Point)
    '''
    
def makePoly(e):
    #print e.is_2d_polyline
    for i in range(1,e.__len__()):
        polyStartX = round(list(e.points())[i-1][0], 3)
        polyStartY = round(list(e.points())[i-1][1], 3)
        polyEndX = round(list(e.points())[i][0], 3)
        polyEndY = round(list(e.points())[i][1], 3)
        if polyStartX != polyEndX or polyStartY != polyEndY:
            polyOutput = ('WIRE ({} {}) ({} {})\n').format(polyStartX, polyStartY, polyEndX, polyEndY)
            print polyOutput,
            file.write(polyOutput)
    '''
    ezdxf renderes ellipses as polylines. The polyline is broken up
    into it's individual points and lines are drawn from point to 
    point. If by rounding the two sets of points making the next 
    line are the same, the line is skipped. 
    '''
    
for entity in modelspace:
    if entity.dxftype() == 'LINE':
        makeLine(entity)
    elif entity.dxftype() == 'CIRCLE':
        makeCircle(entity)
    elif entity.dxftype() == 'ARC':
        makeArc(entity)
    elif entity.dxftype() == 'POLYLINE':
        makePoly(entity)

file.close()
