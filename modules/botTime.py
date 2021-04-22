import time
import datetime


class bot_timer: #кастомный таймер(работает только в секундах)
	#результат вида: 15.294
	timerBegin = 0.0
	timerResult = 0.0
	
	def start(): #начало отсчёта таймера
		global timerBegin
		timerBegin = time.time()
		
	def stop(): #конец отсчёта таймера
		global timerBegin
		global timerResult
		timerResult = round(time.time() - timerBegin, 3)
		return timerResult


class bot_timer2: #модифицированный таймер
	#работает в связке с классом  bot_timer
	#резулультат вида: 39дн. 9ч. 32мин. 58сек.
	def getTime(time_start, time_end):
		time_out = time_end - time_start
		
		#вычисление дней
		t_days = time_out // 60 // 60 // 24
		time_out -= (t_days * 24 * 60 * 60)
		
		#вычисление часов
		t_hours = time_out // 60 // 60
		time_out -= (t_hours * 60 * 60)
		
		#вычисление минут
		t_minutes = time_out // 60
		time_out -= (t_minutes * 60)
		
		#остаток - секунды
		t_seconds = time_out
		
		t_out_str = str(t_days) + 'дн. ' + str(t_hours) + 'ч. ' + str(t_minutes) + 'мин. ' + str(t_seconds) + 'сек.'
		return t_out_str