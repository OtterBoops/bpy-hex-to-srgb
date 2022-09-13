bl_info = {
    "name": "Hex to sRGB",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "Object > Material Properties > Hex to sRGB",
    "description": "Converts Hex to sRGB. Does not do the linear RGB conversion. UI created by Plat#5006 on discord from the Blender community server",
    "doc_url": "https://github.com/OtterBoops/bpy-hex-to-srgb",
}

import bpy
import math

class Hex2RGB(bpy.types.Panel):
    bl_label = "Hex to sRGB"
    bl_idname = "OBJECT_PT_hex2srgb"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        scene = context.scene
        
        col = layout.column(align=True)
        
        row = col.row()
        row.prop(scene.hex2rgb_data, "input", text="Hex Value", icon="COLOR")

        col.prop(scene.hex2rgb_data, "R", slider=True)
        col.prop(scene.hex2rgb_data, "G", slider=True)
        col.prop(scene.hex2rgb_data, "B", slider=True)
        col.prop(scene.hex2rgb_data, "A", slider=True)


def hex_color_to_rgba(hex_color):
    # remove the leading '#' symbol
    if hex_color[0] == "#":
        hex_color = hex_color[1:]

    # extracting the Red color component - RRxxxx
    red = int(hex_color[:2], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_red = red / 255

    # extracting the Green color component - xxGGxx
    green = int(hex_color[2:4], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_green = green / 255


    # extracting the Blue color component - xxxxBB
    blue = int(hex_color[4:6], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_blue = blue / 255

    return tuple([srgb_red, srgb_green, srgb_blue, 1.0])


#   If you need the linear rgb for whatever reason, uncomment lines x through y.
#   Added for posteriority sake, since you already have the results in the standard color picker.

#    linear_red = convert_srgb_to_linear_rgb(srgb_red)
#    linear_green = convert_srgb_to_linear_rgb(srgb_green)
#    linear_blue = convert_srgb_to_linear_rgb(srgb_blue)

#    return tuple([srgb_red, srgb_green, srgb_blue, 1.0])

#def convert_srgb_to_linear_rgb(srgb_color_component: float) -> float:
#    """
#    Converting from sRGB to Linear RGB
#    based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
#    """
#    if srgb_color_component <= 0.04045:
#        linear_color_component = srgb_color_component / 12.92
#    else:
#        linear_color_component = math.pow((srgb_color_component + 0.055) / 1.055, 2.4)

#    return linear_color_component

def Hex2RGB_update(self, context):
    data = context.scene.hex2rgb_data
    data.R, data.G, data.B, data.A = hex_color_to_rgba(data.input)


class Hex2RgbData(bpy.types.PropertyGroup):
    input: bpy.props.StringProperty("hex_input", default="#000000", maxlen=7, update=Hex2RGB_update)
    R: bpy.props.FloatProperty(description="Red", default=0.0, soft_min = 0, soft_max = 1)
    G: bpy.props.FloatProperty(description="Green", default=0.0, soft_min = 0, soft_max = 1)
    B: bpy.props.FloatProperty(description="Blue", default=0.0, soft_min = 0, soft_max = 1)
    A: bpy.props.FloatProperty(description="Alpha", default=1.0, soft_min = 0, soft_max = 1)


classes = (
    Hex2RGB,
    Hex2RgbData
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.hex2rgb_data = bpy.props.PointerProperty(type=Hex2RgbData)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    del bpy.types.Scene.hex2rgb_data
     
if __name__ == "__main__":
    register()
