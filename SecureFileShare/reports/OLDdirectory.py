dirStruct = {"John": ["topFolder", ["directory", "File:MyNameIsJohn.txt", ["newFolder"]], ["suchFolderVeryEmpty"]], "Jack":["emptyFolder"], "Kai":["root"]}

def load_directory_database():
    import psycopg2
    import csv

    #  @C:\Program Files\PostgreSQL\9.5\pg_env.bat

    PG_USER = "postgres"
    PG_USER_PASS = "coffee"
    PG_DATABASE = "course1"
    PG_HOST_INFO = ""  # " host=/tmp/" # use "" for OS X or Windows

    # Connect to an existing database
    conn = psycopg2.connect("dbname=" + PG_DATABASE + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    print("** Connected to database.")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table, but first removes it if it's there already
    # cur.execute("DROP TABLE IF EXISTS test;")
    # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    # print("** Created table.")

    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    with open(csv_filename, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # print(row)
            cur.execute("INSERT INTO " + db_name + " (deptID, courseNum,"
                        "semester, meetingType, seatsTaken, seatsOffered, instructor) "
                        "VALUES (%s, %s, %s, %s,%s, %s, %s)", tuple(row))
            # print("** Executed SQL INSERTS into database.")

    # Query the database and obtain data as Python objects
    cur.execute("SELECT * FROM coursedata;")
    print("** Output from SQL SELECT: ", cur.fetchall())

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    print("** Closed connection and database.  Bye!.")

def getDirectoryTree(name):
	if type(name) is not str:
		return "NotAString"
	if name in dirStruct.keys():
		return dirStruct[name]
	return "NoSuchName"

def displayTree(name):
	#assert type(name) is str
	dir = getDirectoryTree(name)
	if type(dir) is str:
		print(dir)
		return
	dispTreeHelp(dir, 1);

def dispTreeHelp(dir, level):
	print("  "*level, end='')
	print ("Directory:", dir[0]);
	for val in dir[1:]:
		#if type(val) is str:
		#	print(val)
		if type(val) is str:
			print("  "*level, end='  ')
			print (val);
		else:
			dispTreeHelp(val, level+1)
		
def addFile(name, path):
	dir = getDirectoryTree(name)
	if type(dir) is str:
		print(dir)
		return
	path = path.split("/")
	while path != []:
		print(path)
		cur = path[0]
		path = path[1:]

if __name__ == "__main__":
	print("invalid directory:", getDirectoryTree({}))
	print("hi's directory:", getDirectoryTree("hi"))
	print("John's directory:", getDirectoryTree("John"))
	print("Jack's directory:", getDirectoryTree("Jack"))
	
	print("\nDISPLAYED NICELY")
	print("===hi's directory:")
	displayTree("hi")
	print("===John's directory:")
	displayTree("John")
	print("===Jack's directory:")
	displayTree("Jack")
	
	#addFile("John", "topFolder/directory/MyNameIsJohn.txt")