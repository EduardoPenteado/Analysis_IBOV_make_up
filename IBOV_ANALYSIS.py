#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import yfinance as yf
import plotly.express as px
from IPython import display
from numpy import average, argmax
from pytrends.request import TrendReq
from os import path
from datetime import datetime

class Stocks_Variation:
    
    def __init__(self):
        # Get the stocks in the csv archieve and transform it in list "self.stocks"
        ibov = pd.read_csv('Ibov_CSV.csv', sep=';', encoding='latin-1', usecols=[0])
        self.stocks = [ibov.iloc[i][0] for i in range(0, len(ibov)-2)]
        
    def PyTrend(self):
        # Looking the google search about all the stocks which componds the IBOVESPA
        start = input('Initial of search (Format:yyyy-mm-dd): ')
        end = input('End of search (Format:yyyy-mm-dd): ')
        try:
            df = pd.read_excel('Ibov_Search'+start+'_'+end+'.xlsx')
            print('This Search has already been done!')
            print('Loading...\n')
        except FileNotFoundError:
            pytrend = TrendReq(hl='BR')
            dataset = []
            for ibov in self.stocks:
                pytrend.build_payload(
                     kw_list=[ibov],
                     cat=0,
                     timeframe=start+' '+end,
                     geo = 'BR')
                data = pytrend.interest_over_time()
                if not data.empty:
                    data = data.drop(labels=['isPartial'],axis='columns')
                    dataset.append(data)
            # Create a DataFrame and save it in an excel file
            result = pd.concat(dataset, axis=1)
            result.to_excel('Ibov_Search'+start+'_'+end+'.xlsx')
            dir_path = path.dirname(path.realpath('Ibov_Search'+start+'_'+end+'.xlsx'))
            print('Table as been saved in '+dir_path)
        self.Most_Searched(start, end)
        self.Peak_Search(start, end)
        
    def Peak_Search(self, start, end):
        df = pd.read_excel('Ibov_Search'+start+'_'+end+'.xlsx')
        print('Peark Search in the period ('+start+' - '+end+')')
        print('dd-mm-yyyy - Stock')
        print('-'*16)
        for j in range(1, len(df.columns)):
            for i in range(0, len(df)):
                if df.iloc[i][j] >= 95:
                    print(df.loc[i].date.strftime('%d-%m-%Y'), end=' - ')
                    print(df.columns[j])
                    
    def Most_Searched(self, start, end):
        # Return the top 10 most searched stocks.
        df = pd.read_excel('Ibov_Search'+start+'_'+end+'.xlsx')
        soma = [sum(df[i]) for i in df.columns if i != 'date']
        max_ = []
        while len(max_) < 20:
            max_total = 0
            for total in soma:
                if soma.index(total) not in max_:
                    if total > max_total:
                        max_total = total
            max_.append(soma.index(max_total))
        soma.insert(0,'Total')
        df.loc[len(df)+1] = soma
        df.index = df.date
        del df['date']
        #Return the median of searches.
        median = (int(sum(df.loc['Total'])/len(df.columns)))
        print('Median of searches: '+str(median))
        # Print the top 10 searched stocks.
        print('Most searched stocks!')
        max_stocks = []
        max_values = []
        for index in range(0, len(max_)):
            print(str(index+1)+'° '+df.columns[max_[index]]+' ('+ str(df[df.columns[max_[index]]][-1])+')')
            max_stocks.append(df.columns[max_[index]])
            max_values.append(df[df.columns[max_[index]]][-1])
        fig = px.bar(x=max_stocks, y=max_values, labels=dict(x='Stocks', y='Searchs'))
        fig.show()
        
    def Stock_Treemap(self):
        period_ = str(input('Insert the period to plot the Treemap [day, month, ytd]:')).lower()
        if period_ == 'day':
            period_ = '2d'
        elif period_ == 'month':
            period_ = '1mo'
        else:
            period_ = 'ytd'
        var_neg, var_pos = [], []
        error = []
        i = 1
        for stock in self.stocks:
            print('Loading '+ str(int(100*i/len(self.stocks)))+' %')
            price = yf.download(stock+'.SA',period=period_)
            #Remove nan values
            price.dropna(inplace=True)
            try:
                variation = round(((price['Close'][-1]-price['Close'][0])/price['Close'][0])*100,2)
                if variation >= 0:
                    var_pos.append((stock, variation))
                else:
                    variation = variation * -1
                    var_neg.append((stock, variation))
            except Exception:
                error.append(stock)
            display.clear_output(wait=True)
            i += 1
        print('Not Found: '+' - '.join(map(str, error)))
        #Transforming the Data in a DataFrame, which as been sorted descending and return the first 10 most variables.
        df_pos = pd.DataFrame.sort_values(pd.DataFrame(var_pos, columns=['Código', 'Variação']), by="Variação", ascending=False)[0:15]
        df_neg = pd.DataFrame.sort_values(pd.DataFrame(var_neg, columns=['Código', 'Variação']), by='Variação')[0:15]
        print('\nVariação entre '+ price.index[0].strftime("%d/%m/%Y")+' a '+price.index[-1].strftime('%d/%m/%Y'))
        # Plotting the Treemap
        fig_pos = px.treemap(df_pos, path=['Código','Variação'], values='Variação',
                                color ='Variação',
                                color_continuous_scale='greens',
                                title='As '+str(len(df_pos))+' maiores variações <b>Positivas</b> das ações que compõem o índice Ibovespa.')
            
        fig_neg = px.treemap(df_neg, path=['Código', 'Variação'], values='Variação',
                            color ='Variação',
                            color_continuous_scale='reds',
                            title='As '+str(len(df_neg))+' maiores variações <b>Negativas</b> das ações que compõem o índice Ibovespa.')
        # Displaying the figures
        fig_pos.show()
        fig_neg.show()
        
stock = Stocks_Variation()
stock.Stock_Treemap()
stock.PyTrend()

