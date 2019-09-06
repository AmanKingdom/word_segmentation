import json
import re

import jieba
import warnings

# 忽略警告?
warnings.simplefilter('ignore')


# 根据传入的tag分行文本，涉及到处理引号内的tag，比如引号内包含句号是不需要换行的
def split_by_tag(data_str, tag):
    data_split = data_str.split(tag)
    first = True
    temp = ""
    for x in data_split:
        if first:
            temp = x
            first = False
        else:
            if x:
                if x[0] == "”":
                    temp = temp + tag + x
                else:
                    temp = temp + tag + '\n' + x
    return temp


# 数据筛选、整理
def get_data(show_logging=True):
    data = ""
    with open('data/100news.txt', encoding='utf-8') as f:
        i = 1
        for line in f.readlines():
            if show_logging:
                print('取得数据行%d：' % i, line, '该数据行的数据类型为：', type(line))
            # 将数据转化为字典
            line = json.loads(line)
            # 按数据格式要求整理数据
            title = "标题：" + line["Title"] + "\n"
            content = "内容：" + line["content"] + "\n"

            # # 将文章内容中以问号 ？ 结尾的句子分行显示
            # content = re.sub('？', "?\n", content)
            # # 将文章内容中以问号 。 结尾的句子分行显示
            # content = re.sub('。', "。\n", content)

            content = split_by_tag(content, '。')
            content = split_by_tag(content, '？')

            # 去掉所有HTML css样式
            # content = re.sub('[#@]\w+[\-{}:;()\w#%,\.!]*', '', content)
            content = re.sub('[#@]\w+.*', '', content)

            data_item = title + content
            # 去掉所有的HTML标签，并用空格代替
            data_item = re.sub('<.*?>', " ", data_item)

            if show_logging:
                print('\n整理该数据行后：\n', data_item, '-'*150)

            i = i + 1
            data = data + data_item
    return data


if __name__ == '__main__':
    # print('精确模式：', ' '.join(jieba.cut(data, cut_all=False, HMM=False)))
    #
    # print('全模式：', ' '.join(jieba.cut(data, cut_all=True, HMM=False)))
    #
    # print('搜索引擎模式：', ' '.join(jieba.cut_for_search(data)))

    data = get_data(show_logging=False)
    print(data)
