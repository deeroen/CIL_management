import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
"""psql query: 
    SELECT job_creation_date, ag_id, ag_type
	FROM daily_feed_ldap.ag_transform;
"""
# Extract from query
df = pd.read_csv("C:\\Users\\AL7871\\Downloads\\data-1645093512650.csv")

# Keep user which have 2 (limited and glogal) ag_type (otherwise the user is always global => no use, or always limited => no info)
global_limited = df.groupby(['ag_id']).filter(lambda x: x['ag_type'].nunique() > 1).sort_values(["ag_id","job_creation_date"],axis=0)

# Filter out user which are currently in global type
## Take the last info (limited or global) for each user
last_info=global_limited.groupby('ag_id').ag_type.last()
## Remove users having the last state == global (~ means "not")
out = global_limited.loc[~global_limited.ag_id.isin(last_info[last_info=="global"].index)]

# Filter out global type line and take first date
Only_limited = out[out['ag_type'] != "global"]

# Take first limited date for each user
First_limited = Only_limited.groupby('ag_id').first()
First_limited['ag_id'] = First_limited.index

# Take users limited since less than 3 months
First_limited['delta'] = pd.to_datetime(First_limited['job_creation_date']) <= datetime.today() - relativedelta(months=3)
First_limited.delta.value_counts()

"""
First_limited.delta.value_counts()
False    109
True       9
"""

# Users concernés
First_limited[First_limited.delta == True].ag_id.values

"""
array([ 32772,  34136,  40234,  40689,  42189,  42329,  47242,  52762,
       115497], dtype=int64)
"""