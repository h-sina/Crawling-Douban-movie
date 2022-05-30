# -*- coding = utf-8 -*-
# @Time : 2021/8/18 23:59
# @File : ciyun.py
# @Software : PyCharm
import jieba                            # 分词
import pymysql                          # 数据库
from matplotlib import pyplot as plt    # 绘图，数据可视化
from wordcloud import WordCloud         # 词云
from PIL import Image                   # 图片处理
import numpy as np                      # 矩阵运算

# 准备词云所需的文字（词）
con = pymysql.connect(host='localhost', user='root', password='123456', database='jdbc')
cur = con.cursor()
sql = 'select introduction from movie250'
cur.execute(sql)
data = cur.fetchall()
text = ""
for item in data:
    text = text + item[0]
cur.close()
con.close()

# 分词
cut = jieba.cut(text)
string = ' '.join(cut)


img = Image.open(r'.\static\assets\img\tree.jpg')   # 打开遮罩图片
img_array = np.array(img)   # 将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="msyh.ttc"    # 字体所在位置：C:\Windows\Fonts
)
wc.generate_from_text(string)


# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')     # 是否显示坐标轴

plt.show()    # 显示生成的词云图片
print("ok")

# 输出词云图片到文件
plt.savefig(r'.\static\assets\img\treeWorldCould.jpg', dpi=500)
