import numpy as np
import matplotlib.pyplot as plt
import os.path

N = 100
M = 100

# Initial instructions
print("Click in grid boxes to place or remove cells" +
    " and close the figure when done.")
fname = input("Enter a name for your input file: ")

# Load file if it exists....
if os.path.isfile(fname):
    print("File exists; loading for modification")
    cells = np.zeros((N*M,))
    ii = 0
    with open(fname, "r") as f:
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
plt.xticks(np.arange(-0.5, M + 0.5 + 1, 1), [""]*(M+1))
plt.yticks(np.arange(-0.5, N + 0.5 + 1, 1), [""]*(N+1))
plt.grid()
plt.gca().tick_params(length = 0, grid_alpha = 0.5)
im = plt.imshow(cells, cmap = "Greys", vmin = 0, vmax = 1)
plt.title(fname)

# Click event handler: toggle cells
def onclick(event):
    ix = int(np.rint(event.xdata))
    iy = int(np.rint(event.ydata))
    if cells[iy,ix] == 0:
        cells[iy,ix] = 1
    else:
        cells[iy,ix] = 0
    im.set_data(cells)
    plt.pause(0.001)

# Close event handler: save input file
def onclose(event):
    with open(fname, "w") as f:
        for j in range(N):
            for i in range(M):
                f.write("%d " % cells[j,i])
            f.write("\n")

# Start event loop
cid = fig.canvas.mpl_connect('button_press_event', onclick)
did = fig.canvas.mpl_connect('close_event', onclose)
plt.show()

# Stop event loop on close
fig.canvas.mpl_disconnect('cid')
fig.canvas.mpl_disconnect('did')
