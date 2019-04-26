# 去掉所有空格
word_list = []
with open('题目1.txt', 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        word_list.append(line.replace(' ', ''))

with open('题目1.txt', 'w', encoding='UTF-8') as f:
    f.writelines(word_list)

print('应该成功吧')
