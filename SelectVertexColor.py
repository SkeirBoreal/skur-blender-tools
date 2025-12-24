bl_info = {
    "name": "Select by Vertex Color",
    "author": "Skeir Boreal",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Edit Mode > Select Menu",
    "description": "Selects faces based on their vertex color value.",
    "category": "Selection",
}

import bpy
import bmesh

class SelectVertexColor(bpy.types.Operator):
    """Selects faces where the vertex color is less than a threshold"""
    bl_idname = "mesh.select_by_vertex_color"
    bl_label = "Select by Vertex Color"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # --- settings ---
        COLOR_LAYER_NAME = "Attribute" 
        CHANNEL_INDEX = 0 
        THRESHOLD = 0.4 

        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        color_layer = bm.loops.layers.color.get(COLOR_LAYER_NAME)

        if color_layer is None:
            self.report({'ERROR'}, f"Vertex color layer '{COLOR_LAYER_NAME}' not found.")
            return {'CANCELLED'}
        
        for f in bm.faces:
            f.select = False

        for f in bm.faces:
            should_select_face = False
            for loop in f.loops:
                color = loop[color_layer]
                if color[CHANNEL_INDEX] < THRESHOLD:
                    should_select_face = True
                    break
            
            if should_select_face:
                f.select = True

        bmesh.update_edit_mesh(me)
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SelectByVertexColor.bl_idname)

def register():
    bpy.utils.register_class(SelectByVertexColor)
    bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SelectByVertexColor)
    bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)

if __name__ == "__main__":
    register()