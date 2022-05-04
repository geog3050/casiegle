import hw2

#This sets the data using the import function used in hw2
participants = hw2.import_data('solution_test1.txt')


#this chunk of code checks the accuracy of the final function
#if the outcome does not equal the correct solution then the other functions can be tested with the functions below
if hw2.tournament(participants) != ['8', ' 2', ' 4', ' 4', ' 7', ' 5']
    print('There is something wrong with your function, or other functions')


#Function checks to see if the import function creates a list of 4 and if the correct objects are the right types
def import_tester(List):
    if type(List) == list:
        if len(List[0]) == 4:
            if type(List[0][2]) != float:
                if type(List[0][3]) != float:
                    return("Need to make correct objects the right types according to directions")
                else:
                    return("No Error")
        else:
            return("Incorrect")
    else:
        return ("Not a list")

    
import_tester(hw2.import_data('solution_test1.txt'))



#This function looks to see if all of the multipliers are correct given by the function, could look at every option to see if 
#other combinations go good together but it would be a lot so I just did one to confirm assuming the rest would work as well
def attack_tester():
    if hw.2attack_multiplier('Water', 'Fire') != 2.5:
        return ("incorrect")
    if hw.2attack_multiplier('Electric', 'Water') != 1.3:
        return ("incorrect")
    if hw2.attack_multiplier('Ground', 'Electric') != 2.0:
        return ("incorrect")
    if hw2.attack_multiplier('Fire', 'Grass') != 3.0:
        return ("incorrect")
    if hw2.attack_multiplier('Grass', 'Water') != 1.5:
        return ("incorrect")
    if hw2.attack_multiplier('Grass', 'Ground') != 1:
        return ("incorrect")


attack_tester()





def fight_tester():
    #This part checks to see if it returns a list using samples assuming the previous functions are working 
    if type(hw2.fight(participants[1], participants[2], 2)) != list:
        return ("Function does not return a list")
    
    #A lot of this function depends on previous functions so that is why I did not test for a lot here because the
    #main parts were tested before since I did not make certain indexes floats in the beginning in my submission
    #of assignment 2



fight_tester()


#if this is still not what you are looking for, let me know. I think I did it
#in a correct way or close with importing the functions and then being able to test
#some things if the final outcome does not match and is not accurate. The whole
#testing concept is brand new to me since in the BAIS program we just focus on coding
#with data and statistics so let me know what I can improve on. 
