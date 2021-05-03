#DRGT(DarkyRandomGeneratingText)
#система которая генерирует бредовые сообщения путём подбора
#абсолютно рандомных слов, но это выглядит вроде как забавно иногда.

import os
import random

class drgt:
	
	def write_data(event, path):
		#event - объект события от вк, нужен для корректной записи в файлы
		#path - путь к папке mess, где хранится весь текст диалогов(откуда потом будут браться слова для "генерации"
		text = event.obj.message['text']
		if event.from_chat == True:
			id = event.chat_id
		elif event.from_user == True:
			id = event.obj.message['from_id']
		path += '/' + str(id) + '.ini'
		if os.path.exists(path) == True:
			param = 'a'
		else:
			param = 'w'
		with open(path, param) as file:
			file.write(' ' + text)
			file.close()
	
	
	def generate(event, path, from_chat): #генерация текста
		out = ''
		if from_chat == True:
			id = event.chat_id
		else:
			id = event.obj.message['from_id']
		#вычисление длины сообщения
		text_len = random.randint(2, 20)
		#считывание слов из файла
		with open(path + '/' + str(id) + '.ini') as mess_data:
			all_words = mess_data.read()
			mess_data.close()
		#создание списка для удобства генерации
		word_list = all_words.replace('\n', ' ').lstrip(' ').split(' ')
		if len(word_list) < 20:
			darky_resp = '⚠️Я пока собрала недостаточно слов для более менее хорошей генерации. Дайте мне собрать больше данных о беседе и я смогу сгенерировать что-нибудь'
			return darky_resp
		else:
			#составление текста
			for i in range(text_len):
				out += word_list[random.randint(1, len(word_list)) - 1] + ' '
			out = out.rstrip(' ')
			#форматирование текста
			text_style = random.randint(0, 10)
			styles = [out.capitalize(), out.lower(), out.upper()]
			if text_style < 3:
				out = styles[text_style]
			else:
				pass
			return out
	
	
	def del_data(event, path, from_chat): #удаление собранных данных
		if from_chat == True:
			id = event.chat_id
		else:
			id = event.obj.message['from_id']
		os.remove(path + '/' + str(id) + '.ini')
		darky_resp = '✅Собранные для генерации предложений данные - удалены'
		return darky_resp
