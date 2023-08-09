import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from modules import darkyExceptions
from vk_api.utils import get_random_id


class bot:
	
	def auth(group_id, group_token):
		#group_id - id группы без минуса спереди.
		#token - токен сообщества
		vk_session = vk_api.VkApi(token=group_token) #авторизация как сообщество
		botlongpoll = VkBotLongPoll(vk_session, group_id)
		vk = vk_session.get_api()
		return botlongpoll, vk
	
	def typing_state(vk, event): #установка статуса тайпинга
		#event - событие от вк
		#vk - api полученный в результате авторизации
		vk.messages.setActivity(
			type = 'typing',
			peer_id = event.obj.message['peer_id']
		)
	
	def send_mess(vk, peer_ids=None, text='', attachments=''): #отправка сообщения
		#peer_ids - id бесед(-ы) или пользователя(-ей) куда будет отправлено сообщение
			#пользователи - положительные числа меньше 2000000000
			#беседы - положительные числа больше 2000000000
			#группы - отрицательные числа
		#text - текст сообщения
		#attachments - вложения.
		# !!!необходимо указывать название параметров при вызове функции(кроме vk)
		if peer_ids is None:
			raise darkyExceptions.DarkyError(9)
		else:
			vk.messages.send(
				peer_ids = peer_ids,
				random_id = get_random_id(),
				message = text,
				attachment = attachments
			)
	
	def bot_admin_check(vk, event): #проверка админки у бота(не особо используется, но хранится на всякий случай)
		try:
			vk.messages.getConversationMembers(peer_id = 2000000000 + event.chat_id)
			return True
		except vk_api.exceptions.ApiError:
			raise darkyExceptions.DarkyError(2)
	
	def user_admin_check(vk, chat_id, member_id): #проверяет админку у пользователя(также как и с админкой у бота)
		user_is_admin = False
		members_list = vk.messages.getConversationMembers(peer_id = 2000000000 + chat_id)
		for current_member in range(members_list["count"]):
			if members_list["items"][current_member]["member_id"] == id:
				try:
					user_is_admin = members_list["items"][current_member]["is_admin"]
				except:
					user_is_admin = False
		return user_is_admin
	
	def search_id(event, user, cs_users_list={}): #поиск id пользователя
		#cs_users_list - объект, список пользователей в настройках беседы
		#поиск настоящего идентификатора пользователя по никнейму/id/ответу/пересланному сообщению
		id_founded = False
		if user != "":
			if user.startswith('[id'):
				#упоминания вк всегда выглядят как [id<id>|<text>]
				#парсинг информации
				id = int(user.split('|')[0].lstrip('[id'))
				id_founded = True
			elif user.startswith('[club'):
				#парсинг информации вида [club<group_id>|<text>]
				id = -int(user.split('|')[0].lstrip('[club'))
				id_founded = True
			elif user.isdigit() == True:
				if int(user) > -999999999 and int(user) < 999999999:
					id = int(user)
					id_founded = True
			elif cs_users_list != {}:
				#поиск по никнейму
				ready = False
				for curr_user in range(len(list(cs_users_list))):
					if cs_users_list[list(cs_users_list)[curr_user]]["nickname"] == user:
						ready = True
						break
				if ready != False:
					id = int(list(cs_users_list)[curr_user])
					id_founded = True
		elif id_founded == False and event.obj.message["fwd_messages"] != []:
			#извлекание идентификатора из пересланного сообщения
			id = event.obj.message["fwd_messages"][0]["from_id"]
			id_founded = True
		elif id_founded == False and "reply_message" in event.obj.message:
			#извлекание идентификатора из ответа(обрабатывается поскольку "reply_message" бывает отсутствует)
			id = event.obj.message["reply_message"]["from_id"]
			id_founded = True
		if id_founded == True:
			return id
		else:
			raise darkyExceptions.DarkyError(6)

	def is_chat_member(vk, event, id, chat_members=None): #является ли id учатсником беседы
		if chat_members == None:
			chat_members = vk.messages.getConversationMembers(peer_id = 2000000000 + event.chat_id)
		id_founded = False
		if id > 0:
			for curr_mem in range(len(list(chat_members["profiles"]))):
				if chat_members["profiles"][curr_mem]["id"] == id:
					id_founded = True
					break
		elif id < 0:
			for curr_mem in range(len(list(chat_members["groups"]))):
				if chat_members["groups"][curr_mem]["id"] == id:
					id_founded = True
					break
		return id_founded
