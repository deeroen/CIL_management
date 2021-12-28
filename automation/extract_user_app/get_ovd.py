from connectLDAP.connector import *
import pandas as pd
from automation.userful_functions import *



txt = """123472
102742
117626
136817
135528
"""
lt = txt.split("\n")

lt = list(filter(None,lt))
print(lt)
print(uidList_to_filter(lt))