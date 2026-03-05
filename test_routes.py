from app import app, criar_banco

print("creating db")
criar_banco()

app.testing = True
client = app.test_client()

r = client.get('/')
print('index', r.status_code)
r2 = client.get('/agendar')
print('agendar', r2.status_code)
print(r2.data.decode()[:500])
r3 = client.get('/professores')
print('professores', r3.status_code)
print(r3.data.decode()[:500])
r4 = client.get('/disciplinas')
print('disciplinas', r4.status_code)
print(r4.data.decode()[:500])

print('logging in as admin')
client.post('/login', data={'usuario':'admin','senha':'Dotti2826'})
r5 = client.get('/professores')
print('after login professores', r5.status_code)
print(r5.data.decode()[:500])
