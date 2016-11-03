import sys
import math
import ezdxf

try:
    len(sys.argv[2])
    try:
        outputFilename = str(sys.argv[2]).split('.')[0]
        outputFilename = outputFilename + '.scr'
    except:
        outputFilename = outputFilename + '.scr'

except:
    outputFilename = str(sys.argv[1]).split('.')[0]
    outputFilename = outputFilename + '.scr'

dwg = ezdxf.readfile(str(sys.argv[1]))
modelspace = dwg.modelspace()

'''Debug mode prints all output if equal to 1'''
debugMode = 0

'''All CIRCLE entities with less than or equal diameter to the threshold will
be converted to drill holes.'''
drillThreshold = 0.25


def setupScript():
    ''' Will add a switch flag for INCH or MM later. '''
    gridOutput = 'GRID {};\n'.format('INCH')
    file.write(gridOutput)
    if debugMode == 1:
        print gridOutput,
    ''' Layer 20 is the dimension layer in Eagle. '''
    layerOutput = 'LAYER {};\n'.format('20')
    file.write(layerOutput)
    if debugMode == 1:
        print layerOutput,
    '''Force wires to go from point to point.'''
    wireBend = 'SET WIRE_BEND 2;\n'
    file.write(wireBend)
    if debugMode == 1:
        print wireBend,

def makeLine(e):
    startX = str(round(e.dxf.start[0], 3))
    startY = str(round(e.dxf.start[1], 3))
    endX = str(round(e.dxf.end[0], 3))
    endY = str(round(e.dxf.end[1], 3))
    lineOutput = ('WIRE 0 ({} {}) ({} {})\n'.format(startX, startY, endX, endY))
    file.write(lineOutput)
    if debugMode == 1:
        print lineOutput,
    '''
    Eagle defines a a WIRE with a start and end point.
    WIRE  (Start Point) (End Point)
    '''
    
def makeCircle(e):
    centerX = str(round(e.dxf.center[0], 3))
    centerY = str(round(e.dxf.center[1], 3))
    pointX = str(round(e.dxf.radius + e.dxf.center[0], 3))
    pointY = centerY
    lineWidth = 0.001
    circleOutput = ('CIRCLE {} ({} {}) ({} {})\n'.format(lineWidth, centerX, centerY, pointX, pointY))
    file.write(circleOutput)
    if debugMode == 1:
        print circleOutput,
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
    file.write(arcOutput)
    if debugMode == 1:
        print arcOutput,
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
            file.write(polyOutput)
            if debugMode == 1:
                print polyOutput,
    '''
    ezdxf renderes ellipses as polylines. The polyline is broken up
    into it's individual points and lines are drawn from point to 
    point. If by rounding the two sets of points making the next 
    line are the same, the line is skipped. 
    '''
    
def makeDrill(e):
    drillDia = str(round(e.dxf.radius * 2, 3))
    centerX = str(round(e.dxf.center[0], 3))
    centerY = str(round(e.dxf.center[1], 3))
    drillOutput = ('HOLE {} ({} {})\n').format(drillDia, centerX, centerY)
    file.write(drillOutput)
    if debugMode == 1:
        print drillOutput,

def convertEntities(modelspace):
    for entity in modelspace:
        if entity.dxftype() == 'LINE':
            makeLine(entity)
        elif entity.dxftype() == 'CIRCLE':
            if entity.dxf.radius <= drillThreshold / 2:
                makeDrill(entity)
            else:
                makeCircle(entity)
        elif entity.dxftype() == 'ARC':
            makeArc(entity)
        elif entity.dxftype() == 'POLYLINE':
            makePoly(entity)

with open(outputFilename, 'w') as file:
    setupScript()
    convertEntities(modelspace)
