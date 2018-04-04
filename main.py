import random
import string

#Variaveis Globais
soma_pesos=0
pai = 0
mae = 0
taxa_mutacao = 0.05
soma = 0
lembranca = []



def gerar_frase(length): #Gera uma palavra aleatória e seu parametro é o tamanho
   return ''.join(random.choice(string.printable) for i in range(length))
def similaridade(string1,string2): #Checa a porcentagem de similaridade entre strings
    count = 0
    for i in range(min(len(string1), len(string2))):
        if string1[i] == string2[i]:
            count += 1
    return count/len(string1)


    
class elemento:
    gene = ''
    fitness= 0
class pensamento:
    acao=0
    mediafit=0.0
    

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
            self.lista[i].fitness = pow(similaridade(self.lista[i].gene,frase),4)
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
    def taxa_dinamica(self,tax):
         global soma
         if(len(lembranca)>1 and len(lembranca)<self.geracao/100 and (self.geracao/100).is_integer() ):
            print("Tamanho Lista "+str(len(lembranca)))
            print("Valor Geracao -2 "+str((self.geracao/100)-2)) 
            if lembranca[int((self.geracao/100)-3)].mediafit - lembranca[int(self.geracao/100-2)].mediafit > 0:
                pulo = self.lista[(self.geracao/1000)-1].escolha         
         if (self.geracao/100).is_integer() and len(lembranca)<self.geracao/100:
             elemento_lembranca = pensamento
             soma/= 100
             elemento_lembranca.mediafit= soma
             soma=0
             pulo= None
             #if(len(lembranca)> 1 or pulo!= None):
             escolha = random.randint(0,2)
             if(escolha == 0 or pulo==0): # Diminuir Mutacao
                   elemento_lembranca.acao = 0
                   lembranca.append(elemento_lembranca)
                   futuro = random.uniform(tax-0.04,tax)
                   print("Acho que precisamos diminuir a mutação")
                   file = open("mutacao.txt","a")
                   file.write("Geração:"+str(self.geracao)+"\n")
                   file.write("Mutacao:"+str(futuro)+"\n\n")
                   file.close()
                   return futuro
             if(escolha == 1 or pulo ==1):
                   elemento_lembranca.acao = 1
                   lembranca.append(elemento_lembranca)
                   futuro= random.uniform(tax,tax+0.08)
                   print("Acho que precisamos aumentar a mutação")
                   file = open("mutacao.txt","a")
                   file.write("Geração:"+str(self.geracao)+"\n")
                   file.write("Mutacao:"+str(futuro)+"\n\n")
                   file.close()
                   return random.uniform(tax,tax+0.08)
             if(escolha == 2 or pulo ==2):
                   elemento_lembranca.acao = 2
                   lembranca.append(elemento_lembranca)
                   futuro= tax
                   print("A mutação tá boa assim")
                   file = open("mutacao.txt","a")
                   file.write("Geração:"+str(self.geracao)+"\n")
                   file.write("Mutacao:"+str(futuro)+"\n\n")
                   file.close()
                   return tax
         soma += self.lista[0].fitness
         return tax
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
            temp.append(self.mutacao(parte_pai+parte_mae, self.taxa_dinamica(taxa_mutacao)))
        for i in range(0, quantidade_pop):
            self.lista[i].gene = temp[i]
        self.geracao += 1
        soma_pesos= 0

def main():
    print("\n\tFeito por Rafael Faustini")
    print("——————————————————————————————————————————————")

    print("Essa aplicação está sujeita a bugs, sinta-se livre a corrigi-los no git ou reporta-los")
    print("———————————————————————————————————————————————")
    print("\tÉ recomendado um valor menor do que 2000")
    try:
       tamanho = int(input("Digite o tamanho da população: "))
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
       " Fitness: "+str(pop.lista[0].fitness*100))


main()
