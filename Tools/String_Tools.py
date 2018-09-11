# -*- encoding:utf-8 -*-
def clean_str(s):
    return s.replace("展开全部", "").replace("本回答由提问者推荐", "").replace("已赞过", "").replace("已踩过", "").replace("评论", "").replace("收起", "").replace("去必应网典查看更多", "").replace("\n", "").strip()
