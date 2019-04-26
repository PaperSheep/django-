from django.shortcuts import render
from questionnaire.models import ItemBank


# 总分值转标准分
def change_standard(item_type, total_score_dic, standard_score, grand_list):
    if total_score_dic.get(item_type):
        if total_score_dic[item_type] < grand_list[0]:
            standard_score[item_type] = 1
        elif total_score_dic[item_type] < grand_list[1]:
            standard_score[item_type] = 2
        elif total_score_dic[item_type] < grand_list[2]:
            standard_score[item_type] = 3
        elif total_score_dic[item_type] < grand_list[3]:
            standard_score[item_type] = 4
        elif total_score_dic[item_type] < grand_list[4]:
            standard_score[item_type] = 5
        elif total_score_dic[item_type] < grand_list[5]:
            standard_score[item_type] = 6
        elif total_score_dic[item_type] < grand_list[6]:
            standard_score[item_type] = 7
        elif total_score_dic[item_type] < grand_list[7]:
            standard_score[item_type] = 8
        elif total_score_dic[item_type] < grand_list[8]:
            standard_score[item_type] = 9
        else:
            standard_score[item_type] = 10
    else:
        standard_score[item_type] = 1


# 整合测试结果数据到列表里
def processing_result(standard_score, item_type, bad_result, good_result, result_list, middle_result):
        if standard_score[item_type] < 4:
            result_list.append(middle_result + '：' + bad_result)
        elif standard_score[item_type] > 7:
            result_list.append(middle_result + '：'+ good_result)
        else:
            result_list.append(middle_result + '：一般')


# 主页
def home(request):
    # 提交表单的话，就显示检验结果页面
    if request.method == 'POST':
        # print(request.POST)
        total_score_dic = {}
        for key in request.POST.keys():
            if key == 'csrfmiddlewaretoken':
                continue
            else:
                item_object = ItemBank.objects.get(item_num=int(key))
                if total_score_dic.get(item_object.item_type):
                    if request.POST[key][0] == item_object.one_score_anwser:
                        total_score_dic[item_object.item_type] += 1
                    elif request.POST[key][0] == item_object.tow_score_anwser:
                        total_score_dic[item_object.item_type] += 2
                else:
                    if request.POST[key][0] == item_object.one_score_anwser:
                        total_score_dic[item_object.item_type] = 1
                    elif request.POST[key][0] == item_object.tow_score_anwser:
                        total_score_dic[item_object.item_type] = 2
        standard_score = {}
        change_standard('乐群性', total_score_dic, standard_score, [2, 4, 6, 7, 9, 12, 14, 15, 17])
        change_standard('聪慧性', total_score_dic, standard_score, [4, 5, 6, 7, 8, 9, 10, 11, 12])
        change_standard('稳定性', total_score_dic, standard_score, [6, 8, 10, 12, 14, 17, 19, 21, 23])
        change_standard('恃强性', total_score_dic, standard_score, [3, 5, 6, 8, 10, 13, 15, 17, 19])
        change_standard('兴奋性', total_score_dic, standard_score, [4, 5, 7, 8, 10, 13, 15, 17, 19])
        change_standard('有恒性', total_score_dic, standard_score, [6, 8, 10, 11, 13, 15, 17, 18, 19])
        change_standard('敢为性', total_score_dic, standard_score, [2, 3, 4, 7, 9, 12, 15, 17, 20])
        change_standard('敏感性', total_score_dic, standard_score, [6, 7, 9, 10, 12, 14, 15, 17, 18])
        change_standard('怀疑性', total_score_dic, standard_score, [4, 6, 7, 9, 11, 13, 14, 16, 17])
        change_standard('幻想性', total_score_dic, standard_score, [6, 8, 10, 12, 14, 16, 18, 20, 21])
        change_standard('世故性', total_score_dic, standard_score, [3, 4, 5, 7, 9, 11, 12, 14, 15])
        change_standard('忧虑性', total_score_dic, standard_score, [3, 5, 7, 9, 11, 13, 15, 17, 19])
        change_standard('试验性', total_score_dic, standard_score, [5, 6, 8, 9, 11, 13, 14, 15, 16])
        change_standard('独立性', total_score_dic, standard_score, [6, 8, 9, 11, 13, 15, 16, 18, 19])
        change_standard('自律性', total_score_dic, standard_score, [5, 7, 9, 11, 13, 15, 16, 18, 19])
        change_standard('紧张性', total_score_dic, standard_score, [3, 5, 7, 9, 12, 15, 17, 20, 22])
        # 适应与焦虑型：【适应与焦虑型＝[(38+2×怀疑性+3×忧虑性+4×紧张性)－(2×稳定性+2×敢为性+2×独立性)]÷10】
        standard_score['适应与焦虑型'] = ((38 + 2 * standard_score['怀疑性'] + 3 * standard_score['忧虑性'] + 4 * standard_score['紧张性']) - (standard_score['稳定性'] + standard_score['敢为性'] + standard_score['独立性']) * 2) / 10
        # 内向与外向型：【内向与外向型=[(2×乐群性+3×恃强性+4×兴奋性+5×敢为性)－(2×独立性+11)]÷10】
        standard_score['内向与外向型'] = ((2 * standard_score['乐群性'] + 3 * standard_score['恃强性'] + 4 * standard_score['兴奋性'] + 5 * standard_score['敢为性']) - (2 * standard_score['独立性'] + 11)) / 10
        # 感情用事与安详机警型：【感情用事与安详机警型=[(77+2×稳定性+2×恃强性+2×兴奋性+2×世故性)－(4×乐群性+6×敏感性+2×幻想性)]÷10】
        standard_score['感情用事与安详机警型'] = (77 + 2 * (standard_score['稳定性'] + standard_score['恃强性'] + standard_score['兴奋性'] + standard_score['世故性']) - (4 * standard_score['乐群性'] + 6 * standard_score['敏感性'] + 2 * standard_score['幻想性'])) / 10
        # 怯懦与果断型：【怯懦与果断型=[(4×恃强性+3×幻想性+4×试验性+4×独立性)－(3×乐群性+2×有恒性)]÷10】
        standard_score['怯懦与果断型'] = (4 * (standard_score['恃强性'] + standard_score['试验性'] + standard_score['独立性']) + 3 * standard_score['幻想性'] - (3 * standard_score['乐群性'] + 2 * standard_score['有恒性'])) / 10
        # 心理健康因素：【心理健康因素=稳定性+兴奋性+(11－忧虑性)+(11－紧张性)】
        standard_score['心理健康因素'] = standard_score['稳定性'] + standard_score['兴奋性'] + 11 - standard_score['忧虑性'] + 11 - standard_score['紧张性']
        # 专业与成就者的人格因素：【专业与成就者的人格因素=自律性×2+有恒性×2+稳定性×2+恃强性+世故性+独立性+试验性】
        standard_score['专业与成就者的人格因素'] = 2 * (standard_score['自律性'] + standard_score['有恒性'] + standard_score['稳定性']) + standard_score['恃强性'] + standard_score['世故性'] + standard_score['独立性'] + standard_score['试验性']
        # 【创造力强者的人格因素=(11－乐群性)×2+聪慧性×2+恃强性+(11－兴奋性)×2+敢为性+敏感性×2+幻想性+(11－世故性)+试验性+独立性×2】
        total_score_dic['创造力强者的人格因素'] = 2 * (11 - standard_score['乐群性'] + standard_score['聪慧性'] + 11 - standard_score['兴奋性'] + standard_score['敏感性'] + standard_score['独立性']) + standard_score['恃强性'] + standard_score['敢为性'] + standard_score['幻想性'] + 11 - standard_score['世故性'] + standard_score['试验性']
        change_standard('创造力强者的人格因素', total_score_dic, standard_score, [63, 68, 73, 78, 83, 88, 93, 93, 103])
        # 在新环境中有成长能力的人格因素：【在新环境中有成长能力的人格因素=聪慧性+有恒性+自律性+(11－兴奋性)】
        standard_score['在新环境中有成长能力的人格因素'] = standard_score['聪慧性'] + standard_score['有恒性'] + standard_score['自律性'] + 11 - standard_score['兴奋性']
        context = {}
        context['result'] = []
        processing_result(standard_score, '乐群性', '保守、孤僻、严肃、退缩、拘谨、生硬，在职业上倾向于从事富于创造性的工作如科学家（尤其是物理学家和生物学家）、艺术家、音乐家和作家等。典型的代表人物如达尔文、威尔逊、爱迪生、牛顿、奥斯汀、张伯伦、米尔顿、卡莱尔、塞缪尔、约翰生（英国作家）；', '开朗、热情、随和，易于建立社会联系，在集体中倾向于承担责任和担任领导。在性方面倾向于自由、早婚。推销员、企业经理、商人、会计、教士、社会工作者等多具有此种特质。典型的代表人物如狄更斯、富兰克林、罗斯福', context['result'], '乐群性')
        processing_result(standard_score, '聪慧性', '思想迟钝，学识浅薄，抽象思考能力弱。低者通常对学习与了解能力不强，不能“举一反三”。迟钝的原因可能由于情绪不稳定，或答题时未准确把握题意造成的', '聪明，富有才识，善于抽象思考，学习能力强，思考敏捷 真确。教育、文化水准高，个人心身状态健康；', context['result'], '聪慧性')
        processing_result(standard_score, '稳定性', '情绪不稳定、幼稚、意气用事。当在事业和爱情中受挫时情绪沮丧，不易恢复。身体易罹患慢性疾病，婚姻状况较差。多为会计、办事员、农业工人、艺术家、售货员、教授等。典型人物如尼采、波德莱尔（法国诗人）、莫泊桑、切利尼（意大利雕塑家）、尼禄（罗马暴君）、柯勒律治（英国浪漫主义诗人）、哈姆雷特', '情绪稳定、成熟，能够面对现实，在集体中较受尊重。较少患慢性病。容易与别人合作，多倾向于从事技术性、管理性工作。不容易罹精神疾病。如飞行员、空中小姐、护士、研究人员、优秀运动员等。典型人物如华盛顿、俾斯麦；', context['result'], '稳定性')
        processing_result(standard_score, '恃强性', '谦卑、温顺、随和。职业选择倾向与教士、咨询顾问、农业工人、教授、医生、办事员等。典型人物如释迦牟尼、韦伯（英国改良社会主义者）、达尔文、莎士比亚、忏悔者以及许多宗教著名领袖', '武断、盛气凌人、争强好胜、固执己见。有时表现出反传统的倾向，不愿循规蹈矩，在集体活动中有时不遵守纪律，社会接触较为广泛，有时饮酒过量，睡眠较少，不太注重宗教信仰，在婚后更看重独立性。在学校学习期间，学习成绩一般或稍差。在大学期间可能表现出较强的数学能力。创造性和研究能力较强，经商能力稍差。在职业上，倾向于飞行员、竞技体育运动员、管理人员、艺术家、工程师、心理学家、作家、研究人员等。典型人物如凯撒、威廉二世、克列孟梭（第一次世界大战时法国主战派总理）、卢瑟福、路易十六、希特勒、巴斯德；', context['result'], '持强性')
        processing_result(standard_score, '兴奋性', '节制、自律、严肃、沉默寡言。不容易犯罪。在经济生活、道德行为、体育活动等方面都较谨慎，不喜欢冒险。学术活动能力比社会活动能力强一些。职业上倾向于会计、行政人员、艺术家、工程师、教士、教授、科研人员等。典型人物如帕斯卡、达尔文、狄更生（美国女诗人）、约伯（俄国主教）、丁尼生（英国诗人）、欧文（英国诗人）；','轻松、愉快、逍遥、放纵，身体健康，经济状况较好，性方面的自我约束力较差，社会联系广泛，在集体中引人注目。在家庭中，夫妻相互独立性较强。不容易得各种精神疾病和冠心病。在职业上，倾向于运动员、商人、飞行员、战士、空中小姐、水手等。惯犯中具此种特质的人较多。典型人物如包斯威尔（英国作家）、惠特曼、王尔德（美国画家）、威尔斯（英国作家）、伏尔泰等；' , context['result'], '兴奋性')
        processing_result(standard_score, '有恒性', '自私，惟利是图，不讲原则，不守规则，不尊重父母，对异性较随便，缺乏社会责任感，轻视宗教。具有此种特质的人可能有违法行为。声名狼藉的人多具有此特质。在职业上倾向于艺术家、社会工作者、社会科学家、竞技运动员、作家、记者等。典型人物如卡萨诺瓦（意大利作家、间谍、以放荡不羁闻名）、切利尼（意大利雕塑家）、卡廖斯特罗（意大利魔术家、江湖骗子）等；', '真诚、有正义感，有毅力，道德感强，稳重，执着，孝敬尊重父母，对异性较严谨，受到周围人的好评，社会责任感强，重视宗教，工作勤奋，睡眠较少，在直接接触的小群体中会自然而然地成为领导性人物。很少有犯罪违法行为。在职业上倾向于会计、教士、民航驾驶员、空中小姐、百货经营经理等。宗教先知和宗教领袖多具此特质。典型人物如勃朗宁、丁尼生、吉卜林（英国作家）、华盛顿、林肯、纳尔逊（英国海军统帅）、康德、列奥·尼达（古斯巴达将领）、南丁格尔等；', context['result'], '有恒性')
        processing_result(standard_score, '敢为性', '害羞、胆怯、易受惊吓。交感神经占支配地位。在职业上倾向于牧师、教士、编辑人员、农业工人等。典型人物如狄更生、卡文迪许；', '冒险、不可遏制，在社会行为方面胆大妄 为，副交感神经占支配地位。在职业上倾向于竞技体育运动员、商人、音乐家、机械师等。典型人物如西奥多·罗斯福、丘吉尔、杰克逊（美国总统）、理查一世、邓肯；', context['result'], '敢为性')
        processing_result(standard_score, '敏感性', '粗心、自立、现实。通常身体健康，喜爱参加体育运动，遇事果断、自信。职业上倾向于物理学家、工程师、飞行员、电气技师、销售经理、警察等。典型人物如吉卜林、塞缪尔、约翰生、马克·吐温、拿破仑、彭斯（苏格兰诗人）、林白（美国著名飞行员）；', '细心、敏感、依赖。通常身体较弱、多病，不太爱参加体育锻炼，遇事优柔寡断、缺乏自信。儿童期间多受到家庭的溺爱和过分保护，很少喝酒。一半女性得分高于男性。在学习上，语文优于数学。在职业上倾向于美术家、牧师、教士、教授、行政人员、生物学家、社会科学家、社会工作者、编辑等。典型人物如柯勒律治、华兹华斯（英国浪漫主义诗人）、王尔德、罗素、富兰克林·罗斯福夫人；', context['result'], '敏感性')
        processing_result(standard_score, '怀疑性', '真诚、合作、宽容，容易适应环境，在集体中容易与人形成良好关系。职业上倾向于会计、飞行员、空中小姐、炊事员、电气技师、机械师、生物学家、物理学家等。典型人物如托马斯（基督教虔修派最著名代表人物之一）、居里夫人、艾森豪威尔、伯里克利（希腊政治家）；', '多疑、戒备，不易受欺骗。易困，多睡眠。在集体中与他人保持距离，缺乏合作精神。有时有自杀、同性恋、违法、吸毒等行为。职业上倾向于艺术家、编辑、农业工人、管理人员、创造性科学研究人员等。典型人物如本尼狄克、阿诺德（美独立战争期间叛将）、蒙蒂兹（声名狼藉的爱尔兰美女）、亚历山大大帝、斯大林、巴顿（美国将军）、戴高乐；', context['result'], '怀疑性')
        processing_result(standard_score, '幻想性', '现实，脚踏实地，处事稳妥，具忧患意识，办事认真谨慎。典型人物如胡佛、鲍尔温（英国前首相）、卡耐基、柯立芝；', '富于想象，生活豪放不羁，对事漫不经心。通常在中学毕业后努力争取继续学习而不是早早就业。在集体中不太被人们看重。不修边幅，不重整洁，粗枝大叶。经常变换工作，不易被晋升。具此种特质的人大多属于艺术家，有吸毒、同性恋、违法方面的行为。现代“嬉皮士”多具此种特质。典型人物如斯宾诺莎、福楼拜、乔治·博罗（英国旅行家）、卡洛尔（英国童话作家）、凡·高、杰克·伦敦、埃尔、格列柯（西班牙超现实派画家）、毕加索、使文朋（英国诗人）、拜伦；', context['result'], '幻想性')
        processing_result(standard_score, '世故性', '直率、坦诚，不加掩饰，不留情面，有时显得过于刻板，不为社会所接受。在社会中不易取得较高地位。职业上倾向于艺术家、教士、汽车修理供、矿工、厨师、警卫等。典型人物如托尔斯泰、第欧根尼（希腊哲学家）、陀思妥耶夫斯基、卢梭、约翰·班扬（英国清教徒传道士）、克鲁泡特金（俄国无政府主义者）、圣女贞德等；', '机敏、狡诈、圆滑、人情练达、善于处世。不易罹患精神疾病。在社会中容易取得较好的地位。善于解决疑难问题，在集体中受到人们的重视。职业上倾向于心理学家、企业家、商人、空中小姐等。典型人物如卡萨诺瓦、欧·亨利（美国小说家）、辛普森夫人、米歇尔、阿伦（英国作家）、迪斯累里（英国首相）、劳合·乔治（英国首相）、罗斯柴尔德（英国动物学家）、梅特涅（奥地利首相）、伏尔泰等；', context['result'], '世故性')
        processing_result(standard_score, '忧虑性', '自信、心平气和、坦然、宁静，有时自负、自命不凡、自鸣得意，容易适应环境，知足常乐。职业上倾向于战斗飞行员、竞技体育运动员、行政人员、物理学家、机械师、空中小姐、心理学家等。典型人物如成吉思汗、斯大林、罗伯斯庇尔以及许多成功的行政领袖；', '忧郁、自责、焦虑、不安、自扰、朋友较少。在集体中既无领袖欲望，亦不被推选为领袖。常对环境进行抱怨，牢骚满腹。害羞、不善言辞、爱哭。大多数宗教领袖都具有此种特质。职业上倾向于艺术家、教士、农业工人等。典型人物如豪斯曼（英国作家）、坡（美国诗人）、陀思妥耶夫斯基和丘吉尔等；', context['result'], '忧虑性')
        processing_result(standard_score, '试验性', '保守、循规蹈矩、尊重传统。职业上倾向于运动员、教士、农业工人、机械师、军官、音乐家、商人、警察、厨师、保姆等。典型人物如丘吉尔、维多利亚女王、法朗士、高尔斯华绥（英国作家）、布赖恩（美国民主党领袖）、道格拉斯、黑格（英国元帅）；', '好奇，喜欢尝试各种可能性，思想自由、开放、激进。接近进步的政治党派，对宗教活动不够积极，身体健康，在家庭中较少大男子主义。职业上倾向于艺术家、作家、会计、工程师、教授等。典型人物如乐群性·赫胥黎（文学家、神秘主义者）、J·赫胥黎（生物学家、社会活动家）、赖特（建筑师）、萧伯纳、易普生、布律内尔（工程师、发明家）、威尔逊（英国小说家）、马克思、理查德·施特劳斯、拿破仑；', context['result'], '试验性')
        processing_result(standard_score, '独立性', '依赖性强，缺乏主见，在集体中经常是一个随波逐流的人，对于权威是一个忠实的追随者。职业上倾向于空中小姐、厨师、保姆、护士、社会工作者等。典型人物而如阿尔弗雷德、奥斯汀（英国诗人）、饶勒斯（法国社会主义者）、施莱辛格（美国历史学家）、柯西金（前苏联总理）、兰克（美国心理学家）、拉斯基（英国政治家）、霍法（美国劳工领袖）；', '自信，有主见，足智多谋，遇事勇于自己做主，不依赖他人，不推诿责任。职业上倾向于创造性工作，如艺术家、功工程师、科学研究人员、教授、作家等。典型人物如哥白尼、林白、鲍布、霍普（美国著名演员）、牛顿、班廷（加拿大医生，诺贝尔奖获得者）、门肯（美国政治评论家）、嘉宝（美国电影演员）、巴斯德等；', context['result'], '独立性')
        processing_result(standard_score, '自律性', '不能自制，不遵守纪律，自我矛盾，松懈，随心所欲，为所欲为，漫不经心，不尊重社会规范，不太注重道德，饮酒无节制。在职业上倾向于艺术家。典型人物如克吕格（瑞典金融投机家）、本尼狄克、阿诺德、尼禄、罗宾汉、第欧根尼、比尔兹利（英国画家）；', '有较强的自制力、坚强的意志力，较坚定地追求自己的理想，有良好的自我感觉和自我评价，通常注重性道德，饮酒适度。在集体中，可以提出有价值的建议。职业上倾向于大学行政领导、飞行员、科学家、电气技师、警卫、机械师、厨师、物理学家等。典型人物如威尔逊（美国总统）、纽博尔特（英国诗人）、金斯利（英国小说家）、凯撒、布莱（英国海军将领）、罗伯斯庇尔、吉卜林等；', context['result'], '自律性')
        processing_result(standard_score, '紧张性', '放松，平静，有时反应迟钝，不敏感，很少有挫折感，遇事镇静自若。职业倾向于空中小姐、飞行员、海员、地理学家、物理学家等。典型人物如马修、阿诺德（英国诗人）、伊壁鸠鲁、毛姆（英国作家）。', '紧张，有挫折感，经常处于被动局面，神经质，不自然，做作，在集体中很少被选为领导，通常感到不被别人尊重和接受，经常自叹命薄，在压力下容易惊慌失措。多患高血压症。职业倾向于农业工人、售货员、作家、记者等。典型人物如马克白斯、爱德华八世、威尔斯、奥本海默（美国物理学家）；', context['result'], '紧张性')
        processing_result(standard_score, '适应与焦虑型', '生活适应顺利，通常感到心满意足，能做到所期望的及自认为重要的事情。如分数极低，则可能对困难的工作缺乏毅力，有事事知难而退，不肯奋斗努力的倾向；', '不一定有神经症，因为它可能是情境性的，但也可能有一些调节不良的情况，即对生活上所要求的和自己意欲达成的事情常感到不满意。高度的焦虑可能会使工作受到破坏和影响身体健康；', context['result'], '适应与焦虑型')
        processing_result(standard_score, '内向与外向型', '内倾，趋于胆小，自足，在与别人接触中采取克制态度，有利于从事精细工作。这种类型无所谓利弊，主要取决于在哪种情况下采取这种态度；', '外倾，开朗，善于交际，不受拘束，有利于从事贸易工作；', context['result'], '内向与外向型')
        processing_result(standard_score, '感情用事与安详机警型', '情感丰富而感到困扰不安，它可能是缺乏信心、颓丧的类型，对生活中的细节较为含蓄敏感，性格温和，讲究生活艺术，采取行动前再三思考，顾虑太多；', '富有事业心，果断，刚毅，有进取精神，精力充沛，行动迅速，但常忽视生活上的细节，只对明显的事物注意，有时会考虑不周，不计后果，贸然行事；', context['result'], '感情用事与安详机警型')
        processing_result(standard_score, '怯懦与果断型', '依赖别人，纯洁，个性被动，受人驱使而不能独立，对支持他的人在行动上常适应其需求，为获取别人的欢心会事事迁就；', '果断，独立，露锋芒，有气魄，有攻击性的倾向，通常会主动地寻找可以施展这种行为的环境或机会，以充分表现自己的独创能力，并从中取得利益；', context['result'], '怯懦与果断型')
        if standard_score['心理健康因素'] < 12:
            context['result'].append('心理健康因素：情绪比较不稳定')
        else:
            context['result'].append('心理健康因素：情绪较稳定')
        if standard_score['专业与成就者的人格因素'] > 55:
            context['result'].append('专业有成就的成功率：专业有成就的成功率较高')
        else:
            context['result'].append('专业有成就的成功率：专业有成就的成功率偏低')
        if standard_score['创造力强者的人格因素'] > 6:
            context['result'].append('创造力：富有创造力')
        else:
            context['result'].append('创造力：创造力匮乏')
        if standard_score['在新环境中有成长能力的人格因素'] < 17:
            context['result'].append(' 在新环境中的成长能力：不容易在新环境中成长')
        elif standard_score['在新环境中有成长能力的人格因素'] > 24:
            context['result'].append(' 在新环境中的成长能力：容易在新环境中成长')
        else:
            context['result'].append(' 在新环境中的成长能力：一般')
        context['standard_score'] = standard_score
        return render(request, 'questionnaire/report.html', context)



    item_list = ItemBank.objects.all()

    context = {}
    context['item_list'] = item_list
    return render(request, 'questionnaire/home.html', context)


