import argparse

table_var_types = ['T','h','Pr','u','vr','s0']

def tableA17(search_var,known_var,known_value,units=True):
    """
    tableA17(search_var,known_var,known_value,units=0):
        Function accepts 3 required inputs and 1 optional input and uses it to return data
        from the "Ideal-gas properties of air" table (table A17) in "Thermodynamics: An
        Engineering Approach 8th Ed" 

        4 Inputs:
            search_var  - Must be in the set of ['T','h','Pr','u','vr','s0'].  It is the 
                          variable searched for in the table.  The corresonding value of
                          this variable is returned at the end of the function.

                          Ex. search_var = 'T' -> function returns Temp found based on 
                                                  remaining inputs

            known_var   - Must be in the set of ['T','h','Pr','u','vr','s0'].  It is the 
                          type of the value which will be searched for later (let me know
                          if you think of a better way to say that).

                          Ex. known_var = 'T' -> known_val is equal to the temperature at
                                                 the point the user is trying to find

            known_value - Must be a real number.  It is the known value which will be
                          searched for in the table.  It can be any value, if it is in
                          the middle of two points it will interpolate.

                          Ex. known_val = 200 -> If known_var = 'T' then it will look for
                                                 values in the first row of table A17

            units       - Is a boolean true or false for if units are in SI or English. 
                          True if units are SI, and False if units are English.  Default is
                          set to True, because SI units are better.

                          Ex. tableA17('h','T',200) -> Defaults to unit=True and SI units
                          Ex. tableA17('h','T',200,True) -> Defines unit=True and uses SI
                          Ex. tableA17('h','T',200,False) -> Defines unit=False and uses dumb units

    Stephen St. Raymond
    November 15, 2017
    """
    while search_var not in table_var_types: #in case anybody didn't bother to read the above instructions
        search_var = input('Unknown search_var, try again in [ T , h , Pr , u , vr , s0 ]: ')
    
    while known_var not in table_var_types: #you know it's gonna happen at some point
        known_var = input('Unknown known_var, try again in [ T , h , Pr , u , vr , s0 ]: ')
        
    if units: #Default is True, but also any integer that isn't zero will be read as 'True' by Python, so it's hard to mess up
        A17_text = open('thermo_A17.txt','r') #Opens text file and stores it
    else: #User can say False if they feel like using English units
        A17_text = open('thermo_A17E.txt','r') #Different file

    first_line = A17_text.readline() #Python stores the first line as a string in first_line
     
    A17_table = A17_text.readlines() #Python "reads" the rest of the lines, storing each one as a new element in the A17_table array

    for i in range(0,len(A17_table)): #i itterates from 0 to the last index of A17_table
        line_string = A17_table[i] #stores the string of line i of A17_table
        line_value_strings = line_string.split() #line_string is split from 1 string to 6 strings, one for each value in the row (T, h, Pr, u, vr, and s0)
        line_values = [] #initializes line_values as an empty array
        for value_string in line_value_strings: #value_string itterates through line_value_strings
            line_values.append(float(value_string)) #float() converts the values given to a float number type, then that value is appended to the line_value array
        A17_table[i] = line_values #Line number i of A17_table gets changed from one string of the values to an array of numbers

    error = [] #initiallize empty array
    reference_index = first_line.split().index(known_var) #establishing which unit we are looking for, to find the line
    value_index = first_line.split().index(search_var)
    for line in A17_table: #line itterates through each array in A17_table
        error_value = known_value - line[reference_index] #finds the difference between the known_value and each element number reference_index
        error.append(error_value) #appends that difference value to the error array
    
    abs_error = []
    for val in error:
        abs_error.append(abs(val))

    value_row_index = abs_error.index(min(abs_error))
    value_row = A17_table[value_row_index]
    vr_plus_1 = A17_table[value_row_index+1]
    vr_minus_1 = A17_table[value_row_index-1]

    error_value = error[value_row_index]
    
    catch = 0
    if error_value > 0 and value_row_index is not 0:
        y_a = value_row[value_index]
        y_b = vr_plus_1[value_index]
        x_a = value_row[reference_index]
        x_b = vr_plus_1[reference_index]
    elif error_value < 0 or value_row_index is 0:
        y_b = value_row[value_index]
        y_a = vr_minus_1[value_index]
        x_b = value_row[reference_index]
        x_a = vr_minus_1[reference_index]
    else:
        catch = 1
        value = value_row[value_index]
    
    if not catch:
        value = y_a + (y_b - y_a) * ((known_value - x_a) / (x_b - x_a))
    
    return value

def get_commandline_options():
    """
    All credit to Dr. Shackleford for this function.

    It takes the variables given in the command line and turns them into data
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-s','--search_var',
                        help = 'give the search_var, defined in the tableA17 function doc',
                        action='store',
                        type=str,
                        dest='search_var')

    parser.add_argument('-k','--known_var',
                        help = 'give the known_var, defined in the tableA17 function doc',
                        action='store',
                        type=str,
                        dest='known_var')

    parser.add_argument('-v','--known_value',
                        help = 'give the known_value, defined in the tableA17 function doc',
                        action='store',
                        type=float,
                        dest='known_value')

    parser.add_argument('-u','--unit',
                        help = 'set the units, defined in the tableA17 function doc',
                        action='store',
                        type=int,
                        dest='units',
                        default=1)

    opts = parser.parse_args()

    return opts

def main():
    opts = get_commandline_options()
    x = tableA17(opts.search_var,opts.known_var,opts.known_value,opts.units)
    print x

if __name__ == '__main__':
    main()
