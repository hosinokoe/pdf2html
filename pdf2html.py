import glob,os,time,shutil,psutil,subprocess

# folder="//192.168.18.72/share/04_Application/shared_pdf_2"
folder="//192.168.18.72/share/04_Application/tmp/shared_pdf_1"
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
	cmd_p="e:/tools/ADPRP/APDFPR.EXE -batch %s/%s -q" % (folder,pdf_list)
	command="c:/bin/PDFConvert.exe -i %s/%s -o %s -f html" % (folder,pdf_list,output)
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
	sub_c=subprocess.Popen(command)
	time.sleep(5)

	html_file_src=glob.glob("%s/*.html" % output)
	html_length=len(html_file_src)

	# html_list=html_list=html_file_src[0].split("\\")[1]
	# 如果pdf没有解析成html，并且acrobat占用内存超过2500m就kill acrobat。解析完了就跳出循环
	while not html_length:
		html_file_src=glob.glob("%s/*.html" % output)
		html_length=len(html_file_src)
		# print('test')
		# for c in pobj.children(recursive=True):
		# 	c.kill()
		for proc in psutil.process_iter():
			if proc.name() == 'Acrobat.exe':
				if(proc.memory_info().rss / 1024 /1024 > 2500):
				# if(proc.memory_info().rss > 104857600):
				# if(proc.memory_info().rss):
					print(proc.memory_info().rss)
					sub_c.kill()
					os.system("taskkill /f /im Acrobat.exe")
		# html_list=html_file_src[0].split("\\")[1]
		# if html_length > 0:
		# 	shutil.move("%s/%s" % (output,html_list),"%s/%s" % (folder,html_list))
	html_file_src=glob.glob("%s/*.html" % output)
	html_length=len(html_file_src)
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

	# time.sleep(2)
	# 如果pdf名字没变就不进入下一个循环
	pdf_file_con=glob.glob("%s/*.pdf" % folder)
	pdf_con_length=len(pdf_file_con)
	while not pdf_con_length:
		pdf_file_con=glob.glob("%s/*.pdf" % folder)
		pdf_con_length=len(pdf_file_con)
	# pdf_file_con=glob.glob("%s/*.pdf" % folder)
	# pdf_list_con=pdf_file_con[0].split("\\")[1]
	# while pdf_list_con == pdf_list:
	# 	print(1)
	# 	pdf_file_con=glob.glob("%s/*.pdf" % folder)
	# 	pdf_list_con=pdf_file_con[0].split("\\")[1]