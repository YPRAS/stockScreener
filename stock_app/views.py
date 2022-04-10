from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import requests
import yfinance as yf
from .form import TickerForm

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

import pandas as pd
from IPython.display import HTML

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker =request.POST['ticker']
            return HttpResponseRedirect(ticker)
    else:
        form = TickerForm()

    
    url = 'https://newsapi.org/v2/everything?q=(stocks AND indices)&from=&sortBy=popularity&apiKey=0b17f9384f73431fbccaae9972320fae'
    crypto_news = requests.get(url).json()
    print("============================",crypto_news)
    
    a = crypto_news['articles']
    desc =[]
    title =[]
    img =[]
    for i in range(len(a)):
        f = a[i]
        title.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])


    mylist = zip(title, desc, img)

    context={"form":form,'mylist': mylist}
    return render(request, 'accounts/home.html',context)




def ticker(request,tid):
    ticker=''
    longname=''
    price=''
    change_price=''
    percentage=''
    #graph=''
    plt_div=""
    marketcap=''
    bookvalue=''
    peratio=''
    dividendyield=''
    doe=''
    facevalue=''
    pricetobook=''
    traling_eps=''
    sector=''
    annual_report=''
    financial_result=''
    balance_sheet_result=''
    cashflow_result=''

   
    stockInfo = yf.Ticker(tid)
    longname=stockInfo.info['longName']
    price = stockInfo.info['regularMarketPrice']
    marketcap=stockInfo.info['marketCap']
    bookvalue=stockInfo.info['bookValue']
    peratio=stockInfo.info['trailingPE']
    dividendyield=stockInfo.info['dividendYield']
    #roce=stockInfo.info['roce']
    pricetobook=stockInfo.info['priceToBook']
    doe=stockInfo.info['debtToEquity']
    #facevalue=stockInfo.info['faceValue']
    traling_eps=stockInfo.info['trailingEps']
    sector=stockInfo.info['sector']

    todayData = stockInfo.history(period='1d')
    close_price=todayData['Close'][0]

    previousData = stockInfo.history(period='2d')
    open_price=previousData['Close'][0]

    #Change in price
    change_price=round(close_price-open_price,2)

    #Percentage change
    percentage=round((100*(close_price-open_price)/open_price),2)
    

    #graph 
    hist=stockInfo.history(period='1y')
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Candlestick(x=hist.index,
                                open=hist['Open'],
                                high=hist['High'],
                                low=hist['Low'],
                                close=hist['Close'],
                                ))
    
    hist['diff'] = hist['Close'] - hist['Open']
    hist.loc[hist['diff']>=0, 'color'] = 'green'
    hist.loc[hist['diff']<0, 'color'] = 'red'

    fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker={'color':hist['color']}),secondary_y=True)
    fig.update_yaxes(range=[0,700000000],secondary_y=True)
    fig.update_yaxes(visible=False, secondary_y=True)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(showlegend=False)

    #graph=fig.show()
    plt_div = plot(fig, output_type='div')


    annual_report =stockInfo.financials
    financial_result = annual_report.to_html(classes='table table-striped table-bordered table-hover ',float_format='{:10.2f}'.format).replace('<table>','<table style ="margin: 1em">')


    balance_sheet = stockInfo.balance_sheet
    balance_sheet_result = balance_sheet.to_html(classes='table table-striped table-bordered table-hover ',float_format='{:10.2f}'.format)

    cashflow = stockInfo.cashflow
    cashflow_result = cashflow.to_html(classes='table table-striped table-bordered table-hover',float_format='{:10.2f}'.format)


    
    
    context = {'ticker': ticker,
     
     'longname':longname,
     'price':price,
     'change_price':change_price,
     'percentage':percentage,
     'marketcap':marketcap,
     'bookvalue':bookvalue,
     'peratio':peratio,
     'dividendyield':dividendyield,
     'facevalue':facevalue,
     'pricetobook':pricetobook,
     'plt_div':plt_div,
     'traling_eps':traling_eps,
     'doe':doe,'sector':sector,
     'annual_report':annual_report,
     'financial_result':financial_result,
     'balance_sheet_result':balance_sheet_result,
     'cashflow_result':cashflow_result,
     }



    print(longname)
    print(stockInfo)


    # print(type(annual_report))
    
    # result = annual_report.to_html()
    # print(result)
    
    
    # df = df.reset_index()  # make sure indexes pair with number of rows
    #data = dict()
    # for index, row in annual_report.iterrows():
        # print("ROW:", type(row), row, dir(row), " INDEX:", index)
        # print(row['2021-03-31'])

    # print(annual_report.head())
    # for col in annual_report.columns:
    #     data[col.strftime('%d-%m-%Y')] = []
    #     for index, row in annual_report.iterrows():
    #         data[col.strftime('%d-%m-%Y')].append(row[col])
    #     # data.append(datarow)
    # print(data)

    return render(request,'accounts/ticker.html',context)



