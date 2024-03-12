from manim import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import main
import concurrent.futures

class NBodyScene(Scene):
    def construct(self):
        # Load simulation data based on the selected scenario
        file_paths = self.load_data()
        pos_stack, v_sqd_stack, Energy_arr = self.load_simulation_data(file_paths)

        # Create particles and trails
        particles = []
        trails = []
        for i in range(num_body):
            x, y, z = pos_stack[0, i], pos_stack[1, i], pos_stack[2, i]
            particle = Sphere(radius=0.2)
            particle.shift(np.array([x, y, z]))
            trail = particle.copy().set_color(YELLOW).apply_depth_test().set_stroke(width=0.5)
            particles.append(particle)
            trails.append(trail)

        # Create energy graphs
        energy_graphs = VGroup(
            self.get_graph(x_min=0, x_max=10, func=lambda x: Energy_arr[0, int(x / dt)], color=CYAN),
            self.get_graph(x_min=0, x_max=10, func=lambda x: Energy_arr[1, int(x / dt)], color=BLUE),
            self.get_graph(x_min=0, x_max=10, func=lambda x: Energy_arr[2, int(x / dt)], color=BLACK),
        )
        energy_graphs.arrange(DOWN, buff=1)
        energy_graphs.shift(LEFT * 3)

        self.add(trails, particles, energy_graphs)

        # Animation loop
        for i in range(1, len(pos_stack) // 3):
            new_particles = []
            new_trails = []
            for j in range(num_body):
                x, y, z = pos_stack[0 + (3 * i), j], pos_stack[1 + (3 * i), j], pos_stack[2 + (3 * i), j]
                velocity_magnitude = np.sqrt(v_sqd_stack[i, j])
                color = thermal_color_map(velocity_magnitude, mode='global', scale='w2r')
                particles[j].shift(np.array([x, y, z]) - particles[j].get_center())
                particles[j].set_color(color)
                new_particles.append(particles[j].copy())
                new_trails.append(trails[j].copy().shift(np.array([x, y, z]) - trails[j].get_center()))

            self.remove(*particles, *trails)
            self.add(*new_particles, *new_trails)
            self.wait(dt)

        # Render the scene to a video file
        self.renderer.camera.background_color = BLACK
        self.renderer.camera.set_cam(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.renderer.render_quality = "high"
        self.renderer.render_scene(scene=self, movie_name="n_body_simulation.mp4")

    def load_data(self):
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
        confirm_button = tk.Button(root, text="Confirm", command=lambda: root.destroy())
        confirm_button.pack(pady=10)
        # Run the main event loop
        root.mainloop()

        selected_value = selected_option.get()
        file_paths = [
            'Pos_outputs/' + selected_value + '__pos_out.csv',
            'Pos_outputs/' + selected_value + '__vsqd_out.csv',
            'Pos_outputs/' + selected_value + '__energy_out.csv',
            'Pos_outputs/' + selected_value + '__com_out.csv'
        ]
        return file_paths

    def load_data(self, file_path):
        return main.np.loadtxt(file_path)

    def load_simulation_data(self, file_paths):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            data_results = list(executor.map(self.load_data, file_paths))

        pos_stack, v_sqd_stack, Energy_arr, COM = data_results
        return pos_stack, v_sqd_stack, Energy_arr

def thermal_color_map(v_sqd, mode='global', scale='w2r'):
    if mode == 'global':
        max_v_sqd = np.max(v_sqd_stack)
        min_v_sqd = np.min(v_sqd_stack)
    else:
        raise ValueError("mode should be 'global'")

    q = (v_sqd - min_v_sqd) / (max_v_sqd - min_v_sqd)

    if scale == 'w2r':
        R = 1.0
        G = 1 - q
        B = np.exp(-6 * q)
    else:
        raise ValueError("scale should be 'w2r'")

    return rgb_to_color([R, G, B])

# Render the scene
scene = NBodyScene()
scene.render()
