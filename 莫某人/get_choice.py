# 分别获取 A, B, C 选项
import re


a_dic = {}
b_dic = {}
c_dic = {}

with open('题目1.txt', 'r', encoding='UTF-8') as f:
    for i, line in enumerate(f.readlines()):
        if i % 2 == 1:
            a_dic[i] = re.findall(r'（A）(.*?)（B）', line)[0]
            b_dic[i] = re.findall(r'（B）(.*?)（C）', line)[0]
            c_dic[i] = re.findall(r'（C）(.*?)$', line)[-1]

with open('题目1答案.txt', 'w', encoding='UTF-8') as f:
    loop_count = len(a_dic)
    for i in range(0, loop_count):
        word_list = '（A）' + a_dic[2 * i + 1] + '（B）' + b_dic[2 * i + 1] + '（C）' + c_dic[2 * i + 1] + '\n'
        f.writelines(word_list)

print('提取答案成功')
