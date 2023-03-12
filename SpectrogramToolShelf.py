# ------------------------------------------------------------------------
#    Header Stuff
# ------------------------------------------------------------------------
bl_info = {
    "name": "Spectrogram Visualizer Addon",
    "description": "Utility to assist using Audvis to create 3D spectrograms",
    "author": "2023 Astrid Alaniz",
    "version": (0, 2, 1),
    "blender": (3, 5, 0),
    "location": "3D View > Spectrogram",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "alaniz.astrid@gmail.com",
    "tracker_url": "",
    "category": "Development"
}
# ------------------------------------------------------------------------
#    Script
# ------------------------------------------------------------------------
import bpy
import os

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
# ------------------------------------------------------------------------
#    Helper Functions
# ------------------------------------------------------------------------
def get_obj(context):
    return bpy.data.objects["Spectrogram Visualizer"]

def remap( x, oMin, oMax, nMin, nMax ):

    #check reversed input range
    reverseInput = False
    oldMin = min( oMin, oMax )
    oldMax = max( oMin, oMax )
    if not oldMin == oMin:
        reverseInput = True

    #check reversed output range
    reverseOutput = False
    newMin = min( nMin, nMax )
    newMax = max( nMin, nMax )
    if not newMin == nMin :
        reverseOutput = True

    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result
# ------------------------------------------------------------------------
#    Callbacks
# ------------------------------------------------------------------------
def update_wave_speed(self, context):
    n_h = remap(context.scene.spectrum_tool_props.wave_speed, 0.0, 1.0, 2048.0, 0.0)
    context.scene.audvis.spectrogram.height = round(n_h)
def update_wave_height(self, context):
    get_obj(context).modifiers["SpectrumVisualizer"]["Input_14"] = context.scene.spectrum_tool_props.wave_height
    get_obj(context).data.update()
def update_base_height(self, context):
    get_obj(context).modifiers["SpectrumVisualizer"]["Input_12"] = context.scene.spectrum_tool_props.base_height
    get_obj(context).data.update()
def update_resolution(self, context):
    get_obj(context).modifiers["SpectrumVisualizer"]["Input_3"] = context.scene.spectrum_tool_props.resolution
    get_obj(context).data.update()
def update_smooth(self, context):
    get_obj(context).modifiers["SpectrumVisualizer"]["Input_9"] = context.scene.spectrum_tool_props.smooth
    get_obj(context).data.update()
def update_zoom(self, context):
    get_obj(context).modifiers["SpectrumVisualizer"]["Input_13"] = context.scene.spectrum_tool_props.zoom
    get_obj(context).data.update()
def update_fade(self, context):
    get_obj(context).modifiers["SpectrumVisualizer"]["Input_15"] = context.scene.spectrum_tool_props.fade
    get_obj(context).data.update()
def update_freq_slide(self, context):
    get_obj(context).modifiers["SpectrumVisualizer"]["Input_18"] = context.scene.spectrum_tool_props.freq_slide
    get_obj(context).data.update()
def update_time_slide(self, context):
    get_obj(context).modifiers["SpectrumVisualizer"]["Input_19"] = context.scene.spectrum_tool_props.time_slide
    get_obj(context).data.update()
def update_base_gain(self, context):
    get_obj(context).modifiers["SpectrumVisualizer"]["Input_24"] = context.scene.spectrum_tool_props.base_gain
    get_obj(context).data.update()
# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------
class SpectrumToolProps(PropertyGroup):
    wave_speed: FloatProperty(
        name = "Wave Speed",
        description="How quickly sound travels across the surface. This impacts performance when speed is very low.",
        default = 0.9,
        min = 0.0,
        max = 1.0,
        update = update_wave_speed
        )
    wave_height: FloatProperty(
        name = "Wave Height",
        description="How tall the waves rise above the surface",
        default = 1,
        min = 0.0,
        update = update_wave_height
        )
    base_height: FloatProperty(
        name = "Base Height",
        description="Height of the base of the object",
        default = 0.2,
        min = 0.02,
        max = 10.0,
        update = update_base_height
        )
    resolution: IntProperty(
        name = "Resolution",
        description="Detail of the mesh geometry. Try to reduce smoothing before adjusting this.",
        default = 64,
        min = 2,
        max = 256,
        update = update_resolution
        )
    smooth: FloatProperty(
        name = "Smoothing",
        description="How much to smooth out the waves",
        default = 0.5,
        min = 0.0,
        max = 1.0,
        update = update_smooth
        )
    zoom: FloatProperty(
        name = "Zoom",
        description="How much to shrink down the waves so they don't fill up the whole surface",
        default = 1.0,
        min = 0.1,
        max = 10.0,
        update = update_zoom
        )
    fade: FloatProperty(
        name = "Fade Radius",
        description="Controls waves fading out and becoming flat.",
        default = 1.0,
        min = 0.1,
        max = 2.0,
        update = update_fade
        )
    freq_slide: FloatProperty(
        name = "Frequency Slide",
        description="Move the shape along frequency axis.",
        default = 0.0,
        min = -10.0,
        max = 10.0,
        update = update_freq_slide
        )
    time_slide: FloatProperty(
        name = "Time Slide",
        description="Move the shape along time axis.",
        default = 0.0,
        min = -10.0,
        max = 10.0,
        update = update_time_slide
        )
    base_gain: FloatProperty(
        name = "Audio Gain",
        description="Makes quiet sounds louder. Try to adjust this before the Wave Height.",
        default = 0.5,
        min = 0.0,
        max = 0.999,
        update = update_base_gain
        )
    output_path: StringProperty(
        name = "Output Directory",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )
    obj_name: StringProperty(
        name = "Object Name",
        description="Name of working object",
        default="Spectrogram Visualizer",
        )
# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------
class SpectrumTool_OT_DebugUnregister(Operator):
    bl_label = "Unregister Addon"
    bl_idname = "st.debug_unregister"

    def execute(self, context):
        scene = context.scene
        mytool = scene.spectrum_tool_props
        unregister()
        return {'FINISHED'}

class SpectrumTool_OT_ExportMesh(Operator):
    bl_label = "Export Mesh"
    bl_idname = "st.export_mesh"

    def execute(self, context):
        scene = context.scene
        mytool = scene.spectrum_tool_props
        ob = get_obj(context)
        ob.select_set(True)
        bpy.ops.export_scene.obj(
             filepath=bpy.path.abspath(os.path.join(mytool.output_path, mytool.obj_name + '.obj')),
             check_existing=True,
             axis_forward='-Z',
             axis_up='Y',
             filter_glob="*.obj;*.mtl",
             use_selection=True,
             use_animation=False,
             use_mesh_modifiers=True,
             use_edges=True,
             use_smooth_groups=False,
             use_smooth_groups_bitflags=False,
             use_normals=True,
             use_uvs=True,
             use_materials=True,
             use_triangles=False,
             use_nurbs=False,
             use_vertex_groups=False,
             use_blen_objects=True,
             group_by_object=False,
             group_by_material=False,
             keep_vertex_order=False,
             global_scale=1,
             path_mode='AUTO'
            )
        return {'FINISHED'}
# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------
class SpectrumTool_PT_MainPanel(Panel):
    bl_label = "Spectrogram Settings"
    bl_idname = "SpectrumToolPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Spectrogram"
    bl_context = "objectmode"

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        stprops = scene.spectrum_tool_props

        #addon controls
        layout.label(text="Audio Settings")
        layout.prop(stprops, "wave_speed")
        layout.prop(stprops, "base_gain")

        layout.label(text="Size Settings")
        layout.prop(stprops, "wave_height")
        layout.prop(stprops, "base_height")

        layout.label(text="Position Adjustment")
        layout.prop(stprops, "zoom")
        layout.prop(stprops, "freq_slide")
        layout.prop(stprops, "time_slide")

        layout.label(text="Quality Adjustment")
        layout.prop(stprops, "smooth")
        layout.prop(stprops, "fade")

        layout.label(text="Mesh Settings")
        layout.prop(stprops, "resolution")
        layout.prop(stprops, "output_path")
        layout.operator("st.export_mesh")

        layout.label(text="Debug")
        layout.operator("st.debug_unregister")

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    SpectrumToolProps,
    SpectrumTool_OT_DebugUnregister,
    SpectrumTool_OT_ExportMesh,
    SpectrumTool_PT_MainPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.spectrum_tool_props = PointerProperty(type=SpectrumToolProps)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.spectrum_tool_props


if __name__ == "__main__":
    register()
