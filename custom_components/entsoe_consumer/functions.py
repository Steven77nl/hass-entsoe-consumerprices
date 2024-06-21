
import pandas as pd


# MY HANDY FUNCTIONS

def get_attributes(obj, max=1, depth=0, prefix=''):
# Get all attributes for the given object until a certain maximum depth and return this as a string

    attstr = ''
    for attribute, value in vars(obj).items():
        
        if isinstance(value, pd.Series):
            value = f"{value.iloc[0]}... ({len(value)-1} more)"

        attstr += (f"{prefix}{attribute}={value}\n")

        # If the value is an object with its own attributes, return them too
        if hasattr(value, '__dict__') and depth < max:
            attstr += get_attributes(value, max, depth + 1,f"{attribute}.")
    
    return attstr
