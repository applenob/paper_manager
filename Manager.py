# coding=utf-8
import os
from Paper import Paper
from Paper import paper_item_list
from Color import Colored
import cPickle as Pkl
import sqlite3
from datetime import date


color = Colored()
pkl_name = "user_set.pkl"

def init():
    global paper_path
    global user_set
    global conn
    global cursor
    # get path of papers
    if not os.path.exists(pkl_name):
        paper_path = raw_input('input path of your papers: ')
        if paper_path == '':
            paper_path = '/home/cer/文档/nlp'
        user_set = {'paper_path': paper_path}
    else:
        pkl_file = file(pkl_name, 'rb')
        user_set = Pkl.load(pkl_file)
        paper_path = user_set['paper_path']

    # use sqlite
    conn = sqlite3.connect('papers.db')
    conn.text_factory = str
    cursor = conn.cursor()
    sql_create = 'create table if not exists papers' \
                 + ' (paper_name varchar(20) primary key, ' \
                   'importance integer, urgency integer,' \
                   'tags varchar(100), path varchar(100), ' \
                   'read integer, date TEXT)'
    cursor.execute(sql_create)


def refresh():
    global papers_name_now
    papers_name_now = {}
    traverse_papers(paper_path)
    # print papers_name_now
    old_papers = cursor.execute("SELECT * FROM  papers").fetchall()
    for old_paper in old_papers:
        old_name = old_paper[paper_item_list.index('paper_name')]
        old_path = old_paper[paper_item_list.index('path')]
        # delete the paper info that was already been deleted in os
        if old_name not in papers_name_now.keys():
            del_by_names([old_name])
        # if the paper was moved, update the paper path info
        elif old_path != papers_name_now[old_name]:
            cursor.execute("UPDATE papers SET path = ? where paper_name = ?"
                           , (old_name, papers_name_now[old_name]))
    old_paper_names = cursor.execute("SELECT paper_name FROM  papers").fetchall()
    old_paper_names = [rec[0] for rec in old_paper_names]
    for now_paper in papers_name_now.keys():
        # find a new paper, put in infos
        if now_paper not in old_paper_names:
            print color.cyan("Find a new paper: {}".format(now_paper))
            paper_im = raw_input(color.red("Please input the importance of this "
                                           "paper (from 1 to 5):"))
            paper_ug = raw_input(color.yellow("Please input the urgency of this "
                                              "paper (from 1 to 5):"))
            paper_tags = raw_input(color.blue("Please input the tags of this paper"
                                              " (split by space):"))
            read = raw_input(color.magenta("Is this paper has been read?"
                                           " (y/n): "))
            print
            insert_one(now_paper, paper_im, paper_ug, paper_tags, read)


def del_by_names(names):
    for name in names:
        cursor.execute("DELETE FROM papers WHERE paper_name = ?", (name,))


def insert_one(paper_name, paper_im, paper_ug, paper_tags, read):
    cursor.execute("INSERT INTO papers (paper_name, importance, urgency, tags, path, read, date) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?)", (paper_name, paper_im,
                                                            paper_ug, paper_tags, papers_name_now[paper_name],
                                                            read, str(date.today())))
    conn.commit()


def print_papers(recs):
    from terminaltables import DoubleTable
    recs_head = ['paper_name', 'importance',
                   'urgency', 'tags',
                   'read', 'date']
    recs_t = [prettify_one(rec) for rec in recs]
    recs_t.insert(0, recs_head)
    table = DoubleTable(recs_t)
    print table.table


def prettify_one(rec):
    # one_row = [color.cyan("title: " + rec[0]),
    #            color.magenta(" importance: " + str(rec[1])),
    #            color.red(" urgency: " + str(rec[2])),
    #            color.blue(" tags: " + rec[3]),
    #            color.green(" path: " + rec[4]),
    #            color.yellow(" read: " + str(rec[5])),
    #            color.white(" date: " + rec[6])]
    one_row = [color.cyan(rec[0]),
               color.magenta(str(rec[1])),
               color.red(str(rec[2])),
               color.blue(rec[3]),
               color.yellow(str(rec[5])),
               color.green(rec[6])]
    one_row = [item.decode('utf-8') for item in one_row]
    return one_row


def traverse_papers(fa_path):
    """pre-ordered depth-first search for every paper ends with '.pdf' """
    paths = os.listdir(fa_path)
    for path in paths:
        if os.path.isdir(os.path.join(fa_path, path)):
            traverse_papers(os.path.join(fa_path, path))
        else:
            papers_name_now[path] = os.path.join(fa_path, path)


def recommend_papers():
    """select papers i can read for the sake of importance and urgency"""
    pass


def quit_manager():
    # save user data
    pkl_file = file(pkl_name, 'wb')
    Pkl.dump(user_set, pkl_file)
    # close the sqlite db
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init()
    refresh()
    recs = cursor.execute("SELECT * from papers ").fetchall()
    print_papers(recs)
    quit_manager()
