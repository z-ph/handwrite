# coding: utf-8
from PIL import Image, ImageFont
from handright import Template, handwrite
SJNMDJW_config={
    'backgroundPath':'./pic/paper.png',
    'fontsPath':'./fonts/SJNMDJW.ttf',
    'outputPath':'./output_SJNMDJW/',
}
def process_text(string,replace_item_list:list=None):
    '''
    1.保留字符串中的汉字、逗号、句号，将其他字符替换为四个或五个空格，相邻替换的空格的数量需要不一样
    2.保留换行符，连续的多个换行符合并成一个
    3.每段开头增加9个空格
    4.将被替换的字符保存在replace_item_list中
    '''
    import re

    # 如果 replace_item_list 为 None，创建一个空列表
    if replace_item_list is None:
        replace_item_list = []

    # 定义匹配汉字、逗号、句号的正则表达式
    pattern = r'[^\u4e00-\u9fa5，。、！？；：\n]+'
    
    # 用于跟踪上一次替换使用的空格数量
    last_space_count = 4
    
    def replace_func(match):
        nonlocal last_space_count
        # 收集被替换的字符到 replace_item_list 中
        replace_item_list.append(match.group(0))
        if(match.group(0)=='——'):
            return ' '* 9  # 特殊处理长破折号，替换为9个空格
        # 在4和5之间交替
        current_space_count = 5 if last_space_count == 4 else 4
        last_space_count = current_space_count

        return ' ' * current_space_count
    
    # 第一步：使用正则表达式替换非汉字字符（保留换行符）
    processed_text = re.sub(pattern, replace_func, string)
    
    # 第二步：将连续的多个换行符合并成一个
    processed_text = re.sub(r'\n\s*\n+', '\n', processed_text)
    
    # 第三步：在每个段落开头添加9个空格
    # 分割成段落
    paragraphs = processed_text.split('\n')
    # 处理每个段落
    processed_paragraphs = []
    for p in paragraphs:
        if p.strip():  # 如果段落不是空的
            # 删除段落开头的所有空格，然后添加9个空格
            p = re.sub(r'^\s+', '', p)
            p = ' ' * 9 + p
            processed_paragraphs.append(p)
    
    # 重新组合段落
    processed_text = '\n'.join(processed_paragraphs)
    
    return processed_text
class SJNMDJW:
    backgroundPath = SJNMDJW_config['backgroundPath']
    fontsPath = SJNMDJW_config['fontsPath']
    outputPath = SJNMDJW_config['outputPath']
    leftMargin = 560
    gridHeight = 175
    gridWidth = 183.8
    gridGap=41
    bottomMargin = 520
    topMargin=441
    fontColor = (0,0,0,255)  # 黑色字体
    fontSize = 175
    replace_item_list = []  # 用于存储被替换的字符列表
    outputFileName='output.png'
    def __init__(self,lineSpacing=None,top=None,bottom=None,left=None,fontSize=None,outputPath=None,outputFileName=None):
        # 初始化参数
        self.rightMargin = 460-self.gridHeight/2
        self.lineSpacing = self.gridHeight + self.gridGap
        self.wordSpacing = self.gridWidth - self.fontSize

        if(lineSpacing is not None):
            self.lineSpacing=self.fontSize + lineSpacing
        if(top is not None):
            self.topMargin=top
        if(bottom is not None):
            self.bottomMargin=bottom
        if(left is not None):
            self.leftMargin=left
        if(fontSize is not None):
            self.fontSize=fontSize
        import os

        
        # 去除路径末尾的 / 或 \
        if self.outputPath.endswith('/') or self.outputPath.endswith('\\'):
            self.outputPath = self.outputPath[:-1]
        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        # 检查路径的合法性
        if not outputPath:
            raise ValueError("Output path must be provided.")
        if not os.path.isdir(outputPath):
            raise ValueError("Output path must be a valid directory.")
        
        # 添加末尾的 /
        if not self.outputPath.endswith('/'):
            self.outputPath += '/'
        if(outputFileName is not None):
            self.outputPath += outputFileName

    def create_template(self,sigma=2,text='',rotate_sigma=0.08,down_move=0,right_move=0):
        # 创建模板
        self.sigma = sigma
        template = Template(
            background=Image.open(self.backgroundPath),
            fill=self.fontColor,
            font=ImageFont.truetype(self.fontsPath, self.fontSize),
            left_margin= self.leftMargin+right_move,
            right_margin=self.rightMargin-right_move,
            top_margin=self.topMargin+down_move,
            bottom_margin=self.bottomMargin-down_move,
            line_spacing=self.lineSpacing,
            word_spacing=self.wordSpacing,
            line_spacing_sigma=self.sigma,  # 保持行距固定，对齐格子
            font_size_sigma=self.sigma,  # 保持字号固定，保证整齐  
            word_spacing_sigma=self.sigma,  # 保持字间距固定，对齐格子
            perturb_theta_sigma=rotate_sigma,  # 旋转扰动
            perturb_x_sigma=0,  # 水平扰动
            perturb_y_sigma=self.sigma,  # 垂直扰动
            start_chars="“（[<",  # 特定字符提前换行，防止出现在行尾
            end_chars="，。",  # 防止特定字符因排版算法的自动换行而出现在行首
        )
        self.template = template
        self.text = process_text(text,self.replace_item_list)
        return self
    def save_image(self):
        if not hasattr(self, 'template'):
            raise ValueError("Template not created. Call create_template() first.")
        ims = handwrite(self.text, self.template)
        for index, im in enumerate(ims):
            im.save(self.outputPath + self.outputFileName.replace('.png','_') + str(index) + '.png')  # 保存到指定路径
            im.show()  # 显示图片
        return self
    def save_replace_item(self):
        with open(self.outputPath + self.outputFileName.replace('.png','_') + 'replace_item.txt', 'w', encoding='utf-8') as file:
            for item in self.replace_item_list:
                file.write(item + '\n')
        return self

def test():
    text='''人工智能+时代推动大学生劳动教育内容方式改革创新
随着人工智能技术的快速发展，我们正步入一个全新的时代——人工智能+时代。这一时代的到来，不仅改变了我们的生产方式和生活方式，也对教育领域产生了深远的影响。特别是在大学生劳动教育这一领域，人工智能技术的引入，为教育内容和方式的改革创新提供了新的可能性。本文将探讨在人工智能+时代背景下，如何推动大学生劳动教育内容和方式的改革创新。
人工智能对劳动教育的影响是深远的。它改变了劳动教育的内容，使得教育内容需要不断更新以适应时代的发展。在传统的劳动教育中，体力劳动占据了重要位置，而在人工智能时代，智力劳动和创造性劳动变得越来越重要。因此，劳动教育的内容需要增加对AI技术、编程、数据分析等方面的教育，以培养学生在未来社会中的竞争力。同时，人工智能技术的应用也改变了劳动教育方式，使得教育方式更加多样化和个性化。通过AI技术，可以实现个性化教学，根据学生的学习进度和兴趣，提供定制化的学习内容和教学方法。此外，AI还可以通过虚拟现实VR和增强现实AR技术，提供更加直观和互动的学习体验，增强学生的实践能力和创新思维。'''
    sjnmdjw = SJNMDJW(outputPath='./output/')
    sjnmdjw.create_template(text=text).save_image().save_replace_item()
    print(sjnmdjw.replace_item_list)
if __name__ == "__main__":
    test()
'''
文本应避免出现英文，如果出现最好不要超过三个连续的英文字符,破折号会空出两格，双引号会空出一个，连续的英文字母会空出一格（多余连续的三个英文字符也只会空出一格），特殊标点符号不要和英文字母同时连续出现
'''