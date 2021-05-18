import datetime

def coloredText(text, textColor='white', bgColor='black'): #красит текст(аля красива)
	#Работает ТОЛЬКО с кодировкой ANSII
	#text - string, нужный текст
	#textColor - string цвет текста
	#backgroundColor - string цвет фона
	#доступные цвета: black, red, green, yellow, blue, purple, cian, white
	reset = '\033[0m'
	color_object = {
		'black': '0',
		'red': '1',
		'green': '2',
		'yellow': '3',
		'blue': '4',
		'purple': '5',
		'cian': '6',
		'white': '7'
	}
	text_color = '\033[3' + color_object[textColor] + 'm'
	bg_color = '\033[4' + color_object[bgColor] + 'm'
	out = text_color + bg_color + text + reset
	return out


def reprint(text='', t_end=False): #очищает текущую строчку и пишет новый текст
	#text - string, нужный текст
	#t_end - boolean, необходим ли перенос строки(True - да, False - нет)
	print('\r\033[K', flush=True, end='')
	if t_end == True:
		print(text, flush=True)
	else:
		print(text, flush=True, end='')


def print_botEvent(event, text):
	if event.from_chat:
		print(datetime.datetime.now().strftime('[%d-%m-%Y %H:%M]'), 'chat:', event.chat_id, 'user:', event.obj.message['from_id'], ':', text)
	elif event.from_user:
		print(datetime.datetime.now().strftime('[%d-%m-%Y %H:%M]'), 'user:', event.obj.message['from_id'], ':', text)
