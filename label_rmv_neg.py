import os


def process_negative_labels(folder_path):
    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)

    for file_name in file_list:
        # 检查文件扩展名是否为txt
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)

            # 读取文件内容
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # 处理文件中的负数
            processed_lines = []
            for line in lines:
                numbers = line.split()
                processed_numbers = []
                for number in numbers:

                    try:
                        number = float(number)
                        if number == 0:
                            number = int(number)
                            # print(file_name, number, ' occur err: =0')
                        if number < 0:
                            number = abs(number)  # 将负数转换为正数
                            print(file_name, number, ' occur err: < 0')
                    except ValueError:
                        pass
                    processed_numbers.append(str(number))

                processed_line = ' '.join(processed_numbers)
                processed_lines.append(processed_line)

            # 将处理后的内容写回文件
            with open(file_path, 'w') as file:
                file.write('\n'.join(processed_lines))

def process_nonnormalized_labels(folder_path):
    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)

    for file_name in file_list:
        # 检查文件扩展名是否为txt
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)

            # 读取文件内容
            with open(file_path, 'r') as file:
                lines = file.readlines()

            processed_lines = []
            for line in lines:
                numbers = line.split()
                processed_numbers = []
                for number in numbers:
                    try:
                        number = float(number)
                        if number > 1:
                            number = 1
                            print(file_name, number, ' non-normalizated !')
                    except ValueError:
                        pass
                    processed_numbers.append(str(number))

                processed_line = ' '.join(processed_numbers)
                processed_lines.append(processed_line)

            # 将处理后的内容写回文件
            with open(file_path, 'w') as file:
                file.write('\n'.join(processed_lines))

if __name__ == '__main__':
    # negative labels
    folder_path = r'./data/mydata_test/labels_json'  # 只需修改成你的txt路径
    process_nonnormalized_labels(folder_path)
    process_negative_labels(folder_path)

