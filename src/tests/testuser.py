import requests, unittest

class TestUser(unittest.TestCase):
  base_url = 'http://localhost:8000'

  def test_list_users(self):
    response = requests.get(f"{self.base_url}/list-users/")

    self.assertNotEqual(len(response.json()), 0)
  
  def test_create_users(self):
    payload = {
	    "name": "jerbeson",
	    "email": "jerbesonviny@gmail.com",
	    "password": "123"
    }

    response = requests.post(
      f"{self.base_url}/register/", 
      data=payload
    )

    self.assertLess(0, response.json())