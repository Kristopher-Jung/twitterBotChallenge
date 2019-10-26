from setup import *

class inputHandler:
    def __init__(self, userInput, userId):
        self.userInput = userInput
        self.userId = userId
        self.profile = None
        self.q_id = None
        self.isNew = self.initiate_handler()


    def getProfile(self):
        try:
            query = "SELECT * FROM profile WHERE user_id = '{}';".format(self.userId)
            cursor.execute(query)
            self.profile = cursor.fetchone()
            return True
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching profile data(inputHandler.profile)", error)
            return False

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

    def recordAndResponse(self):
        if self.profile and self.userId and self.userInput and self.q_id:
            #new user
            if self.isNew:
                try:
                    q_id = self.q_id
                    query = "SELECT content FROM question WHERE q_id={}".format(q_id)
                    cursor.execute(query)
                    curr_q = cursor.fetchone()[0]

                    insert_query = "INSERT INTO answer (responses, user_id) VALUES (ARRAY[]::TEXT[], '{}');".format(self.userId)
                    cursor.execute(insert_query)
                    conn.commit()

                    response = "==INITIATING GM'S TWITTER INTERVIEW!==\nWelcome {} !\nThis interview is consists of 6 questions.\nYour answers will be recorded CONFIDENTIALLY.\nANSWER THE QUESTION WITH @TAG:\n{}).{}".format(self.userId, self.q_id, curr_q)
                    print(response)
                    return response
                except (Exception, psycopg2.Error) as error:
                    print("Error while parsing input(inputHandler.recordAndResponse.isNew)", error)

            #record
            else:
                try:
                    new_q_id = self.q_id + 1
                    max_query = "SELECT MAX(q_id) FROM question;"
                    cursor.execute(max_query)

                    max = int(cursor.fetchone()[0])
                    if new_q_id > max:
                        response = "YOU HAVE COMPLETED ALL INTERVIEW QUESTIONS!\nTHANK YOU SO MUCH! {}.".format(self.userId)
                        print(response)
                        return response
                    else:
                        curr_array_query = "SELECT responses FROM answer WHERE user_id = '{}';".format(self.userId)
                        cursor.execute(curr_array_query)
                        curr_fetch = cursor.fetchone()
                        if not curr_fetch:
                            curr_array = []
                        else:
                            curr_array = curr_fetch[0]
                        length = len(curr_array)
                        insert_query = "UPDATE answer SET responses[{}] = '{}' WHERE user_id = '{}'".format(length+1, self.userInput, self.userId)
                        cursor.execute(insert_query)
                        conn.commit()

                        curr_array_query = "SELECT content FROM question WHERE q_id = '{}';".format(new_q_id)
                        cursor.execute(curr_array_query)
                        next_question = cursor.fetchone()[0]


                        insert_query = "UPDATE profile SET q_id = {} WHERE user_id = '{}'".format(new_q_id, self.userId)
                        cursor.execute(insert_query)
                        conn.commit()

                        response = "THANKS!\nYour answer for Question {} has been recorded!\nNOW, ANSWER THE FOLLOWING QUESTION:\n{}).{}".format(self.q_id, new_q_id, next_question)
                        print(response)
                        return response


                except (Exception, psycopg2.Error) as error:
                    print("Error while parsing input(inputHandler.recordAndResponse.record)", error)






if __name__ == '__main__':
    inputHandler = inputHandler("540-553-238z",'KristopherJung2')
    inputHandler.recordAndResponse()