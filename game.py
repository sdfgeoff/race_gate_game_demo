import bge
import math
import mathutils
import trail
import time

import vehicle

def start(cont):
    if "GAME" not in cont.owner:
        cont.owner["GAME"] = Game(cont.owner.scene)
    else:
        cont.owner["GAME"].update()



def get_key(key_str):
    key_code = bge.events.__dict__[key_str]
    return key_code in bge.logic.keyboard.active_events







class Game:
    def __init__(self, scene):
        self.scene = scene
        self.environment = Environment(scene.objects["EnvironmentRoot"])
        self.terrain = Terrain(scene.objects["TerrainRoot"])
        
        self.trail_manager = trail.TrailManager(self.scene)
        
        self.player = self.create_vehicle()
        self.player.set_as_camera()
        self.player.set_position([0,0,1250])
        
        self.enemies = [
            self.create_vehicle(),
            self.create_vehicle(),
            self.create_vehicle(),
            self.create_vehicle(),
            self.create_vehicle(),
            self.create_vehicle(),
            self.create_vehicle(),
            self.create_vehicle(),
        ]
        for e_id, enemy in enumerate(self.enemies):
            enemy.set_position([
                (e_id + 1) * 30.0,
                (e_id + 1) * 30.0,
                1250,
            ])
            enemy.set_color(e_id / len(self.enemies))
        
        bge.logic.mouse.position = (0.5, 0.5)
    
    def update(self):
        
        mouse_pos = bge.logic.mouse.position
        bge.logic.mouse.position = (0.5, 0.5)
        
        pan = (0.5 - mouse_pos[0]) * 20.0
        tilt = (0.5 - mouse_pos[1]) * 20.0
        roll = get_key("EKEY") - get_key("QKEY")
        thrust = 0.5
        
        if abs(pan) < 10/bge.render.getWindowWidth():
            pan = 0.0
        if abs(tilt) < 10/bge.render.getWindowHeight():
            tilt = 0.0
        self.player.set_control(thrust, mathutils.Vector([pan, tilt, roll]))
        
        self.environment.update()
        self.player.update()
        
        for e_id, enemy in enumerate(self.enemies):
            pan = math.sin(time.time() + e_id) * -0.05
            tilt = math.cos(time.time() + e_id) * -0.02
            enemy.set_control(0.48, mathutils.Vector([pan,tilt,0]))
            enemy.update()

        
        self.trail_manager.update(0.016)

    def create_vehicle(self):
        new_vehicle = vehicle.Vehicle(self.scene.addObject("VehicleRoot"))
        
        trail = self.trail_manager.attach_trail(
            new_vehicle.get_trail_attach_point(),
            10.0,
            10.0,
            (1.0, 1.0, 0.0, 0.0)
        )
        new_vehicle.set_trail(trail)
        
        return new_vehicle




class Environment:
    def __init__(self, root_obj):
        self.obj = root_obj
        
        self.sun = root_obj.childrenRecursive["Sun"]
        self.skylight = root_obj.childrenRecursive["SkyLight"]
        self.skydome = root_obj.childrenRecursive["SkyDome"]
    
    def update(self):
        """ Move the skydome to be over the active camera """
        active_camera = self.obj.scene.active_camera
        self.obj.worldPosition.xy = active_camera.worldPosition.xy
        active_camera.near = 0.1
        active_camera.far = 26000.0



class Terrain:
    def __init__(self, root_obj):
        self.obj = root_obj
        self.land = root_obj.childrenRecursive["Land"]
        
        mesh = self.land.meshes[0]
        mat_index = 0
          
        for vert_index in range(mesh.getVertexArrayLength(mat_index)):
             vertex = mesh.getVertex(mat_index, vert_index)
             # Do something with vertex here...
             # ... eg: color the vertex red.
             xyz = vertex.getXYZ()
             xyz.z = math.sin(xyz.y) + math.cos(xyz.x)
             vertex.setXYZ(xyz)
    
