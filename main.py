import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

class DiskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Manager App")

        # Create tabs
        self.tabs = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)

        # Add tabs to notebook
        self.tabs.add(self.tab1, text='Disk Usage')
        self.tabs.add(self.tab2, text='System Info')

        # Initialize GUI components
        self.init_disk_usage_tab()
        self.init_system_info_tab()

        # Pack the notebook
        self.tabs.pack(expand=1, fill="both")

    def init_disk_usage_tab(self):
        # Disk Usage Tab
        self.label_disk_usage = ttk.Label(self.tab1, text="Disk Usage:")
        self.label_disk_usage.pack(pady=10)

        # Create a pie chart
        self.update_disk_usage()

        # Button to update disk usage
        self.btn_update_disk_usage = ttk.Button(self.tab1, text="Update Disk Usage", command=self.update_disk_usage)
        self.btn_update_disk_usage.pack(pady=10)

    def init_system_info_tab(self):
        # System Info Tab
        self.label_most_used_app = ttk.Label(self.tab2, text="Most Used App:")
        self.label_most_used_app.pack(pady=10)

        self.label_power_consumption = ttk.Label(self.tab2, text="Most Power Consuming App:")
        self.label_power_consumption.pack(pady=10)

        # Button to update system info
        self.btn_update_system_info = ttk.Button(self.tab2, text="Update System Info", command=self.update_system_info)
        self.btn_update_system_info.pack(pady=10)

    def update_disk_usage(self):
        # Get disk usage information
        partitions = psutil.disk_partitions()
        usage = [psutil.disk_usage(partition.mountpoint) for partition in partitions]

        # Create a pie chart
        labels = [partition.device for partition in partitions]
        sizes = [u.percent for u in usage]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display the pie chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.tab1)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def update_system_info(self):
        # Get most used app and most power-consuming app
        processes = [p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])]
        most_used_app = max(processes, key=lambda x: x['cpu_percent'])
        most_power_consuming_app = max(processes, key=lambda x: x['memory_percent'])

        # Display most used app and most power-consuming app
        self.label_most_used_app.config(text=f"Most Used App: {most_used_app['name']} (PID: {most_used_app['pid']})")
        self.label_power_consumption.config(text=f"Most Power Consuming App: {most_power_consuming_app['name']} (PID: {most_power_consuming_app['pid']})")


if __name__ == "__main__":
    root = tk.Tk()
    app = DiskManagerApp(root)
    root.mainloop()
