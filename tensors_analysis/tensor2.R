# load in data. 
mydata = read.csv('tensor_data.csv')
# there's a weird thing where pred similarity loads as a non-convertable factor, so fix that by converting to char, then to float.
mydata$PredicateSimilarity = as.numeric(as.character(mydata$PredicateSimilarity))
mydata$PredicateSimilarity[7301] = 1.0

# scale ratings ($RATING.3) from 0 to 100. 
mydata$RATING.3 = (mydata$RATING.3+100)/2

# scale ratings of human pred and noun sims to 0 to 100. 
mydata$hum_pred_sim = (mydata$hum_pred_sim+300)/600
mydata$hum_noun_sim = (mydata$hum_noun_sim+300)/600

# simplest possible models. 
fit_int = lmer(RATING.3~ hum_noun_sim * hum_pred_sim +(1|Participant.), data = mydata)
fit_simple = lmer(RATING.3~ hum_noun_sim + hum_pred_sim +(1|Participant.), data = mydata)
anova(fit_int, fit_simple)
multilevelR2(fit_int)
multilevelR2(fit_simple)

# mutiplicative vs. additive binding models. 
mydata$additive_vec = mydata$PredicateSimilarity+mydata$NounSimilarity
mydata$mult_vec = mydata$PredicateSimilarity*mydata$NounSimilarity
mydata$additive_hum = mydata$hum_pred_sim+mydata$hum_noun_sim
mydata$mult_hum = mydata$hum_pred_sim*mydata$hum_noun_sim
fit_add_vec = lmer(RATING.3~ additive_vec +(1|Participant.), data = mydata)
fit_mult_vec = lmer(RATING.3~ mult_vec +(1|Participant.), data = mydata)
fit_add_hum = lmer(RATING.3~ additive_hum +(1|Participant.), data = mydata)
fit_mult_hum = lmer(RATING.3~ mult_hum +(1|Participant.), data = mydata)
anova(fit_add_vec, fit_mult_vec)
anova(fit_add_hum, fit_mult_hum)
multilevelR2(fit_add_vec)
multilevelR2(fit_mult_vec)
multilevelR2(fit_add_hum)
multilevelR2(fit_mult_hum)
fit_both = lmer(RATING.3~ additive_hum + mult_hum +(1|Participant.), data = mydata)
anova(fit_add_hum, fit_both)
multilevelR2(fit_add_hum)
multilevelR2(fit_both)




