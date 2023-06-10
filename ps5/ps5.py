# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    '''
    A class representation of a news story
    '''

    def __init__(self, guid, title, description, url, pubdate):
        '''
        Initializes a NewsStory object
                    
        guid (string)       : globally unique identifier for this news story
        title (string)      : the news story's headline
        description (string): a paragraph summarizing the news story
        link (string)       : a link to a website with the entire story
        pubdate (datetime)  : date the news was published

        a NewsStory object has 5 attributes:
            self.guid (string, determined by input guid)
            self.title (string, determined by input title)
            self.description (string, determined by input description)
            self.link (string, determined by input link)
            self.pubdate (datetime, determined by input pubdate)
        '''

        self.guid        = guid
        self.title       = title
        self.description = description
        self.url         = url
        self.pubdate     = pubdate

    def get_guid(self):
        '''
        Used to safely access self.guid outside of the class
        
        Returns: self.guid
        '''
        return self.guid
    
    def get_title(self):
        '''
        Used to safely access self.title outside of the class
        
        Returns: self.title
        '''
        return self.title
    
    def get_description(self):
        '''
        Used to safely access self.description outside of the class
        
        Returns: self.description
        '''
        return self.description
    
    def get_link(self):
        '''
        Used to safely access self.url outside of the class
        
        Returns: self.url
        '''
        return self.url
    
    def get_pubdate(self):
        '''
        Used to safely access self.pubdate outside of the class
        
        Returns: self.pubdate
        '''
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    '''
    An abstract class representation of trigger to a phrase
    '''
        
    def __init__(self, phrase):
        '''
        Initializes a PhaseTrigger object
                    
        phrase (string) : phrase that causes the trigger

        a NewsStory object has 1 attribute:
            self.phrase (string, determined by input phrase)
        '''
        self.phrase = phrase

    def is_phrase_in(self, text):
        '''
        Checks if the class variable self.phrase is in text.       
        
        text (string): sentence to check if self.phrase is in 

        Returns: True if self.phrase is in text, False otherwise
        '''
        translation_table = str.maketrans(string.punctuation, " "*len(string.punctuation))
        translated_text = text.translate(translation_table)
        stripped_text = " ".join(translated_text.lower().split())
        phrase_with_boundries = r'\b' + self.phrase.lower() + r'\b'
        return bool( re.search(phrase_with_boundries, stripped_text) )

# Problem 3
class TitleTrigger(PhraseTrigger):
    '''
    A class representation of trigger of a news title
    ''' 
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news title, or False otherwise.
        """
        return self.is_phrase_in(story.get_title()) 

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    '''
    A class representation of trigger of a news description
    ''' 
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news description, or False otherwise.
        """
        return self.is_phrase_in(story.get_description()) 

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    '''
    A class representation of trigger of a news time stamp
    '''
    def __init__(self, time_est):
        '''
        Initializes a TimeTrigger object
                    
        time_est (string) : Time has to be in EST and in the format of "%d %b %Y %H:%M:%S"

        a TimeTrigger object has 1 attribute:
            self.pubtime (datatime, determined by input time_est)
        '''
        time_format = "%d %b %Y %H:%M:%S"
        pubtime = datetime.strptime(time_est, time_format)
        pubtime = pubtime.replace(tzinfo=pytz.timezone("EST"))
        self.pubtime = pubtime

# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        """
        Returns True if given news dated before trigger, or False otherwise.
        """
        return self.pubtime > story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))

class AfterTrigger(TimeTrigger): 
    def evaluate(self, story):
        '''
        Returns True if given news dated after trigger, or False otherwise.
        '''
        return self.pubtime < story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    '''
    A class representation of a not trigger
    '''
    def __init__(self, T) -> None:
        '''
        Initializes a NotTrigger object
                    
        T (Trigger) : Trigger object that will be inverted"

        a NotTrigger object has 1 attribute:
            self.T (Trigger, determined by input T)
        '''
        self.trigger = T

    def evaluate(self, story):
        '''
        Returns inverse output of another trigger.
        '''
        return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    '''
    A class representation of an and trigger
    '''
    def __init__(self, T_1, T_2) -> None:
        '''
        Initializes an AndTrigger object
                    
        T_1 (Trigger) : Trigger object"
        T_2 (Trigger) : Trigger object"

        an AndTrigger object has 2 attribute:
            self.T_1 (Trigger, determined by input T)
            self.T_2 (Trigger, determined by input T)
        '''
        self.trigger_1 = T_1
        self.trigger_2 = T_2

    def evaluate(self, story):
        '''
        Returns True if both of the inputted triggers 
        evalute to True, or False otherwise
        '''
        return self.trigger_1.evaluate(story) and self.trigger_2.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    '''
    A class representation of an or trigger
    '''
    def __init__(self, T_1, T_2) -> None:
        '''
        Initializes an OrTrigger object
                    
        T_1 (Trigger) : Trigger object"
        T_2 (Trigger) : Trigger object"

        an OrTrigger object has 2 attribute:
            self.T_1 (Trigger, determined by input T)
            self.T_2 (Trigger, determined by input T)
        '''
        self.trigger_1 = T_1
        self.trigger_2 = T_2

    def evaluate(self, story):
        '''
        Returns True if either of the inputted triggers 
        evalute to True, or False otherwise
        '''
        return self.trigger_1.evaluate(story) or self.trigger_2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    # return a list of stories that have a True trigger
    trig_stories = []
    for story in stories:
        for trig in triggerlist:
            if trig.evaluate(story):
                trig_stories.append(story)
                break
    return trig_stories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    trig_dict = {}
    trig_list = []
    for line in lines:
        trig = line.split(',')
        if trig[1] == 'TITLE':
            trig_dict[trig[0]] = TitleTrigger(trig[2])
        elif trig[1] == 'DESCRIPTION':
            trig_dict[trig[0]] = DescriptionTrigger(trig[2])
        elif trig[1] == 'AFTER':
            trig_dict[trig[0]] = AfterTrigger(trig[2])
        elif trig[1] == 'BEFORE':
            trig_dict[trig[0]] = BeforeTrigger(trig[2])
        elif trig[1] == 'NOT':
            trig_dict[trig[0]] = NotTrigger(trig[2])
        elif trig[1] == 'AND':
            trig_dict[trig[0]] = AndTrigger(trig_dict[trig[2]], trig_dict[trig[3]])
        elif trig[0] == 'ADD':
            for x in range(1, len(trig)):
                trig_list.append(trig_dict[trig[x]])
    return trig_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

