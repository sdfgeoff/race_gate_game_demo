import bpy
import math
import mathutils


class Vehicle:
    def __init__(self, root_obj):
        self.obj = root_obj
        print(self.obj.childrenRecursive)
        self.camera = self.obj.childrenRecursive["VehicleCamera"]
        
        self.angular_input = mathutils.Vector([0,0,0])
        self.thrust = 0.0
        
        self.trail = None
        
    def set_trail(self, trail):
        self.trail = trail
        
    def set_as_camera(self):
        self.camera.scene.active_camera = self.camera
    
    def set_position(self, position):
        self.obj.worldPosition = position
        
        if self.trail != None:
            self.trail.clear()
    
    def set_control(self, thrust, angular):
        self.thrust = thrust
        self.angular_input = angular
    
    def update(self):
        # Antigravity
        self.obj.applyForce([0,0,9.8])
        
        # Engine thrust
        self.obj.applyForce([0, self.thrust*10000.0, 0], True)
        
        # Drag
        self.obj.applyForce(self.obj.worldLinearVelocity * -10, False)
        self.obj.applyTorque(self.obj.worldAngularVelocity * -50, False)
        
        # Steering
        angular_lookahead = self.obj.localAngularVelocity * 0.1 + self.angular_input.yzx * 0.05
        
        angular_lookahead.y -= angular_lookahead.z * 0.5
        angular_lookahead *= 0.2
        self.camera.localOrientation = [
            1.5 + angular_lookahead.x, 
            0 + angular_lookahead.y,
            -1.5 + angular_lookahead.z
        ]
        self.obj.applyTorque(self.angular_input.yzx * 500.0, True)
        
        if self.trail != None:
            self.trail.set_intensity(self.thrust)
    
    def set_color(self, hue):
        r = math.sin((hue + 0.0) * 3.14)
        g = math.sin((hue + 0.3) * 3.14)
        b = math.sin((hue + 0.6) * 3.14)
        color = [r, g, b, 1.0]
        self.obj.color = color
        
        if self.trail is not None:
            self.trail.set_color(color)


    def get_trail_attach_point(self):
        return self.obj.childrenRecursive["EngineFlare"]
