#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    if newVar:  # only check constraints containing newVar
        cons = csp.get_cons_with_var(newVar)
    else:  # check all constraints
        cons = csp.get_all_cons()  # check all constraints

    # list of all pruned variables
    pruned = []
    for con in cons:
        if con.get_n_unasgn() == 1:
            var = con.get_unasgn_vars()[0]  # get the only unassigned variable
            values = var.cur_domain()  # get all possible values of the variable
            for val in values:
                if not con.has_support(var, val):  # the value of the variable falsifies the constraint
                    pruned.append((var, val))  # record it in list
                    var.prune_value(val)  # prune the value from the domain of the variable
                    if var.cur_domain_size() == 0:  # dead-end is found
                        return False, pruned
    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    if newVar:  # only check constraints containing newVar
        cons = csp.get_cons_with_var(newVar)
    else:  # check all constraints
        cons = csp.get_all_cons()

    # list of all pruned variables
    pruned = []
    # loop until cons is empty
    while cons:
        con = cons.pop(0)
        for var in con.get_scope():
            for val in var.cur_domain():
                if not con.has_support(var, val):  # the value of the variable falsifies the constraint
                    pruned.append((var, val))  # record it in list
                    var.prune_value(val)  # prune the value from the domain of the variable
                    if var.cur_domain_size() == 0:  # dead-end is found
                        return False, pruned
                    else:
                        # add affected constraints to cons
                        for c in csp.get_cons_with_var(var):
                            if c not in cons:
                                cons.append(c)
    return True, pruned


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    # list of tuples (variable, current domain size of variable)
    size_ordering = []
    # get the current domain size of all the variable and append them in list
    for var in csp.get_all_unasgn_vars():
        size_ordering.append((var, var.cur_domain_size()))
    # order tuples by the current domain size of variables
    size_ordering.sort(key=lambda x: x[1])
    return size_ordering[0][0]
