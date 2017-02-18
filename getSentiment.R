library(RCurl)
library(httr)
#Check API Status
#POST(url=paste("http://gateway-a.watsonplatform.net/calls/info/GetAPIKeyInfo?apikey=18c6890a2dbe7aeedab646b94d219a0062ffe1aa&outputMode=json"))


#read file
file<-read.csv("realDonaldTrump_tweets.csv",sep = ",")

#View(file)

file<-file[1:100, ]

#set api parameters
api_feature = "TextGetEmotion"
alchemy_url = "https://watson-api-explorer.mybluemix.net/alchemy-api/calls/text/"
api_key = "18c6890a2dbe7aeedab646b94d219a0062ffe1aa"
output_mode = "json"

es <- data.frame("1" = double(6), "2" = double(6),"3" = double(6),"4" = double(6),"5" = double(6), stringsAsFactors=FALSE)

for(i in 1:nrow(file))
{
  TEXT= as.character(file[i,3])
  TEXT = URLencode(TEXT)
  query = paste(alchemy_url,api_feature,"?apikey=",api_key,"&text=",TEXT,"&outputMode=",output_mode, sep="")
  response = POST(query)
  a=content(response)
  ang<- a$docEmotions$anger
  dis<- a$docEmotions$disgust
  fear<- a$docEmotions$fear
  joy<- a$docEmotions$joy
  sad<- a$docEmotions$sadness
  #es<-rbind(es,c(joy,fear,sad,dis,ang))
  if(is.null(joy))
  {
    es<-rbind(es,c("0","0","0","0","0"))
  }
  else
  {
    es<-rbind(es,c(joy,fear,sad,dis,ang))
  }
  Sys.sleep(4)
}



#nrow(file)
es<- es[-(1:6),]


names(es) <- c("joy","fear","sadness","disgust","anger")
View(es)
output<-cbind(file,es)

View(output)

write.csv(output,"EmotionalData.csv",row.names = FALSE)

