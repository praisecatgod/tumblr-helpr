# Tumblr Helpr

A simple suite of command-line tools to help Tumblr ~~addicts~~ powerusers manage their archive of blog posts.

## Start Up

### Initialization

[Please register your own Tumblr API app](https://www.tumblr.com/oauth/apps). If you have never registered with an API before, don't worry about the details. Because this software does a lot and runs on the command line, you will need to have your own keys.

In the `keys.yaml` file, insert your `consumer_key` and `consumer_secret`. If you would like to insert your `oauth_secret` and `oauth_token` manually, you can do that too. If you have absolutely no idea how to do the latter, don't fret! Helpr will help you set it when you first run the application, and remember if for later sessions.

In `settings.yaml`, please enter the blog name you wish to manage. (That's the `BLOGNAME` as in `BLOGNAME.tumblr.com`.)

That is the absolute bare minimum Helpr needs to get started. You can initialize or test this out by running 

```bash
python helpr.py
```

If all goes according to plan, it should greet you and let you know how many posts are on that blog. But the real fun begins with the different Actions! 

### Unicode Issue

**There is a (currently) inavoidable issue with Unicode characters when editing tags.** This includes emoji characters. The issue is rooted in a library PyTumblr uses, so it's hard to remedy on my own. I have written a workaround that will simply skip any troublesome posts, and have included a function called ``PurgeUnicode`` which will delete all Unicode containing tags. Emoji's be gone! 💩

### Preview

Running Actions that add, edit, or delete tags can be scary. Actions that delete posts are downright horrifying! Save yourself the nightmare of misplaced keystrokes and general internet shenanigans and run a preview run. Just append `--preview` to your arguements, and it will just print to Log, so you can see what would get done. This will not work with `PurgeUnicode`, which has a manual confirmation.

### Log

Wanna see what actually happened? Each Action spits out a txt file that gives you progress of what was done. It also contains aggravated ranting whenever it encounters that obnoxious Unicode bug.


## Actions

The general format for running an Action is like this:

```bash
python helpr.py ACTION --option1 'ONE' --option2 'TWO' 
```
Change things up depending on what you want to do, but please keep your options in single-quotes to make things easier!


### TotalTags

```bash
python helpr.py TotalTags
```

Lists all tags and their number of usages in TotalTags.txt, sorted by most frequent.

This takes a long time.

### TagReplace

```bash
python helpr.py TagReplace --tag 'OLDTAG' --newTag 'NEWTAG'
```

Replaces one tag with a new one.

### TagAppend

```bash
python helpr.py TagAppend --tag 'TAG' --newTag 'NEWTAG'
```

Adds a tag to any posts with a certain tag. Does not delete the original tag.

### DeleteTag

```bash
python helpr.py DeleteTag --tag 'TAG'
```

Deletes a certain tag. Does not delete the post it was tagged on.

### PostTypeLabel

```bash
python helpr.py PostTypeLabel --postType 'TYPE' --tag 'TAG'
```
Adds a tag to posts of a certain type.

### PurgeUnicode

```bash
python helpr.py PurgeUnicode
```

Tired of skipping over posts? Are you willing to give up the 👀💥💯🍆 in favor or more post editing?

This will remove all Unicode tags from all posts. It will not delete the actual posts. 

This one takes a while.
