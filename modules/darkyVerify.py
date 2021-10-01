import os
import xml.etree.ElementTree as ET
import requests
import datetime
from modules import darkyExceptions
import vk_api

class darky_verify: #система верификации пользователя
	
	def check(vk, id, dayscheck=0, groupcheck=[], path=None): #проверка количества друзей, групп и тд.
		#id - int, идентификатор пользователя, должен быть больше 0
		#dayscheck - int, параметр проверки длительности существования аккаунта(0 - выкл.)
		#args - list, список элементов которые нужно проверить
		#path - str, путь к папке с ботом
		if id > 0:
			if groupcheck != []:
				for i in range(len(groupcheck)):
					#проверка наличия пользователя в группе
					if vk.groups.isMember(group_id=groupcheck[i], user_id=id) == 0:
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
			return True
		else:
			raise darkyExceptions.DarkyError(8)
	
	def display_settings(verify_sys):
		result = '⚙️Настройки системы DarkyVerify:\n'
		result += '🔹Статус: ' + str(verify_sys["status"]).replace('True', '✅Вкл.').replace('False', '❌Выкл.') + '\n'
		result += '🔹Наказание: ' + verify_sys["punishment"].replace('kick', '❕Кик❕').replace('ban', '❗Бан❗') + '\n'
		result += '🔹Насколько давно должен быть создан аккаунт:\nНе менее ' + str(verify_sys["days_check"]) + ' дней назад\n'
		if verify_sys["group_check"] != []:
			result += '🔹Участник должен быть в '
			if len(verify_sys["group_check"]) > 1:
				result += 'группах: \n'
			else:
				result += 'группе: \n'
			for i in range(len(verify_sys["group_check"])):
				result += 'https://vk.com/club' + str(verify_sys["group_check"][i]) + '\n'
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
			if param_name == "group_check" and param_value not in ["-", ".", 0, False]:
				if "," in param_value:
					param_value_list = param_value.split(',')
				else:
					param_value_list = [param_value]
				if len(param_value_list) > 4:
					raise darkyExceptions.DarkyError(504)
				param_value = []
				for i in range(len(param_value_list)):
					if '/' in param_value_list[i]:
						param_value_cache = param_value_list[i].split('/')[-1].replace(' ', '')
					else:
						param_value_cache = param_value_list[i].replace(' ', '')
					try:
						group_id_cache = vk.groups.getById(group_id=param_value_cache)[0]["id"]
						param_value.append(group_id_cache)
					except vk_api.exceptions.ApiError as exc:
						if exc.code == 100:
							raise darkyExceptions.DarkyError(503)
			elif param_name == "group_check" and param_value in ["-", ".", 0, False]: #отключение параметра group_check
				param_value = []
			#сравнение классов старого и нового значений
			if type(param_value) == type(verify_sys[param_name]):
				#проверка доступности значений
				if param_name == "days_check":
					if param_valye not in range(1, 7):
						raise darkyExceptions.DarkyError(502)
				if param_name == "punishment":
					if param_value not in ["kick", "ban"]:
						raise darkyExceptions.DarkyError(502)
				verify_sys[param_name] = param_value
				return verify_sys
			else:
				raise darkyExceptions.DarkyError(501)
		else:
			raise darkyExceptions.DarkyError(500)
