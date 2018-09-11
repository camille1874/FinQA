import codecs

from math import cos, pi

CODE_LENGTH = 8
COEF = [0.1, 0.65, 0.8, 0, 0.9, 0.96, 0, 0, 0.5]
DEGREE = 180


class Similarity:
    def __init__(self):
        self.encode2words = {}
        self.word2encodes = {}
        self.read_dict()        

    def read_dict(self):
        file_object = codecs.open("./data/dict/cilin.txt", 'r', encoding='utf-8')
        items = file_object.readlines()
        for item in items:
            if not (item is None or item == ""):
                strs = item.rstrip().split(" ")
                if len(strs) <= 1:
                    continue
                encode = strs[0]
                words = strs[1:]
                self.encode2words[encode] = words
                for key in words:
                    if key in self.word2encodes:
                        self.word2encodes[key].append(encode)
                    else:
                        self.word2encodes[key] = [encode]

    def get_common_encode(self, encode1, encode2):
        for i in range(len(encode1)):
            if encode1[i] != encode2[i]:
                if i == 0:
                    return None
                if i == 3 or i == 6:
                    i -= 1
                return encode1[:i]
        return encode1

    def get_nodes(self, common_str):
        nodes = set()
        str_len = len(common_str) + 1
        for i in self.encode2words.keys():
            if i.startswith(common_str):
                nodes.add(i[:str_len])
        return len(nodes)

    def get_dis(self, encode1, encode2, common_len):
        if (common_len == 8):
            return 0
        if (common_len == 2 or common_len == 5):
            tmp1 = encode1[common_len: common_len + 2]
            tmp2 = encode2[common_len: common_len + 2]
            return abs(int(tmp1) - int(tmp2))
        else:
            tmp1 = encode1[common_len]
            tmp2 = encode2[common_len]
            return abs(ord(tmp1) - ord(tmp2))

    def get_simi(self, word1, word2):
        if word1 not in self.word2encodes or word2 not in self.word2encodes:
            return COEF[0]  # 到word2vec中查找
        encode1 = self.word2encodes[word1]
        encode2 = self.word2encodes[word2]
        max_simi = 0
        for e1 in encode1:
            for e2 in encode2:
                simi = 0
                common_str = self.get_common_encode(e1, e2)
                if common_str == None:
                    simi = COEF[0]
                else:
                    common_len = len(common_str)
                    dis = self.get_dis(e1, e2, common_len)
                    # print("dis")
                    # print(dis)
                    nodes = self.get_nodes(common_str)
                    # print("nodes")
                    # print(nodes)
                    if common_len == 8:
                        if common_str[-1] == "=":
                            simi = 1
                        elif common_str[-1] == "#":
                            simi = COEF[common_len]
                    else:
                        simi = COEF[common_len] * cos(nodes * pi / DEGREE) * ((nodes - dis + 1) / nodes)
                if simi > max_simi:
                    max_simi = simi
        return max_simi


if __name__ == "__main__":
    s = Similarity()
    word1 = "爸爸"
    word2 = "妈妈"
    sim = s.get_simi(word1, word2)
    print(word1 + "-" + word2)
    print(sim)
    word1 = "母亲"
    word2 = "妈妈"
    sim = s.get_simi(word1, word2)
    print(word1 + "-" + word2)
    print(sim)
    word1 = "母亲"
    word2 = "父亲"
    sim = s.get_simi(word1, word2)
    print(word1 + "-" + word2)
    print(sim)
    while True:
        word1 = input("第一个词")
        word2 = input("第二个词")
        print(s.get_simi(word1, word2))
