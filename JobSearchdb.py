import mysql.connector
import pandas as pd

class JobSearchdb:
    """
    class JobSearchdb

    Object that integrates methods and attributes for  easier handling
    of the database with job applications.

    Input:
        path_to_config: str - path to a file containing  credentials needed
        to establish connection with the mysql db
    """
    
    def __init__(self,path_to_config,test_mode=False):
        self.path_to_config = path_to_config
        self.connection = mysql.connector.connect()
        self.test = test_mode
        self.__main_table = "MyJobApplications" 
        self.__test_table = "TestTable"
        print(">>> Jobsearch initiated! Remeber to establish connection with your db")
        if self.test:
            print(">>> Run in the test mode")

    def establish_connection(self):
        """
        Function to establish connection with mysql db
        using config stored in a text file

        RETURNS connection
        """

        def get_connection_config():
            """
            Creates a dictionary from the config file
            """
            with open(self.path_to_config,'r') as file:
                content= file.readlines()
            # Funcs used for more redable dict comprehension
            def get_value(line):
                return line.split(":")[1].split("\n")[0].split(" ")[1]
            def get_key(line):
                return line.split(":")[0]

            return {get_key(line) : get_value(line) for line in content }

        connection_config = get_connection_config()
        conn = mysql.connector.connect(
            host=connection_config["host"],
            user=connection_config["user"],
            password=connection_config["password"],
            database = connection_config["database"]
            )

        print(f"> Connection established with {connection_config['database']}")
        self.connection = conn 

    def query(self, query_str):
        """
        Build-in function enabling  quering a fetched db by passing a query
        as a string

        Input:
            query_str: str - string containing valid SQL query
        RETURN:
            list
        """
        cursor = self.connection.cursor()
        cursor.execute(query_str)
        rows = cursor.fetchall()
        cursor.close()
        return(rows)

    def show_all(self):
        """
        Show all of jobs application in a MyJobApplications table
        """
        if self.test:
            table_to_show = self.__test_table
        else:
            table_to_show = self.__main_table
        print(f">>> Currently displaying {table_to_show} table")
        return self.query(f"SELECT * FROM {table_to_show};")
    
    def create_df(self ):
        """
        Creates a pandas.DataFrame object from the db.

        RETURNS: pandas.DataFrame
        """

        if self.test:
            table = self.__test_table
            print(">>> Using test table")
        else:
            table = self.__main_table
            print(">>> Using MyJobApplications")

        query = f"SELECT * FROM {table}"
        return pd.read_sql(query, self.connection)

    def commit_to_db(self):
        self.connection.commit()
        print(">>> Commited to the database")
        
    def add_new_application(self,application_dict):
        """
        Fast adding of a new application
        """

        labels = [
            "Applications submitted","Replied",
            "Rejected before interview","No reply",
            "Initial interviews","Replied Too Late",
            "Task required/Technical interview scheduled",
            "No task/technical interview required",
            "Rejected by me","Rejected after the first interview",
            "Final interview","No additional interview",
            "Offer Received","Rejected Before Offer",
            "Accepted","Rejected"
        ]

        hierar_labels_dict = {label : num+1 for num,label in enumerate(labels)}

        # The block belowe handles multiple scenario that can occure while
        # adding a new application to the db.

        try:
            # In case  there is no valid key iin the dictionary, a prompt is displayed
            # with avaible options to chose from 
            if not application_dict['ApplicationStatus'] in labels:
                wrong_status = True
                while wrong_status:
                    print("""
                        > Wrong Application status passed!
                        > You have to chose from following:
                        """)
                    # Lists avaible options
                    for num , label in enumerate(labels):
                        print(f"{num+1} : {label}")
                    print("---------------")
                    choice = int(input("Provide a number (1-16)"))
                    if choice > 0 and choice <17:
                        wrong_status=False
                        application_dict['ApplicationStatus'] = choice
            else:
                # In case the pass value is an actuall key, its translated
                # to int that is coherent with the database.
                application_dict['ApplicationStatus'] = hierar_labels_dict[application_dict['ApplicationStatus']]
        except KeyError:
            # In case there is no key in provided dictionary
            # the value is set to 1, which represents 'Submitted'
            application_dict['ApplicationStatus'] = 1
            print("Default status added")

        # Creating  a query string
        avaible_keys = list(application_dict.keys())
        colums_values = list(map(lambda x:(x,f"%({x})s"),avaible_keys))
        columns_str= ", ".join([tup[0] for tup in colums_values])
        values_str = ", ".join([tup[1] for tup in colums_values])
        query =f"INSERT INTO {self.__test_table} ({columns_str}) VALUES ({values_str})"

        # Query execution
        cursor = self.connection.cursor()
        cursor.execute(query, application_dict)
        cursor.close()

        # After that stage a query is not fetched to mysql db
        # to do it a commit() method needs to be executed
        print(">>> Remember to commit your changes to the db") 
