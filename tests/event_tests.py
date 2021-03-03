import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game, Event
from datetime import datetime

class EventTests(APITestCase):
	def setUp(self):
		"""
		Create a new account and create sample category
		"""
		url = "/register"
		data = {
			"username": "steve",
			"password": "Admin8*",
			"email": "steve@stevebrownlee.com",
			"address": "100 Infinity Way",
			"phone_number": "555-1212",
			"first_name": "Steve",
			"last_name": "Brownlee",
			"bio": "Love those gamez!!"
		}
		response = self.client.post(url, data, format='json')

		json_response = json.loads(response.content)

		self.token = json_response["token"]

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		gametype = GameType()
		gametype.label = "Board game"
		gametype.save()

		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

		url = "/games"

		data = {
			"gameTypeId": 1,
			"title": "Clue",
			"description": "Milton Bradley",
			"numberOfPlayers": 6,
		}

		response = self.client.post(url, data, format='json')

		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(json_response["title"], "Clue")
		self.assertEqual(json_response["description"], "Milton Bradley")
		self.assertEqual(json_response["number_of_players"], 6)

	def test_create_event(self):
		"""
		Ensure we can create a new event.
		"""
		url = "/events"
		data = {
			"time": "2021-03-02 15:53:53.043387",
			"location": "Living room",
			"gameId": 1,
		}


		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

		response = self.client.post(url, data, format='json')

		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		self.assertEqual(json_response["location"], "Living room")
		self.assertEqual(json_response["game"]["id"], 1)
		self.assertEqual(json_response["event_time"], "2021-03-02 15:53:53.043387")

	def test_get_event(self):
		"""
		Ensure we can get an existing event.
		"""

		# Seed the database with a game
		event = Event()

		now = datetime.now()

		event.game_id = 1
		event.scheduler_id = 1
		event.location = "Living room"
		event.event_time = now
		event.save()

		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

		response = self.client.get(f"/events/{event.id}")

		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.assertEqual(json_response["game"]["id"], 1)
		self.assertEqual(json_response["location"], "Living room")
		self.assertEqual(json_response["scheduler"]["id"], 1)
		self.assertEqual(json_response["event_time"], now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

		#2021-03-02T16:30:25.535442Z

	# def test_change_game(self):
	# 	"""
	# 	Ensure we can change an existing game.
	# 	"""
	# 	game = Game()
	# 	game.game_type_id = 1
	# 	#game.skill_level = 5
	# 	game.title = "Sorry"
	# 	game.description = "Milton Bradley"
	# 	game.number_of_players = 4
	# 	game.gamer_id = 1
	# 	game.save()

	# 	# DEFINE NEW PROPERTIES FOR GAME
	# 	data = {
	# 		"gameTypeId": 1,
	# 		"title": "Sorry",
	# 		"description": "Hasbro",
	# 		"numberOfPlayers": 4
	# 	}

	# 	self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
	# 	response = self.client.put(f"/games/{game.id}", data, format="json")
	# 	self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	# 	# GET GAME AGAIN TO VERIFY CHANGES
	# 	response = self.client.get(f"/games/{game.id}")
	# 	json_response = json.loads(response.content)
	# 	self.assertEqual(response.status_code, status.HTTP_200_OK)

	# 	# Assert that the properties are correct
	# 	self.assertEqual(json_response["title"], "Sorry")
	# 	self.assertEqual(json_response["description"], "Hasbro")
	# 	self.assertEqual(json_response["number_of_players"], 4)

	# def test_delete_game(self):
	# 	"""
	# 	Ensure we can delete an existing game.
	# 	"""
	# 	game = Game()
	# 	game.game_type_id = 1
	# 	game.title = "Sorry"
	# 	game.description = "Milton Bradley"
	# 	game.number_of_players = 4
	# 	game.gamer_id = 1
	# 	game.save()

	# 	self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
	# 	response = self.client.delete(f"/games/{game.id}")
	# 	self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	# 	# GET GAME AGAIN TO VERIFY 404 response
	# 	response = self.client.get(f"/games/{game.id}")
	# 	self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)