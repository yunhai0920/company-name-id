# -*- coding:utf-8 -*-
"""
@author:HuangJie
@time:18-11-6 上午10:33

"""
import os
import ocr_whole
import time
import sys
import numpy as np
from PIL import Image
from glob import glob
import Levenshtein
from tgrocery import Grocery
import pickle
import re
from tgrocery.classifier import *
from stupid_addrs_rev import stupid_revise
reload(sys)
sys.setdefaultencoding("utf-8")


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def demo_flask(image_file):
    grocery = Grocery('NameId_NLP')
    model_name = grocery.name
    text_converter = None
    if os.path.exists(model_name):
        tgm = GroceryTextModel(text_converter, model_name)
        tgm.load(model_name)
        grocery.model = tgm
        print('load!!!!!')
    else:
        name_file = open('pkl_data/company_name.pkl', 'rb')
        id_file = open('pkl_data/company_id.pkl', 'rb')
        other_file = open('pkl_data/others2.pkl', 'rb')
        name_list = pickle.load(name_file)
        id_list = pickle.load(id_file)
        other_list = pickle.load(other_file)
        name_file.close()
        id_file.close()
        other_file .close()
        grocery = Grocery('NameId_NLP')
        name_list.extend(id_list)
        name_list.extend(other_list)
        grocery.train(name_list)
        print (grocery.get_load_status())
        grocery.save()
        # print('train!!!!!!!!')
    addrline = [] 
    t = time.time()
    result_dir = './result'
    image = np.array(Image.open(image_file).convert('RGB'))
    result, image_framed = ocr_whole.model(image)
    output_file = os.path.join(result_dir, image_file.split('/')[-1])
    Image.fromarray(image_framed).save(output_file)
    ret_total = ''
    name_total = ''
    id_total = ''
    for key in result:
        string1 = result[key][1]
        # print("predict line text :", string1)
        string2 = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*{}[]+", "", string1)
        no_digit = len(list(filter(str.isdigit, string2.encode('gbk'))))
        no_alpha = len(list(filter(is_alphabet, string2)))
        if len(set('法定代表人') & set(string2)) >= 2 or '住所' in string2 or '资本' in string2 or '类型' in string2:
            predict_result = 'others'
        elif no_alpha > 5 or len(set('经营范围') & set(string2)) >= 2 or len(set('年月日') & set(string2)) >= 2 or len(set('登记机关') & set(string2)) >= 3 or '电话' in string2:
            predict_result = 'others'
        elif len(set('统一社会信用代码') & set(string2)) >= 2 or (no_digit / len(string2) > 0.7 and no_digit > 5):
            predict_result = 'company_id'
        else:
            predict_result = grocery.predict(string2)
        if str(predict_result) == 'company_name':
            string1 = string1.replace('《', '(')
            string1 = string1.replace('》', ')')
            string1 = string1.replace('(', '（')
            string1 = string1.replace(')', '）')
            string1 = string1.replace('（（', '（')
            if (not name_total) or len(string1) > len(name_total):
                name_total = ''
                name_total += string1
            else:
                name_total += string1
        elif str(predict_result) == 'company_id':
            string1 = string1.replace('!', '')
            string1 = string1.replace('[', '')
            string1 = string1.replace(']', '')
            if (not id_total) or len(string1) > len(id_total):
                id_total = ''
                id_total += string1
            else:
                id_total += string1
        else:
            continue
    
    if '）' in ret_total:
        if '（' not in ret_total:
            ret_total = ret_total.replace('C', '（')
    ret_total = re.sub(r'（(\w)住所(.*)', '', ret_total)
    ret_total = re.sub(r'（(\w)住房(.*)', '', ret_total)
    ret_total = re.sub(r'（不作为(.*)', '', ret_total)
    ret_total = re.sub(r'（有效期(.*)', '', ret_total)
    ret_total = re.sub(r'（仅限(.*)', '', ret_total)
    ret_total = re.sub(r'（临时经营(.*)', '', ret_total)
    ret_total = re.sub(r'（仅限办公(.*)', '', ret_total)
    ret_total = re.sub(r'（经营场所(.*)', '', ret_total)
    ret_total = re.sub(r"^[经]*[营]*[场/住]*[所]*", "", ret_total)
    ret_total = stupid_revise(ret_total)
    print("Mission complete, it took {:.3f}s".format(time.time() - t))
    print('\nRecongition Result:\n')
    print(ret_total)
    print(id_total)
    print(name_total)
    return output_file, ret_total, id_total, name_total


if __name__ == "__main__":
    demo_flask('./test_images/ID.jpg')