import psycopg2


#sqlquery queries for the top article
sqlquery1 = "SELECT title, count(*) AS count_path, path  FROM articles, log WHERE log.path = concat('/article/', articles.slug) GROUP BY log.path, articles.title  ORDER BY count_path DESC LIMIT 3;"

#sqlquery2 queries for the top authors
sqlquery2 = "SELECT name, SUM(authors_views.count_path) FROM authors_views GROUP BY authors_views.name ORDER BY SUM(authors_views.count_path) DESC;"

#sqlquery3 queries for the errors
sqlquery3 = "SELECT total_requests.day_time, (error_404.error_time_count * 100.00/ total_requests.time_count) AS err_perc FROM error_404, total_requests WHERE error_404.error_day_time = total_requests.day_time GROUP BY error_404.error_time_count, total_requests.time_count, total_requests.day_time ORDER BY err_perc DESC limit 1;"
    

def search_top_three_articles():
    """This method searches for the top three articles"""
    db = psycopg2.connect("dbname=news")
    cursor=db.cursor()
    cursor.execute(sqlquery1)
    results=cursor.fetchall()
    print("\n\033[4mThe top three articles:\033[0m \n")
    #this for loop iterates through the lists provided by 
    for result in results:
        title = str(result[0])
        views = str(result[1])
        #formatted output   
        print(title + " - " + views + "\n" )    
    cursor.close()
    db.close() 

def search_top_authors():
    """This method searches for the authors that have get more page views"""
    db = psycopg2.connect('dbname=news')
    cursor = db.cursor()
    cursor.execute(sqlquery2)
    results = cursor.fetchall()
    print("\033[4mThe most popular authors:\033[0m \n")
    for result in results:
        author = str(result[0])
        views = str(result[1])
        #formatted output   
        print(author + " - " + views + "\n" ) 
    cursor.close()
    db.close()

def search_error_request_rate():
    """ This method searches and posts the day(s) in which there was more than 1% of GET requests leading to errors"""
    #method field contains all the "GET" keywords
    #there are 167735 rows
    db = psycopg2.connect('dbname=news')
    cursor = db.cursor()
    cursor.execute(sqlquery3)
    results = cursor.fetchall()
    print("\n\033[4mDays of Error greater than 1%:\033[0m \n")
    for result in results:
        day = str(result[0])
        err = str(result[1])
        print(day + " - " + err + "\n")

search_top_three_articles()
search_top_authors()
search_error_request_rate()