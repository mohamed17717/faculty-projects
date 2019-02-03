#!/usr/bin/env	python3
from string import ascii_lowercase as letters

class Operations:
    def AND(self, x,y):
        return x and y

    def OR(self, x,y):
        return x or y

    def NOT(self, x):
        return not x

    def XOR(self, x, y):
        return x != y

    def IF_THEN(self, x, y):
        return self.OR(  self.NOT(x), y )

    def BI (self, x, y):
        return x == y

class TruthTable(Operations):
    """ 
        Generate TruthTable for some logical operations 
        ** note that variables must be one symbol **
    """
    
    def __init__(self, logical_exp):
        self.logical_exp = logical_exp.lower().replace('<->', '_').replace('->', '>')
        self.variables = self.__get_vars()
        self.rows      = [list(row) for row in self.__intial_truth_table()]

    def __get_vars(self):
        """ get vars in the exp """

        ## clean exp
        ## 'v' is represent OR symbol
        ## remove repeated
        cleaned = ()
        for i in self.logical_exp:
            if i in letters and i != 'v' and i not in cleaned:
                cleaned += (i,)

        return cleaned

    def __intial_truth_table(self):
        """ to make intial truth table between the variables
            without execute any logical operation """

        num_of_vars = len(self.variables)

        ## this row will go throw the whole code
        ## and its clms data will changed accroding to law
        ## row_number % (2 ** (rows_number-clm_number) ) == 0
        lst  = [True] * num_of_vars
        
        rows = ()
        rows_number = 2 ** num_of_vars

        # num of what will produced
        for row_number in range(1, rows_number + 1):
            rows += (tuple(lst), )
            
            # change the clms
            # range start from 0 cus index is from 0
            # clm + 1 cus this accroding to law
            # last clm must be (1 -> 2^0)
            for clm in range(num_of_vars):
                ## get clm_number and fuck the index
                clm_number = clm + 1
                if row_number % ( 2**(num_of_vars - clm_number) ) == 0:
                    lst[clm] = not lst[clm] 
        return rows

    def output_in_table(self):
        """ print data in organized table """

        rows = self.rows

        ## to give row a number
        ## and save clms fully parallel
        ## first we need to know length of max number i will reach
        ## ex: 958 is 3 number ... 56 is 2 numbers etc
        mx_len_num = len(str(len(rows)))

        ## number of row intiate from 1
        num = 1

        ## first row contain vars name ##
        first_row = mx_len_num*' '+ '| ' + ' | '.join(['%5s'%str(variable) for variable in self.variables])
        print(first_row)
        ## print splitter between data and header
        print(len(first_row) * '-')

        clms_number = len(rows[0])
        for row in rows:
            ## to handle the tab
            ## first i wanna know length of current number
            len_num = len(str(num))
            ## then complete the difference between it and the max with spaces
            tab = ' ' * (mx_len_num - len_num)
            ## create the row_numbers in my format
            row_number = tab + str(num) + '| '
            
            ## produce the row
            ## in fully parallel format
            # ['%5s'%(str(elm)) for elm in row]
            row_data = []
            for index in range(clms_number):
                clm_length = max(len(self.variables[index]), 5)
                string_format = '%' + '%is' % clm_length
                row_data.append(string_format % row[index])

            row = row_number + ' | '.join(row_data) + ' |'
            print( row )

            ## increase the row number for the next loop
            num += 1

    ## i send logical_exp as variable cus it will be recursive function
    ## if i meet any data in brackets ()
    def __separate_logical_exp(self, logical_exp):
        """ variable symbol must be length == 1 """
        separated     = ()
        brackets      = []
        bracket_value = ''
        for elm in logical_exp:
            ## skip spaces
            if elm == ' ':
                continue

            ## recognize that u r in bracket
            elif elm == '(':
                ## if bracket inside bracket you cant ignore it
                if brackets:
                    bracket_value += '('
                brackets += [True]
            elif elm == ')':
                #print(self.logical_exp, logical_exp, brackets, bracket_value)
                brackets.pop()
                ## if i out of brackets then 
                # execute the inside the brackets recursion function
                if not brackets:
                    ## add the output as one elment
                    separated += ( self.__separate_logical_exp(bracket_value) ,)
                    ## elmpty the bracket value for new data
                    bracket_value = ''
                ## this bracket inside bracket
                ## you cant ignore it
                else:
                    bracket_value += ')'

            elif brackets:
                bracket_value += elm

            else:
                separated += (elm, )

        if len(separated) == 1 and len(logical_exp) > 2 and logical_exp[0]+logical_exp[-1] == '()':
            logical_exp = logical_exp[1:-1]
            separated   = self.__separate_logical_exp(logical_exp)
        
        return separated

    def sure_logical_exp_is_valid(self, logical_exp):
        separated = self.__separate_logical_exp(logical_exp)
        # print(separated)
        """ there are 2 rules to be true
            1 - not must be Preceded by op 
            2 - elm cant be Consecutive to other elm
            2 - all op cant be Consecutive by op but not
         """

        operators = ('^', 'v', '>', '_', '~')
        
        ## it will be 'op' for operator, 'vr' for var
        prev = '' 

        for elm in separated:
            ## get the type of element
            if elm in operators:
                elm_type = 'op'
            else:
                elm_type = 'vr'

            ## if this is first elm and this elm not a tuple
            ## if it is a tuple skip this if and i will handle tuple in next if
            if not prev and type(elm) != tuple:
                ## this first must be variable or not
                ## else this is wrong exp
                if elm_type == 'vr' or elm == '~':
                    prev = elm_type
                    continue
                else:
                    return False

            if type(elm) == tuple:
                new_logical_exp = str(elm)[1:-1].replace('\'','').replace(',', '').replace(' ', '')
                if not self.sure_logical_exp_is_valid(new_logical_exp):
                    return False

            ## if elm == not then prev must be operator
            ## otherwise no data cant be preceded by its type
            if elm == '~':
                if prev != 'op':
                    return False
            elif elm_type == prev:
                return False

            prev = elm_type

        return True
    
    def __tuple_to_string_exp(self, t):
        if type(t) in (list, tuple, set):
            return str(t).replace('\'', '').replace(', ', '')
        return t

    def __order_logical_exp(self, logical_exp):
        speparated = list(self.__separate_logical_exp(logical_exp))

        ## op NOT cus its behavior is different
        while speparated.count('~'):
            index = speparated.index('~')
            nxt   = speparated[index+1]

            if type(nxt) == tuple:
                nxt = self.__tuple_to_string_exp(nxt)
                self.__order_logical_exp(nxt)
            else:
                ## to fuck repeated -- but it in var
                if ('~' + nxt) not in self.variables:
                    self.variables += ('~' + nxt,)

            speparated.pop(index+1)
            speparated.pop(index)
            
            speparated.insert(index, '~'+ nxt)


        for op in ('^', 'v', '>', '_'):
            while speparated.count(op):
                index = speparated.index(op)
                nxt   = speparated[index+1]
                prv   = speparated[index-1]

                for i in (nxt, prv):
                    if type(i) == tuple:
                        new_logical_exp = self.__tuple_to_string_exp(i)
                        self.__order_logical_exp(new_logical_exp)
                        
                prv = self.__tuple_to_string_exp(prv)
                nxt = self.__tuple_to_string_exp(nxt)

                ## to fuck repeated -- but it in var
                if ('%s%s%s' % (prv, op, nxt)) not in self.variables:
                    self.variables += ('%s%s%s' % (prv, op, nxt),)

                speparated.pop(index+1)
                speparated.pop(index)
                speparated.pop(index-1)

                speparated.insert(index-1, '%s%s%s' % (prv, op, nxt))

    def __get_clms_relations(self):
        self.__order_logical_exp(self.logical_exp)
        ## to fuck repeated (editted) 
        # self.variables = list(set(self.variables))
        clms_names = list(self.variables)

        for index, clm_name in enumerate(clms_names):
            ## remove comment if you wanna only last relation
            # clms_names[index] = str(index)

            clms_on_right = clms_names[index+1:]
            for right_index, right_clm in enumerate(clms_on_right):
                if clm_name in right_clm:
                    clms_names[index+ right_index+1] = right_clm.replace(clm_name, str(index))
        
        clms_names = [i.replace('(', '').replace(')', '') for i in clms_names]

        return clms_names ## ['y', 'z', 'x', 'f', '1v3', '~0', '5v1', '2^6', '7>4']

    def __split_relation(self, elm):
        """
            this function cus numbers may be more than 1 digit and that will fuck my code
        """
        splitted = ()
        digits = '0123456789'
        container = ''
        for i in elm:
            if i in digits:
                container += i
            else:
                if container:
                    splitted += (container,)
                    container = ''

                splitted += (i, )
        if container:
            splitted += (container,)

        return splitted

    def __fill_clms(self):
        """ 
            - every clm is relation between 2 or 1 clm 
            - you cant fill clm before clm you must go in order

            solve
            -------
            - i wanna know the relation is between which clms
            - operation which in use (AND, OR, ....)
                * i will go throw all clms names and replace clm_name with its number
                * this method will get me indexes and op with very simple way
                * note that this a horrible algorithm for huge data
            - loop on indexes throw them to the functions get the new clm value
        """
        ## get clms relations
        relations = self.__get_clms_relations()
        # print(relations)
        
        ## to check that iam in range and avoid index out of range
        lenght_current_row = len(self.rows[0])

        for relation in relations:
            ## relation length will make it simple to solve
            ## relation will be like (1^3, 10v5 ....)
            relation = self.__split_relation(relation)
            length   = len(relation)

            ## this is not operation it just intial variables
            if length == 1:
                continue

            ## if there is only 2 elements in relation
            ## it must be not
            ## and sure that relational clm is inside row range
            elif length == 2 and relation[0] == '~' and int(relation[1]) <= lenght_current_row:
                relational_clm = int(relation[1])
                for row in self.rows:
                    row.append(self.NOT(row[relational_clm]))
                lenght_current_row += 1

            ## remove = this will cause error 
            elif length == 3 and relation[1] in ('^', 'v', '>', '_') and int(relation[0]) < lenght_current_row and int(relation[2]) < lenght_current_row:
                relational_clm1 = int(relation[0])
                relational_clm2 = int(relation[2])
                op = relation[1]

                if op == '^':
                    function = self.AND
                elif op == 'v':
                    function = self.OR
                elif op == '>':
                    function = self.IF_THEN
                elif op == '_':
                    function = self.BI

                else:
                    print('wrong operation')
                    exit(1)

                for row in self.rows:
                    # print(lenght_current_row, len(row),[relational_clm1], [relational_clm2])
                    row.append( function(row[relational_clm1], row[relational_clm2]) )
                lenght_current_row += 1

    def solve(self):
        if self.sure_logical_exp_is_valid(self.logical_exp):
            self.__fill_clms()
            self.output_in_table()

        else:
            print('this is not valid exp')


"""
	func needs for this shit
    1 - separate elms
    2 - sure that its valid logical exp
        - NOT operator is for one element
        - (AND,OR,XOR,IFTHEN,BI) operators are for two elements
    3 - execute exps in order
        - NOT
        - AND
        - OR
        - IF_THEN
        - BI
"""

x  = '(x^(~yvz)>(zvf))^(~f^z)v(~y)'
x1 = '(x^(~yvz)>(zvf))'
x2 = '(x^(~yvz)>(zvf))^(~f)'

x2 = '(p>q)^(q>r)'

#logical = TruthTable(x)
#logical.solve()
#print()

#logical = TruthTable(x1)
#logical.solve()
#print()

x = input('ur logical_exp: ')
logical = TruthTable(x)
logical.solve()


