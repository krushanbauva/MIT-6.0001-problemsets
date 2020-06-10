# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Krushans
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

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Initializes a NewsStory object
        ------------------------
        Parameters:
            guid (string) : A globally unique identifier for this news story
            title (string) : The news story's headline
            description (string) : A paragraph or so summarizing the news story
            link (string) : A link to a website with the entire story
            pubdate (datetime) : Date the news was published
        ------------------------
        Returns:
            None
        '''
        self.guid = guid
        self. title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
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

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        '''
        Returns True if the phrase is in the text
        '''
        text = text.lower()
        text_without_punctuation = text[:]
        for i in string.punctuation:
            text_without_punctuation = text_without_punctuation.replace(i, " ")
        #print("Text without punctuation:", text_without_punctuation)
        list_of_words = text_without_punctuation.split(" ")
        list_of_words_in_text = []
        for i in list_of_words:
            if not (i == "" or i == " "):
                list_of_words_in_text.append(i)
        updated_text = " " + " ".join(list_of_words_in_text) + " "
        phrase = " " + self.phrase + " "
        if phrase in updated_text:
            return True
        else:
            return False


class TitleTrigger(PhraseTrigger):
    '''
    Returns True if phrase is in the Title
    '''
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, NewsStory_object):
        return self.is_phrase_in(NewsStory_object.get_title())


class DescriptionTrigger(PhraseTrigger):
    '''
    Returns True if phrase is in the Description
    '''
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, NewsStory_object):
        return self.is_phrase_in(NewsStory_object.get_description())


# TIME TRIGGERS

class TimeTrigger(Trigger):
    def __init__(self, time):
        '''
        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
        Convert time from string to a datetime before saving it as an attribute
        '''
        format = "%d %b %Y %H:%M:%S"
        time = datetime.strptime(time, format)
        self.time = time

class BeforeTrigger(TimeTrigger):
    def evaluate(self, NewsStory_object):
        if NewsStory_object.get_pubdate() < self.time:
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):
    def evaluate(self, NewsStory_object):
        if NewsStory_object.get_pubdate() > self.time:
            return True
        else:
            return False


# COMPOSITE TRIGGERS

class NotTrigger(Trigger):
    def __init__(self, T):
        self.T = T

    def evaluate(self, NewsStory_object):
        if self.T.evaluate(NewsStory_object):
            return False
        return True


class AndTrigger(Trigger):
    def __init__(self, T1, T2):
        self.T1 = T1
        self.T2 = T2

    def evaluate(self, NewsStory_object):
        if self.T1.evaluate(NewsStory_object) and self.T2.evaluate(NewsStory_object):
            return True
        return False


class OrTrigger(Trigger):
    def __init__(self, T1, T2):
        self.T1 = T1
        self.T2 = T2

    def evaluate(self, NewsStory_object):
        if self.T1.evaluate(NewsStory_object) or self.T2.evaluate(NewsStory_object):
            return True
        return False


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
    return filtered_stories


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
    
    trigger_dict = {}
    trigger_list = []
    
    for line in lines:
        l = line.split(",")
        if l[0] == "ADD":
            for i in range(1, len(l)):
                trigger_list.append(trigger_dict[l[i]])
        else:
            if l[1] == "TITLE":
                trigger_dict[l[0]] = TitleTrigger(l[2])
            elif l[1] == "DESCRIPTION":
                trigger_dict[l[0]] = DescriptionTrigger(l[2])
            elif l[1] == "AFTER":
                trigger_dict[l[0]] = AfterTrigger(l[2])
            elif l[1] == "BEFORE":
                trigger_dict[l[0]] = BeforeTrigger(l[2])
            elif l[1] == "NOT":
                trigger_dict[l[0]] = NotTrigger(l[2])
            elif l[1] == "AND":
                trigger_dict[l[0]] = AndTrigger(l[2], l[3])
            elif l[1] == "OR":
                trigger_dict[l[0]] = OrTrigger(l[2], l[3])
    return trigger_list    


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        
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
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


# if __name__ == '__main__':
#     root = Tk()
#     root.title("Some RSS parser")
#     t = threading.Thread(target=main_thread, args=(root,))
#     t.start()
#     root.mainloop()

