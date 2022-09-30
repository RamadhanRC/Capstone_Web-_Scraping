from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'lister-list'})
row = table.find_all('h3', attrs={'class':'lister-item-header'})
judul = table.find_all('h3', attrs={'class':'lister-item-header'}) 
rating = table.find_all('div', attrs={'class':'ratings-bar'})

row_length = len(row)

temp = [] #initiating a list 

temp = [] #initiating a tuple

for i in range(0, row_length):

#scrapping process
    Title = judul[i].find('a').text
    IMDB_Rating = rating[i].find('meta', attrs={'itemprop':'ratingValue'})['content']
    Vote = rating[i].find('meta', attrs={'itemprop':'ratingCount'})['content']
    MetaScore = rating[i].find_all('span', attrs={'class':'metascore favorable'})
    if len(MetaScore) > 0:
        MetaScore = rating[i].find_all('span', attrs={'class':'metascore favorable'})[0].text.strip()
    else:
        MetaScore = "0"

        
    temp.append((Title,IMDB_Rating,MetaScore,Vote))

temp = temp[::-1]

#change into dataframe
Data_Film = pd.DataFrame(temp, columns = ('Title','IMDB_Rating','MetaScore','Vote'))

#insert data wrangling here
Data_Film[['IMDB_Rating','MetaScore']] = Data_Film[['IMDB_Rating','MetaScore']].astype('float64')
Data_Film['Vote'] = Data_Film['Vote'].astype('int64')
dfRating=Data_Film.sort_values(by= 'IMDB_Rating', ascending=True).tail(7)
dfScore=Data_Film.sort_values(by= 'MetaScore', ascending=True).tail(7)
dfVote=Data_Film.sort_values(by= 'Vote', ascending=True).tail(7)

X_Rating=dfRating['Title']
Y_Rating= dfRating['IMDB_Rating']

X_Score=dfScore['Title']
Y_Score=dfScore['MetaScore']

X_Vote=dfVote['Title']
Y_Vote=Score=dfVote['Vote']

#end of data wranggling 

@app.route("/")
def index(): 
	card_data = f'{Data_Film["IMDB_Rating"].mean().round(2)}' #be careful with the " and ' 
	# generate plot
	#ax = df.plot.barh(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	plt.clf()
	plt.barh(X_Rating,Y_Rating)
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True, bbox_inches='tight')
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_rating = str(figdata_png)[2:-1]

	plt.clf()
	plt.barh(X_Score,Y_Score)
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True, bbox_inches='tight')
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_score = str(figdata_png)[2:-1]

	plt.clf()
	plt.barh(X_Vote,Y_Vote)
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True, bbox_inches='tight')
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_vote = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_rating=plot_rating,
		plot_score=plot_score,
		plot_vote=plot_vote
		)


if __name__ == "__main__": 
    app.run(debug=True)