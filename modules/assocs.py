import json
from modules.jsonObjects import json_objects
from modules import darkyExceptions


class command_assocs: #ассоциации с командами
	
	def earse(originalCommand, commandAssoc): #стирает лишнее
		#originalCommand - вид команды при вызове
		#commandAssoc - то, что нужно вырезать(работает по своей сути как lstrip, но при этом не затрагивает то, что не нужно
		out = ''
		origCmd = originalCommand.split(' ')
		assocCmd = commandAssoc.split(' ')
		for i in range(len(origCmd)):
			try:
				if origCmd[i] != assocCmd[i]:
					out += origCmd[i] + ' '
			except:
				out += origCmd[i] + ' '
		return out.rstrip(' ')
	
	
	def check(command, assoc_list): #проверка ассоциации с командами
		#command - string, сообщение которое вызвало команду
		#assoc_list - object, список установленных ассоциаций
		cmdCheckSlot1 = command #слот в которому в процессе проверки будут по отдельности добавляться слова
		cmdOut = '' #оригинальная команда
		cmdOut2 = '' #дополнительное поле команды(используется если команда требует например указать какой либо параметр)
		while len(cmdCheckSlot1.split(' ')) > 0 and cmdCheckSlot1 != '':
			if cmdCheckSlot1.lower() in assoc_list: #если команда совпадает с списком установленных ассоциаций
				cmdOut = assoc_list[cmdCheckSlot1.lower()]
				cmdOut2 = command_assocs.earse(command, cmdCheckSlot1)
				break
			else:
				cmdCheckSlot1 = cmdCheckSlot1.rstrip(cmdCheckSlot1.split(' ')[-1]).rstrip(' ')
		if cmdOut == '':
			raise darkyExceptions.DarkyError(51)
		return cmdOut, cmdOut2
	
	
	def check2(command, assoc_list):
		if command.lower() in assoc_list:
			return assoc_list[command.lower()]
		else:
			raise darkyExceptions.DarkyError(51)
	
	
	def add(assoc_list, orig_command, assoc): #установка ассоциации для команды
		#assoc_list - обьект ассоциаций в настройках бота
		#orig_command - настоящая команда (например: /darky_startUp)
		#assoc - ассоциация для указанной команды
		if not assoc.startswith('/darky'):
			assoc_list[assoc] = orig_command.lower()
			return assoc_list
		else:
			raise darkyExceptions.DarkyError(50)
	
	
	def remove(assoc_list, assoc): #удаление ассоциации
		#assoc_list - обьект ассоциаций в настройках бота
		#assoc - ассоциация которую нужно удалить
		if not assoc.startswith('/darky'):
			del(assoc_list[assoc.lower()])
			return assoc_list
		else:
			raise darkyExceptions.DarkyError(50)
