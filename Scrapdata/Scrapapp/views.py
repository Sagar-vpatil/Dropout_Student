from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.utils import formats
# Create your views here.
from .models import ScrapedData


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def index(request):
    if request.method == 'POST':
        url_to_check = request.POST.get('url')
        if url_to_check:
            url_validator = URLValidator()
            try:
                url_validator(url_to_check)
                req = requests.get(url_to_check)
                soup = BeautifulSoup(req.content, "html.parser")
                # for re in soup(["thead"]):
                #     re.extract()
                # for script in soup(["script", "style", "title", "head", "form", 'meta', '[document]']):
                #     script.extract()
                # res = soup.table.text
                # print(res)

                table = soup.find('table')
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip the header row if present
                    columns = row.find_all('td')
                    college_name = columns[0].text.strip()
                    prn = columns[1].text.strip()
                    std_name = columns[2].text.strip()
                    tcNo = columns[3].text.strip()
                    date = columns[4].text.strip()
                    reason = columns[5].text.strip()
                    phone = columns[6].text.strip()
                    print(date)
                    # df = DateFormat(date)
                    # formatted_datetime = formats.date_format(df, "%d-%m-%Y")
                    # # Df = df.format(get_format('DATE_FORMAT'))
                    # print(formatted_datetime)
                    ScrapedData.objects.create(college_name=college_name, PRN=prn, name=std_name, TcNo=tcNo, date=date, reason=reason, mobile=phone)
                    print(college_name, prn, std_name, tcNo, date, reason, phone)

                # for row in rows:
                #     th = row.find_all('th')
                #     columns = row.find_all('td')
                #     for i in th:
                #         if i.text == "First":
                #             n = len(i)
                #         elif i.text == "Last":
                #             a = len(i)
                #             print(a)
                # print(n, a)
                # for row in rows[1:]:
                #     th = row.find_all('th')
                #     columns = row.find_all('td')
                #     name = columns[a].text.strip()
                #     address = columns[n].text.strip()
                #     print(name, address, a)



            except ValidationError as e:

                error_message = "Invalid URL provided."
                print(error_message)

        else:
            error_message = "Please provide a URL."
            print(error_message)
    return render(request, 'index.html')
