import os
import urllib.request

# 定义文件夹路径和下载保存路径
folder_path = "./ori"
save_path = "./pdf"

# 创建保存路径文件夹（如果不存在）
os.makedirs(save_path, exist_ok=True)

# 遍历文件夹中的所有txt文件
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        # 打开文件读取第一行
        with open(file_path, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
        url = first_line.split(" ")[1]
        urllib.request.urlretrieve(url, f"./pdf/{filename}_content.pdf")
        # # 检查第一行是否为URL格式
        # if first_line.startswith("GET "):
        #     # 提取URL
        #     url = first_line.split(" ")[1]
        #     print(url)
            
        #     try:
        #         # 发送HTTP请求
        #         response = requests.get(url)
        #         response.raise_for_status()  # 检查HTTP请求是否成功
                
        #         # 保存内容到文件
        #         save_file_path = os.path.join(save_path, f"{filename}_content.pdf")
        #         with open(save_file_path, "wb") as output_file:
        #             output_file.write(response.content)
                
        #         print(f"下载成功: {url}")
        #     except Exception as e:
        #         print(f"下载失败: {url}, 错误: {e}")

