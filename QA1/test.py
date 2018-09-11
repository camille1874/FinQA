# -*- encoding:utf-8 -*-
import synonyms
print("位置: %s" % (synonyms.nearby("位置")))
print("英文名: %s" % (synonyms.nearby("英文名")))
print("NOT_EXIST: %s" % (synonyms.nearby("NOT_EXIST")))

s1 = "效力于哪个队"
s2 = "所属运动队"
r = synonyms.compare(s1, s2, seg=True)
print(s1, s2, "相似度：", r)

s1 = "效力于哪个队"
s2 = "位置"
r = synonyms.compare(s1, s2, seg=True)
print(s1, s2, "相似度:", r)

s1 = "出生在哪里"
s2 = "出生地"
r = synonyms.compare(s1, s2, seg=True)
print(s1, s2, "相似度:", r)

s1 = "出生在哪里"
s2 = "初中"
r = synonyms.compare(s1, s2, seg=True)
print(s1, s2, "相似度:", r)

s1 = "奖"
s2 = "主要奖项"
r = synonyms.compare(s1, s2, seg=True)
print(s1, s2, "相似度:", r)

s1 = "奖"
s2 = "自传"
r = synonyms.compare(s1, s2, seg=True)
print(s1, s2, "相似度:", r)

s1 = "写"
s2 = "作者"
r = synonyms.compare(s1, s2, seg=True)
print(s1, s2, "相似度:", r)

s1 = "写"
s2 = "发行"
r = synonyms.compare(s1, s2, seg=True)
print(s1, s2, "相似度:", r)

# 出生地点 出生地 相似度： 0.762
# 出生地点 地点 相似度: 0.582
# 出生日期 生日 相似度: 0.696
# word2vec里没有的词