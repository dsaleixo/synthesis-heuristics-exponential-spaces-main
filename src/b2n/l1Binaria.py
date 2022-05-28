from b2n.level1 import Level1

class L1Binaria(Level1):

    def __init__(self,rules):
        self.tabela = {}
        for  key in rules:
            if not key.is_terminal():
                self.tabela[key.class_name()]={}
                for acc2 in key.accepted_types:
                    for acc in acc2:
                        self.tabela[key.class_name()][acc]=[None,0]

    def getSemente(self):
        raise Exception('Unimplemented method: getSemente')
    
    def update(self,guia,avaliacao):
        for key, value in self.tabela.items():
            for k,v in value.items():
                if guia.rules[key][k]>0:
                    if self.tabela[key][k][1] == 0:
                        self.tabela[key][k][1]=1
                        self.tabela[key][k][0]=avaliacao
                    else:
                        T =self.tabela[key][k][1]
                        self.tabela[key][k][0] = min(self.tabela[key][k][0],avaliacao)
                        #self.tabela[key][k][0] = (T*self.tabela[key][k][0]+avaliacao)/(T+1)
                        self.tabela[key][k][1]+=1

                
    def to_string(self):
        s=''
        for key, value in self.tabela.items():
            s+= key+'\n'
            for k,v in value.items():
                if v[1] == 0:
                    s+="\tnull\t"+str(v[1])+"\t"+str(key)+"==>"+str(k)  +"\n"
                else:
                    s+="\t"+str(v[0])+"\t"+str(v[1])+"\t"+str(key)+"==>"+str(k)+"\n"
            s+="\n"
        return s

    def printer(self):
        for key, value in self.tabela.items():
            print("%s" % (key))
            for k,v in value.items():
                if v[1] == 0:
                    print("\tnull\t%d\t%s==>%s "% (v[1],key,k))
                else:
                    print("\t%f\t%d\t%s==>%s "% (v[0],v[1],key,k))
            print()