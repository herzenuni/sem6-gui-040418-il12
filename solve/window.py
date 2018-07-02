from tkinter import Tk, Entry, Frame, Label, Button, Canvas, Text, messagebox, Toplevel, Listbox, Scrollbar
from solve import solve

class main(Frame):

    def savePreviousValues(self):
        length = self.previousMatrixSize

        prevValues = [None for i in range(length ** 2)]

        # Сохраним в список предыдущие значения полей ввода
        for i in range(length):
            for j in range(length):
                prevValues[i * length + j] = self.inputsList[i * length + j].get()

        return prevValues

    def savePreviousBValues(self):
        length = self.previousMatrixSize
        prevBValues = [None for i in range(length)]

        #print('prevMS: {}'.format(length))

        # Сохраним в список предыдущие значения полей ввода свободных членов
        for i in range(length):
                prevBValues[i] = self.inputsBList[i].get()

        return prevBValues

    def redrawInputs(self):
            # Сохраним значение старых инпутов
            self.prevValues = self.savePreviousValues()

            # Удалим старые инпуты
            for i in range(len(self.inputsList)):
                #self.inputsList[i].place_forget()
                self.inputsList[i].destroy()

            # Обнулим список инпутов
            self.inputsList = [None for i in range (self.currentMatrixSize ** 2)]

            # Отрисуем новые инпуты с сохранением значения старых, если есть
            for i in range(0, self.currentMatrixSize):
                self.currentY = 100 + 60 * i

                for j in range(0, self.currentMatrixSize):
                    self.currentX = 100 + 100 * j

                    obj = self.addInput(self.currentX,self.currentY)

                    self.inputsList[i * self.currentMatrixSize + j] = obj

                    valueOfCell = 0
                    if (i < self.previousMatrixSize and j < self.previousMatrixSize):
                        valueOfCell = self.prevValues[i * self.previousMatrixSize + j]

                    else:
                        valueOfCell = 0 #i * self.currentMatrixSize + j

                    obj.insert(0,valueOfCell)

            # Повторим процедуру с инпутами свободных членов
            # Сохраним значение старых инпутов
            self.prevBValues = self.savePreviousBValues()

            # Удалим старые инпуты
            for i in range(len(self.inputsBList)):
                #self.inputsBList[i].place_forget()
                self.inputsBList[i].destroy()

            # Обнулим список инпутов
            self.inputsBList = [None for i in range(self.currentMatrixSize)]

            self.currentBX = 200 + self.currentMatrixSize * 100
            # Отрисуем новые инпуты с сохранением значения старых, если есть
            for i in range(0, self.currentMatrixSize):
                self.currentBY = 100 + 60 * i

                obj = self.addInput(self.currentBX,self.currentBY)

                self.inputsBList[i] = obj

                valueOfCell = 0
                if (i < self.previousMatrixSize):
                    valueOfCell = self.prevBValues[i]


                obj.insert(0,valueOfCell)


            # Запомним текущий размер матрицы
            self.previousMatrixSize = self.currentMatrixSize

            self.scrollRegionWidth = 1000 + 100 * self.currentMatrixSize
            self.scrollRegionHeight = 1000 + 20 * self.currentMatrixSize

            self.canvas.configure(scrollregion = (0,0, self.scrollRegionWidth, self.scrollRegionHeight))

            #self.scrolling_window.configure(width = self.scrollRegionWidth, height = self.scrollRegionHeight)

    def addInput(self,px,py):
        res_e = None

        res_e = Entry(self.scrolling_area, width=5, bd=3, font='times 15')
        res_e.place(x=px, y=py)

        return res_e

    def validateMatrixSize(self,event):
        text = self.n_input.get()
        res = ''
        length = len(text)
        for i in range(length):
            c = text[i]
            if (ord(c) >= 48 and ord(c) <= 57):
                res += c
        self.n_input.delete(0,length)
        self.n_input.insert(0,res)

        try:
            if (int(text) != self.currentMatrixSize):
                self.currentMatrixSize = int(text)

                self.redrawInputs()
        except(ValueError):
            pass

    def solveButtonClicked(self,event):
        m = self.currentMatrixSize

        delimiter = 0
        delimiter_i = 0
        matrix = []
        subMatrix = []

        # Сформируем матрицу для последующей отправки в модуль решения
        for i in range(len(self.inputsList)):
            try:
                subMatrix.append(float(self.inputsList[i].get()))
            except ValueError:
                print('Ошибка в заполнении ячейки [{},{}]'.format(delimiter_i,delimiter))
                exit(1)
            delimiter += 1

            if (delimiter == m):
                try:
                    subMatrix.append(float(self.inputsBList[delimiter_i].get()))
                except ValueError:
                    print('Ошибка в заполнении ячейки коэффициентов [{}]'.format(delimiter_i))

                matrix.append(subMatrix)
                subMatrix = []
                delimiter = 0
                delimiter_i += 1

        s = solve(matrix)

        messagebox.showwarning('Решение системы','Решение системы записано в файл "Ответ.txt".')

        out = open('Ответ.txt',encoding='utf-8',mode='w')

        for x in s:
            out.write(str(x) + '\n')
        out.close()




    def fileButtonClicked(self,event):



        try:
            file = open('src.txt',encoding='utf-8')
        except FileNotFoundError:
            messagebox.showerror('Ошибка','Файл "src.txt" не найден.')
        else:
            n = None
            matrix = []
            for line in file:
                mRow = line.split(',')
                if (n == None):
                    n = len(mRow)
                matrix.append(mRow)

            self.currentMatrixSize = n - 1
            self.redrawInputs()

            for i in range(self.currentMatrixSize):
                for j in range(self.currentMatrixSize):
                    ind = i * self.currentMatrixSize + j
                    self.inputsList[ind].delete(0,len(self.inputsList[i].get()))
                    self.inputsList[ind].insert(0,matrix[i][j])

                self.inputsBList[i].delete(0, len(self.inputsBList[i].get()))
                self.inputsBList[i].insert(0,matrix[i][n-1])

            file.close()

    def __init__(self,master):
        self.master = master
        self.master.title('Решение СЛАУ')
        self.master.geometry('1245x510+70+70')
        self.master.minsize(width=1245, height=510)
        self.master.maxsize(width=1245, height=510)

        # Скроллбар для холста по вертикали
        self.scrollbar = Scrollbar(self.master, width = 16)
        self.scrollbar.place(x=0,y=10, height = 490)

        # Скроллбар для холста по горизонтали
        self.scrollbar_x = Scrollbar(self.master, width = 16, orient = 'horizontal')
        self.scrollbar_x.place(x=16,y=0, width = 1230)

        # Холст
        self.scrollRegionWidth = 1000
        self.scrollRegionHeight = 1000

        self.canvas = Canvas(self.master, height = 510, width = 1245, yscrollcommand = self.scrollbar.set, xscrollcommand = self.scrollbar_x.set, scrollregion = (0,0, self.scrollRegionWidth, self.scrollRegionHeight))
        self.canvas.place(x=16,y=100)

        # Скроллируемая область
        self.scrolling_area = Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.scrolling_area, width=5000, height=5000, anchor='nw')

        # Связывание компонентов
        self.scrollbar.config(command=self.canvas.yview)
        self.scrollbar_x.config(command=self.canvas.xview)

        self.currentMatrixSize = 3
        self.previousMatrixSize = 0

        self.prevValues = []

        self.currentX = 0
        self.currentY = 0

        self.inputsList = []
        self.inputsBList = []

        self.test = 0



        # Поле для ввода n-параметра матрицы
        self.n_input = Entry(self.master, width=20, bd=3, font='times 15')
        self.n_input.place(x=500, y=50)
        self.n_input.bind('<KeyRelease>', self.validateMatrixSize)

        self.n_input_label = Label(self.master, text='Размер матрицы')
        self.n_input_label.place(x=500, y=25)

        # Кнопка "решить"
        self.solve_button = Button(self.master, width=20, bd=3, font='times 15', text="Решить систему")
        self.solve_button.place(x=100, y=50)
        self.solve_button.bind('<Button-1>', self.solveButtonClicked)

        # Кнопка "заполнить из файла"
        self.file_button = Button(self.master, width=20, bd=3, font='times 15', text="Взять данные из файла")
        self.file_button.place(x=900, y=50)
        self.file_button.bind('<Button-1>', self.fileButtonClicked)

        self.redrawInputs()