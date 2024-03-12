import manim as mnm
import tkinter as tk
import numpy as np
import main
import matplotlib.pyplot as plt
from io import BytesIO

class NBodyScene(mnm.Scene):
    def construct(self):
        # Load simulation data based on the selected scenario
        file_paths = self.load_scenario_files()
        pos_stack, v_sqd_stack, Energy_arr, dt, num_body = self.load_simulation_data(file_paths)

        # Create particles and trails
        particles = []
        trails = []
        for i in range(num_body):
            x, y, z = pos_stack[0, i], pos_stack[1, i], pos_stack[2, i]
            particle = mnm.Sphere(radius=0.2)
            particle.shift(np.array([x, y, z]))
            trail = particle.copy().set_color(mnm.YELLOW).set_stroke(width=0.5)
            particles.append(particle)
            trails.append(trail)

        # Create a matplotlib plot
        t_values = np.arange(0, len(Energy_arr[0])) * dt
        plt.plot(t_values, Energy_arr[0], label='Kinetic Energy', color='cyan')
        plt.plot(t_values, Energy_arr[1], label='Potential Energy', color='blue')
        plt.plot(t_values, Energy_arr[2], label='Total Energy', color='black')
        plt.xlabel('Time')
        plt.ylabel('Energy')
        plt.legend()
        plt.tight_layout()

        # Convert the plot to an image and add it to the Manim scene
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()  # Close the figure after saving
        pixel_array = plt.imread(buffer, format='png')
        energy_graph = mnm.ImageMobject(pixel_array)
        energy_graph.scale(0.5)
        energy_graph.to_corner(mnm.UR)

        # Convert lists to Mobject instances
        trails = mnm.VGroup(*trails)
        particles = mnm.VGroup(*particles)

        self.add(trails, particles, energy_graph)

        # Animation loop
        for i in range(1, len(pos_stack) // 3):
            new_particles = []
            new_trails = []
            for j in range(num_body):
                x, y, z = pos_stack[0 + (3 * i), j], pos_stack[1 + (3 * i), j], pos_stack[2 + (3 * i), j]
                velocity_magnitude = np.sqrt(v_sqd_stack[i, j])
                particles[j].shift(np.array([x, y, z]) - particles[j].get_center())
                new_particles.append(particles[j].copy())
                new_trails.append(trails[j].copy().shift(np.array([x, y, z]) - trails[j].get_center()))

            self.remove(*particles, *trails)
            self.add(*new_particles, *new_trails)
            self.wait(dt)

        # Render the scene to a video file
        self.renderer.camera.background_color = mnm.BLACK
        self.renderer.camera.set_cam(phi=70 * mnm.DEGREES, theta=-45 * mnm.DEGREES)
        self.renderer.render_quality = "high"
        self.renderer.render_scene(scene=self, movie_name="n_body_simulation.mp4")

    def load_scenario_files(self):
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

    def load_simulation_data(self, file_paths):
        pos_stack = np.loadtxt(file_paths[0])
        v_sqd_stack = np.loadtxt(file_paths[1])
        Energy_arr = np.loadtxt(file_paths[2])
        COM = np.loadtxt(file_paths[3])

        dt = 0.02  # Time step used in the simulation
        num_body = pos_stack.shape[1]  # Number of particles

        return pos_stack, v_sqd_stack, Energy_arr, dt, num_body

# Render the scene
scene = NBodyScene()
scene.render(preview=False)
