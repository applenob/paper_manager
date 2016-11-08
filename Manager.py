# coding=utf-8
import os
from Paper import Paper
from Color import Colored
import cPickle as Pkl

color = Colored()
pkl_name = "user_set.pkl"

def init():
    global paper_path
    global user_data
    if not os.path.exists(pkl_name):
        paper_path = raw_input('input path of your papers: ')
        if paper_path == '':
            paper_path = '/home/cer/文档/nlp'
        user_data = {'paper_path': paper_path}
    else:
        pkl_file = file(pkl_name, 'rb')
        user_data = Pkl.load(pkl_file)
        paper_path = user_data['paper_path']
        if 'papers' not in user_data.keys():
            user_data['papers'] = {}


def refresh():
    global papers_name_now
    papers_name_now = {}
    traverse_papers(paper_path)
    # print papers_name_now
    for old_paper in user_data['papers']:
        # delete the paper info that was already been deleted in os
        if old_paper not in papers_name_now.keys():
            del user_data['papers'][old_paper]
        # if the paper was moved, update the paper path info
        elif old_paper.path != papers_name_now['paper']:
            user_data['papers'][old_paper]["path"] = papers_name_now['paper']
    for now_paper in papers_name_now:
        # find a new paper, put in infos
        if now_paper not in user_data['papers'].keys():
            print color.green("Find a new paper: {}".format(now_paper))
            paper_im = raw_input("Please input the importance of this "
                                  "paper (from 1 to 5):")
            paper_ug = raw_input("Please input the urgency of this "
                                 "paper (from 1 to 5):")
            paper_tags = raw_input("Please input the tags of this paper"
                                   " (split by space):")
            new_paper = Paper(paper_im, paper_ug, paper_tags, now_paper, papers_name_now[now_paper])
            user_data['papers'][now_paper] = new_paper


def print_papers():
    pass


def traverse_papers(fa_path):
    # pre-ordered depth-first search for every paper ends with '.pdf'
    paths = os.listdir(fa_path)
    for path in paths:
        if os.path.isdir(os.path.join(fa_path, path)):
            traverse_papers(os.path.join(fa_path, path))
        else:
            papers_name_now[path] = os.path.join(fa_path, path)


def quit_manager():
    pkl_file = file(pkl_name, 'wb')
    Pkl.dump(user_data, pkl_file)

if __name__ == '__main__':
    init()
    refresh()
    quit_manager()
