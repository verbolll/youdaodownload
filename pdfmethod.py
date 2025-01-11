import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger

def split_pdf(file_path, pages_per_file):
    # 打开原始PDF文件
    with open(file_path, 'rb') as infile:
        reader = PdfReader(infile)
        total_pages = len(reader.pages)

        # 创建与原文件同名的新文件夹
        file_dir, file_name = os.path.split(file_path)
        file_base, file_ext = os.path.splitext(file_name)
        new_folder_path = os.path.join(file_dir, file_base)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # 分割PDF
        for start_page in range(0, total_pages, pages_per_file):
            writer = PdfWriter()
            end_page = min(start_page + pages_per_file, total_pages)

            for page in range(start_page, end_page):
                writer.add_page(reader.pages[page])

            output_filename = os.path.join(new_folder_path, f"{start_page // pages_per_file + 1}{file_ext}")

            with open(output_filename, 'wb') as outfile:
                writer.write(outfile)

def get_num_pages(file_path):
    reader = PdfReader(file_path)
    if reader.is_encrypted:
        reader.decrypt('')
    page_num = len(reader.pages)
    return page_num
class AppendPdf:
    def __init__(self, appendPdflist, name):
        self.appendPdflist = appendPdflist
        self.name = name
        self.merger = PdfMerger()
    def merger_pdf(self):
        for appendPdf in self.appendPdflist:
            self.merger.append(appendPdf)
    def returnPdf(self):
        self.merger.write('Zh' + str(self.name) + '.pdf')
        self.merger.close()

# # 使用示例
# split_pdf(r"UAV path planning algorithm based on improved artificial potential field method.pdf", 1)  # 这里5是每个分割文件的页面数