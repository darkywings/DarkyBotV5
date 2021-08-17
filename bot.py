#bot V5.0.0
##Darky-Bot by Darky(https://vk.com/id507365405)

#скрипт содержащий основную часть алгориимов бота для вк
		
print('\033[0m', end='')


print('Импорт модулей...')

try:
	#модуль, позволяющий немного улучшить визуал и иногда упростить его использование
	print('modules.visual', flush=True, end='')
	import modules.visual as visual
	#работа со vk api
	visual.reprint('vk_api')
	import vk_api
	#список стандартных команд бота
	visual.reprint('bot_files.cmd_list.command_list_default')
	from bot_files.cmd_list import command_list_default
	#пресеты настроек бота
	visual.reprint('bot_files.cmd_list.chat_settings_presets')
	from bot_files.cmd_list import chat_settings_presets
	#возврат трейсбека
	visual.reprint('modules.getTraceback')
	from modules.getTraceback import getTraceback
	#работа с главными настройками бота
	visual.reprint('modules.botSettings')
	from modules.botSettings import bot_settings, chat_settings, user_settings
	#большинство основных команд бота
	visual.reprint('commands')
	from modules import commands
	#работа с json-обьектами
	visual.reprint('modules.jsonObjects')
	from modules.jsonObjects import json_objects
	#работа с ассоциациями команд
	visual.reprint('modules.assocs')
	from modules.assocs import command_assocs
	#исключения Дарки
	visual.reprint('modules.darkyExceptions')
	from modules import darkyExceptions
	#функции Дарки для работы с vk api
	visual.reprint('modules.darkyVk')
	from modules.darkyVk import bot
	#реквесты для работы с api
	visual.reprint('requests')
	import requests
	#работа со временем
	visual.reprint('time')
	import time
	#операции с os
	visual.reprint('os')
	import os
	#работа с системой DarkyRandomGeneratingText
	visual.reprint('modules.drgt')
	from modules.drgt import drgt
	#получение событий от vk api
	visual.reprint('vk_api.bot_longpoll')
	from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
	#получение важных элементов для работы бота
	visual.reprint('rdb')
	import rdb
	#система верификации
	visual.reprint('modules.darkyVerify')
	from modules.darkyVerify import darky_verify
	#работа с рандомом
	visual.reprint('random')
	import random
	OS_PATH = rdb.osPath #путь к папке с ботом
	ACCESS_TOKEN = rdb.accessToken #ключ доступа к сообществу вк(чтобы бот мог взаимодействовать с vk_api)
	visual.reprint(visual.coloredText('Модули успешно импортированы', 'black', 'cian'), True)
except:
	visual.reprint(visual.coloredText('Ошибка импорта модулей!', 'white', 'red'), True)
	print(visual.coloredText(getTraceback(0), 'red'))
	raise SystemExit



print('Проверка наличия файлов и папок...')

visual.reprint('Инициализация путей к файлам...')
BOT_SETTINGS = OS_PATH + 'bot_files/bot_mainSettings.json'
BOT_INFO = OS_PATH + 'bot_files/bot_info.json'
BOT_MESS = OS_PATH + 'mess'
BOT_CHATSETTINGS = OS_PATH + 'bot_files/chats.json'
BOT_USERSETTINGS = OS_PATH + 'bot_files/users.json'

files_list = [BOT_SETTINGS, BOT_INFO, BOT_MESS, BOT_CHATSETTINGS, BOT_USERSETTINGS] #список файлов и папок

for current_file in range(len(files_list)):
	if os.path.exists(files_list[current_file]) == True:
		visual.reprint('Проверка существования необходимых файлов/папок: ' + files_list[current_file].split('/')[-1])
	else:
		visual.reprint(visual.coloredText('Файл/папка отсутствует', 'white', 'red'), True)
		print(visual.coloredText(files_list[current_file], 'red'))
		if not '.' in files_list[current_file]:
			visual.reprint(visual.coloredText('Создание папки...', 'cian'))
			os.mkdir(files_list[current_file])
			visual.reprint(visual.coloredText('Папка создана', 'cian'), True)
		else:
			print(visual.coloredText('Завершение работы...', bgColor='red'))
			raise SystemExit
visual.reprint(visual.coloredText('Необходимые файлы и папки были найдены', 'black', 'cian'), True)



print('Считывание настроек бота...')
try:
	botSettings = bot_settings.read(BOT_SETTINGS)
except darkyExceptions.ReadBotSettingsExc:
	print(visual.coloredText('Ошибка чтения настроек бота. Завершение работы...', 'white', 'red'))
	raise SystemExit



print('Авторизация...')
try:
	botlongpoll, vk = bot.auth(192784148, ACCESS_TOKEN)
	print(visual.coloredText('Авторизация прошла успешно', 'black', 'cian'))
except requests.exceptions.ConnectionError:
	print(visual.coloredText('Ошибка подключения к сети!', 'white', 'red'))
	raise SystemExit
except:
	print(visual.coloredText('Ошибка авторизации. Завершение работы...', 'white', 'red'))
	print(getTraceback(0))
	raise SystemExit



def check_assocs(message): #автоматизированный вызов функции проверяющий ассоциации к командам
	(command, command_args) = ('', '')
	try:
		if event.from_chat == True:
			command_assoc_list = chatSettings[str(event.chat_id)]["command_assocs"]
		elif event.from_user == True:
			command_assoc_list = userSettings[str(event.obj.message["from_id"])]["command_assocs"]
		command, command_args = command_assocs.check(message, command_assoc_list)
	except (darkyExceptions.DarkyError, KeyError):
		try:
			command, command_args = command_assocs.check(message, command_list_default)
		except darkyExceptions.DarkyError as exc:
			if exc.code == 51:
				(command, command_args) = ('', '')
	return command, command_args



def check_accss_to_command(command): #проверка доступности команды
	accss_grntd = False
	if event.from_chat == True and 'chats' in command_list_default['info'][command]['access']:
		accss_grntd = True
	elif event.from_user == True and 'users' in command_list_default['info'][command]['access']:
		accss_grntd = True
	return accss_grntd



def execute_command(command, command_args): #выполнение команды
	global chatSettings
	global userSettings
	darky_resp = ''
	darky_attachments = ''
	if command_args == '':
		args_count = 0
	else:
		args_count = len(command_args.split('; '))
	visual.print_botEvent(event, command + ' ' + command_args)
	if check_accss_to_command(command):
		if command == command_list_default['/darky reg']:
			if bot_is_admin == True:
				if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
					chatSettings = chat_settings.reg_chat(vk, event, BOT_CHATSETTINGS, chatObj[0]["chat_settings"]["title"])
					darky_resp = '✅Ваша беседа была зарегистрирована'
				else:
					raise darkyExceptions.DarkyError(3)
			else:
				raise darkyExceptions.DarkyError(2)
		elif command == '/darky exc':
			if command_args.split('; ')[0] == '2310':
				bot.send_mess(vk, event.obj.message["peer_id"], "Вызов исключения " + command_args.split('; ')[1] + "...")
				exc_name = command_args.split('; ')[1]
				if exc_name == "SystemExit":
					raise SystemExit
				elif exc_name == "TimeoutError":
					raise TimeoutError
				else:
					darky_resp = '⚠️Исключение не найдено'
			else:
				darky_resp = '⚠️Неверный пароль'
		elif command == command_list_default['/darky chat settings']:
			if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
				darky_resp = chat_settings.show_settings(event, chatSettings)
			else:
				raise darkyExceptions.DarkyError(3)
		elif command == command_list_default['/darky chat set']:
			if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
				if args_count == command_list_default['info'][command]['args_count']:
					if command_args.split('; ')[0] == "preset":
						chatSettings[str(event.chat_id)] = chat_settings.set_preset(chat_settings_presets, chatSettings[str(event.chat_id)], command_args)
						json_objects.write(chatSettings, BOT_CHATSETTINGS)
						darky_resp = '✅Пресет настроек ' + command_args.split('; ')[1] + ' успешно установлен в вашу беседу'
					else:
						chatSettings = chat_settings.change_setting(vk, event, command_args, chatSettings, BOT_CHATSETTINGS)
						darky_resp = '✅Настройка ' + str(command_args.split('; ')[0]) + ' изменена'
				else:
					raise darkyExceptions.DarkyError(250)
			else:
				raise darkyExceptions.DarkyError(3)
		elif command == command_list_default['/darky unreg']:
			if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
				chatSettings = chat_settings.unreg_chat(event, BOT_CHATSETTINGS, chatSettings)
				darky_resp = '❗Ваша беседа теперь не зарегистрирована. Большинство моего функционала более недоступно для этой беседы'
			else:
				raise darkyExceptions.DarkyError(3)
		elif command == command_list_default['/darky verify settings']:
			darky_resp = darky_verify.display_settings(verify_sys)
		elif command == command_list_default['/darky user settings']:
			darky_resp = user_settings.show_settings(event, userSettings)
		elif command == command_list_default['/darky user set']:
			if args_count == command_list_default['info'][command]['args_count']:
				userSettings = user_settings.change_setting(vk, event, command_args, userSettings, BOT_USERSETTINGS)
				darky_resp = '✅Настройка ' + str(command_args.split('; ')[0]) + ' изменена'
			else:
				raise darkyExceptions.DarkyError(250)
		elif command == command_list_default['/darky help']:
			darky_resp = '❔Руководство по использованию бота вы можете прочитать, перейдя по ссылке ниже:\nvk.com/@darkybot-help'
		elif command == command_list_default['/darky bug report']:
			if args_count == command_list_default['info'][command]['args_count']:
				bug_rep = '⚠️БАГ-РЕПОРТ!\nПользователь, сообщивший о баге:\n[id' + str(event.obj.message['from_id']) + '|' + vk.users.get(user_ids = event.obj.message['from_id'])[0]['first_name'] + ']\n'
				if event_from_chat == True:
					bug_rep += 'Идентификатор беседы:\n' + str(event.chat_id) + '\n'
				bug_rep += 'Текст репорта:\n' + command_args
				bot.send_mess(vk, botSettings["settings"]["snd_msgs"], bug_rep)
				darky_resp = '✅Ваш репорт был отправлен моим администраторам на рассмотрение. При необходимости они с вами свяжутся. Спасибо, что сообщили об ошибке в моей работе'
			else:
				raise darkyExceptions.DarkyError(250)
		elif command == command_list_default['/darky send m']:
			if args_count == command_list_default['info'][command]['args_count']:
				if event.obj.message['from_id'] in botSettings["admin_users"]:
					ids, darky_resp, darky_attachments = commands.main_commands.multiply_mess(command_args, chatSettings, userSettings)
					bot.send_mess(vk, ids, darky_resp, darky_attachments)
					darky_resp = '✅Сообщение разослано по указанным идентификаторам'
					darky_attachments = ''
				else:
					raise darkyExceptions.DarkyError(1)
			else:
				raise darkyExceptions.DarkyError(250)
		elif command == command_list_default['/darky choose']:
			darky_resp = commands.main_commands.choose(command_args)
		elif command == command_list_default['/darky prob']:
			darky_resp = commands.main_commands.probably(command_args)
		elif command == command_list_default['/darky try']:
			darky_resp = commands.main_commands.trying(command_args)
		elif command == command_list_default['/darky dist']:
			darky_resp = commands.main_commands.distort(command_args)
		elif command == command_list_default['/darky layout']:
			darky_resp = 'Текст с изменённой раскладкой:\n' + commands.main_commands.layout(command_args)
		elif command == command_list_default['/darky roll']:
			if not args_count > command_list_default['info'][command]['args_count']:
				darky_resp = commands.main_commands.roll(command_args)
			else:
				raise darkyExceptions.DarkyError(250)
		elif command == command_list_default['/darky random']:
			if args_count == command_list_default['info'][command]['args_count']:
				darky_resp = commands.main_commands.random_int(command_args)
			else:
				raise darkyExceptions.DarkyError(250)
		elif command == command_list_default['/darky speak']:
			if command_args == 'del data':
				darky_resp = drgt.del_data(event, BOT_MESS, event_from_chat)
			else:
				darky_resp = drgt.generate(event, BOT_MESS, event_from_chat)
		elif command == command_list_default['/darky notes']:
			if args_count >= command_list_default['info'][command]['args_count']:
				if command_args.split('; ')[0] in ["add", "del", "rename", "edit"]:
					if command_args.split('; ')[0] == "add":
						userSettings[str(event.obj.message["from_id"])]["notes"] = commands.notes.add(userSettings[str(event.obj.message["from_id"])]["notes"], command_args)
						json_objects.write(userSettings, BOT_USERSETTINGS)
						darky_resp = "✅Заметка внесена в список с идентификатором " + str(userSettings[str(event.obj.message["from_id"])]["notes"][-1]["id"])
					elif command_args.split('; ')[0] == "del":
						userSettings[str(event.obj.message["from_id"])]["notes"] = commands.notes.delete(userSettings[str(event.obj.message["from_id"])]["notes"], command_args)
						json_objects.write(userSettings, BOT_USERSETTINGS)
						darky_resp = "✅Заметка с идентификатором " + command_args.split('; ')[1] + ' - удалена'
					elif command_args.split('; ')[0] == "rename":
						userSettings[str(event.obj.message["from_id"])]["notes"] = commands.notes.rename(userSettings[str(event.obj.message["from_id"])]["notes"], command_args)
						json_objects.write(userSettings, BOT_USERSETTINGS)
						darky_resp = "✅Заметка с идентификатором " + command_args.split('; ')[1] + ' - переименнована'
					elif command_args.split('; ')[0] == "edit":
						userSettings[str(event.obj.message["from_id"])]["notes"] = commands.notes.edit(userSettings[str(event.obj.message["from_id"])]["notes"], command_args)
						json_objects.write(userSettings, BOT_USERSETTINGS)
						darky_resp = "✅Описание заметки с идентификатором " + command_args.split('; ')[1] + ' - изменено'
				else:
					darky_resp = commands.notes.get(userSettings[str(event.obj.message["from_id"])]["notes"], command_args)
			else:
				raise darkyExceptions.DarkyError(252)
		elif command == command_list_default['/darky assoc set']:
			if args_count == command_list_default['info'][command]['args_count']:
				if event_from_chat == True:
					if chat_is_registered == False:
						raise darkyExceptions.DarkyError(101)
					chatSettings[str(event.chat_id)]["command_assocs"] = command_assocs.add(chatSettings[str(event.chat_id)]["command_assocs"], command_args.split('; ')[0], command_args.split('; ')[1])
					json_objects.write(chatSettings, BOT_CHATSETTINGS)
				else:
					userSettings[str(event.obj.message['from_id'])]["command_assocs"] = command_assocs.add(userSettings[str(event.obj.message["from_id"])]["command_assocs"], command_args.split('; ')[0], command_args.split('; ')[1])
					json_objects.write(userSettings, BOT_USERSETTINGS)
				darky_resp = '✅Ассоциация для команды ' + command_args.split('; ')[0] + ' - установлена'
			else:
				raise darkyExceptions.DarkyError(250)
		elif command == command_list_default['/darky assoc del']:
			if args_count == command_list_default['info'][command]['args_count']:
				if command_args != 'all':
					if event_from_chat == True:
						if chat_is_registered == False:
							raise darkyExceptions.DarkyError(101)
						chatSettings[str(event.chat_id)]["command_assocs"] = command_assocs.remove(chatSettings[str(event.chat_id)]["command_assocs"], command_args)
						json_objects.write(chatSettings, BOT_CHATSETTINGS)
					else:
						userSettings[str(event.obj.message['from_id'])]["command_assocs"] = command_assocs.remove(userSettings[str(event.obj.message["from_id"])]["command_assocs"], command_args)
						json_objects.write(userSettings, BOT_USERSETTINGS)
					darky_resp = '✅Ассоциация ' + command_args + ' - удалена'
				else:
					if event_from_chat == True:
						if chat_is_registered == False:
							raise darkyExceptions.DarkyError(101)
						chatSettings[str(event.chat_id)]["command_assocs"] = {}
						json_objects.write(chatSettings, BOT_CHATSETTINGS)
					else:
						userSettings[str(event.obj.message["from_id"])]["command_assocs"] = {}
						json_objects.write(userSettings, BOT_USERSETTINGS)
					darky_resp = '✅Все ассоциации - удалены'
			else:
				raise darkyExceptions.DarkyError(250)
		elif str(event.chat_id) not in chatSettings:
			#вызов исключения связанный с беседой что незарегистрирована(всё что ниже выполняться в таком случае не будет)
			raise darkyExceptions.DarkyError(101)
		elif command == command_list_default['/darky greet']:
			if args_count <= command_list_default['info'][command]['args_count']:
				if command_args == 'set':
					if bot_is_admin == True:
						if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
							chatSettings = commands.greeting.set(vk, event, chatSettings)
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
							darky_resp = '✅Приветствие установлено'
						else:
							raise darkyExceptions.DarkyError(3)
					else:
						raise darkyExceptions.DarkyError(2)
				elif command_args == 'del':
					if bot_is_admin == True:
						if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
							chatSettings = commands.greeting.delete(event, chatSettings)
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
							darky_resp = '✅Приветствие удалено'
						else:
							raise darkyExceptions.DarkyError(3)
					else:
						raise darkyExceptions.DarkyError(2)
				elif command_args == 'upd att accsskey':
					if bot_is_admin == True:
						if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
							chatSettings = commands.greeting.upd_att_accsskey(vk, event, chatSettings)
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
							darky_resp = '✅Ключ доступа для прикреплённого в приветствии элемента - обновлён'
						else:
							raise darkyExceptions.DarkyError(3)
					else:
						raise darkyExceptions.DarkyError(2)
				else:
					darky_resp, darky_attachments = commands.greeting.display(event, chatSettings)
					#добавление упоминания человека перед приветствием
					if chatSettings[str(event.chat_id)]["chat_settings"]["mention_in_greetings"] == True:
						if userSettings[str(event.obj.message['from_id'])]["mentions"] == True:
							mention = '[id' + str(event.obj.message['from_id']) + '|' + vk.users.get(user_ids = event.obj.message['from_id'])[0]['first_name'] + ']'
						else:
							mention = vk.users.get(user_ids = event.obj.message['from_id'])[0]['first_name']
						darky_resp = mention + '\n' + darky_resp
					else:
						pass
		elif command == command_list_default['/darky rules']:
			if args_count <= command_list_default['info'][command]['args_count']:
				if command_args == 'set':
					if bot_is_admin == True:
						if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
							chatSettings = commands.rules.set(event, chatSettings)
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
							darky_resp = '✅Правила установлены'
						else:
							raise darkyExceptions.DarkyError(3)
					else:
						raise darkyExceptions.DarkyError(2)
				elif command_args == 'del':
					if bot_is_admin == True:
						if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
							chatSettings = commands.rules.delete(event, chatSettings)
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
							darky_resp = '✅Правила удалены'
						else:
							raise darkyExceptions.DarkyError(3)
					else:
						raise darkyExceptions.DarkyError(2)
				else:
					darky_resp = commands.rules.display(event, chatSettings)
			else:
				raise darkyExceptions.DarkyError(251)
		elif command == command_list_default['/darky kick']:
			if args_count <= command_list_default['info'][command]['args_count']:
				if bot_is_admin == True:
					if chatSettings[str(event.chat_id)]["chat_settings"]["kick_access"] == "off":
						raise darkyExceptions.DarkyError(10)
					elif chatSettings[str(event.chat_id)]["chat_settings"]["kick_access"] == "admins":
						if user_is_admin == False and event.obj.message['from_id'] not in botSettings['admin_users']:
							raise darkyExceptions.DarkyError(3)
					try:
						commands.chat.kick(vk, event, command_args, chatSettings)
						darky_resp = '✅Пользователь - исключён'
					except vk_api.exceptions.ApiError as exc:
						if exc.code == 15:
							raise darkyExceptions.DarkyError(11)
				else:
					raise darkyExceptions.DarkyError(2)
			else:
				raise darkyExceptions.DarkyError(251)
		elif command == command_list_default['/darky ban']:
			if args_count <= command_list_default['info'][command]['args_count']:
				if command_args == 'list':
					banned_list = commands.chat.get_banned_list(chatSettings[str(event.chat_id)]["members"])
					if banned_list == []:
						raise darkyExceptions.DarkyError(202)
					#формирование читабельного списка
					out = ''
					cui = 1
					users_info = vk.users.get(user_ids = banned_list)
					for i in range(len(banned_list)):
						#получение имени пользователя
						if str(banned_list[i]) in chatSettings[str(event.chat_id)]["members"]:
							username = chatSettings[str(event.chat_id)]["members"][str(banned_list[i])]["nickname"]
							if username == '' or chatSettings[str(event.chat_id)]["chat_settings"]["nicknames"] == False:
								username = users_info[i]['first_name'] + ' ' + users_info[i]['last_name']
						else:
							username = users_info[i]['first_name'] + ' ' + users_info[i]['last_name']
						#проверка можно ли упоминать его
						if str(banned_list[i]) in userSettings:
							if userSettings[str(banned_list[i])]["mentions"] == True:
								username = '[id' + str(banned_list[i]) + '|' + username + ']'
						else:
							username = '[id' + str(banned_list[i]) + '|' + username + ']'
						#запись в список
						out += str(cui) + '. ' + username + '\n'
						cui += 1
					darky_resp = '⛔Список забаненных в этой беседе:\n' + out
				else:
					if bot_is_admin == True:
						if chatSettings[str(event.chat_id)]["chat_settings"]["ban_access"] == "off":
							raise darkyExceptions.DarkyError(10)
						elif chatSettings[str(event.chat_id)]["chat_settings"]["ban_access"] == "admins":
							if user_is_admin == False and event.obj.message['from_id'] not in botSettings['admin_users']:
								raise darkyExceptions.DarkyError(3)
						try:
							chatSettings = commands.chat.ban(vk, event, command_args, chatSettings)
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
							darky_resp = '✅Пользователь - забанен'
						except vk_api.exceptions.ApiError as exc:
							if exc.code == 15:
								raise darkyExceptions.DarkyError(11)
					else:
						raise darkyExceptions.DarkyError(2)
			else:
				raise darkyExceptions.DarkyError(251)
		elif command == command_list_default['/darky unban']:
			if args_count <= command_list_default['info'][command]['args_count']:
				if bot_is_admin == True:
					if chatSettings[str(event.chat_id)]["chat_settings"]["ban_access"] == "off":
						raise darkyExceptions.DarkyError(10)
					elif chatSettings[str(event.chat_id)]["chat_settings"]["ban_access"] == "admins":
						if user_is_admin == False and event.obj.message['from_id'] not in botSettings['admin_users']:
							raise darkyExceptions.DarkyError(3)
					if command_args == 'all':
						chatSettings = commands.chat.unban_all(event, chatSettings)
						json_objects.write(chatSettings, BOT_CHATSETTINGS)
						darky_resp = '✅Все баны в этой беседе сняты'
					else:
						chatSettings = commands.chat.unban(event, command_args, chatSettings)
						json_objects.write(chatSettings, BOT_CHATSETTINGS)
						darky_resp = '✅Пользователь - разбанен'
				else:
					raise darkyExceptions.DarkyError(2)
			else:
				raise darkyExceptions.DarkyError(251)
		elif command == command_list_default['/darky warn']:
			if args_count <= command_list_default['info'][command]['args_count']:
				if bot_is_admin == True:
					if chatSettings[str(event.chat_id)]["chat_settings"]["warn_access"] == "off":
						raise darkyExceptions.DarkyError(10)
					elif chatSettings[str(event.chat_id)]["chat_settings"]["warn_access"] == "admins":
						if user_is_admin == False and event.obj.message['from_id'] not in botSettings['admin_users']:
							raise darkyExceptions.DarkyError(3)
					try:
						chatSettings, darky_resp = commands.chat.warn(vk, event, command_args, chatSettings)
						json_objects.write(chatSettings, BOT_CHATSETTINGS)
					except vk_api.exceptions.ApiError as exc:
						if exc.code == 15:
							raise darkyExceptions.DarkyError(11)
				else:
					raise darkyExceptions.DarkyError(2)
			else:
				raise darkyExceptions.DarkyError(251)
		elif command == command_list_default['/darky unwarn']:
			if args_count <= command_list_default['info'][command]['args_count']:
				if bot_is_admin == True:
					if chatSettings[str(event.chat_id)]["chat_settings"]["ban_access"] == "off":
						raise darkyExceptions.DarkyError(10)
					elif chatSettings[str(event.chat_id)]["chat_settings"]["ban_access"] == "admins":
						if user_is_admin == False and event.obj.message['from_id'] not in botSettings['admin_users']:
							raise darkyExceptions.DarkyError(3)
					if command_args == 'all':
						chatSettings = commands.chat.unwarn_all(event, chatSettings)
						json_objects.write(chatSettings, BOT_CHATSETTINGS)
						darky_resp = '✅Все предупреждения в беседе были сняты'
					else:
						chatSettings = commands.chat.unwarn(vk, event, command_args, chatSettings)
						json_objects.write(chatSettings, BOT_CHATSETTINGS)
						darky_resp = '✅Предупреждение было снято'
				else:
					raise darkyExceptions.DarkyError(2)
			else:
				raise darkyExceptions.DarkyError(251)
		elif command == command_list_default['/darky full unwarn']:
			if args_count <= command_list_default['info'][command]['args_count']:
				if bot_is_admin == True:
					if chatSettings[str(event.chat_id)]["chat_settings"]["ban_access"] == "off":
						raise darkyExceptions.DarkyError(10)
					elif chatSettings[str(event.chat_id)]["chat_settings"]["ban_access"] == "admins":
						if user_is_admin == False and event.obj.message['from_id'] not in botSettings['admin_users']:
							raise darkyExceptions.DarkyError(3)
					if command_args == 'all':
						darky_resp = '⚠️Возможно вы имели в виду /darky unwarn all'
					else:
						chatSettings = commands.chat.unwarn(vk, event, command_args, chatSettings, True)
						json_objects.write(chatSettings, BOT_CHATSETTINGS)
						darky_resp = '✅Все предупреждения данного пользователя сняты'
			else:
				raise darkyExceptions.DarkyError(251)
		elif command == command_list_default['/darky warns']:
			if args_count <= command_list_default['info'][command]['args_count']:
				if command_args == 'my':
					darky_resp = '❕Количество ваших предупреждений: ' + str(chatSettings[str(event.chat_id)]["members"][str(event.obj.message['from_id'])]["warns"]) + '/' + str(chatSettings[str(event.chat_id)]["chat_settings"]["warn_limit"])
				elif command_args == 'list':
					warned_list = commands.chat.get_warn_list(chatSettings[str(event.chat_id)]["members"])
					if warned_list == []:
						raise darkyExceptions.DarkyError(203)
					#формирование читабельного списка
					out = ''
					cui = 1
					users_info = vk.users.get(user_ids = warned_list)
					for i in range(len(warned_list)):
						#получение имени пользователя
						if str(warned_list[i]) in chatSettings[str(event.chat_id)]["members"]:
							username = chatSettings[str(event.chat_id)]["members"][str(warned_list[i])]["nickname"]
							if username == '' or chatSettings[str(event.chat_id)]["chat_settings"]["nicknames"] == False:
								username = users_info[i]['first_name'] + ' ' + users_info[i]['last_name']
						else:
							username = users_info[i]['first_name'] + ' ' + users_info[i]['last_name']
						#проверка можно ли упоминать его
						if str(warned_list[i]) in userSettings:
							if userSettings[str(warned_list[i])]["mentions"] == True:
								username = '[id' + str(warned_list[i]) + '|' + username + ']'
						else:
							username = '[id' + str(warned_list[i]) + '|' + username + ']'
						#запись в список
						out += str(cui) + '. ' + username + '(' + str(chatSettings[str(event.chat_id)]["members"][str(warned_list[i])]["warns"]) + '/' + str(chatSettings[str(event.chat_id)]["chat_settings"]["warn_limit"]) + ')\n'
						cui += 1
					darky_resp = '❕Список пользователей с предупреждениями в этой беседе:\n' + out
				else:
					raise darkyExceptions.DarkyError(253)
			else:
				raise darkyExceptions.DarkyError(251)
		elif command == command_list_default["/darky verify set"]:
			if args_count == command_list_default['info'][command]['args_count']:
				if user_is_admin == True or event.obj.message['from_id'] in botSettings['admin_users']:
					chatSettings[str(event.chat_id)]["verify_system"] = darky_verify.change_setting(vk, verify_sys, command_args)
					json_objects.write(chatSettings, BOT_CHATSETTINGS)
					darky_resp += '✅Параметр ' + command_args.split('; ')[0] + ' для DarkyVerify - изменён'
				else:
					raise darkyExceptions.DarkyError(3)
			else:
				raise darkyExceptions.DarkyError(250)
		elif command == command_list_default["/darky nick"]:
			if args_count >= command_list_default['info'][command]['args_count']:
				if chatSettings[str(event.chat_id)]["chat_settings"]["nicknames"] == True:
					if command_args == "list":
						nick_list = commands.nicknames.get_list(chatSettings[str(event.chat_id)]["members"])
						if nick_list == []:
							raise darkyExceptions.DarkyError(401)
						out = ''
						cui = 1
						for i in range(len(nick_list)):
							#получение никнейма
							username = chatSettings[str(event.chat_id)]["members"][nick_list[i]]["nickname"]
							#проверка можно ли упоминать владельца никнейма
							if nick_list[i] in userSettings:
								if userSettings[nick_list[i]]["mentions"] == True:
									username = '[id' + nick_list[i] + '|' + username + ']'
							else:
								username = '[id' + nick_list[i] + '|' + username + ']'
							out += str(cui) + '. ' + username + '\n'
							cui += 1
						darky_resp = '🧾Список никнеймов, установленных в этой беседе:\n' + out
					elif command_args.split('; ')[0] == "set" or command_args == "del":
						#получение идентификатора пользователя которому нужно сменить никнейм
						try:
							id = bot.search_id(event, "", {})
						except darkyExceptions.DarkyError as exc:
							if exc.code == 6:
								id = event.obj.message['from_id']
						#если id и from_id не совпадают это значит что человек пытается сменить никнейм кому-то другому
						if id != event.obj.message['from_id']:
							if chatSettings[str(event.chat_id)]["chat_settings"]["nicknames_access"] == "off":
								raise darkyExceptions.DarkyError(402)
							elif chatSettings[str(event.chat_id)]["chat_settings"]["nicknames_access"] == "admins":
								if user_is_admin == False and event.obj.message['from_id'] not in botSettings['admin_users']:
									raise darkyExceptions.DarkyError(3)
						if id < 0:
							raise darkyExceptions.DarkyError(8)
						if command_args.split('; ')[0] == "set":
							chatSettings[str(event.chat_id)]["members"] = commands.nicknames.set(id, chatSettings[str(event.chat_id)]["members"], command_args.split('; ')[1])
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
							if str(id) in userSettings and userSettings[str(id)]["mentions"] == True or str(id) not in userSettings:
								nick = '[id' + str(id) + '|' + command_args.split('; ')[1] + ']'
							else:
								nick = command_args.split('; ')[1]
							darky_resp = '✅Никнейм пользователя ' + vk.users.get(user_ids=id)[0]["first_name"] + ' теперь - ' + nick
						elif command_args == "del":
							chatSettings[str(event.chat_id)]["members"] = commands.nicknames.delete(id, chatSettings[str(event.chat_id)]["members"])
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
							darky_resp = '✅Никнейм пользователя ' + vk.users.get(user_ids=id)[0]["first_name"] + ' - удалён'
					else:
						raise darkyExceptions.DarkyError(253)
				else:
					raise darkyExceptions.DarkyError(10)
			else:
				raise darkyExceptions.DarkyError(252)
		elif command == command_list_default['/darky rp list']:
			if chatSettings[str(event.chat_id)]["chat_settings"]["rp"] == True:
				darky_resp = '🧾Список ролевых команд в этой беседе:\n' + commands.roleplay.get_list(chatSettings[str(event.chat_id)]["rp_commands"])
			else:
				raise darkyExceptions.DarkyError(10)
		elif command == command_list_default['/darky rp new']:
			if chatSettings[str(event.chat_id)]["chat_settings"]["rp"] == True:
				if args_count == command_list_default['info'][command]['args_count']:
					if chatSettings[str(event.chat_id)]["chat_settings"]["rp_access"] == "off":
						raise darkyExceptions.DarkyError(452)
					elif chatSettings[str(event.chat_id)]["chat_settings"]["rp_access"] == "admins":
						if user_is_admin == False and event.obj.message['from_id'] not in botSettings['admin_users']:
							raise darkyExceptions.DarkyError(3)
					chatSettings[str(event.chat_id)]["rp_commands"] = commands.roleplay.add(command_args, chatSettings[str(event.chat_id)]["rp_commands"])
					json_objects.write(chatSettings, BOT_CHATSETTINGS)
					darky_resp = '✅РП команда ' + command_args.split('; ')[0].lower().lstrip(' ').rstrip(' ') + ' - добавлена'
				else:
					raise darkyExceptions.DarkyError(250)
			else:
				raise darkyExceptions.DarkyError(10)
		elif command == command_list_default['/darky rp del']:
			if chatSettings[str(event.chat_id)]["chat_settings"]["rp"] == True:
				if args_count == command_list_default['info'][command]['args_count']:
					if chatSettings[str(event.chat_id)]["chat_settings"]["rp_access"] == "off":
						raise darkyExceptions.DarkyError(452)
					elif chatSettings[str(event.chat_id)]["chat_settings"]["rp_access"] == "admins":
						if user_is_admin == False and event.obj.message['from_id'] not in botSettings['admin_users']:
							raise darkyExceptions.DarkyError(3)
					chatSettings[str(event.chat_id)]["rp_commands"] = commands.roleplay.delete(command_args, chatSettings[str(event.chat_id)]["rp_commands"])
					json_objects.write(chatSettings, BOT_CHATSETTINGS)
					darky_resp = '✅РП команда ' + command_args.split('; ')[0].lower().lstrip(' ').rstrip(' ') + ' - удалена'
				else:
					raise darkyExceptions.DarkyError(250)
			else:
				raise darkyExceptions.DarkyError(10)
		elif command == command_list_default['/darky random rp']:
			try:
				darky_resp = commands.roleplay.rand_rp(vk, event, chatSettings, userSettings, True)
			except darkyExceptions.DarkyError as exc:
				if exc.code in [454]:
					darky_resp = "⚠️Выбранный пользователь ограничил использование ролевых команд на себе"
				elif exc.code in [12]:
					darky_resp = "⚠️Выбранный идентификатор принадлежит мне самой"
				else:
					raise darkyExceptions.DarkyError(exc.code)
		elif command == command_list_default['/darky stats']:
			if args_count <= command_list_default['info'][command]['args_count']:
				darky_resp = commands.chat.user_info(event, command_args, chatSettings, userSettings, botInfo)
			else:
				raise darkyExceptions.DarkyError(250)
		elif command == command_list_default['/darky top']:
			if args_count > command_list_default['info'][command]['args_count']:
				raise darkyExceptions.DarkyError(250)
			if command_args == "":
				command_args = "5"
			darky_resp = commands.chat.get_top_members(vk, chatSettings[str(event.chat_id)]["members"], command_args, userSettings, chatSettings[str(event.chat_id)]["chat_settings"]["nicknames"])
	else:
		raise darkyExceptions.DarkyError(4)
	return darky_resp, darky_attachments



def easy_commands(): #простенькие команды по типу привет или спокойной ночи
	darky_resp = ''
	trigger_rep = []
	text = event.obj.message['text'].lower().replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split(' ')
	#set(<текст>) & {список слов} - определяет есть ли слова в тексте или нет, возвращает также {} содержащий в себе список найденных слов
	darky_bad_words_trigger = set(text) & {'дорки', 'дурки', 'доркя', 'дуркя', 'дорке'}
	hello_trigger = set(text) & {'привет', 'приветствую', 'здравствуйте', 'преет', 'преть', 'приветик', 'приветики', 'здрасте', 'хай', 'хелло', 'ку'}
	morning_trigger = set(text) & {'утра', 'утречка', 'доброе', 'утро', 'проснулся', 'проснулась', 'добре', 'доброго', 'проснувся', 'проснувась'}
	good_night_trigger = set(text) & {'спокойной', 'ночи', 'споки', 'споке', 'ночки', 'снов', 'спать'}
	if darky_bad_words_trigger != set():
		trigger_rep = ['ДАРКИ!', 'ДАРКИ Я!', 'Я - ДАРКИ!', 'Обидно ;с', 'Прекратите так меня называть', 'Поправочка. Я - Дарки', 'Ррр']
	elif hello_trigger != set():
		trigger_rep = ['Привет', 'Рада видеть вас здесь']
	elif morning_trigger != set():
		trigger_rep = ['Утра', 'Привет', 'Доброе утро', 'Доброе', 'Как спалось?', 'Надеюсь кошмаров не было']
	elif good_night_trigger != set():
		trigger_rep = ['Спокойной', 'Спокойной ночи', 'Споки', 'Добрых снов', 'Сладких снов', 'Спи сладко', 'Спи крепко', 'Ночи', 'Ночки', 'Пусть приснятся вам гигапони', 'Приятных снов']
	if trigger_rep != []:
		darky_resp = random.choice(trigger_rep)
	return darky_resp



def init_command(): #инициализация команды
	darky_resp = ''
	darky_attachments = ''
	visual.reprint('определение ассоциаций для "пресетных" команд...')
	try:
		if event.from_chat == True:
			command_assoc_list = chatSettings[str(event.chat_id)]["command_assocs"]
		elif event.from_user == True:
			command_assoc_list = userSettings[str(event.obj.message["from_id"])]["command_assocs"]
		message = command_assocs.check2(event.obj.message['text'], command_assoc_list)
	except (darkyExceptions.DarkyError, KeyError):
		message = event.obj.message['text']
	visual.reprint('определение ассоциации для вызванной команды...')
	command, command_args = check_assocs(message)
	visual.reprint()
	if command in command_list_default: #команда должна быть в command_list_default, чтобы она распознавалась ботом
		bot.typing_state(vk, event)
		try:
			darky_resp, darky_attachments = execute_command(command, command_args)
		except vk_api.exceptions.ApiError as exc:
			if exc.code == 935:
				darky_resp = '⚠️Данного пользователя нет в беседе'
			else:
				darky_resp = '⚠️Исключение ApiError\n- - -\nДополнительная информация: ' + getTraceback(1)
		except darkyExceptions.DarkyError as exc:
			if exc.code == 100:
				darky_resp = '⚠️Ваша беседа уже зарегистрирована'
			elif exc.code == 101:
				darky_resp = '❌Ваша беседа не зарегистрирована. Я не могу выполнить данную команду'
			elif exc.code == 4:
				darky_resp = '❌Эта команда здесь не работает'
			elif exc.code == 2:
				darky_resp = '❌Выполнение этой команды невозможно, поскольку у меня отсутствует статус администратора.'
			elif exc.code == 3:
				darky_resp = '⛔В доступе отказано. Вы не являетесь администратором беседы и не находитесь в списке разрешённых пользователей бота'
			elif exc.code == 250:
				darky_resp = '⚠️Количество аргументов для команды ' + command + ' должно быть равно: ' + str(command_list_default["info"][command]["args_count"])
			elif exc.code == 251:
				darky_resp = '⚠️Максимальное количество аргументов для команды ' + command + ': ' + str(command_list_default["info"][command]["args_count"])
			elif exc.code == 252:
				darky_resp = '⚠️Минимальное количество аргументов для команды ' + command + ': ' + str(command_list_default["info"][command]["args_count"])
			elif exc.code == 500:
				darky_resp = '⚠️Параметра ' + command_args.split('; ')[0] + ' не сущестует. Проверьте правильность написания параметра, возможно вы ошиблись'
			elif exc.code == 501:
				darky_resp = '⚠️Неверное значение для параметра ' + command_args.split('; ')[0]
			elif exc.code == 5:
				darky_resp = '❌Меня нельзя задействовать в этой команде'
			elif exc.code == 6:
				darky_resp = '⚠️Пользователь не был обнаружен. Убедитесь, что вы правильно указали его'
			elif exc.code == 7:
				darky_resp = '⚠️Данного пользователя нет в беседе'
			elif exc.code == 152:
				darky_resp = '❌Не удалось установить приветствие. Убедитесь, что вы прислали нужное приветствие мне в личные сообщения и при использовании команды переслали это сообщение в беседу'
			elif exc.code == 154:
				darky_resp = '⚠️Обнаружена некорректная работа вашего приветствия. Настоятельно рекомендую установить его заново'
			elif exc.code == 150:
				darky_resp = '⚠️В вашей беседе нет установленного приветствия'
			elif exc.code == 153:
				darky_resp = '❌Не удалось установить правила. Убедитесь, что вы переслали сообщение с текстом правил при использовании команды'
			elif exc.code == 151:
				darky_resp = '⚠️В вашей беседе нет установленных правил'
			elif exc.code == 10:
				darky_resp = '❌Данная команда выключена'
			elif exc.code == 502:
				darky_resp = '⚠️Указано недопустимое значение параметра ' + command_args.split('; ')[0]
			elif exc.code == 11:
				darky_resp = '❌Данный пользователь, возможно, является администратором или создателем беседы'
			elif exc.code == 102:
				darky_resp = '❌Данный пользователь ни разу не посещал эту беседу, я не могу выполнить эту команду'
			elif exc.code == 200:
				darky_resp = '⚠️Данный пользователь уже забанен в этой беседе'
			elif exc.code == 201:
				darky_resp = '⚠️Данный пользователь уже разбанен в этой беседе'
			elif exc.code == 202:
				darky_resp = '❕Список забаненных пуст'
			elif exc.code == 203:
				darky_resp = '❕Список пользователей с предупреждениями пуст'
			elif exc.code == 400:
				darky_resp = '⚠️Данный никнейм занят, попробуйте другой'
			elif exc.code == 401:
				darky_resp = '❕Список никнеймов пуст'
			elif exc.code == 402:
				darky_resp = '⛔Вы не можете менять никнеймы другим пользователям, данная функция отключена в настройках'
			elif exc.code == 253:
				darky_resp = '⚠️Передан неверный аргумент для команды ' + command
			elif exc.code == 503:
				darky_resp = '❌Сообщество не найдено, убедитесь, что вы правильно указали ссылку или короткое имя на сообщество'
			elif exc.code == 8:
				darky_resp = '❌Невозможно выполнить команду. Идентификатор принадлежит сообществу'
			elif exc.code == 450:
				darky_resp = '⚠️Данная рп команда уже существует'
			elif exc.code == 451:
				darky_resp = '⚠️Данной рп команды не существует'
			elif exc.code == 452:
				darky_resp = '⛔В доступе отказано. Вы не можете управлять этими рп командами'
			elif exc.code == 600:
				darky_resp = "❕Список заметок пуст"
			elif exc.code == 601:
				darky_resp = "⚠️Данной заметки не существует"
			elif exc.code == 603:
				darky_resp = "⚠️Заголовок для этой заметки занят, попробуйте другой"
			elif exc.code == 604:
				darky_resp = "❌Заметка не была удалена"
			elif exc.code == 155:
				darky_resp = "⚠️В приветствии текущей беседы нет какого либо прикреплённого объекта типа картинки и тп."
			elif exc.code == 103:
				darky_resp = "⚠️Пресета настроек " + command_args.split('; ')[1] + " не существует. Проверьте правильность написания названия пресета, возможно вы ошиблись"
			elif exc.code == 254:
				darky_resp = "⚠️Неверное значение в аргументе!\nАргумент должен быть числом от 5 до 20(по умолчанию - 5)"
			elif exc.code in [605, 607, 608]:
				darky_resp = '⚠️Количество аргументов для команды ' + command + ' с аргументами add / rename / edit должно быть равно: 3'
			elif exc.code == 606:
				darky_resp = '⚠️Количество аргументов для команды ' + command + ' с аргументом del должно быть равно: 2'
			else:
				darky_resp = "⚠️Исключение DarkyError\n" + getTraceback(1, 1)
		except TimeoutError:
			raise TimeoutError
		except Exception:
			darky_resp = '⚠️Исключение обработано\n- - -\nДополнительная информация: ' + getTraceback(1, 0)
	else:
		try:
			if event_from_chat == True:
				if chat_is_registered == True:
					if chatSettings[str(event.chat_id)]['chat_settings']['easy_commands_react'] == True:
						darky_resp = easy_commands()
					if chatSettings[str(event.chat_id)]["chat_settings"]["rp"] == True:
						darky_resp = commands.roleplay.do_rp(vk, event, event.obj.message["from_id"], event.obj.message["text"], chatSettings[str(event.chat_id)], userSettings)
				else:
					darky_resp = easy_commands()
			else:
				darky_resp = easy_commands()
		except darkyExceptions.DarkyError as exc:
			if exc.code == 6:
				darky_resp = '⚠️Данного пользователя нет в беседе'
			elif exc.code == 454:
				darky_resp = "⚠️Данный пользователь ограничил использование рп на себе"
			elif exc.code == 51:
				pass
			else:
				darky_resp = "⚠️Исключение DarkyError\n" + getTraceback(1, 1)
		except:
			darky_resp = '⚠️Исключение обработано\n- - -\nДополнительная информация: ' + getTraceback(1)
	#отправка результата
	if (darky_resp, darky_attachments) != ('', ''):
		bot.send_mess(vk, peer_ids=event.obj.message['peer_id'], text=darky_resp, attachments=darky_attachments)
		botInfo["commands"] += 1
		json_objects.write(botInfo, BOT_INFO)
					
			


print('Всё готово')
bot.send_mess(vk, botSettings["admin_users"], "✅Я запущена и готова к работе")
bd_date = 'null' #предотвращает ошибку в commands.easter_eggs.ee1() (лучше не трогать, одна строка не сильно мешает)

#основной цикл
while True:
	try:
		for event in botlongpoll.listen():
			
			
			botInfo = json_objects.load(BOT_INFO)
			
			visual.reprint('загрузка chatSettings...')
			chatSettings = json_objects.load(BOT_CHATSETTINGS)
			
			
			
			try:
				event_from_chat = False
				if event.from_chat == True:
					event_from_chat = True
					bot_is_admin = False
					chat_is_registered = False
					user_is_admin = False
					chatObj = vk.messages.getConversationsById(peer_ids = 2000000000 + event.chat_id)["items"]
					
					visual.reprint('проверка зарегистрирована ли беседа...')
					if str(event.chat_id) in chatSettings:
						chat_is_registered = True
					
					visual.reprint('проверка админки у бота...')
					if chatObj != []:
						bot_is_admin = True
						visual.reprint('проверка админки у пользователя...')
						if event.obj.message['from_id'] in chatObj[0]["chat_settings"]["admin_ids"] or chatObj[0]["chat_settings"]["owner_id"] == event.obj.message['from_id']:
							user_is_admin = True
					
					visual.reprint('считывание настроек системы верификации...')
					#определение настроек системы верификации
					if chat_is_registered == True:
						verify_sys = chatSettings[str(event.chat_id)]["verify_system"]
					else:
						verify_sys = {
							"status": True,
							"punishment": "kick", #kick/ban
							"days_check": 3,
							"group_check": 0,
							"info_check": "-photo-friends"
						}
					
					visual.reprint('проверка актуальности названия беседы...')
					if bot_is_admin == True and str(event.chat_id) in chatSettings:
						if chatSettings[str(event.chat_id)]['chat_info']['title'] != chatObj[0]["chat_settings"]["title"]:
							chatSettings[str(event.chat_id)]['chat_info']['title'] = chatObj[0]["chat_settings"]["title"]
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
						
						if random.randint(1, botSettings["settings"]["upd_gr_acskeys"]) == 1:
							visual.reprint('обновление ключа доступа у прикрепленного объекта в приветствии')
							try:
								chatSettings = commands.greeting.upd_att_accsskey(vk, event, chatSettings)
								json_objects.write(chatSettings, BOT_CHATSETTINGS)
								if botSettings["settings"]["upd_gr_acskeys_msg"] == True:
									bot.send_mess(vk, peer_ids=botSettings["settings"]["snd_msgs"], text='✅Ключ доступа у прикреплённого объекта приветствия в беседе id' + str(event.chat_id) + ' - обновлён')
							except darkyExceptions.DarkyError as exc:
								if exc.code in [150, 155]:
									pass
								else:
									raise exc
					else:
						raise darkyExceptions.DarkyError(2)
			except darkyExceptions.DarkyError as exc:
				if exc.code != 2:
					print(getTraceback(1))
			except AttributeError:
				pass
			
			visual.reprint('загрузка userSettings...')
			userSettings = json_objects.load(BOT_USERSETTINGS)
			
			
			
			if random.randint(1, 100) == 1:
				print("bot_random_rp")
				try:
					darky_resp, peerid = commands.roleplay.rand_rp(vk, event, chatSettings, userSettings)
					bot.send_mess(vk, peerid, darky_resp)
				except darkyExceptions.DarkyError as exc:
					if exc.code in [10, 12, 454]:
						pass
					else:
						raise exc
			
			visual.reprint()
			
			#реакция на выход пользователя из беседы
			try:
				if event.obj.message['action']['type'] == 'chat_kick_user' and chatSettings[str(event.chat_id)]["chat_settings"]["autokick"] == True:
					visual.print_botEvent(event, 'member_leaved_from_chat')
					vk.messages.removeChatUser(chat_id = event.chat_id, member_id = event.obj.message['action']["member_id"])
			except:
				pass
			
			
			
			#приветствие при добавлении бота в беседу
			try:
				if event.obj.message['action']['type'] == 'chat_invite_user' and event.obj.message['action']['member_id'] == -192784148:
					visual.print_botEvent(event, 'bot_was_added_to_chat')
					bot.typing_state(vk, event)
					bot.send_mess(vk, peer_ids=event.obj.message['peer_id'], text='Спасибо за добавление в беседу\n\nМоё имя - Дарки.\nЯ - бот, предназначенный для администрирования бесед, включающий в себя множество команд и гибких настроек.\n\nТакже я заметила, что у меня нет статуса администратора, поэтому прошу вас выдать его мне и написать "/darky reg" для активации полного функционала и регистрации беседы\n\nПодробная инструкция по регистрации беседы: vk.com/@darkybot-info\n\nПомощь по командам бота: vk.com/@darkybot-help')
			except:
				pass
			
			#приветствие при новом пользователе
			try:
				if event_from_chat == True:
					if event.obj.message['action']['type'] == 'chat_invite_user' and event.obj.message['action']['member_id'] != -192784148 or event.obj.message['action']['type'] == 'chat_invite_user_by_link':
						
						visual.print_botEvent(event, 'new_member_in_chat')
						
						if event.obj.message['action']['type'] == 'chat_invite_user':
							id = event.obj.message['action']['member_id']
						else:
							id = event.obj.message['from_id']
						
						#регистрация нового пользователя в беседе
						visual.reprint('регистрация нового пользователя в chatSettings...')
						if chat_is_registered == True:
							if id > 0 and str(id) not in chatSettings[str(event.chat_id)]["members"]:
								chatSettings[str(event.chat_id)]["members"][str(id)] = chat_settings.reg_user_in_chat()
								json_objects.write(chatSettings, BOT_CHATSETTINGS)
						
						is_verified = False
						visual.reprint('работа системы DarkyVerify...')
						#сам вызов системы верификации и обработка её исключений
						if verify_sys['status'] == True:
							try:
								is_verified = darky_verify.check(vk, id, verify_sys['days_check'], verify_sys['info_check'], verify_sys["group_check"], OS_PATH)
							except darkyExceptions.DarkyError as exc:
								if exc.code in [300, 301, 302, 304]:
									if verify_sys['punishment'] == "ban":
										if chatSettings[str(event.chat_id)]["members"][str(id)]["is_banned"] == False:
											chatSettings = commands.chat.ban(vk, event, str(id), chatSettings)
											json_objects.write(chatSettings, BOT_CHATSETTINGS)
										else:
											vk.messages.removeChatUser(chat_id = event.chat_id, member_id = id)
									elif verify_sys['punishment'] == 'kick':
										vk.messages.removeChatUser(chat_id = event.chat_id, member_id = id)
									darky_resp = '⚠️Система DarkyVerify распознала данную личность как подозрительную'
									if exc.code == 300:
										darky_resp += '\n\n❗Аккаунт пользователя был создан не более ' + str(verify_sys["days_check"]) + ' дней назад'
									elif exc.code == 301:
										darky_resp += '\n\n❗Аккаунт пользователя не имеет установленной аватарки'
									elif exc.code == 302:
										darky_resp += '\n\n❗Количество друзей у аккаунта пользователя меньше 5'
									elif exc.code == 304:
										darky_resp += '\n\n❗Данный пользователь не является участником, указанной в настройках беседы, группы'
									if verify_sys['punishment'] == "ban":
										darky_resp += '\n\n✅Пользователь был исключён и забанен'
									elif verify_sys['punishment'] == 'kick':
										darky_resp += '\n\n✅Пользователь был исключён'
									bot.send_mess(vk, event.obj.message['peer_id'], darky_resp)
								elif exc.code == 8:
									print(getTraceback(0))
						
						#формировка приветствия
						visual.reprint('обработка информации и формировка приветствия...')
						if verify_sys["status"] == True and is_verified == True or verify_sys["status"] == False:
							if chat_is_registered == True and bot_is_admin == True:
								if chatSettings[str(event.chat_id)]["members"][str(id)]["is_banned"] == False and chatSettings[str(event.chat_id)]["members"][str(event.obj.message['from_id'])]["is_banned"] == False:
									try:
										darky_resp, darky_attachments = commands.greeting.display(event, chatSettings)
										#добавление упоминания человека перед приветствием
										if chatSettings[str(event.chat_id)]["chat_settings"]["mention_in_greetings"] == True:
											if str(id) not in userSettings or userSettings[str(id)]["mentions"] == True:
												mention = '[id' + str(id) + '|' + vk.users.get(user_ids = id)[0]['first_name'] + ']'
											else:
												mention = vk.users.get(user_ids = id)[0]['first_name']
											darky_resp = mention + '\n' + darky_resp
										bot.send_mess(vk, event.obj.message['peer_id'], darky_resp, darky_attachments)
									except darkyExceptions.DarkyError as exc:
										if exc.code == 150:
											pass
								else:
									try:
										vk.messages.removeChatUser(chat_id = event.chat_id, member_id = id)
										vk.messages.removeChatUser(chat_id = event.chat_id, member_id = event.obj.message['from_id'])
									except vk_api.exceptions.ApiError as exc:
										if exc.code in [15, 935]:
											pass
									bot.send_mess(vk, event.obj.message['peer_id'], '⚠️Данный пользователь исключён\nПричина: получен бан в этой беседе')
							
			except (AttributeError, KeyError) as exc:
				pass
			
			if event.type == VkBotEventType.MESSAGE_NEW:
				if botSettings["settings"]["testing_mode"] == True:
					if event.obj.message["peer_id"] not in botSettings["settings"]["testing_ids"]:
						raise darkyExceptions.DarkyError(13)
				if event_from_chat == True:
					#регистрация нового пользователя в беседе
					if chat_is_registered == True and bot_is_admin == True and event.obj.message['from_id'] > 0:
						if event.obj.message['from_id'] > 0 and str(event.obj.message['from_id']) not in chatSettings[str(event.chat_id)]["members"]:
							chatSettings[str(event.chat_id)]["members"][str(event.obj.message['from_id'])] = chat_settings.reg_user_in_chat()
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
						#удаление пользователя если он был забанен
						if chatSettings[str(event.chat_id)]["members"][str(event.obj.message['from_id'])]["is_banned"] == True:
							try:
								vk.messages.removeChatUser(chat_id = event.chat_id, member_id = event.obj.message['from_id'])
								bot.send_mess(vk, peer_ids=event.obj.message['peer_id'], text='⚠️Данный пользователь исключён\nПричина: получен бан в этой беседе')
							except vk_api.exceptions.ApiError as exc:
								if exc.code in [15, 935]:
									pass
					#засчитывание опыта пользователя
					if chat_is_registered == True and event.obj.message['from_id'] > 0:
						try:
							chatSettings[str(event.chat_id)]["members"] = commands.chat.add_lvl_exp(vk, event.obj.message["peer_id"], event.obj.message["text"], event.obj.message["attachments"], event.obj.message["from_id"], chatSettings[str(event.chat_id)]["members"], chatSettings[str(event.chat_id)]["chat_settings"]["lvlup_mentions"], userSettings)
							json_objects.write(chatSettings, BOT_CHATSETTINGS)
						except darkyExceptions.DarkyError as exc:
							if exc.code == 104:
								pass
							else:
								raise exc
				#регистрация пользователя в настройках
				if event.obj.message["peer_id"] < 20000000000:
					userSettings = user_settings.reg_user(event, BOT_USERSETTINGS)
				if "test" in event.obj.message['text'].lower() or "тест" in event.obj.message['text'].lower():
					bd_date = commands.easter_eggs.ee1(vk, event, bd_date)
				#запись текста сообщения для будущей генерации сообщений(нет)
				drgt.write_data(event, BOT_MESS)
				#выполнение самих команд
				init_command()
	
	except darkyExceptions.DarkyError as exc:
		if exc.code == 13:
			pass
	except (TimeoutError, requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
		#обработка timeout исключения и рвндомный вызов рп
		if random.randint(1, 25) == 1:
			print("bot_random_rp")
			try:
				darky_resp, peerid = commands.roleplay.rand_rp(vk, event, chatSettings, userSettings)
				bot.send_mess(vk, peerid, darky_resp)
			except darkyExceptions.DarkyError as exc:
				if exc.code in [10, 12, 454]:
					pass
				else:
					raise exc
	except requests.exceptions.ConnectionError:
		#при проблеме с подключением к сети бот будет ждать 5 секунд,
		#а затем заново авторизовываться.
		#бесконечно, пока интернет не восстановится
		print('Ожидание подключения...')
		time.sleep(5)
		try:
			botlongpoll, vk = bot.auth(192784148, ACCESS_TOKEN)
			print(visual.coloredText('Подключение восстановлено', 'cian'))
		except requests.exceptions.ConnectionError:
			print(visual.coloredText('Подключение не восстановлено', 'red'))
	except KeyboardInterrupt:
		print()
		raise SystemExit
	except SystemExit:
		print()
		raise SystemExit
	except:
		#обработка исключения внутри работы бота
		if botSettings["settings"]["exc_msg"] == True:
			bot.send_mess(vk, peer_ids=botSettings["admin_users"], text='⚠️В моей работе произошла ошибка.\nТребуется полный перезапуск.\n\nДополнительная информация:\n- - -\n' + getTraceback(1))
		raise SystemExit
