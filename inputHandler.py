from setup import *
"""
    inputHandler class.
    input: userInput, userId.
    
    This class is parsing userInput and Id, determining what is the next step for the interview bot.
    recordAndResponse method should return the bot's answer as a string.
"""
class inputHandler:
    # Constructor.
    def __init__(self, userInput, userId):
        self.userInput = userInput
        self.userId = userId
        self.profile = None
        self.q_id = None
        self.isNew = self.initiate_handler()


    # Get profile of a user given user_id.
    # If user_id exists in the database, fetch the information.
    # print error and return false otherwise.
    def getProfile(self):
        try:
            query = "SELECT * FROM profile WHERE user_id = '{}';".format(self.userId)
            cursor.execute(query)
            self.profile = cursor.fetchone()
            return True
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching profile data(inputHandler.profile)", error)
            return False

    # Initiating and processing necessary information
    # if user profile exists, save the information to this object.
    # otherwise, create a new profile for the new user.
    # return True if the given user_id is a new user.
    # return False if the given user_id is not a new user.
    def initiate_handler(self):
        try:
            self.getProfile()
            if not self.profile:
                query = "INSERT INTO profile VALUES('{}', 1)".format(self.userId)
                cursor.execute(query)
                conn.commit()
                self.q_id = 1
                self.getProfile()
                return True
            else:
                self.q_id = int(self.profile[1])
                return False
        except (Exception, psycopg2.Error) as error:
            print("Error while parsing input(inputHandler.initiate_handler)", error)


    # Record and response should record user given information to database and return a next question for the user.
    def recordAndResponse(self):
        # if user record successfully found or successfully created.
        if self.profile and self.userId and self.userInput and self.q_id:
            #new user
            if self.isNew:
                try:
                    # get first question from the database
                    q_id = self.q_id
                    query = "SELECT content FROM question WHERE q_id={}".format(q_id)
                    cursor.execute(query)
                    curr_q = cursor.fetchone()[0]

                    # inserting user response.
                    insert_query = "INSERT INTO answer (responses, user_id) VALUES (ARRAY[]::TEXT[], '{}');".format(self.userId)
                    cursor.execute(insert_query)
                    conn.commit()

                    #generating bot's response.
                    response = "INITIATING GM'S TWITTER INTERVIEW!\nWelcome {} !\nThis interview is consists of 6 Qs.\nYour answers will be recorded.\nANSWER THE QUESTIONs WITH @FakeInterviewGM:\n{}).{}".format(self.userId, self.q_id, curr_q)

                    #for debugging purpose.
                    print(response)
                    return response
                except (Exception, psycopg2.Error) as error:
                    print("Error while parsing input(inputHandler.recordAndResponse.isNew)", error)

            #record exists. not a new user.
            else:
                try:
                    #get a next question from the database.
                    new_q_id = self.q_id + 1
                    max_query = "SELECT MAX(q_id) FROM question;"
                    cursor.execute(max_query)

                    #bound checking.
                    max = int(cursor.fetchone()[0])

                    #if user completed all questions available in the database.
                    if new_q_id > max:
                        #user has completed all interview questions.
                        response = "YOU HAVE COMPLETED ALL INTERVIEW QUESTIONS!\nTHANK YOU SO MUCH! {}.".format(self.userId)
                        #debugging purpose.
                        print(response)
                        return response
                    else:
                        #get accumulated user responses from the database,
                        curr_array_query = "SELECT responses FROM answer WHERE user_id = '{}';".format(self.userId)
                        cursor.execute(curr_array_query)
                        curr_fetch = cursor.fetchone()
                        #check if there was a previous responses. if not, create a new one. Otherwise, return current.
                        if not curr_fetch:
                            curr_array = []
                        else:
                            curr_array = curr_fetch[0]
                        length = len(curr_array)
                        #add a new response to the array.
                        insert_query = "UPDATE answer SET responses[{}] = '{}' WHERE user_id = '{}'".format(length+1, self.userInput, self.userId)
                        cursor.execute(insert_query)
                        conn.commit()

                        #get a new question
                        curr_array_query = "SELECT content FROM question WHERE q_id = '{}';".format(new_q_id)
                        cursor.execute(curr_array_query)
                        next_question = cursor.fetchone()[0]

                        #update profile, tracking current question number we are looking at.
                        insert_query = "UPDATE profile SET q_id = {} WHERE user_id = '{}'".format(new_q_id, self.userId)
                        cursor.execute(insert_query)
                        conn.commit()

                        #generate response based on the information gathered.
                        response = "THANKS!\nYour answer for Question {} has been recorded!\nNOW, ANSWER THE FOLLOWING QUESTION:\n{}).{}".format(self.q_id, new_q_id, next_question)
                        print(response)
                        return response


                except (Exception, psycopg2.Error) as error:
                    print("Error while parsing input(inputHandler.recordAndResponse.record)", error)



#testing purpose.
if __name__ == '__main__':
    inputHandler = inputHandler("540-553-238z",'KristopherJung2')
    inputHandler.recordAndResponse()