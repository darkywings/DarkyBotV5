import traceback
from sys import exc_info

def getTraceback(footnotes, mode=0): #формирование трейсбека и отправка сообщением
	#footnotes - int, количество '\n' (сносок)(min - 0, max - 4)
	#mode - отвечает за режим вывода трейсбека (0 - стандартный, как в консоли, 1 - внешне модифицированный, без лишнего)
	exc_type, exc_value, exc_traceback = exc_info()
	tbObject = traceback.format_exception(exc_type, exc_value, exc_traceback, limit = 5)
	tbOut = '' #трейсбек будет записываться сюда
	fns = '' #сноски
	for i in range(footnotes):
		fns += '\n'
	if mode == 0: #стандартный режим трейсбека, выводящий весь объект полностью
		for c in range(len(tbObject)):
			tbOut = tbOut + tbObject[c] + fns
	elif mode == 1: #внешне модифицированный трейсбек и без лишнего
		tb_filename = str(traceback.extract_tb(exc_info()[2])[-1][0])
		tb_lineindex = str(traceback.extract_tb(exc_info()[2])[-1][1])
		tb_exctype = tbObject[-1]
		#формирование трейсбека
		tbOut = "FILE: '" + tb_filename + "'" + fns
		tbOut += "LINE: " + tb_lineindex + fns
		tbOut += "TYPE: " + tb_exctype + fns
	return tbOut
