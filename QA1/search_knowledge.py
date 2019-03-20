from pymongo import MongoClient
def find(entity, db):
    ans_rt = []
    rel_set = set()
    for u in db.find({'head':entity}):
        rel_set.add(u['relation'])
        ans_rt.append((u['relation'],u['tail']))
    return (entity,ans_rt)





def stat():
    try:
        #with MongoClient("mongodb://172.16.35.1:27017") as client:
        with MongoClient("mongodb://172.16.31.1:27017") as client:
            db = client['triple']
            m_collection = db['baidubaike']
            return m_collection
    except Exception as e:
        print(e)


