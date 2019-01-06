 # Скачиваем иконки с сайта http://viks.tv/tv_sputnikovye_kanaly
import requests
from bs4 import BeautifulSoup
import os

folfer = "./logo_viks.tv/"								#путь к папке (начинаться должна с './' и в конце '/')
url_site = 'http://viks.tv/tv_sputnikovye_kanaly'			#сайт с которого парсим иконки и имена каналов для них
name_site = 'http://viks.tv'							#имя сайта для создания полного пути к картинке для скачивания
response = requests.get(url_site)
html = response.content
soup = BeautifulSoup(html, 'lxml')
nav_l=[]												#список ссылок навигации по разделу (страницы)
nav_all = []											#список ссылок навигации по разделу  без повторов (страницы)
nav_l.append(url_site)								#добавляем первую ссылку (страница раздела)
img_list = []											#список названия канала и ссылки на логотип
REQUEST_STATUS_CODE = 200						#Константа запроса к сайту с ответом 200 (для проверки доступа к ресурсу)

#поиск ссылок 
def url_nav():
	nav = soup.find_all('div', class_='naviiiiiiii')
	for n in nav:
		url = n.find_all('a')
		for href in url:
			url2 = href.get('href')
			nav_l.append(url2)
	nav_all= list(set(nav_l))
	#print(url_nav)
	return nav_all
		
		
#добавление имени канала и ссылки на картинку в список img_list
def logo_all():

	list_page = url_nav()
	for page in list_page:
		response = requests.get(page)
		html = response.content
		soup = BeautifulSoup(html, 'lxml')
		logo_all = soup.find_all('div', class_='all_tv')
	
		for logo in logo_all:
			tv_name = logo.find('span').text					#название канала
			img = logo.find('img').get('src')						#ссылка на логотип канала
			url_img = name_site + img						#полный путь к картинке (логотипу)
			r = img.rfind('.')									#определяем где находится '.' для отделения расширения типа файла
			raw = img[r:]										#получаем расширение файла
			full_name_new = tv_name + raw					#новое имя файла с расширение (имя из тега ''span'' и расширение 'raw')
			img_list.append((tv_name, url_img, full_name_new))					#добавляем в списко имя, ссулку расширение файла

def  download_logo():
	#Скачиваем иконки с сайта http://viks.tv/tv_sputnikovye_kanaly
	a=0
	for num in img_list:
		a+=1
		#img_list
		# 0 - название канала из тега на сайте
		# 1 - относительный путь к картинке /uploads/posts/2016-05/1463477891_rossiya-rtr.png
		# 2 - новое имя img_list[2]
		
		if  os.path.isdir(folfer):								#проверяем существование папки
			url = num[1]										#Путь к иконке на сайте
			patch = folfer + str(num[2])						#Путь к папке и новое имя иконки логотипа
			#print(patch)
			send=requests.get(url) 

			if send.status_code == REQUEST_STATUS_CODE:	#Получаем ответ от сайта 200 (REQUEST_STATUS_CODE = 200) тогда выполняемсохранение
				with open (patch,'wb') as f:
					f.write(send.content)
					print('Иконка №' + str(a)  + ' -  ' + num[2]  )
		else:
	
			os.mkdir(folfer)									#Создаем папку (путь в переменной 'folfer')
			print('Папка созданна - ' + folfer)					#Выводим путь папки
			download_logo()									#Запускаем функцию по новой

	
	
#------------------
url_nav() 			#Находим все ссылки из навигации страниц 
logo_all()			#Записываем имена, ссылки на иконку  и новое имя иконки в список ''mg_list''
download_logo()		#Скачиваем и сохраняем иконки на основании списка ''img_list''


	
	

