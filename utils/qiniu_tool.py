# -*- coding: utf-8 -*-


from globals import config


#
def get_photo(key, **kwargs):
    domain = config.get("QINIU").get('url')
    if kwargs.get("flag"):
        width = kwargs.get("width")
        height = kwargs.get("height")
        arg = 'imageView2/2/w/%s/h/%s/interlace/0/q/100' % (width, height)
        url = "%s/%s?%s" % (domain, key, arg)
    else:
        url = "%s/%s" % (domain, key)
    return url

#

# qiniu:
# secret_key: 'oKq15bIPuVjrIk6v7nI3L1bzcVK5z4cVBES4og-x'
# access_key: 'NmYHY9METZ8DMuxSuJv_u8xE5EuESKtcbAmhN1b4'
# url: '7xvcpi.com1.z0.glb.clouddn.com'
# bucket: 'o3partner'
# mark_text: 'aoao'
# small: 'http://%s/%s-small.jpg'
# medium: 'http://%s/%s-medium.jpg'
# large: 'http://%s/%s-large.jpg'
