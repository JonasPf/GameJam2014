from main import Obstacle, Recharge, Character

def create_obstacles(pictures):
	return [
		# Obstacle((-50,5), pictures['asteroid']),
		# Obstacle((300, 300), pictures['planet']),
		Obstacle((-1000, -1000), pictures['bigwhite8']), #, deadly=True
		Obstacle((3000, -7000), pictures['mediumred6']), 
		Obstacle((-11000, -3000), pictures['smallgreen6']), 
		Obstacle((-15000, -5000), pictures['bigblue3']), 
		Obstacle((-5000, -11000), pictures['smallgold3']), 
		Obstacle((-19000, -11000), pictures['mediumblue2']), 
		Obstacle((-15000, -19000), pictures['smallred2']),
		Obstacle((7000, 7000), pictures['mediumwhite2']), 
		Obstacle((19000, 17000), pictures['elysium'], deadly=True), 
		Obstacle((-15000, -11000), pictures['sun'], deadly=True), 
		Obstacle((5000, -1000), pictures['sun'], deadly=True), 
		Obstacle((15000, 17000), pictures['sun'], deadly=True), 
	]

def create_rechargers(pictures):
	return [
		Recharge((-11021, -3208), pictures['recharger']),
		Recharge((-1102, -1708), pictures['recharger_big']),
	]

def create_characters(pictures):
	return [
		# bigwhite
		Character((-800, -600), pictures['character'], ["Hover near the water to refuel!"]),
		Character((-1200, -500), pictures['character'], ["Go to the green planet!", 'It\'s position is -110/-30']),

		# smallgreen
		Character((-11207, -2900), pictures['character_small'], ["I know where Elysium is.", "Elysium is east of the sun in 150/170"]),
		Character((-11100, -2900), pictures['character_small'], ["There is a small golden planet.", "It's in -50/-110"]),
		Character((-11000, -2900), pictures['character_small'], ["There is a big blue planet.", "It's in -150/-50"]),
	]
