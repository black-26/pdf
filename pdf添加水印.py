from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

def create_watermark(watermark_text):
    # 创建一个内存中的PDF文件作为水印
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 40)
    can.setFillColorRGB(1, 0, 0, alpha=0.4)  # 设置水印为红色和透明度，alpha为设置透明度

    # 获取页面宽度和高度
    width, height = A4

    # 设置水印间隔（密集水印）
    x_offset = 150  # 水印之间的水平间隔
    y_offset = 150  # 水印之间的垂直间隔
    angle = 45      # 倾斜角度

    # 绘制水印
    for x in range(0, int(width), x_offset):
        for y in range(0, int(height), y_offset):
            can.saveState()  # 保存当前状态
            can.translate(x, y)  # 移动到水印位置
            can.rotate(angle)  # 旋转
            can.drawString(0, 0, watermark_text)  # 绘制水印
            can.restoreState()  # 恢复状态

    can.save()
    packet.seek(0)
    return packet

def add_watermark(input_pdf, output_pdf, watermark_text):
    watermark_pdf = create_watermark(watermark_text)
    watermark_reader = PdfReader(watermark_pdf)
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    watermark_page = watermark_reader.pages[0]

    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    with open(output_pdf, "wb") as f_out:
        writer.write(f_out)


if __name__ == '__main__':
    # 示例用法
    input_pdf = r"文件地址.pdf"  # 输入PDF文件路径
    output_pdf = r"输出后的文件地址.pdf"  # 输出PDF文件路径
    watermark_text = "水印内容"  # 水印文本内容

    add_watermark(input_pdf, output_pdf, watermark_text)
