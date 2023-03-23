# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask_migrate import Migrate

from app import app, db

# =============================================================================

# Migrate App (if necessary):
Migrate(app, db)


# Inner command:
def load_cmd(aUseRandomValues=None):
    import csv
    from datetime import datetime
    from random import randint
    from api.models import Data

    if aUseRandomValues:
        print( ' >>> Randomize Values ')
    else:
        print( ' >>> Use Values from input file ')

    # Create Tables (if not exist):
    db.create_all()
    # Truncate :
    db.session.query(Data).delete()
    db.session.commit()

    with open('media/data.csv', newline='') as csvfile:
        # Load CSV file:
        csvreader = csv.reader(csvfile)
        # Ignore header (1st line):
        header    = next(csvreader)
        
        '''
        Expected format: 
            HEADER: product_code,product_info,value,currency,type
            SAMPLE: Lenovo_Ideapad_3i, Lenovo Ideapad 3i 14.0inch FHD Laptop,9.5,euro,transaction
            
            product_code (string)  : Lenovo_Ideapad_3i
            product_info (string)  : Lenovo Ideapad 3i 14.0inch FHD Laptop
            value        (integer) : 9 
            currency     (string)  : usd, eur 
            type         (string)  : transaction (hardoded)
        '''
        # Iterate over the rows for timestamp:
        iter = 0 
        for row in csvreader:
            iter += 1
            if len(row) != 5:
                print( ' >>> Error parsing line ('+str(iter)+') -> ' + ' '.join([str(elem) for elem in row]) )
                continue        

            item_code     = row[0]
            item_name     = row[1]

            if aUseRandomValues:
                item_value = randint(5, 100)
            else:
                item_value = row[2]

            item_currency = row[3]
            item_type     = row[4]

            # randomize in the past the transaction date
            # The distribuition range ~1 month 
            item_ts       = datetime.utcnow().timestamp() - ( 2 * iter * randint(5, 10) * 3600 )
            item_ts       = int( item_ts )

            _data = Data(code=item_code, name=item_name, value=item_value, currency=item_currency, type=item_type, ts=item_ts)
            db.session.add(_data)

        db.session.commit()


@app.cli.command("load_data")
def load_data():
    return load_cmd()


@app.cli.command("load_random_data")
def load_random_data():
    return load_cmd( True )


if __name__ == "__main__":
    app.run()
