from datetime import datetime

class TweetsClean:
    def __init__(self):
        pass
    def clean(self, dict):
        #dict["time_stamp"] = datetime.strptime(dict["time_stamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

        try:
            dict["reply"] = int(dict["reply"].replace(' Respuestas. Respuesta', ''))
        except:
            dict["reply"] = int(dict["reply"].replace(' Respuesta. Respuesta', ''))

        try:
            dict["retweet"] = int(dict["retweet"].replace(' reposts. Repostear', ''))
        except:
            dict["retweet"] = int(dict["retweet"].replace(' repost. Repostear', ''))
            
        dict["like"] = int(dict["like"].replace(" Me gusta. Me gusta", ''))

        try:
            dict["visualizations"] = int(dict["visualizations"].replace(" visualizaciones. Ver estadísticas del post", ''))
        except:
            print(dict["visualizations"].replace(" visualización. Ver estadísticas del post", ''))
        
        return dict
    def its_here(self, data, tweet):
        flag = False
        for data_ in data:
            if data_["tweet"] == tweet:
                flag = True
        return flag

            