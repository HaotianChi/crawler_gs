#-*- coding:utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup
import time

def getHtml(url):
    values = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0' }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req) 
    html = response.read()
    return html

def get_results_entry(url):   
    #travesal all the results
    result_entries = []
    link = url
    count = 0
    while(True):
        time.sleep(0.1)
        web_data = getHtml(link)
        soup = BeautifulSoup(web_data, features='html.parser')
        #results = soup.select('span[class="gs_hlt"]')
        results = list(set([each.parent for each in soup.findAll(name="span", attrs={"class": "gs_hlt"})]))
        result_entries += results
        next_button_tag = soup.find(name="button", attrs={"type":"button", "aria-label":"Next"})
        
        try:
            link = "http://scholar.google.com" + next_button_tag.get('onclick').split("=", 1)[1].strip("'")
            link = link.replace("\\x3d", "=")
            link = link.replace("\\x26", "&")
        except:
            break;        
        count = count +1
    return result_entries

    
def get_data_from_entry(result_entries, destination):
    #data = []
    for each in result_entries:
        author = {}
        href = each.get('href')
        gs_homepage = "https://scholar.google.com" + href
        url = gs_homepage
        soup_each = BeautifulSoup(getHtml(url), features='html.parser')
        #data acquisition
        #name
        name = soup_each.select('div[id="gsc_prf_in"]')[0].text
        #position and affiliation
        first_line_text= soup_each.find(name="div", attrs={"class": "gsc_prf_il"}).text
        if(first_line_text.find(',') == -1):
            position = "Unknown"
            affiliation = first_line_text
        else:
            (position, affiliation) = first_line_text.split(',', 1)
        #email            
        email= soup_each.find(name="div", id={"gsc_prf_ivh"}).text.split('-')[0].strip()
        #homepage
        homepage_tag = soup_each.find(name="a", rel="nofollow")
        if homepage_tag != None:
            homepage = homepage_tag.get('href')
        else:
            homepage = gs_homepage
        #interests
        interests = [each.text for each in soup_each.findAll(name="a", attrs={"class": "gsc_prf_ila"})]
        hindex = soup_each.find(name="td", attrs={"class": "gsc_rsb_sc1"}).parent.next_sibling.contents[1].text
        #iteration to get all publications
        publications = []
        pub_page = 0
        while(True):
            url = url + "&cstart={}&pagesize=20".format(str(pub_page))
            soup_pub = BeautifulSoup(getHtml(url), features='lxml')
            publication_entry_list = soup_each.findAll(name="a", attrs={"class": "gsc_a_at"})
            titles = [each.text for each in publication_entry_list]
            authors = [each.next_sibling.text for each in publication_entry_list]
            venues = [each.next_sibling.next_sibling.text for each in publication_entry_list]
            years = [each.span.text for each in soup_each.findAll(name="td", attrs={"class": "gsc_a_y"})]
            for title, author, venue, year in zip(titles, authors, venues, years):
                paper_info = {
                        "title": title,
                        "authors": author,
                        "publication venue": venue,
                        "year": year,
                              }
                publications.append(paper_info)
            pub_page += 20
            if soup_pub.find(name="button", attrs={"id": "gsc_bpf_next", "aria-label": "Next"}).get('disabled') != None:
                break
        author = {
                "name": name,
                "position": position,
                "affiliation": affiliation,
                "email": email,
                "homepage": homepage,
                "interests:": interests,
                "h-index": hindex,
                "publications": publications,
                }
        print >> destination, author
        print >> destination, '\n'
        
        
def get_author_num(url):   
    link = url
    num = 0
    while(True):
        time.sleep(0.1)
        web_data = getHtml(link)
        soup = BeautifulSoup(web_data, features='html.parser')
        #results = soup.select('span[class="gs_hlt"]')
        results = list(set([each.parent for each in soup.findAll(name="span", attrs={"class": "gs_hlt"})]))
        num += len(results)
        try:
            next_button_tag = soup.find(name="button", attrs={"type":"button", "aria-label":"Next"})
            link = "http://scholar.google.com" + next_button_tag.get('onclick').split("=", 1)[1].strip("'")
            link = link.replace("\\x3d", "=")
            link = link.replace("\\x26", "&")
        except:
            break;        
    return num        


if __name__ == "__main__":
    names = []
    with open("names.txt", "r") as f:
        names = f.readlines()
        names = [item.strip() for item in names]
        
    
    search_list = []
    for each in names:
        (firstname, lastname) = each.split()
        name_dictionary = {"firstname": firstname, "lastname": lastname}
        search_list.append(name_dictionary)
    
    print search_list
    
    
    search_urls = ['https://scholar.google.com/citations?mauthors={}+{}&hl=en&view_op=search_authors'.
                   format(search_list[i]['firstname'], search_list[i]['lastname']) for i in range(0, len(search_list))]

    with open('data.txt', 'wb') as fout:    
        for each in search_urls:       
            num = get_author_num(each)
            print num
            #get_data_from_entry(result_entries, fout)
            #all_data.append(data)
    
    
    
#    with open('data.txt', 'wb') as fout:
#        print >> fout, all_data 
#    with open('data.pkl', 'wb') as f:
#        pickle.dump(data, f)
        
    f.close()
    

