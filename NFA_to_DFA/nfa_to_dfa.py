import tkinter as tk

#Global Variables
F_dfa=[] #Accepting states of the DFA
d = {} #Dictionary to store DFA's transition function

def delta_nfa(state, alphabet):
    return trans[state][alphabet] #transition function of the nfa. Returns a list

def main():
    #----------------------------------Input processing---------------------#
    
    f = open("nfa.txt", "r")
    
    #-----------Reading States-----------#
    line=f.readline()
    line=line.strip()
    length=len(line)
    state_comma=line[1:length-1] #Removing braces
    state_comma = state_comma.replace(" ", "") #Removing whitespaces
    global Q_nfa 
    Q_nfa = state_comma.split(",") #Reading CSVs into a list
    
    
    #-----------Reading Alphabets-----------#
    line=f.readline()
    line=line.strip()
    length=len(line)
    letters_comma=line[1:length-1]
    letters_comma = letters_comma.replace(" ","")
    global sigma
    sigma=letters_comma.split(",")
    
    
    #-----------Reading Transition Function-----------#
    line=f.readline()
    line=line.strip()
    line=line.replace(" ", "") #Removing whitespaces
    qline=""
    oq=False #Open(Unpaired) Quote
    #Enclosing all states and alphabets in quotes
    for i in line:
        if(i == '{'):
            qline+=i
            continue

        
        if(i==':' or i==',' or i=='}' or i=='[' or i==']'):
            if(oq):
                qline+="'"
                qline+=i
                oq=False
            else:
                qline +=i
                
            continue
                
                
        if(oq==False):
            oq=True
            qline +="'"
            qline +=i
            continue
        
        if(oq==True):
            qline +=i
                
    global trans
    trans=eval(qline) #String to dictionary conversion
    
    #-----------Reading Start State-----------#
    line=f.readline()
    line=line.strip()
    line=line.replace(" ", "")
    line = str(line)
    global start_nfa
    start_nfa =line
    
    #-----------Reading Final States-----------#
    line=f.readline()
    line=line.strip()
    length=len(line)
    final_comma=line[1:length-1]
    final_comma = final_comma.replace(" ","")
    global F
    F = final_comma.split(",")    
    
    
    
    #Getting the power set of Q_nfa, and filling
    #it in Q_dfa
    global Q_dfa
    Q_dfa = sub_lists(Q_nfa)
    
    
    construct_delta_dfa() #Calling the function to create the transition function of dfa
    
    
    
    #Start State of dfa is the e closure of the start state of nfa, 
    #plus start state itself. 
    start_eclose = e_closure_state(start_nfa,[])
    start_eclose.append(start_nfa)
    start_state_dfa = find_dfa_state(start_eclose)
   
    
    f.close()
    
    #----------------------------------Output processing---------------------#
    fo = open("dfa.txt", "w")
    #-----------Writing States-----------#
    statesStr = str(Q_dfa)
    statesStr = statesStr.replace("'", "") #Remove quotes around states
    fo.write('States: '+statesStr+"\n")
    #-----------Writing Alphabets-----------#
    alphaWrite = str(sigma).replace("'","")
    fo.write('Alphabets: '+alphaWrite+"\n")
    #-----------Writing Transition Function-----------#
    dString = str(d).replace("'","")
    fo.write('Transition Function: '+dString+"\n")
    #-----------Writing Start State-----------#
    StartString = str(start_state_dfa).replace("'","")
    fo.write('Start State: '+StartString+"\n")
    #-----------Writing Accept States-----------#
    AcceptString = str(F_dfa).replace("'","")
    fo.write('Accept States: '+AcceptString)
    
    fo.close()
    
def construct_delta_dfa():#Constructing the transition function for the DFA
   for i in Q_dfa: #For each state in the dfa, we figure out the transitions
      dict_state = {} 
      for k in sigma:#For each alphabet 
         to_composite = []
         for j in i: #For each dfa state,corresponding to multiple nfa states, find E(q) i.e. closure
            to = []
            tos_alpha = delta_nfa(j,k) #Add states reachable from the main state by the alphabet
            to.extend(tos_alpha)
            '''tos_epsilon = e_closure_state(j,[]) #Apparently these states are not counted in the transition,
            #so it is commented out.
            for l in tos_epsilon: #Add states reachable from the e-closure states by the alphabet
               tos_epsilon_alpha = delta_nfa(l,k)
               to.extend(x for x in tos_epsilon_alpha if x not in to)'''
            for l in to: #Add states e-reachable from states reachable by alphabet
               tos_alpha_epsilon = e_closure_state(l,[])
               to= to + list(set(tos_alpha_epsilon) - set(to))
            to_composite = to_composite + list(set(to) - set(to_composite))
         to_composite_state = find_dfa_state(to_composite)#Sort the states in the nomenclature
         dict_state[k] = to_composite_state
      d[str(i)] = dict_state
      
   for i in Q_dfa: #Accept states of the DFA
      for j in i:
         if j in F:
            F_dfa.append(i)
            continue
                
        
def delta_dfa(state, alphabet):
    t=tuple(state, alphabet)
    return d[t]
    
def sub_lists(l):
   #Returns the power set of the input list
   
   def decimalToBinary(n):   # converting decimal to binary
       b = 0
       i = 1
       while (n != 0):
   
           r = n % 2
           b+= r * i
           n//= 2
           i = i * 10
       return b
   
   
   def makeList(k):       # list of the binary element produced
       a =[]
       if(k == 0):
           a.append(0)
   
       while (k>0):
   
           a.append(k % 10)
           k//= 10
       a.reverse()
       return a
   
   def checkBinary(bin, l):
       temp =[]
       for i in range(len(bin)):
           if(bin[i]== 1):
               temp.append(l[i])
       return temp

   binlist =[]
   subsets =[]
   
   n = len(l)
   
   for i in range(2**n):
       s = decimalToBinary(i)
       arr = makeList(s) 
       binlist.append(arr)   
       for i in binlist:      
          k = 0     
          while(len(i)!= n):
             i.insert(k, 0) # representing the binary equivalent according to len(l)
             k = k + 1
   for i in binlist:
      subsets.append(checkBinary(i, l))
   return subsets
            
def e_closure_state(state,eclose): 
   #Recursive function. Input - 
   #a state and a list of states which are reachable from it(initially empty)
   primary = trans[state]['epsilon'] #A list of states one hop away
   primary_no_duplicates=[]
   [primary_no_duplicates.append(x) for x in primary if x not in primary_no_duplicates] #Remove duplicates
   #eclose.append(primary_no_duplicates)
   eclose = eclose + list(set(primary_no_duplicates) - set(eclose))
   for i in primary_no_duplicates:
      if i not in eclose:#Base case = the state is already recorded in the e-closure
         eclose.append(i)
         secondary = e_closure_state(i,eclose.copy()) #Recursive step
         for j in secondary:#Sort through the e-reachable states of the secondary state
            if j not in eclose: #Add it to list of reachable states if it is not already added
               eclose.append(j)              
   return eclose.copy()

    
def find_dfa_state(state_list):
   #Given a list of nfa states in random order, find the corresponding single dfa state in correct order
   for i in Q_dfa:
       if(set(i) == set(state_list)):
          return i.copy()

main()
def show_output():
    # Call main function
    main()
    
    # Create GUI window
    root = tk.Tk()
    root.title("DFA Output")
    
    # Create label to display output
    output_label = tk.Label(root, text="DFA Output:\n\n")
    output_label.pack()
    
    # Open and read output file
    with open("dfa.txt", "r") as f:
        output_text = f.read()
        
    # Create text box to display output
    output_textbox = tk.Text(root, height=15, width=150)
    output_textbox.pack()
    output_textbox.insert(tk.END, output_text)
    
    root.mainloop()

# Create GUI button to run show_output function
button = tk.Button(text="Run Program", command=show_output)
button.pack()

# Run GUI loop
tk.mainloop()