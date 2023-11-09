import vpython as vp
import main

body_list = []

for i in range(main.num_body):
    x = main.pos_array[0, i]
    y = main.pos_array[1, i]
    z = main.pos_array[2, i]
    body_list.append(vp.sphere(pos=vp.vector(x, y, z), radius=1, color=vp.color.red))

pos_stack = main.numerical_sim(main.mass_array, main.pos_array, main.vel_array)
n = len(pos_stack)/3
i = 0

print(main.np.size(pos_stack))

while i < n:
    vp.rate(100)
    for j in range(main.num_body):
        x = pos_stack[0+(3*i), j]
        y = pos_stack[1+(3*i), j]
        z = pos_stack[2+(3*i), j]
        body_list[j].pos = vp.vector(x, y, z)
    i += 1