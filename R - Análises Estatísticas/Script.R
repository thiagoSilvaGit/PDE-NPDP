# Selecionar diretório, no RStudio não é necessário que seja feito por linha de comando
wd = "/home/thiago/Dropbox/Pesquisas/Ativas/PDE\ -\ NDPP/Git-Python/PDE-NPDP"
setwd(wd)

# lendo o arquivo de saida
saida = read.csv("teste_saida.txt",sep=",")

str(saida)
saida$X=NULL

# TODO
#1-Estatística descritiva
# Comando summary() - Ex: summary(saida$custoSim)
#2- Fazer o Histograma 
# Comando hist() - Ex: hist(saida$custoSim)
#3- Fazer correlação entre a v0 e as variáveis
# Comando cor(,) - Ex:cor(saida$v0,saida$custoSim)
#4- Fazer um plot v0 vs Y: Ex: plot(saida$v0,saida$custoSim)
#5 - heatmap 
##Comando
##library(psych)
##library(ggplot2)
##library(reshape2)
#corsaida = cor(saida[,c(2,10:15)])# correlação das variáveis de saida
#sortedCor = mat.sort(corsaida) # ordenação
#meltedCor = melt(sortedCor) # transformar no formato de matriz(data.frame) 
#qplot(x=Var1, y=Var2, data=meltedCor, fill=value, geom="tile")
#6 - regressão linear e linear múltipla
#lm(formula, data, subset, weights, na.action,
 #  method = "qr", model = TRUE, x = FALSE, y = FALSE, qr = TRUE,
 #  singular.ok = TRUE, contrasts = NULL, offset, …) 
# Ex: lmV1 = lm(v0~custoSim, data = saida)
# summary(lmV1)

###SAIDA:
#lm(formula = v0 ~ custoSim, data = saida)

#Residuals:
#    Min      1Q  Median      3Q     Max 
#-64.181   0.831   4.289   6.900  14.494 

#Coefficients:
#            Estimate Std. Error t value Pr(>|t|)    
#(Intercept) 64.25486    0.97858  65.661   <2e-16 ***
#custoSim    -0.03048    0.02180  -1.398    0.162    
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1 -> referente a ultima coluna da tabela de coeficientes (até 0.05)

#Residual standard error: 13.67 on 1998 degrees of freedom
#Multiple R-squared:  0.0009773,	Adjusted R-squared:  0.0004773 -> Qto maior, melhor 
#F-statistic: 1.955 on 1 and 1998 DF,  p-value: 0.1623 -> qto menor melhor (<0.05)

# Ex2: lmV2 = lm(v0~valorSim+custoSim, data = saida)
# summary(lmV2)

