import Rhino
import scriptcontext
import System.Guid
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import scriptcontext as sc


class Build():                                                
    def __init__(self, base_height=0):
        self.base_height = base_height

    def buildStorey(self,curve, height,i):
        z_v = rg.Transform.Translation(rg.Vector3d(0,0,i*height+self.base_height))
        wall = self.buildWall(curve,height)
        floor =self.buildFloor(curve)
        wall.Transform(z_v)
        floor.Transform(z_v)
        return [wall,floor]
                
    def buildWall(self,curve,height):
        return rg.Extrusion.Create(curve,height,False)

    def buildFloor(self,curve):
        return rg.Brep.CreatePlanarBreps(curve)[0]


def AddCircle():
    center = Rhino.Geometry.Point3d(0, 0, 0)
    radius = 10.0
    c = Rhino.Geometry.Circle(center, radius)
    if sc.doc.Objects.AddCircle(c) != System.Guid.Empty:
        rs.AddCurve(c)
#        sc.doc.Views.Redraw()
#        return Rhino.Commands.Result.Success
    return Rhino.Commands.Result.Failure



if __name__ == "__main__":
    AddCircle()
    print("h")