import requests

url = "https://graph.facebook.com/v2.5/153080620724/feed"

querystring = {"access_token":"EAACEdEose0cBAOB7cevFUjBDeYEWqN6KaYzuhm7IooMKgAXOD92lYRMFZB0AObZCLemQcQfwDcIrzBxh64joZAgyyghj4SZCEYnKlpdz494PyRFWx59nl54pDW0W2X5zvMxbbNv8gRAxHJSLcVmNUAJr03cZBEPW8zZBVhSZB7JKLZA6AyrzEDcWhQK8NxXezwoZD","debug":"all","format":"json","method":"get","pretty":"0","suppress_http_code":"1"}

headers = {
    'cacheg': "5aeb7a94-d25b-2134-2aaf-31ac7d560055"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)