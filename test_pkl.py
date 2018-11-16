# -*- coding:utf-8 -*-
"""
@author:HuangJie
@time:18-11-6 上午10:33

"""
import xlrd
import cPickle as pickle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
"""
import cPickle as pickle
import json
with open('./pkl_data/address1.pkl', 'rb') as f:
    w = pickle.load(f)
pickle.dump(w, open('./pkl_data/address2.pkl', "wb"), protocol=2)
with open('./pkl_data/others1.pkl', 'rb') as f:
    w = pickle.load(f)
pickle.dump(w, open('./pkl_data/others2.pkl', "wb"), protocol=2)
with open('./pkl_data/address2.pkl', 'rb') as f:
    result = pickle.load(f)
    # R = str(result).replace('u\'', '\'')
    # t = R.decode("unicode-escape")
    t = json.dumps(result, encoding='utf-8', ensure_ascii=False)
    print(t)
    f.close()
with open('./converter3/class_map.config.pickle.pkl', 'rb') as f:
    w = pickle.load(f)
pickle.dump(w, open('./pkl_data/others2.pkl', "wb"), protocol=2)
"""


def read_pkl(pkl_file):
    with open(pkl_file, 'rb') as f:
        result = pickle.load(f)
        R = str(result).replace('u\'', '\'')
        t = R.decode("unicode-escape")
        print t


def strs(row):
    """
    :返回一列数据
    """
    try:
        txt_values = []
        for i in range(1, len(row)):
            if row[0] == u'统一信用代码':
                values = ('company-id', row[i])
            else:
                values = ('company-name', row[i])
            txt_values.append(values)
        return txt_values
    except:
        raise


def xls_txt(xls_name, txt_name):
    """
     :excel文件转换为txt文件
     :param xls_name excel 文件名称
     :param txt_name txt 文件名称
    """
    try:
        data = xlrd.open_workbook(xls_name)
        sqlfile = open(txt_name, "w+")
        table = data.sheets()[0]  # 表头
        ncols = table.ncols  # 行数
        # 如果不需跳过表头，则将下一行中1改为0
        for colnum in range(1, ncols):
            col = table.col_values(colnum)
            values = strs(col)  # 调用函数，将列数据拼接成字符串
            print values[0][0]
            if values[0][0] == u'company-id':
                with open('./company_and_id/company_id.pkl', 'wb') as f:
                    pickle.dump(values, f)
            else:
                with open('./company_and_id/company_name.pkl', 'wb') as f:
                    pickle.dump(values, f)
            rotation = str(values).replace('u\'', '\'')
            values = rotation.decode("unicode-escape")
            sqlfile.writelines(values)  # 将字符串写入新文件
            sqlfile.writelines("\n")
        sqlfile.close()  # 关闭写入的文件
        with open('./company_and_id/company_name.pkl', 'rb') as f:
            result = pickle.load(f)
            R = str(result).replace('u\'', '\'')
            t = R.decode("unicode-escape")
            print t
        with open('./company_and_id/company_id.pkl', 'rb') as f:
            result = pickle.load(f)
            R = str(result).replace('u\'', '\'')
            t = R.decode("unicode-escape")
            print t
    except:
        pass


def main():
    xls_name = './company_and_id/test.xls'
    txt_name = './company_and_id/test.txt'
    xls_txt(xls_name, txt_name)
    for index, line in enumerate(open('./company_and_id/test.txt', 'r')):
        with open('./company_and_id/line%d.txt' % index, 'w+') as tmp:
            tmp.write(line)


if __name__ == '__main__':
    pkl_file = './pkl_data/others2.pkl'
    read_pkl(pkl_file)

