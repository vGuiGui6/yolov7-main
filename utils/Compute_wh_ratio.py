import os
import matplotlib.pyplot as plt
import numpy as np


# 读取单个YOLO标记文件
def read_yolo_labels(file_path):
    labels = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 5:
                class_id, x_center, y_center, width, height = map(float, parts[:5])

                # 检查宽度是否为零，如果是，跳过该标注框
                if width == 0:
                    continue

                labels.append((class_id, x_center, y_center, width, height))
    return labels


# 计算宽高比
def calculate_aspect_ratio(labels):
    aspect_ratios = []
    for label in labels:
        width, height = label[3], label[4]

        # 检查宽度是否为零，如果是，跳过该标注框
        if width == 0:
            continue

        aspect_ratio = height / width
        aspect_ratios.append(aspect_ratio)
    return aspect_ratios


# 统计宽高比分布
def plot_aspect_ratio_distribution(aspect_ratios):
    plt.hist(aspect_ratios, bins=20, edgecolor='k')
    plt.xlabel('Aspect Ratio (height/width)')
    plt.ylabel('Frequency')
    plt.title('Aspect Ratio Distribution')
    plt.show()


# 处理整个文件夹中的YOLO标记文件
def process_folder(folder_path):
    aspect_ratios_all = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            yolo_labels = read_yolo_labels(file_path)
            aspect_ratios = calculate_aspect_ratio(yolo_labels)
            aspect_ratios_all.extend(aspect_ratios)
    return aspect_ratios_all


# 主程序
if __name__ == '__main__':
    yolo_labels_folder = '../datasets/labels/train'  # 替换为包含多个YOLO标记文件的文件夹路径
    aspect_ratios_all_files = process_folder(yolo_labels_folder)
    print(np.mean(aspect_ratios_all_files))
    plot_aspect_ratio_distribution(aspect_ratios_all_files)
