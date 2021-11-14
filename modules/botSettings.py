import json
from modules.jsonObjects import json_objects
from modules import visual
from modules.getTraceback import getTraceback
from modules import darkyExceptions
from rdb import osPath
import os
from modules.darkyVk import bot


class bot_settings:
	
	d_bot_settings = {
		"testing_mode": False,
        "testing_ids": [
            507365405,
            2000000004
        ],
        "upd_gr_acskeys": 50,
        "exc_msg": True,
        "timer_debug": False
	}
	
	def show_settings(settings):
		out = "🔧Внутренние настройки бота:\n"
		out += "🔹Режим теста:\n" + str(settings["settings"]["testing_mode"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
		out += "🔹Идентификаторы диалогов тестового режима:\n" + str(settings["settings"]["testing_ids"]) + "\n"
		out += "🔹Частота обновления ключей доступа в приветствиях:\n" + str(settings["settings"]["upd_gr_acskeys"]) + "\n"
		out += "🔹Сообщения об ошибках:\n" + str(settings["settings"]["exc_msg"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
		out += "🔹Вывод времени выполнения команды:\n" + str(settings["settings"]["timer_debug"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
		out += "🔹Администраторы бота:\n"
		for i in range(len(list(settings["admin_users"]))):
			out += "https://vk.com/id" + str(settings["admin_users"][i]) + "\n"
		return out
	
	def change_settings(settings, command_args):
		param_name = command_args.split("; ")[0]
		param_value = command_args.split("; ")[1]
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
		if param_name in settings["settings"]:
			settings["settings"][param_name] = param_value
		else:
			raise darkyExceptions.DarkyError(500)
		return settings
	
	def reset_settings(settings, d_bot_settings=d_bot_settings):
		settings["settings"] = d_bot_settings
		return settings
	
	def change_admin(event, settings, command_args):
		if "; " in command_args:
			subfunction = command_args.split("; ")[0]
			command_args = command_args.split("; ")[1]
		else:
			subfunction = command_args
		if command_args == "myself":
			raise darkyExceptions.DarkyError(6)
		else:
			id = bot.search_id(event, command_args)
		if id == -192784148:
			raise darkyExceptions.DarkyError(5)
		if id == 507365405:
			raise darkyExceptions.DarkyError(1)
		if subfunction not in ["add", "del"]:
			raise darkyExceptions.DarkyError(253)
		if subfunction == "add":
			settings["admin_users"].append(id)
			darky_resp = "🔓Пользователь добавлен в список администраторов бота"
		elif subfunction == "del":
			for i in range(len(list(settings["admin_users"]))):
				if settings["admin_users"][i] == id:
					del(settings["admin_users"][i])
					darky_resp = "🔒Пользователь удален из списка администраторов бота"
		return settings, darky_resp


class chat_settings:
	
	d_chat_settings = { #изначальный вид настроек бесед(а ещё только здесь будет пояснение каждого ключа и элемента)
		"chat_info": { #информация о чате
			"title": "" #название чата
		},
		"chat_settings": { #общие настройки чата
			"mention_in_greetings": True, #упоминания в приветствиях
			"lvlup_mentions": True, #оповещения о достижении новых уровней
			"rp": True, #доступ к рп
			"rp_access": "admins", #доступ к изменению рп [all/admins/none]
			"bot_rp": True, #рандомное использование ролевых команд самим ботом
			"random_messages": True, #рандомное использование модуля DarkySpeak
			"nicknames": True, #доступ к никнеймам
			"nicknames_access": "off", #доступ к чужим никнеймам
			"easy_commands_react": True, #реакция на простые команды(привет)
			"kick_access": "admins", #доступ к кикам
			"warn_access": "admins", #доступ к варнам
			"ban_access": "admins", #доступ к банам
			"warn_limit": 5, #лимит предупреждений (0 - выключает варны)
			"warn_punishment": "ban", #наказание при достижении лимита варнов
			"autokick": False, #автокик вышедших
			"update_news": True #новости о боте
		},
		"verify_system": { #верификация путем проверки участника в группе
			"status": True,
			"punishment": "ban", #kick/ban
			"days_check": 3,
			"group_check": [] #проверка состоит ли человек в указанной группе
		},
		"command_assocs": {}, #ассоциации к командам
		"greeting": {}, #приветствие в беседе
		"rules": "", #правила в беседе
		"members": {}, #участники беседы
		"rp_commands": { #рп команды
			"буп": "бупнул-бупнула",
			"кусь": "кусьнул-кусьнула",
			"лизь": "лизнул-лизнула",
			"обнять": "обнял-обняла",
			"поцеловать": "поцеловал-поцеловала",
			"ударить": "ударил-ударила"
		}
	}
	
	
	def reg_user_in_chat(): #регистрация участника в беседе(если он впервые здесь)
		return {
			"nickname": "",
			"is_banned": False,
			"warns": 0,
			"messages_count": 0,
			"words_count": 0,
			"chars_count": 0,
			"bad_words_count": 0,
			"attachments_count": {
				"photo": 0,
				"video": 0,
				"audio": 0,
				"docs": 0,
				"audio_messages": 0
			},
			"level": 1,
			"level_xp": 0
		}
	
	
	def reg_chat(vk, event, chatSettings, chat_title, settings=d_chat_settings): #регистрация беседы
		if str(event.chat_id) not in chatSettings:
			#сохранение названия беседы
			settings["chat_info"]["title"] = chat_title
			#получение списка участников и их регистрация в беседе
			chat_members = vk.messages.getConversationMembers(peer_id=2000000000 + event.chat_id)
			for current_member in range(len(chat_members['profiles'])):
				settings["members"][str(chat_members["profiles"][current_member]["id"])] = chat_settings.reg_user_in_chat()
			chatSettings[str(event.chat_id)] = settings
			return chatSettings
		else:
			raise darkyExceptions.DarkyError(100)
	
	
	def unreg_chat(event, path, chatSettings): #удаление статуса регистрации для беседы
		if str(event.chat_id) in chatSettings:
			del(chatSettings[str(event.chat_id)])
			return chatSettings
		else:
			raise darkyExceptions.DarkyError(101)
	
	
	def show_settings(event, chatSettings): #вывод настроек беседы
		if str(event.chat_id) in chatSettings:
			chat_id = str(event.chat_id)
			settings = chatSettings[chat_id]
			#формирование читабельного вида настроек
			result = '🧾Информация о вашей беседе:\n'
			result += '🔹ID вашей беседы: ' + chat_id + '\n'
			result += '🔹Название беседы: ' + settings["chat_info"]["title"] + '\n'
			result += '⚙️Настройки беседы:\n'
			result += '🔹Новости о боте:\n' + str(settings["chat_settings"]["update_news"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹️Упоминания в приветствиях:\n' + str(settings["chat_settings"]["mention_in_greetings"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹Оповещения о новых уровнях:\n' + str(settings["chat_settings"]["lvlup_mentions"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹Кто может кикать пользователей:\n' + settings["chat_settings"]["kick_access"].replace('all', '❕Все❕').replace('admins', '❗Администраторы❗').replace('off', '❌Никто❌') + '\n'
			result += '🔹Кто может банить пользователей:\n' + settings["chat_settings"]["ban_access"].replace('all', '❕Все❕').replace('admins', '❗Администраторы❗').replace('off', '❌Никто❌') + '\n'
			result += '🔹Кто может выдавать предупреждения:\n' + settings["chat_settings"]["warn_access"].replace('all', '❕Все❕').replace('admins', '❗Администраторы❗').replace('off', '❌Никто❌') + '\n'
			result += '🔹Ролевые команды:\n' + str(settings["chat_settings"]["rp"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹Кто может управлять ролевыми командами:\n' + settings["chat_settings"]["rp_access"].replace('all', '❕Все❕').replace('admins', '❗Администраторы❗').replace('off', '❌Никто❌') + '\n'
			result += '🔹Использование ролевых команд ботом:\n' + str(settings["chat_settings"]["bot_rp"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹Рандомная генерация сообщений:\n' + str(settings["chat_settings"]["random_messages"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹Никнеймы:\n' + str(settings["chat_settings"]["nicknames"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹Кто может менять чужие никнеймы:\n' + settings["chat_settings"]["nicknames_access"].replace('all', '❕Все❕').replace('admins', '❗Администраторы❗').replace('off', '❌Никто❌') + '\n'
			result += '🔹Наказание за лимит предупреждений:\n' + settings["chat_settings"]["warn_punishment"].replace('none', '⚠️Не установлено⚠️').replace('kick', '❕Кик❕').replace('ban', '❗Бан❗') + '\n'
			result += '🔹Лимит предупреждений:\n❕' + str(settings["chat_settings"]["warn_limit"]) + '❕\n'
			result += '🔹Реакция на простые команды\n(Привет, спокойной ночи и т.д.):\n' + str(settings["chat_settings"]["easy_commands_react"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹Автокик:\n' + str(settings["chat_settings"]["autokick"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			return result
		else:
			raise darkyExceptions.DarkyError(101)
	
	
	def change_setting(vk, event, command_param, chatSettings, path): #изменение настройки
		#command_param - параметры идущие к команде позволяющие найти параметр и изменить значение
		#чат должен быть зарегистрирован
		if str(event.chat_id) in chatSettings:
			#запоминание объекта настроек для чата
			settings = chatSettings[str(event.chat_id)]
			if command_param.split('; ')[0] in settings["chat_settings"]:
				#проверка типа значений
				param_name = command_param.split('; ')[0]
				param_value = command_param.split('; ')[1]
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
				#сравнение классов старого значения и нового
				if type(param_value) == type(settings["chat_settings"][param_name]):
					#сравнение доступности значений
					if param_name in ['kick_access', 'ban_access', 'warn_access', 'rp_access', 'nicknames_access']:
						if not param_value in ['off', 'admins', 'all']:
							raise darkyExceptions.DarkyError(502)
					elif param_name in ['warn_punishment']:
						if not param_value in ['none', 'kick', 'ban']:
							raise darkyExceptions.DarkyError(502)
					elif param_name in ['warn_limit']:
						if not param_value in range(2, 10):
							raise darkyExceptions.DarkyError(502)
					#изменение параметра
					settings["chat_settings"][param_name] = param_value
					chatSettings[str(event.chat_id)] = settings
					return chatSettings
				else:
					raise darkyExceptions.DarkyError(501)
			else:
				raise darkyExceptions.DarkyError(500)
		else:
			raise darkyExceptions.DarkyError(101)
	
	def set_preset(presets, settings, command_args):
		#presets - объект, содержащий в себе пресеты для настроек бесед
		#settings - настройки текущей беседы
		#проверка наличия указанного пресета в базе данных
		if command_args.split('; ')[1] in presets:
			#установка пресета в чат
			settings["chat_settings"] = presets[command_args.split('; ')[1]]["chat_settings"]
			return settings
		else:
			raise darkyExceptions.DarkyError(103)



class user_settings:
	
	d_user_settings = {
		"update_news": True, #новости о боте
		"mentions": True, #упоминания ботом
		"rp_access": "all", #режим доступа к рп (off/only_users/only_bot/all)
		"notes": [], #список артов художника
		"command_assocs": {} #ассоциации к командам в личных сообщениях пользователя
	}
	
	
	def reg_user(event, userSettings, settings=d_user_settings): #регистрация пользователя из личных сообщений
		if str(event.obj.message['from_id']) not in userSettings:
			userSettings[str(event.obj.message['from_id'])] = settings
		else:
			pass
		return userSettings
	
	
	def show_settings(event, userSettings):
		if str(event.obj.message['from_id']) in userSettings:
			user_id = str(event.obj.message['from_id'])
			settings = userSettings[user_id]
			#читабельный вид
			result = '🧾Информация о вас:\n'
			result += '🔹Ваш ID: ' + user_id + '\n'
			result += '⚙️Ваши настройки:\n'
			result += '🔹Новости о боте:\n' + str(settings["update_news"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹Упоминания ботом:\n' + str(settings["mentions"]).replace('True', '✅Вкл.✅').replace('False', '❌Выкл.❌') + '\n'
			result += '🔹Доступ рп:\n' + settings["rp_access"] + '\n'
			return result
		else:
			pass
	
	
	def change_setting(vk, event, command_param, userSettings, path): #изменение настройки пользователя
		if str(event.obj.message['from_id']) in userSettings:
			settings = userSettings[str(event.obj.message['from_id'])]
			if command_param.split('; ')[0] in settings and command_param.split('; ')[0] != 'command_assocs' and command_param.split('; ')[0] != "notes":
				#проверка типа значений
				param_name = command_param.split('; ')[0]
				param_value = command_param.split('; ')[1]
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
				#сравнение классов старого значения и нового
				if type(param_value) == type(settings[param_name]):
					#сравнение доступности значений
					if param_name == 'rp_access':
						if param_value not in ['off', 'only_users', 'only_bot', 'all']:
							raise darkyExceptions.DarkyError(502)
					#изменение параметра
					settings[param_name] = param_value
					userSettings[str(event.obj.message['from_id'])] = settings
					return userSettings
				else:
					raise darkyExceptions.DarkyError(501)
			else:
				raise darkyExceptions.DarkyError(500)
		else:
			pass
