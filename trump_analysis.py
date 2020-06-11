import pandas as pd
import csv
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import jieba
import re
from matplotlib import colors
import numpy as np
from PIL import Image

"""
大家好，我是菜鸟程序员，公众号：Python知识圈

1、生成词云图的代码中，你需要修改下你的电脑的具体字体路径，给出你生成词云的背景图片，否则会默认一张白色的矩形背景

2、对Python感兴趣的同学可以关注我的个人公众号「Python知识圈」，有疑问也可以通过公众号加我微信，一起探讨交流
"""


# 读取Excel表格信息并返回结果
def excel_one_line_to_list():
    data = pd.read_excel('/Users/brucepk/Documents/trump_20200530_中文翻译版.xlsx', header=1, usecols=[0], names=None)
    df_li = data.values.tolist()
    result = []
    for s_li in df_li:
        result.append(s_li[0])
    return result


if __name__ == '__main__':
    result = str(excel_one_line_to_list())
    results = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\。\@\#\\\&\*\%]", "", result).replace('谢谢', '').replace('今天', '')
    text = ''
    for line in results:
        text += ' '.join(jieba.cut(line, cut_all=False))
    print('text:', text)
    backgroud_Image = np.array(Image.open('trumppic2.png'))   # 生成词云图的背景图片

    # 设置生成词云的参数，font_path为电脑里的字体路径，需要改成你电脑的字体路径
    wc = WordCloud(scale=32, background_color='white', mask=backgroud_Image,
                   font_path='/System/Library/Fonts/Supplemental/Songti.ttc',
                   max_words=1000, max_font_size=100, random_state=42, mode='RGB')
    wc.generate_from_text(text)

    process_word = WordCloud.process_text(wc, text)
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    print(sort[:50])   # 打印出排名前50的词
    img_colors = ImageColorGenerator(backgroud_Image)
    wc.recolor(color_func=img_colors)
    plt.imshow(wc)
    plt.axis('off')
    wc.to_file("trump20.jpg")  # 保存词云图在代码的的同一目录下
    print('生成词云成功!')

