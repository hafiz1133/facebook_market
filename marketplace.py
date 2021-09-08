from seleniumwire import webdriver
import time
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

headers = ['Name','Price','Description','Location','Seller_Name','Image_urls','Category','prod_url']
fileout = open('Fb_market.csv','a',newline='',encoding='utf-8')
writer = csv.DictWriter(fileout,fieldnames=headers)
writer.writeheader()

def get_driver(fb_username, fb_password):
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-notifications')

    driver = webdriver.Chrome( chrome_options=options)
    driver.get("https://www.facebook.com/")
    driver.maximize_window()
    email = driver.find_element_by_id("email")
    time.sleep(1)
    email.send_keys(fb_username)
    time.sleep(1)
    password = driver.find_element_by_id("pass")
    password.send_keys(fb_password)
    password.send_keys(Keys.RETURN)
    time.sleep(2)
    mainlink=[]
    mainlink.append('https://www.facebook.com/marketplace/category/hobbies')
    # mainlink.append('https://www.facebook.com/marketplace/category/vehicles')
    # mainlink.append('https://www.facebook.com/marketplace/category/electronics')
    for m_link in mainlink:
        driver.get(m_link)
        cat=driver.find_elements_by_xpath('//a[@class="oajrlxb2 tdjehn4e qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 j83agx80 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys d1544ag0 qt6c0cv9 tw6a2znq i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l bp9cbjyn e72ty7fz qlfml3jp inkptoze qmr60zad btwxx1t3 tv7at329 taijpn5t k4urcfbm"]')
        categories=[]
        catnames=[]
        for c in cat:
            if c.text == '':
                pass
            else:
                categories.append(c.get_attribute('href'))
                catnames.append(c.text)

        for subcat in categories:

            cat = subcat.split('/')
            finalcat=cat[len(cat) - 2]
            driver.get(subcat)
            time.sleep(2)
            #for x in range(7):
                #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                links=driver.find_elements_by_xpath('//div[@class="kbiprv82"]')
                newlink = []
                for l in links:
                    newlink.append(l.find_element_by_tag_name('a').get_attribute('href'))
                for link in newlink:
                    driver.get(link)
                    data=dict()
                    test_flag =True
                    try:
                        with open('Fb_market.csv') as csv_f:
                            csv_reader = csv.reader(csv_f, delimiter=',')
                            for row in csv_reader:
                                if row[7] == driver.current_url:
                                    test_flag = False
                    except:
                        pass
                    if test_flag:
                        data['prod_url'] = driver.current_url
                        forname=driver.find_elements_by_xpath('//span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 qg6bub1s fe6kdd0r mau55g9w c8b282yb iv3no6db o0t2es00 f530mmz5 hnhda86s oo9gr5id"]')
                        for n in forname:
                            if n.text == '':
                                pass
                            else:
                                data['Name']=n.text
                        try:
                            temp=driver.find_element_by_xpath(
                                '//div[@class="aov4n071"]/div[1]/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr ekzkrbhg oo9gr5id"]/span').text
                            latest_P=driver.find_element_by_xpath(
                                '//div[@class="aov4n071"]/div[1]/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr ekzkrbhg oo9gr5id"]').text
                            final=latest_P.replace(temp,'')
                            data['Price']=final
                        except:
                            data['Price'] = driver.find_element_by_xpath(
                                '//div[@class="aov4n071"]/div[1]/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb mdeji52x a5q79mjw g1cxx5fr ekzkrbhg oo9gr5id"]').text
                        try:
                            driver.find_element_by_xpath(
                                '//div[@class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l"][@role="button"]/span').click()
                            data['Description'] = driver.find_element_by_xpath(
                                '//div[@class="ii04i59q a8nywdso f10w8fjw rz4wbd8a pybr56ya"]/div[1]/span').text
                        except:
                            try:
                                data['Description'] = driver.find_element_by_xpath(
                                    '//div[@class="ii04i59q a8nywdso f10w8fjw rz4wbd8a pybr56ya"]/div[1]/span').text
                            except:
                                data['Description']=''
                        try:
                            data['Location']=driver.find_element_by_xpath('.//div[@class="hcukyx3x n851cfcs cxmmr5t8 n1l5q3vz"]/div/div[@class="j83agx80 cbu4d94t ew0dbk1b irj2b8pg"]/div[@class="qzhwtbm6 knvmm38d"]/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v b1v8xokw oo9gr5id hzawbc8m"]/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh jq4qci2q a3bd9o3v lrazzd5p oo9gr5id"]').text
                            x=1
                        except:
                            data['Location']=''
                        try:
                            data['Seller_Name']=driver.find_element_by_xpath(
                                './/div[@class="j83agx80 cbu4d94t ew0dbk1b irj2b8pg"]/div[@class="qzhwtbm6 knvmm38d"]/span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db a5q79mjw g1cxx5fr ekzkrbhg oo9gr5id hzawbc8m"]').text
                        except:
                            data['Seller_Name']=''
                        try:
                            images=driver.find_elements_by_xpath('//img[@class="k4urcfbm bixrwtb6 datstx6m"]')
                            full_url=''
                            for i in images:
                                full_url=full_url + ',' + i.get_attribute('src')

                            data['Image_urls']=full_url
                        except:
                            data['Image_urls']=''
                        data['Category']=finalcat
                        writer.writerow(data)
                        fileout.flush()
            except:
                pass
    driver.quit()
if __name__ == '__main__':
    input_file = open('facebook_email.txt', 'r')
    file_data = input_file.read().split('\n')
    fb_username = file_data[0]
    fb_password = file_data[1]
    while True:
        driver = get_driver(fb_username, fb_password)

