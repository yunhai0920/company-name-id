# ChineseNameAddress_OCR
Photographing Chinese-Name-Address implemented using CTPN+CTC+Address Correction.   

## Method 
Text Detection : CTPN (https://arxiv.org/pdf/1609.03605.pdf)  
Text Recognition: CTC+DenseNet（https://github.com/YCG09/chinese_ocr)
Address Judgment: Light GBM or textgrocery (https://github.com/2shou/TextGrocery)  
Address Correction: Fuzzy matching based on address library   
## About Code
demo_final.py  
You can simpely use demo_final.py for inference. Input a picture and output the Chinese address string.   
run_flask.py  
Communicate between server and wechat program using flask
ocr_whole.py  
Text detection using CTPN, then text recognition using Densenet  
stupid_addrs_rev.py  
Address correction using fuzyy-matching based on address library  
