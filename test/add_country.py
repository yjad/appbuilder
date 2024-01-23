from datetime import datetime
import pandas as pd
import logging
import random

from app import appbuilder, db
from app.models import Country

log = logging.getLogger(__name__)


cnty_df = pd.read_csv("./test/country_code.csv")


for index, row in cnty_df.iterrows():
    c = Country()
    c.id = index
    c.country = row['Country']
    c.alpha_2_code = row['Alpha 2']
    c.alpha_3_code = row['Alpha 3 code']
    c.un_code = row[ 'UN Code']

    db.session.add(c)
    try:
        db.session.commit()
        print("inserted", c)
    except Exception as e:
        log.error("Contact creation error: %s", e)
        db.session.rollback()
