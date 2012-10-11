from SOAPpy import SOAPServer
import sys, os, json, urllib, datetime
from twitter import Twitter, OAuth

def geturllength(url):
    twitterconfig = json.loads(
        urllib.urlopen('http://api.twitter.com/1/help/configuration.json')
        .read()
        )
    if url.startswith('https://'):
        return twitterconfig['short_url_length_https']
    else:
        return twitterconfig['short_url_length']
    
def tweet(data, conf):
    body = conf['body'] % data
    url = conf['url'] % data
    urllen = geturllength(url)

    if len(body+' ')+urllen > 140:
      body = body[:136-urllen]+"..."
    
    tweet = '%s %s' % (body, url)

    t = Twitter(
        auth=OAuth(
            conf['accesstoken'],
            conf['accesstokensecret'],
            conf['consumerkey'],
            conf['consumersecret']
        )
    )
    print '%s Tweeting: %r' % (datetime.datetime.now(), tweet)
    try:
        t.statuses.update(status=tweet)
        print '%s Done!' % (datetime.datetime.now())
    except Exception, e:
        print '%s Failed: %s' % (datetime.datetime.now(), e)

def commit(Array):
    data = dict(zip(('version', 'repoid', 'checksum', 'rev', 'paths', 'log', 'author', 'branch', 'module'), Array))
    if data['repoid'] in config['repos']:
        tweet(data, config['repos'][data['repoid']])

    return "OK"

if __name__=='__main__':
    config = json.loads(file('config.json').read())
    server = SOAPServer((config['host'], config['port']))
    server.registerFunction(commit, config['namespace'])
    server.serve_forever()
