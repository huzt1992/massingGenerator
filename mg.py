from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import scriptcontext as sc
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import Rhino.DocObjects as rd
doc = Rhino.RhinoDoc.ActiveDoc


construction = sc.sticky["construction"] 
helper = sc.sticky["helper"] 
 
    
class MyComponent(component):
    
    def RunScript(self, x, y):


    
        class Build():                   
                                             
            def __init__(self, curveObject, height, base_height, st):
                self.curve = curveObject.Geometry
                self.height = height
                self.base_height = base_height
                self.st = st
                self.top = st*height+base_height
                self.building = self.buildWhole()
                
            
            def buildWhole(self):
                building = []
                for i in range(self.st):
                    building.extend(self.buildStorey(i))
                return building
             
            def buildStorey(self, i):
                z_v = rg.Transform.Translation(rg.Vector3d(0,0,i*self.height+self.base_height))
                wall = self.buildWall()
                floor =self.buildFloor()
                wall.Transform(z_v)
                floor.Transform(z_v)
                return [wall,floor]
                                        
            def buildWall(self):
                return rg.Extrusion.Create(self.curve,self.height,False)
                
            def buildFloor(self):
                return rg.Brep.CreatePlanarBreps(self.curve)[0]
                
        class filterObjects():
            def __init__(self, list, curveList, textList):
                self.list = list
                self.curveList = curveList
                self.textList = textList
            
            def getList(self):
                for i in range(len(self.list)):
                    # isCurve
                    if self.list[i].ObjectType== Rhino.DocObjects.ObjectType.Curve:
                        self.curveList.append(self.list[i])
                    # isAnnotation
                    elif self.list[i].ObjectType == Rhino.DocObjects.ObjectType.Annotation:
                        self.textList.append(self.list[i])

        class getSTDict:
            def __init__(self,curveObjects,testObjects):
                self.curveList = helper.convertToGeometry(curveObjects)
                self.textList = helper.convertToGeometry(testObjects)
                
            def getStdict(self):
                self.curveList=self.sortCurveList()                
                #left shit list
                curveList2 = self.rightShiftList()
                #get centers list
                centers = self.getCenters()
                st_dict = {}
                seen = set()
                print(len(centers))
                for i in range(len(self.curveList)):
                    crv1 = self.curveList[i]
                    crv2 = curveList2[i]
                    for j in range(len(centers)):
                        # Create flat plane
                        plane = rg.Plane(centers[j],rg.Vector3d.ZAxis)
                        # Project the curves onto the plane
                        crv1 = rg.Curve.ProjectToPlane(crv1, plane)
                        # Not the top outline
                        if not(crv2 == None):
                            crv2 = rg.Curve.ProjectToPlane(crv2, plane)
                            if not(j in seen) and crv1.Contains(centers[j], plane) == rg.PointContainment.Inside and \
                                    crv2.Contains(centers[j], plane) == rg.PointContainment.Outside:  
#                                    print("add",self.curveList[i].GetLength(),centers[j],self.textList[j].Text)
                                    st_dict[self.curveList[i]]=self.textList[j].Text
                                    seen.add(j)
                                    break
                        else:
                            if crv1.Contains(centers[j], plane) == rg.PointContainment.Inside:  
                                    st_dict[self.curveList[i]]=self.textList[j].Text
                                    
                print(len(seen))
                for st in st_dict:
                    print(st.GetLength(),st_dict[st])
                return st_dict
                
             
            def getCenters(self):
                centers = []
                for i in range(len(self.textList)):
                    centers.append(self.textList[i].GetBoundingBox(True).Center)
                return centers
             
            def rightShiftList(self):
                list = []
                for i in range(len(self.curveList)):
                    if(i == 0):
                         list.append(None)
                    else:
                        list.append(self.curveList[i-1]) 
                return list
            
            
            # this sort function is not entirely correct!
            def curve_length(self,crv):
                return crv.GetLength() 
            def sortCurveList(self):
                return sorted(self.curveList,key = self.curve_length) 
                  

        curveObjects = []
        textObjects = []
        
        filter = filterObjects(x,curveObjects,textObjects)
        filter.getList()
        

        getStDict= getSTDict(curveObjects,textObjects);
        st_dict = getStDict.getStdict()

##       curve extrusion test
#        curveObject =curveList[0] 
#        build= Build(curveObject,2950,10000,100)
#        return build.building
       

##       textObject test
#        textObject = textList[0]
#        # get text string
#        print(textObject.Geometry.Text)
#        
#        # find the center of textObject: Point3D
#        center = textObject.Geometry.GetBoundingBox(True).Center
#        print(center)


##      Determine whether point is in two enclosed
#        crv1 = curveList[0].Geometry
#        crv2 = curveList[1].Geometry
#        point1 = center
#        # Create flat plane
#        plane = rg.Plane(point1,rg.Vector3d.ZAxis)
#        
#        # Project the curves onto the plane
#        proj_crv1 = rg.Curve.ProjectToPlane(crv1, plane)
#        proj_crv2 = rg.Curve.ProjectToPlane(crv2, plane)
#        
#        # Check if point1 is inside the enclosed area between the curves
#        if proj_crv1.Contains(point1, plane) == rg.PointContainment.Inside and \
#                proj_crv2.Contains(point1, plane) == rg.PointContainment.Outside:
#            a = "Point is inside enclosed area"
#        else:
#            a = "Point is outside enclosed area"
#
#        print(a)
#        return [proj_crv1, proj_crv2, point1]



