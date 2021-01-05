import glob,os,time,shutil,psutil,subprocess
from datetime import datetime

folder="c:/bin/pdf"
# folder="//192.168.18.72/share/04_Application/tmp/shared_pdf_1"
output="c:/bin/pdf"

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
	pdf_list=pdf_file[0].split("\\")[1]
	# file_name=os.path.splitext(pdf_list)[0]
	#解决空格问题
	pdf_list_len=len(pdf_list)
	pdf_list_len2=len(pdf_list.replace(" ",""))
	if pdf_list_len2 == pdf_list_len:
		cmd_p="e:/tools/ADPRP/APDFPR.EXE -batch %s/%s -q" % (folder,pdf_list)
		command="c:/bin/PDFConvert.exe -i %s/%s -o %s -f html" % (folder,pdf_list,output)
	else:
		cmd_p='e:/tools/ADPRP/APDFPR.EXE -batch "%s/%s" -q' % (folder,pdf_list)
		command='c:/bin/PDFConvert.exe -i "%s/%s" -o "%s" -f html' % (folder,pdf_list,output)
	# os.system(command)
	sub_p=subprocess.Popen(cmd_p)
	time.sleep(2)
	#判断是否有解密临时文件
	pdf_tmp_file=glob.glob("%s/*.pdf--$$tmp$$3aatmpf80$$" % folder)
	pdf_tmp_length=len(pdf_tmp_file)
	while pdf_tmp_length:
		pdf_tmp_file=glob.glob("%s/*.pdf--$$tmp$$3aatmpf80$$" % folder)
		pdf_tmp_length=len(pdf_tmp_file)
	# pobj=psutil.Process(sub_p.pid) 
	print('tets')
	# time.sleep(20)
	sub_p.kill()
	print('开始解析pdf:',pdf_list)
	start_t=datetime.now()
	sub_c=subprocess.Popen(command)
	time.sleep(5)

	html_file_src=glob.glob("%s/*.html" % output)
	html_length=len(html_file_src)

	# html_list=html_list=html_file_src[0].split("\\")[1]
	# 如果pdf没有解析成html，并且acrobat占用内存超过2500m就kill acrobat。解析完了就跳出循环
	p=1
	while not html_length:
		html_file_src=glob.glob("%s/*.html" % output)
		html_length=len(html_file_src)
		# print('test')
		# for c in pobj.children(recursive=True):
		# 	c.kill()
		for proc in psutil.process_iter():
			if proc.name() == 'Acrobat.exe':
				mem_info=int(proc.memory_info().rss / 1024 /1024)
				time.sleep(1)
				mem_tmp=int(proc.memory_info().rss / 1024 /1024)
				a=1
				while True:
					mem_info=int(proc.memory_info().rss / 1024 /1024)
					time.sleep(1)
					print(a)
					print('目前内存占用: %dM' % mem_info)
					mem_tmp=int(proc.memory_info().rss / 1024 /1024)
					if not abs(mem_tmp-mem_info):
						a+=1
					else:
						a=0
					if a > 60:
						print('目前内存占用: %dM' % mem_info)
						sub_c.kill()
						p=os.system("taskkill /f /im Acrobat.exe")
						print('该pdf无法解析，Acrobat进程已kill')
						break
					if(mem_info > 2000):
					# 测试使用120
					# if(proc.memory_info().rss / 1024 /1024 > 120):
					# if(proc.memory_info().rss > 104857600):
					# if(proc.memory_info().rss):
						print('目前内存占用: %dM' % mem_info)
						sub_c.kill()
						p=os.system("taskkill /f /im Acrobat.exe")
						print('该pdf解析使用内存过多，Acrobat进程已kill')
						break
		if a > 60:
			break
		time.sleep(2)
		if p == 0:
			break
		# html_list=html_file_src[0].split("\\")[1]
		# if html_length > 0:
		# 	shutil.move("%s/%s" % (output,html_list),"%s/%s" % (folder,html_list))
	end_t=datetime.now()
	spend_t=(end_t - start_t).seconds/60
	print('解析花费: %s 分钟' % spend_t)
	html_file_src=glob.glob("%s/*.html" % output)
	html_length=len(html_file_src)
	if a < 60:
		if p !=0:
			html_list=html_file_src[0].split("\\")[1]
			if html_length > 0:
				sub_c.kill()
				shutil.move("%s/%s" % (output,html_list),"%s/%s" % (folder,html_list))
			
			#移动文件计1s
			time.sleep(2)
			# 如果有html就不进入下一个循环
			html_file=glob.glob("%s/*.html" % folder)
			html_length=len(html_file)
			while html_length:
				html_file=glob.glob("%s/*.html" % folder)
				html_length=len(html_file)
		else:
			break
	else:
		break

	# 如果pdf名字没变就不进入下一个循环
	pdf_file_con=glob.glob("%s/*.pdf" % folder)
	pdf_con_length=len(pdf_file_con)
	while not pdf_con_length:
		pdf_file_con=glob.glob("%s/*.pdf" % folder)
		pdf_con_length=len(pdf_file_con)
	pdf_file_con=glob.glob("%s/*.pdf" % folder)
	pdf_list_con=pdf_file_con[0].split("\\")[1]
	while pdf_list_con == pdf_list:
		print('pdf名字没变,目前还是:',pdf_list_con)
		pdf_file_con=glob.glob("%s/*.pdf" % folder)
		pdf_list_con=pdf_file_con[0].split("\\")[1]
		time.sleep(5)