import os
import re
import sys
import io
import numpy as np



stringRegex = "<ENAMEX TYPE[^>]*>[^<]+</ENAMEX>"
nestStringRegex = "<ENAMEX TYPE[^>]*>([^<]*<ENAMEX TYPE[^>]*>([^<]*<ENAMEX TYPE[^>]*>([^<]*<ENAMEX TYPE[^>]*>[^<]+</ENAMEX>[^<]*|[^<]+)</ENAMEX>[^<]*|[^<]+)</ENAMEX>[^<]*)*</ENAMEX>"
list_ner = ['ADDRESS', 'DATETIME', 'DATETIME-DATE', 'DATETIME-DATERANGE',
            'DATETIME-DURATION', 'DATETIME-SET', 'DATETIME-TIME',
            'DATETIME-TIMERANGE', 'EMAIL', 'EVENT', 'EVENT-CUL',
            'EVENT-GAMESHOW', 'EVENT-NATURAL', 'EVENT-SPORT', 'IP',
            'LOCATION', 'LOCATION-GEO', 'LOCATION-GPE', 'LOCATION-STRUC',
            'MISCELLANEOUS', 'ORGANIZATION', 'ORGANIZATION-MED', 'ORGANIZATION-SPORTS',
            'ORGANIZATION-STOCK', 'PERSON', 'PERSONTYPE', 'PHONENUMBER', 'PRODUCT','PRODUCT-AWARD',
            'PRODUCT-COM', 'PRODUCT-LEGAL', 'QUANTITY', 'QUANTITY-AGE', 'QUANTITY-CUR',
            'QUANTITY-DIM', 'QUANTITY-NUM', 'QUANTITY-ORD', 'QUANTITY-PER', 'QUANTITY-TEM',
            'SKILL', 'URL']

def get_content(file_path):
    if not os.path.exists(file_path):
        print(file_path)
        sys.exit("An error occurred while opening the file")
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()
    return content
    pass

def get_original(content):
    return re.sub(r'<ENAMEX TYPE="[A-Z|\-]*">|</ENAMEX>', '', content).strip(" ").replace("  ", " ")
    pass

def findStringRegex(text, rule):
    matchList = dict()
    regex = re.compile(rule)
    # id = 0
    # while regex.search(text, id) is not None:
    #     regexMatcher = regex.search(text, id)
    #     # print(regexMatcher.group())
    #     matchList[regexMatcher.start()] = regexMatcher.group()
    #     id = regexMatcher.end() + 1
    # stop_event = Event()
    id = 0
    while id < len(text):
        regexMatcher = regex.search(text, id)
        if regexMatcher is not None:
            matchList[regexMatcher.start()] = regexMatcher.group()
            id = regexMatcher.end()
        else:
            id = len(text)
        # else:
            # id += 1
            # print("chưa chạy xong")
            # break

    # print(matchList)
    # print("dao")
    return matchList
    pass


def extractEntities(original_content, labeled_content):
    entities = dict()
    labeledEntities = findStringRegex(labeled_content, stringRegex)
    labeledNestedEntities = findStringRegex(labeled_content, nestStringRegex)

    nestedEntities = dict()

    # print("labeledEntities =",labeledEntities)
    # print("labeledNestedEntities =",labeledNestedEntities)
    index = 0
    for key in labeledNestedEntities.keys():
        entity = get_original(labeledNestedEntities.get(key))
        # print(entity)
        type = ""
        for e in list_ner:
            e_full = "<ENAMEX TYPE=\"" + e + "\">"
            if labeledNestedEntities.get(key).startswith(e_full):
                # print("e_full = ", e_full)
                type = e

        begin_entity = original_content.find(entity, index)
        end_entity = begin_entity + len(entity)
        index = end_entity
        # print(begin_entity)
        nestedEntities[str(begin_entity) + "_" + str(end_entity) + "_" + type + "_" + "outer"] = entity
        entities[str(begin_entity) + "_" + str(end_entity) + "_" + type + "_" + "outer"] = entity

    index = 0
    for key in labeledEntities.keys():
        entity = get_original(labeledEntities.get(key))

        type = ""
        for e in list_ner:
            e_full = "<ENAMEX TYPE=\"" + e + "\">"
            if labeledEntities.get(key).startswith(e_full):
                type = e
        begin_entity = original_content.find(entity, index)
        end_entity = begin_entity + len(entity)
        index = end_entity

        flag = False
        for props in nestedEntities.keys():
            props = props.split('_')
            if int(props[0]) <= begin_entity and int(props[1]) >= end_entity:
                entities[str(begin_entity) + "_" + str(end_entity) + "_" + type + "_" + "inner"] = entity
                flag = True
                break
        if not flag:
            entities[str(begin_entity) + "_" + str(end_entity) + "_" + type + "_" + "outer"] = entity
    # printEntity(entities)
    return entities
    pass


def printEntity(entities):
    for key, val in entities.items():
        print(val, key)
    pass

def print_table(table_scores, table_F_score):
    total_TP = 0
    total_TP_FP = 0
    total_TP_FN = 0
    header = ["NER", "TP", "TP+FP", "TP+FN", "P", "R", "F1"]

    print("%-20s%-10s%-10s%-10s%-10s%-10s%-10s" % (
        header[0], header[1], header[2], header[3], header[4], header[5], header[6]), file=log)

    for i in range(len(table_scores)):
        print("%-20s%-10d%-10d%-10d%-10.4f%-10.4f%-10.4f" % (
            list_ner[i], table_scores[i][0], table_scores[i][1], table_scores[i][2], table_F_score[i][0],
            table_F_score[i][1], table_F_score[i][2]), file=log)

        total_TP += table_scores[i][0]
        total_TP_FP += table_scores[i][1]
        total_TP_FN += table_scores[i][2]

    if total_TP_FP == 0:
        P = 0
    else:
        P = total_TP / total_TP_FP
    if total_TP_FP == 0:
        R = 0
    else:
        R = total_TP / total_TP_FN
    if P == R == 0:
        F = 0
    else:
        F = 2 * P * R / (P + R)

    print("%-20s%-10d%-10d%-10d%-10.4f%-10.4f%-10.4f" % ("--->Overall", total_TP, total_TP_FP, total_TP_FN, P, R, F), file=log)
    pass


def get_scores(table_scores):
    table_F_score = []
    for i in range(len(table_scores)):
        table_F_score.append([0.0, 0.0, 0.0])
    for i in range(len(table_scores)):
        # P:
        if table_scores[i][1] == 0:
            table_F_score[i][0] = 0
        else:
            table_F_score[i][0] = float(table_scores[i][0] / table_scores[i][1])
        # R:
        if table_scores[i][2] == 0:
            table_F_score[i][1] = 0
        else:
            table_F_score[i][1] = float(table_scores[i][0] / table_scores[i][2])
        # F:
        if table_F_score[i][0] != 0 and table_F_score[i][1] != 0:
            table_F_score[i][2] = 2 * table_F_score[i][0] * table_F_score[i][1] / (
                    table_F_score[i][0] + table_F_score[i][1])
    return table_F_score


def evaluate(path_test, path_anno, toplevel):
    if not os.path.exists(path_test):
        sys.exit("An error occurred while opening the folder test data")
    if not os.path.exists(path_anno):
        sys.exit("An error occurred while opening the the folder annotation data")

    total_scores = []
    for i in range(len(list_ner)):
        total_scores.append([0, 0, 0])

    subFolders = os.listdir(path_anno)
    for subFolder in subFolders:
        # print("-----------------------------", file=log)
        # print(subFolder, file=log)
        # print("-----------------------------", file=log)

        table_scores = []
        for i in range(len(list_ner)):
            table_scores.append([0, 0, 0])

        path_anno_subFolder = path_anno + "/" + subFolder
        list_anno_files = os.listdir(path_anno_subFolder)

        path_test_subFolder = path_test + "/" + subFolder
        list_test_files = os.listdir(path_test_subFolder)

        if len(list_anno_files) != len(list_test_files):
            sys.exit("The number of files in two folder is not equal.")
        else:
            for i in range(len(list_anno_files)):

                labeledFile = list_anno_files[i]
                # print(labeledFile)
                labeled_content = get_content(path_anno_subFolder + "/" + labeledFile)

                testFile = list_test_files[i]
                test_content = get_content(path_test_subFolder + "/" + testFile)

                original_content = get_original(labeled_content)

                if labeledFile != testFile:
                    sys.exit("The annotation file is not equal to test file")
                else:
                    # print("testEntities")
                    testEntities = extractEntities(original_content, test_content)
                    # print("annEntities")

                    annEntities = extractEntities(original_content, labeled_content)

                    # count TP+FP
                    for key in testEntities.keys():
                        key = key.split('_')
                        if toplevel:
                            if key[3] == "inner":
                                continue
                        for j in range(len(list_ner)):
                            if key[2] == list_ner[j]:
                                table_scores[j][1] += 1
                    # count TP+FN
                    for key in annEntities.keys():
                        key = key.split('_')
                        # print(key)
                        if toplevel:
                            if key[3] == "inner":
                                continue
                        for j in range(len(list_ner)):
                            if key[2] == list_ner[j]:
                                table_scores[j][2] += 1
                    # count TP
                    # print("TP:")
                    # print("annot:", annEntities.keys())
                    # print("test:", testEntities.keys())
                    for key1 in annEntities.keys():
                        key_1 = key1.split('_')
                        for key2 in testEntities.keys():
                            key_2 = key2.split('_')
                            if toplevel:
                                if key_2[3] == "inner":
                                    continue
                            for j in range(len(list_ner)):
                                if key_1[0] == key_2[0] and \
                                        key_1[1] == key_2[1] and \
                                        key_1[2] == key_2[2] and \
                                        key_1[3] == key_2[3] and \
                                        annEntities.get(key1) == testEntities.get(key2) and \
                                        key_1[2] == list_ner[j]:
                                    table_scores[j][0] += 1
                            # print(key_2)
        table_F_score = get_scores(table_scores)
        # print_table(table_scores, table_F_score)

        for i in range(len(total_scores)):
            for j in range(len(total_scores[i])):
                total_scores[i][j] += table_scores[i][j]
    # print("\n-----------------------------", file=log)
    # print("Total evaluation of test", file=log)
    # print("-----------------------------", file=log)
    # table_F_score = get_scores(total_scores)
    # print_table(total_scores, table_F_score)

    return total_scores
    pass


def print_overall_eval(top, nested):
    header = ["TP", "TP+FP", "TP+FN", "P", "R", "F1"]

    print("\n-----------------------------", file=log)
    print("Total evaluation of all tests", file=log)
    print("-----------------------------", file=log)
    print("=====================Top-level evaluation=====================", file=log)
    print("%-10s%-10s%-10s%-10s%-10s%-10s" % (header[0], header[1], header[2], header[3], header[4], header[5]), file=log)
    P = top[0] / top[1]
    R = top[0] / top[2]
    if P != 0 and R != 0:
        F1 = (2 * P * R) / (P + R)
        print("%-10d%-10d%-10d%-10.4f%-10.4f%-10.4f" % (top[0], top[1], top[2], P, R, F1), file=log)
    else:
        print("%-10d%-10d%-10d%-10.4f%-10.4f%-10.4f" % (top[0], top[1], top[2], P, R, 0), file=log)
    # print(top_level_score)
    print("\n=====================Nested evaluation=====================", file=log)
    print("%-10s%-10s%-10s%-10s%-10s%-10s" % (header[0], header[1], header[2], header[3], header[4], header[5]), file=log)
    P = nested[0] / nested[1]
    R = nested[0] / nested[2]
    if P != 0 and R != 0:
        F1 = (2 * P * R) / (P + R)
        print("%-10d%-10d%-10d%-10.4f%-10.4f%-10.4f" % (nested[0], nested[1], nested[2], P, R, F1), file=log)
    else:
        print("%-10d%-10d%-10d%-10.4f%-10.4f%-10.4f" % (nested[0], nested[1], nested[2], P, R, 0), file=log)
    # print(nested_score)
    print("\n-----------------------------", file=log)
    print("Overall evaluation", file=log)
    print("-----------------------------", file=log)
    print("%-10s%-10s%-10s%-10s%-10s%-10s" % (header[0], header[1], header[2], header[3], header[4], header[5]),
          file=log)
    TP_overall = top[0] + nested[0]
    TP_FP_overall = top[1] + nested[1]
    TP_FN_overall = top[2] + nested[2]

    P = TP_overall / TP_FP_overall
    R = TP_overall / TP_FN_overall
    if P != 0 and R != 0:
        F1 = (2 * P * R) / (P + R)
        print("%-10d%-10d%-10d%-10.4f%-10.4f%-10.4f" % (TP_overall, TP_FP_overall, TP_FN_overall, P, R, F1), file=log)
    else:
        print("%-10d%-10d%-10d%-10.4f%-10.4f%-10.4f" % (TP_overall, TP_FP_overall, TP_FN_overall, P, R, 0), file=log)
    return


if __name__ == '__main__':
    path = "E:\VLSP\Evaluate1\Tests"
    path_anno = "E:\VLSP\Evaluate1\Annot"
    path_out = "E:\VLSP\Evaluate1\Results _by_NE_types"
    list_NER_test = os.listdir(path)
    for test in list_NER_test:
        log = io.StringIO()
        path_test = os.path.join(path, test)
        list_tests = os.listdir(path_test)
        top_level_score = [0, 0, 0]
        nested_score = [0, 0, 0]
        overall = np.array(list_ner)
        overall = np.r_[overall, ["Overall"]]
        for i in range(len(list_tests)):
            # print("==>>>Test:", list_tests[i], file=log)
            print("==>>>Test:", list_tests[i])
            test_folder = path_test + "/" + list_tests[i]
            anno_folder = path_anno
            total_scores_top = evaluate(test_folder, anno_folder, toplevel=True)
            total_scores_nested = evaluate(test_folder, anno_folder, toplevel=False)
            top = np.array(total_scores_top)
            nested = np.array(total_scores_nested)
            total_scores = top + nested
            total_scores = np.r_[total_scores, [total_scores.sum(0)]]
            table_scores = list(total_scores)
            F_table_scores = np.array(get_scores(table_scores))
            overall = np.c_[overall, F_table_scores*100]

        for t in overall:
            t = list(t)
            # print(t[0], end="\t", file=log)
            for f in t[1:]:
                print("%-.2f" % (float(f)), end="\t", file=log)
            print(file=log)

        f_out = open(path_out+"/"+ test+".txt", "w", encoding="utf-8")
        text = log.getvalue().replace(".",",")
        print(text)
        f_out.write(text)
        log.close()