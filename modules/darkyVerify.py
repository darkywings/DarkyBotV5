import os
import xml.etree.ElementTree as ET
import requests
import datetime
from modules import darkyExceptions

class darky_verify: #система верификации пользователя
	
	def check(vk, id, dayscheck=0, args='-photo-friends', groupcheck=0, path=None): #проверка количества друзей, групп и тд.
		#id - int, идентификатор пользователя, должен быть больше 0
		#dayscheck - int, параметр проверки длительности существования аккаунта(0 - выкл.)
		#args - list, список элементов которые нужно проверить
		#path - str, путь к папке с ботом
		if id > 0:
			if groupcheck != 0:
				#проверка наличия пользователя в группе
				if vk.groups.isMember(group_id=groupcheck, user_id=id) == 0:
					raise darkyExceptions.DarkyError(304)
			#обработка xml перед сохранением в файл ибо при парсинге возникали ошибки
			doc = requests.get('https://vk.com/foaf.php?id=' + str(id))
			doc = doc.text.replace('--', '').replace('<foaf:Image', '<!--?<foaf:Image').replace('</foaf:Image>', '</foaf:Image>?-->').replace('И', 'и')
			with open(path + '/foaf.xml', 'w') as xmldoc:
				xmldoc.write(doc)
				xmldoc.close()
			user = ET.ElementTree(file=path + '/foaf.xml').getroot()
			os.remove(path + '/foaf.xml')
			if dayscheck != 0:
				#парсинг даты регистрации
				for i in user.iter('{http://blogs.yandex.ru/schema/foaf/}created'):
					reg_date = i.attrib['{http://purl.org/dc/elements/1.1/}date']
				reg_date = reg_date.split('T')[0].split('-')
				#получение текущей даты
				curr_date = datetime.datetime.now().strftime('%Y-%m-%d').split('-')
				#вычисление разницы в датах
				#проверка разницы в годах
				if int(curr_date[0]) - int(reg_date[0]) < 1:
					#проверка разницы в месяцах
					if int(curr_date[1]) - int(reg_date[1]) < 1:
						#проверка дней
						if int(curr_date[2]) - int(reg_date[2]) < dayscheck:
							raise darkyExceptions.DarkyError(300)
			if '-photo' in args:
				#проверка аватарки
				if '<foaf:img>' not in doc:
					raise darkyExceptions.DarkyError(301)
			if '-friends' in args:
				#проверка количества друзей
				friends_count = 0
				if '<ya:friendsCount>' in doc:
					for i in user.iter('{http://blogs.yandex.ru/schema/foaf/}friendsCount'):
						friends_count = i.text
					if int(friends_count) < 5:
						raise darkyExceptions.DarkyError(302)
			return True
		else:
			raise darkyExceptions.DarkyError(8)
	
	def display_settings(verify_sys):
		result = '⚙️Настройки системы DarkyVerify:\n'
		result += '🔹Статус: ' + str(verify_sys["status"]).replace('True', '✅Вкл.').replace('False', '❌Выкл.') + '\n'
		result += '🔹Наказание: ' + verify_sys["punishment"].replace('kick', '❕Кик❕').replace('ban', '❗Бан❗') + '\n'
		result += '🔹Насколько давно должен быть создан аккаунт:\nНе менее ' + str(verify_sys["days_check"]) + ' дней назад\n'
		if verify_sys["group_check"] != 0:
			result += '🔹Участник должен быть в группе: \nhttps://vk.com/club' + str(verify_sys["group_check"]) + '\n'
		if verify_sys["info_check"] != ".":
			result += '🔹Дополнительные поля проверки:\n'
			result += verify_sys["info_check"]
		return result
	
	def change_setting(vk, verify_sys, command_args): #управление настройками DarkyVerify
		#проверка наличия указанного параметра
		if command_args.split('; ')[0] in verify_sys:
			param_name = command_args.split('; ')[0]
			param_value = command_args.split('; ')[1]
			#проверка сходств классов значений
			#проверка параметра на сходство с boolean
			if param_value.lower() in ['true', 'false']:
				if param_value.lower() == 'true':
					param_value = True
				elif param_value.lower() == 'false':
					param_value = False
			#проверка параметра на сходство с integer
			elif param_value.isdigit() == True:
				param_value = int(param_value)
			else:
				param_value = str(param_value)
			#определение идентификатора группы для group_check если было передано короткое имя или ссылка
			if param_name == "group_check" and type(param_value) != type(0):
				if '/' in param_value:
					param_value = param_value.split('/')[-1]
				try:
					param_value = vk.groups.getById(group_id=param_value)[0]["id"]
				except vk_api.exceptions.ApiError as exc:
					if exc.code == 100:
						raise darkyExceptions.DarkyError(503)
			#сравнение классов старого и нового значений
			if type(param_value) == type(verify_sys[param_name]):
				#проверка доступности значений
				if param_name == "days_check":
					if param_valye not in range(1, 7):
						raise darkyExceptions.DarkyError(502)
				if param_name == "punishment":
					if param_value not in ["kick", "ban"]:
						raise darkyExceptions.DarkyError(502)
				elif param_name == "info_check":
					info_chk_prms = ""
					if "photo" in param_value.lower():
						info_chk_prms += "-photo"
					if "friends" in param_value.lower():
						info_chk_prms += "-friends"
					if "." in param_value.lower():
						info_chk_prms = ""
				verify_sys[param_name] = info_chk_prms
				return verify_sys
			else:
				raise darkyExceptions.DarkyError(501)
		else:
			raise darkyExceptions.DarkyError(500)
