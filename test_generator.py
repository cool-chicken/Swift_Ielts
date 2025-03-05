import pdfplumber
from PIL import Image
from pdf2image import convert_from_path
import os


def extract_writing_section(pdf_path, output_folder):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # 获取页面原始尺寸
            page_width = page.width
            page_height = page.height

            text = page.extract_text()
            if "WRITING TASK 1" in text:
                # 使用字符定位精确获取坐标
                task1_chars = [char for char in page.chars if "WRITING TASK 1" in char["text"]]
                end_chars = [char for char in page.chars if "Write at least 150 words." in char["text"]]

                if task1_chars and end_chars:
                    # 获取实际坐标
                    y_start = min([char["top"] for char in task1_chars])
                    y_end = max([char["bottom"] for char in end_chars])

                    # 扩展截取区域（向下延伸200像素）
                    crop_area = (
                        50,  # 左边距
                        y_start - 20,  # 上边距
                        page_width - 50,  # 右边距
                        min(y_end + 200, page_height)  # 下边距
                    )

                    # 使用更高分辨率渲染（需要安装pdf2image）
                    images = convert_from_path(
                        pdf_path,
                        dpi=300,
                        first_page=page_num + 1,
                        last_page=page_num + 1
                    )

                    # 裁剪并保存图片
                    if images:
                        img = images[0].crop(crop_area)
                        img_path = os.path.join(output_folder, f"Ielts_{page_num}.png")
                        img.save(img_path,
                                 dpi=(300, 300),  # 保持高DPI元数据
                                 quality=100,  # 最高质量
                                 optimize=True,  # 启用PNG优化
                                 compress_level=9  # 最高压缩级别
                                 )




# 示例调用
pdf_folder = "/Users/rachelwu/ielts_platform/database/test"
output_folder = "/Users/rachelwu/ielts_platform/database/writing_tasks"
# Ensure the pdf_folder exists
os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

for pdf_file in os.listdir(pdf_folder):
    pdf_path = os.path.join(pdf_folder, pdf_file)
    extract_writing_section(pdf_path, output_folder)