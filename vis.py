import vpython as vp
import main
import tkinter as tk
import concurrent.futures

def thermal_color_map(v_sqd_stack,mode='local',scale='r2b'):
    colour_stack = main.np.zeros_like(pos_stack)
    for i in range(len(v_sqd_stack)):
        for j in range(len(v_sqd_stack[0])):

            if mode == 'local':    # color grading for each body as per its own max/min velocity of all times.
                max = main.np.max(v_sqd_stack[:, j])
                min = main.np.min(v_sqd_stack[:, j])
            elif mode =='global':  # color grading for each body as per max/min velocity of all bodies of all times.
                max = main.np.max(v_sqd_stack)
                min = main.np.min(v_sqd_stack)
            else:
                print('Error: Invalid parameter for mode: Fn thermal colour map...')

            q = (v_sqd_stack[i, j] - min) / (max - min)

            if scale=='r2b':
                R = (1 - q) ** 2
                G = q * (1 - q) * 4
                B = q ** 2
            elif scale=='w2r':
                R=1
                G=1-q
                B=main.np.e**(-6*q)

            else:
                print('Error: Invalid parameter for scale: Fn thermal colour map...')

            colour_stack[0 + 3 * i, j] = R
            colour_stack[1 + 3 * i, j] = G
            colour_stack[2 + 3 * i, j] = B

    return colour_stack

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

#This part of code creates a drop down to selct the scenario

def load_data(file_path):
    return main.np.loadtxt(file_path)

def on_confirm():
    global pos_stack, v_sqd_stack, Energy_arr, COM
    selected_value = selected_option.get()
    root.destroy()
    file_paths = [
        'Pos_outputs/' + selected_value + '__pos_out.csv',
        'Pos_outputs/' + selected_value + '__vsqd_out.csv',
        'Pos_outputs/' + selected_value + '__energy_out.csv',
        'Pos_outputs/' + selected_value + '__com_out.csv'
        
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        data_results = list(executor.map(load_data, file_paths))
        
    pos_stack, v_sqd_stack, Energy_arr, COM = data_results
    

# Create the main application window
root = tk.Tk()
root.title("Select a scenario")
root.geometry("400x300")
# Create a StringVar to hold the selected option
selected_option = tk.StringVar()
# Create the dropdown menu
dropdown = tk.OptionMenu(root, selected_option, "solar", "param2", "jupiter", "attractor", "binary")
dropdown.pack()
# Confirm button
confirm_button = tk.Button(root, text="Confirm", command=on_confirm)
confirm_button.pack(pady=10)
# Run the main event loop
root.mainloop()

#End of drop-down section

num_body = int(input("Enter the number of particles: "))
body_list = []

# pos_stack, v_sqd_stack, Energy_arr = main.numerical_sim(main.mass_array, main.pos_array, main.vel_array)

colour_stack = thermal_color_map(v_sqd_stack, mode='local',scale='w2r')

for i in range(num_body):
    x = pos_stack[0, i]
    y = pos_stack[1, i]
    z = pos_stack[2, i]
    body_list.append(vp.sphere(pos=vp.vector(x, y, z), radius=2, color=vp.color.red, make_trail=True, retain=10000, trail_radius=0.30))
    

# for chaos demmostration
# body_list[0].opacity=0.4
# body_list[1].opacity=0.4
# body_list[2].opacity=0.4
# body_list[3].opacity=0.4
# body_list[4].opacity=0.4
# body_list[5].opacity=0.4
# body_list[6].opacity=0.4
# body_list[7].opacity=0.4
# body_list[8].opacity=0.4
# body_list[0].color=vp.color.yellow
# body_list[1].color=vp.color.yellow
# body_list[2].color=vp.color.yellow
# body_list[3].color=vp.color.red
# body_list[4].color=vp.color.red
# body_list[5].color=vp.color.red
# body_list[6].color=vp.color.blue
# body_list[7].color=vp.color.blue
# body_list[8].color=vp.color.blue
# body_list[0].trail_color=vp.color.yellow
# body_list[1].trail_color=vp.color.yellow
# body_list[2].trail_color=vp.color.yellow
# body_list[3].trail_color=vp.color.red
# body_list[4].trail_color=vp.color.red
# body_list[5].trail_color=vp.color.red
# body_list[6].trail_color=vp.color.blue
# body_list[7].trail_color=vp.color.blue
# body_list[8].trail_color=vp.color.blue


# vp.sphere(pos=vp.vector(0,0,0),texture='BG_images/xx', radius=1000)

# body_list[4].color=vp.color.yellow
# body_list[4].radius=30
# body_list[4].emissive=True
# body_list[4].shininess=0.2

print(main.np.size(pos_stack))

make_grid_3d(300,20)
turn_grid('off')


graph = vp.graph(scroll=True, fast=False, xmin=0, xmax=10) #shd try without scroll
f1 = vp.gcurve(color=vp.color.cyan)
f2 = vp.gcurve(color=vp.color.blue)
f3 = vp.gcurve(color=vp.color.black)

n = len(pos_stack)/3
i = 1
t=0
dt=0.003

vp.scene.camera.pos = vp.vector(COM[0],COM[1],COM[2])

while i < n:
    vp.rate(200)
    for j in range(num_body):

        R = colour_stack[0 + (3 * i), j]
        G = colour_stack[1 + (3 * i), j]
        B = colour_stack[2 + (3 * i), j]

        x = pos_stack[0+(3*i), j]
        y = pos_stack[1+(3*i), j]
        z = pos_stack[2+(3*i), j]

        body_list[j].pos = vp.vector(x, y, z)
        body_list[j].trail_color = vp.vector(R,G,B) #comment this line out before chaos demonstration
        
    f1.plot(t, Energy_arr[0, i])
    f2.plot(t, Energy_arr[1, i])
    f3.plot(t, Energy_arr[2, i])

    i += 1
    t += dt