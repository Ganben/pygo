from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)

db = client.bleparking

#rewrite the save method of agent, for other objects, replace agent;
    def save(self):
        current = {
                   "key1": self.key1, #fill it with corrected or permitted field;
                   "key2": self.key2,
                   ....
                   }

        agent = db.agent
        pre = agent.find_one({'_id': ObjectId(self.pk)}) #should confirm if self.pk exist
        if pre == None:
            #TODO: init default value of a new object here;
            pre_id = agent.insert_one(current).inserted_id
            #if not exist, insert and print id here, if true then success
        else:
            #if exist, update it manually
            res =  agent.update_one({'_id': ObjectId(self.pk)},
                    {'$set': current})
            if res == 1:
                //success


