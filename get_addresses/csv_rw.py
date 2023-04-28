import csv
class CSVrw:
    def __init__(self,csvname):
        self.csvname = csvname
        self.rows = []
        
    def append_row(self,fields):
        with open(self.csvname,'a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            
    def read_rows(self):
        with open(self.csvname) as csvfile:
            reader = csv.reader(csvfile,delimiter = ';')
            for row in reader:
                self.rows.append(row)
                
    def delete_rows(self):
        with open(self.csvname) as csvfile:
            reader = csv.reader(csvfile,delimiter = ';')
            
        with open(self.csvname,'w',newline='') as csvfile:
            writer = csv.writer(csvfile,delimiter=';')
            for r in range(20):
                writer.writerow(['',''])
                
    def write_rows(self,rows):
        with open(self.csvname,'w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            for n in range(len(rows)) :
                writer.writerow(rows[n])
            