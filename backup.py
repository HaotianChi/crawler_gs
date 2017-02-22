#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time

def get_results_entry(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    result_entries = []
    while(True):
        web_data = requests.get(url, headers=headers)
        #web_data
        soup = BeautifulSoup(web_data.text, features='lxml')
        results = list(set(soup.select('span[class="gs_hlt"]')))
        result_entries += results
        
        next_button_tag = soup.find(name="button", attrs={"type":"button", "aria-label":"Next"})
        if next_button_tag.get('disabled') != None:
            break;
        else:
            url = next_button_tag.get('onclick').split('=', 1)[1].strip("'")
        print result_entries
    return result_entries

    
def get_data_from_entry(result_entries):
    for each in result_entries:
        href = each.parent.get('href')
        gs_homepage = "https://scholar.google.com" + href
        url = gshomepage
        soup_each = BeautifulSoup(requests.get(url).text, features='lxml')
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
            homepage = None
        #interests
        interests = [each.text for each in soup_each.findAll(name="a", attrs={"class": "gsc_prf_ila"})]
        hindex = soup_each.find(name="td", attrs={"class": "gsc_rsb_sc1"}).parent.next_sibling.contents[1].text
        #iteration to get all publications
        publications = []
        pub_page = 0
        while(True):
            url = url + "&cstart={}&pagesize=20".format(str(pub_page))
            soup_pub = BeautifulSoup(requests.get(url).text, features='lxml')
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
    
    
    search_urls = ['https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors={}+{}&before_author=5Hno_8sFAAAJ&astart=0'.
                   format(search_list[i]['firstname'], search_list[i]['lastname']) for i in range(0, len(search_list))]
    
    result_entries = get_results_entry(search_urls[0])
    get_data_from_entry(result_entries)

#url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html'
#urls = ['https://cn.tripadvisor.com/Attractions-g60763-Activities-oa{}-New_York_City_New_York.html'.format(str(s)) for s in range(00, 1080, 30)]
#
#def get_attractions(url, data=None):
#    web_data = requests.get(url)
#    #web_data
#    time.sleep(2)
#    soup = BeautifulSoup(web_data.text, features='lxml')
#    titles = soup.select('div.property_title > a[target="_blank"]')
#    imgs = soup.select('img[width="160"]')
#    cates = soup.select('div.p13n_reasoning_v2')  
#    for title, img, cate in zip(titles, imgs, cates):
#        data = {
#                'title': title.get_text(),
#                'img': img.get('srt'),
#                'cate': list(cate.stripped_strings),
#        }
#        #print(data['cate'][0])
#
#for each_url in urls:
#    get_attractions(each_url)
#
#
#print("hello world")
    

