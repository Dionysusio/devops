#!/usr/bin/python
#coding:utf-8

import requests,json


class ipm_data:
    """处理ipm返回的数据"""

    def showidc(self):
        """显示所有机房 """
        idc = [
            {
                "name": "GL",
                "tree_id": 1117,
                "idc_az": []
            },{
                "name": "FB",
                "tree_id": 1113,
                "idc_az": []
            },{
                "name": "FB",
                "tree_id": 1114,
                "idc_az": []
            },{
                "name": "FB",
                "tree_id": 1115,
                "idc_az": []
            },{
                "name": "DSB",
                "tree_id": 1116,
                "idc_az": []
            }
        ]

        return idc


    def get_function(self):
        """ 某个机房下有哪些功能大类"""
        function = [
            {
                "name": "核心区",
                "name_en": "core"
            },{
                "name": "网络区",
                "name_en": "network"
            },{
                "name": "工具区",
                "name_en": "tools"
            },{
                "name": "管理区",
                "name_en": "admin"
            }
        ]
        return function


    def get_sub_function(self):
        """某个功能大类下有哪些功能小类"""
        subfunction = [
            {
                "name": "fat",
                "name_en": "fat"
            },{
                "name": "uat",
                "name_en": "uat"
            },{
                "name": "fat001",
                "name_en": "fat001"
            },{
                "name": "fat002",
                "name_en": "fat002"
            }
        ]
        return subfunction


