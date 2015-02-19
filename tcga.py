from flask import Flask, url_for, render_template
from enterz import TCGA
import datetime

app = Flask(__name__)

tcga = TCGA(datetime.datetime(2000,1,1))


@app.route('/')
def my_view():
    tcgaRecord, tcgaData = tcga.records()
    # d = data.next()
    # print(d)
    # for d in tcgaData:
    #     print d['TI']
    #     print d['AU']
    #     print d.get('AB', '')[0:200]
    #     print d['PMID']
    return render_template('tcga.jinja2',
        tcgaRecord = tcgaRecord,
        tcgaData = tcgaData
    )


if __name__ == '__main__':
    app.debug = True
    app.run()