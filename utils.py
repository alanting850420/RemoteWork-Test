import re
from datetime import datetime


def sep(s, thou=",", dec="."):
    try:
        integer, decimal = s.split(".")
    except:
        integer = s
        decimal = ""
    integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
    while len(decimal) > 0 and decimal[-1:] == "0":
        decimal = decimal[:-1]
    if len(decimal) > 0:
        return integer + "." + decimal
    return integer


def get_html_template(body):
    return """
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Alan Table</title>

            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                }

                .form-header {
                  background-color: #173862;
                  padding-top: 12px;
                  padding-bottom: 12px;
                }

                .form-header span {
                  color: #ffffff;
                  font-size: 20px;
                  padding: 8px;
                }

                .highlight {
                  color: red;
                  vertical-align: initial;
                }

                .block-title {
                    position: relative;
                    overflow: hidden;
                    margin: 0;
                    white-space: var(--f7-block-title-white-space);
                    text-align: center;
                    text-overflow: ellipsis;
                    text-transform: var(--f7-block-title-text-transform);
                    color: var(--f7-block-title-text-color);
                    font-size: var(--f7-block-title-font-size,inherit);
                    font-weight: var(--f7-block-title-font-weight);
                    line-height: var(--f7-block-title-line-height);
                    margin-top: var(--f7-block-margin-vertical);
                    margin-bottom: var(--f7-block-title-margin-bottom);
                    margin-left: calc(var(--f7-block-padding-horizontal) + var(--f7-safe-area-left));
                    margin-right: calc(var(--f7-block-padding-horizontal) + var(--f7-safe-area-right))
                }

                .col-17 {
                    width: 16%;
                }

                .col-50 {
                    width: 50%;
                }

                .data-table {
                    overflow-x: auto;
                }

                .data-table table, table.data-table {
                    width: 100%;
                    border: none;
                    padding: 8px;
                    margin: 0;
                    border-collapse: collapse;
                    text-align: left;
                    font-family: -apple-system, BlinkMacSystemFont, sans-serif, PingFang TC;
                    font-size: 28px;
                }

                .data-table tbody td, .data-table tbody th {
                    height: auto;
                }

                td, th {
                    text-align: center;
                }

                tr {
                    height: 50px;
                }

                .waterMark {
                    text-align:right;
                    position:fixed;
                    width:100%;
                    height:100%;
                    z-index:-9999;
                    pointer-event:none;
                    font-size:5em;
                    font-weight:bold;
                    color:#EDEDED;
                    padding-left: 0;
                }

                .waterMark-inner{
                    -webkit-transform:rotate(-10deg);
                    line-height:200px;
                    margin-top:200px;
                    text-align:justify;
                    text-align-last:justify;
                }

                .waterMark-inner:nth-child(2n){
                    -webkit-transform:rotate(10deg);
                }
            </style>
        </head>
    """ + body + \
           """
    </html>
        """


def adam_to_html(my_str, data):
    color = lambda x: "red" if x > 0 else "green"
    my_type = lambda x: "📈" if x > 0 else "📉"
    date = data["date"]
    close = data["close"]
    open = data["open"]
    high = data["high"]
    low = data["low"]
    vol = data["vol"]
    change = round(float(data["change"].replace("%", "")), 2)
    return my_str.format(type=my_type(change),
                         date=date,
                         close=sep(close),
                         open=sep(open),
                         high=sep(high),
                         low=sep(low),
                         vol=sep(vol),
                         color_change=color(change),
                         change=change)


def get_html_body(historic_data):
    html = ""
    for info in historic_data:
        html += adam_to_html("""
                        <tr>
                            <td style="font-size:32px">{type}</td>
                            <td>{date}</td>
                            <td>{close}</td>
                            <td>{open}</td>
                            <td>{high}</td>
                            <td>{low}</td>
                            <td>{vol}</td>
                            <td style="color: {color_change};">{change} %</td>
                        </tr>
        """, info)

    dict = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "html": html
    }

    body = """
        <body>

            <div class="waterMark">
                <div>
                    <img src="https://i.imgur.com/RE6gsMX.jpg" style="opacity: 0.5;">
                </div>
                <div class="waterMark-inner" style="height:15%"> Create By Alan Ting </div>
                <div class="waterMark-inner" style="height:15%"> Create By Alan Ting </div>
                <div class="waterMark-inner" style="height:15%"> Create By Alan Ting </div>
                <div class="waterMark-inner" style="height:15%"> Create By Alan Ting </div>
                <div class="waterMark-inner" style="height:15%"> Create By Alan Ting </div>
                <div class="waterMark-inner" style="height:15%"> Create By Alan Ting </div>
            </div>
            <div  style="margin:28px">
                <span class="highlight" style="font-size:28px">{date}</span><br><br>
                <span style="font-size:28px" id="name">Alan Ting:</span><br><br>
                <div class="block" style="padding-top:32px">
                    <span class="highlight" style="font-size:28px">歷史資料</span><br><br>
                    <div class="data-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>漲跌</th>
                                    <th>日期</th>
                                    <th>收盤價</th>
                                    <th>開盤價</th>
                                    <th>最高價</th>
                                    <th>最低價</th>
                                    <th>交易量</th>
                                    <th>漲跌幅</th>
                                </tr>
                            </thead>
                            <tbody>
                                {html}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </body>
    """.format(**dict)
    return body
