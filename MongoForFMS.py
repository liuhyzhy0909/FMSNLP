#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pymongo import MongoClient
import  regex as re
settings = {
    "ip":'localhost',   #ip
    "port":27017,           #端口
    "db_name" : "mydb",    #数据库名字
    "set_name" : "test_set"   #集合名字
}

class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db[settings["set_name"]]

    def insert(self,dic):
        print("inser...")
        self.my_set.insert(dic)

    def update(self,dic,newdic):
        print("update...")
        self.my_set.update(dic,newdic)

    def delete(self,dic):
        print("delete...")
        self.my_set.remove(dic)

    def dbfind(self,dic):
        data = self.my_set.find(dic)
        for result in data:
            return result["value"]

def main():
    mongo = MyMongoDB()
    #dic = {"name": "药占比", "value": "keyword_name"}
    #mongo.insert(dic)

    f = open("1_updata.txt",encoding="utf-8")
    for line in f:
        lines = re.split(r'\s+',str(line).strip())
        tname = lines[0]
        tvalue = lines[1]
        #print("name:"+ tname  + "value:" + tvalue)
        dic={"name":tname,"value":tvalue}
        mongo.insert(dic)

if __name__ == "__main__":
    main()

'''
#门诊量	keyword_name
#全院	department
#内一科	department
#最高	keyword_type_max
#最多	keyword_type_max
'''