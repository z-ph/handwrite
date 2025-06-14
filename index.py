# coding: utf-8
from PIL import Image, ImageFont
from handright import Template, handwrite

# 背景图片路径
backgroundPath = "./paper/1.png"
fonts = "./fonts/SJNMDJW.ttf"  # 字体文件路径，修正路径格式
prePath='./5times paper/'
backgroundPathList = ['1.png','2.png','3.png','4.png',]  # 可选背景图片列表
# 要写的文本
text1 = '''人工智能+时代推动大学生劳动教育内容方式改革创新
         随着人工智能技术的快速发展，我们正步入一个全新的时代——人工智能+时代。这一时代的到来，不仅改变了我们的生产方式和生活方式，也对教育领域产生了深远的影响。特别是在大学生劳动教育这一领域，人工智能技术的引入，为教育内容和方式的改革创新提供了新的可能性。本文将探讨在人工智能+时代背景下，如何推动大学生劳动教育内容和方式的改革创新。
         人工智能对劳动教育的影响是深远的。它改变了劳动教育的内容，使得教育内容需要不断更新以适应时代的发展。在传统的劳动教育中，体力劳动占据了重要位置，而在人工智能时代，智力劳动和创造性劳动变得越来越重要。因此，劳动教育的内容需要增加对AI技术、编程、数据分析等方面的教育，以培养学生在未来社会中的竞争力。同时，人工智能技术的应用也改变了劳动教育方式，使得教育方式更加多样化和个性化。通过AI技术，可以实现个性化教学，根据学生的学习进度和兴趣，提供定制化的学习内容和教学方法。此外，AI还可以通过虚拟现实VR和增强现实AR技术，提供更加直观和互动的学习体验，增强学生的实践能力和创新思维。
'''
rate2=4700/1070
text3=text1
def process_text(string):
    '''
    1.保留字符串中的汉字、逗号、句号，将替他字符替换为四个或五个空格，相邻替换的空格的数量需要不一样
    2.保留换行符，连续的多个换行符合并成一个
    3.每段开头增加9个空格
    '''
    import re

    # 定义匹配汉字、逗号、句号的正则表达式
    pattern = r'[^\u4e00-\u9fa5，。、！？；：\n]+'
    
    # 用于跟踪上一次替换使用的空格数量
    last_space_count = 4
    
    def replace_func(match):
        nonlocal last_space_count
        # 在4和5之间交替
        current_space_count = 5 if last_space_count == 4 else 4
        last_space_count = current_space_count
        return ' ' * current_space_count
    
    # 第一步：使用正则表达式替换非汉字字符（保留换行符）
    processed_text = re.sub(pattern, replace_func, string)
    
    # 第二步：将连续的多个换行符合并成一个
    processed_text = re.sub(r'\n\s*\n+', '\n\n', processed_text)
    
    # 第三步：在每个段落开头添加9个空格
    # 分割成段落
    paragraphs = processed_text.split('\n\n')
    # 处理每个段落
    processed_paragraphs = []
    for p in paragraphs:
        if p.strip():  # 如果段落不是空的
            # 删除段落开头的所有空格，然后添加9个空格
            p = re.sub(r'^\s+', '', p)
            p = ' ' * 9 + p
            processed_paragraphs.append(p)
    
    # 重新组合段落
    processed_text = '\n\n'.join(processed_paragraphs)
    
    return processed_text
# 创建模板并设置详细参数
template1 = Template(
    background=Image.open('./paper5times/1.png'),  # 打开背景图片
    font=ImageFont.truetype(fonts, size=37*rate2),  # 调小字号以适应格子大小
    fill=(0, 0, 0, 255),  # 字体颜色，黑色
    left_margin=133*rate2,        # 左边距，与第一个格子对齐
    right_margin=(110-35)*rate2,       # 右边距，留出右侧数字标记的空间
    top_margin=612*rate2,         # 上边距，跳过表格标题和信息栏
    bottom_margin=120*rate2,      # 下边距
    line_spacing=(35+14)*rate2,        # 行间距，匹配格子高度
    word_spacing=5*rate2,        # 字间距，匹配格子宽度
    line_spacing_sigma=0.1,   # 保持行距固定，对齐格子
    font_size_sigma=0.1,      # 保持字号固定，保证整齐
    word_spacing_sigma=0.1,    # 保持字间距固定，对齐格子
    perturb_theta_sigma=0.05,  
    perturb_x_sigma=0.1,  
    perturb_y_sigma=0.1,  
)
# 创建模板并设置详细参数
template2 = Template(
    background=Image.open('./paper5times/2.png'),  # 打开背景图片
    font=ImageFont.truetype(fonts, size=37*rate2),  # 调小字号以适应格子大小
    fill=(0, 0, 0, 255),  # 字体颜色，黑色
    left_margin=130*rate2,        # 左边距，与第一个格子对齐
    right_margin=(110-35)*rate2,       # 右边距，留出右侧数字标记的空间
    top_margin=110*rate2,         # 上边距，跳过表格标题和信息栏
    bottom_margin=120*rate2,      # 下边距
    line_spacing=(35+14)*rate2,        # 行间距，匹配格子高度
    word_spacing=5*rate2,        # 字间距，匹配格子宽度
    line_spacing_sigma=0.1,   # 保持行距固定，对齐格子
    font_size_sigma=0.1,      # 保持字号固定，保证整齐
    word_spacing_sigma=0.1,    # 保持字间距固定，对齐格子
    perturb_theta_sigma=0.05,  
    perturb_x_sigma=0.1,  
    perturb_y_sigma=0.1,  
)
rate3=10
template3 = Template(
    background=Image.open('./paper5times/2.png'),  # 打开背景图片
    font=ImageFont.truetype(fonts, size=17.5*rate3),  # 调小字号以适应格子大小
    fill=(0, 0, 0, 255),  # 字体颜色，黑色
    left_margin=56*rate3,        # 左边距，与第一个格子对齐
    right_margin=(46-17/2)*rate3,       # 右边距，留出右侧数字标记的空间
    top_margin=46*rate3,         # 上边距，跳过表格标题和信息栏
    bottom_margin=52*rate3,      # 下边距
    line_spacing=(17.5+4)*rate3,        # 行间距，匹配格子高度
    word_spacing=0.9*rate3,        # 字间距，匹配格子宽度
    line_spacing_sigma=0.08,   # 保持行距固定，对齐格子
    font_size_sigma=0.08,      # 保持字号固定，保证整齐
    word_spacing_sigma=0.08,    # 保持字间距固定，对齐格子
    perturb_theta_sigma=0.05,  
    perturb_x_sigma=0.12,  
    perturb_y_sigma=0.12,  
)
index=1
# 生成手写图片
# images1 = handwrite(text1, template1)
images2 = handwrite(process_text(text1), template3)

def save_images(images,index,once=False,path='./'):

    # 保存并显示结果
    for im in images:
        assert isinstance(im, Image.Image)
        im.save(path+str(index)+'.png')  # 保存到指定路径
        im.show()
        index += 1
        if(once):
            break
def main():
    global index
    # save_images(images1,index,True)
    save_images(images2,index+1)
main()


class handwriteConfig:
    def __init__(self, backgroundPath, fonts, prePath, backgroundPathList, text1, rate2, text3, template1, template2, template3, index):
        self.backgroundPath = backgroundPath
        self.fonts = fonts
        self.prePath = prePath
        self.backgroundPathList = backgroundPathList
        self.text1 = text1
        self.rate2 = rate2
        self.text3 = text3
        self.template1 = template1
        self.template2 = template2
        self.template3 = template3
        self.index = index


        