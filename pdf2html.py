import glob,os,time,shutil,psutil,subprocess,configparser
from datetime import datetime

config = configparser.ConfigParser()
config_file = "config/config.ini"
config.read('config/config.ini')

# folder="//192.168.18.72/share/04_Application/tmp/shared_pdf_1"
# output="c:/bin/pdf"
# pass_d="e:/tools/ADPRP/APDFPR.EXE"
# pdf_c="c:/bin/PDFConvert.exe"
folder=config['con']['folder']
output=config['con']['output']
pass_d=config['con']['pass_d']
pdf_c=config['con']['pdf_c']

def process_live(i):
  pl=[]
  for proc in psutil.process_iter():
    pl.append(proc.name())
  if i in pl:
    return 1
  else:
    return 0

def remove_file(j):
  file=glob.glob("%s/*.%s" % (folder,j))
  file_length=len(file)
  if file_length:
    for i in file:
      os.remove(i)

def remove_pdf():
	pdf_file=folder+'/'+pdf_list
	if os.path.exists(pdf_file):
		os.remove(pdf_file)
		print('已删除pdf文件%s' % pdf_file)


while True:
  pdf_file=glob.glob("%s/*.pdf" % folder)
  pdf_length=len(pdf_file)
  #防止没有pdf文件报错
  while not pdf_length:
    pdf_file=glob.glob("%s/*.pdf" % folder)
    pdf_length=len(pdf_file)
    # pdf_list=pdf_file[0].split("\\")[1]
    pdf_file=glob.glob("%s/*.pdf" % folder)
    pdf_length=len(pdf_file)
    # pdf_list=pdf_file[0].split("\\")[1]
    # file_name=os.path.splitext(pdf_list)[0]
    #解决空格问题
  pdf_list=pdf_file[0].split("\\")[1]
  pdf_list_len=len(pdf_list)
  pdf_list_len2=len(pdf_list.replace(" ",""))
  if pdf_list_len2 == pdf_list_len:
    cmd_p="%s -batch %s/%s" % (pass_d,folder,pdf_list)
    command="%s -i %s/%s -o %s -f html" % (pdf_c,folder,pdf_list,output)
  else:
    cmd_p='%s -batch "%s/%s"' % (pass_d,folder,pdf_list)
    command='%s -i "%s/%s" -o "%s" -f html' % (pdf_c,folder,pdf_list,output)
  # os.system(command)
  sub_p=subprocess.Popen(cmd_p)
  time.sleep(2)
  #判断是否有解密临时文件
  pdf_tmp_file=glob.glob("%s/*.pdf--*" % folder)
  pdf_tmp_length=len(pdf_tmp_file)
  while pdf_tmp_length:
    pdf_tmp_file=glob.glob("%s/*.pdf--*" % folder)
    pdf_tmp_length=len(pdf_tmp_file)
  # pobj=psutil.Process(sub_p.pid) 
  print('tets')
  # time.sleep(20)
  sub_p.kill()
  print('开始解析pdf:',pdf_list)
  start_t=datetime.now()
  sub_c=subprocess.Popen(command)
  time.sleep(1)

  html_file_src=glob.glob("%s/*.html" % output)
  html_length=len(html_file_src)

  # html_list=html_list=html_file_src[0].split("\\")[1]
  # 如果pdf没有解析成html，并且acrobat占用内存超过2500m就kill acrobat。解析完了就跳出循环
  a=1
  p=1
  while not html_length:
    # html_file_src=glob.glob("%s/*.html" % output)
    # html_length=len(html_file_src)
    # print('test')
    # for c in pobj.children(recursive=True):
    #   c.kill()
    for proc in psutil.process_iter():
      if proc.name() == 'Acrobat.exe':
        mem_info=int(proc.memory_info().rss / 1024 /1024)
        time.sleep(1)
        mem_tmp=int(proc.memory_info().rss / 1024 /1024)
        a=1
        p=1
        pdf_type='pdf'
        pl=process_live('Acrobat.exe')
        while not html_length:
          html_file_src=glob.glob("%s/*.html" % output)
          html_length=len(html_file_src)
          if html_length:
            break
          pl=process_live('Acrobat.exe')
          if pl:
            mem_info=int(proc.memory_info().rss / 1024 /1024)
          else:
            break
          time.sleep(6)
          pl=process_live('Acrobat.exe')
          if pl:
            mem_tmp=int(proc.memory_info().rss / 1024 /1024)
          else:
            break
          print(mem_info,mem_tmp)
          print(a)
          p_time=(datetime.now()-start_t).seconds/60
          print('目前内存占用: %dM，已花费%s分钟' % (mem_info,p_time))
          if not abs(mem_tmp-mem_info):
            a+=1
          else:
            a=1
            p=1
          if a > 10:
            p_time=(datetime.now()-start_t).seconds/60
            print('目前内存占用: %dM，已花费%s分钟' % (mem_info,p_time))
            sub_c.kill()
            p=os.system("taskkill /f /im Acrobat.exe")
            print('该pdf无法解析，Acrobat进程已kill')
            remove_pdf()
            pl=process_live('Acrobat.exe')
            break
          if(mem_info > 2500):
          # if(mem_info > 3000):
          # 测试使用120
          # if(proc.memory_info().rss / 1024 /1024 > 120):
          # if(proc.memory_info().rss > 104857600):
          # if(proc.memory_info().rss):
            p_time=(datetime.now()-start_t).seconds/60
            print('目前内存占用: %dM，已花费%s分钟' % (mem_info,p_time))
            sub_c.kill()
            p=os.system("taskkill /f /im Acrobat.exe")
            print('该pdf解析使用内存过多，Acrobat进程已kill')
            remove_pdf()
            pl=process_live('Acrobat.exe')
            break
          html_file_src=glob.glob("%s/*.html" % output)
          html_length=len(html_file_src)
      if html_length:
        break
    print(222)
    #如果解析成功,kill Acrobat.exe
    if html_length:
      pl=process_live('Acrobat.exe')
      if pl:
        sub_c.kill()
        os.system("taskkill /f /im Acrobat.exe")
      break
    # pl=process_live('Acrobat.exe')
    # if not pl:
    #   break
    #如果pdf异常退出，退出解析循环
    if a > 10 or p != 1:
      break
    if a < 10 or p==1:
      html_file_src=glob.glob("%s/*.html" % output)
      html_length=len(html_file_src)
    # break
  print(333)
  if html_length:
    pl=process_live('Acrobat.exe')
    if pl:
      sub_c.kill()
      os.system("taskkill /f /im Acrobat.exe")
    # continue
    # time.sleep(2)
    # html_list=html_file_src[0].split("\\")[1]
    # if html_length > 0:
    #   shutil.move("%s/%s" % (output,html_list),"%s/%s" % (folder,html_list))
  end_t=datetime.now()
  spend_t=(end_t - start_t).seconds/60
  print('解析花费: %s 分钟' % spend_t)
  print('现在时间:', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  #删除解密备份文件
  bak_type='bak'
  remove_file(bak_type)
  html_file_src=glob.glob("%s/*.html" % output)
  html_length=len(html_file_src)
  #Acrobat进程没有被kill并且html被解析出来
  if a < 10 and p !=0 and html_length:
    # if p !=0:
    html_list=html_file_src[0].split("\\")[1]
    sub_c.kill()
    shutil.move("%s/%s" % (output,html_list),"%s/%s" % (folder,html_list))
    
    #移动文件计2s
    time.sleep(2)
    # 如果有html就不进入下一个循环
    html_file=glob.glob("%s/*.html" % folder)
    html_length=len(html_file)
    while html_length:
      html_file=glob.glob("%s/*.html" % folder)
      html_length=len(html_file)
  else:
    continue

  # 如果pdf名字没变就不进入下一个循环
  pdf_file_con=glob.glob("%s/*.pdf" % folder)
  pdf_con_length=len(pdf_file_con)
  while not pdf_con_length:
    pdf_file_con=glob.glob("%s/*.pdf" % folder)
    pdf_con_length=len(pdf_file_con)
  pdf_file_con=glob.glob("%s/*.pdf" % folder)
  pdf_list_con=pdf_file_con[0].split("\\")[1]
  #防止文件名一直不变
  for i in range(5):
    if pdf_list_con == pdf_list:
      print('pdf名字没变,目前还是:',pdf_list_con)
      pdf_file_con=glob.glob("%s/*.pdf" % folder)
      pdf_list_con=pdf_file_con[0].split("\\")[1]
      time.sleep(5)