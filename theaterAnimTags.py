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
['smutek', 'Sad_1', '#008FE1'], 
['płacz', 'Sad_2', '#073876'], 
['zaskoczenie', 'Surprise_1', '#EB900C'], 
['szczęście', 'Happy_1', '#11BF08'], 
['śmiech', 'Laugh_2', '#81D80A'], 
['zastanawianie się', 'Think_1', '#B3AF33'], 
['ukłon', 'BowShort_1', '#87450D'], 
['brawo', 'Applause_1', '#730D87'], 
['machanie', 'Hey_1', '#CC22A8'], 
]