import unittest
import A3_clientserver

class Test(unittest.TestCase):


    def test_get_1(self):
        client = A3_clientserver.Benutzerschnittstelle()        
        self.assertEqual({'name': 'Ries', 'prename': 'Patrick', 'age': 22}, client.get("Patrick Ries"))    

    def test_get_2(self):
        client = A3_clientserver.Benutzerschnittstelle()        
        self.assertEqual({'name': 'Kai', 'prename': 'Schwank', 'age': 21}, client.get("Schwank Kai"))

    def test_get_3(self):
        client = A3_clientserver.Benutzerschnittstelle()        
        self.assertEqual({'name': 'Ries', 'prename': 'Patrick', 'age': 22}, client.get("PatRick RiEs"))  

    def test_get_6(self):
        client = A3_clientserver.Benutzerschnittstelle()        
        self.assertNotEqual({'name': 'Kai', 'prename': 'Schwank', 'age': 21}, client.get("Kai"))

    def test_get_7(self):
        client = A3_clientserver.Benutzerschnittstelle()        
        self.assertNotEqual({'name': 'Kai', 'prename': 'Schwank', 'age': 21}, client.get("Schwank"))



    def test_get_all(self):
        client = A3_clientserver.Benutzerschnittstelle()        
        self.assertEqual({'1': {'name': 'Ries', 'prename': 'Patrick', 'age': 22}, '2': {'name': 'Kai', 'prename': 'Schwank', 'age': 21}}, client.get_all())





if __name__ == '__main__':
    unittest.main()
