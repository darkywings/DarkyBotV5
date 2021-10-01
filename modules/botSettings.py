import json
from modules.jsonObjects import json_objects
from modules import visual
from modules.getTraceback import getTraceback
from modules import darkyExceptions
from rdb import osPath
import os


class bot_settings:
	
	def optionValue_visual(option):
		out = ''
		if str(option) == '':
			option = 'null'
		elif option == True:
			out = '✅'
		elif option == False:
			out = '❌'
		else:
			out = '❕'
		out += str(option) + out
		return out
	
	
	def reset(botSettings_m, path): #сброс настроек бота
		#botSettings_m - обьект которыц будет записываться
		#path - путь к json файлу, в который будет записан обьект настроек
		json_objects.write(botSettings_m, path) #запись в json
		path_botSettings = path #запись пути к файлу в path_botSettings
		return path_botSettings
	
	
	def init(botSettings_m): #инициализация настроек бота
		#botSettings_m - object, обьект с которым будут сравниваться настройки бота.
		debug = ''
		botSettings = {}
		path_botSettings = osPath + '/bot_files/bot_mainSettings.json'
		#поиск файла настроек в директории бота
		if os.path.exists(path_botSettings) == True:
			try:
				#загрузка настроек из файла
				botSettings, debug = json_objects.load(path_botSettings)
			#проверка наличия создателя в разрешённых пользователях
				if botSettings['admin_users'][0] == 507365405:
					#проверка наличия параметров из списка settingsList в настройках бота
					#при отсутствии какого либо параметра этот параметр будет добавлен автоматически
					settingsNameList = ['debug', 'upd_gr_acskeys', 'upd_gr_acskeys_msg', 'reconnect_msg', 'exc_msg', 'snd_msgs', 'command_assoc'] #список параметров, что нужно проверить
					settingsValueList = [0, 20, True, True, True, [], {}]
					curEl = 0
					while curEl < len(settingsNameList):
						if settingsNameList[curEl] in botSettings["settings"]:
							curEl += 1
						else:
							botSettings["settings"][settingsNameList[curEl]] = settingsValueList[curEl]
							curEl += 1
					json_objects.write(botSettings, path_botSettings)
					print(visual.coloredText('Инициализация настроек бота завершена', bgColor='cian'))
				else:
					#установка списка разрешенных пользователей в исходное состояние
					#по причине того, что создатель не был найден в этом списке в первую очередь
					botSettings["admin_users"] == botSettings_m["admin_users"]
					json_objects.write(botSettings, path_botSettings)
					print(visual.coloredText('Список разрешённых пользователей восстановлен в исходное состояние', 'red'))
			except:
				#в целях "обезопасить" другие части кода настроки возвращаются в дефолтный вид
				path_botSettings = bot_settings.reset(botSettings_m, path_botSettings)
				print(visual.coloredText('Настройки установлены в исходное состояние из-за ошибки в них', 'red'))
				print(getTraceback(0))
		else:
			#при отстутствии файла он будет создан с дефолтными параметрами
			path_botSettings = bot_settings.reset(botSettings_m, path_botSettings)
			print(visual.coloredText('Файл настроек сброшен к стандартным параметрам', 'red'))
		return path_botSettings
	
	
	def read(path): #простое считывание настроек
		#path - путь до файла настроек
		#botSettings_m - оригинал настроек
		try:
			object = json_objects.load(path)
		except:
			raise darkyExceptions.ReadBotSettingsExc
		return object



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
		"members": { #участники беседы
			"507365405": {
				"nickname": "Дарки", #никнейм пользователя
				"is_banned": False, #забанен ли пользователь
				"warns": 0, #предупреждения у пользователя
				"messages_count": 0, #количество сообщений
				"words_count": 0, #количество написанных им слов
				"chars_count": 0, #количество символов написанных пользователем
				"attachments_count": {
					"photo": 0, #количество отправленных фото
					"video": 0, #количество отправленных видео
					"audio": 0, #количество отправленных аудио
					"docs": 0, #количество отправленных документов
					"audio_messages": 0 #количество отправленных голосовых сообщений
				},
				"bad_words_count": 0, #количество использованного им мата
				"level": 1, #уровень пользователя
				"level_xp": 0 #опыт пользователя
			}
		},
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
	
	
	def reg_chat(vk, event, path, chat_title, settings=d_chat_settings): #регистрация беседы
		#path - должен быть BOT_CHATSETTINGS, это путь к настройкам всех бесед
		chatSettings = json_objects.load(path)
		if str(event.chat_id) not in chatSettings:
			#сохранение названия беседы
			settings["chat_info"]["title"] = chat_title
			#получение списка участников и их регистрация в беседе
			chat_members = vk.messages.getConversationMembers(peer_id=2000000000 + event.chat_id)
			for current_member in range(len(chat_members['profiles'])):
				settings["members"][str(chat_members["profiles"][current_member]["id"])] = chat_settings.reg_user_in_chat()
			chatSettings[str(event.chat_id)] = settings
			json_objects.write(chatSettings, path)
			return chatSettings
		else:
			raise darkyExceptions.DarkyError(100)
	
	
	def unreg_chat(event, path, chatSettings): #удаление статуса регистрации для беседы
		if str(event.chat_id) in chatSettings:
			del(chatSettings[str(event.chat_id)])
			json_objects.write(chatSettings, path)
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
					json_objects.write(chatSettings, path)
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
	
	
	def reg_user(event, path, settings=d_user_settings): #регистрация пользователя из личных сообщений
		userSettings = json_objects.load(path)
		if str(event.obj.message['from_id']) not in userSettings:
			userSettings[str(event.obj.message['from_id'])] = settings
			json_objects.write(userSettings, path)
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
					json_objects.write(userSettings, path)
					return userSettings
				else:
					raise darkyExceptions.DarkyError(501)
			else:
				raise darkyExceptions.DarkyError(500)
		else:
			pass
