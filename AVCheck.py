#!/usr/bin/env python3


# 提取进程名
def Process_extraction():
    with open(r'tasklist.txt', 'r', encoding="utf-8") as file:
        for line in file.readlines():
            line = line.strip('\n')
            #取出tasklist中的进程名称
            target = line.split(' ')[0]
            Process_list.append(target)

# 杀软识别
def avcheck():
    result_list = []
    for target in Process_list:
        with open('avlist.txt', 'r', encoding="utf-8") as f:
            for i in f.readlines():
                # print(target+":"+i.strip('\n').split('\"')[1])
                #将取出的进程名与杀软识别列表中的名称进行对比
                if target == i.strip('\n').split('\"')[1]:
                    result = i.strip('\n').split('\"')[3]
                    # print(target)
                    result_list.append(result)
                else:
                    pass
    if len(result_list) == 0:
        print("\t没有识别到杀软或者不存在杀软")
    else:
        avreuslts = []
        for result in result_list:
            if result and not result in avreuslts:
                avreuslts.append(result)
        print("\t服务器上存在的杀毒软件有:", avreuslts)

# 软件识别
def vncrdp():
    result_list = []
    for target in Process_list:
        with open('application.txt', 'r', encoding="utf-8") as f:
            for i in f.readlines():
                # print(target+":"+i.strip('\n').split('\"')[1])
                #将取出的进程名与杀软识别列表中的名称进行对比
                if target == i.strip('\n').split('\"')[1]:
                    result = i.strip('\n').split('\"')[3]
                    result_list.append(result)
                else:
                    pass
    if len(result_list) == 0:
        print("\t没有识别到软件")
    else:
        rdreuslts = []
        for result in result_list:
            if result and not result in rdreuslts:
                rdreuslts.append(result)
        print("\t服务器上存在的软件有:",rdreuslts)

if __name__ == "__main__":
    banner = '''
     ___   ____    ____  ______  __    __   _______   ______  __  ___ 
    /   \  \   \  /   / /      ||  |  |  | |   ____| /      ||  |/  / 
   /  ^  \  \   \/   / |  ,----'|  |__|  | |  |__   |  ,----'|  '  /  
  /  /_\  \  \      /  |  |     |   __   | |   __|  |  |     |    <   
 /  _____  \  \    /   |  `----.|  |  |  | |  |____ |  `----.|  .  \  
/__/     \__\  \__/     \______||__|  |__| |_______| \______||__|\__\ 

                                                       --by s1g0day修改
                                                                      
                                                                      
注: 结果不一定准确,可能会存在未收录的情况,检查完毕还请注意查看下进程
    若发现未收录的杀软,请手动添加到`杀软识别.txt`
                                                                      
'''
    print(banner)
    Process_list=[]
    Process_extraction()
    print('开始识别杀软')
    avcheck()
    print('\n开始识别软件')
    vncrdp()