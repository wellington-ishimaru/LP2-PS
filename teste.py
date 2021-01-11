import _sqlite3

conn = _sqlite3.connect("Condominio.db")
c = conn.cursor()

#c.execute("Drop table funcionarios")
#conn.commit()
#print(resultado[len(resultado)-1][0])
"""
print("{:^15}".format("Numero vaga") +"|"+ "{:^15}".format("Bloco") +"|"+ "{:^15}".format("Nome") +"|"+ "{:^15}".format("Carro"))
print("________________________________________________________________")
print("{:^15}".format(resultado[0]) +"|"+"{:^15}".format(resultado[1]) +"|"+
    "{:^15}".format(resultado[4]) +"|"+ "{:^15}".format(resultado[5]))
"""