# coding=utf-8
import os
from Color import Colored
import cPickle as Pkl
import sqlite3
from datetime import date
import cmd


color = Colored()
pkl_name = "user_set.pkl"
paper_item_list = ['paper_name', 'importance',
                   'urgency', 'tags', 'path',
                   'read', 'date', 'id']

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
                  ' ( paper_name varchar(100) , ' \
                   'importance integer, urgency integer, ' \
                   'tags varchar(100), path varchar(100), ' \
                   'read varchar(10), date TEXT, ' \
                   'id integer primary key autoincrement)'
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
            paper_im, paper_ug, paper_tags, read = get_on_paper_info_from_user()
            insert_one(now_paper, paper_im, paper_ug, paper_tags, read)


def del_by_names(names):
    for name in names:
        cursor.execute("DELETE FROM papers WHERE paper_name = ?", (name,))
    conn.commit()


def insert_one(paper_name, paper_im, paper_ug, paper_tags, read):
    cursor.execute("INSERT INTO papers (paper_name, importance, urgency, tags, path, read, date) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?)", (paper_name, paper_im,
                                                            paper_ug, paper_tags, papers_name_now[paper_name],
                                                            read, str(date.today())))
    conn.commit()


def update_one(paper_name, paper_im, paper_ug, paper_tags, read):
    cursor.execute("UPDATE papers set importance=?, urgency=?, "
                   "tags=?, path=?, read=?, date=? where paper_name=?",
                   (paper_im, paper_ug, paper_tags, papers_name_now[paper_name],
                    read, str(date.today()), paper_name))
    conn.commit()


def print_papers(recs):
    from terminaltables import DoubleTable
    recs_head = ['id', 'paper_name',
                 'importance', 'urgency', 'tags',
                 'read', 'date']
    recs_t = [prettify_one(rec) for rec in recs]
    recs_t.insert(0, recs_head)
    table = DoubleTable(recs_t)
    print table.table


def prettify_one(rec):
    one_row = [color.blue_yellow(str(rec[7])),
               color.cyan(rec[0]),
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
    rec_papers = cursor.execute("SELECT * from papers where importance!='' and urgency!='' and read='n' ORDER BY urgency DESC , importance DESC LIMIT 5 ").fetchall()
    if len(rec_papers) > 0:
        print_papers(rec_papers)


def show_tags():
    """show all tags of my papers"""
    tags = cursor.execute("SELECT tags from papers").fetchall()
    tags = [tag[0] for tag in tags]
    tag_set = set()
    for line in tags:
        for tag in line.strip().split(' '):
            if tag.strip() != '':
                tag_set.add(tag)
    from Color import colors
    tag_s = 'All Tags: \n'
    for i, tag in enumerate(tag_set):
        tag_s += color.paint(colors[i % len(colors)], tag) + ' '
    print tag_s


def query_by_tags(tags_s):
    """search papers by tags"""
    sets = []
    tags = tags_s.strip().split(' ')
    if len(tags) > 0:
        for tag in tags:
            recs = cursor.execute("select * from papers where tags like '%{}%'".format(tag)).fetchall()
            if len(recs) > 0:
                res_set = set()
                for rec in recs:
                    res_set.add(rec)
                sets.append(res_set)
    results = reduce(lambda x, y: x & y, sets)
    if len(results) > 0:
        print_papers(results)
    else:
        print color.red("find nothing !")


def query_path_by_nums(num_s):
    results = []
    nums = num_s.strip().split(' ')
    if len(nums) > 0:
        for num in nums:
            recs = cursor.execute("select * from papers where id=? ", (num,)).fetchall()
            if len(recs) > 0:
                for rec in recs:
                    results.append(rec[4])
    if len(results) > 0:
        for res in results:
            print res
    else:
        print color.red("find nothing !")


def query_by_nums(num_s):
    """search papers by id nums"""
    results = []
    nums = num_s.strip().split(' ')
    if len(nums) > 0:
        for num in nums:
            recs = cursor.execute("select * from papers where id=? ", (num,)).fetchall()
            if len(recs) > 0:
                for rec in recs:
                    results.append(rec)
    if len(results) > 0:
        print_papers(results)
    else:
        print color.red("find nothing !")


def query_by_id(id_num):
    papers = cursor.execute("select * from papers where id=?", (id_num,)).fetchall()
    if len(papers) == 1:
        print color.cyan("find the paper:")
        print_papers(papers)
    return papers


def edit_one_paper(id_num):
    papers = query_by_id(id_num)
    if len(papers) > 0:
        paper_im, paper_ug, paper_tags, read = get_on_paper_info_from_user()
        # if user only press enter,  save the old value
        if paper_im == '':
            paper_im = papers[0][1]
        if paper_ug == '':
            paper_ug = papers[0][2]
        if paper_tags == '':
            paper_tags = papers[0][3]
        if read == '':
            paper_ug = papers[0][5]
        update_one(papers[0][0], paper_im, paper_ug, paper_tags, read)
    else:
        print color.red("paper id num equals {} dose not exist!".format(id_num))


def get_on_paper_info_from_user():
    paper_im = raw_input(color.red("Please input the importance of this "
                                   "paper (from 1 to 5):"))
    paper_ug = raw_input(color.yellow("Please input the urgency of this "
                                      "paper (from 1 to 5):"))
    paper_tags = raw_input(color.blue("Please input the tags of this paper"
                                      " (split by space):"))
    read = raw_input(color.magenta("Is this paper has been read?"
                                   " (y/n): "))
    print
    return paper_im, paper_ug, paper_tags, read


def quit_manager():
    # save user data
    pkl_file = file(pkl_name, 'wb')
    Pkl.dump(user_set, pkl_file)
    # close the sqlite db
    cursor.close()
    conn.commit()
    conn.close()


class MyCmd(cmd.Cmd):
    """my command processor"""

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(manager)>'
        self.intro = '''
Paper Manager Usage：
^---^ ^---^ ^---^ ^---^ ^---^
rec   recommend the papers according to urgency and importance
all   show all the papers info
tags  show all tags
sbt   search by tags, like (sbt tag1 tg2)
sbn   search by id nums, like (sbn 1 2)
edit  edit one paper info by paper id, like (edit 1)
path find path by paper id, like (path 1 2)
help  help info
quit  exit the manager
            '''

    def do_rec(self, arg):
        recommend_papers()

    def help_rec(self):
        print "recommend the papers according to urgency and importance"

    def do_all(self, arg):
        recs = cursor.execute("SELECT * from papers ").fetchall()
        print_papers(recs)

    def help_all(self):
        print "show all the papers info"

    def do_tags(self, arg):
        show_tags()

    def help_tags(self):
        print "show all tags"

    def do_sbt(self, arg):
        query_by_tags(arg)

    def help_sbt(self):
        print "search by tags, like (sbt tag1 tg2)"

    def do_sbn(self, arg):
        query_by_nums(arg)

    def help_sbn(self):
        print "search by id nums, like (sbn 1 2)"

    def do_edit(self, arg):
        edit_one_paper(arg)

    def help_edit(self):
        print "edit one paper info by paper id, like (edit 1),\n" \
              "use 'all' or 'tags' to see the id of your paper."

    def do_path(self, arg):
        query_path_by_nums(arg)

    def help_path(self):
        print "find path by paper id, like (path 1 2)"

    def do_quit(self, arg):
        print color.yellow("Bye ...")
        quit_manager()
        import sys
        sys.exit()

    def help_quit(self):
        print 'exit the manager'

if __name__ == '__main__':
    init()
    refresh()
    mycmd = MyCmd()
    mycmd.cmdloop()

