import mysql.connector
import random

crnList = [31352]
namesList = ["Danny", "Jimmy", "Alex", "Ilana", "Eli", "Matt", "Barrett", "Meghan", "Izzy", "Drew",
                "Zach", "Nikhil", "Sydney", "Ethan", "Billy", "Brandon", "Rachel", "Markus", "Matthew",
                "Elizabeth", "Allison"]

majorList = ["Accounting", "Biology", "Business Administration", "Chemistry", "CS", "CS + Math", "CS + Statistics",
                "Economics", "Finance", "Microcellular Biology", "Music"]

yearList = ["Freshman", "Sophomore", "Junior", "Senior", "Masters"]

emailList = ["gmail.com", "yahoo.com", "illinois.edu"]

try:
    cnx = mysql.connector.connect(user='root', password='INSERTDBPASS',
                                  host='127.0.0.1',
                                  database='coursebuddy')
except Error as e:
    print("Connection Failed")

cursor = cnx.cursor(dictionary=True)

# Get random CRN's and add to crnList
query = ("SELECT CRN FROM sp19 ORDER BY RAND() LIMIT 4;")
cursor.execute(query)

result = cursor.fetchall()
print("RL:", len(result))

for i in range(0, len(result)):
    crn = result[i]['CRN']
    crnList.append(crn)

# Generate random combinations of data
query = ("CALL insertUserData(%s,%s,%s,%s,%s)") #CALL insertUserData("Username", "Major", "Email", "Year", CRN);
for i in range(0, 10):
    name = random.choice(namesList)
    major = random.choice(majorList)
    email = name + str(random.choice(range(1, 9))) +"@" + random.choice(emailList)
    year = random.choice(yearList)
    crn = random.choice(crnList)

    #add the data to the database
    args = (name, major, email, year, crn)
    cursor.execute(query, args)



cnx.commit()

cursor.close()
cnx.close()
