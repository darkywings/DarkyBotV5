import traceback
import sys

def getTraceback(footnotes): #формирование трейсбека и отправка сообщением
	#footnotes - int, количество '\n' (сносок)(min - 0, max - 4)
	exc_type, exc_value, exc_traceback = sys.exc_info()
	tbObject = traceback.format_exception(exc_type, exc_value, exc_traceback, limit = 5)
	tbOut = '' #трейсбек будет записываться сюда
	fns = '' #сноски
	for i in range(footnotes):
		fns += '\n'
	for c in range(len(tbObject)):
		tbOut = tbOut + tbObject[c] + fns
	return tbOut