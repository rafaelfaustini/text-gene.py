import random
import string

#Variaveis Globais
soma_pesos=0
pai = 0
mae = 0


def gerar_frase(length): #Gera uma palavra aleatória e seu parametro é o tamanho
   return ''.join(random.choice(string.printable) for i in range(length))
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
            self.lista[i].fitness = similaridade(self.lista[i].gene,frase)
            self.lista.sort(key=lambda self: self.fitness, reverse=True)
            soma_pesos += self.lista[i].fitness
    def selecao(self):
        global soma_pesos
        peso_aleatorio1 = abs(int(random.uniform(1, soma_pesos)))
        
        peso_aleatorio2 = abs(int(random.uniform(1, soma_pesos)))
        
        global pai,mae
        quantidade_pop = len(self.lista)
        for i in range(0,quantidade_pop):
   
            peso_aleatorio1 -= self.lista[i].fitness
            
            pai = peso_aleatorio1
            
            if(peso_aleatorio1 <= 0):
               pai = 0
            
            peso_aleatorio2 -= self.lista[i].fitness
            mae = peso_aleatorio2
            if(peso_aleatorio2 <= 0):
               mae = 0  
    def mutacao(self,dna, taxa):
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
            self.selecao()
            string = self.lista[pai].gene
            parte_pai = string[:int(len(string)/2)]
            string = self.lista[mae].gene
            parte_mae = string[int(len(string)/2):]
            temp.append(self.mutacao(parte_pai+parte_mae, 0.01))
            
        for i in range(0, quantidade_pop):
            self.lista[i].gene = temp[i]
        self.geracao += 1

def main():
    print("\n\tFeito por Rafael Faustini")
    print("——————————————————————————————————————————————")
    print("Essa aplicação é sujeita a bugs, sinta-se livre a corrigi-los no git ou reporta-los")
    print("———————————————————————————————————————————————")
    print("\tÉ recomendado um valor menor do que 2000")
    tamanho = int(input("Digite o tamanho da população: "))
    print("———————————————————————————————————————————————")
    print("\tNessa versão de testes é recomendado uma palavra menor ou igual a 10 caracteres")
    frase = str(input("Digite a palavra para a ser descoberta: "))
    pop = populacao(tamanho,frase)
    while(pop.lista[0].gene!= frase):
       pop.fitness(frase)
       pop.procriar(tamanho)
       print("Geração "+str(pop.geracao)+": "+pop.lista[0].gene+
       " Fitness: "+str(pop.lista[0].fitness*100))
          

    
main()
    
    
    
