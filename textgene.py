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
      letters = string.printable
      return ''.join(random.choice(letters) for i in range(n))          

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
         aux = random.random()
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
      
      tamanho = len(pai)
      try:
         if tamanho%2 == 0:
            marcador = tamanho/2
         else:
            marcador = (tamanho/2)+1
         marcador = int(marcador)
         gene = self.mutacao(pai[:marcador] + mae[marcador:])
         filho = Elemento(gene)
         filho.calcularFitness(self.objetivo)
         return filho
      except Exception as error:
         print('Caught this error: ' + repr(error))
         
         

   def reproduzir(self):
      tamanho = len(self.lista)
      pivo = round((tamanho-1)*0.2)
      
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

   def printLista(self,lista):
      texto = ""
      for i in lista:
         texto+= i.gene+","
      return texto

   def ciclo(self):
      with open("log-runtime.txt", "a+") as arquivo: 
         while self.fim == False:
            try: 
               self.ordenar()
               self.reproduzir()
               self.geracao += 1
               arquivo.write("\nGeracao: %d Maior Fitness: %2f | Gene: %s \n"%
                          (self.geracao, self.lista[0].fitness, self.lista[0].gene))
               if self.lista[0].fitness == 100:
                  self.parar()
            except Exception as error:
               print('Caught this error: ' + repr(error))
         arquivo.close()
      try:
         with open("log.txt", "a+") as f: 
            agora = datetime.now()
            f.write("\n\nTempo de Execução: "+str(time.time() - self.inicio)+" segundos")
            f.write("\n"+agora.strftime('%d/%m/%Y %H:%M'))
            f.write("\nObjetivo: "+self.objetivo+"\n")
            f.write("Geracoes: "+str(self.geracao)+"\n")
            f.write("Resultado: "+self.lista[0].gene+"\n")
            f.write("\nPopulacao Final: \n\n"+self.printLista(self.lista)+"\n\n")
            f.close()
            print("Relatorio Gerado com sucesso")
      except Exception as error:
         print("Houve um erro ao gerar o relatório")
         print('Caught this error: ' + repr(error))    
   def iniciar(self):
      self.fim=False
      self.ciclo()

   def ordenar(self):
      self.lista.sort(key=lambda x: x.fitness, reverse=True)


try:
   tamanho = int(sys.argv[2])
   frase = sys.argv[1]
except:
   print("———————————————————————————————————————————————")
   print("\tArgumentos inválidos")
   print("———————————————————————————————————————————————")
   sys.exit("Argumentos inválidos")
p = Populacao(frase, tamanho)
p.iniciar()
