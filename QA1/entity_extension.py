# -*-coding:utf-8-*-

import codecs
import time
import jieba
import global_data


class EntityExtension:
    def __init__(self):
        self.entity_set = {}  # entity => aliases
        self.reversed_set = {}  # alias => entity

    def load_alias(self, entity_extension=global_data.entity_extension_file_name):
        file_obj = codecs.open(entity_extension, 'r', encoding='utf-8')
        for i, line in enumerate(file_obj.readlines()):
            try:
                entity, other = line.rstrip().split(' ||| ')
                aliases = other.split('\t')
                self.entity_set[entity] = set(aliases)
                for alias in aliases:
                    self.reversed_set[alias] = entity
            except:
                continue
        file_obj.close()
        print('Loading extension file finished.')

    def show(self, total=30):
        for i, entity in enumerate(self.entity_set.keys()):
            print(i, "entity:", entity)
            for alias in self.entity_set[entity]:
                print(alias)
            if i > total:
                break

    def search_aliases(self, entity):
        if entity in self.entity_set:
            for alias in self.entity_set[entity]:
                print(alias)
            return self.entity_set[entity]
        else:
            print(entity + 'not found!')
            return set()

    def search_entity(self, alias):
        if alias in self.reversed_set:
            return self.reversed_set[alias]
        else:
            print(alias + 'not found!')
            return alias


if __name__ == '__main__':
    mid = EntityExtension()
    mid.load_alias()
    # mid.print()
    while True:
        s = jieba.cut(input())
        print("fenci:",s)
        for item in s:
            result = mid.search_aliases(item)
            if len(result) > 0:
                print(result)
