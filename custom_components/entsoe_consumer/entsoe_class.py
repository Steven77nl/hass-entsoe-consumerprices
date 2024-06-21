from entsoe import EntsoePandasClient
from .functions import get_attributes
import pandas as pd
from datetime import datetime
from datetime import timedelta

class Entsoe_Class:

    def __init__(self):
        
        self.api_key = None
        self.country_code = None
        self.timezone = None
        
        self.supplier_costs = None
        self.energy_tax = None
        self.vat = None

        self.currenthour = None
        self.nexthour = None
        
        self.all = None
        self.week = None
        self.today = None
        self.tomorrow = None
        self.yesterday = None
        self.upcoming = None


    def __str__(self):
        attstr = get_attributes(obj=self)
        return attstr

    def calc_price(self, value) -> float:

        # Used to calculate the consumer price based on given values
        price = round(value / 1000, 5)
        
        # Add the Supplier Costs if provided
        if self.supplier_costs != None or self.supplier_costs > 0:
            price = price + self.supplier_costs  
        
        # Add the Energy Tax if provided
        if self.energy_tax != None or self.energy_tax > 0:
            price = price + self.energy_tax
        
        # Add the Sales Tax if provided
        if self.vat != None or self.vat > 0:
            vat_mp = 1 + (self.vat/100)
            price = price * vat_mp
                
        return round(price,5)


    def get_prices(self, start, end):

        ts_start = pd.Timestamp(start.year, start.month, start.day, 0, tz=self.timezone)
        ts_end = pd.Timestamp(end.year, end.month, end.day, 23, tz=self.timezone)

        client = EntsoePandasClient(api_key=self.api_key)
        result = client.query_day_ahead_prices(self.country_code, start=ts_start, end=ts_end)
        
        if result.empty:
            return None
        
        if len(result) == 0:
            return None
        
        for id, value in result.items():
            price = self.calc_price(value)
            result.at[id] = price

        return result


    def update_prices_online(self):

        # Get a full last week including next day if available.
        start_date = datetime.now().date() - timedelta(days=6)
        end_date = datetime.now().date() + timedelta(days=1)
        current_hour = datetime.now().hour

        result = self.get_prices(start=start_date, end=end_date)

        if result.empty:
            return 0
            
        self.all = Statistics(result)

        if len(result) == 168:
            self.tomorrow = None
            self.week = Statistics(result)
        elif len(result) == 192:
            self.tomorrow = Statistics(result[168:192])
            self.week = Statistics(result[24:])
        else:
            return len(result)
        
        self.yesterday = Statistics(result[120:144])
        self.today = Statistics(result[144:168])
        self.upcoming = Statistics(result[current_hour+144:])
        self.currenthour = result.iloc[current_hour+144]
        self.nexthour = result.iloc[current_hour+145]

        return len(result)


    def update_prices_offline(self):

        result = self.all.prices
        current_hour = datetime.now().hour
        
        if len(result) < 168:
            # we don't have enough data
            return 0
        
        if current_hour == 23 and len(result) == 168:
            # we don't have enough data for next hour
            self.upcoming = Statistics(result[current_hour+144:])
            self.currenthour = result.iloc[current_hour+144]
            self.nexthour = None
            return 2

        if current_hour == 0 and self.tomorrow != None:

            if len(result) < 192:
                # Not enough information for new today
                self.yesterday = self.today
                self.today = None
                self.tomorrow = None
                self.upcoming = None
                self.currenthour = None
                self.nexthour = None
                return len(result)

            elif len(result) == 192:
                # move today to yesterday, tomorrow to today, empty tomorrow.
                result = result[24:]
                self.yesterday = self.today
                self.today = self.tomorrow
                self.tomorrow = None
                self.all = Statistics(result)
                self.upcoming = Statistics(result[current_hour+144:])
                self.currenthour = result.iloc[current_hour+144]
                self.nexthour = result.iloc[current_hour+145]
                return 3

        # Update the current hour, next hour and upcoming prices
        self.upcoming = Statistics(result[current_hour+144:])
        self.currenthour = result.iloc[current_hour+144]
        self.nexthour = result.iloc[current_hour+145]

        return 1


class Statistics:
    
    def __init__(self, prices):
        
        low = 10.0
        high = -10.0
        total = 0

        for id, value in prices.items():
            if value < low: low =  value
            if value > high: high = value
            total += value
        
        self.low = low
        self.high = high
        self.average = round(total / len(prices),5)
        self.prices = prices
