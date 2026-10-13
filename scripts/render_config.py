"""Render equivalent inline and standalone browser team configuration pages."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def presets():
    def member(role, model, effort):
        return dict(role=role, model='gpt-'+model, effort=effort)
    return [
        dict(id='A', name='轻量双人协作', benefit='轻量扫描与逐项核对', boundary='复杂根因留给主 Agent', order='parallel', members=[member('结构与依赖扫描','6-luna','medium'),member('逐项核对','6-luna','high')]),
        dict(id='B', name='实现与独立审查', benefit='实现与审查职责分离', boundary='最终审查须等待实现完成', order='review', members=[member('功能实现','6.1-sol','high'),member('接口与回归审查','6-luna','high')]),
        dict(id='C', name='架构与模块开发', benefit='先定接口，再分模块实现', boundary='架构先行，注意集成成本', order='architecture', members=[member('架构与接口','6-astra','high'),member('核心模块','6.1-sol','high'),member('配套模块','6-luna','high')]),
        dict(id='D', name='故障定位与修复', benefit='根因、证据、修复分工', boundary='修复依赖诊断结果，按证据提高强度', order='diagnosis', members=[member('根因分析','6-astra','high'),member('日志与复现证据','6-luna','high'),member('修复与验证','6.1-sol','high')]),
        dict(id='E', name='科研代码与稿件核对', benefit='方法、代码与细项证据分工', boundary='只读核对，不替代原始实验', order='parallel', members=[member('方法与实验逻辑','6-astra','high'),member('代码与实验流程追踪','6.1-sol','high'),member('公式与数值核对','6-luna','high')]),
        dict(id='F', name='对抗式方案审查', benefit='独立方案、反例与验收用例', boundary='不按投票裁决，协调成本较高', order='parallel', members=[member('可实施方案','6.1-sol','high'),member('反例与约束','6-astra','xhigh'),member('验收用例','6-luna','high')]),
        dict(id='G', name='日常开发三岗位', benefit='实现、独立审查、测试与复现', boundary='测试准备可并行，最终审查等待代码与证据', order='tested_review', members=[member('功能实现','6.1-sol','high'),member('独立审查','6-luna','high'),member('测试与复现','6-luna','medium')]),
        dict(id='H', name='关键改动审查', benefit='复杂审查与测试证据配合', boundary='适用于关键改动，增加审查投入', order='tested_review', members=[member('功能实现','6.1-sol','high'),member('关键逻辑审查','6-astra','high'),member('测试与复现','6-luna','high')]),
    ]


def render(context, output, mode="inline"):
    if mode not in ("inline", "browser"):
        raise ValueError("Unsupported presentation mode")
    caps=context.get('capabilities')
    if not isinstance(caps,dict) or not caps:
        raise ValueError('Provide verified capabilities; no guessed model catalog.')
    for key,values in caps.items():
        if not isinstance(key,str) or not isinstance(values,list) or not values or not all(isinstance(v,str) for v in values):
            raise ValueError('Invalid model/effort capability mapping.')
    limit=context.get('max_concurrency')
    if type(limit) is not int or limit<1:
        raise ValueError('Provide the actual positive subagent concurrency limit.')
    context={**context,'presets':presets(), 'presentation_mode':mode}
    data=json.dumps(context,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    template=(ROOT/'assets/team-config.html').read_text(encoding='utf-8')
    if template.count('__TEAM_CONTEXT__')!=1:
        raise ValueError('Template context marker mismatch')
    fragment=template.replace('__TEAM_CONTEXT__',data)
    if mode == 'browser':
        fragment = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n'
                    '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                    '<title>团队配置 · 浏览器版</title>\n'
                    '<style>html{color-scheme:light dark}body{margin:0;padding:20px;'
                    'background:light-dark(#eef0f6,#111319);font-family:system-ui,sans-serif;}'
                    'main{max-width:1100px;margin:auto;}@media(max-width:500px){body{padding:8px;}}</style>\n'
                    '</head>\n<body><main>\n' + fragment + '\n</main></body>\n</html>\n')
    output.write_text(fragment, encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--context',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--mode',choices=['inline','browser'],default='inline')
    a=p.parse_args()
    render(json.loads(a.context.read_text(encoding='utf-8')),a.output,a.mode)
    print(a.output)
