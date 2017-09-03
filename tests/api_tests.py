import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO, BytesIO

import sys; print(list(sys.modules.keys()))
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "project.config.TestingConfig"

from project import app
from project import models
from project.utils import upload_path
from project.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)


    def test_get_posts(self):
        cat = models.Label(name="cat")
        dog = models.Label(name="dog")
        postA = models.Post(channel="Facebook", social_id="1", content='In case you missed it... "Everything comes to life when it has movement" says Artist of the moment and NYX Spain Face Awards 2016 Winner, Jimena! 🎨 Watch how she creates this peachy, pink makeup look inspired by her own art. 🖌', post_url="https://www.facebook.com/ipsy/videos/1439586409422009/",img_url="https://scontent.xx.fbcdn.net/v/t15.0-10/s720x720/19691980_1390243597689624_6854099318526181376_n.jpg?oh=1861694b4bd98022b55c12061c0feb8e&oe=5A1B1AA5")
        postA.labels = [cat]
        postB = models.Post(channel="Facebook", social_id="2", content='In case you missed it... "Everything comes to life when it has movement" says Artist of the moment and NYX Spain Face Awards 2016 Winner, Jimena! 🎨 Watch how she creates this peachy, pink makeup look inspired by her own art. 🖌', post_url="https://www.facebook.com/ipsy/videos/1439586409422009/", img_url="https://scontent.xx.fbcdn.net/v/t15.0-10/s720x720/19691980_1390243597689624_6854099318526181376_n.jpg?oh=1861694b4bd98022b55c12061c0feb8e&oe=5A1B1AA5")
        postB.labels = [dog]
        postC = models.Post(channel="Facebook", social_id="3", content='In case you missed it... "Everything comes to life when it has movement" says Artist of the moment and NYX Spain Face Awards 2016 Winner, Jimena! 🎨 Watch how she creates this peachy, pink makeup look inspired by her own art. 🖌', post_url="https://www.facebook.com/ipsy/videos/1439586409422009/", img_url="https://scontent.xx.fbcdn.net/v/t15.0-10/s720x720/19691980_1390243597689624_6854099318526181376_n.jpg?oh=1861694b4bd98022b55c12061c0feb8e&oe=5A1B1AA5")
        postC.labels = [cat,dog]
        session.add_all([postA,postB,postC])
        session.commit()

        response = self.client.get("/api/posts",
                headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(data), 3)

        postA = data[0]
        self.assertEqual(postA["social_id"], '1')
        self.assertEqual(postA["post_url"], "https://www.facebook.com/ipsy/videos/1439586409422009/")
        self.assertEqual(postA["labels"][0]["name"], "cat")

        postB = data[1]
        self.assertEqual(postB["social_id"], '3')
        self.assertEqual(postB["post_url"], "https://www.facebook.com/ipsy/videos/1439586409422009/")
        self.assertEqual(postB["labels"][0]["name"], "cat")
        self.assertEqual(postB["labels"][1]["name"], "dog")

        postC = data[2]
        self.assertEqual(postC["social_id"], '2')
        self.assertEqual(postC["post_url"], "https://www.facebook.com/ipsy/videos/1439586409422009/")
        self.assertEqual(postC["labels"][0]["name"], "dog")

    def test_add_label_association(self):
        #TODO
        pass

    def test_remove_label_association(self):
        cat = models.Label(name="cat")
        dog = models.Label(name="dog")
        postA = models.Post(channel="Facebook", social_id="1",
                            content='In case you missed it... "Everything comes to life when it has movement" says Artist of the moment and NYX Spain Face Awards 2016 Winner, Jimena! 🎨 Watch how she creates this peachy, pink makeup look inspired by her own art. 🖌',
                            post_url="https://www.facebook.com/ipsy/videos/1439586409422009/",
                            img_url="https://scontent.xx.fbcdn.net/v/t15.0-10/s720x720/19691980_1390243597689624_6854099318526181376_n.jpg?oh=1861694b4bd98022b55c12061c0feb8e&oe=5A1B1AA5")
        postA.labels = [cat]
        postB = models.Post(channel="Facebook", social_id="2",
                            content='In case you missed it... "Everything comes to life when it has movement" says Artist of the moment and NYX Spain Face Awards 2016 Winner, Jimena! 🎨 Watch how she creates this peachy, pink makeup look inspired by her own art. 🖌',
                            post_url="https://www.facebook.com/ipsy/videos/1439586409422009/",
                            img_url="https://scontent.xx.fbcdn.net/v/t15.0-10/s720x720/19691980_1390243597689624_6854099318526181376_n.jpg?oh=1861694b4bd98022b55c12061c0feb8e&oe=5A1B1AA5")
        postB.labels = [dog]
        postC = models.Post(channel="Facebook", social_id="3",
                            content='In case you missed it... "Everything comes to life when it has movement" says Artist of the moment and NYX Spain Face Awards 2016 Winner, Jimena! 🎨 Watch how she creates this peachy, pink makeup look inspired by her own art. 🖌',
                            post_url="https://www.facebook.com/ipsy/videos/1439586409422009/",
                            img_url="https://scontent.xx.fbcdn.net/v/t15.0-10/s720x720/19691980_1390243597689624_6854099318526181376_n.jpg?oh=1861694b4bd98022b55c12061c0feb8e&oe=5A1B1AA5")
        postC.labels = [cat, dog]
        session.add_all([postA, postB, postC])
        session.commit()

        response = self.client.delete("/api/label/association_delete",
                                   headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")





    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()