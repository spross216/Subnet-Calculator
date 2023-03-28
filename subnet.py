import tkinter as tk
import csv
import os


class Model:
    
    def __init__(self, numSubnets, networkOctets):
        self.numSubnets = numSubnets
        self.networkOctets = networkOctets
        self.magicNumber = ""
        self.intOctet = ""
        self.ipRangeList = []
        self.ipRange = ""
        self.startingNum = 0
        self.endingNum = 0
        self.networkID = ""
        self.broadcastID = ""
        self.addressTableData = []

        self.magicNumberDict = {
            "2" : "128",
            "4" : "64",
            "8" : "32",
            "16" : "16",
            "32" : "8",
            "64" : "4"
        }

        self.intOctetDict = {
            "128" : "128",
            "64" : "192",
            "32" : "224",
            "16" : "240",
            "8" : "248",
            "4" : "252"
        }

        self.cidrDict = {
            "128" : "/25",
            "192" : "/26",
            "224" : "/27",
            "240" : "/28",
            "248" : "/29",
            "252" : "/30"
        }

    def findMagicNum(self):
        self.magicNumber = self.magicNumberDict[self.numSubnets]
        
    def findIntOctet(self):
        self.intOctet = self.intOctetDict[self.magicNumber]
    
    def findSubnetMask(self):
        self.subnetMask = "255.255.255." + self.intOctet
    
    def findCidrNotation(self):
        self.cidr = self.cidrDict[self.intOctet]
    
    def addressRange(self):
        self.endingNum += int(self.magicNumber)
        self.ipRangeList = [i for i in range(self.startingNum, self.endingNum)]
        self.networkID = self.networkOctets + str(self.ipRangeList.pop(0))
        self.broadcastID = self.networkOctets + str(self.ipRangeList.pop(-1))
        self.ipRange = self.networkOctets + str(self.ipRangeList.pop(0)) + " - " + self.networkOctets + str(self.ipRangeList.pop(-1))
        self.startingNum += int(self.magicNumber)
        self.row = [f'{self.networkID}', f'{self.ipRange}', f'{self.broadcastID}']
        self.addressTableData.append(self.row)
        self.ipRangeList.clear()
    
    def fillTable(self):
        for _ in range(int(self.numSubnets)):
            self.addressRange()
    
    def createCsv(self):
        with open("Subnet.csv", "w", newline='') as file:
            writer = csv.writer(file)

            subnetMask = ["Subnet Mask", f'{self.subnetMask}']
            writer.writerow(subnetMask)

            cidr = ["CIDR Notation", f'{self.cidr}']
            writer.writerow(cidr)

            header = ["Network ID", "IP Address Range", "Broadcast ID"]
            writer.writerow(header)

            for row in self.addressTableData:
                writer.writerow(row)
    
    

class View:

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        
    def createBoxFrame(self):
        self.boxFrame = tk.Frame(self.master)
        self.boxFrame.pack()
    
    def createPrompt(self):
        self.prompt = tk.Label(
            self.boxFrame, 
            text="Please enter the desired network octet in xxx.xxx.xxx. format, \nand select the desired number of subnets."
        )
        self.prompt.pack()
    
    def createEntryBox(self):
        self.entryBox = tk.Entry(self.boxFrame)
        self.entryBox.pack()
    
    def createButtonFrame(self):
        self.buttonFrame = tk.Frame(self.master)
        self.buttonFrame.pack()
    
    def createButtons(self):
        self.button1 = tk.Button(self.buttonFrame, text='2', command=lambda:self.controller.submitButton1Press())
        self.button1.grid(column=0, row=0)

        self.button2 = tk.Button(self.buttonFrame, text='3-4', command=lambda:self.controller.submitButton2Press())
        self.button2.grid(column=1, row=0)

        self.button3 = tk.Button(self.buttonFrame, text='5-8', command=lambda:self.controller.submitButton3Press())
        self.button3.grid(column=2, row=0)

        self.button4 = tk.Button(self.buttonFrame, text='9-16', command=lambda:self.controller.submitButton4Press())
        self.button4.grid(column=0, row=1)

        self.button5 = tk.Button(self.buttonFrame, text='17-32', command=lambda:self.controller.submitButton5Press())
        self.button5.grid(column=1, row=1)

        self.button6 = tk.Button(self.buttonFrame, text='33-64', command=lambda:self.controller.submitButton6Press())
        self.button6.grid(column=2, row=1)
    

class Controller:

    def __init__(self):
        self.master = tk.Tk()
        self.view = View(self.master, self)
    
    def initView(self):
        self.master.title("<3 Subnet Me Daddy <3")
        self.master.geometry('600x300')
        self.view.createBoxFrame()
        self.view.createButtonFrame()
        self.view.createPrompt()
        self.view.createEntryBox()
        self.view.createButtons()
    
    def initModel(self):
        self.model.findMagicNum()
        self.model.findIntOctet()
        self.model.fillTable()

    def getEntryBox(self):
        self.networkOctets = self.view.entryBox.get()
    
    def openCsv(self):
        os.system("cmd.exe /C start excel Subnet.csv")

    def initModel(self):
        self.model.findMagicNum()
        self.model.findIntOctet()
        self.model.findSubnetMask()
        self.model.findCidrNotation()
        self.model.fillTable()
        self.model.createCsv()
        self.openCsv()

    def submitButton1Press(self):
        self.getEntryBox()
        self.model = Model("2", self.networkOctets)
        self.initModel()
        

    def submitButton2Press(self):
        self.getEntryBox()
        self.model = Model("4", self.networkOctets)
        self.initModel()
        
    def submitButton3Press(self):
        self.getEntryBox()
        self.model = Model("8", self.networkOctets)
        self.initModel()
    
    def submitButton4Press(self):
        self.getEntryBox()
        self.model = Model("16", self.networkOctets)
        self.initModel()

    def submitButton5Press(self):
        self.getEntryBox()
        self.model = Model("32", self.networkOctets)
        self.initModel()

    def submitButton6Press(self):
        self.getEntryBox()
        self.model = Model("64", self.networkOctets)
        self.initModel()
    
    def main(self):
        self.view.master.mainloop()


if __name__ == "__main__":
    subnetCalc = Controller()
    subnetCalc.initView()
    subnetCalc.main()
    
