#coding=utf-8
import json
import os
import glob
import string

import nltk

def addPunctuation(utterance):
    new = []
    for i in range(len(utterance)):
        start = ""
        for j in range(len(utterance[i])):
            if utterance[i][j] not in string.punctuation:
                start += utterance[i][j]
            else:
                new.append(start)
                new.append(utterance[i][j])
                start = ""
        if start != "":new.append(start)
    return new


def data_abstact(destpath, srcpath):
    for eachfile in glob.glob(os.path.join(destpath, '*')):
        try:
            item = json.load(open(eachfile, encoding='utf-8-sig'))
        except Exception as e:
            print(eachfile)
            print(e)
            exit(1000)
        raw_utterance = nltk.tokenize.word_tokenize(item['raw_utterance'])
        #raw_utterance = re.split('\s+',raw_utterance)

        #加入标点符号
        #raw_utterance = addPunctuation(raw_utterance)
        #raw_utterance

        tag_info = item['new_tag_utterance']
        mark = {}
        for i in range(len(tag_info)):
            tag = tag_info[i]['tags']  # 是一个list
            left = tag_info[i]['left_index']
            right = tag_info[i]['right_index']
            type = tag[0]['Type']
            if type == 'c' or type == 'v' or type == 'T' or type == 'D' or type == 'blank' or type == 'Excluding':
                #标记下
                mark[(left,right)] = type
                tag_info[i]['inter_utterance'] = type
            elif  type == 'N' and tag[0]['value'] == 'numberange':
                # 标记下
                mark[(left, right)] = type
                tag_info[i]['inter_utterance'] = type
            else:
                mark[(left,right)] = tag_info[i]['inter_utterance']

        i = 0
        raw_utterance_copy = []
        new_mark = {}
        while i < len(raw_utterance):
            flag = False
            for key,value in mark.items():
                if i >= key[0] and i <= key[-1]:
                    k = mark[key].split()
                    if len(k) == 1:
                        raw_utterance_copy.append(mark[key])
                        new_mark[key] = (len(raw_utterance_copy) - 1, len(raw_utterance_copy) - 1)
                    else:
                        # raw_utterance_copy.append("".join(k))
                        # new_mark[key] = (len(raw_utterance_copy) - 1, len(raw_utterance_copy) - 1)
                        new_mark[key] = (len(raw_utterance_copy), len(raw_utterance_copy) + len(k) - 1)
                        for k_index in range(len(k)):
                            raw_utterance_copy.append(k[k_index])


                    i = key[-1]+1
                    flag = True
            if flag == False:
                raw_utterance_copy.append(raw_utterance[i])
                i += 1
        #新加一个字段
        item['abstract_utterance'] = " ".join(raw_utterance_copy)

        #重写left right 索引
        for i in range(len(tag_info)):
            tag = tag_info[i]['tags']  # 是一个list
            left = tag_info[i]['left_index']
            right = tag_info[i]['right_index']
            for key,value in new_mark.items():
                if key == (left,right):
                    tag_info[i]['left_index'] = value[0]
                    tag_info[i]['right_index'] = value[1]

        #写入文件
        if not os.path.exists(srcpath): os.mkdir(srcpath)
        json.dump(item,open(os.path.join(srcpath,eachfile.split('\\')[-1]),'w'),indent=4)

data_abstact('D:\\Git\\AnnaTalkParser\\Data\\SharkAttackNew','shark_data_post_1')
