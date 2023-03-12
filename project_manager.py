bl_info = {
    "name": "Project Manager",
    "author": "Co-Written by Astrid Alaniz and GPT-Codex",
    "version": (0, 0, 2),
    "blender": (3, 4, 1),
    "location": "View3D",
    "description": "Simply manage projects with Blender",
    "warning": "",
    "wiki_url": "",
    "category": "Development",
}

import bpy
import os
import glob
import datetime
import time

# bytes pretty-printing
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]


def pretty_size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix

class ProjectManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    projects_directory: bpy.props.StringProperty(
        name="Projects Directory",
        subtype='DIR_PATH',
        default=os.path.join(os.path.expanduser("~"), "Documents", "Blender Projects")
    )

    blendfile_directory: bpy.props.StringProperty(
        name="Blend File",
        #subtype='DIR_PATH',
        default="blendfiles"
    )

    default_folders: bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "projects_directory")
        #layout.prop(self, "blendfile_directory")
        layout.label(text="Default Folders:")
        for index, folder in enumerate(self.default_folders):
            row = layout.row()
            row.prop(folder, "name", text="")
            row.operator("project_manager.remove_default_folder", text="", icon="X").index=index
        layout.operator("project_manager.add_default_folder", text="Add Folder")

class ProjectManagerAddDefaultFolder(bpy.types.Operator):
    bl_idname = "project_manager.add_default_folder"
    bl_label = "Add Default Folder"

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        folder = prefs.default_folders.add()
        folder.name = "New Folder"
        return {'FINISHED'}

class ProjectManagerRemoveDefaultFolder(bpy.types.Operator):
    bl_idname = "project_manager.remove_default_folder"
    bl_label = "Remove Default Folder"

    index: bpy.props.IntProperty()

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        prefs.default_folders.remove(self.index)
        return {'FINISHED'}

class ProjectManagerPanel(bpy.types.Panel):
    bl_idname = "project_manager.panel"
    bl_label = "Project Manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Project Manager"

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[__name__].preferences
        layout.prop(context.scene, "project_manager_new_project_name")
        layout.operator("project_manager.create_project", text="Create Project")
        layout.label(text="Projects")
        for project in os.listdir(prefs.projects_directory):
            row = layout.row()
            #row.label(text=project)
            row.operator("project_manager.report_file_info", text="", icon="INFO").project_name = project
            row.operator("project_manager.open_project_blendfile", text=project, icon="FILE_BLEND").project_name = project
            row.operator("project_manager.open_project_folder", text="", icon="FILE_FOLDER").project_name = project
            row.operator("project_manager.save_project_blendfile", text="", icon="FILE_TICK").project_name = project

class ProjectManagerCreateProject(bpy.types.Operator):
    bl_idname = "project_manager.create_project"
    bl_label = "Create Project"

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        project_name = context.scene.project_manager_new_project_name
        project_path = os.path.join(prefs.projects_directory, project_name)
        blendfile_path = os.path.join(project_path, prefs.blendfile_directory)
        os.makedirs(blendfile_path)
        for folder in prefs.default_folders:
            os.makedirs(os.path.join(project_path, folder.name))
        return {'FINISHED'}

class ProjectManagerOpenProjectFolder(bpy.types.Operator):
    bl_idname = "project_manager.open_project_folder"
    bl_label = "Open Project Folder"

    project_name: bpy.props.StringProperty()

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        project_path = os.path.join(prefs.projects_directory, self.project_name)
        bpy.ops.wm.path_open(filepath=project_path)
        return {'FINISHED'}

class ProjectManagerOpenProjectBlendfile(bpy.types.Operator):
    bl_idname = "project_manager.open_project_blendfile"
    bl_label = "Open Project Blendfile"

    project_name: bpy.props.StringProperty()

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        project_path = os.path.join(prefs.projects_directory, self.project_name)
        blendfile_path = os.path.join(project_path, prefs.blendfile_directory)
        blendfiles = glob.glob(os.path.join(blendfile_path, "*.blend"))
        blendfiles.sort(key=os.path.getmtime)
        bpy.ops.wm.open_mainfile(filepath=blendfiles[-1])
        return {'FINISHED'}

class ProjectManagerSaveProjectBlendfile(bpy.types.Operator):
    bl_idname = "project_manager.save_project_blendfile"
    bl_label = "Save Project Blendfile"

    project_name: bpy.props.StringProperty()

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        project_path = os.path.join(prefs.projects_directory, self.project_name)
        blendfile_path = os.path.join(project_path, prefs.blendfile_directory)
        blendfiles = glob.glob(os.path.join(blendfile_path, "*.blend"))
        blendfiles.sort(key=os.path.getmtime)
        if len(blendfiles) > 0:
            last_blendfile = blendfiles[-1]
            last_blendfile_name = os.path.basename(last_blendfile)
            last_blendfile_name_parts = last_blendfile_name.split("_")
            last_blendfile_name_parts[-1] = last_blendfile_name_parts[-1].split(".")[0]
            last_blendfile_name_parts[-1] = str(int(last_blendfile_name_parts[-1]) + 1)
            new_blendfile_name = "_".join(last_blendfile_name_parts)
        else:
            new_blendfile_name = f'{self.project_name}.blend'
        new_blendfile_path = os.path.join(blendfile_path, new_blendfile_name)
        bpy.ops.wm.save_as_mainfile(filepath=new_blendfile_path)
        return {'FINISHED'}

class ProjectManagerReportFileInfo(bpy.types.Operator):
    """Reports general statistucs on the selected project"""
    bl_idname = "project_manager.report_file_info"
    bl_label = "Project Info Report:"

    project_name: bpy.props.StringProperty()
    project_file: bpy.props.StringProperty()
    file_size: bpy.props.StringProperty()
    edit_date: bpy.props.StringProperty()
    libs: bpy.props.CollectionProperty()
    groups: bpy.props.CollectionProperty()

    def execute(self, context):
        return {'FINISHED'}
    def invoke(self, context, event):
        prefs = context.preferences.addons[__name__].preferences
        project_path = os.path.join(prefs.projects_directory, self.project_name)
        blendfile_path = os.path.join(project_path, prefs.blendfile_directory)
        blendfiles = glob.glob(os.path.join(blendfile_path, "*.blend"))
        blendfiles.sort(key=os.path.getmtime)
        blendfile=blendfiles[-1]

        # get the file size
        self.project_name = blendfile
        self.file_size = pretty_size(os.path.getsize(blendfile))

        # get the edit date
        self.edit_date = time.ctime(os.path.getmtime(blendfile))

        # get the linked libraries
        self.libs = []
        for lib in bpy.data.libraries:
            self.libs.append(lib.filepath)

        # get the node groups
        self.groups = []
        for group in bpy.data.node_groups:
            self.groups.append(group.name)
        return context.window_manager.invoke_props_dialog(self, width = 400)
    def draw(self, context):
        layout = self.layout
        layout.label(text=f"Project Name: {self.project_name}")
        layout.label(text=f"Project File: {self.project_file}")
        layout.label(text=f"File Size: {self.file_size}")
        layout.label(text=f"Last Edit: {self.edit_date}")
        """
        if len(self.libs) > 0:

            layout.label(text=f"{len(self.libs)} Libraries:")
            for index, libs in enumerate(self.libs):
                layout.label(text=f"{index}: {libs}")
        """
        if len(self.groups) > 0:
            row = layout.row()
            row.label(text=f"{len(self.groups)} Node Groups:")
            for index, group in enumerate(self.groups):
                layout.label(text=f"{index+1}: {group}")

classes = (
    ProjectManagerPreferences,
    ProjectManagerAddDefaultFolder,
    ProjectManagerRemoveDefaultFolder,
    ProjectManagerPanel,
    ProjectManagerCreateProject,
    ProjectManagerOpenProjectFolder,
    ProjectManagerOpenProjectBlendfile,
    ProjectManagerSaveProjectBlendfile,
    ProjectManagerReportFileInfo,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.project_manager_new_project_name = bpy.props.StringProperty(name='Name', default='New Project')

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.project_manager_new_project_name

if __name__ == "__main__":
    register()
