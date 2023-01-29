import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def compare(x, y):
    return x[2] < y[0] or (x[0]==y[0] and x[0]>y[0])
def compare2(x, y):
    return x[2] > y[0] or (x[0]==y[0] and x[0]>y[0])
def run(pref,gender_past,brand_past,color_past,filters):

    analyser = SentimentIntensityAnalyzer()
    data=pd.read_csv("flipkart_skirt.csv")
    data=pd.concat([data,pd.read_csv("flipkart_shirt.csv")], ignore_index=True)
    data=pd.concat([data,pd.read_csv("flipkart_tshirt.csv")],ignore_index=True)
    data=pd.concat([data,pd.read_csv("flipkart_jeans.csv")], ignore_index=True)

    for ind in range(len(data)):
        data.loc[ind, 'rating'] = int(data.loc[ind, 'rating'].replace(',', ''))
        data.loc[ind, 'price'] = int(data.loc[ind, 'price'].replace(',', '')[1:])
        if(not isinstance(data.loc[ind, 'reviews'], int)):
            data.loc[ind, 'reviews'] = int(data.loc[ind, 'reviews'].replace(',', ''))

    data.brand=data.brand.str.lower()
    data.text_reviews = data.text_reviews.str.lower()
    data.text_reviews = data.text_reviews.str.replace('\n','').str.replace('[\'!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~]','')
    data.item_name = data.item_name.str.lower()

    vader_score = []
    for ind in range(len(data)):
        rev = data['text_reviews'][ind]
        x = rev.split()
        sum_score=0.0
        for i in x:
            score = analyser.polarity_scores(i)
            sum_score=sum_score+score['compound']
        vader_score.append(sum_score)
    data['vader_score'] = vader_score

    total_star_givers = data['rating'].sum()
    total_review_givers = data['reviews'].sum()

    data['final_score'] = ((data['stars']*data['rating'])/total_star_givers)+((data['vader_score']*data['reviews'])/total_review_givers)


    #adding gender column
    import numpy as np
    data = data.sample(frac = 1)
    if(pref==True):

        inp={"gender":filters[0] ,"brand":filters[2],"color":filters[1],"price_low":filters[4][0],"price_high":filters[4][1]}
        result = []
        for ind in range(len(data)):
            flag1=(len(inp.get("gender"))==0)
            flag2=(len(inp.get("category"))==0)
            flag3=(len(inp.get("brand"))==0)
            flag4=(len(inp.get("color"))==0)
            for gender in inp.get("gender"):
                if (gender=='women' and gender in data['item_name'][ind]) or (gender=='men' and 'women' not in data['item_name'][ind]):
                    flag1 = True
                    break
            for category in inp.get("category"):
                if category in data['item_name'][ind]:
                    flag2 = True
                    break
            for brand in inp.get("brand"):
                if brand in data['brand'][ind]:
                    flag3 = True
                    break
            for color in inp.get("color"):
                if color in data['item_name'][ind]:
                    flag4 = True
                    break
            if flag1 == True and flag2 == True and flag3 == True and flag4 == True and data['price'][ind]>=inp.get("price_low") and data['price'][ind]<=inp.get("price_high"):
                result.append([data['final_score'][ind], data['url'][ind],data['price'][ind], data['item_name'][ind].title(), data['brand'][ind][:-4].title()])

        import functools
        if(filters[3][0]==1):
            result = sorted(result, key=functools.cmp_to_key(compare))
        elif(filters[3][1]==True):
            result = sorted(result, key=functools.cmp_to_key(compare2))
        else:
            result=sorted(result,reverse=True)

        result.sort(reverse=True)
        print("-----------Output------------")
        return_obj=[]
        for res in result:
             return_obj.append([res[1], res[2],res[3], res[4]])
        return return_obj

    else:
        no_preference=(gender_past=='#' and brand_past=='#' and color_past=='#')
        if(no_preference==True):
            result=[]
            for ind in range(len(data)):
                result.append([data['final_score'][ind],data['url'][ind], data['price'][ind], data['item_name'][ind].title(), data['brand'][ind][:-4].title()])
            result.sort(reverse=True)
            return_obj=[]
            for res in result:
                 return_obj.append([res[1], res[2],res[3], res[4]])
            return return_obj

        else:
            ind1=0
            ind2=0
            preference = {"gender": [gender_past], "brand": [brand_past], "color": [color_past]}
            data['flag']=0
            for ind in range(len(data)):
                flag=False
                for gender in preference.get("gender"):
                    if (gender=='women' and gender in data['item_name'][ind]) or (gender=='men' and 'women' not in data['item_name'][ind]):
                        flag=True
                        break
                for brand in preference.get("brand"):
                    if brand in data["brand"][ind]:
                        flag = True
                        break
                for color in preference.get("color"):
                    if color in data["item_name"][ind]:
                        flag = True
                        break
                if(flag==True):
                    data['flag'][ind]=1
                else :
                    data['flag'][ind]=0
            result=[]
            data_pref=data[data['flag']==1]
            data_nonpref=data[data['flag']==0]
            for i in range(len(data_pref)):
                result.append([data_pref.iloc[i]['final_score'], data_pref.iloc[i]['url'], data_pref.iloc[i]['price'], data_pref.iloc[i]['item_name'].title(), data_pref.iloc[i]['brand'][:-1].title()])
            print(len(data_pref))
            maxi=float(0.4*len(data_nonpref))
            print(maxi)
            for i in range(0,int(maxi)):
                result.append([data_nonpref.iloc[i]['final_score'], data_nonpref.iloc[i]['url'], data_nonpref.iloc[i]['price'], data_nonpref.iloc[i]['item_name'].title(), data_nonpref.iloc[i]['brand'][:-1].title()])
            result.sort(reverse=True)
            return_obj=[]
            for res in result:
                 return_obj.append([res[1], res[2],res[3], res[4]])
            print(return_obj)
            # while(ind1+ind2<len(data)):
            #     new_data1=data_pref[:][ind1:min(ind1+10,len(data_pref)-1)]
            #     new_data2 = data_nonpref[:][ind2:min(ind2 + 30, len(data_nonpref) - 1)]
            #     for ind in range(len(new_data1)):
            #         return_obj.append(new_data1['url'][ind])
            #     for ind in range(len(new_data2)):
            #         return_obj.append(new_data2['url'][ind])
            #     print(ind1)
            #     print(ind2)
            #     ind1 +=min(ind1+10,len(data_pref)-1)+1
            #     ind2 += min(ind2 + 10, len(data_nonpref) - 1) + 1
            return return_obj


