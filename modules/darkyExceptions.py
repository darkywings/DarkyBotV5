
def get_error(error_code=0):
	
	errors = { #база данных ошибок
		"1": "Access denied",
		"2": "Bot is not admin",
		"3": "Access denied: user is not admin",
		"4": "Command doesn't work here",
		"5": "Darky can't be used in this command!",
		"6": "Id not found",
		"7": "User/group is not chat member",
		"8": "Id is group",
		"9": "Wrong method params",
		"10": "This command was deactivated",
		"11": "User is admin",
		"12": "Id is DarkyBot",
		
		"50": "Wrong association name",
		"51": "Association for current command not found",
		
		"100": "Chat is already registered",
		"101": "Chat is not registered",
		"102": "User is not registered in the chat",
		"103": "This preset doesn't exist",
		
		"150": "Greeting does not exist",
		"151": "Rules does not exist",
		"152": "Greeting set error",
		"153": "Rules set error",
		"154": "Update access keys for greetings error",
		"155": "Attachment in the greeting didn't set",
		
		"200": "User is already banned in this chat",
		"201": "User is already unbanned in this chat",
		"202": "Banlist is empty",
		"203": "Warn list is empty",
		
		"250": "Wrong args count(must be equals)",
		"251": "Wrong args count(more than maximal)",
		"252": "Wrong args count(less than minimal)",
		"253": "Incorrect arguments for this command",
		"254": "(top members list) Wrong value in argument",
		
		"300": "User not verified(Account was created in 2-10 last days)",
		"301": "User not verified(Account doesn't have photo)",
		"302": "User not verified(Account doesn't have friends)",
		"304": "User not verified(Account is not group member)",
		
		"400": "This nickname is already used",
		"401": "Nickname list is empty",
		"402": "Access denied: you can't change other people's nicknames",
		
		"450": "This roleplay command is already exist",
		"451": "This roleplay command is not exist",
		"453": "Access denied: You don't have access to manage this rp command",
		"454": "User closed his rp access",
		
		"500": "Invalid parameter name in bot settings",
		"501": "Invalid value for parameter in bot settings",
		"502": "Wrong param value in bot settings",
		"503": "(DarkyVerify)Group not found",
		
		"600": "Notes list is empty",
		"601": "This note didn't found",
		"602": "Incorrect note's title",
		"603": "This title is already used",
		"604": "This note is didn't deleted"
	}
	
	if str(error_code) in errors:
		error = {
			"code": error_code,
			"msg": errors[str(error_code)]
		}
	else:
		error = {
			"code": 0,
			"msg": "Unknown exception"
		}
	return error


class ReadBotSettingsExc:
	pass

class DarkyError(Exception):
	#исключение внутри Дарки
	
	def __init__(self, error):
		self.code = error["code"]
		self.msg = error["msg"]
		self.error = error
	
	def __str__(self):
		return "\n\nERROR CODE: " + str(self.code) + "\nERROR MSG: " + self.msg
