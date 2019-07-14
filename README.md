# Analysis Log

analysislog.py is Python code that will allow you to query a Postgresql database in order to find out the following:

    1. The top three articles
    2. The most popular authors
    3. Error percentage rates by days 

## Installation:
In order to run the code it is recommended to run it on a Linux based virtual machine. 

If you're a windows user, utilize [Gitbash](https://git-scm.com/downloads) and run it. Once that is up and running, make sure to run Vagrant using the command `vagrant up`. This installs an Ubunto virtual machine, that way you can run SQL data using the analysislog.py file. Once installed, run the command `vagrant ssh` which begin virtual machine. 

Useful commands that can be used to run the analysislog.py file are `python analysislog.py` which runs the file. You can also use the virtual machine to run the sql file like so: `psql -d news` which brings you into the database. You can then run drop table commands, which allow you to view the contents of certain tables. `\dt log` will show you the log table in the newsdata sql file along with the data type of each column and name. 

Before running the code in analysislog.py file, there is an important aspect that must be explained. The SQL queries used contain *views* (virtual tables that are a result of a SQL query). These views must be loaded onto the database before running the Python file. Each view can be found in the latter section of this README file. **Please load these views before running the file.**

## Usage
###### Purpose
The purpose of the analysislog.py is to query the database for three different reasons. The first is to locate the the top three articles based on the amount of views they've gathered. The second is a list of the most popular authors. The third is the date in which there were more than 1% of errors per http request. 

The code utilizes three different methods: 

    -search_top_three_articles()
    -search_top_authors()
    -search_error_request_rate()

Each of these methods utilizes variables that have stored SQL queries. These variables can have their SQL queries edited without making any changes to the code in the methods. 


###### SQL Views Overview
An important aspect of the SQL queries is that they use views. A list of these views can be found in the last section of this README file. 

**Please load these views before running the file.**

The views can be loaded by typing it into the command line virtual machine starting with the keyword `CREATE VIEW` or simply copy and paste each view individually, starting from `CREATE VIEW` all the way to the semi colon. 

Below is what you might see on screen when you're about to type in the view query.

`news => CREATE VIEW path_count AS SELECT COUNT(path) FROM log GROUP BY path ORDER BY path_count DESC;`

Hit the enter key, or return key, and your command line should notify you once the table has been created. Below is a sample of what you should see.

`CREATE VIEW`

This mean that the view has been created.

Please consult the [Postgresql](https://www.postgresql.org/docs/9.2/sql-createview.html) documentation for more details on creating views or deleting them. 

###### Psycopg Overview
The entirety of the backend code has been written in Python using the database adapter **Psycopg**. This is a database adapter that allows you to use Python to connect to a database and query it. Below is a sample of how you might connect to a database. 

    db = psycopg2.connect("dbname=news")
    cursor=db.cursor()
    cursor.execute(sqlquery1)
    results=cursor.fetchall()

    cursor.close()
    db.close() `

As can be seen above, the variable `db` holds the object that allows you access to the database (in this code the database is called *news*).

`cursor=db.cursor()` is creating a cursor object. This cursor is responsible for running through the database, similar to the cursor that can run through your text when you're typing in a text file.

`cursor.execute(sqlquery1)` is *executing* the query that is inside the variable `sqlquery1` using the `execute()` method provided by connecting to the database via the `db` variable found in `cursor`. 

`results=cursor.fetchall()` is using the `fetchall()` method provided by the `db` variable that is connected to the database, and stored into `cursor`, to fetch the results from the SQL query in the variable `sqlquery1` and holding it in a variable called `results`. 

From here the results can be printed using Python's `print()` method, formatted, or run through a for loop. 

`cursor.close()` and `db.close()` closes down the connection to the cursor and to the database.

This brief explanation should allow you to read and comprehend what is happening when you run the file.

Happy coding.

## Views

#### path_count
`CREATE VIEW path_count AS SELECT COUNT(path) FROM log GROUP BY path ORDER BY path_count DESC;`

#### article_views
`CREATE VIEW article_views AS
SELECT title, count(*) AS count_path, path  FROM articles, log WHERE log.path = concat('/article/', articles.slug) GROUP BY log.path, articles.title  ORDER BY count_path DESC;`

#### authors_articles
`CREATE VIEW authors_articles AS
SELECT author, name, title, authors.id FROM articles, authors WHERE articles.author = authors.id GROUP BY authors.name, articles.title, articles.author, authors.id ORDER BY articles.author;`

#### authors_title_count

`CREATE VIEW authors_title_count AS
select name, count(title) as article_title_count from authors_articles group by name;`

#### authors_views 

`CREATE VIEW authors_views AS
select authors_articles.name, article_views.count_path FROM authors_articles, article_views WHERE authors_articles.title = article_views.title GROUP BY article_views.count_path, authors_articles.name;`

#### error_404

`CREATE VIEW error_404 AS
SELECT to_char(time,'MONTH:DD') AS error_day_time, count(time) as error_time_count, status FROM log WHERE status <> '200 OK' GROUP BY error_day_time, status ORDER BY error_time_count DESC; `

#### total_requests

`CREATE VIEW total_requests AS
SELECT to_char(time,'MONTH:DD') AS day_time, count(time) AS time_count FROM log GROUP BY day_time ORDER BY time_count DESC;`
