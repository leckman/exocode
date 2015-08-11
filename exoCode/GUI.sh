#!/usr/bin/env python

from Tkinter import *
import tkFileDialog
from PIL import Image,ImageTk
import os
from dataAcq import target_download
import csv
from analysis_script import target_analysis
import display

class Data(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.index=0
        self.initUI()

        self.image_data = {'tam_cat_sample.csv':'FITS/TAM/',
                          'random_catalog_sample+1000.csv':'FITS/RandSample-1000/',
                          'random_catalog_sample+2000.csv':'FITS/RandSample-2000/',
                          'tycho_2mass_wise_XMATCH-POS.csv':'FITS/Full_Cat/'}
        self.num_data = {'tam_cat_sample.csv':'Results/TAM/',
                          'random_catalog_sample+1000.csv':'Results/RandSample_1000/',
                          'random_catalog_sample+2000.csv':'Results/RandSample_2000/',
                          'tycho_2mass_wise_XMATCH-POS.csv':'Results/Full_Cat/'}

    def initUI(self):

        self.parent.title('exocode GUI')
        self.pack(fill=BOTH,expand=1)
        self.frame = Frame(self,relief=RAISED,bd=1)
        self.frame.pack(expand=2,fill=BOTH)
        
        self.data = Frame(self.frame)
        self.data.pack(fill=BOTH,side=LEFT,expand=1)
        top = Frame(self.data,width=40)
        bot = Frame(self.data,height=90)
        top.pack()
        bot.pack(fill=Y)

        self.dwnld = StringVar()
        self.dwnld.set('Checking Download...\nSelect catalog to run')
        self.check = Label(top,textvariable=self.dwnld,anchor=N,justify=LEFT,width=17)
        self.check.pack(side=LEFT,fill=BOTH)
        scrollbar = Scrollbar(bot)
        self.listbox = Listbox(bot, yscrollcommand=scrollbar.set,height=13,width=16)
        scrollbar.pack(side=RIGHT,fill=Y)
        self.listbox.pack(side=LEFT,fill=BOTH)

        scrollbar.config(command=self.listbox.yview)

        csv_frame = Frame(self.frame,width=200,padx=5)
        csv_frame.pack(fill=BOTH,side=LEFT,expand=1)
        csv_title = Frame(csv_frame)
        csv_title.pack(fill=BOTH)
        csv_label = Label(csv_title,text='Data')
        csv_label.pack(fill=BOTH)
        self.csv_table = Frame(csv_frame)
        self.csv_table.pack(fill=BOTH)

        grid = Frame(self.csv_table,width = 210)
        grid.pack(side=LEFT)

        self.l0 = Listbox(grid, height=15,width=210,font=('FreeMono',10))
        self.l0.pack(side=LEFT,fill=BOTH)


        list_titles = ['Image Address','Target Index','Target Right Ascension',
                       'Target Declination','Survey','Band',
                       'Number of Central Blobs','Main Blob Center',
                       'Main Blob Radius','Main Blob Displacement',
                       'Percent Outside Diffraction','Threshold Value',
                       'Percent of Image White','Validation','Error']
        list_titles = [list_titles[0],
                       list_titles[6],list_titles[7],list_titles[8],
                       list_titles[9],list_titles[11],list_titles[12],list_titles[14]]

        list_header = ('Image Address                                     | Number of Central Blobs | Main Blob Center | Main Blob Radius | \
Main Blob Displacement | Threshold Value | Percent of Image White | Error        ')
        self.l0.insert(END,list_header)

        close_button = Button(self,text='Close',command=self.parent.destroy)
        close_button.pack(side=RIGHT,padx=5,pady=5)
        self.catalog = StringVar()
        self.catalog.set('Select Catalog')
        cat_button = Button(self,textvariable=self.catalog,command=self.update_catalog)
        cat_button.pack(side=RIGHT,padx=5,pady=5)

        self.current = StringVar()
        self.current_id = Label(self.data,textvariable=self.current)
        self.img_display = Button(self.csv_table.master,text='Display Next Index',command=self.data_display)
        self.download_button = Button(self.data,text='Click to Download',command=self.data_protocol)

        self.label1 = Label(self.csv_table.master, text="Jump to Index:")
        self.E1 = Entry(self.csv_table.master,width=5)
        self.images = Button(self.csv_table.master,text='Show Target Images',command=self.image_display)


    def update_catalog(self):
        self.download_button.destroy()
        self.listbox.delete(0, END)
        self.l0.delete(1,END)
        self.current.set('')
        self.index=0
        self.catalog_file = tkFileDialog.askopenfilename(initialdir='Catalogs/')
        self.data_container = self.image_data[self.catalog_file.split('/')[-1]]
        self.catalog.set('Catalog: '+self.data_container)

        with open(self.catalog_file,'rb') as f:
            self.num_lines = sum(1 for line in f)
        self.data_button = Button(self.csv_table.master,text='Display New Catalog Data',command=self.data_display)
        for i in range(0,self.num_lines):
            if os.path.isdir(self.data_container+'index-'+str(i)+'/'):
                self.listbox.insert(END,'index-'+str(i)+':   EXISTS')
                if i == self.num_lines-1:
                    self.dwnld.set('\nDownload Complete!')
                    self.check.config(fg='green')
                    
                    self.data_button.pack(side=BOTTOM,fill=X)
            else:
                self.listbox.insert(END,'ERROR')
                self.listbox.insert(END,'MISSING index-'+str(i))
                
                self.download_button = Button(self.data,text='Click to Download',command=self.data_protocol)
		self.download_button.pack(padx=5,pady=5)

                self.dwnld.set('\nDownload Incomplete')
                self.check.config(fg='red')
                break


    def data_protocol(self):
        self.listbox.delete(0,END)
        self.dwnld.set('\nDownloading Now...')
        with open(self.catalog_file,'rb') as csvfile: #rand cat
            reader = csv.reader(csvfile)
            table = [[e for e in r] for r in reader]
        for i in range(self.num_lines):
            target_download(i,self.data_container,table)
            self.listbox.insert(END,'index-'+str(i)+':   EXISTS')
            if i == self.num_lines-1:
                self.dwnld.set('\nDownload Complete!')
                self.check.config(fg='green')
        self.download_button.destroy()
        self.data_button = Button(self.csv_table.master,text='Display New Catalog Data',command=self.data_display)
        self.data_button.pack(side=BOTTOM,fill=X)


    def data_display(self):
        self.data_button.destroy()
        self.l0.delete(1,END)
        full = target_analysis(self.index,self.data_container)[1:]
        full.sort(key=lambda x: x[0])
        
        max_len = {0:49, 1:12, 2:22, 3:18, 4:6, 5:9, 6:23, 7:16,
                   8:16, 9:22, 10:27, 11:15, 12:22, 13:10, 14:24}

        for row in range(len(full)):
            for column in range(len(full[row])):
                full[row][column] = str(full[row][column]) + ' '*(max_len[column]-len(str(full[row][column])))

        formatted = []
        for row in full:
            formatted.append(' | '.join([row[0],row[6],row[7],row[8],
                   row[9],row[11],row[12],row[14]]))

        for line in formatted:
            self.l0.insert(END,line)




        self.index+=1

        self.img_display.pack(padx=5,pady=5,side=LEFT)

        self.current.set('\nDisplaying\nIndex '+str(self.index-1))
	self.current_id.pack(padx=5,pady=5)


        self.label1.pack(side=LEFT,padx=5,pady=5)
        self.E1.pack(side=LEFT)
        self.E1.bind('<Return>',self.input_index)

        self.images.pack(side=RIGHT,padx=5,pady=5)

    def input_index(self,event):
        if int(self.E1.get()) in range(0,self.num_lines):
            self.index = int(self.E1.get())
            self.data_display()  

    def image_display(self):
        pass
        new = Toplevel(self.parent)
        new.title('Images for Index '+str(self.index-1))
        results_dir = self.num_data[self.catalog_file.split('/')[-1]]
        image_dir = self.image_data[self.catalog_file.split('/')[-1]]
        img_window= Display(new,self.index-1,results_dir,image_dir)

class Display(Frame):

    def __init__(self,parent,index,results,images):
        Frame.__init__(self,parent)
        self.parent = parent
        self.index = index
        self.results = results
        self.fits = images
        self.pack(fill=BOTH)
        self.initUI()

    def initUI(self):
        frame = Frame(self,relief=RAISED,bd=1)
        frame.pack(expand=2,fill=BOTH)
        close_button = Button(self,text='Close',command=self.parent.destroy)

        out_file = self.results+'index_'+str(self.index)+'_images.png'
        display.display(self.index,self.fits,show=False,save=out_file)
        target_images = Image.open(out_file)
        background = ImageTk.PhotoImage(target_images)
        label=Label(frame,image=background)
        label.image=background

        label.pack(fill=BOTH)
        close_button.pack(side=RIGHT,padx=5,pady=5)
        
        
def main():
    root = Tk()
    root.geometry('2000x360')
    app = Data(root)
    root.mainloop()

if __name__ == '__main__':
    main()
