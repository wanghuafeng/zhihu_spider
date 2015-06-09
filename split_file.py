#coding:utf-8
__author__ = 'huafeng'
import sys
import os
def cut_file(filename, partial_count=1):
    with open(filename) as f:
        line_list = list(set(f.readlines()))#打乱顺序
        lenght_of_lines = len(line_list)
        print 'total line count: ', lenght_of_lines
        partial_file_line_count = lenght_of_lines/partial_count#共切割为partial_count文件
        for fileno in range(partial_count):
            partial_filename = filename + ".partial_%s"%(fileno + 1)#切割后的子文件由1开始编号
            if fileno == partial_count - 1:
                partial_line_list = line_list[partial_file_line_count*fileno:]#当文件行数不能被分为整数行时，将余数行写入到最后一个文件，也即：初最后一个文件外，其他文件都是partial_file_line_count行
                print 'line count of partial_%s is: '%(fileno + 1), len(partial_line_list)
            else:
                partial_line_list = line_list[partial_file_line_count*fileno:partial_file_line_count*(fileno+1)]
                print 'line count of partial_%s: '%(fileno + 1), partial_file_line_count
            with open(partial_filename, 'w') as wf:
                wf.writelines(partial_line_list)
USAGE = '''
-f, -F -filename    待切割文件
-c, -C, -count      切割数目，默认为1
'''

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 4:
        if args[0] in ('-f', '-F' '-filename'):
            filename = os.path.join(args[1])
            if not filename:
                print "%s not exists"%filename
                sys.exit()
            elif args[2] in ('-c', '-C', '-count'):
                try:
                    count = int(args[3])
                    cut_file(filename, count)
                except BaseException, e:
                    print e
                    sys.exit()
        else:
            print USAGE
            sys.exit()