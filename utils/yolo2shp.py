import os
import gdal
import geopandas as gpd
from shapely.geometry import box

os.environ['PROJ_LIB'] = r'D:\Users\12100\anaconda3\envs\yolov7\Lib\site-packages\pyproj\proj_dir\share\proj'

# 定义一个函数，将YOLO坐标映射为地理坐标
def yolo_to_geo(x_center_norm, y_center_norm, width_norm, height_norm, image_width, image_height, geo_transform):
    # 坐标反归一化
    x_center = x_center_norm * image_width
    y_center = y_center_norm * image_height
    width = width_norm * image_width
    height = height_norm * image_height

    # 在此处执行坐标映射，需要根据具体的地理信息和地理变换参数来完成
    x_geo = geo_transform[0] + x_center * geo_transform[1]
    y_geo = geo_transform[3] + y_center * geo_transform[5]
    width_geo = width * geo_transform[1]
    height_geo = height * geo_transform[5]
    '''
        geoTransform[0] / * top left x 左上角x坐标 * /
        geoTransform[1] / * w - e pixel resolution 东西方向上的像素分辨率 * /
        geoTransform[2] / * rotation, 0 if image is "north up" 如果北边朝上，地图的旋转角度 * /
        geoTransform[3] / * top left y 左上角y坐标 * /
        geoTransform[4] / * rotation, 0 if image is "north up" 如果北边朝上，地图的旋转角度 * /
        geoTransform[5] / * n - s pixel resolution 南北方向上的像素分辨率 * /
    '''
    return x_geo, y_geo, width_geo, height_geo


# 指定YOLO标签文件夹和输出SHP文件名
yolo_labels_folder = '../runs/detect/exp3/labels'  # 替换为YOLO标签文件夹的路径
output_folder = '../runs/detect/exp3/shp_output'  # 输出SHP文件的路径

os.makedirs(output_folder, exist_ok=True)  # 创建输出文件夹

# 循环处理每个yolo标签文件
for file_name in os.listdir(yolo_labels_folder):
    if file_name.endswith('.txt'):
        file_path = os.path.join(yolo_labels_folder, file_name)

        with open(file_path, 'r') as file:
            lines = file.readlines()
            gdf_list = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 6:
                    class_id, x_center, y_center, width, height, confidence = map(float, parts[:6])
                    image_name = file_name.replace('.txt', '.tif')
                    image_path = os.path.join(r'E:\dataset\sample_process\test', image_name)  # 图像文件的路径

                    # 使用GDAL打开TIFF图像以获取地理信息和地理变换参数
                    ds = gdal.Open(image_path)
                    if ds is not None:
                        projection_info = ds.GetProjection()
                        geo_transform = ds.GetGeoTransform()

                        # 映射YOLO坐标为地理坐标
                        x_geo, y_geo, width_geo, height_geo = yolo_to_geo(x_center, y_center, width, height, 512, 512,
                                                                          geo_transform)

                        # 创建Shapely几何对象（矩形框）
                        geom = box(x_geo - width_geo / 2, y_geo - height_geo / 2, x_geo + width_geo / 2,
                                   y_geo + height_geo / 2)

                        # 将要素添加到GeoDataFrame
                        gdf_list.append({'class_id': class_id, 'confidence': confidence, 'geometry': geom})

                # 将要素列表转换为GeoDataFrame
                gdf = gpd.GeoDataFrame(gdf_list, crs=projection_info)  # 添加地理坐标系信息

                # 将GeoDataFrame保存为SHP文件
                output_shp_file = os.path.join(output_folder, file_name.replace('.txt', '.shp'))
                gdf.to_file(output_shp_file)

                # 打印GeoDataFrame
                print(gdf)

print("Processing completed.")
