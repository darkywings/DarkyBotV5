# -*- coding: utf-8 -*-
import random
import os

class DarkySpeak:
	#модернизированный генератор текста для Дарки-бота
	#работает также на основе рандома, но имеет некие закономерности для генерации
	
	
	def read(text, database): #своеобразный метод обучения
		#под каждое слово алгоритм создаёт словарь
		#в этот словарь будут записываться слова который могут идти после данного слова

		#параметры:
		#text - текст получаемый на входе
		#database - база данных слов которая записывается в json файлах
		
		#создание списка слов из входного текста
		
		text = text.replace("\n", " ")
		text_list = text.split(" ")
		
		#создание словарей в базе данных
		
		for current_word_id in range(len(text_list)):
			if text_list[current_word_id] not in database:
				database[text_list[current_word_id]] = []
		
		#указание ассоциаций какие слова после каких должны идти
		
		for current_word_id in range(len(text_list) - 1):
			if text_list[current_word_id + 1] not in database[text_list[current_word_id]]:
				database[text_list[current_word_id]].append(text_list[current_word_id + 1])
		
		return database
	
	
	def generate(database):
		#генерация текста
		#берёт слова из базы данных и на основе её с помощью рандома пишет текст
		
		out = ""
		
		#определение длины текста
		text_length = random.randint(2, 20)
		
		#сама генерация, собственно
		
		if len(list(database)) < 40:
			out = "⚠️Я пока собрала недостаточно данных для более менее хорошей генерации. Позвольте мне собрать больше информации и я смогу сгенерировать что-нибудь"
		else:
			#выбор первого слова
			word = random.choice(list(database))
			out = word + " "
			
			#выбор последующих слов
			while len(out.split(' ')) < text_length:
				if database[word] != []:
					word = random.choice(database[word])
				else:
					word = random.choice(list(database))
				
				#замена ссылок фразой "[DELETED_LINK]"
				if 'http' in word or 'vk.cc' in word or 'bit.ly' in word:
					word = "[DELETED_LINK]"
				
				out += word + " "
			
			#форматирование текста
			out = out.rstrip(" ")
			text_style = random.randint(0, 10)
			styles = [out.capitalize(), out.lower(), out.upper()]
			if text_style < 3:
				out = styles[text_style]
			
		return out
	
	
	def del_data(peer_id, path): #удаление собранных данных
		
		#параметры
		#peer_id - идентификатор диалога
		#path - путь к базам данных
		
		#проверка последнего файла базы данных
		last_database_index = 0
		while os.path.exists(path + str(peer_id) + "_" + str(last_database_index) + ".json") == True:
			last_database_index += 1
		last_data_index -= 1
		
		#удаление файлов где встречается нужный идентификатор
		while os.path.exists(path + str(peer_id) + "_" + str(last_database_index) + ".json") == True:
			os.remove(path + str(peer_id) + "_" + str(last_database_index) + ".json")
			last_database_index -= 1
		
		return True
