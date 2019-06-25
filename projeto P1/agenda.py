import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso a agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):
  data = ''
  hora = ''
  pri = ''
  cont = ''
  proj = ''
  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  else:
    for elemento in extras:
      if dataValida(elemento):
        data = elemento
      elif horaValida(elemento):
        hora = elemento
      elif prioridadeValida(elemento):
        pri = elemento
      elif contextoValido(elemento):
        cont = elemento
      elif projetoValido(elemento):
        proj = elemento
  return pri + ' ' + data + ' ' + hora + ' ' + descricao + ' ' + cont + ' ' + proj
  
      
  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  if len(pri) > 2 and len(pri) < 4:
    if pri[0] == '(' and pri[2] == ')' and len(pri) == 3 and (pri[1] > '@' and pri[1] < '[' or pri[1] > "'" and pri[1] < '{'):
        return True
    else:
        return False
  else:
      return False


# Valida a hora. Codiaque o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    listaMin = []
    listaHora = []
    cont = 0
    for elemento in horaMin:
      if cont < 2:
        listaHora += [elemento]
      else:
        listaMin += [elemento]
    listaTudo = listaHora + listaMin
    if (int(listaTudo[0]) >= 0 and int(listaTudo[0]) <= 23) and (int(listaTudo[1]) >= 0 and int(listaTudo[1]) <= 59):
      return True
    else:
      return False 

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if len(data) == 8 and soDigitos(data):
    lista = []
    dia = ""
    mes = ""
    ano = ""
    cont = 0
    for i in data:
      if cont < 2:
        dia += i
      elif cont < 4:
        mes += i
      else:
        ano += i
      cont += 1
    lista.append(dia)
    lista.append(mes)
    lista.append(ano)
    if int(lista[1]) >= 0 or int(lista[1]) <= 12:
      if int(lista[1]) == 12 or int(lista[1]) == 10 or int(lista[1]) == 8 or int(lista[1]) == 7 or int(lista[1]) == 5 or int(lista[1]) == 3 or int(lista[1]) == 1:
        if int(lista[0]) >= 0 and int(lista[0]) <= 31:
          return True
        else:
            return False
      elif int(lista[1]) == 11 or int(lista[1]) == 9 or int(lista[1]) == 6 or int(lista[1]) == 4:
        if int(lista[0]) >=0 and int(lista[0]) <= 30:
          return True
        else:
          return False
      elif int(lista[1]) == 2:
        if int(lista[0]) >= 0 and int(lista[0]) <= 28:
          return True
        else:
            return False
      else:
          return False
    else:    
      return False
  else:
    return False





# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):

  if len(proj) >= 2 and proj[0] == '+':
      return True
  else:
      return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):

  if len(cont) >= 2 and cont[0] == '@':
    return True
  else:
    return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True




# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 
    indice = 0
    listaDesc = []
    for elemento in tokens:
      if dataValida(elemento):
        data = elemento
      elif horaValida(elemento):
        hora = elemento
      elif prioridadeValida(elemento):
        pri = elemento
      elif projetoValido(elemento):
        projeto = elemento
      elif contextoValido(elemento):
        contexto = elemento
      else:
        listaDesc.append(elemento)
    for palavra in listaDesc:
        desc += palavra + ' '
    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens

# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades d22072000e determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, 22072000porém. 
def listar():

  fp = open('todo.txt','r')
  tudoLista = fp.readlines()
  listaDeTuplas = organizar(tudoLista)

  pri = ordenarPorPrioridade(listaDeTuplas)
  hora = ordenarPorDataHora(pri)
  cont = 1
  for elemento in hora:
    if elemento[1][2] == "(A)":
      print(str(cont) + ' ' + str(elemento) + BOLD + RED)
    elif elemento[1][2] == "(B)":
      print(str(cont) + ' ' + str(elemento) + BLUE)
    elif elemento[1][2] == "(C)":
      print(str(cont) + ' ' + str(elemento) + YELLOW)
    elif elemento[1][2] == "(D)":
      print(str(cont) + ' ' + str(elemento) + GREEN)
    else:
      print(str(cont) + ' ' + str(elemento))
    cont += 1
  return hora

def ordenarPorDataHora(itens):
  semPri = []
  ComPri = []
  lista = []
  cont = 0
  for elemento in itens:
    if cont > len(itens) - 1:
      cont = len(itens) - 1
    if elemento[1][2] != '':
      if elemento == len(lista) - 1:
        lista += [elemento]
      elif elemento[1][2] == itens[cont + 1][1][2]:
        lista += [elemento]
      else:
        lista += [elemento]
        lista = ordenarPorDataHoraSPri(lista)
        ComPri += lista
        lista = []
    else:
      semPri += [elemento]
    cont += 1
  semPri = ordenarPorDataHoraSPri(semPri)
  return ComPri + semPri


def ordenarPorDataHoraSPri(itens):
  semDataHora = []
  semData = []
  semHora = []
  comDataHora = []
  for elemento in itens:
    if elemento[1][1] != '' and elemento[1][0] != '':
      comDataHora += [elemento]
    elif elemento[1][0] == '' and elemento[1][1] != '':
      semData += [elemento]
    elif elemento[1][0] != '' and elemento[1][1] == '':
      semHora += [elemento]
    else:
      semDataHora += [elemento]
  semData = ordenarSemData(semData)
  semHora = ordenarSemHora(semHora)
  comDataHora = ordenarComDataHora(comDataHora)
  ordenado = comDataHora + semHora + semData + semDataHora
  return ordenado
      
def ordenarSemData(lista):
  for elemento in lista:
    cont = 0
    while cont < len(lista) - 1:
      if int(lista[cont][1][1]) > int(lista[cont + 1][1][1]):
        aux = lista[cont]
        lista[cont] = lista[cont + 1]
        lista[cont + 1] = lista[cont]
      cont += 1
  return lista

def ordenarSemHora(lista):
  for elemento in lista:
    cont = 0
    while cont < len(lista) - 1:
      if maiorData(lista[cont][1][0],lista[cont][1][0]):
        aux = lista[cont]
        lista[cont] = lista[cont + 1]
        lista[cont + 1] = aux
      cont += 1
  return lista

def ordenarComDataHora(lista):
  for elemento in lista:
    cont = 0
    while cont < len(lista) - 1:
      if int(lista[cont][1][0]) != int(lista[cont + 1][1][0]) and maiorData(int(lista[cont][1][0]),int(lista[cont + 1][1][0])):
        aux = lista[cont]
        lista[cont] = lista[cont + 1]
        lista[cont + 1] = aux
      elif int(lista[cont][1][0]) == int(lista[cont + 1][1][0]):
        if lista[cont][1][1] > lista[cont + 1][1][1]:
          aux = lista[cont]
          lista[cont] = lista[cont + 1]
          lista[cont + 1] = aux
      cont += 1
  return lista

        

      

# funcao que retorna True caso a data1 (data do primeiro parametro) seja maior
def maiorData(data1,data2):
  dia1 = [data1[0] + data1[1]]
  dia2 = [data2[0] + data2[0]]
  mes1 = [data1[2] + data1[3]]
  mes2 = [data2[2] + data2[3]]
  ano1 = [data1[4] + data1[5] + data1[6] + data1[7]]
  ano2 = [data2[4] + data2[5] + data1[6] + data1[7]]
  if int(ano1[0]) > int(ano2[0]):
    return True
  elif int(ano1[0]) == int(ano2[0]):
    if int(mes1[0]) > int(mes2[0]):
      return True
    elif int(mes1[0]) == int(mes2[0]):
      if int(dia1[0]) > int(dia2[0]):
        return True
      else:
        return False
    else:
      return False
  else:
    return False

# funcao que devolve True caso hora1 seja maior que hora2  
def maiorHora(hora1,hora2):
  pontGrande1 = [hora1[0] + hora1[1]]
  pontGrande2 = [hora2[0] + hora2[1]]
  pontPequeno1 = [hora1[2] + hora1[3]]
  pontPequeno2 = [hora2[2] + hora2[3]]
  if int(pontGrande1[0]) > int(pontGrande2[0]):
    return True
  elif int(pontGrande1[0]) == int(pontGrande2[0]):
    if int(pontPequeno1[0]) > int(pontPequeno2[0]):
      return True
    else:
      return False
  else:
    return False


def ordenarPorPrioridade(itens):
  aux = ''
  for elemento in itens:
    cont = 0
    while cont < len(itens) - 1:
      if itens[cont][1][2] != '' and itens[cont + 1][1][2] != '':
        if str(itens[cont][1][2][1]).upper() > str(itens[cont + 1][1][2][1]).upper():
          aux = itens[cont]
          itens[cont] = itens[cont + 1]
          itens[cont + 1]= aux
      else:
        if itens[cont][1][2] == '':
          itens += [itens.pop(cont)]
        elif itens[cont + 1][1][2] == '': 
          itens += [itens.pop(cont + 1)] 
      cont += 1     
  return itens

def fazer(num):
  fp = open('todo.txt','r')
  cont = 1
  todo = fp.readlines()
  if int(num) > len(todo) - 1:
    return 'Erro, número não é valido'
  for elemento in todo:
    if int(num) == cont:
      feito = todo.pop(cont - 1)
    cont += 1
  fp = open('todo.txt','w')
  for elemento in todo:
    fp.write(elemento)
  fp.close()
  fp = open('done.txt','r+')
  fp.write(feito)
  fp.close()
  
  return feito

def remover(num):
  fp = open('todo.txt','r')
  todo = fp.readlines()
  cont = 1
  if int(num) > len(todo) - 1:
    return 'Erro, esse numero não é válido'
  for elemento in todo:
    if cont == int(num):
      linhaRemovida = todo.pop(cont - 1)
    cont += 1
  fp = open('todo.txt','w')
  for elemento in todo:
    fp.write(elemento)
  fp.close()
  return linhaRemovida


# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num,pri):
  fp = open('todo.txt','r')
  listaDeTudo = fp.readlines()
  novaPri = ''
  cont = 0
  cont1 = 0
  while cont < len(listaDeTudo) - 1:
    if cont + 1 == int(num):
      if listaDeTudo[cont][0] == '(' and listaDeTudo[cont][2] == ')':
        for elemento in listaDeTudo[cont]:
          if cont1 >= 3:
            novaPri += elemento
          cont1 += 1
        novaPri = '(' + pri.upper() + ')' + ' ' + novaPri
        listaDeTudo[cont] = novaPri
      else:
        listaDeTudo[cont] = '(' + pri.upper() + ')' + ' ' + listaDeTudo[cont]
    cont += 1
  fp = open('todo.txt','w')
  for elemento in listaDeTudo:
    fp.write(elemento)
  fp.close()
  return listaDeTudo
  


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    novo = adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
    fp = open('todo.txt','r')
    lista = fp.readlines()
    fp = open('todo.txt','w')
    for elemento in lista:
      fp.write(elemento)
    fp.write(novo)
    fp.close()
    return novo
    
  elif comandos[1] == LISTAR:
    lista = listar()
    return lista   
  elif comandos[1] == REMOVER:
    numeroRemov = comandos[2]
    linhaTirada = remover(numeroRemov)
    return linhaTirada + ' foi removida'   
  elif comandos[1] == FAZER:
    num = comandos[2]
    linhaFeita = fazer(num)
    return linhaFeita + ' foi removida e passada pra o done' 
  elif comandos[1] == PRIORIZAR:
    numero = comandos[2]
    pri = comandos[3]
    linhaAlterada = priorizar(numero,pri)  
    return linhaAlterada + ' foi alterada'  
  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
