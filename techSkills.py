from wifi import Cell, Scheme
cells = list(Cell.all('wlp4s0'))
for cell in cells:
    print(cell.address + " " + cell.ssid + ' ' + str(cell.channel))
