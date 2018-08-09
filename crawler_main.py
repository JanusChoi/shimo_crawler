import crawler_new as cn
import time
import getpass
from datetime import datetime

############

## Welcome information
print("**********************************************************************************************")
print("**                                                                                          **")
print("**     欢迎使用石墨文档自动索引小工具！                                                     **")
print("**                                                                                          **")
print("**     目前可供使用的版本如下：                                                             **")
print("**                                                                                          **")
print("**     1. 谷歌浏览器Chrome版                                                                **")
print("**                                                                                          **")
print("**     - 优势：可把结果写回到石墨文档中，便于后续全自动化。                                 **")
print("**     - 缺点：要求石墨文档名称不可包含表情包类型的字符，即只可使用键盘上可输入的字符。     **")
print("**                                                                                          **")
print("**     2. 火狐浏览器FireFox版                                                               **")
print("**                                                                                          **")
print("**     - 优势：可处理文件名内表情包类型的字符。                                             **")
print("**     - 缺点：无法把结果写回到石墨文档中，只能写到txt文件上。                              **")
print("**                                                                                          **")
print("**     欢迎访问我的github： https://github.com/JanusChoi/shimo_crawler                      **")
print("**********************************************************************************************")

pars, exclude_link = cn.read_config('config.ini')

shimo_base = pars['shimo_base']
pagewait = int(pars['pagewait'])
pw_key = '41859800'

driver_type = ''
if pars['driver_type'] == '':
    print("\n请输入你要使用的版本，1 = Chrome版，2 = FireFox版（请回复‘1’或‘2’，然后输入回车）")
    driver_type = input("> ")
else:
    driver_type = pars['driver_type']

if driver_type != '1' and driver_type != '2':
    print("\n输入有误，请重新执行程序。")
    exit()

if pars['shimo_start']=='':
    print("\n请输入你要抓取的石墨页面链接：")
    shimo_start = input("> ")
else:
    shimo_start = pars['shimo_start']

if pars['shimo_result']=='':
    print("\n请输入你用于存放结果的石墨文档链接：")
    shimo_result = input("> ")
else:
    shimo_result = pars['shimo_result']

if pars['name']=='':
    print("\n请输入你的石墨用户名：")
    name = input("> ")
else:
    name = pars['name']

if pars['passwd']=='':
    print("\n请输入你的石墨密码：")
    passwd = getpass.getpass("> ")
    passwd = cn.encode(pw_key, passwd)
else:
    passwd = pars['passwd']

print(f"\n抓取程序正在运行中，页面等待时间为：{pagewait}秒，请稍候. . . ")
print("你可在程序文件config.ini中设置该等待时间，参数名为：pagewait")

## Write info back to config.ini
pars['driver_type'] = driver_type
pars['shimo_start'] = shimo_start
pars['shimo_result'] = shimo_result
pars['name'] = name
pars['passwd'] = passwd

rs = open('config.ini', "w", encoding='utf-8')
for key in pars:
	rs.write(f"{key}:{pars[key]}\n")

for var in exclude_link:
	rs.write(f"{var}\n")

rs.close()

## Initial crawler object
current_date = str(datetime.now())
current_date = current_date.replace('-','')[2:8]

shimo = cn.SeleniumCrawler(
driver_type = driver_type,
base_url = shimo_base,
exclusion_list = exclude_link,
output_file='ResultSet' + current_date + '.txt', ## default save in ./
start_url = shimo_start
)

rs = open(shimo.output_file, "w", encoding='utf-8')
rs.write("")
rs.close()
## Log in shimo
passwd = cn.decode(pw_key, passwd)
shimo.log_in('https://shimo.im/login', name, passwd)
time.sleep(pagewait)
passwd = ''
## Start crawling
shimo.run_crawler()

## Write log to the end
current_time = str(datetime.now())
out_text1 = [[["文档自动更新于："],[current_time]]]
shimo.txt_output(out_text1,0)

if driver_type == '2':
    print(f"内容生产完毕，请查看程序目录下的文件：{shimo.output_file}")
    shimo.browser.quit()
    exit(0)

## read in all text
rs = open(shimo.output_file, "r", encoding='utf-8')
rs_all = rs.read()
rs_sep = rs_all.split("\n")
rs.close()

## write into the shimo indexing document
idx_file = shimo.get_page(shimo_result)
time.sleep(pagewait)
editor = shimo.browser.find_element_by_xpath('//*[@id="ql-container"]/div[1]')
#debug# print("Clear the Result Page")
editor.clear()

#debug# print(f"Writing to Page: {rs_all[0:20]}...")
editor.send_keys(rs_all)

#debug# print("Finished. Wait to close page.")
time.sleep(pagewait)

print("内容生产完毕，请访问你指定的石墨文档。")
shimo.browser.quit()
