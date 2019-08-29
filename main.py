#!/usr/bin/python3
import json
import random
import os
from set_types import *
set_objects = dict()
randx = random.randint(0, 79)
randy = random.randint(0, 79)
import requests


def sort_sets():
	for file in os.listdir(os.path.join('.', 'jsons')): 
		if file.endswith('.json'):
			with open(os.path.join('jsons', file)) as json_data:
				#Get the set name:
				set_name = os.path.splitext(str(file))[0]

				#Identify what kind of set this is:
				for i in CS.Core_Set.sets:
					if(set_name.startswith(i)):
						set_objects[set_name] = CS.Core_Set()

				for i in HA.Hidden_Arsenal_Like.sets:
					if(set_name.startswith(i)):
						set_objects[set_name] = HA.Hidden_Arsenal_Like()

				for i in GS.Gold_Series.sets:
					if(set_name.startswith(i)):
						set_objects[set_name] = GS.Gold_Series()

				for i in BP.Battle_Pack.sets:
					if(set_name.startswith(i)):
						set_objects[set_name] = BP.Battle_Pack()

				data = json.load(json_data)
				for x in data:
					if '\n' in x['rarity'] :
						for i in x['rarity'].split('\n'):
							set_objects[set_name].add_card(str(i), str(x['name']))
					else:
						set_objects[set_name].add_card(str(x['rarity']), str(x['name']))



def main(filename):
	sort_sets()

	'''
	x = []
	for i in range(12):
		randx = random.randint(0, 79)
		selected_set = set_objects[list(set_objects.keys())[randx]]
		print(list(set_objects.keys())[randx])
		x.extend(selected_set.generate_pack())
	'''
	

	selected_set = set_objects[str("BP03-EN")]
	x = []
	
	for i in range(4):
		x.extend(selected_set.generate_pack())


	'''
	selected_set = set_objects[str("BP02-EN")]
	for i in range(1):
		x.extend(selected_set.generate_pack())



	print(list(set_objects.keys())[randx])
	print(list(set_objects.keys())[randy])

	selected_set = set_objects[list(set_objects.keys())[randx]]
	#selected_set = set_objects[str("NUMH-EN")]
	for i in range(2):
		x.extend(selected_set.generate_pack()[:5])

	selected_set = set_objects[list(set_objects.keys())[randy]]
	for i in range(1):
		x.extend(selected_set.generate_pack()[:5])
	'''


	main = []
	extra = []
	for each in x:
		temp = "https://db.ygoprodeck.com/api/v5/cardinfo.php?name={}".format(each.strip()).strip()
		response = requests.get(temp)
		try:
			data = response.json()[0]
		except:
			print(each)
			print(temp)

		#print (data['id'])
		if (data['type'] == "XYZ Monster"):
			extra+= [data['id']]
		else:
			main += [data['id']]



	file_name = filename+'.ydk'
	f = open(file_name, 'a+')  # open file in append mode
	f.write('#created by ...\n')
	f.write('#main\n')
	f.write(str(len(main)))
	f.write("\n")
	for each in main:
		print(each)
		f.write(each)
		f.write("\n")

	print("\nextra deck")
	f.write('#extra\n')
	for each in extra:
		print(each)
		f.write(each)
		f.write("\n")

	f.write("\n!side")	
	f.close()

if __name__ == '__main__':
	try:
		os.remove("deck1.ydk")
		os.remove("deck2.ydk")
	except:
		pass
	main("deck1")
	main("deck2")
