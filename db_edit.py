# -*- coding: utf-8 -*-
import os
from modules.jsonObjects import json_objects
from DarkySpeak.DarkySpeak import DarkySpeak
print("Processing...")
with open('/storage/sdcard0/DarkyBot5-12-126/mess/' + str(input("input: ")) + '.ini') as mess_data:
	text = mess_data.read()
	mess_data.close()
text = text.lstrip(" ")
peer_id = str(input("output: "))
darky_speak_database = {}
text_l = text.split("\n")
files_count = 0
for i in range(len(text_l)):
	BOT_SPEAK = "/storage/sdcard0/DarkyBot5-15-130/DarkySpeak/" + peer_id + "_" + str(files_count) + ".json"
	if os.path.exists(BOT_SPEAK) == False:
		json_objects.write(darky_speak_database, BOT_SPEAK)
	if os.path.getsize(BOT_SPEAK) < 1048576:
		darky_speak_database = DarkySpeak.read(text_l[i], darky_speak_database)
		json_objects.write(darky_speak_database, BOT_SPEAK)
	else:
		print('\r\033[K', flush=True, end='')
		print(str(peer_id) + "_" + str(files_count) + ".json", str(round(os.path.getsize(BOT_SPEAK) / 1024, 2)), "KB", i, "/", len(text_l))
		files_count += 1
		BOT_SPEAK = "/storage/sdcard0/DarkyBot5-15-130/DarkySpeak/" + peer_id + "_" + str(files_count) + ".json"
		darky_speak_database = DarkySpeak.read(text_l[i], {})
		json_objects.write(darky_speak_database, BOT_SPEAK)
	print('\r\033[K', flush=True, end='')
	print(str(peer_id) + "_" + str(files_count) + ".json", str(round(os.path.getsize(BOT_SPEAK) / 1024, 2)), "KB", i, "/", len(text_l), flush=True, end='')
print()
print("Done")
