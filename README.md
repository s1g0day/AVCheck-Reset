# AVCheck
对windows系统进程中的杀软进行识别，快速发现杀软，为后续绕过进行准备。

### 工具简介:
首先使用tasklist查看windows服务器上运行的进程，然后将结果复制到“tasklist.txt”，然后遍历tasklist文件并将进程名获取到，然后将进程名与“杀软识别.txt”中的进程名进行对比，如果存在即证明服务器上存在该杀软。

### 使用方法
1.在服务器上执行tasklist命令查看运行的进程

2.将结果复制到tasklit.txt文件中

3.执行命令`python3 AVCheck.py`运行程序



### 软件列表更新

20250212

| 收录时间      | 收录进度 | 编程语言 | 项目最后更新时间 | 项目地址                                                 |
| ------------- | -------- | -------- | ---------------- | -------------------------------------------------------- |
| 2025年2月11日 | 已完成   | python   | 2022年4月19日    | https://github.com/wwl012345/AVCheck                     |
| 2025年2月11日 | 已完成   | python   | 2024年5月2日     | https://github.com/BugFor-Pings/Antivirus-identification |
| 2025年2月11日 | 已完成   | go       | 2022年12月24日   | https://github.com/Goqi/AvHunt                           |
| 2025年2月11日 | 已完成   | python   | 2020年11月30日   | https://github.com/StudyCat404/WhatAV                    |
| 2025年2月11日 | 已完成   | python   | 2020年8月3日     | https://github.com/Ruiruigo/WinEXP                       |
| 2025年2月12日 | 已完成   | json     | 2024年1月18日    | https://github.com/yzddmr6/As-Exploits                   |
| 2025年2月12日 | 已完成   | python   | 2023年2月10日    | https://github.com/jiushill/csplugin                     |
| 2025年2月12日 | 已完成   | go       | 2021年5月6日     | https://github.com/CTF-MissFeng/GoScan/                  |
| 2025年2月12日 | 已完成   | c#       | 2023年8月7日     | https://github.com/Ridter/MSSQL_CLR                      |
| 2025年2月12日 | 已完成   | js       | 2021年10月21日   | https://github.com/gh0stkey/avList                       |
| 2025年2月12日 | 已完成   | c#       | 2024年12月19日   | https://github.com/lintstar/SharpHunter/                 |
| 2025年2月12日 | 已完成   | python   | 2023年3月18日    | https://github.com/sftfjugg/CodeTest                     |
| 2025年2月12日 | 已完成   | c#       | 2021年9月2日     | https://github.com/microvorld/DetectAV/                  |
| 2025年2月12日 | 已完成   | c#       | 2020年9月30日    | https://github.com/3had0w/Antivirus-detection            |
| 2025年2月12日 | 已完成   | can      | 2023年10月22日   | https://github.com/xf555er/Nobody/                       |
| 2025年2月12日 | 已完成   | go       | 2024年4月15日    | https://github.com/ceciliaaii/CheckAV                    |
| 2025年2月12日 | 已完成   | c#       | 2021年7月15日    | https://github.com/RedSiege/CIMplant                     |
| 2025年2月12日 | 已完成   | can      | 2021年8月4日     | https://github.com/0x727/AggressorScripts_0x727          |
| 2025年2月12日 | 已完成   | java     | 2024年7月10日    | https://github.com/smxiazi/xia_Liao                      |
| 2025年2月12日 | 已完成   | go       | 2023年6月11日    | https://github.com/yhy0/ChYing                           |
| 2025年2月12日 | 已完成   | python   | 2020年11月30日   | https://github.com/StudyCat404/WhatAV                    |
| 2025年2月12日 | 已完成   | python   | 2024年1月5日     | https://github.com/FunnyWolf/viperpython                 |
