import random
import string
import math

#Variaveis Globais
soma_pesos=0
pai = 0
mae = 0


def gerar_frase(length): #Gera uma palavra aleatória e seu parametro é o tamanho
   c = math.floor(random.randrange(63,122))
   if (c== 63):
      c=32
   if (c== 64):
      c=46
   return ''.join(chr(c) for i in range(length))

def similaridade(string1,string2): #Checa a porcentagem de similaridade entre strings
    count = 0
    for i in range(min(len(string1), len(string2))):
        if string1[i] == string2[i]:
            count = count + 1
    return count/len(string1)

class elemento:
    gene = ''
    fitness= 0

class populacao:
    lista = []
    geracao = 0
    def __init__(self, length, frase): # Cria a população Inicial
        frase_len = len(frase)
        self.geracao += 1
        for i in range(0,length):
            el = elemento()
            el.gene = gerar_frase(frase_len)
            self.lista.append(el)
    def fitness(self,frase): # Calcula o fitness
        quantidade_pop = len(self.lista)
        global soma_pesos
        soma_pesos= 0
        for i in range(0,quantidade_pop):
            ft = pow(similaridade(self.lista[i].gene,frase),4)
            self.lista[i].fitness = ft
            self.lista.sort(key=lambda self: self.fitness, reverse=True)
            soma_pesos += self.lista[i].fitness
            
    def selecao(self):
        global soma_pesos
        global pai,mae
        r1 = int(random.uniform(0, soma_pesos))
        r2 = int(random.uniform(0, soma_pesos))
        quantidade_pop = len(self.lista)
        seen = 0
        next = 0
        for i in range(0,quantidade_pop):
            next += self.lista[i].fitness
            if(seen<r1<=seen+next):
               pai = i
               break
            if(seen<r2<=seen+next):
               mae = i
               break
            seen+= self.lista[i].fitness;

            seen+= self.lista[i].fitness;             
    def mutacao(self,dna, taxa): #Faz as mudanças de mutação genética
        tamanho_dna = len(dna)
        for i in range(0,tamanho_dna):
           aleatori = random.uniform(0,1)
           if(aleatori < taxa):
               dna = dna[:i] + gerar_frase(1) + dna[i + 1:]
        return dna
    def procriar(self,tamanho):
        global pai,mae
        temp = []
        quantidade_pop = len(self.lista)
      
        for i in range(0,quantidade_pop):
            self.selecao() # Método que seleciona pai e mãe conforme fitness
            string = self.lista[pai].gene
            parte_pai = string[:int(len(string)/2)]
            string = self.lista[mae].gene
            parte_mae = string[int(len(string)/2):]
            temp.append(self.mutacao(parte_pai+parte_mae, 0.2))
            
        for i in range(0, quantidade_pop):
            self.lista[i].gene = temp[i]
        self.geracao += 1
        soma_pesos= 0

def main():
    print("\n\tFeito por Rafael Faustini")
    print("——————————————————————————————————————————————")
    print("Essa aplicação está sujeita a bugs, sinta-se livre a corrigi-los no git ou reporta-los")
    print("———————————————————————————————————————————————")
    try:
       tamanho = 500
    except:
       print("———————————————————————————————————————————————")
       print("Tamanho inválido")
       print("———————————————————————————————————————————————")
       return;
    
    print("———————————————————————————————————————————————")
    frase = str(input("Digite a palavra para a ser descoberta: "))
    pop = populacao(tamanho,frase)
    while(pop.lista[0].gene!= frase):
       pop.fitness(frase)
       pop.procriar(tamanho)
       soma_pesos= 0
       print("Geração "+str(pop.geracao)+": "+pop.lista[0].gene+
       " Fitness: "+str(pop.lista[0].fitness*100)+"%")
       print(pop.lista[0].gene+" "+pop.lista[1].gene+" "+pop.lista[2].gene)
          

    
main()
    
    
    
