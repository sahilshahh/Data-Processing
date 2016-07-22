import csv
import os
import pandas as pd
import matplotlib.pyplot as plt, mpld3

class Data:

    def __init__(self, name):
        self.name = name
        self.stats = []
        self.data_sheet_type()
        self.format_data()
        self.df = self.build_data_frame()

    def format_data(self):
        rows = []
        i = 0
        with open('files/'+self.name+'.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if i == self.info_number:
                    self.stats = row
                if i >= self.data_number:
                    if row:
                        rows.append(row)
                i += 1
        with open('formatted_files/'+ self.name + '_updated_' + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def build_data_frame(self):
        return pd.read_csv('formatted_files/'+ self.name + '_updated_' + '.csv', low_memory=False)

    def data_sheet_type(self):
        if ('RRC' in self.name) or ('SYS' in self.name):
            self.info_number = 4
            self.data_number = 9
        else:
            self.info_number = 0
            self.data_number = 0

class RRC(Data):

    def build_data_frame(self):
        df = pd.read_csv('formatted_files/'+ self.name + '_updated_' + '.csv', low_memory=False)
        df = df[df["#State"] == 0]
        df = df[['Time', 'Total: RRC Connection Request Request Count', 'Total: RRC Connection Request Success Count',
            'Total: RRC Connection Request Failure Count']]
        return df

    def plot_data(self):
        my_plot = self.df.plot(kind='line')
        fig = my_plot.get_figure()
        mpld3.save_html(fig, 'graphs/test.html')
        fig.savefig('graphs/' + self.name+'.png')

class SYS(Data):

    def build_data_frame(self):
        df = pd.read_csv('formatted_files/'+ self.name + '_updated_' + '.csv', low_memory=False)
        df = df[df["#State"] == '0']
        df = df[df["UL-SCH Throughput(kbps)"] != '-']
        df = df[['Time', 'DL-SCH Throughput(kbps)', 'UL-SCH Throughput(kbps)']]
        df['UL-SCH Throughput(kbps)'] = df['UL-SCH Throughput(kbps)'].astype(float)
        return df

    def plot_data(self):
        my_plot = self.df.plot(kind='line')
        fig = my_plot.get_figure()
        mpld3.save_html(fig, 'graphs/test1.html')
        fig.savefig('graphs/' + self.name+'.png')


def get_file_names():
    names = []
    files = []
    with open('C:/Users/ss5399/Desktop/reader/files/files.txt', 'a+') as f:
        f.seek(0)
        for line in f:
            files.append(line)
        for file in os.listdir("C:/Users/ss5399/Desktop/reader/files"):
            if file.endswith(".csv"):
                if file+'\n' in files:
                    continue
                else:
                    f.write(file+'\n')
                    file = file[:-4]
                    names.append(file)
    return names

def main():
    names = get_file_names()
    if names.__len__() != 0:
        for name in names:
            if 'RRC' in name:
                RRC(name).plot_data()
            elif 'SYS' in name:
                SYS(name).plot_data()
    print ('All visuals have been made.')

if __name__ == "__main__":
    main()