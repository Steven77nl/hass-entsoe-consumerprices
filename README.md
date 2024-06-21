# Home Assistant ENTSO-e Consumer Prices Integration
Custom Integration for Home Assistant to fetch consumer dynamic energy prices from European countries via the ENTSO-e Transparency Platform (https://transparency.entsoe.eu/).
Several energy price sensor are edit and can be used in automations to switch equipment. A 24 Hour forecast of the energy prices when available are loaden into sensors as well.

### API Access
You need an ENTSO-e Restful API key for this integration. 
To request this API key, register on the [Transparency Platform](https://transparency.entsoe.eu/) and send an email to transparency@entsoe.eu with “Restful API access” in the subject line. 
Indicate the email address you entered during registration in the email body.

### Sensors
Multiple sets of price sensors will be made available:
Today (based on hour prices of the current day)
Yesterday (based on hour prices of the past day)
Tomorrow (based on hour prices of the next day)
Week (based on the hour prices of the last available 7 days of data)
Upcoming (based on the hour prices from the current hour until the next day)

Each set will contain out of:
the highest price
the lowest price
the average price
the full price series per hour (as series attribute)
  
------
## Installation

### Manual
Download this repository and place the contents of `custom_components` in your own `custom_components` map of your Home Assistant installation. Restart Home Assistant and add the integration through your settings. 

