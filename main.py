import requests 
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import messagebox
from tkinter import ttk
from tkinter import *


class Scraper :
    def __init__(self,product):

        """This is the Constructor, a special method which is automatically called when the instance of a 
          class is created
          it takes a product name as a argument and create connection with website
          after that does all the operations like checking whether data is available or not,
          cleaning the data, merging different dataframes created for different product numbers
          and return the final dataframe"""

        self.product = product
        self.base_url = "https://www.accessdata.fda.gov/scripts/cder/ob/"
        self.url = 'https://www.accessdata.fda.gov/scripts/cder/ob/search_product.cfm' 
        self.post_params = {'drugname': self.product, 'discontinued': 'RX,OTC,DISCN','submit':'Search'}
        print(self.post_params['drugname'])
        res1 = requests.post(self.url, data=self.post_params)
        soup = BeautifulSoup(res1.text, 'lxml')
        # print(soup)


        head = []
        for headers in soup.table.thead.find_all('th'):
            head.append(headers.text)
        # print(head)
        self.myData = pd.DataFrame(columns = head)

        for j in soup.table.tbody.find_all('tr'):

            row_data = j.find_all('td')
            Scraper.fill_rows(row_data,self.myData)

        self.myData.drop(['Potency_Sort_1', 'TE Code', 'RLD', 'Potency_Sort_2','RS'],axis=1,inplace=True)
        if len(self.myData)==0:
            self.final_df = None
        else:
            
            tr=soup.table.tbody.find_all('tr')
            list_of_df2=[]
            set_of_apn_links=set()
            for apn in tr:
                l=apn.find_all('a',{'id':'id'})
                for i in l:
                    set_of_apn_links.add(i['href'].split('#')[0])


            for link1 in set_of_apn_links:
                print(link1)
                new_url = self.base_url+link1
                soup2 = Scraper.connection(new_url)
                links=[]
                content = soup2.find('div',{'class':'ui-accordion ui-widget ui-helper-reset'})
                for l_1 in content.find_all('div'):
                    for c in l_1.find_all('a'):
                        links.append(c['href'])
                
                header2=[]
                list_of_df1 = []
                for link in links:
                    new_url2 = self.base_url+link
                    soup3=Scraper.connection(new_url2)

                    for head1 in soup3.table.thead.find_all('th'):
                        header2.append(head1.text)
                    df2 = pd.DataFrame(columns = header2)
                    header2.clear()

                    for j1 in soup3.table.tbody.find_all('tr'):
                        row_data = j1.find_all('td')
                        Scraper.fill_rows(row_data,df2)
                    list_of_df1.append(df2)

                df2=pd.concat(list_of_df1,ignore_index=True)
                list_of_df2.append(df2)
            df3=pd.concat(list_of_df2,ignore_index=True)
            df3.drop(['Drug Substance','Drug Product','Patent Use Code','Delist Requested'],axis=1,inplace=True)
            final_df_list = []
            for prod_no in self.myData['Product Number']: 
                df3_temp=df3[df3['Product No']==prod_no]
                mydata_temp=self.myData[self.myData['Product Number']==prod_no]

                f_df = pd.merge(mydata_temp,df3_temp,how='cross')
                f_df=f_df.T.drop_duplicates().T
                final_df_list.append(f_df)
            self.final_df = pd.concat(final_df_list,ignore_index=True)
    


    def list_of_product(prod_list):
        """It takes the list of products as a list and pass it to the the Scraper class constructor 
        and get the data for each product available in the list
        and save it to a new list of dataframes """
        prod_df_list = []
        for prod in prod_list:  
            obj1=Scraper(prod)
            obj1=obj1.final_df
            prod_df_list.append(obj1)
        
        return prod_df_list

    def connection(url):
            """takes a url as a argument , create connection with the url and return the Parsed document"""
            res = requests.get(url)
            soup=BeautifulSoup(res.text,'html.parser')
            return soup
    
    def fill_rows(rows,df):
        """this method fills the rows of the table """
        row = [i.text for i in rows]
        row =[r.replace("\n","") for r in row]
        df.loc[len(df)] = row


