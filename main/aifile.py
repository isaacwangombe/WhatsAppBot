import os
import openai
from django.conf import settings
openai.api_key = settings.OPENAI_API_KEY 


def companyDescription(business_name, business_type,country,product_service,short_description,years_operation,progress):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Generate Company Description section for a Business Plan for the following business, using the guidelines provided:\nBusiness Name: {business_name}\nBusiness Type:{business_type}\nCountry:{country}\nProduct or Service:{product_service}\nShort Description:{short_description}\n Years in operation:{years_operation} \nProgress to date:{progress}\nstructure, if one is  provided. Write a detailed business description for the short description provided in a professional tone".format(business_name, business_type,country,product_service,short_description,years_operation,progress),
        temperature=0.7,
        max_tokens=2000,
        top_p=1,
        best_of=2,
        frequency_penalty=0,
        presence_penalty=0

    )

    if 'choices' in response:
        if len(response['choices'])>0:
            # answer = response['choices'][0]['text']
            answer = response['choices'][0]['text'].replace('\n',"<br>")
            return business_name + answer
        else:
            return ""
    else:
        return ""