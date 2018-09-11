from pymongo import MongoClient
def find(entity):
    client = MongoClient()
    db = client['QAdb']
    ans_rt = []
    rel_set = set()
    for u in db.zhishime.find({'head':entity}):
        rel_set.add(u['relation'])
        ans_rt.append((u['relation'],u['tail']))
    for u in db.posts.find({'head':entity}):
        if(u['relation'] not in rel_set):
            ans_rt.append((u['relation'],u['tail']))
    return (entity,ans_rt)

#if __name__ == "__main__":
