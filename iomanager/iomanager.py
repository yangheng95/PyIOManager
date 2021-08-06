# -*- coding: utf-8 -*-
# file: iomanager.py
# time: 2021/8/6
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os
import pickle
import random
import shutil
import string

import win32api
import win32con


class IOManager:

    @staticmethod
    def get_workspace(workspace=None, reinit=True, visible=False):
        '''
        init IOManager from existing workspace
        :param workspace:
        :return:
        '''
        if not workspace:
            workspace = os.getcwd()

        if os.path.exists(os.path.join(workspace, 'IOManagerWorkspace')):
            workspace = os.path.join(workspace, 'IOManagerWorkspace')
        elif os.path.exists(os.path.join(workspace, '.IOManagerWorkspace')):
            workspace = os.path.join(workspace, '.IOManagerWorkspace')
        else:
            print('No workspace found at {}, init the workspace...'.format(workspace))

            return IOManager(workspace, visible)

        if os.path.exists(os.path.join(workspace, IOManager.__name__)):
            workspace = os.path.join(workspace, IOManager.__name__)

        config_path = os.path.join(workspace, 'config.pickle')
        return pickle.load(open(config_path, mode='rb'))

    def __init__(self, workspace: str = None, visible=False):
        '''

        :param workspace: workspace path to handle IO operations
        :param visible:
        '''
        self.workspace = workspace

        if not self.workspace:
            self.workspace = os.getcwd()

        self.workspace = os.path.join(self.workspace, 'IOManagerWorkspace')

        if not visible:
            dir_name, base_name = os.path.split(self.workspace)
            base_name = '.{}'.format(base_name)
            self.workspace = os.path.join(dir_name, base_name)

        self.id2file = {}
        self.file2id = {}
        if os.path.exists(self.workspace):
            shutil.rmtree(workspace)

        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)
        else:
            raise RuntimeError('IOManager workspace already exists, '
                               'you should use {}.from_existing_workspace("{}") to init IOManager'.format(__class__.__name__, workspace))

        if os.name == 'nt':
            win32api.SetFileAttributes(self.workspace, win32con.FILE_ATTRIBUTE_HIDDEN)

        self.update_trigger()

    def update_trigger(self):
        '''
        update IOManager config
        :param workspace:
        :return:
        '''
        config_path = os.path.join(self.workspace, 'config.pickle')
        return pickle.dump(self, open(config_path, mode='wb'))

    def load_object_by_id(self, obj_id):

        obj_file = self.id2file[obj_id]
        obj = pickle.load(open(obj_file, mode='rb'))

        return obj

    def save_object(self, obj):
        '''
        :param obj: object to save
        :return: obj_id
        '''

        obj_id = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        file_name = '{}.object'.format(obj_id)

        obj_file = os.path.join(self.workspace, file_name)

        self.id2file[obj_id] = obj_file
        self.file2id[obj_file] = obj_id

        pickle.dump(obj, open(obj_file, mode='wb'))

        self.update_trigger()

        return obj_id

    def delete_object_by_id(self, obj_id):
        '''
        :param obj_id:
        :return:
        '''
        obj_file = self.id2file[obj_id]

        try:
            os.remove(obj_file)
            self.id2file.pop(self.file2id[obj_file])
            self.file2id.pop(obj_file)
        except IOError as e:
            print('IOManager object deletion failed, error: {}'.format(e))

        self.update_trigger()

    def destroy(self):
        '''
        delete all the objects and destroy the workspace
        :return:
        '''
        try:
            shutil.rmtree(self.workspace)
            files = list(self.file2id.keys())
            for f in files:
                self.id2file.pop(self.file2id[f])
                self.file2id.pop(f)
        except IOError as e:
            print('IOManager workspace destroy failed, error: {}'.format(e))
