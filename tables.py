# import requests
# from bs4 import BeautifulSoup

# url = "https://en.wikipedia.org/wiki/List_of_districts_of_Nepal"

# response = requests.get(url)

# soup = BeautifulSoup(response.content, 'html.parser')

# tables = soup.find_all('table', {'class': 'wikitable sortable'})

# for i, table in enumerate(tables):
#     print(f"Table {i+1}:")
#     headers = [header.text.strip() for header in table.find_all('th')]
#     print(f" Province Name : {headers[6]}  Province Number : {i}")
#     rows = []
#     for row in table.find_all('tr'):
#         rows.append([cell.text.strip() for cell in row.find_all('td')])
#     for row in rows:
#         if len(row) > 4:
#             print(f"District : {row[0]} \t\t\t Headquarter : {row[2]} ")

