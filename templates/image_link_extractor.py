#!/usr/bin/env python
# coding: utf-8

# In[4]:


from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re
import numpy as np


# In[12]:


def extract(url):
    x = requests.get(url)
    soup = bs(x.content,'html.parser')
    img_link = soup.findAll("img",{'class':'_2r_T1I _396QI4'})
    img_link = str(img_link)
    return img_link[42:-4]


# In[16]:


s = extract("https://www.flipkart.com/unique-choice-printed-women-a-line-black-skirt/p/itm6114c3ede223c?pid=SKIFZWYZJZMAHZ9H&lid=LSTSKIFZWYZJZMAHZ9HCTRUEZ&marketplace=FLIPKART&store=clo%2Fvua%2Fiku&srno=b_1_18&otracker=browse&iid=a84346d9-b4b3-4211-a504-21d48bbc81df.SKIFZWYZJZMAHZ9H.SEARCH&ssid=lmymys8mw00000001674934341414")
s


# In[ ]:




