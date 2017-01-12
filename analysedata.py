import matplotlib.pyplot as plt
from collections import Counter
from pymongo import MongoClient
from datetime import datetime
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.dates import MONDAY


######################################################
# Example query - getting distribution of modalities #
######################################################


def get_modality_dist(pat_dose_ests):
    modality_list = []
    for post in pat_dose_ests.find({},{"Type":1}):
        if post['Type']:
            modality_list.append(post['Type'])

    D = Counter(modality_list)
    plt.bar(range(len(D)), D.values(), align='center')
    plt.xticks(range(len(D)), D.keys())
    plt.ylabel('Modalities')
    plt.title('Patient dose estimates: Modalities')
    plt.show()

########################################################################
# Example query - scatter plot of overexposure factors for CT vs. date #
########################################################################


def get_overexposure_ct(pat_dose_ests):
    data_list = []
    dates_list = []
    for post in pat_dose_ests.find({"CT": "x"}, {"Overexposure factor": 1, "Date": 1}):
        if post['Overexposure factor']:
            data_list.append(float(post['Overexposure factor']))
            dates_list.append(datetime.strptime(post['Date'], '%d/%m/%Y'))

    mondays = WeekdayLocator(MONDAY)
    months = MonthLocator(range(1, 13), bymonthday=1, interval=3)
    monthsFmt = DateFormatter("%b '%y")

    fig, ax = plt.subplots()
    plt.plot(dates_list, data_list,marker=(5, 0))
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.xaxis.set_minor_locator(mondays)
    ax.autoscale_view()
    ax.grid(True)
    fig.autofmt_xdate()
    plt.ylabel('Overexposure factor')
    plt.ylabel('Date')
    plt.title('Patient dose estimates: Overexposure factors')
    plt.show()

def count_modalities(pat_dose_ests):
    ct_count = pat_dose_ests.count({'$or':[{'ct':'X'},{'ct':'x'}]})
    dxr_count = pat_dose_ests.count({'$or':[{'dxr':'X'},{'dxr':'x'}]})
    fluoro_count = pat_dose_ests.count({'$or':[{'fluoro':'X'},{'fluoro':'x'}]})
    nm_count = pat_dose_ests.count({'$or':[{'nuc med':'X'},{'nuc med':'x'}]})
    rt_count = pat_dose_ests.count({'$or':[{'rt':'X'},{'rt':'x'}]})
    modality_list = ['CT','DXR','Fluoro','Nuc Med','RT']
    data_list = [ct_count,dxr_count,fluoro_count,nm_count,rt_count]
    plt.bar(range(len(data_list)), data_list, align='center')
    hfont = {'fontname': 'Gill Sans'}
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.xticks(range(len(modality_list)), ['CT','DXR','Fluoro','Nuc Med','RT'], fontsize=16,**hfont)
    plt.ylabel('# cases', fontsize=16,**hfont)
    plt.title('Patient dose estimates: Modalities', fontsize=22,**hfont)
    plt.savefig("./figs/modality_count.png", bbox_inches="tight")
    plt.show()

def main():
    client = MongoClient()
    db = client.pat_dose_ests_db
    pat_dose_ests = db.pat_dose_ests
    # get_modality_dist(pat_dose_ests)
    # get_overexposure_ct(pat_dose_ests)
    count_modalities(pat_dose_ests)
if __name__ == '__main__':
    main()
