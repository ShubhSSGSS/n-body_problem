import vpython as vp
import main

def make_grid_3d(xmax,dx):
    # xmax = extent of grid in each direction
    # dx = grid spacing
    global grid
    grid = []
    # Create vertical lines.
    # Make xy-plane.
    for x in range(-xmax,xmax+dx,dx):
        grid.append(vp.curve(pos=[vp.vector(x,xmax,0),vp.vector(x,-xmax,0)],radius=0.05,opacity=0.1,color=vp.color.green))
    for y in range(-xmax,xmax+dx,dx):
        grid.append(vp.curve(pos=[vp.vector(xmax,y,0),vp.vector(-xmax,y,0)],radius=0.05,opacity=0.1,color=vp.color.green))
    # Make xz-plane.
    for x in range(-xmax,xmax+dx,dx):
        grid.append(vp.curve(pos=[vp.vector(x,0,xmax),vp.vector(x,0,-xmax)],radius=0.05,opacity=0.1,color=vp.color.green))
    for z in range(-xmax,xmax+dx,dx):
        grid.append(vp.curve(pos=[vp.vector(xmax,0,z),vp.vector(-xmax,0,z)],radius=0.05,opacity=0.1,color=vp.color.green))
    # Make yz-plane.
    for y in range(-xmax,xmax+dx,dx):
        grid.append(vp.curve(pos=[vp.vector(0,y,xmax),vp.vector(0,y,-xmax)],radius=0.05,opacity=0.1,color=vp.color.green))
    for z in range(-xmax,xmax+dx,dx):
        grid.append(vp.curve(pos=[vp.vector(0,xmax,z),vp.vector(0,-xmax,z)],radius=0.05,opacity=0.1,color=vp.color.green))
    return

def turn_grid(OnOrOff):
    global grid
    if (OnOrOff == "on" or OnOrOff == "On" or OnOrOff == "ON"):
        for shape in grid:
            shape.visible = True
    if (OnOrOff == "off" or OnOrOff == "Off" or OnOrOff == "OFF"):
        for shape in grid:
            shape.visible = False
    return

body_list = []


pos_stack = main.numerical_sim(main.mass_array, main.pos_array, main.vel_array)

for i in range(main.num_body):
    x = main.pos_array[0, i]
    y = main.pos_array[1, i]
    z = main.pos_array[2, i]
    body_list.append(vp.sphere(pos=vp.vector(x, y, z), radius=1, color=vp.color.red, make_trail=True,retain=2000))

n = len(pos_stack)/3
i = 0

print(main.np.size(pos_stack))

make_grid_3d(300,20)
turn_grid('on')

while i < n:
    vp.rate(100)
    for j in range(main.num_body):
        x = pos_stack[0+(3*i), j]
        y = pos_stack[1+(3*i), j]
        z = pos_stack[2+(3*i), j]
        body_list[j].pos = vp.vector(x, y, z)
    i += 1