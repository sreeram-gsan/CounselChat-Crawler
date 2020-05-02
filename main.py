import configparser
import requests
import logging
from bs4 import BeautifulSoup

#loding configuration
config = configparser.ConfigParser()
config.read('config.ini')
website_config = config['WEBSITE']
logging_config = config['LOGGING']


def find_question_item_url(questionItem):
    return website_config['WEBSITE_MAIN_URL'] + questionItem.find("a", {"class": "question-title"}).attrs['href']

def get_question_urls_for_a_topic(topic):
    logging.info('Enter get_question_urls_for_a_topic') 
    result = []
    count = 1
    while (count==1 or questionItems != []):
        url = website_config['WEBSITE_MAIN_URL'] + website_config['TOPICS_URL'] + "/" + topic + "?page=" + str(count)
        logging.debug("Topic URL: " + url) 
        page = requests.get(url)    
        soup = BeautifulSoup(page.text, 'html.parser')
        questionItems = soup.find("div", {"class": "list-group list-question-group"}).find_all("div", {"class": "item-question"})                         
        questionUrls = list(map(find_question_item_url,questionItems))    
        logging.debug("Question URLs")
        logging.debug(questionUrls)         
        result+=questionUrls         
        count += 1

    logging.debug("Result of get_question_urls_for_a_topic")
    logging.debug(result)    
    logging.info('Exit get_question_urls_for_a_topic') 
    return result

def write_list_into_file(filename,listItems):
    logging.info('Enter write_list_into_file')     
    with open(filename, "a") as filehandle:
        for listItem in listItems:
            filehandle.write('%s\n' % listItem)
    logging.info('Exit write_list_into_file')

def read_list_from_file(filename):    
    logging.info('Enter read_list_from_file')     
    url_list = []    
    with open(filename, 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]            
            url_list.append(currentPlace)            
    logging.info('Exit read_list_from_file')
    return url_list    
        
def crawl_questions():    
    logging.info('Enter crawl') 
    topics = website_config["TOPICS"].split(",")
    logging.debug("Topics: "+str(topics))
    for topic in topics:
        url_list = get_question_urls_for_a_topic(topic)
        write_list_into_file("questions/"+topic+".txt",url_list)
    logging.info('Exit crawl') 

def main():    
    #logging
    logging.basicConfig(filename=logging_config["LOG_FILE_NAME"],level=logging.DEBUG,filemode="w")
    logging.info('Application Started')      
    # crawl_questions()   
    # crawl_answers()   
    logging.info('Application Ended')

if __name__ == '__main__':
    main()