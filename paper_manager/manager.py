# coding=utf-8
# @author=cer

from __future__ import print_function
import os
from paper_manager.color import Colored, colors
from paper_manager.repository import Repository
import pickle as pkl
import sqlite3
from datetime import date
import sys
from functools import reduce
import json
from six.moves import input


class Manager:
    def __init__(self, color):
        self.db_path = "paper_manager.db"
        self.user_config_path = "user_config.json"
        self.paper_item_list = ['paper_name', 'importance',
                                'urgency', 'tags', 'path',
                                'read', 'date', 'id']
        self.color = color
        self.user_config = self.get_user_config()
        self.conn = sqlite3.connect(self.db_path)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()
        # get repository and path
        self.select_repository()

    def get_user_config(self):
        if os.path.exists(self.user_config_path):
            with open(self.user_config_path) as f:
                user_config = json.load(f)
        else:
            user_config = {}
        return user_config

    def select_repository(self):
        rep_dict = self.user_config.get("all_repositories", {})
        is_new = False
        while True:
            if len(list(rep_dict.keys())) != 0:
                print("Choose one of the repositories below or add a new repository. "
                      "(first repository as default, if a new repository is needed, input a new name)")
                for one_rep in rep_dict:
                    print(one_rep, " : ", rep_dict[one_rep][0], " type: ", rep_dict[one_rep][1])
            else:
                print(self.color.red("No repository in your system now, please input a new name"))
            rep_name = input().strip()
            if rep_name == "":
                if len(list(rep_dict.keys())) != 0:
                    rep_name = list(rep_dict.keys())[0]
                else:
                    print(self.color.red("Please input a repository name !"))
            if rep_name in rep_dict:
                self.user_config["all_repositories"] = rep_dict
                rep_path, support_suffix = rep_dict[rep_name]
                break
            else:
                print("It's a new repository name, input the path of this repository."
                      "(current dir as default, re-input repository name input 'back')")
                rep_path = input().strip()
                if rep_path.strip() == "back":
                    continue
                if rep_path == "":
                    rep_path = "."
                print("Input support suffix of this repository, seperate by space, lisk("
                      "pdf mobi). (pdf as default, re-input repository name input 'back')")
                support_suffix = input().strip()
                if support_suffix.strip() == "back":
                    continue
                if support_suffix == "":
                    support_suffix = "pdf"
                is_new = True
                rep_path = os.path.abspath(rep_path)
                support_suffix = support_suffix.split()
                rep_dict[rep_name] = [rep_path, support_suffix]
                self.user_config["all_repositories"] = rep_dict
                break
        self.cur_rep = Repository(rep_name, rep_path, support_suffix)
        if is_new:
            self.create_a_new_table_for_repository(rep_name)
            self.refresh()

    def create_a_new_table_for_repository(self, rep_name):
        # use sqlite
        # create the table if not exist, table name is same as repository name
        sql_create = 'create table if not exists {}' \
                     ' ( paper_name varchar(100) , ' \
                     'importance integer, urgency integer, ' \
                     'tags varchar(100), path varchar(100), ' \
                     'read varchar(10), date TEXT, ' \
                     'id integer primary key autoincrement)'.format(rep_name)
        self.cursor.execute(sql_create)

    def delete_repository(self):
        rep_dict = self.user_config.get("all_repositories", {})
        while True:
            if len(list(rep_dict.keys())) != 0:
                print("Choose one of the repositories below to delete. (give up input 'back')")
                for one_rep in rep_dict:
                    print(one_rep, " : ", rep_dict[one_rep])
            else:
                print(self.color.red("No repository in your system now!"))
                return
            rep_name = input().strip()
            if rep_name in rep_dict:
                print(self.color.red("confirm to delete repository {}? (y or n)".format(rep_name)))
                confirm = input().strip()
                if confirm == "y" or confirm == "":
                    del rep_dict[rep_name]
                    self.user_config["all_repositories"] = rep_dict
                    sql_drop = 'drop table {}'.format(rep_name)
                    self.cursor.execute(sql_drop)
                    if rep_name == self.cur_rep.name:
                        self.select_repository()
                    print(self.color.red("repository: {} deleted!"))
                    return
                else:
                    continue
            elif rep_name.strip() == "back":
                return
            else:
                print("It's a new repository name, re-input again!")
                continue

    def refresh(self):
        self.cur_paper_names = {}
        self.traverse_papers(self.cur_rep.path)
        # print papers_name_now
        old_papers = self.cursor.execute("SELECT * FROM  {}".format(self.cur_rep.name)).fetchall()
        for old_paper in old_papers:
            old_name = old_paper[self.paper_item_list.index('paper_name')]
            old_path = old_paper[self.paper_item_list.index('path')]
            # delete the paper info that was already been deleted in os
            if old_name not in self.cur_paper_names.keys():
                self.del_by_names([old_name])
            # if the paper was moved, update the paper path info
            elif old_path != self.cur_paper_names[old_name]:
                self.cursor.execute("UPDATE {} SET path = ? WHERE paper_name = ?".format(self.cur_rep.name)
                                    , (self.cur_paper_names[old_name], old_name))
        old_paper_names = self.cursor.execute("SELECT paper_name FROM  {}".format(self.cur_rep.name)).fetchall()
        old_paper_names = [rec[0] for rec in old_paper_names]
        for now_paper in self.cur_paper_names.keys():
            # find a new paper, put in infos
            if now_paper not in old_paper_names:
                print(self.color.cyan("Find a new paper: {}".format(now_paper)))
                paper_im, paper_ug, paper_tags, read = self.get_on_paper_info_from_user()
                self.insert_one(now_paper, paper_im, paper_ug, paper_tags, read)

    def del_by_names(self, names):
        for name in names:
            self.cursor.execute("DELETE FROM {} WHERE paper_name = ?".format(self.cur_rep.name), (name,))
        self.conn.commit()

    def insert_one(self, paper_name, paper_im, paper_ug, paper_tags, read):
        self.cursor.execute("INSERT INTO {} (paper_name, importance, urgency, tags, path, read, date) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?)".format(self.cur_rep.name), (paper_name, paper_im,
                                                                                       paper_ug, paper_tags,
                                                                                       self.cur_paper_names[paper_name],
                                                                                       read, str(date.today())))
        self.conn.commit()

    def update_one(self, paper_name, paper_im, paper_ug, paper_tags, read):
        self.cursor.execute("UPDATE {} SET importance=?, urgency=?, "
                            "tags=?, path=?, read=?, date=? WHERE paper_name=?".format(self.cur_rep.name),
                            (paper_im, paper_ug, paper_tags, self.cur_paper_names[paper_name],
                             read, str(date.today()), paper_name))
        self.conn.commit()

    def print_papers(self, recs):
        from terminaltables import DoubleTable
        recs_head = ['id', 'paper_name',
                     'importance', 'urgency', 'tags',
                     'read', 'date']
        recs_t = [self.prettify_one(rec) for rec in recs]
        recs_t.insert(0, recs_head)
        table = DoubleTable(recs_t)
        print(table.table)

    def prettify_one(self, rec):
        one_row = [self.color.blue_yellow(str(rec[7])),
                   self.color.cyan(rec[0]),
                   self.color.magenta(str(rec[1])),
                   self.color.red(str(rec[2])),
                   self.color.blue(rec[3]),
                   self.color.yellow(str(rec[5])),
                   self.color.green(rec[6])]
        one_row = [item for item in one_row]
        return one_row

    def traverse_papers(self, fa_path):
        """pre-ordered depth-first search for every paper ends with 'supported suffix """
        paths = os.listdir(fa_path)
        for path in paths:
            if os.path.isdir(os.path.join(fa_path, path)):
                self.traverse_papers(os.path.join(fa_path, path))
            else:
                for one_suffix in self.cur_rep.support_suffix:
                    if path.endswith(one_suffix):
                        self.cur_paper_names[path] = os.path.join(fa_path, path)

    def recommend_papers(self):
        """select papers i can read for the sake of importance and urgency"""
        rec_papers = self.cursor.execute(
            "SELECT * FROM {} WHERE importance!='' AND urgency!='' AND read='n' ORDER BY urgency DESC , importance DESC LIMIT 5 ".format(
                self.cur_rep.name)).fetchall()
        if len(rec_papers) > 0:
            self.print_papers(rec_papers)

    def show_tags(self):
        """show all tags of my papers"""
        tags = self.cursor.execute("SELECT tags FROM {}".format(self.cur_rep.name)).fetchall()
        tags = [tag[0] for tag in tags]
        tag_set = set()
        for line in tags:
            for tag in line.strip().split(' '):
                if tag.strip() != '':
                    tag_set.add(tag)
        tag_s = 'All Tags: \n'
        for i, tag in enumerate(tag_set):
            tag_s += self.color.paint(colors[i % len(colors)], tag) + ' '
        print(tag_s)

    def query_by_tags(self, tags_s):
        """search papers by tags"""
        sets = []
        tags = tags_s.strip().split(' ')
        if len(tags) > 0:
            for tag in tags:
                recs = self.cursor.execute(
                    "select * from {} where tags like '%{}%'".format(self.cur_rep.name, tag)).fetchall()
                if len(recs) > 0:
                    res_set = set()
                    for rec in recs:
                        res_set.add(rec)
                    sets.append(res_set)
        results = reduce(lambda x, y: x & y, sets)
        if len(results) > 0:
            self.print_papers(results)
        else:
            print(self.color.red("find nothing !"))

    def print_path_by_nums(self, num_s):
        results = self.query_path_by_nums(num_s)
        if len(results) > 0:
            for res in results:
                print(res)
        else:
            print(self.color.red("find nothing !"))

    def query_path_by_nums(self, num_s):
        results = []
        nums = num_s.strip().split(' ')
        if len(nums) > 0:
            for num in nums:
                recs = self.cursor.execute("SELECT * FROM {} WHERE id=? ".format(self.cur_rep.name), (num,)).fetchall()
                if len(recs) > 0:
                    for rec in recs:
                        results.append(rec[4])
        return results

    def open_paper_by_num(self, num_s):
        results = self.query_path_by_nums(num_s)
        if len(results) == 0:
            print(self.color.red("find nothing !"))
        elif len(results) > 1:
            print(self.color.red("too much nums, please input one id num !"))
        else:
            # open paper by system default software, only support linux platform now
            if sys.platform.startswith('linux'):
                file_path = '\\'.join(results[0])
                # print file_path
                os.system("xdg-open {} > log.txt 2>&1 &".format(file_path))
            else:
                print(self.color.red("open file only support linux platform now !"))

    def query_by_nums(self, num_s):
        """search papers by id nums"""
        results = []
        nums = num_s.strip().split(' ')
        if len(nums) > 0:
            for num in nums:
                recs = self.cursor.execute("SELECT * FROM {} WHERE id=? ".format(self.cur_rep.name), (num,)).fetchall()
                if len(recs) > 0:
                    for rec in recs:
                        results.append(rec)
        if len(results) > 0:
            self.print_papers(results)
        else:
            print(self.color.red("find nothing !"))

    def query_by_id(self, id_num):
        papers = self.cursor.execute("SELECT * FROM {} WHERE id=?".format(self.cur_rep.name), (id_num,)).fetchall()
        if len(papers) == 1:
            print(self.color.cyan("find the paper:"))
            self.print_papers(papers)
        return papers

    def edit_one_paper(self, id_num):
        papers = self.query_by_id(id_num)
        if len(papers) > 0:
            paper_im, paper_ug, paper_tags, read = self.get_on_paper_info_from_user()
            # if user only press enter,  save the old value
            if paper_im == '':
                paper_im = papers[0][1]
            if paper_ug == '':
                paper_ug = papers[0][2]
            if paper_tags == '':
                paper_tags = papers[0][3]
            if read == '':
                read = papers[0][5]
            self.update_one(papers[0][0], paper_im, paper_ug, paper_tags, read)
        else:
            print(self.color.red("paper id num equals {} dose not exist!".format(id_num)))

    def get_on_paper_info_from_user(self):
        paper_importance = input(self.color.red("Please input the importance of this "
                                                "paper (from 1 to 5, 3 as default):")).strip()
        if paper_importance == "":
            paper_importance = "3"
        paper_urgency = input(self.color.yellow("Please input the urgency of this "
                                                "paper (from 1 to 5, 3 as default):")).strip()
        if paper_urgency == "":
            paper_urgency = "3"
        paper_tags = input(self.color.blue("Please input the tags of this paper"
                                           " (split by space):")).strip()
        read = input(self.color.magenta("Is this paper has been read?"
                                        " (y/n, n as default): ")).strip()
        if read == "":
            read = "n"
        print()
        return paper_importance, paper_urgency, paper_tags, read

    def quit_manager(self):
        # save user data
        with open(self.user_config_path, 'w') as f:
            json.dump(self.user_config, f)
        # close the sqlite db
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
