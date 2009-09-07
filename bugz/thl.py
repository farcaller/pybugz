#!/usr/bin/env python

from appscript import *
from bugz.bugzilla import Bugz

class THLBugz(object):
    def __init__(self, bz):
        self.bz = bz
    
    def get_bugz_folder(self):
        return [f for f in app('The Hit List').folders_group.folders.get() if f.name() == 'Bugz'][0]
    
    def get_projects(self, bugfolder):
        return [(l.name(), l) for l in bugfolder.lists.get()]
    
    def get_buglist_for_project_bz(self, p):
        return bz.search('', product=p, status=['ASSIGNED','NEW'])
    
    def get_buglist_for_project_thl(self, p):
        if type(p) == str:
            pl = self.get_projects(self.get_bugz_folder())
            pr = None
            for pp in pl:
                print "proj ", pp
                if pp[0] == p:
                    pr = pp[1]
                    break
                print "next..."
        else:
            pr = p
        if not pr: return []
        return [self.thl_task_to_dict(tt) for tt in pr.tasks.get()]
    
    def thl_task_to_dict(self, tt):
        return {
            'bugid': tt.title()[:tt.title().find(':')],
            'desc': tt.title()[tt.title().find(':')+2:],
        }

if __name__ == '__main__':
    burl, blogin, bpwd = 'http://bugs.codeneedle.com/bugzilla/', open('/users/farcaller/.pybugz').readlines()
    bz = Bugz(burl, blogin, bpwd)