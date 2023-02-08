import os
import re
import random
import chardet
import hashlib
import sys
import json
from datetime import datetime

string = sys.argv[1]
string = string.replace("#", " ")
json_path = sys.argv[2]
json_path = json_path.replace("#", " ")
top_dir = string
ignore_file_list = ['RUIKit', 'R']
oc_obscure_file_type = [".pch", ".h", ".m", ".hpp", ".cpp", ".mm", ".cc", ".c", ".inl", ".frag", ".vert"]
# ignore_dir_list = ['.framework', '/Protobuf', '/AFNetworking', '/FMDB', '/Headers/Private', '/Headers/Public',
#                          '/React-Core', '/React']
ignore_dir_list = ['.framework', '/Protobuf', '/FMDB', '/Headers/Private', '/Headers/Public',
                         '/React-Core', '/React']
system_func_list = []
define_arg_list = []
define_arg_dic = {}
property_arg_list = []
global_arg_list = []
temp_w_define_list = []

dup_new_define_list = []
start_time = datetime.now()
dir_path = sys.path[0]
func_path = os.path.join(dir_path, "file/OC_Function.txt")
run_output_path = ''
if not run_output_path:
    temp_list_output = sys.argv[0].split('/')
    user_name = ''
    time = datetime.now().strftime('%m-%d %H时%M分')
    time = datetime.now().strftime('%m-%d')
    for i in range(0, len(temp_list_output)):
        value = temp_list_output[i]
        if value == 'Users':
            user_name = temp_list_output[i + 1]
            run_output_path = '/Users/%s/Desktop/%s_Output' % (user_name, time)

if not os.path.exists(run_output_path):
    os.mkdir(run_output_path)


obscure_class_dic_path2 = os.path.join(run_output_path, 'ObscureData.txt')
with open(func_path, encoding="utf-8", mode="r", errors="ignore") as file_object:
    system_func_list = file_object.readlines()
for v in system_func_list:
    index = system_func_list.index(v)
    if v.endswith('\n'):
        v = v.replace('\n', '')
    system_func_list[index] = v

def is_in_ignore_dir_list(match_string):
    for v in ignore_dir_list:
        if v in match_string:
            return True
    return False
# 扫描define里定义的变量
def beginSearchDefine():
    for dir_path, sub_paths, files in os.walk(top_dir, False):
        for s_file in files:
            # print("进入ConfuseFunAndPro:" + file_path)
            # if s_file == "sqlite3.c":
            #     continue
            file_path = os.path.join(dir_path, s_file)
            # # is_ignore = is_ignore_path(file_path)
            # # if is_ignore:
            # #     # print("遍历类名：跳过静态库对应的头文件")
            # #     print("1")
            # #     continue
            # if ".framework" in str(file_path):
            #     print("2")
            #     continue
            # file_name, file_type = os.path.splitext(s_file)
            # if file_name in ignore_file_list:
            #     print("3")
            #     continue
            # if file_type not in oc_obscure_file_type:
            #     print("4")
            #     continue
            print("ConfuseArgInFun正在处理...:" + file_path)
            f = open(file_path, 'rb')
            data = f.read()
            encode_type = chardet.detect(data)["encoding"]
            f.close()
            if s_file == 'AppDelegate+WiFi.m':
                encode_type = 'utf-8'
            if file_path.endswith(".h") is False:
                obscure_oc_funArg_name(file_path, encode_type)


def get_oc_define_string(match_string):
    match_string = str(match_string)
    # define 一共下标到6 一般第七位开始是空格
    start_index = 8
    if match_string[start_index] == " ":
        while match_string[start_index] == " ":
            start_index += 1

    end_index = start_index + 1
    while match_string[end_index] != " ":
        end_index += 1
    arg = match_string[start_index:end_index]
    print("define里的参数:", arg)
    return arg

def get_oc_property_string(match_string):
    match_string = str(match_string)
    # property最后一位为分号
    end_index = len(match_string)-1
    while match_string[end_index-1] == " ":
        end_index -= 1
    start_index = end_index - 1
    char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    while match_string[start_index] in char_list:
        start_index -= 1
    arg = match_string[start_index+1:end_index]
    print("property里的参数:", arg)
    return arg

def get_oc_global_string(match_string):
    match_string = str(match_string)
    # 全局变量定义最后一位为分号
    end_index = len(match_string)-1
    while match_string[end_index-1] == " ":
        end_index -= 1
    start_index = end_index - 1
    char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    while match_string[start_index] in char_list:
        start_index -= 1
    arg = match_string[start_index+1:end_index]
    print("global里的参数:", arg)
    return arg



def scanDefine():
    for dir_path, sub_paths, files in os.walk(top_dir, False):
        for s_file in files:
            # print("进入ConfuseFunAndPro:" + file_path)
            if s_file == "sqlite3.c":
                continue
            file_path = os.path.join(dir_path, s_file)
            # is_ignore = is_ignore_path(file_path)
            # if is_ignore:
            #     # print("遍历类名：跳过静态库对应的头文件")
            #     print("1")
            #     continue
            if ".framework" in str(file_path):
                print("2")
                continue
            file_name, file_type = os.path.splitext(s_file)
            if file_name in ignore_file_list:
                print("3")
                continue
            if file_type not in oc_obscure_file_type:
                print("4")
                continue
            f = open(file_path, 'rb')
            data = f.read()
            encode_type = chardet.detect(data)["encoding"]
            with open(file_path, mode='r', encoding=encode_type, errors='ignore') as file_object:
                file_content = file_object.readlines()
                for line_val in file_content:
                    define_pattern = re.compile(r'#define[\s]*[\w\(\)]+[\s]+.+')
                    define_match = define_pattern.match(line_val)
                    if define_match:
                        define_list = define_match.group()
                        define_match_string = str(define_list)
                        define_string = get_oc_define_string(define_match_string)
                        define_arg_list.append(define_string)

        print("有%d个define参数" % len(define_arg_list))

def scanPropertyName():
    for dir_path, sub_paths, files in os.walk(top_dir, False):
        for s_file in files:
            # print("进入ConfuseFunAndPro:" + file_path)
            if s_file == "sqlite3.c":
                continue
            file_path = os.path.join(dir_path, s_file)
            # is_ignore = is_ignore_path(file_path)
            # if is_ignore:
            #     # print("遍历类名：跳过静态库对应的头文件")
            #     print("1")
            #     continue
            if ".framework" in str(file_path):
                print("2")
                continue
            file_name, file_type = os.path.splitext(s_file)
            if file_name in ignore_file_list:
                print("3")
                continue
            if file_type not in oc_obscure_file_type:
                print("4")
                continue
            f = open(file_path, 'rb')
            data = f.read()
            encode_type = chardet.detect(data)["encoding"]
            with open(file_path, mode='r', encoding=encode_type, errors='ignore') as file_object:
                file_content = file_object.readlines()
                for line_val in file_content:
                    property_pattern = re.compile(r'[\s]*@property[\s]*([(].*[)]).*;')
                    property_match = property_pattern.match(line_val)
                    if property_match:
                        property_list = property_match.group()
                        property_match_string = str(property_list)
                        property_string = get_oc_property_string(property_match_string)
                        property_arg_list.append(property_string)

        print("有%d个property参数" % len(property_arg_list))

def scanGlobalName():
    for dir_path, sub_paths, files in os.walk(top_dir, False):
        for s_file in files:
            # print("进入ConfuseFunAndPro:" + file_path)
            if s_file == "sqlite3.c":
                continue
            file_path = os.path.join(dir_path, s_file)
            # is_ignore = is_ignore_path(file_path)
            # if is_ignore:
            #     # print("遍历类名：跳过静态库对应的头文件")
            #     print("1")
            #     continue
            if ".framework" in str(file_path):
                print("2")
                continue
            file_name, file_type = os.path.splitext(s_file)
            if file_name in ignore_file_list:
                print("3")
                continue
            if file_type not in oc_obscure_file_type:
                print("4")
                continue
            f = open(file_path, 'rb')
            data = f.read()
            encode_type = chardet.detect(data)["encoding"]
            with open(file_path, mode='r', encoding=encode_type, errors='ignore') as file_object:
                file_content = file_object.readlines()
                for line_val in file_content:
                    if line_val.startswith("static"):
                        global_pattern = re.compile(r'static.*;')
                        global_match = global_pattern.match(line_val)
                        if global_match:
                            global_list = global_match.group()
                            global_match_string = str(global_list)
                            global_string = get_oc_global_string(global_match_string)
                            global_arg_list.append(global_string)
                    else:
                        continue

        print("有%d个property参数" % len(global_arg_list))


def beginChangeArginFun():
    for dir_path, sub_paths, files in os.walk(top_dir, False):
        for s_file in files:
            # print("进入ConfuseFunAndPro:" + file_path)
            if s_file == "sqlite3.c":
                continue
            file_path = os.path.join(dir_path, s_file)
            if is_in_ignore_dir_list(dir_path):
                # print("过滤特殊文件夹，例如Pods、framework")
                continue
            # is_ignore = is_ignore_path(file_path)
            # if is_ignore:
            #     # print("遍历类名：跳过静态库对应的头文件")
            #     print("1")
            #     continue
            if ".framework" in str(file_path):
                print("2")
                continue
            file_name, file_type = os.path.splitext(s_file)
            if file_name in ignore_file_list:
                print("3")
                continue
            if file_type not in oc_obscure_file_type:
                print("4")
                continue
            print("ConfuseArgInFun正在处理...:" + file_path)
            f = open(file_path, 'rb')
            data = f.read()
            encode_type = chardet.detect(data)["encoding"]
            f.close()
            if s_file == 'AppDelegate+WiFi.m':
                encode_type = 'utf-8'
            if file_path.endswith(".h") is False:
                obscure_oc_funArg_name(file_path, encode_type)


def obscure_oc_funArg_name(file_path, encode_type):
    with open(json_path, encoding="utf-8", mode="r", errors="ignore") as file:
        system_json_class_dic = json.loads(file.read())
    for k, v in system_json_class_dic.items():
        if (k == 'classes'):
            print("classes")
            class_method = v

        if (k == 'words'):
            print("words")
            class_word = v
    class_method_len = len(class_method)
    class_word_len = len(class_word)
    end_path = file_path.split("/")
    end = end_path[-1]
    print("正在处理:", end, "中的方法内部参数")
    w_file_content = ''
    with open(file_path, mode='r', encoding=encode_type, errors='ignore') as file_object:
        w_file_content = file_object.read()
    # start_md5 = get_string_md5(w_file_content)
    random_class_string = ''
    old_v = ''
    is_change = False
    is_change = False

    def change(match_value):
        global is_change
        is_change = False
        line1 = str(match_value.group())
        print("line_in_change", line1)
        tuple_temp = match_value.span()
        j = 1
        if tuple_temp[0] - j < 0:
            char_pre = " "
        else:
            char_pre = line[tuple_temp[0] - j]
        if tuple_temp[1] <= len(line) - 1:
            char_suf = line[tuple_temp[1]]
        else:
            char_suf = " "

        print("char_pre", char_pre)
        print("char_suf", char_suf)
        char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
        # char_list1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/'
        if char_pre in char_list or char_suf in char_list:
            return line1
        if char_suf == ":":
            return line1
        if char_pre == ".":
            return line1
        print('方法参数名从: %s 改为 %s' % (old_v, random_class_string))
        return line1.replace(old_v, random_class_string)

    # for i, val in enumerate(ignore_set_list):
    #     print("startwithset", val)
    oc_func_arg_pattern = re.compile(
        r'(\-|\+)[\s]*([(][\s]*(.*)[\s]*[*]?[\s]*[)])[\s]*[A-Za-z_]+([\s]|.)*?({|;|\s)')
    split_w_file_content = w_file_content.split("\n")
    # 标识是否已在方法声明后
    arg_change_begin = False
    arg_fun_begin = False
    temp_arg_dic = {}
    temp_arg_fun_dic = {}
    fun_arg_list_duplicate = []
    for index, line in enumerate(split_w_file_content):
        print("第%d行:" % index + " 内容为:%s" % line)
        if oc_func_arg_pattern.match(line):
            print("进方法声明行1")
            # 把上一个方法的参数的dic和list清空 开始新的一个方法
            arg_change_begin = False
            arg_fun_begin = True
            temp_arg_dic = {}
            temp_arg_fun_dic = {}
            fun_arg_list_duplicate = []
            # 找到方法行
            # 有左花括号说明方法声明已结束 进入方法体
            if "{" in line:
                arg_change_begin = True
                arg_fun_begin = False
            if ":" not in line:
                # 这行没参数
                continue
            else:
                # 有参数 开始找
                begin_search_arg = 0
                # 遍历整行 找所有引号
                while begin_search_arg < len(line) and ":" in line[begin_search_arg:]:
                    if line[begin_search_arg] != ":":
                        begin_search_arg += 1
                    # 遇到引号 开始找后边第一个参数
                    else:
                        search_quo = begin_search_arg + 1
                        # 找第一个右括号 右括号右边就是参数
                        while line[search_quo] != ")" and search_quo < len(line) - 1:
                            search_quo += 1
                        # 找到之后 找结尾
                        search_quo_end = search_quo + 1
                        # 先规避(之后就是空格的状况

                        if line[search_quo_end] == " " and search_quo_end < len(line) - 1:
                            while line[search_quo_end] == " ":
                                search_quo_end += 1

                        search_quo_start = 0
                        if search_quo_end != search_quo + 1:
                            # 进过上面的循环
                            search_quo_start = search_quo_end

                        # line[search_quo_end]为第一位右括号后不为空格的字符
                        char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
                        while line[search_quo_end] in char_list and search_quo_end < len(line):
                            search_quo_end += 1
                            if search_quo_end == len(line):
                                break
                        if search_quo_start != 0:
                            # (后第一位为空格的不规范写法
                            if search_quo_end == len(line):
                                this_arg = line[search_quo_start:]
                            else:
                                this_arg = line[search_quo_start:search_quo_end]
                            print("可能存在的多行方法声明中的方法参数名:", this_arg)
                        else:
                            if search_quo_end == len(line):
                                this_arg = line[search_quo + 1:]
                            else:
                                this_arg = line[search_quo + 1:search_quo_end]
                            print("可能存在的多行方法声明中的方法参数名:", this_arg)
                            temp_arg_fun_dic[this_arg] = "True"
                        # 继续遍历下一个可能存在的引号
                        begin_search_arg += 1

        # 排除以{开头的行
        elif arg_fun_begin and arg_change_begin is False and oc_func_arg_pattern.match(
                line) is None and line.startswith("{") is False:
            print("进方法声明2")
            if ":" not in line:
                # 这行没参数
                continue
            else:
                # 有参数 开始找
                begin_search_arg = 0
                # 遍历整行 找所有引号
                while begin_search_arg < len(line) and ":" in line[begin_search_arg:]:
                    if line[begin_search_arg] != ":":
                        begin_search_arg += 1
                    # 遇到引号 开始找后边第一个参数
                    else:
                        search_quo = begin_search_arg + 1
                        # 找第一个右括号 右括号右边就是参数
                        while line[search_quo] != ")" and search_quo < len(line) - 1:
                            search_quo += 1
                        # 找到之后 找结尾
                        search_quo_end = search_quo + 1
                        # 先规避(之后就是空格的状况

                        if line[search_quo_end] == " " and search_quo_end < len(line) - 1:
                            while line[search_quo_end] == " ":
                                search_quo_end += 1

                        search_quo_start = 0
                        if search_quo_end != search_quo + 1:
                            # 进过上面的循环
                            search_quo_start = search_quo_end

                        # line[search_quo_end]为第一位右括号后不为空格的字符
                        char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
                        while line[search_quo_end] in char_list and search_quo_end < len(line):
                            search_quo_end += 1
                            if search_quo_end == len(line):
                                break
                        if search_quo_start != 0:
                            # (后第一位为空格的不规范写法
                            if search_quo_end == len(line):
                                this_arg = line[search_quo_start:]
                            else:
                                this_arg = line[search_quo_start:search_quo_end]
                            print("可能存在的多行方法声明中的方法参数名:", this_arg)
                        else:
                            if search_quo_end == len(line):
                                this_arg = line[search_quo + 1:]
                            else:
                                this_arg = line[search_quo + 1:search_quo_end]
                            print("可能存在的多行方法声明中的方法参数名:", this_arg)
                            temp_arg_fun_dic[this_arg] = "True"
                        # 继续遍历下一个可能存在的引号
                        begin_search_arg += 1
            # 虽然这行不匹配 但是上一个方法的参数扫描还没结束
            if "{" in line:
                arg_change_begin = True
                temp_arg_dic = {}
                fun_arg_list_duplicate = []
                temp_arg_fun_dic = {}

        # 有可能出现的以{开头的行且方法没扫描完 此时结束扫描方法声明,进入方法体替换
        elif line.startswith("{") and arg_change_begin is False:
            arg_change_begin = True
            print("进方法体参数替换3")

            # 开始扫描方法体中的参数
            if "=" not in line:
                print("扫描不到要替换的局部变量 跳过")
            elif "//" in line:
                print("注释行")
            else:
                # 一般一行只有一个局部变量声明
                arg_end = line.find("=")
                temp = arg_end
                if line[temp - 1] == " ":
                    while line[temp - 1] == " ":
                        temp -= 1
                arg_start = temp - 1
                can_add = True
                if line[arg_end + 1] == "=":
                    # == 号是判断 跳过扫描
                    print("出现的==")
                else:
                    # 往前找
                    char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
                    # 下划线有可能掉的全局变量
                    while arg_start >= 0:
                        if line[arg_start] == "_":
                            if arg_start == 0:
                                # 前面没有了 说明掉的全局变量 这种不添加
                                print("_开头的全局变量，跳过")
                                can_add = False
                                break
                            elif arg_start > 0 and line[arg_start] not in char_list:
                                print("_开头的全局变量，跳过")
                                can_add = False
                                break
                            else:
                                arg_start -= 1
                        elif line[arg_start] in char_list:
                            arg_start -= 1
                        elif line[arg_start] not in char_list:
                            if line[arg_start] == "\"":
                                # 是个静态字符串里边的
                                can_add = False
                            break
                    if can_add:
                        this_arg = line[arg_start + 1:temp + 1]
                        print("方法体内这行的局部变量:", this_arg)
                        if this_arg not in temp_arg_dic.keys() and this_arg != "self" and this_arg not in temp_arg_fun_dic.keys() \
                                and this_arg not in system_func_list and this_arg not in define_arg_list:
                            random_funarg_string = class_word[random.randint(0, class_word_len - 1)] + class_method[
                                random.randint(0, class_method_len - 1)]
                            if random_funarg_string not in fun_arg_list_duplicate:
                                print("111", this_arg)
                                temp_arg_dic[this_arg] = random_funarg_string
                            else:
                                while random_funarg_string in fun_arg_list_duplicate:
                                    random_funarg_string = class_word[random.randint(0, class_word_len - 1)] + \
                                                           class_method[
                                                               random.randint(0, class_method_len - 1)]

            if len(temp_arg_dic.keys()) < 1:
                continue
            for key, val in temp_arg_dic.items():
                if key in line:
                    random_class_string = val
                    old_v = key
                    com_string = r"%s" % old_v
                    t_list = re.sub(com_string, change, line)
                    line = ''.join(t_list)
                    split_w_file_content[index] = line

        # 方法声明已经扫描完毕 开始扫描方法体参数并替换
        # 正常情况下都走这个
        elif arg_change_begin and oc_func_arg_pattern.match(line) is None:
            arg_change_begin = True
            print("进方法体参数替换4")
            print("temp_arg_dic:", temp_arg_dic)
            # 没有赋予初始值的初始化
            oc_double_check_arg_pattern = re.compile(r'[\s]*[\w]+[\s]*[\w\*]+[\s]*;')
            # 开始扫描方法体中的参数
            if line.startswith("//"):
                print("注释行")
            elif "=" not in line:
                # 可能有未赋予初始值的初始化变量名
                if oc_double_check_arg_pattern.match(
                        line) is not None and "return" not in line and "continue" not in line:
                    can_add = True
                    arg_end = line.find(";")
                    temp = arg_end
                    if line[temp - 1] == " ":
                        while line[temp - 1] == " ":
                            temp -= 1
                    arg_start = temp - 1
                    print("line[arg_start00]:", line[arg_start])
                    # 往前找
                    char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
                    # 下划线有可能调的全局变量
                    while arg_start >= 0:
                        if line[arg_start] == "_":
                            if arg_start == 0:
                                # 前面没有了 说明调的全局变量 这种不添加
                                print("_开头的全局变量，跳过")
                                can_add = False
                                break
                            elif arg_start > 0 and line[arg_start] not in char_list:
                                print("_开头的全局变量，跳过")
                                can_add = False
                                break
                            else:
                                arg_start -= 1
                        elif line[arg_start] in char_list:
                            arg_start -= 1
                        elif line[arg_start] not in char_list:
                            if line[arg_start] == "\"":
                                # 是个静态字符串里边的
                                can_add = False
                            break
                    if can_add:
                        this_arg = line[arg_start + 1:temp]
                        print("这行的局部变量:", this_arg)
                        print("global_arg_list:",global_arg_list)
                        print("property_arg_list:",property_arg_list)
                        if this_arg not in temp_arg_dic.keys() and this_arg != "break" and len(
                                this_arg) > 0 and this_arg not in temp_arg_fun_dic.keys() and this_arg not in system_func_list \
                                and this_arg not in define_arg_list and this_arg not in property_arg_list and this_arg not in global_arg_list:
                            random_funarg_string = class_word[random.randint(0, class_word_len - 1)] + class_method[
                                random.randint(0, class_method_len - 1)]
                            if random_funarg_string not in fun_arg_list_duplicate:
                                print("000", this_arg)
                                temp_arg_dic[this_arg] = random_funarg_string
                            else:
                                while random_funarg_string in fun_arg_list_duplicate:
                                    random_funarg_string = class_word[random.randint(0, class_word_len - 1)] + \
                                                           class_method[
                                                               random.randint(0, class_method_len - 1)]
                print("扫描不到要替换的局部变量 跳过")
            else:
                # 一般一行只有一个局部变量声明
                arg_end = line.find("=")
                temp = arg_end
                can_add = True
                # if line[temp -1] !=" ":
                #     can_add = False
                if line[temp - 1] == " ":
                    while line[temp - 1] == " ":
                        temp -= 1
                arg_start = temp - 1
                print("line[arg_start]:", line[arg_start])
                if arg_end + 1 < len(line) and (line[arg_end + 1] == "=" or line[arg_end + 1] == "\""):
                    print("11")
                    # == 号是判断 跳过扫描
                    # ="是字符串 跳过
                    print("出现的==或=\"")
                elif line[arg_end - 1] == "!":
                    print("22")
                    # != 号也是判断 跳过扫描
                    print("出现!=")
                else:
                    # 往前找
                    print("33")
                    char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
                    # 下划线有可能掉的全局变量
                    while arg_start >= 0:
                        if line[arg_start] == "_":
                            if arg_start == 0:
                                # 前面没有了 说明调的全局变量 这种不添加
                                print("_开头的全局变量，跳过")
                                can_add = False
                                break
                            elif arg_start > 0 and line[arg_start] not in char_list:
                                print("_开头的全局变量，跳过")
                                can_add = False
                                break
                            else:
                                arg_start -= 1
                        elif line[arg_start] in char_list:
                            arg_start -= 1
                        elif line[arg_start] not in char_list:
                            if line[arg_start] == "\"":
                                # 是个静态字符串里边的
                                can_add = False
                            break
                    if can_add:
                        this_arg = line[arg_start + 1:temp]
                        print("这行的局部变量:", this_arg)
                        double_judge = ""
                        if this_arg.startswith("_"):
                            # 可能是调用全局变量
                            double_judge = this_arg[1:]
                        if double_judge in property_arg_list:
                            print("监测到调用全局property")
                        elif this_arg not in temp_arg_dic.keys() and this_arg != "self" and len(
                                this_arg) > 0 and this_arg not in temp_arg_fun_dic.keys() \
                                and this_arg not in system_func_list and this_arg not in define_arg_list and this_arg not in property_arg_list \
                                and this_arg not in global_arg_list:
                            random_funarg_string = class_word[random.randint(0, class_word_len - 1)] + class_method[
                                random.randint(0, class_method_len - 1)]
                            if random_funarg_string not in fun_arg_list_duplicate:
                                print("111", this_arg)
                                temp_arg_dic[this_arg] = random_funarg_string
                            else:
                                while random_funarg_string in fun_arg_list_duplicate:
                                    random_funarg_string = class_word[random.randint(0, class_word_len - 1)] + \
                                                           class_method[
                                                               random.randint(0, class_method_len - 1)]

            if len(temp_arg_dic.keys()) < 1:
                continue
            for key, val in temp_arg_dic.items():
                if key in line:
                    random_class_string = val
                    old_v = key
                    print("old_v", old_v)
                    print("val", val)
                    com_string = r"%s" % old_v
                    t_list = re.sub(com_string, change, line)
                    line = ''.join(t_list)
                    split_w_file_content[index] = line

    w_file_content = ""
    for index, line in enumerate(split_w_file_content):
        w_file_content += line + "\n"

    # end_md5 = get_string_md5(w_file_content)
    # if not start_md5 == end_md5:
    with open(file_path, mode='w', encoding=encode_type, errors='ignore') as file_object:
        file_object.write(w_file_content)

def changeDefine():
    for dir_path, sub_paths, files in os.walk(top_dir, False):
        for s_file in files:
            # print("进入ConfuseFunAndPro:" + file_path)
            if s_file == "sqlite3.c":
                continue
            file_path = os.path.join(dir_path, s_file)
            if is_in_ignore_dir_list(dir_path):
                # print("过滤特殊文件夹，例如Pods、framework")
                continue
            # is_ignore = is_ignore_path(file_path)
            # if is_ignore:
            #     # print("遍历类名：跳过静态库对应的头文件")
            #     print("1")
            #     continue
            if ".framework" in str(file_path):
                print("2")
                continue
            file_name, file_type = os.path.splitext(s_file)
            if file_name in ignore_file_list:
                print("3")
                continue
            if file_type not in oc_obscure_file_type:
                print("4")
                continue
            print("ConfuseArgInFun正在处理Define...:" + file_path)
            f = open(file_path, 'rb')
            data = f.read()
            encode_type = chardet.detect(data)["encoding"]
            f.close()
            if s_file == 'AppDelegate+WiFi.m':
                encode_type = 'utf-8'
            obscure_oc_define(file_path, encode_type)

def obscure_oc_define(file_path, encode_type):
    end_path = file_path.split("/")
    end = end_path[-1]
    print("正在处理:", end, "中的define参数")
    w_file_content = ''
    with open(file_path, mode='r', encoding=encode_type, errors='ignore') as file_object:
        w_file_content = file_object.read()
    random_class_string = ''
    old_v = ''
    is_change = False
    is_change = False

    def change(match_value):
        global is_change
        is_change = False
        line1 = str(match_value.group())
        print("line_in_change", line1)
        tuple_temp = match_value.span()
        j = 1
        char_pre = w_file_content[tuple_temp[0] - j]
        char_suf = w_file_content[tuple_temp[1]]

        print("char_pre", char_pre)
        print("char_suf", char_suf)
        char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
        # char_list1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/'
        if char_pre in char_list or char_suf in char_list:
            return line1
        if char_suf == ":":
            return line1
        if char_pre == ".":
            return line1
        print('define参数名从: %s 改为 %s' % (old_v, random_class_string))
        temp_w_define_list.append('%s:%s' % (old_v, random_class_string) + "\n")
        return line1.replace(old_v, random_class_string)

    for key, val in define_arg_dic.items():
        if key in w_file_content:
            print("key", key)
            print("value", val)
            random_class_string = val
            old_v = key
            com_string = r"%s" % old_v
            t_list = re.sub(com_string, change, w_file_content)
            w_file_content = ''.join(t_list)

    with open(file_path, mode='w', encoding=encode_type, errors='ignore') as file_object:
        file_object.write(w_file_content)


def set_define_dic():
    with open(json_path, encoding="utf-8", mode="r", errors="ignore") as file:
        system_json_class_dic = json.loads(file.read())
    for k, v in system_json_class_dic.items():
        if (k == 'words'):
            class_word = v
    class_word_len = len(class_word)
    for index, value in enumerate(define_arg_list):
        new_define_arg = class_word[random.randint(0, class_word_len-1)] + class_word[random.randint(0, class_word_len-1)]
        while new_define_arg in dup_new_define_list:
            new_define_arg = class_word[random.randint(0, class_word_len - 1)] + class_word[
                random.randint(0, class_word_len - 1)]
        dup_new_define_list.append(new_define_arg)
        define_arg_dic[value] = new_define_arg



scanDefine()
scanPropertyName()
scanGlobalName()
beginChangeArginFun()
set_define_dic()
changeDefine()

with open(obscure_class_dic_path2, encoding="utf-8", mode="a", errors="ignore") as file_object:
    file_object.write("\n\nDefine:{\n")
    file_object.write(''.join(temp_w_define_list))
    file_object.write("}\nDefine_end\n")

end_time1 = datetime.now()
print("define中定义的变量名包括:",define_arg_list)
print("脚本ConfuseArgInFun运行时间：%s" % str((end_time1 - start_time).seconds))

str = sys.path[0] + "/ReformFun.py" + " " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3]
os.system("python3 " + str)

if int(sys.argv[3])>0:
    str = sys.path[0] + "/ConfuseArgsAndAddTrash.py" + " " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3]
    os.system("python3 " + str)
else:
    print("不混淆 结束运行")