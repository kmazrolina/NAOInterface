# -*- encoding: UTF-8 -*-
def getIndex(animTags, tag):
    if tag[0:7] == 'powiedz':
        return 0
    else:
        for i in animTags:
            if i[0] == tag:
                return animTags.index(i)
    


animTags = [
['powiedz','ok','#B2AD72'],
['złość', 'Angry_1', '#CB2805'], 
['strach', 'Fear_1', '#E1AE00'], 
['smutek', 'Exauhsted_2', '#008FE1'], 
['płacz', 'Sad_1', '#073876'], 
['zaskoczenie', 'Surprise_3', '#EB900C'], 
['radość', 'Happy_3', '#11BF08'], 
['zastanawianie się', 'Think_1', '#B3AF33'], 
['ukłon', 'BowShort_1', '#87450D'], 
['brawo', 'Applause_1', '#730D87'], 
['machanie', 'Hey_1', '#CC22A8'], 
['smok','Monster_1', '#7EBD23'],
['picie', 'Drink_1', '#56C1C8'],
['rycerz', 'Knight_1', '#A1250F'],
['śmiech', 'Laugh_3', '#080201'],
['hejnał', 'Trumpet', '#E1D816'],
['śmierć', 'Dead','#090902' ],
['ptak', 'Bird', '#D845A9'],
['zwycięstwo', 'Winner_1', '#3FEE1C']
]
"""
siadanie
wstawanie
spanie  dodac animacje ze spaniem na kucajaco?
 jedzenie
"""



