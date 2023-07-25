# Web-Scraping-the-US-FDA-Website-Data
This Project is Created using Python and it's libraries for scraping the data from the US FDA website.
for working with the project there should be Python 3 installed on the machine
When the user starts working with the projects , first of all the main page pops up to the screen . Shown in the image(1).There are mutiple functionalities in the main page. Let us Suppose a user have a product name and he wants to download the details of that product. So the user will have to enter the the product name to the entry field. Now there are two buttons we see on the page , first one is Download Data Button and the second one is View Data Button
![Screenshot 1](https://github.com/gour23/Web-Scraping-the-US-FDA-Website-Data/assets/91954903/768fdabb-744a-45e5-8b42-b1611dfa1596)


When the user clicks on the Download Data Button. There are some conditions checked first, like if the button is clicked with less than 3 character in the entry field or with a empty entry field, a warning  message pops up to the screen which says that there should be more than 3 character of a product name. And if the entered product name is more than 3 characters than it is been checked that whether the data is available or not on the website. if the data is not available a message pops up to the screen saying that there is no data available, and if the data  is available than a new window pops up for choosing the path for  where to save the downloaded data, Shown in the image(2). After choosing the path for saving data downloading process gets started and it takes some time to process and ends with the message to the screen saying that the data is downloaded. 

![Screenshot 2](https://github.com/gour23/Web-Scraping-the-US-FDA-Website-Data/assets/91954903/b6614f46-eb5a-46ed-a191-21d8dfb2d292)


On the other hand , when the user clicks on the View Data Button. The backend process gets started , different conditions for data is available or not are checked . If the data is available  the data for the given product name is fetched from the website and a new page pops up with a table containig different details of the product like approval date , expiry date , strength of the product etc. Image(3) shows the data fetched for a product here user can also download the data which is in the table. 
![Screenshot 3](https://github.com/gour23/Web-Scraping-the-US-FDA-Website-Data/assets/91954903/29e8c406-122c-4171-9ecc-5d2fb7b15968)


There is another Multiple Product Button on the main page which redirect to the next page , where we can download the multiple product’s data at a time. In Image(4) next page is shown. 
![Screenshot 4](https://github.com/gour23/Web-Scraping-the-US-FDA-Website-Data/assets/91954903/d1cf3e78-0418-44d7-bdf5-e3fce7a4ab8c)

Here in this page , there are two fields one for entering multiple products name manually and other one is for uploading the list of  products from the internal memory. 

In the backend process when working with the multiple products, each product is being checked whether it has data available on the FDA website or not. 

If the data is not available on the website for a product , that product is saved to a list and returned to the log file  

If the data is available on the website , Each product data is downloaded and saved as a CSV file format. And the time for the entire process is calculated. 
