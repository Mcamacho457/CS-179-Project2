#Visualize the route of the optimal path
#input: Path of points (array)
#Output: visualization of route
#Jason
import os # used for saving the image to the computer
from PIL import Image, ImageDraw # pillow is used to make image


def saveClusterRoutesImg(listOfPoints, clusters, centers, clusterPaths, input_filename):
    
    # convert data to pairs of coordinates
    coords = [(float(p.x), float(p.y)) for p in listOfPoints]
    #routePoints = [(float(p.x), float(p.y)) for p in finalPath]
    
    
    # bounds
    xs, ys = zip(*coords) # separates the x's and y's from coords so now have collection of x's and collection of y's
    
    # find max and min of x and of y
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    
    # make image size & smaller side 1920 px (specified)
    
    dx = max_x - min_x # span of min x to max x so total width
    dy = max_y - min_y # span of min y to max y so total height
    
    aspect = dx/dy if dy !=0 else 1 # checks to make sure the set of points is not vertically flat
    min_dim = 1920 # was specified
    
    if aspect >= 1:
        height = min_dim
        width = int(height * aspect)
    else:
        width = min_dim
        height = int(width / aspect)
        
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    
    
    # scale/convert coords to pixels adds 10 px margin
    
    def scale(x, y):
        sx = 10 + (x - min_x) / dx * (width - 20)
        sy = 10 + (y - min_y) / dy * (height - 20)
        return (sx, height - sy) # pixel position and height - sy is to keep image upright

    clusterColors = ["red", "green", "orange", "purple", "magenta"]
    
    
    # draw scaled points cluster by cluster
    for idx, cluster in enumerate(clusters):
        color = clusterColors[idx % len(clusterColors)]

        for p in cluster:
            x, y = scale(float(p.x), float(p.y))
            draw.ellipse((x-5, y-5, x+5, y+5), fill = color)
    
    # centroids
    for c in centers:
        x, y = scale(float(c.x), float(c.y))
        draw.ellipse((x-9, y-9, x+9, y+9), fill = "blue")
    
    # setting up file name
    baseName = os.path.splitext(os.path.basename(input_filename))[0]
    #D = int(round(sumOfDistance))
    fileSaveName = f"{baseName}_SOLUTION.png"   # f"{baseName}_SOLUTION_{D}.png"

    # find desktop path
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    oneDrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    if os.path.isdir(oneDrive):
        desktop = oneDrive

    os.makedirs(desktop, exist_ok=True)
    full_path = os.path.join(desktop, fileSaveName)

    # saving the image to the computer
    img.save(full_path)
    print(f"Image saved to: {full_path}")
    return full_path