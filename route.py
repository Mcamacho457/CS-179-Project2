#Visualize the route of the optimal path
#input: Path of points (array)
#Output: visualization of route
#Jason
import os # used for saving the image to the computer
import matplotlib.pyplot as plt # create  graph/image using matplotlib (good for graphs)


def saveClusterRoutesImg(listOfPoints, clusters, centers, clusterPaths, input_filename):
    
    xs = [float(p.x) for p in listOfPoints]
    ys = [float(p.y) for p in listOfPoints]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    dx = max_x - min_x or 1 # this is just in case max and min val is same val so dont get 0
    dy = max_y - min_y or 1

    padX = dx * 0.02 # using this to add a buffer so there is a little space around everything
    padY = dy * 0.02

    # only need 4 colors, added extra just in case
    clusterColors = ["red", "green", "orange", "purple", "magenta"]

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    ax.set_title("Drone Paths")
    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")
    ax.grid(True)

    for idx, cluster in enumerate(clusters):
        color = clusterColors[idx % len(clusterColors)]
        cx_vals = [float(p.x) for p in cluster]
        cy_vals = [float(p.y) for p in cluster]

        # for the small points in clusters
        ax.scatter(cx_vals, cy_vals, c=color, s=2, label = f"Cluster {idx+1}")

        # for the route
        if idx < len(clusterPaths) and clusterPaths[idx]:
            rx = [float(p.x) for p in clusterPaths[idx]]
            ry = [float(p.y) for p in clusterPaths[idx]]

        rx.append(rx[0])
        ry.append(ry[0])
        ax.plot(rx, ry, color=color, linewidth=1)

    landX = [float(c.x) for c in centers]
    landY = [float(c.y) for c in centers]
    ax.scatter(landX, landY, c="blue", s=120, edgecolors="black", zorder=5, label="Landing Pads")

    ax.set_xlim(min_x - padX, max_x + padX)
    ax.set_ylim(min_y - padY, max_y + padY)
    
    # setting up file name
    baseName = os.path.splitext(os.path.basename(input_filename))[0]
    #D = int(round(sumOfDistance))
    fileSaveName = f"{baseName}_OVERALL_SOLUTION.png"

    # find desktop path
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    oneDrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    if os.path.isdir(oneDrive):
        desktop = oneDrive

    os.makedirs(desktop, exist_ok=True)
    full_path = os.path.join(desktop, fileSaveName)

    # saving the image to the computer
    plt.tight_layout()
    plt.savefig(full_path, dpi=160) # dpi is 160 and figsize is 12, so this gets the dimension of 1920 pixels
    plt.close()

    print(f"Image saved to: {full_path}")
    return full_path

# comment out later just for testing 
# also add a thing that explains what the graph says 
def saveObjectiveFunctionImg(all_landings_time):
    ys = [int(i) for i in all_landings_time]
    xs = [1, 2, 3, 4]

    ys1 = [2, 4, 6, 8]

    ys2 = []
    for i in range(len(xs)):
        if (i == 0):
            ys2.append(all_landings_time[i] + 2)
        elif (i == 1):
            ys2.append(all_landings_time[i] + 4)
        elif (i == 2):
            ys2.append(all_landings_time[i] + 6)
        else:
            ys2.append(all_landings_time[i] + 8)

    plt.figure(figsize=(10, 6))
    plt.xticks(range(1,5))
    plt.plot(xs, ys, label = "Path Time vs Number Of Drones", color = "blue")
    plt.plot(xs, ys1, label = "Set Up Time vs Number Of Drones", color = "red")
    plt.plot(xs, ys2, label = "Path Time + Set Up Time vs Number Of Drones", color = "green")
    plt.xlabel("Number Of Drones")
    plt.ylabel("Time (minutes)")
    plt.title("Time vs Number Of Drones")
    plt.legend()
    plt.grid(True)
    plt.show()