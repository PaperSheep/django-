# 分别获取 A, B, C 选项
import re
from questionnaire.models import ItemBank


def input_item():
    title_dic = {}
    a_dic = {}
    b_dic = {}
    c_dic = {}

    with open('题目1.txt', 'r', encoding='UTF-8') as f:
        for i, line in enumerate(f.readlines()):
            if i % 2 == 1:
                a_dic[i] = re.findall(r'（A）(.*?)（B）', line)[0]
                b_dic[i] = re.findall(r'（B）(.*?)（C）', line)[0]
                c_dic[i] = re.findall(r'（C）(.*?)$', line)[-1]
            else:
                title_dic[i] = line.replace('\n', '')

    loop_count = len(a_dic)

    for i in range(0, loop_count):
        new_item = ItemBank()
        new_item.item_num = i + 1
        new_item.item_title = title_dic[i * 2]
        new_item.item_a_anwser = a_dic[2 * i + 1]
        new_item.item_b_anwser = b_dic[2 * i + 1]
        new_item.item_c_anwser = c_dic[2 * i + 1]
        new_item.save()

    print('题目与答案录入成功')


# 替换错误的b选项与c选项
def change_b_and_c():
    # all_b_item = ItemBank.objects.filter(item_b_anwser='介于（A），')
    # for b_item in all_b_item:
    #     b_item.item_b_anwser = '介于（A），（C）之间'
    #     b_item.save()
    all_c_item = ItemBank.objects.all()
    for c_item in all_c_item:
        # c_item.item_c_anwser = c_item.item_c_anwser.replace('之间', '')
        c_item.item_c_anwser = c_item.item_c_anwser.replace('（C）', '')
        c_item.save()
    print('替换成功')


# 修改相应的题的类型
def change_item_type():
    type_dic = {
        '乐群性': [3, 26, 27, 51, 52, 76, 101, 126, 151, 176],
        '聪慧性': [28, 53, 54, 77, 78, 102, 103, 127, 128, 152, 153, 177, 178, 180],
        '稳定性': [4, 5, 29, 30, 55, 79, 80, 104, 105, 129, 130, 154, 179],
        '恃强性': [6, 7, 31, 32, 56, 57, 81, 106, 131, 155, 156, 180, 181],
        '兴奋性': [8, 33, 58, 82, 83, 107, 108, 132, 133, 157, 158, 182, 183 ],
        '有恒性': [9, 34, 59, 84, 109, 134, 159, 160, 184, 185],
        '敢为性': [10, 35, 36, 60, 61, 85, 86, 110, 111, 135, 136, 161, 186],
        '敏感性': [11, 12, 37, 62, 87, 112, 137, 138, 162, 163],
        '怀疑性': [13, 38, 63, 64, 88, 89, 113, 114, 139, 164],
        '幻想性': [14, 15, 39, 40, 65, 90, 91, 115, 116, 140, 141, 165, 166],
        '世故性': [16, 17, 41, 42, 66, 67, 92, 117, 142, 167],
        '忧虑性': [18, 19, 43, 44, 68, 69, 93, 94, 118, 119, 143, 144, 168],
        '试验性': [20, 21, 45, 46, 70, 95, 120, 145, 169, 170],
        '独立性': [22, 47, 71, 72, 96, 97, 121, 122, 146, 171],
        '自律性': [23, 24, 48, 73, 98, 123, 147, 148, 172, 173],
        '紧张性': [25, 49, 50, 74, 75, 99, 100, 124, 125, 149, 150, 174, 175],
    }

    for key in type_dic.keys():
        for item_num in type_dic[key]:
            item_object = ItemBank.objects.get(item_num=item_num)
            item_object.item_type = key
            item_object.save()

    print('题的类型录入成功')


# 录入相应答案得分
def input_score():
    one_score_dic = {
        28: 'B',
        53: 'B',
        54: 'B',
        77: 'C',
        78: 'B',
        102: 'C',
        103: 'B',
        127: 'C',
        128: 'B',
        152: 'B',
        153: 'C',
        177: 'A',
        178: 'A',
    }
    for key in one_score_dic.keys():
        item_object = ItemBank.objects.get(item_num=key)
        item_object.one_score_anwser = one_score_dic[key]
        item_object.tow_score_anwser = '无'
        item_object.save()
    two_score_dic = {
        3: 'A',
        4: 'A',
        5: 'C',
        6: 'C',
        7: 'A',
        8: 'C',
        9: 'C',
        10: 'A',
        11: 'C',
        12: 'C',
        13: 'A',
        14: 'C',
        15: 'C',
        16: 'C',
        17: 'A',
        18: 'A',
        19: 'C',
        20: 'A',
        21: 'A',
        22: 'C',
        23: 'C',
        24: 'C',
        25: 'A',
        26: 'C',
        27: 'C',
        29: 'C',
        30: 'A',
        31: 'C',
        32: 'C',
        33: 'A',
        34: 'C',
        35: 'C',
        36: 'A',
        37: 'A',
        38: 'A',
        39: 'A',
        40: 'A',
        41: 'C',
        42: 'A',
        43: 'A',
        44: 'C',
        45: 'C',
        46: 'A',
        47: 'A',
        48: 'A',
        49: 'A',
        50: 'A',
        51: 'C',
        52: 'A',
        55: 'A',
        56: 'A',
        57: 'C',
        58: 'A',
        59: 'A',
        60: 'C',
        61: 'C',
        62: 'C',
        63: 'C',
        64: 'C',
        65: 'A',
        66: 'C',
        67: 'C',  
        68: 'C',
        69: 'A',
        70: 'A',
        71: 'A',
        72: 'A',
        73: 'A',
        74: 'A',
        75: 'C',
        76: 'C',
        77: 'C',
        78: 'C',
        79: 'C',
        80: 'C',
        81: 'C',
        82: 'C',
        83: 'C',
        84: 'C',
        85: 'C',
        86: 'C',
        87: 'C',
        88: 'A',
        89: 'C',
        90: 'C',
        91: 'A',
        92: 'C',
        93: 'C',
        94: 'C',
        95: 'C',
        96: 'C',
        97: 'C',
        98: 'A',
        99: 'A',
        100: 'A',
        101: 'A',
        102: 'A',
        103: 'A',
        104: 'A',
        105: 'A',
        106: 'C',
        107: 'A',
        108: 'A',
        109: 'A',
        110: 'A',
        111: 'A',
        112: 'A',
        113: 'A',
        114: 'A',
        115: 'A',
        116: 'A',
        117: 'A',
        118: 'A',
        119: 'A',
        120: 'C',
        121: 'C',
        122: 'C',
        123: 'C',
        124: 'A',
        125: 'C',
        126: 'A',
        129: 'A',
        130: 'A',
        131: 'A',
        132: 'A',
        133: 'A',
        134: 'A',
        135: 'C',
        136: 'A',
        137: 'C',
        139: 'C',
        140: 'A',
        141: 'C',
        142: 'A',
        143: 'A',
        144: 'C',
        145: 'A',
        146: 'A',
        147: 'A',
        148: 'A',
        149: 'A',
        150: 'A',
        151: 'C',
        154: 'C',
        155: 'A',
        156: 'A',
        157: 'C',
        158: 'C',
        159: 'C',
        160: 'A',
        161: 'C',
        162: 'C',
        163: 'A',
        164: 'A',
        165: 'C',
        166: 'C',
        167: 'A',
        168: 'A',
        169: 'A',
        170: 'C',
        171: 'A',
        172: 'C',
        173: 'A',
        174: 'A',
        175: 'C',
        176: 'A',
        179: 'A',
        180: 'A',
        181: 'A',
        182: 'A',
        183: 'A',
        184: 'A',
        185: 'A',
        186: 'A',
    }
    for key in two_score_dic.keys():
        item_object = ItemBank.objects.get(item_num=key)
        item_object.one_score_anwser = 'B'
        item_object.tow_score_anwser = two_score_dic[key]
        item_object.save()
    print('得分答案录入成功')
