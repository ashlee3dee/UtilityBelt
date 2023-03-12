bl_info = {
    "name": "Project Manager",
    "author": "Dylan S. Swiggett",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Project Manager",
    "description": "Create and manage project folders",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
}

import bpy
import os

class ProjectManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    projects_directory: bpy.props.StringProperty(
        name="Projects Directory",
        subtype='DIR_PATH',
        default=os.path.join(os.path.expanduser("~"), "Documents", "Blender Projects")
    )

    default_folders: bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup,
        name="Default Folders"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "projects_directory")
        layout.label(text="Default Folders")
        for folder in self.default_folders:
            row = layout.row()
            row.prop(folder, "name", text="")
            row.operator("project_manager.remove_default_folder", text="", icon="X")

        layout.operator("project_manager.add_default_folder", text="Add Folder")

class ProjectManagerAddDefaultFolder(bpy.types.Operator):
    bl_idname = "project_manager.add_default_folder"
    bl_label = "Add Default Folder"

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        prefs.default_folders.add()
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
        layout.prop(prefs, "projects_directory")
        layout.prop(context.scene, "project_manager_new_project_name")
        layout.operator("project_manager.create_project", text="Create Project")
        layout.label(text="Projects")
        for project in os.listdir(prefs.projects_directory):
            layout.operator("project_manager.open_project", text=project).project_name = project

class ProjectManagerCreateProject(bpy.types.Operator):
    bl_idname = "project_manager.create_project"
    bl_label = "Create Project"

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        project_name = context.scene.project_manager_new_project_name
        project_path = os.path.join(prefs.projects_directory, project_name)
        os.mkdir(project_path)
        for folder in prefs.default_folders:
            os.mkdir(os.path.join(project_path, folder.name))
        return {'FINISHED'}

class ProjectManagerOpenProject(bpy.types.Operator):
    bl_idname = "project_manager.open_project"
    bl_label = "Open Project"

    project_name: bpy.props.StringProperty()

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        project_path = os.path.join(prefs.projects_directory, self.project_name)
        bpy.ops.wm.path_open(filepath=project_path)
        return {'FINISHED'}

classes = (
    ProjectManagerPreferences,
    ProjectManagerAddDefaultFolder,
    ProjectManagerRemoveDefaultFolder,
    ProjectManagerPanel,
    ProjectManagerCreateProject,
    ProjectManagerOpenProject
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.project_manager_new_project_name = bpy.props.StringProperty()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.project_manager_new_project_name

if __name__ == "__main__":
    register()
