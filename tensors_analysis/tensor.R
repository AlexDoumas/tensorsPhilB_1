# load data. 
mydata = read.csv('AllData768CleanResorted.csv')
# there's a weird thing where pred similarity loads as a non-convertable factor, so fix that by converting to char, then to float.
mydata$PredicateSimilarity = as.numeric(as.character(mydata$PredicateSimilarity))
mydata$PredicateSimilarity[7301] = 1.0

# scale ratings ($RATING.3) from 0 to 100. 
mydata$RATING.3 = (mydata$RATING.3+100)/2

# create bins of pred (and noun) similarity. 
# first, 0-1 in bins of 0.2. 
predBins = c()
for (i in mydata$PredicateSimilarity) {
  if (i <= .2) {
    predBins = c(predBins,1)
  }
  if (i > .2 & i <=.4) {
    predBins = c(predBins,2)
  }
  if (i > .4 & i <= .6) {
    predBins = c(predBins,3)
  }
  if (i > .6 & i <=.8) {
    predBins = c(predBins,4)
  }
  if (i >= .8) {
    predBins = c(predBins,5)
  }
}
nounBins = c()
for (i in mydata$NounSimilarity) {
  if (i <= .2) {
    nounBins = c(nounBins,1)
  }
  if (i > .2 & i <=.4) {
    nounBins = c(nounBins,2)
  }
  if (i > .4 & i <= .6) {
    nounBins = c(nounBins,3)
  }
  if (i > .6 & i <=.8) {
    nounBins = c(nounBins,4)
  }
  if (i >= .8) {
    nounBins = c(nounBins,5)
  }
}
# and add back to data set.
mydata$PredBins = predBins
mydata$NounBins = nounBins
# create adj and verb sets.
mydatvb = subset(mydata, mydata$PredicateType=='V')
mydataj = subset(mydata, mydata$PredicateType=='A')


fit = lmer(RATING.3~ NounBins * PredBins +(1|Participant.), data = mydata)

# simplest possible models. 
fit = lmer(RATING.3~ NounSimilarity * PredicateSimilarity +(1|Participant.), data = mydata)
fit1 = lmer(RATING.3~ NounSimilarity + PredicateSimilarity +(1|Participant.), data = mydata)
fit_null = lmer(RATING.3~ (1|Participant.), data = mydata)
anova(fit, fit1)
multilevelR2(fit)
multilevelR2(fit1)
multilevelR2(fit_null)
fit = lmer(RATING.3~ NounSimilarity + PredicateSimilarity + NounSimilarity:PredicateSimilarity +(1|Participant.), data = mydata)
fit1 = lmer(RATING.3~ NounSimilarity + PredicateSimilarity +(1|Participant.), data = mydata)
anova(fit, fit1)

# look for interaction on participant level. 
part = unique(mydata$Participant.)
datp1 = subset(mydata, mydata$Participant.==part[2])
fit_full = lm(RATING.3~ NounBins * PredBins, data=datp1)
summary(fit_full)

# boxplot of means by bin.
psim1p1 = subset(mydata, mydata$PredBin==1)
boxplot(psim1p1$RATING.3~psim1p1$NounBins)
psim1p1 = subset(mydatvb, mydatvb$PredBin==4)
boxplot(psim1p1$RATING.3~psim1p1$NounBins)
psim1p1 = subset(mydataj, mydataj$PredBin==1)
boxplot(psim1p1$RATING.3~psim1p1$NounBins)

nsim1 = subset(mydata, mydata$NounBin==1)
boxplot(nsim1$RATING.3~nsim1$PredBins)

# plots of regression lines.
plot(mydata$NounBins, mydata$RATING.3)
abline(lm(RATING.3 ~ NounBins, data = subset(mydata, mydata$PredBins==5)))
lines(lowess(mydata$NounBins, mydata$RATING.3))
datp5 = subset(mydata, mydata$PredBins == 5)
lines(lowess(datp5$NounBins, datp5$RATING.3))
datp4 = subset(mydata, mydata$PredBins == 4)
lines(lowess(datp4$NounBins, datp4$RATING.3))
datp3 = subset(mydata, mydata$PredBins == 3)
lines(lowess(datp3$NounBins, datp3$RATING.3))

# is it just low rated preds that fuck us? 
fit = lmer(RATING.3~ as.factor(NounBins) * as.factor(PredBins) +(1|Participant.), data = subset(mydata, mydata$PredBins != 1 & mydata$NounBins != 1))
fit1 = lmer(RATING.3~ as.factor(NounBins) + as.factor(PredBins) +(1|Participant.), data = subset(mydata, mydata$PredBins != 1 & mydata$NounBins != 1))
anova(fit, fit1)

fit = lmer(RATING.3~ NounBins * PredBins +(1|Participant.), data = subset(mydata, mydata$PredBins != 1 & mydata$NounBins != 1))
fit1 = lmer(RATING.3~ NounBins + PredBins +(1|Participant.), data = subset(mydata, mydata$PredBins != 1 & mydata$NounBins != 1))
anova(fit, fit1)

# make proxies to time vs. multiplicative binding using similarity scores. 
additive = mydata$PredicateSimilarity+mydata$NounSimilarity
mult = mydata$PredicateSimilarity*mydata$NounSimilarity
mydata$additive = additive
mydata$mult = mult
fitadd = lmer(RATING.3~ additive +(1|Participant.), data = mydata)
fitmult = lmer(RATING.3~ mult +(1|Participant.), data = mydata)
anova(fitadd, fitmult)
multilevelR2(fitadd)
multilevelR2(fitmult)

# noun similarity vs. pred similarity
fitnoun = lmer(RATING.3~ NounSimilarity+(1|Participant.), data = mydata)
fitverb = lmer(RATING.3~ PredicateSimilarity +(1|Participant.), data = mydata)
anova(fitnoun, fitverb)

# simplest possible models correcting for pred type. 
fit = lmer(RATING.3~ NounBins * PredBins +(1|Participant.), data = subset(mydata, mydata$PredicateType=='V' & mydata$NounBins != 1))
fit1 = lmer(RATING.3~ NounBins + PredBins +(1|Participant.), data = subset(mydata, mydata$PredicateType=='V' & mydata$NounBins != 1))
anova(fit, fit1)

# playing around with additive and multiplicative divergent cases.
# normalise additive to between 0 and 1. 
mydata$addnorm = mydata$additive/2
mydata$diff = mydata$addnorm-mydata$mult
mydata_diff = subset(mydata, mydata$diff > .4)
fitadd = lmer(RATING.3~ addnorm +(1|Participant.), data = mydata_diff)
fitmult = lmer(RATING.3~ mult +(1|Participant.), data = mydata_diff)
anova(fitadd, fitmult)

# for subjects
fits1a = lm(RATING.3 ~ additive, data = subset(mydata, mydata$Participant.==5))
fits1m = lm(RATING.3 ~ mult, data = subset(mydata, mydata$Participant.==5))
summary(fits1a)
summary(fits1m)
for (i in unique(mydata$Participant.)) {
  fitsa = lm(RATING.3 ~ additive, data = subset(mydata, mydata$Participant.==i))
  fitsm = lm(RATING.3 ~ mult, data = subset(mydata, mydata$Participant.==i))
  print(c(summary(fitsa)$r.squared, summary(fitsm)$r.squared))
}


