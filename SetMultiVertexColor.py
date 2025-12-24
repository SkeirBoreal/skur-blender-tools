bl_info = {
    "name": "Set Vertex Color on Multiple Objects",
    "author": "Skeir Boreal",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object Mode > Object Menu",
    "description": "Sets the vertex color for all selected objects.",
    "category": "Object",
}

import bpy

class SetMultiObjectVertexColor(bpy.types.Operator):
    """Sets the vertex color for all selected mesh objects"""
    bl_idname = "object.set_multi_vertex_color"
    bl_label = "Set Vertex Color on Selected"
    bl_options = {'REGISTER', 'UNDO'}

    # properties appear in "redo last" panel
    color: bpy.props.FloatVectorProperty(
        name="Color",
        description="The color to apply to the vertices",
        subtype='COLOR',
        default=(1.0, 0.0, 0.0, 1.0), # // default to pure red
        min=0.0,
        max=1.0,
        size=4
    )

    layer_name: bpy.props.StringProperty(
        name="Layer Name",
        description="The name of the vertex color layer to edit or create",
        default="Attribute"
    )

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected.")
            return {'CANCELLED'}

        modified_count = 0

        for obj in selected_objects:
            if obj.type != 'MESH':
                continue

            mesh = obj.data
            
            # prevents accidentally replacing old layers
            if self.layer_name not in mesh.vertex_colors:
                mesh.vertex_colors.new(name=self.layer_name)
            
            color_layer = mesh.vertex_colors[self.layer_name]

            for i in range(len(color_layer.data)):
                color_layer.data[i].color = self.color
            
            modified_count += 1

        self.report({'INFO'}, f"Set vertex color on {modified_count} objects.")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SetMultiObjectVertexColor.bl_idname)

def register():
    bpy.utils.register_class(SetMultiObjectVertexColor)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SetMultiObjectVertexColor)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
