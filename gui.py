import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
from tkinter.filedialog import asksaveasfilename
from tkinter import filedialog
import pandas as pd
from main import Scraper
import time
import logging
class Gui :
    def __init__(self,win):        
        self.win = win
        self.win.state("zoomed")
        self.win.resizable(width=False,height= False)
        self.win.config(bg="black")
        self.win.title('fetching data from FDA website')

    def main_screen(self):
        """ All main Screen Functionalities are defined here..."""
        frame = Frame(self.win,width=1350,height=1000,bg="black")
        frame.pack()
        
        title = Label(frame,text="SCRAP THE US FDA PRODUCT'S DATA",font="Helvetica 25 bold",fg="white",bg="black")
        title.place(relx=.25,rely=.1)
        
        
        product_name = Label(frame,text="Enter the Product Name :",font="Helvetica 20 bold",fg="brown",bg="black")
        product_name.place(relx=.2,rely=.3)
        product_name_entry = Entry(frame,font="Helvetica 20 bold",bd=3)
        product_name_entry.place(relx=.5,rely=.3)

        def get_data():
            """This method fetch the values(product name) from entry widget and pass it to Scrapper Class 
            also returns the fetched data as a dataframe"""

            global p_name
            p_name=product_name_entry.get()
            if len(p_name)<3:
                messagebox.showerror("error","Name can not be Empty,Should be atleast 3 characters")
                
            else:
                df_obj = Scraper(p_name)
                global df_final
                df_final = df_obj.final_df
                return df_final

        def go_download_page():
            """ this method checks if product has data or not  , if yes then it sends data to download method
            """

            get_data()
            if len(p_name)<3:
                pass
            elif df_final is None:
                messagebox.showwarning("warning",f"No Data For {p_name}")
            else:
                frame.destroy()
                Gui.download(self)

        def go_to_view_page():
            """After checking whether data is available or not , if yes then sends data to view page"""
            get_data()
            if len(p_name)<3:
                pass
            elif df_final is None:
                messagebox.showwarning("warning",f"No Data For {p_name}")
            else:
                frame.destroy()
                Gui.view(self)

        def multiple_prod():
            """jump to next page for downloading multiple products"""
            frame.destroy()
            Gui.down_list_prod(self)

        download_button = Button(frame,text='Download Data',command=go_download_page,bg="blue",fg="white",width=23,height=2).place(relx=.3,rely=.4)
        view_button = Button(frame,text='View Data',command=go_to_view_page,bg="blue",fg="white",width=23,height=2).place(relx=.5,rely=.4)
        
        nxt_lable = Label(frame,text="Have List of Products ?  click Here:",font="Helvetica 20 bold",fg="white",bg="black").place(relx=.28,rely=.60)
        multiple_download = Button(frame,text='Multiple Products',command=multiple_prod,bg="blue",fg="white",width=30,height=2).place(relx=.39,rely=.7)

    def download(self):
        """This method saves the data to choosen path by user"""
        data = [("csv file(*.csv)","*.csv")]
        file = asksaveasfilename(filetypes = data, defaultextension = data)
        with open(file,"w") as f:
            f.write(df_final.to_csv())
        messagebox.showinfo("title","file downloaded..")
        Gui.main_screen(self)

    def view(self):
        """This method creates the new page and show fetched data in the table format"""
        frame1 = Frame(self.win,width=1350,height=1000,bg="black")
        frame1.pack()
        
        columns=list(df_final.columns)
        scrollbar = Scrollbar(frame1,orient='vertical')
        scrollbar.pack(side='right',fill=Y)

        scrollbar1 = Scrollbar(frame1,orient='horizontal')
        scrollbar1.pack(side='bottom' , fill=X)

        tree = ttk.Treeview(frame1,yscrollcommand=scrollbar.set,xscrollcommand=scrollbar1.set, columns=columns,show='headings',height=30 )
        for i in columns:
            tree.heading(i,text=f"{i}")
            tree.column(i,width=160)
        
        contacts = df_final.to_numpy().tolist()
        for contact in contacts:
            tree.insert('', tk.END, values=contact)

        tree.pack(side=TOP,anchor='w')

        scrollbar.config(command=tree.yview)

        scrollbar1.config(command=tree.xview)

        def download_data():
            """Opens download window for save the data"""
            frame1.destroy()
            Gui.download(self)
        
        def back():
            """Go back to previous page"""
            frame1.destroy()
            Gui.main_screen(self)


        download_button = Button(frame1,text='Download Data',command=download_data,bg="blue",fg="white",width=23,height=2).pack(side='bottom',anchor='c')
        back_button = Button(frame1,text='Home Page',command=back,bg="blue",fg="white",width=23,height=2).pack(side='bottom',anchor='c')
        


    def down_list_prod(self):
        """This method creates a new page for  downloading multiple products or list of products """

        logging.basicConfig(filename="products.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
        
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        frame1 = Frame(self.win,width=1350,height=1000,bg="black")
        frame1.pack()

        title = Label(frame1,text="Download Multiple Products",font="Helvetica 25 bold",fg="white",bg="black")
        title.place(relx=.3,rely=.1)

        list_lable = Label(frame1,text="Enter the Multiple Products :",font="Helvetica 20 bold",fg="brown",bg="black")
        list_lable.place(relx=.2,rely=.25)
        
        list_entry = Entry(frame1,font="Helvetica 20 bold",bd=3)
        list_entry.place(relx=.5,rely=.25)
        text_labl = Label(frame1,text="Products Entered Should be Seprated by  ' , ' ",font="Helvetica 12 bold",fg="white",bg="black")
        text_labl.place(relx=.48,rely=.3)
        

        def back():
            """Go back to previous page"""
            frame1.destroy()
            Gui.main_screen(self)

        def down_list():
            """This method is defined to take input of multiple products as a list and pass this list to 
               to the method list_of_product() of the class Scraper , if the data is available this method 
                download the data of all products seprately and saves them to the csv file
                 it also save those productsin the log file which have no data available """
            t=time.time()
            no_data_list = []
            p_name_list = list_entry.get()
            p_name_list=p_name_list.split(',')
            list_df = Scraper.list_of_product(p_name_list)
            # Gui.pBar(frame1,p_name_list)
            l = list(zip(p_name_list,list_df))
            # print(list_df)
            file = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Video")

            for prod , df in l:
                if len(prod)<3:
                    messagebox.showwarning("Warning",f"Enter Atleast 3 characters , {prod}")
                elif df is None:
                    no_data_list.append(prod)
                else:

                    ext = f"/{prod}.csv"
                    path = file+ext
                    df.to_csv(path)
            e=time.time()
            logger.info(f"\n The Website  have no data available for these products \n {no_data_list} \n and time total time taken {e-t} Seconds")
            

            messagebox.showinfo("Successful","Downloaded...")

        download_list = Button(frame1,text='Download',command=down_list,bg="blue",fg="white",width=23,height=2).place(relx=.4,rely=.4)
        back_button1 = Button(frame1,text='Go Back',command=back,bg="blue",fg="white",width=23,height=2).place(relx=.6,rely=.4)


## Working With List in dropdown

        upload_labl = Label(frame1,text=" Upload the List of Products : ",font="Helvetica 20 bold",fg="brown",bg="black")
        upload_labl.place(relx=.2,rely=.55)
        self.n = tk.StringVar()
        combox = ttk.Combobox(frame1,state= "readonly", width = 42, textvariable = self.n)
        combox['values']=("text file","csv file","excel file")
        combox.current(1)
        combox.place(relx=.5,rely=.56)

        def search(): 
            """This method , first search for the list of products as a text/excel/csv file format
            after that upload that list and pass that list to the function of Scraper class 
            and returns the data Scrapped from the website through the function as csv files seprately
            it also save those productsin the log file which have no data available """
            t=time.time()
            no_data_list = []
            val=combox.get()
            if val == "text file" :
                file = filedialog.askopenfilename(filetypes=[("Text File",".txt")])
                df = pd.read_csv(file)
                p_list=list(df.iloc[0: ,-1])
            elif val=="csv file":
                file = filedialog.askopenfilename(filetypes=[("CSV File",".csv")])
                df = pd.read_csv(file)
                p_list=list(df.iloc[0: ,-1])
            else:
                file = filedialog.askopenfilename(filetypes=[("excel file",".xlsx"),("excel file",".xlsm"),("excel file",".xltx")])
                df = pd.read_excel(file)
                p_list=list(df.iloc[0: ,-1])
            # print("hii" ,l)
            messagebox.showinfo("Success","List is Uploaded , Select the Path where you want to save data...")
            file1 = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Download List of Products")
            p_list_df = Scraper.list_of_product(p_list)

            l= list(zip(p_list,p_list_df))
            for prod, df in l:
                if len(prod)<3:
                    messagebox.showwarning("Warning",f"Enter Atleast 3 characters , {prod}")
                elif df is None:
                    no_data_list.append(prod)
                else:

                    ext = f"/{prod}.csv"
                    path = file1+ext
                    df.to_csv(path)

            logger.info(f"The Website  have no data available for these products {no_data_list} /n hghdsgf ")
            print(no_data_list)
            e=time.time()
            logger.info(f"{e-t} Seconds")
            # print((e-t), "seconds")
            messagebox.showinfo("Successful","Downloaded...")

        search = Button(frame1,text='Upload & Download',command=search,bg="blue",fg="white",width=23,height=2).place(relx=.5,rely=.66)

if __name__=="__main__":
    win=Tk()
    obj=Gui(win)
    obj.main_screen()
    win.mainloop()