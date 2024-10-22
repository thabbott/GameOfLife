import numpy as np
import matplotlib.pyplot as plt
import os.path

N = 100
M = 100
pname = None

# Initial instructions
print("Click in grid boxes to place or remove cells" +
    " and close the figure when done.")

fname = input("Enter a name for your input file: ")

# Load file if it exists....
if os.path.isfile(f"entries/{fname}"):
    print("File exists; loading for modification")
    cells = np.zeros((N*M,))
    ii = 0
    with open(f"entries/{fname}", "r") as f:
        for line in f:
            for ch in line:
                if ch == "0":
                    cells[ii] = 0
                    ii += 1
                elif ch == "1":
                    cells[ii] = 1
                    ii += 1
    cells = np.reshape(cells, (N,M))

# ... otherwise, create a new file
else:
    print("Creating new file")
    cells = np.zeros((N,M))

# Set up figure
fig = plt.figure(figsize = (7,7), dpi = 100)
plt.xticks(np.arange(-0.5, M + 0.5 + 1, 1), [""]*(M+2))
plt.yticks(np.arange(-0.5, N + 0.5 + 1, 1), [""]*(N+2))
plt.grid()
plt.gca().tick_params(length = 0, grid_alpha = 0.5)
im = plt.imshow(cells, cmap = "Greys", vmin = 0, vmax = 1)
ann = plt.annotate(str(np.int64(np.sum(cells))), xy=(0.004, 1.015), fontsize=14, xycoords="axes fraction")
plt.title(fname)


def read_pattern(pname, suppress_print = False):
    if os.path.isfile("patterns/"+pname):
        if not suppress_print: print(f"Pattern '{pname}' exists; loading.")
        with open("patterns/"+pname, "r") as f:
            pattern_chars = ""
            for line in f:
                if (line[0] == "#"): pass
                elif ("x" in line) or ("y" in line):
                    for phrase in line.split(","):
                        if "x" in phrase:
                            m = np.int64(phrase.split("=")[1])
                        if "y" in phrase:
                            n = np.int64(phrase.split("=")[1])
                    cell = np.zeros((n,m))
                    i = 0
                else:
                    pattern_chars += line.replace("\n","")
                
            rle_lines = pattern_chars.replace("!", "").split("$")
            for rle_line in rle_lines:
                if len(rle_line) != 0:
                    cell[i,:] = decode_rle(rle_line, m)
                i+=1
        return cell
    else:
        if not suppress_print: print(f"Pattern '{pname}' does not exist.")
        return
    
def decode_rle(rle_line, m):
    row = np.zeros(m)
    j = 0
    j_inc = 1
    for ch in seperate_string_number(rle_line):
        if ch.isdigit():
            j_inc = np.int64(ch)
            continue
        elif ch == "b":
            row[j:j+j_inc] = 0.
        elif ch == "o":
            row[j:j+j_inc] = 1.
        j += j_inc
        j_inc = 1
        
    return row

def seperate_string_number(string):
    previous_character = string[0]
    groups = []
    newword = string[0]
    for x, i in enumerate(string[1:]):
        if i.isnumeric() and previous_character.isnumeric():
            newword += i
        else:
            groups.append(newword)
            newword = i

        previous_character = i

        if x == len(string) - 2:
            groups.append(newword)
            newword = ''
    return groups


class PatternCanvas:
    def __init__(self, fig):
        self.fig = fig
        self.ax = fig.axes[0]
        self.ann = ann
        self.pname = None
        self.ptransform = None
    
    def connect(self):
        self.cid_button = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.onkey)
        self.cid_close = self.fig.canvas.mpl_connect('close_event', self.onclose)
        self.cid_hover = self.fig.canvas.mpl_connect("motion_notify_event", self.onhover)
    
    # Click event handler: toggle cells
    def onclick(self, event):
        if event.inaxes == self.ax:
            ix = int(np.rint(event.xdata))
            iy = int(np.rint(event.ydata))
            if self.pname is not None:
                cell = read_pattern(self.pname)
                if cell is not None:
                    
                    if self.ptransform is not None:
                        for transform in self.ptransform.split("_"):
                            if transform == "r90":
                                cell = cell[:,::-1].transpose()
                            if transform == "r180":
                                cell = (cell[:,::-1].transpose())[:,::-1].transpose()
                            if transform == "rx":
                                cell = cell[:,::-1]
                            if transform == "ry":
                                cell = cell[::-1,:]
                    
                    (n, m) = cell.shape
                    (N, M) = cells.shape
                    
                    cells[iy:min(N,iy+n), ix:min(M,ix+m)] = cell[:min(n, N-iy), :min(m, M-ix)]
                    if iy+n > N:
                        cells[:iy+n-N, ix:min(M,ix+m)] = cell[min(n, N-iy): n, :min(m, M-ix)]

                im.set_data(cells)
                self.ann.set_text(str(np.int64(np.sum(cells))))
                plt.pause(0.001)
            else:
                if cells[iy,ix] == 0:
                    cells[iy,ix] = 1
                else:
                    cells[iy,ix] = 0
                im.set_data(cells)
                self.ann.set_text(str(np.int64(np.sum(cells))))
                plt.pause(0.001)
            
    # Key event handler: query name of pattern
    def onkey(self, event):
        # Add pattern
        if event.key == 'a':
            pstr = input("Enter the name of a pattern to be placed: ")
            self.pname = pstr.split(".")[0]
            if len(pstr.split(".")) > 1:
                self.ptransform = pstr.split(".")[1]
        # Toggle out of adding pattern
        if event.key == 't':
            self.pname = None
            self.ptransform = None
            im.set_data(cells)
            plt.pause(0.001)
            
    def onhover(self, event):
        if event.inaxes == self.ax:
            ix = int(np.rint(event.xdata))
            iy = int(np.rint(event.ydata))
            if iy < 0: iy = 0
            tmp = cells.copy()
            if self.pname is not None:
                cell = read_pattern(self.pname, suppress_print = True)
                if cell is not None:

                    if self.ptransform is not None:
                        for transform in self.ptransform.split("_"):
                            if transform == "r90":
                                cell = cell[:,::-1].transpose()
                            if transform == "r180":
                                cell = (cell[:,::-1].transpose())[:,::-1].transpose()
                            if transform == "rx":
                                cell = cell[:,::-1]
                            if transform == "ry":
                                cell = cell[::-1,:]
                    
                    (n,m) = cell.shape
                    (N, M) = cells.shape

                    tmp[iy:min(N,iy+n), ix:min(M,ix+m)] = 0.4*cell[:min(n, N-iy), :min(m, M-ix)]
                    if iy+n > N:
                        tmp[:iy+n-N, ix:min(M,ix+m)] = 0.4*cell[min(n, N-iy):n, :min(m, M-ix)]

                im.set_data(tmp)
                plt.pause(0.0002)

    # Close event handler: save input file
    def onclose(self, event):
        with open(f"entries/{fname}", "w") as f:
            for j in range(N):
                for i in range(M):
                    f.write("%d " % cells[j,i])
                f.write("\n")
        self.disconnect()

    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cid_button)
        self.fig.canvas.mpl_disconnect(self.cid_key)
        self.fig.canvas.mpl_disconnect(self.cid_close)

pattern = PatternCanvas(fig)
pattern.connect()
plt.show()
