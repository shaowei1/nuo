# import itchat
#
# itchat.auto_login()
#
# itchat.send('Hello, filehelper', toUserName='filehelper')

"""
pip install pyqrcode
pip install pypng

"""
import json

import itchat, time
import matplotlib.pyplot as plot

rName = ['从0开始做增长读者群', 'AssetClub官方用户群', 'ECPro 项目组', '懂你英语-Laurinda-VIP14班', "【下午18点解散】17期实操15班"][-1]


def chatProportion(rName):
    need_user = []
    province_mapping = {}

    itchat.auto_login(True)
    male = female = other = 0
    # rName = rName
    roomSum = 0
    chatRooms = itchat.search_chatrooms(name=rName)
    print(chatRooms)
    if chatRooms is None:
        print("no this:" + rName)
    else:
        chatRoom = itchat.update_chatroom(chatRooms[0]['UserName'], detailedMember=True)
        index = 0
        mem_list = chatRoom['MemberList']
        roomSum = len(mem_list)
        for friend in mem_list:
            dis = friend['DisplayName']
            nick = friend['NickName']
            sex = friend['Sex']
            city = friend['City']
            province = friend['Province']

            if sex == 1:
                male += 1
            elif sex == 2:
                female += 1
                if city in ['北京',
                            'Beijing',
                            '东城',
                            '西城',
                            '海淀',
                            '朝阳',
                            '丰台',
                            '门头沟',
                            '石景山',
                            '房山',
                            '通州',
                            '顺义',
                            '昌平',
                            '大兴',
                            '怀柔',
                            '平谷',
                            '延庆',
                            '密云',
                            'Dongcheng',
                            'Xicheng',
                            'Haidian',
                            'Zhaoyang',
                            'Fengtai',
                            'Mentougou',
                            'Shijingshan',
                            'Fangshan',
                            'Tongzhou',
                            'Shunyi',
                            'Changping',
                            'Daxing',
                            'Huairou',
                            'Pinggu',
                            'Yanqing',
                            'Miyun']:
                    need_user.append((index, dis, nick, sex, city))
                # print(index, dis, nick, sex, city, province)
                if province in province_mapping:
                    province_mapping[province].append((index, dis, nick, sex, city))
                else:
                    province_mapping[province] = [(index, dis, nick, sex, city)]
            else:
                other += 1
            index += 1

    labels = ['男:' + str(male), '女' + str(female), '其他' + str(other)]
    sizes = [male, female, other]
    colors = ['green', 'red', 'gray']
    # 几个分量向外偏移
    explode = (0.1, 0.1, 0)
    plot.pie(sizes, explode, labels, colors, '%2.0f%%')
    plot.axis('equal')
    plot.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))

    plot.rcParams[u'font.sans-serif'] = ['simhei']
    plot.rcParams['axes.unicode_minus'] = False

    plot.title("群名：" + str(rName) + "[总人数：" + str(roomSum) + "]\n" + str("(男女比例分析-流年master出品)"))
    plot.grid()
    plot.show()
    print(need_user)
    print(province_mapping)


def getInfo():
    # 测试数据
    # info = []
    # city_list = ["西安","大理","西安","city","西安","西安","","大理"]
    # sex_list = ["男","女","男"]
    # for city in city_list:

    #     for sex in sex_list:
    #         per_info = {
    #             'city':None,
    #             'sex':None
    #         }
    #         if city == "":
    #             city = "其他"

    #         per_info['city'] = city
    #         per_info['sex'] = sex
    #         info.append(per_info)

    # return info

    data_info = []
    itchat.auto_login(True)
    # rName = rName
    chatRooms = itchat.search_chatrooms(name=rName)
    if chatRooms is None:
        print("no this:" + rName)
    else:
        chatRoom = itchat.update_chatroom(chatRooms[0]['UserName'], detailedMember=True)
        mem_list = chatRoom['MemberList']
        for friend in mem_list:
            sex = friend['Sex']
            city = friend['City']
            if sex == 2:
                tmp = [friend["NickName"], friend['Signature'], friend["Province"]]  # , friend["HeadImgUrl"]
                print(tmp)
            per_info = {
                'city': None,
                'sex': None
            }
            if city == "":
                city = "其他"
            per_info['city'] = city
            per_info['sex'] = sex
            data_info.append(per_info)
    return data_info


def cityData(rName):
    info = getInfo()
    city_list = []
    for ereryOne in info:
        city_list.append(ereryOne['city'])

    # 归一去重
    single_list = set(city_list)
    men_arr = []
    women_arr = []
    for single in single_list:
        men_count = 0
        women_count = 0
        for everyOne in info:
            if everyOne['city'] == single:
                if everyOne['sex'] == 1 or everyOne['sex'] == "男":
                    men_count += 1
                else:
                    women_count += 1
        men_arr.append(men_count)
        women_arr.append(women_count)

    wid = 0.4
    ax = plot.subplot()
    x_dir = list(range(len(single_list)))
    # 第二个柱状图偏移一点
    x_dir2 = [x_dir[i] + wid for i in range(len(x_dir))]
    tick_loc = [i + wid / 2 for i in range(len(single_list))]

    # 1 竖向柱状图
    # label1 = plot.bar(x_dir, men_arr, width=wid, fc='gray')
    # for rect in label1:
    #     height = rect.get_height()
    #     # .-0.1 : 反向移动0.1
    #     plot.text(rect.get_x()+rect.get_width()/2.-0.1, 1.03*height, "%s" % float(height))

    # label2 = plot.bar(x_dir2, women_arr, width=wid, fc='r')
    # for rect in label2:
    #     height = rect.get_height()
    #     plot.text(rect.get_x()+rect.get_width()/2.-0.1, 1.03*height, "%s" % float(height))

    # # 横向标签位置
    # ax.set_xticks(tick_loc)
    # # 横向标签名称
    # ax.set_xticklabels(single_list)
    # plot.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # plot.title("男女地区竖向柱状图")
    # plot.show()

    # 2 横向柱状图
    label1 = ax.barh(x_dir, men_arr, height=wid, fc='gray')
    for rect in label1:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, '%d' % int(w), ha='left', va='center')

    label2 = ax.barh(x_dir2, women_arr, height=wid, fc='r')
    for rect in label2:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, '%d' % int(w), ha='left', va='center')

    # 纵向标签位置
    ax.set_yticks(tick_loc)
    # 纵向标签名称
    ax.set_yticklabels(single_list)
    # plot.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plot.rcParams[u'font.sans-serif'] = ['simhei']
    plot.rcParams['axes.unicode_minus'] = False

    plot.title("男女地区横向柱状图")
    plot.show()


def get_group_list():
    itchat.auto_login(True)

    groupChat = itchat.get_chatrooms()
    len(groupChat)
    print([it['NickName'] for it in groupChat])


def get_mps():
    itchat.auto_login(True)

    # mps是公众服务号，还包括小程序
    mps = itchat.get_mps(update=True)
    # 搜索某个公众号
    hello = itchat.search_mps(name='有书书院')
    print(['%s : %s' % (it['NickName'], it['Signature']) for it in mps])
    len(mps)


def get_friends():
    province_mapping = {}
    itchat.auto_login(hotReload=True)

    # 获取所有好友信息
    account = itchat.get_friends()

    # #获取自己的UserName，以上列表的第一个就是自己，如果要寻找某个用户的话，可以通过搜索名字获得UserName
    # userName = account[0]['UserName']
    for index, friend in enumerate(account):
        dis = friend['DisplayName']
        nick = friend['NickName']
        sex = friend['Sex']
        city = friend['City']
        province = friend['Province']
        if province in province_mapping:
            province_mapping[province].append((index, dis, nick, sex, city))
        else:
            province_mapping[province] = [(index, dis, nick, sex, city)]
    print(json.dumps(province_mapping))
    # 寻找某个好友，把Mou改成你要查找的某人的备注就可以了
    # users = itchat.search_friends(name='Mou')

    # 获得用户的UserName，一个特定的code
    # katie = users[0]['UserName']

    # itchat.send('hello Mou，Vincent is missing you', toUserName=katie)
    # 世界地图数据
    value = [95.1, 23.2, 43.3, 66.4, 88.5]
    attr = ["China", "Canada", "Brazil", "Russia", "United States"]

    # 省和直辖市
    province_distribution = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16,
                             '湖南': 9, '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7,
                             '内蒙古': 3, '重庆': 3, '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1,
                             '舵主科技，质量保证': 1, '天津': 1, '其他': 1}
    provice = list(province_distribution.keys())
    values = list(province_distribution.values())

    # 城市 -- 指定省的城市 xx市
    city = ['郑州市', '安阳市', '洛阳市', '濮阳市', '南阳市', '开封市', '商丘市', '信阳市', '新乡市']
    values2 = [1.07, 3.85, 6.38, 8.21, 2.53, 4.37, 9.38, 4.29, 6.1]

    # 区县 -- 具体城市内的区县  xx县
    quxian = ['夏邑县', '民权县', '梁园区', '睢阳区', '柘城县', '宁陵县']
    values3 = [3, 5, 7, 8, 2, 4]
    # https://echarts.baidu.com/examples/#chart-type-map

if __name__ == "__main__":
    chatProportion(rName)

    # cityData(rName)
    # getInfo()
    # get_group_list()
    # get_mps()
    # get_friends()
    pass


"""pip install echarts-countries-pypkg
pip install echarts-china-provinces-pypkg
pip install echarts-china-cities-pypkg
pip install echarts-china-counties-pypkg
pip install echarts-china-misc-pypkg
pip install echarts-united-kingdom-pypkg
"""