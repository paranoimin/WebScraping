import requests
from bs4 import BeautifulSoup
from xml.dom import minidom

url = "http://arribista.co.kr/sitemap.xml"
page = requests.get(url)

root = minidom.Document()
rss = root.createElement('rss')
rss.setAttribute('version', '2.0')
rss.setAttribute('xmlns:g', 'http://base.google.com/ns/1.0')
root.appendChild(rss)

channel = root.createElement('channel')
rss.appendChild(channel)

title = root.createElement('title')
title.appendChild(root.createTextNode('아리비스트 - arribista'))
channel.appendChild(title)

siteLink = root.createElement('link')
siteLink.appendChild(root.createTextNode('http://arribista.co.kr'))
channel.appendChild(siteLink)

desc = root.createElement('description')
desc.appendChild(root.createTextNode('아리비스타'))
channel.appendChild(desc)

if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')

    for link in soup.find_all('loc'):
        correctURL = link.text
        correctPAGE = requests.get(correctURL)
        corSoup = BeautifulSoup(correctPAGE.content, 'html.parser')
        p_no = corSoup.find('input', id='pars_no')['dds']
        p_name = corSoup.find('input', id='pars_name')['dds']
        p_img = corSoup.find('input', id='pars_img')['dds']
        p_price = corSoup.find('input', id='pars_price')['dds']

        item = root.createElement('item')
        channel.appendChild(item)

        g_id = root.createElement('g:id')
        g_id.appendChild(root.createTextNode(p_no))
        item.appendChild(g_id)

        g_title = root.createElement('g:title')
        g_title.appendChild(root.createCDATASection(p_name))
        item.appendChild(g_title)

        g_description = root.createElement('g:description')
        g_description.appendChild(root.createCDATASection(p_name))
        item.appendChild(g_description)

        g_google_product_category = root.createElement('g:google_product_category')
        g_google_product_category.appendChild(root.createCDATASection('Apparel & Accessories > Clothing'))
        item.appendChild(g_google_product_category)

        g_product_type = root.createElement('g:product_type')
        g_product_type.appendChild(root.createTextNode('product'))
        item.appendChild(g_product_type)

        g_link = root.createElement('g:link')
        g_link.appendChild(root.createTextNode(correctURL))
        item.appendChild(g_link)

        g_image_link = root.createElement('g:image_link')
        g_image_link.appendChild(root.createTextNode(p_img))
        item.appendChild(g_image_link)

        g_condition = root.createElement('g:condition')
        g_condition.appendChild(root.createTextNode('new'))
        item.appendChild(g_condition)

        g_availability = root.createElement('g:availability')
        g_availability.appendChild(root.createTextNode('in stock'))
        item.appendChild(g_availability)

        g_price = root.createElement('g:price')
        g_price.appendChild(root.createTextNode(p_price))
        item.appendChild(g_price)

        g_brand = root.createElement('g:brand')
        g_brand.appendChild(root.createTextNode('아리비스타'))
        item.appendChild(g_brand)

else:
    print("fail...")

# childOfProduct.appendChild(root.createCDATASection('abc & > def'))
# productChild.appendChild(childOfProduct)

xml_str = root.toprettyxml(indent="\t")
save_path_file = "test.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)




#### xml ###

# <?xml version="1.0" encoding="utf-8"?>
# <rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">
# <channel>
# <title>탐난다 - TAMNANDA</title>
# <link>http://tam-nanda.com</link>
# <description>탐난다</description>
# <item>
# <g:id><%=product_no%></g:id>
# <g:title><![CDATA[<%=product_name%>]]></g:title>
# <g:description><![CDATA[<%=product_name%>]]></g:description>
# <g:google_product_category><![CDATA[Apparel & Accessories > Clothing]]></g:google_product_category>
# <g:product_type>product</g:product_type>
# <g:link><%=product_url%></g:link>
# <g:image_link>http:<%=product_img%></g:image_link>
# <g:condition>new</g:condition>
# <g:availability>in stock</g:availability>
# <g:price><%=product_price%> KRW</g:price>
# <g:brand>탐난다</g:brand>
# </item>
# </channel>
# </rss>