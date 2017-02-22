#!/usr/bin/env python2
# coding=utf-8
import sqlite3
def _wrap_value(value):
    return repr(value)

def _wrap_values(values):
    return list(map(_wrap_value, values))

def _wrap_fields(fields):
    for key,value in fields.items():
        fields[key] = _wrap_value(value)
    return fields

def _concat_keys(keys):
    return "[" + "],[".join(keys) + "]"

def _concat_values(values):
    return ",".join(values)

def _concat_fields(fields, operator = (None, ",")):
    if operator:
        unit_operator, group_operator = operator
    # fields = _wrap_fields(fields)
    compiled = []
    for key,value in fields.items():
        compiled.append("[" + key + "]")
        if unit_operator:
            compiled.append(unit_operator)
            compiled.append(value)
        compiled.append(group_operator)
    compiled.pop() # pop last group_operator
    return " ".join(compiled)

class DataCondition(object):
    """
        �������ڲ���SQL�������������������䲿��

        ����:
        DataCondition(("=", "AND"), id = 26)
        DataCondition(("=", "AND"), True, id = 26)
    """

    def __init__(self, operator = ("=", "AND"), ingroup = True, **kwargs):
        """
            ���췽��
            ����:
                operator ����������Ϊ(���ʽ������, ���������)
                ingroup  �Ƿ���飬������飬�������Ű���
                kwargs   ��ֵԪ�飬�������ݿ��������Լ�ֵ
                         ע������ĵ��ںŲ�����ʵ������SQL������
                         ʵ�ʷ�������operator[0]���Ƶ�
            ����:
            DataCondition(("=", "AND"), id = 26)
            (id=26)
            DataCondition((">", "OR"), id = 26, age = 35)
            (id>26 OR age>35)
            DataCondition(("LIKE", "OR"), False, name = "John", company = "Google")
            name LIKE 'John' OR company LIKE "Google"
        """
        self.ingroup = ingroup
        self.fields = kwargs
        self.operator = operator

    def __unicode__(self):
        self.fields = _wrap_fields(self.fields)
        result = _concat_fields(self.fields, self.operator)
        if self.ingroup:
            return "(" + result + ")"
        return result

    def __str__(self):
        return self.__unicode__()

    def toString(self):
        return self.__unicode__()


class dataBaseHelper(object):
    def __init__(self,filename='./data/urldata.db'):
        """
            ���췽��
            ����: filename ΪSQLite3 ���ݿ��ļ���
        """
        self.file_name = filename
        
    def open(self):
        """
            �����ݿⲢ�����α�
        """
        self.connection = sqlite3.connect(self.file_name,check_same_thread = False)
        self.cursor = self.connection.cursor()
        
    def close(self):
        """
            �ر����ݿ⣬ע��������ʽ���ô˷�����
            ���౻����ʱҲ�᳢�Ե���
        """
        if hasattr(self, "connection") and self.connection:
            self.connection.close()
            
    def __del__(self):
        """
            ������������һЩ������
        """
        self.close()
    def commit(self):
        """
            �ύ����
            SELECT��䲻��Ҫ�˲�����Ĭ�ϵ�execute������
            commit_at_once��ΪTrue����ʽ���ô˷�����
            �������Ҫ��ʾ���ñ�������
        """
        self.connection.commit()
    def execute(self, sql = None, commit_at_once = True):
        """
            ִ��SQL���
            ����:
                sql  Ҫִ�е�SQL��䣬��ΪNone������ù��������ɵ�SQL��䡣
                commit_at_once �Ƿ������ύ��������������ύ��
                ���ڷǲ�ѯ����������Ҫ����commit��ʽ�ύ��
        """
        if not sql:
            sql = self.sql
        self.cursor.execute(sql)
        if commit_at_once:
            self.commit()

    def fetchone(self, sql = None):
        """
            ȡһ����¼
        """
        self.execute(sql, False)
        return self.cursor.fetchone()

    def fetchall(self, sql = None):
        """
            ȡ���м�¼
        """
        self.execute(sql, False)
        return self.cursor.fetchall()

    def __concat_keys(self, keys):
        return _concat_keys(keys)

    def __concat_values(self, values):
        return _concat_values(values)

    def table(self, *args):
        """
            ���ò�ѯ�ı���������ö��ŷָ�
        """
        self.tables = args
        self.tables_snippet = self.__concat_keys(self.tables)
        return self

    def __wrap_value(self, value):
        return _wrap_value(value)

    def __wrap_values(self, values):
        return _wrap_values(values)

    def __wrap_fields(self, fields):
        return _wrap_fields(fields)

    def __where(self):
        # self.condition_snippet
        if hasattr(self, "condition_snippet"):
            self.where_snippet = " WHERE " + self.condition_snippet

    def __select(self):
        template = "SELECT %(keys)s FROM %(tables)s"
        body_snippet_fields = {
            "tables" : self.tables_snippet,
            "keys" : self.__concat_keys(self.body_keys), 
        }
        self.sql = template % body_snippet_fields

    def __insert(self):
        template = "INSERT INTO %(tables)s (%(keys)s) VALUES (%(values)s)"
        body_snippet_fields = {
            "tables" : self.tables_snippet,
            "keys" : self.__concat_keys(list(self.body_fields.keys())),
            "values" : self.__concat_values(list(self.body_fields.values()))
        }
        self.sql = template % body_snippet_fields

    def __update(self):
        template = "UPDATE %(tables)s SET %(fields)s"
        body_snippet_fields = {
            "tables" : self.tables_snippet,
            "fields" : _concat_fields(self.body_fields, ("=",","))
        }
        self.sql = template % body_snippet_fields

    def __delete(self):
        template = "DELETE FROM %(tables)s"
        body_snippet_fields = {
            "tables" : self.tables_snippet
        }
        self.sql = template % body_snippet_fields

    def __build(self):
        {
            "SELECT": self.__select,
            "INSERT": self.__insert,
            "UPDATE": self.__update,
            "DELETE": self.__delete
        }[self.current_token]()

    def __unicode__(self):
        return self.sql

    def __str__(self):
        return self.__unicode__()

    def select(self, *args):
        self.current_token = "SELECT"
        self.body_keys = args
        self.__build()
        return self

    def insert(self, **kwargs):
        self.current_token = "INSERT"
        self.body_fields = self.__wrap_fields(kwargs)
        self.__build()
        return self

    def update(self, **kwargs):
        self.current_token = "UPDATE"
        self.body_fields = self.__wrap_fields(kwargs)
        self.__build()
        return self

    def delete(self, *conditions):
        self.current_token = "DELETE"
        self.__build()
        #if *conditions:
        self.where(*conditions)
        return self

    def where(self, *conditions):
        conditions = list(map(str, conditions))
        self.condition_snippet = " AND ".join(conditions)
        self.__where()
        if hasattr(self, "where_snippet"):
            self.sql += self.where_snippet
        return self
        
    