# -*- coding: utf-8 -*-
# file: test.py
# time: 2021/8/6
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

import random

from iomanager import IOManager

manager = IOManager.get_workspace()

obj1 = ['dsafa', 123]
obj2 = 7
obj3 = 'test'

obj_id1 = manager.save_object(obj1)
obj_id2 = manager.save_object(obj2)
obj_id3 = manager.save_object(obj3)

obj2 = [random.randint(1, 1000) for _ in range(10)]
obj_load1 = manager.load_object_by_id(obj_id1)
obj_load2 = manager.load_object_by_id(obj_id2)

manager.delete_object_by_id(obj_id1)
manager.delete_object_by_id(obj_id2)

# manager.destroy()




