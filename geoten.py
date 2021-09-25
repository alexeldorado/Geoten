##############################################################################
# Instruções para os dados de entrada
##############################################################################

# p_na : posicao do ni­vel d'agua em relacao ao ni­vel do terreno
# Um valor positivo significa Nivel d'agua acima do ni­vel do terreno
# Um valor negativo significa Ni­vel d'agua abaixo do ni­vel do terreno
# Zero significa que o ni­vel d'agua coincide com o ni­vel do terreno
# Quando nao ha ni­vel d'agua preencher com "nao_aplica" com haspas

# n_camadas : numero de camadas de solos diferentes (suporta ate 7)
# cx : par de valores para cada camada em ordem de profundidade 
# onde, [0,0] = [Espessura da camada(m), Peso especi­fico (kN/m3) ]
# Uma camada inexistente deve ser preenchida com [0,0]
# cn : lista compilando as informacoes das camadas

# n_pontos : numero de pontos que se deseja conhecer as tensoes (ate 7 pontos)
# px : posicao do ponto em relacao ao ni­vel do terreno
# Um valor positivo significa que o ponto esta acima do ni­vel do terreno
# Um valor negativo significa que o ponto esta abaixo do ni­vel do terreno
# Zero significa que o ponto coincide com o ni­vel do terreno
# Quando nao ha interesse em um dos pontos preencher com "nao_aplica" com haspas
# Um ponto deverá ser colocado no inicio do nível d'agua, se houver
# Um ponto deverá ser colocado no inicio do nível do terreno
# pn: lista compilando as informacoes dos pontos

# Modelo de conjunto de dados:
# p_na = "nao aplica"
# n_camadas = 0
# c1 = [0,0] 
# c2 = [0,0]      
# c3 = [0,0]        
# c4 = [0,0] 
# c5 = [0,0] 
# c6 = [0,0] 
# c7 = [0,0] 
# cn = [c1,c2,c3,c4,c5,c6,c7]
# n_pontos = 0
# p1  = "nao aplica"
# p2  = "nao aplica"
# p3  = "nao aplica"
# p4  = "nao aplica"
# p5  = "nao_aplica"
# p6  = "nao_aplica"
# p7  = "nao_aplica"
# pn  = [p1,p2,p3,p4,p5,p6,p7]


##############################################################################
# Instruções para plotagem
##############################################################################

# # modulos auxiliares
# import matplotlib.pyplot as plt
# import pandas as pd

# fig, axs = plt.subplots(1, 2, figsize=(7, 7),dpi=100)   

# #Perfil geotécnico
# ax1 = axs[0]
# ax1.set_xlim(0,10) ; ax1.set_ylim(-1*e_solo,(e_total-e_solo))     
# if type(p_na) != str:
#     ax1.scatter(10,p_na,c='blue');ax1.annotate('NA',[8,p_na],c='blue') # nivel d'agua
# ax1.plot([0,10],[0,0],c='black',linewidth=4);ax1.scatter(10,0,c='black');ax1.annotate('NT',[10,0],c='black') # nivel do terreno
# for i in range (n_camadas):
#     ax1.plot([0,10],[cf[i],cf[i]],c='maroon',linewidth=4)
#     ax1.annotate('γ={0:3.1f}kN/m³'.format(cn[i][1]),fontsize=11, xy=(0, (cf[i]+((cn[i][0])/2)))) 
# ax1.set_ylabel('Profundidade (m)',fontsize=14) 
# ax1.set_xticklabels([])
# ax1.grid(True)

# #Tensões
# ax2 = axs[1]
# ax2.set_xlim(0,max(t_total)); ax2.set_ylim(pn[n_pontos-1],pn[0])     
# ax2.plot(t_total,pn[0:n_pontos],c='black',label='Tensão total')
# ax2.plot(poropressao,pn[0:n_pontos],c='blue',label='Poropressão')
# ax2.plot(t_efetiva,pn[0:n_pontos],c='red',label='Tensão efetiva')
# ax2.legend(loc='upper right',fontsize=11, ncol=1, shadow=True, fancybox=True)
# ax2.set_xlabel('tensão (kPa)',fontsize=14);#ax2.set_ylabel('Profundidade (m)',fontsize=16) 
# ax2.set_yticklabels([])
# ax2.grid(True)

# # Tabela
# dados = {'Profundidade (m)':pn[0:n_pontos],'Tensão total(kPa)':t_total,'Poropressão(kPa)':poropressao,'Tensão efetiva(kPa)':t_efetiva}
# tabela_solos = pd.DataFrame(dados)
# print (tabela_solos.to_string(index=False))

##############################################################################
# Funções Geoten
##############################################################################
 
def tensoes (n_camadas, cn, p_na, n_pontos, pn):
    # Recebe:
    # n_camadas: numero de camadas de solos diferentes (ate 7 camadas)
    # cn       : lista compilando as informacoes das camadas
    # p_na     : informacao do ni­vel d'agua
    # n_pontos : numero de pontos que se deseja conhecer as tensoes (ate 7 pontos)
    # pn       : lista compilando as informacoes dos pontos
    # ci       : cotas iniciais das camadas em relacao ao nivel do terreno
    # cf       : cotas finais das camadas em relacao ao nivel do terreno  
    # unidades : kN e metro
    
    #Retorna:
    # e_total     : espessura total do perfil
    # e_solo      : espessura de solo do perfil
    # ci          : cotas iniciais das camadas em relacao ao nivel do terreno
    # cf          : cotas finais das camadas em relacao ao nivel do terreno
    # t_total     : Lista com as tensoes totais nos pontos de interesse 
    # poropressao : Lista com as poropressoes nos pontos de interesse
    # t_efetiva   : Lista com as tensoes efetivas nos pontos de interesse
    # unidades    : kPa e metro      
    
    # Criando as listas necessarias
    gamaw       = 10            #Peso especifico da agua em kN/m3
    t_total     = [0]*n_pontos
    poropressao = [0]*n_pontos
    t_efetiva   = [0]*n_pontos
    e_solo      = 0
    ci          = [0]*n_camadas
    cf          = [0]*n_camadas
    
    # Determinando valores auxiliares    
    for i in range (7):
        e_solo += cn[i][0]
    
    semniveldagua = (e_solo + 1)*-1
    
    if type(p_na) == str:
        p_na = semniveldagua
    else:
        pass   
    
    if p_na > 0:
        e_total = e_solo + p_na
    else:
        e_total = e_solo
    
    # determinando as cotas das camadas em relacao ao nivel do terreno
    ci[0] = 0            # cota inicial da primeira camada
    cf[0] = -1*cn[0][0]  # cota final da primeira camada
    
    for i in range (n_camadas-1):        
        cf [i+1]   = cf[i] - cn[i+1][0]
        ci [i+1]   = cf[i]
       
    # resolvendo a poropressao   
    if p_na != semniveldagua:
        for i in range (n_pontos):        
            if p_na <= pn[i]:
                poropressao [i] = 0        
            else:
                poropressao [i] = (p_na - pn[i])*gamaw            
                
    # resolvendo as tensoes totais e efetivas  
    # qx e a lista de quantidades de cada camada, em ordem, para o ponto px
    # qn e uma lista compilando as informacoes de todos os pontos    
    q1  = [0]*n_camadas
    q2  = [0]*n_camadas
    q3  = [0]*n_camadas
    q4  = [0]*n_camadas
    q5  = [0]*n_camadas
    q6  = [0]*n_camadas
    q7  = [0]*n_camadas    
    qn  = [q1,q2,q3,q4,q5,q6,q7]
    
    for i in range (n_pontos):
       for j in range (n_camadas): 
           if pn[i] >= 0:      
               qn[i][j] = 0   
               t_total[i] =  poropressao [i]       
           else:
               if pn[i] < ci[j] and pn[i] >= cf[j]:
                   qn[i][j] = abs(pn[i]) - abs(ci[j])               
               elif pn[i] <= cf[j]:
                   qn[i][j] = cn[j][0]        
               else:
                   qn[i][j] = 0                                              
               t_total[i] +=  (qn[i][j] * cn[j][1])          
               
       if p_na > 0 and pn[i] <0:
           t_total[i] += p_na*gamaw
       else:
           pass
          
       t_efetiva[i]   = t_total[i] - poropressao [i]
        
    return t_total, poropressao, t_efetiva, e_total, e_solo, ci, cf



