# -*- coding:utf-8 -*-
import os
import numpy as np
from imp import reload
from PIL import Image, ImageOps
import io
from keras.layers import Input
from keras.models import Model
from keras.utils import multi_gpu_model
# import keras.backend as K

from . import keys
from . import densenet

reload(densenet)

char_file = '/home/hj/ZX_DL/DL_OCR/ChineseAddress_OCR-master/densenet/char_std_4944.txt'
characters = io.open(char_file, 'r', encoding='utf-8').readlines()
characters = characters[0].split()+['卍']
# characters = keys.alphabet[:]
# characters = characters[1:] + u'卍'
nclass = len(characters)
inputs = Input(shape=(32, None, 1), name='the_input')
y_pred = densenet.dense_cnn(inputs, nclass)
basemodel = Model(inputs=inputs, outputs=y_pred)
# model = multi_gpu_model(basemodel, 2)
# model.summary()
modelPath = os.path.join(os.getcwd(), 'densenet/models/weights_densenet1.h5')
if os.path.exists(modelPath):
    basemodel.load_weights(modelPath)
    # temp_x = np.zeros([1, 32, 32, 1])
    # temp_y = basemodel.predict(temp_x)


def decode(pred):
    char_list = []
    pred_text = pred.argmax(axis=2)[0]
    for i in range(len(pred_text)):
        if pred_text[i] != nclass - 1 and ((not (i > 0 and pred_text[i] == pred_text[i - 1])) or (i > 1 and pred_text[i] == pred_text[i - 2])):
            char_list.append(characters[pred_text[i]])
    return u''.join(char_list)


def predict(img):
    width, height = img.size[0], img.size[1]
    scale = height * 1.0 / 32
    width = int(width / scale)
    
    img = img.resize([width, 32], Image.ANTIALIAS)
   
    '''
    img_array = np.array(img.convert('1'))
    boundary_array = np.concatenate((img_array[0, :], img_array[:, width - 1], img_array[31, :], img_array[:, 0]), axis=0)
    if np.median(boundary_array) == 0:  # 将黑底白字转换为白底黑字
        img = ImageOps.invert(img)
    '''

    img = np.array(img).astype(np.float32) / 255.0 - 0.5
    
    x = img.reshape([1, 32, width, 1])
    y_pred = basemodel.predict(x)
    y_pred = y_pred[:, :, :]

    # out = K.get_value(K.ctc_decode(y_pred, input_length=np.ones(y_pred.shape[0]) * y_pred.shape[1])[0][0])[:, :]
    # out = u''.join([characters[x] for x in out[0]])
    out = decode(y_pred)

    return out
