import bpy
import os

import math

# # 获取输入文件夹和输出文件夹的路径
input_folder = r"D:\y2-sum-intern\inputfolder\character-model\model"
output_folder = r"D:\y2-sum-intern\inputfolder\character-model\image"

# 设置渲染背景为纯白色
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
bpy.context.scene.render.image_settings.color_depth = '8'
bpy.context.scene.view_settings.view_transform = 'Standard'
bpy.context.scene.world.use_nodes = True
bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

# 清除上一份同名的图片
# for file_name in os.listdir(output_folder):
#     if file_name.endswith(".png"):
#         if file_name.startswith("some_prefix"):  # 替换 "some_prefix" 为您的文件名前缀
#             file_path = os.path.join(output_folder, file_name)
#             os.remove(file_path)


# 遍历输入文件夹中的所有文件
for file_name in os.listdir(input_folder):
    if file_name.endswith(".fbx"): # 可修改 .gltf / .fbx

        # 导入3D模型
        file_path = os.path.join(input_folder, file_name)
        bpy.ops.import_scene.fbx(filepath=file_path) # 可修改 .gltf / .fbx
        
    
        # 检测是否能加载gltf格式的文件

        # try:
        #     bpy.ops.import_scene.gltf(filepath=file_path)
        # except Exception as e:
        #     print(f"Failed to import {file_name}: {e}")
        #     continue
        
        # # 选择导入的模型对象
        model_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']


        # 调整环境光的强度
        bpy.context.scene.world.node_tree.nodes["Background"].inputs[1].default_value = 1
        
        # # 调整曝光
        bpy.context.scene.view_settings.exposure = 0

        # 选择并删除所有名称以"Light"开头的灯光对象 (防止光斑出现)
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT' and obj.name.startswith("Light"):
                bpy.context.collection.objects.unlink(obj)
                bpy.data.objects.remove(obj)
        
        for obj in model_objects:
            # 记录模型的原始尺寸
        
            # 缩放模型
            obj.scale *= 1 # 调整缩放因子，这里设置为多少倍
                     
            # # 调整模型位置（这个不能让模型整体移动，部分组织可能会掉落）
            # obj.location.x = 0  # 在X轴上向右移动2个单位
            # obj.location.y = 0  # 在Y轴上向前移动1个单位
            # obj.location.z = 0  # 在Z轴上向上移动0.5个单位
            

        # # 设置摄像机焦距以放大视图
        bpy.context.scene.camera.data.lens =302
        # 调整焦距值来放大或缩小视图P  

        # 作为模型旋转用途（注意：旋转这部分代码如果要用，可能会导致不能全部模型截图，因为会导致blender截图一半就会自动退出）
        # 设置原点到模型的几何中心
        # for obj in model_objects:
        #     bpy.context.view_layer.objects.active = obj
        #     bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
        # # # 设置轴向为X, Y, Z轴
        # for obj in model_objects:
        #     bpy.context.view_layer.objects.active = obj
        # bpy.ops.transform.rotate(value=3.14159/-2, orient_axis='X')  # 旋转90度，即π/2  3.14159/9
        # bpy.ops.transform.rotate(value=3.14159/-3, orient_axis='Y')  # 旋转90度，即π/2 3.14159/8 3.14159/20
        # bpy.ops.transform.rotate(value=3.14159/2.11, orient_axis='Z') #3.14159/6 3.14159/1.35



        # 在这里添加摄像机旋转代码（作为旋转摄像角度来观看模型）
        # bpy.context.scene.camera.rotation_euler = (3.14159/2.51713,3.14159/180, 3.14159/1)  # 旋转45度，即π/4
    
        # 定位模型（作为移动摄像机的位置，可xyz的移动-可去除加号来直接控制数值）
        # 因为有时候模型位于摄像机的后面，我们要讲摄像机旋转加位移来调整
        # bpy.context.scene.camera.location.x =51.559  
        # bpy.context.scene.camera.location.y =-6.9
        # bpy.context.scene.camera.location.z =5.68

        # 调整渲染分辨率为正方形
        bpy.context.scene.render.resolution_x = 420
        bpy.context.scene.render.resolution_y = 420

        # 渲染截图
        output_file_path = os.path.join(output_folder, file_name.replace(".gltf", ".png"))# 可修改 .gltf / .fbx
        bpy.context.scene.render.filepath = output_file_path
        bpy.ops.render.render(write_still=True)

        # 清理场景
        bpy.ops.object.select_all(action='DESELECT') 
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()
    
        