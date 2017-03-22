#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from PIL import Image
import oauth2 as oauth
import argparse
import pytumblr
import sys
import urlparse
import yaml


class Blog:
  def __init__(self, client, blog_name):
    self.client = client
    self.blog_name = blog_name
    
    total_posts =  self.client.posts(self.blog_name)['blog']['total_posts']
    print('Hello '+self.blog_name+'! I see you have made '+str(total_posts)+' posts!')

  def setPreviewOnly(self, preview):
    self.preview = preview

  # Print iterations progress
  def print_progress(self, iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    '''
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    '''
    str_format = '{0:.' + str(decimals) + 'f}'
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

  def PurgeUnicode(self):
    log = []
    print('THIS WILL DELETE ALL TAGS WITH UNICODE, INCLUDING EMOJI. THIS WILL NOT DELETE THE POSTS.')
    testVar = ''
    while not (testVar.lower() == 'y' or testVar.lower() == 'n'):
      testVar = raw_input('ARE YOU SURE YOU WANT TO DO THIS?')
    if(testVar.lower() == 'n'):
      sys.exit(0)

    total_posts =  self.client.posts(self.blog_name)['blog']['total_posts']
    log.append(str('Purging Unicode from '+self.blog_name))
    for i in range(0,total_posts,20):
      self.print_progress(i, total_posts)
      for post in self.client.posts(self.blog_name, offset=i)['posts']:
        if len(post['tags']) > 0:
          for t in post['tags']:
            try:
              t.decode('ascii')
            except UnicodeEncodeError:
              log.append(str('Removing  Tag \"'+str(t.encode('utf-8'))+'\"" From Post ID '+str(post['id'])))
              post['tags'].remove(t)
              self.client.edit_post(self.blog_name, id=post['id'], tags=post['tags'])    
    print('Complete!')
    with open('PurgeUnicode.txt', 'w') as f:
      for item in log:
        f.write('%s\n' % item)
    f.closed

  def TotalTags(self):
    print('Printing tags for '+self.blog_name+' in TotalTags.txt')
    total_posts =  self.client.posts(self.blog_name)['blog']['total_posts']
    tags = dict()
    for i in range(0,total_posts,20):
      self.print_progress(i, total_posts)
      for post in self.client.posts(self.blog_name, offset=i)['posts']:
        if len(post['tags']) > 0:
          post['tags'] = [x.lower().encode('utf-8') for x in post['tags']]
          for t in post['tags']:
            if t in tags:
              tags[t] += 1
            else:
              tags[t] = 1
    print('Complete!')
    with open('TotalTags.txt', 'w') as f:
      for x in sorted(tags.items(), key=lambda x:x[1], reverse=True):
        f.write('{0} {1}'.format(*x))
        f.write('\n')
    f.closed

  def TagReplace(self, original_tag, new_tag):
    log = []
    original_tag = original_tag.lower()
    new_tag = new_tag.lower()
    print('Changing tag '+original_tag+' to '+new_tag+' for '+self.blog_name)
    log.append(str('Changing tag '+original_tag+' to '+new_tag+' for '+self.blog_name))
    total_tag_posts = self.client.posts(self.blog_name, tag=original_tag)['total_posts']
    log.append(str(total_tag_posts)+' Posts')
    for i in range(0,total_tag_posts,20):
      for post in self.client.posts(self.blog_name, tag=original_tag, offset=i)['posts']:
        post['tags'] = [x.lower().encode('utf-8') for x in post['tags']]
        if new_tag not in post['tags'] and original_tag in post['tags']:
          post['tags'].append(new_tag)
          post['tags'].remove(original_tag)
          try:
            if self.preview == False:
              self.client.edit_post(self.blog_name, id=post['id'], tags=post['tags'])
            log.append(str('Replaced in: '+str(post['id'])))
          except UnicodeEncodeError:
            log.append(str('ERROR REPLACING TAG IN POST '+str(post['id'])+'! PLEASE CONSIDER RUNNING \'PurgeUnicode\''))
        elif new_tag in post['tags'] and original_tag in post['tags']:
          post['tags'].remove(original_tag)
          try:
            if self.preview == False:
              self.client.edit_post(self.blog_name, id=post['id'], tags=post['tags'])
            log.append(str('Removed in: '+str(post['id'])))
          except UnicodeEncodeError:
            log.append(str('ERROR REPLACING TAG IN POST '+str(post['id'])+'! PLEASE CONSIDER RUNNING \'PurgeUnicode\''))
    print('Complete!')
    with open('TagReplace.txt', 'w') as f:
      for item in log:
        f.write('%s\n' % item)
    f.closed

  def TagAppend(self, tag, additional_tag):
    log = []
    tag = tag.lower()
    additional_tag = additional_tag.lower()
    print('Adding tag '+additional_tag+' to posts tagged as '+tag+' for '+self.blog_name)
    log.append(str('Adding tag '+additional_tag+' to posts tagged as'+tag+' for '+self.blog_name))
    total_tag_posts = self.client.posts(self.blog_name, tag=tag)['total_posts']
    log.append(str(total_tag_posts)+' Posts')
    for i in range(0,total_tag_posts,20):
      if total_tag_posts > 100:
        self.print_progress(i, total_tag_posts)
      for post in self.client.posts(self.blog_name, tag=tag, offset=i)['posts']:
        post['tags'] = [x.lower().encode('utf-8') for x in post['tags']]
        if additional_tag not in post['tags'] and tag in post['tags']:
          post['tags'].append(additional_tag)
          log.append(str('Appended in: '+str(post['id'])))
          try:
            if self.preview == False:
              self.client.edit_post(self.blog_name, id=post['id'], tags=post['tags'])
          except UnicodeEncodeError:
            log.append(str('ERROR REPLACING TAG IN POST '+str(post['id'])+'! PLEASE CONSIDER RUNNING \'PurgeUnicode\''))
    print('Complete!')
    with open('TagAppend.txt', 'w') as f:
      for item in log:
        f.write('%s\n' % item)
    f.closed

  def DeleteTag(self, tag):
    log = []
    tag = tag.lower()
    print('Deleting tag '+tag+' from '+self.blog_name)
    log.append(str('Deleting tag '+tag+' from '+self.blog_name))
    total_tag_posts = self.client.posts(self.blog_name, tag=tag)['total_posts']
    log.append(str(total_tag_posts)+' Posts')
    for i in range(0,total_tag_posts,20):
      if total_tag_posts > 100:
        self.print_progress(i, total_tag_posts)
      for post in self.client.posts(self.blog_name, tag=tag, offset=i)['posts']:
        post['tags'] = [x.lower().encode('utf-8') for x in post['tags']]
        post['tags'].remove(tag)
        log.append(str('Deleted in: '+str(post['id'])))
        if self.preview == False:
          self.client.edit_post(self.blog_name, id=post['id'], tags=post['tags'])
    print('Complete!')
    with open('DeleteTag.txt', 'w') as f:
      for item in log:
        f.write('%s\n' % item)
    f.closed


def init_oauth(yaml_data):
  request_token_url = 'http://www.tumblr.com/oauth/request_token'
  authorize_url = 'http://www.tumblr.com/oauth/authorize'
  access_token_url = 'http://www.tumblr.com/oauth/access_token'

  consumer = oauth.Consumer(yaml_data['consumer_key'], yaml_data['consumer_secret'])
  client = oauth.Client(consumer)

  # Get request token
  resp, content = client.request(request_token_url, 'POST')
  request_token =  urlparse.parse_qs(content)

  # Redirect to authentication page
  print ('\nPlease go here and authorize:\n%s?oauth_token=%s' % (authorize_url, request_token['oauth_token'][0]))
  redirect_response = raw_input('Allow then paste the full redirect URL here:\n')

  # Retrieve oauth verifier
  url = urlparse.urlparse(redirect_response)
  query_dict = urlparse.parse_qs(url.query)
  oauth_verifier = query_dict['oauth_verifier'][0]

  # Request access token
  token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'][0])
  token.set_verifier(oauth_verifier)
  client = oauth.Client(consumer, token)

  resp, content = client.request(access_token_url, 'POST')
  access_token = urlparse.parse_qs(content)

  yaml_data['oauth_token'] = access_token['oauth_token'][0]
  yaml_data['oauth_secret'] = access_token['oauth_token_secret'][0]

  with open('keys.yaml', 'w') as stream:
    yaml.dump(keys_data, stream)

  return yaml_data

def main(argv):
  parser = argparse.ArgumentParser(description='A simple suite of command-line tools to help Tumblr powerusers manage their archive of blog posts.')
  parser.add_argument('actions', metavar='A', type=str, nargs='?',
                    help='the Action for Helpr to run')
  parser.add_argument('--postType', nargs='?', type=str, help='the target post type in an Action')
  parser.add_argument('--tag', nargs='?', type=str, help='the target tag in an Action')
  parser.add_argument('--newTag', nargs='?', type=str, help='the new tag in an Action')
  parser.add_argument('--preview', nargs='?', dest='preview', help='print actions in text file and do not edit blog')
  parser.set_defaults(preview=False)


  args = vars(parser.parse_args())
  with open('keys.yaml', 'r') as stream:
    keys_data = yaml.load(stream)

  if keys_data['oauth_token'] == None or keys_data['oauth_secret'] == None:
    keys_data = init_oauth(keys_data)

  client = pytumblr.TumblrRestClient(
      keys_data['consumer_key'],
      keys_data['consumer_secret'],
      keys_data['oauth_token'],
      keys_data['oauth_secret']
  )

  with open('settings.yaml', 'r') as stream:
    settings_data = yaml.load(stream)

  blog = Blog(client, settings_data['blog_name'])

  blog.setPreviewOnly(args['preview'])

  if args['actions'] == None:
    sys.exit(0)
  elif 'TotalTags' in args['actions']:
    blog.TotalTags()
  elif 'PurgeUnicode' in args['actions']:
    blog.PurgeUnicode()
  elif 'TagReplace' in args['actions']:
    if args['tag'] == None or args['newTag'] == None:
      print('Invalid tag options!')
      sys.exit(2)
    blog.TagReplace(args['tag'], args['newTag'])
  elif 'TagAppend' in args['actions']:
    if args['tag'] == None or args['newTag'] == None:
      print('Invalid tag options!')
      sys.exit(2)
    blog.TagAppend(args['tag'], args['newTag'])
  elif 'DeleteTag' in args['actions']:
    if args['tag'] == None:
      print('Invalid tag options!')
      sys.exit(2)
    blog.DeleteTag(args['tag'])
  else:
    print('Invalid action!')

  

if __name__ == '__main__':
   main(sys.argv[1:])
