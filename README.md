# Paper Manager (Version 2)

##  1.Intro
A command-line manager programed in python, help with managing your local academic papers.
[Chinese blog address](http://www.jianshu.com/p/768db1472042)

It support both python2.7 and python3.6 now.
## 2.Usage

- 1.from code:

First, clone this repository to your computer.

Just run main.py:
 ```
 python main.py
 ```

Or you can install this as a system command:
```
python setup.py install
```

After installation, you can run command `paper_manager` anywhere in you terminator.

### detail

In version2, it support multiple repository now. You can use `paper_manager` to manage multiple directories of your system.

You can specifies a repository's supported suffix, like 'pdf', 'mobi', 'tex' or so on.

```

     select_rep select or create a repository to operate
     delete_rep delete a repository
     cur_rep    show current repository
     refresh    refresh a repository
     rec        recommend the papers according to urgency and importance
     all        show all the papers info
     tags       show all tags
     sbt        search by tags, like (sbt tag1 tg2)
     sbn        search by id nums, like (sbn 1 2)
     edit       edit one paper info by paper id, like (edit 1)
     path       find path by paper id, like (path 1 2)
     open       open paper to read by id, like (open 1)
     help       help info
     quit       exit the manager
```

## 3. Have fun!

```
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%      %%%%    %%%%%%%    %%
%%%%   %%%  %%%   %%%%%%   %%%
%%%%   %%%  .%%   -%%%% .  %%%
%%%%   %%%  %%% %  %%%.=.  %%%
%%%%      -%%%% %   %% %.  %%%
%%%%   %%%%%%%% %%  = %%.  %%%
%%%%   %%%%%%%% %%%  %%%.  %%%
%%%%   %%%%%%%% %%%  %%%   %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
```

## 4. Release Note

### version1
- Build a repository by a directory.
- Search a paper with tag.
- Search a paper with id num.
- Show all papers.
- Edit a paper info.
- Delete a paper info.
- Recommend papers.
- Open paper from manager by system default reader.

### version2
- Select from multiple repository.
- Delete a repository.
- Customize supported suffix for a repository.
