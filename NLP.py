'''
n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
v/动词 a/形容词 d/副词 h/前接成分 k/后接成分 i/习语
j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
e/叹词 o/拟声词 g/语素 w/标点 x/其它 uw/自定义
'''
# -*- coding: utf-8 -*-
import thulac
thu1 = thulac.thulac(user_dict='THUOCL_medical_1.txt')  #默认模式

'''
user_dict='C://UserDict//THUOCL_medical.txt'
thulac(user_dict=None, model_path=None, T2S=False, seg_only=False, filt=False)初始化程序，进行自定义设置
user_dict           设置用户词典，用户词典中的词会被打上uw标签。词典中每一个词一行，UTF8编码
T2S                 默认False, 是否将句子从繁体转化为简体
seg_only            默认False, 时候只进行分词，不进行词性标注
filt                默认False, 是否使用过滤器去除一些没有意义的词语，例如“可以”。
model_path          设置模型文件所在文件夹，默认为models/
'''

#text = thu1.cut("朔州中心医院最近三个月电子耳蜗植入术数量", text=True)  #进行一句话分词
text = thu1.cut("精神科本季度住院人数", text=True)
print(text)

'''
#某项指标在数据库里面没有
#缺省值：全院、近一年
'''