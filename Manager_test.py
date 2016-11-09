# coding=utf-8
import sqlite3
from datetime import date
import Manager
conn = sqlite3.connect('papers.db')
global cursor
cursor = conn.cursor()
sql_create = 'create table if not exists papers' \
             + ' (paper_name varchar(20) primary key, ' \
               'importance integer, urgency integer,' \
               'tags varchar(100), path varchar(100), ' \
               'read integer, date TEXT)'
cursor.execute(sql_create)
cursor.execute("INSERT INTO papers (paper_name, importance, urgency, tags, path, read, date) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?)", (" Calculus on Computational Graphs_ Backpropagation -- colah's blog.pdf",
               '3', '2', "nn bp basic blog", " Calculus on Computational Graphs_ Backpropagation -- colah's blog.pdf", 'n', str(date.today())))