import string,random,sys,time
from datetime import datetime

class Elemento:
   gene = ""
   fitness = 0

   def __init__(self, gene):
      self.gene = gene

   def calcularFitness(self,objetivo):
      count = 0
      i=0
      for a in self.gene:
         try:
            if a == objetivo[i]:
               count+=1
            i+=1
         except:      
            continue
      score = count/float(i)
      self.fitness = (score**2)*100

class Populacao:
   inicio = time.time()
   lista = []
   objetivo = ""
   tamanho = 0
   geracao=0
   fim = False
   taxa = 0.01

   def randomString(self, n):
      letters = string.printable.replace('\t\n\r\x0b', '')
      
      r= random.SystemRandom()
      return ''.join(r.choice(letters) for i in range(n))          

   def __init__(self,objetivo, tamanho):
      self.objetivo = objetivo
      self.tamanho = tamanho
      for i in range(0,tamanho):
         try:
            gene = self.randomString(len(self.objetivo))
            elemento = Elemento(gene)
            elemento.calcularFitness(self.objetivo)
            self.lista.append(elemento)

         except Exception as error:
            print('Caught this error: ' + repr(error))
      self.ordenar()

   def mutacao(self,elemento):
      i=0
      novo = ""
      for n in elemento:
         r = random.SystemRandom()
         aux = r.random()
         try:
            if(aux < self.taxa):
               novo+= self.randomString(1)
            else:
               novo += elemento[i]   
         except Exception as error:
               print('Caught this error: ' + repr(error))
         i= i+1
      return novo         
      
      

   def crossover(self,pai,mae):
      
      try:
         gene = ""
         aleatorio = random.SystemRandom()
         for i in range(0, len(pai)):
            r = aleatorio.random()
            if r < 0.5:
               gene+= pai[i]
            else:
               gene+= mae[i]
         filho = Elemento(gene)
         filho.calcularFitness(self.objetivo)
         return filho
      except Exception as error:
         print('Caught this error: ' + repr(error))
         
         

   def reproduzir(self):
      tamanho = len(self.lista)
      pivo = round((tamanho-1)*0.4)
      
      selecionados= self.lista[:(tamanho-pivo)]
      i=0

      novo = []
      aux=0
      for n in selecionados:
         try:
            if i%2 == 1: 
               novo.append(self.crossover(n.gene,selecionados[aux].gene))
               novo.append(self.crossover(selecionados[aux].gene, n.gene))
               if pivo > 0:
                  novo.append(self.crossover(selecionados[aux].gene,n.gene))
                  pivo -= 1
               aux+=1
            i+=1
            self.lista = novo
         except Exception as error:
            print('Caught this error: '+ repr(error))

   def parar(self):
      self.fim = True

   def avaliar(self):
      if self.lista[0].fitness == 100:
         self.parar()
      else:
         self.geracao += 1

   def gerarLog(self,runtime=None):
      if runtime == None:
         with open("log-"+datetime.now().strftime("%Y%m%d-%H%M%S"+".txt"), "a+") as f: 
            agora = datetime.now()
            f.write("Tempo de Execução: "+str(time.time() - self.inicio)+" segundos")
            f.write("\n"+agora.strftime('%d/%m/%Y %H:%M'))
            f.write("\nObjetivo: "+self.objetivo+"\n")
            f.write("Geracoes: "+str(self.geracao)+"\n")
            f.write("Resultado: "+self.lista[0].gene+"\n")
            f.write("\nPopulacao Final: \n"+self.printLista(self.lista)+"\n")
            print("Relatorio Gerado com sucesso")
         f.close()
      else:
         runtime.write("\nGeracao: %d Maior Fitness: %2f | Gene: %s \n"%(self.geracao, self.lista[0].fitness, self.lista[0].gene))
                       
   def printLista(self,lista):
      texto = ""
      j=0
      tamanho = len(lista)
      for i in lista:
         texto+= i.gene
         if not j==tamanho-1:
            texto+= ','
         j+=1
      return texto.replace("\n", "")

   def ciclo(self):
      try: 
         with open("log-runtime.txt", "w") as arquivo: 
            while self.fim == False:
               
               self.ordenar()
               self.reproduzir()
               self.gerarLog(runtime=arquivo)
               self.avaliar()
                       
         self.gerarLog()
      except Exception as error:
         print('Houve um erro ' + repr(error))
      finally:
         arquivo.close
                       
   def iniciar(self):
      self.fim=False
      self.ciclo()

   def ordenar(self):
      self.lista.sort(key=lambda x: x.fitness, reverse=True)


try:
   if sys.argv[1] == "-f" and len(sys.argv) == 4:
      with open(sys.argv[2], 'r') as file:
          frase = file.read().replace('\n', '')
          tamanho = int(sys.argv[3])
      file.close()
   else:
      tamanho = int(sys.argv[2])
      frase = sys.argv[1]
   p = Populacao(frase, tamanho)
   p.iniciar()
except:
   print("———————————————————————————————————————————————")
   print("\tArgumentos inválidos")
   print("———————————————————————————————————————————————")
   sys.exit("Argumentos inválidos")
