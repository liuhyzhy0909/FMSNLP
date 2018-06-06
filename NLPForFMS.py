# -*- coding: utf-8 -*-
import thulac
from MongoForFMS import MyMongoDB
import importlib,sys
import regex as re
from TimeParse import TimeParse
import pickle
importlib.reload(sys)
#sys.setdefaultencoding('utf-8')
class SelectForFMS(object):
    #selectTest = '2017年6月全院门诊量最高的科室'#输入文本
    '''
    {
        "keyword":
        {   "name":"门诊量",
            "type":"max"
        },
        "dimension":
        {
            "t":{["6月","7月","8月"]},
            "dep":{["内一科"]}
        }        
    }
    '''
    user_dict = '1_updata.txt'#用户词典
    T2S = ''#是否将繁体转换为简体
    seg_only = ''#是否进行标注
    filt = ''#过滤器
    model_path = ''#模型文件夹
    model = ''

    def fenci(self,js):#分词
        print(js)
        jsondict = {"dimension": {}, "keyword": {}}  # 返回的json串
        selectTest = js["NLPstring"]
        thu1 = thulac.thulac(user_dict = self.user_dict , seg_only = False)  #默认模式
        text = thu1.cut(selectTest, text = True)
        TimeList = []    # 时间列表
        DepartList = ["全院"]  # 科室列表，默认全院
        mongo = MyMongoDB()
        texts = str(text).split(' ')
        for i in texts:
            tmps = str(i).split("_")
            value = mongo.dbfind({"name": tmps[0]})

            if (value != None):
                print(tmps[0] + "_" + value)
            else:
                value = tmps[1]
                print(tmps[0] + "_" + value)

            dimens = str(value).split('_')
            if(len(dimens)==1):

            # 加入时间列表
                '''
                if (value == 't'):
                    TimeList.append(tmps[0])
             '''

                if (value == 'department'):
                    if "全院" in DepartList:
                        DepartList.remove("全院")
                    DepartList.append(tmps[0])

            if (len(dimens) == 2):
                jsondict[dimens[0]][dimens[1]] = tmps[0]

            if (len(dimens) == 3):
                jsondict[dimens[0]][dimens[1]] = [dimens[2]]

        '''
        获取时间
       '''

        pkl_file = open('timedict_re.pkl', 'rb')
        time_str = pickle.load(pkl_file)
        pkl_file.close()
        pattern = re.compile(time_str)


        Time = []
        for m in pattern.finditer(selectTest):
            print(m.group())
            Gsize = TimeParse.findGsize(TimeParse,m.group())
            Time.append(TimeParse.getTime(TimeParse,m.group()))
        Time = sum(Time,[])

        # Gsize = findGsize(s)#在匹配后的时间字符串内寻找代表时间粒度的关键字，目的是排查除时间表达式之外的字符串含有相应的关键字
        #print(Time)

        jsondict["dimension"]["t"] = Time #+ Gsize
        jsondict["dimension"]["dep"] = DepartList
        print(jsondict)
        return  jsondict

        '''
       user_dict='C://UserDict//THUOCL_medical.txt'
       thulac(user_dict=None, model_path=None, T2S=False, seg_only=False, filt=False)初始化程序，进行自定义设置
       user_dict           设置用户词典，用户词典中的词会被打上uw标签。词典中每一个词一行，UTF8编码
       T2S                 默认False, 是否将句子从繁体转化为简体
       seg_only            默认False, 时候只进行分词，不进行词性标注
       filt                默认False, 是否使用过滤器去除一些没有意义的词语，例如“可以”。
       model_path          设置模型文件所在文件夹，默认为models/
       '''
        #print(text)

if __name__ == '__main__':
    js = {
        "id":1,
        "NLPstring":"中医科、肾内科3月份药占比"
    }
    #s = "6月份门诊量最高的科室"
    SelectForFMS.fenci(SelectForFMS,js)
