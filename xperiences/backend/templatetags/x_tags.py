import random
from django.template.context import Context
from django.template.defaulttags import url

__author__ = 'ishai'

__author__ = 'ishai'

from django import template


def register_all():
    pass

register = template.Library()

class TextNode(template.Node):
    def __init__(self, str):
        self.str = str
    def render(self,context):
        return self.str

@register.tag
def t_if(parser,token):
    exp = token.split_contents()
    return TextNode('{{if ' + exp[1] + '}}')

@register.tag
def t_else(parser,token):
    return TextNode('{{else}}')

@register.tag
def t_endif(parser,token):
    return TextNode('{{/if}}')

@register.tag
def t_var(parser,token):
    exp = token.split_contents()
    if len(exp) == 2:
        return TextNode('${' + exp[1] + '}')
    else:
        return TextNode('${%s!=null?%s:%s}' % (exp[1],exp[1],exp[2]))

@register.tag
def t_url(parser,token):
    exp = token.split_contents()
    new_content = exp[0] + ' ' + exp[1]
    args = {}
    arg_names = {}
    for i in range(len(exp)-2):
        argname = ''.join([random.choice('1234567890') for j in range(15)] ) # 'xp_tag_arg%d'% i
        args[argname] = '${' + exp[i+2] + '}'
        arg_names[argname] = argname
        new_content += ' ' + argname
    token.contents = new_content
    tagged =  url(parser,token)
    old_render = tagged.render
    def new_render(context):
        rendered = old_render(Context(arg_names))
        for arg in args:
            rendered = rendered.replace(arg,args[arg])
        return rendered
    tagged.render = new_render
    return tagged

@register.tag
def t_uri(parser,token):
    exp = token.split_contents()
    return TextNode('${encodeURIComponent(' + exp[1] + ')}')


@register.tag
def t_for(parser,token):
    exp = token.split_contents()
    if len(exp) > 2:
        arg = exp[2]
    else:
        arg = 'tmpl_for_item'
    if len(exp) > 3:
        index = exp[3]
    else:
        index = 'tmpl_for_index'
    return TextNode('{{if %s.length}}{{each(%s,%s) %s}}' % (exp[1], index,arg,exp[1]))

@register.tag
def t_for_index(parser,token):
    exp = token.split_contents()
    arg = ''
    if len(exp) > 1:
        arg = exp[1]
    return TextNode('${tmpl_for_index' + arg + '}')

@register.tag
def t_endfor(parser,token):
    return TextNode('{{/each}}{{/if}}')

@register.tag
def t_empty(parser,token):
    return TextNode('{{/each}}{{else}}')

@register.tag
def t_endfor_empty(parser,token):
    return TextNode('{{/if}}')

@register.tag
def t_include(parser,token):
    exp = token.split_contents()
    sel = exp[1]
    if len(exp) > 2:
        data = '(%s)' % exp[2]
    else:
        data = ''
    return TextNode('{{tmpl%s %s}}' % (data, sel))