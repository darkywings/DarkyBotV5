import json

class json_objects:
	
	def write(object, path): #запись json-обьекта в файл
		#object - obj, обьект который будет записываться в файл
		with open(path, 'w') as jsonFile:
			jsonFile.write(json.dumps(object, indent=4, ensure_ascii=False))
			jsonFile.close()
	
	
	def load(path): #загрузка json-обьекта из файла
		#path - string, путь к файлу
		with open(path, 'r') as jsonFile:
			jsonContent = json.load(jsonFile)
			jsonFile.close()
		return jsonContent