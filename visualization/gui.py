import configparser
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule

from covid_simulation.model import CovidModel


class GUI:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title('COVID-19 Agent-based Simulation')

        self.default_frame = ttk.LabelFrame(self.win, text='Simulation Settings')
        self.default_frame.grid(column=0, row=0, padx=10, pady=8)

        self.hospital_toggle_label = ttk.Label(self.default_frame, text='Activate Hospital:')
        self.hospital_toggle_label.grid(column=0, row=0, sticky='W')
        self.hospital_toggle = tk.IntVar()
        self.hospital_rad_1 = tk.Radiobutton(self.default_frame, text='Yes', variable=self.hospital_toggle, value=1)
        self.hospital_rad_1.grid(column=1, row=0, padx=8, pady=5, sticky="W")
        self.hospital_rad_2 = tk.Radiobutton(self.default_frame, text='No', variable=self.hospital_toggle, value=0)
        self.hospital_rad_2.grid(column=2, row=0, padx=8, pady=5, sticky="W")

        self.social_toggle_label = ttk.Label(self.default_frame, text='Activate Automatic Social Distancing Policy:')
        self.social_toggle_label.grid(column=0, row=1, sticky='W')
        self.social_toggle = tk.IntVar()
        self.social_rad_1 = tk.Radiobutton(self.default_frame, text='Yes', variable=self.social_toggle, value=1)
        self.social_rad_1.grid(column=1, row=1, padx=8, pady=5, sticky="W")
        self.social_rad_2 = tk.Radiobutton(self.default_frame, text='No', variable=self.social_toggle, value=0)
        self.social_rad_2.grid(column=2, row=1, padx=8, pady=5, sticky="W")

        self.manual_social_label = ttk.Label(self.default_frame, text='Manual Social Distancing Level Setting:')
        self.manual_social_label.grid(column=0, row=2, stick='W')
        self.manual_social_lvl = tk.StringVar()
        self.manual_social_selected = ttk.Combobox(self.default_frame, width=5, textvariable=self.manual_social_lvl,
                                                   state='readonly')
        self.manual_social_selected['values'] = ('0', '1', '2')
        self.manual_social_selected.grid(column=1, row=2, padx=8, pady=5, sticky="W")
        self.manual_social_selected.current(0)

        self.model_frame = ttk.LabelFrame(self.win, text='Model Settings')
        self.model_frame.grid(column=0, row=1, padx=10, pady=8)

        self.agent_number_label = ttk.Label(self.model_frame, text='Number of Agents:')
        self.agent_number_label.grid(column=0, row=0, padx=8, pady=5, sticky="W")
        self.agent_number = tk.StringVar(value=200)
        self.agent_number_entry = ttk.Entry(self.model_frame, width=10, textvariable=self.agent_number)
        self.agent_number_entry.grid(column=1, row=0, padx=8, pady=5, sticky="W")

        self.initial_infected_label = ttk.Label(self.model_frame, text='Number of Initially Infected Agents:')
        self.initial_infected_label.grid(column=0, row=1, padx=8, pady=5, sticky="W")
        self.initial_infected = tk.StringVar(value=30)
        self.initial_infected_entry = ttk.Entry(self.model_frame, width=10, textvariable=self.initial_infected)
        self.initial_infected_entry.grid(column=1, row=1, padx=8, pady=5, sticky="W")

        self.initial_healthy_mask_label = ttk.Label(self.model_frame, text='Number of Healthy Agents Wear Face Masks:')
        self.initial_healthy_mask_label.grid(column=0, row=2, padx=8, pady=5, sticky="W")
        self.initial_healthy_mask = tk.StringVar(value=40)
        self.initial_healthy_mask_entry = ttk.Entry(self.model_frame, width=10, textvariable=self.initial_healthy_mask)
        self.initial_healthy_mask_entry.grid(column=1, row=2, padx=8, pady=5, sticky="W")

        self.initial_infected_mask_label = ttk.Label(self.model_frame, text='Number of Carriers Wear Face Masks:')
        self.initial_infected_mask_label.grid(column=0, row=3, padx=8, pady=5, sticky="W")
        self.initial_infected_mask = tk.StringVar(value=2)
        self.initial_infected_mask_entry = ttk.Entry(self.model_frame, width=10,
                                                     textvariable=self.initial_infected_mask)
        self.initial_infected_mask_entry.grid(column=1, row=3, padx=8, pady=5, sticky="W")

        self.grid_width_label = ttk.Label(self.model_frame, text='Width of The Grid:')
        self.grid_width_label.grid(column=0, row=4, padx=8, pady=5, sticky="W")
        self.grid_width = tk.StringVar(value=50)
        self.grid_width_entry = ttk.Entry(self.model_frame, width=10, textvariable=self.grid_width)
        self.grid_width_entry.grid(column=1, row=4, padx=8, pady=5, sticky="W")

        self.grid_height_label = ttk.Label(self.model_frame, text='Height of The Grid:')
        self.grid_height_label.grid(column=0, row=5, padx=8, pady=5, sticky="W")
        self.grid_height = tk.StringVar(value=50)
        self.grid_height_entry = ttk.Entry(self.model_frame, width=10, textvariable=self.grid_height)
        self.grid_height_entry.grid(column=1, row=5, padx=8, pady=5, sticky="W")

        self.hospital_capacity_label = ttk.Label(self.model_frame, text='Hospital Capacity')
        self.hospital_capacity_label.grid(column=0, row=6, padx=8, pady=5, sticky='W')
        self.hospital_capacity = tk.StringVar(value=20)
        self.hospital_capacity_entry = ttk.Entry(self.model_frame, width=10, textvariable=self.hospital_capacity)
        self.hospital_capacity_entry.grid(column=1, row=6, padx=8, pady=5, sticky='W')

        self.pass_pr_frame = ttk.LabelFrame(self.win, text='Passing Probability')
        self.pass_pr_frame.grid(column=0, row=2, padx=10, pady=8)

        self.pass_pr_both_on_label = ttk.Label(self.pass_pr_frame, text='Both Agents Wear Masks:')
        self.pass_pr_both_on_label.grid(column=0, row=0, padx=8, pady=5, sticky="W")
        self.pass_pr_both_on = tk.StringVar(value=0.015)
        self.pass_pr_both_on_entry = ttk.Entry(self.pass_pr_frame, width=10, textvariable=self.pass_pr_both_on)
        self.pass_pr_both_on_entry.grid(column=1, row=0, padx=8, pady=5, sticky='W')

        self.pass_pr_carrier_on_label = ttk.Label(self.pass_pr_frame,
                                                  text='Only The Carriers Wear Masks:')
        self.pass_pr_carrier_on_label.grid(column=0, row=1, padx=8, pady=5, sticky="W")
        self.pass_pr_carrier_on = tk.StringVar(value=0.05)
        self.pass_pr_carrier_on_entry = ttk.Entry(self.pass_pr_frame, width=10, textvariable=self.pass_pr_carrier_on)
        self.pass_pr_carrier_on_entry.grid(column=1, row=1, padx=8, pady=5, sticky='W')

        self.pass_pr_contact_on_label = ttk.Label(self.pass_pr_frame,
                                                  text='Only The Healthy Contacts Wear Masks:')
        self.pass_pr_contact_on_label.grid(column=0, row=2, padx=8, pady=5, sticky="W")
        self.pass_pr_contact_on = tk.StringVar(value=0.7)
        self.pass_pr_contact_on_entry = ttk.Entry(self.pass_pr_frame, width=10, textvariable=self.pass_pr_contact_on)
        self.pass_pr_contact_on_entry.grid(column=1, row=2, padx=8, pady=5, sticky='W')

        self.pass_pr_both_off_label = ttk.Label(self.pass_pr_frame,
                                                text='Both Agents Don\'t Wear Masks:')
        self.pass_pr_both_off_label.grid(column=0, row=3, padx=8, pady=5, sticky="W")
        self.pass_pr_both_off = tk.StringVar(value=0.95)
        self.pass_pr_both_off_entry = ttk.Entry(self.pass_pr_frame, width=10, textvariable=self.pass_pr_both_off)
        self.pass_pr_both_off_entry.grid(column=1, row=3, padx=8, pady=5, sticky='W')

        self.incubation_symptomatic_frame = ttk.LabelFrame(self.win, text='Incubation Setting')
        self.incubation_symptomatic_frame.grid(column=1, row=0, padx=10, pady=8)

        self.incubation_min_label = ttk.Label(self.incubation_symptomatic_frame, text='Minimum Incubation Period:')
        self.incubation_min_label.grid(column=0, row=0, padx=8, pady=5, sticky='W')
        self.incubation_min = tk.StringVar(value=1)
        self.incubation_min_entry = ttk.Entry(self.incubation_symptomatic_frame, width=10,
                                              textvariable=self.incubation_min)
        self.incubation_min_entry.grid(column=1, row=0, padx=8, pady=5, sticky='W')

        self.incubation_max_label = ttk.Label(self.incubation_symptomatic_frame, text='Maximum Incubation Period:')
        self.incubation_max_label.grid(column=0, row=1, padx=8, pady=5, sticky='W')
        self.incubation_max = tk.StringVar(value=14)
        self.incubation_max_entry = ttk.Entry(self.incubation_symptomatic_frame, width=10,
                                              textvariable=self.incubation_max)
        self.incubation_max_entry.grid(column=1, row=1, padx=8, pady=5, sticky='W')

        self.symptomatic_min_label = ttk.Label(self.incubation_symptomatic_frame, text='Minimum Symptomatic Period:')
        self.symptomatic_min_label.grid(column=0, row=2, padx=8, pady=5, sticky='W')
        self.symptomatic_min = tk.StringVar(value=14)
        self.symptomatic_min_entry = ttk.Entry(self.incubation_symptomatic_frame, width=10,
                                               textvariable=self.symptomatic_min)
        self.symptomatic_min_entry.grid(column=1, row=2, padx=8, pady=5, sticky='W')

        self.symptomatic_max_label = ttk.Label(self.incubation_symptomatic_frame, text='Maximum Symptomatic Period:')
        self.symptomatic_max_label.grid(column=0, row=3, padx=8, pady=5, sticky='W')
        self.symptomatic_max = tk.StringVar(value=35)
        self.symptomatic_max_entry = ttk.Entry(self.incubation_symptomatic_frame, width=10,
                                               textvariable=self.symptomatic_max)
        self.symptomatic_max_entry.grid(column=1, row=3, padx=8, pady=5, sticky='W')

        self.fatality_rate_frame = ttk.LabelFrame(self.win, text='Fatality Rate')
        self.fatality_rate_frame.grid(column=1, row=1, padx=10, pady=8)

        self.fatality_rate_0_label = ttk.Label(self.fatality_rate_frame, text='0~9 Years Old:')
        self.fatality_rate_0_label.grid(column=0, row=0, padx=8, pady=5, sticky='W')
        self.fatality_rate_0 = tk.StringVar(value=0.5)
        self.fatality_rate_0_entry = ttk.Entry(self.fatality_rate_frame, width=10,
                                               textvariable=self.fatality_rate_0)
        self.fatality_rate_0_entry.grid(column=1, row=0, padx=8, pady=5, sticky='W')

        self.fatality_rate_1_label = ttk.Label(self.fatality_rate_frame, text='10~19 Years Old:')
        self.fatality_rate_1_label.grid(column=0, row=1, padx=8, pady=5, sticky='W')
        self.fatality_rate_1 = tk.StringVar(value=0.4)
        self.fatality_rate_1_entry = ttk.Entry(self.fatality_rate_frame, width=10,
                                               textvariable=self.fatality_rate_1)
        self.fatality_rate_1_entry.grid(column=1, row=1, padx=8, pady=5, sticky='W')

        self.fatality_rate_2_label = ttk.Label(self.fatality_rate_frame, text='20~29 Years Old:')
        self.fatality_rate_2_label.grid(column=0, row=2, padx=8, pady=5, sticky='W')
        self.fatality_rate_2 = tk.StringVar(value=0.2)
        self.fatality_rate_2_entry = ttk.Entry(self.fatality_rate_frame, width=10,
                                               textvariable=self.fatality_rate_2)
        self.fatality_rate_2_entry.grid(column=1, row=2, padx=8, pady=5, sticky='W')

        self.fatality_rate_3_label = ttk.Label(self.fatality_rate_frame, text='30~39 Years Old:')
        self.fatality_rate_3_label.grid(column=0, row=3, padx=8, pady=5, sticky='W')
        self.fatality_rate_3 = tk.StringVar(value=0.3)
        self.fatality_rate_3_entry = ttk.Entry(self.fatality_rate_frame, width=10,
                                               textvariable=self.fatality_rate_3)
        self.fatality_rate_3_entry.grid(column=1, row=3, padx=8, pady=5, sticky='W')

        self.fatality_rate_4_label = ttk.Label(self.fatality_rate_frame, text='40~49 Years Old:')
        self.fatality_rate_4_label.grid(column=0, row=4, padx=8, pady=5, sticky='W')
        self.fatality_rate_4 = tk.StringVar(value=0.3)
        self.fatality_rate_4_entry = ttk.Entry(self.fatality_rate_frame, width=10,
                                               textvariable=self.fatality_rate_4)
        self.fatality_rate_4_entry.grid(column=1, row=4, padx=8, pady=5, sticky='W')

        self.fatality_rate_5_label = ttk.Label(self.fatality_rate_frame, text='50~59 Years Old:')
        self.fatality_rate_5_label.grid(column=0, row=5, padx=8, pady=5, sticky='W')
        self.fatality_rate_5 = tk.StringVar(value=0.4)
        self.fatality_rate_5_entry = ttk.Entry(self.fatality_rate_frame, width=10,
                                               textvariable=self.fatality_rate_5)
        self.fatality_rate_5_entry.grid(column=1, row=5, padx=8, pady=5, sticky='W')

        self.fatality_rate_6_label = ttk.Label(self.fatality_rate_frame, text='60~69 Years Old:')
        self.fatality_rate_6_label.grid(column=0, row=6, padx=8, pady=5, sticky='W')
        self.fatality_rate_6 = tk.StringVar(value=0.4)
        self.fatality_rate_6_entry = ttk.Entry(self.fatality_rate_frame, width=10,
                                               textvariable=self.fatality_rate_6)
        self.fatality_rate_6_entry.grid(column=1, row=6, padx=8, pady=5, sticky='W')

        self.fatality_rate_7_label = ttk.Label(self.fatality_rate_frame, text='70~79 Years Old:')
        self.fatality_rate_7_label.grid(column=0, row=7, padx=8, pady=5, sticky='W')
        self.fatality_rate_7 = tk.StringVar(value=0.4)
        self.fatality_rate_7_entry = ttk.Entry(self.fatality_rate_frame, width=10,
                                               textvariable=self.fatality_rate_7)
        self.fatality_rate_7_entry.grid(column=1, row=7, padx=8, pady=5, sticky='W')

        self.fatality_rate_8_label = ttk.Label(self.fatality_rate_frame, text='80~89 Years Old:')
        self.fatality_rate_8_label.grid(column=0, row=8, padx=8, pady=5, sticky='W')
        self.fatality_rate_8 = tk.StringVar(value=0.5)
        self.fatality_rate_8_entry = ttk.Entry(self.fatality_rate_frame, width=10,
                                               textvariable=self.fatality_rate_8)
        self.fatality_rate_8_entry.grid(column=1, row=8, padx=8, pady=5, sticky='W')

        self.immunity_frame = ttk.LabelFrame(self.win, text='Immunity Settings')
        self.immunity_frame.grid(column=1, row=2, padx=10, pady=8)

        self.immunity_loss_pr_label = ttk.Label(self.immunity_frame,
                                                text='Probability Of Agents Losing Immunity After Recovery:')
        self.immunity_loss_pr_label.grid(column=0, row=0, padx=8, pady=5, sticky='W')
        self.immunity_loss_pr = tk.StringVar(value=0.83)
        self.immunity_loss_pr_entry = ttk.Entry(self.immunity_frame, width=10,
                                                textvariable=self.immunity_loss_pr)
        self.immunity_loss_pr_entry.grid(column=1, row=0, padx=8, pady=5, sticky='W')

        self.immunity_loss_min_label = ttk.Label(self.immunity_frame,
                                                 text='Minimum Time Agents Lose Immunity After Recovery:')
        self.immunity_loss_min_label.grid(column=0, row=1, padx=8, pady=5, sticky='W')
        self.immunity_loss_min = tk.StringVar(value=7)
        self.immunity_loss_min_entry = ttk.Entry(self.immunity_frame, width=10,
                                                 textvariable=self.immunity_loss_min)
        self.immunity_loss_min_entry.grid(column=1, row=1, padx=8, pady=5, sticky='W')

        self.immunity_loss_max_label = ttk.Label(self.immunity_frame,
                                                 text='Maximum Time Agents Lose Immunity After Recovery:')
        self.immunity_loss_max_label.grid(column=0, row=2, padx=8, pady=5, sticky='W')
        self.immunity_loss_max = tk.StringVar(value=14)
        self.immunity_loss_max_entry = ttk.Entry(self.immunity_frame, width=10,
                                                 textvariable=self.immunity_loss_max)
        self.immunity_loss_max_entry.grid(column=1, row=2, padx=8, pady=5, sticky='W')

        self.quarantine_frame = ttk.LabelFrame(self.win, text='Social Distancing Policy')
        self.quarantine_frame.grid(column=0, row=3, padx=10, pady=8, columnspan=2)

        self.quarantine_ratio_0_label = ttk.Label(self.quarantine_frame,
                                                  text='Level 0 Ratio Of Social-distancing Agents')
        self.quarantine_ratio_0_label.grid(column=0, row=0, padx=8, pady=5, sticky='W')
        self.quarantine_ratio_0 = tk.StringVar(value=0)
        self.quarantine_ratio_0_entry = ttk.Entry(self.quarantine_frame, width=10,
                                                  textvariable=self.quarantine_ratio_0)
        self.quarantine_ratio_0_entry.grid(column=1, row=0, padx=8, pady=5, sticky='W')

        self.quarantine_ratio_1_label = ttk.Label(self.quarantine_frame,
                                                  text='Level 1 Ratio Of Social-distancing Agents')
        self.quarantine_ratio_1_label.grid(column=0, row=1, padx=8, pady=5, sticky='W')
        self.quarantine_ratio_1 = tk.StringVar(value=0.6)
        self.quarantine_ratio_1_entry = ttk.Entry(self.quarantine_frame, width=10,
                                                  textvariable=self.quarantine_ratio_1)
        self.quarantine_ratio_1_entry.grid(column=1, row=1, padx=8, pady=5, sticky='W')

        self.quarantine_ratio_2_label = ttk.Label(self.quarantine_frame,
                                                  text='Level 2 Ratio Of Social-distancing Agents')
        self.quarantine_ratio_2_label.grid(column=0, row=2, padx=8, pady=5, sticky='W')
        self.quarantine_ratio_2 = tk.StringVar(value=0.9)
        self.quarantine_ratio_2_entry = ttk.Entry(self.quarantine_frame, width=10,
                                                  textvariable=self.quarantine_ratio_2)
        self.quarantine_ratio_2_entry.grid(column=1, row=2, padx=8, pady=5, sticky='W')

        self.level_1_threshold_label = ttk.Label(self.quarantine_frame,
                                                 text='Threshold For Agents To Start Level 1 Social-distancing Policy:')
        self.level_1_threshold_label.grid(column=0, row=3, padx=8, pady=5, sticky='W')
        self.level_1_threshold = tk.StringVar(value=0.1)
        self.level_1_threshold_entry = ttk.Entry(self.quarantine_frame, width=10,
                                                 textvariable=self.level_1_threshold)
        self.level_1_threshold_entry.grid(column=1, row=3, padx=8, pady=5, sticky='W')

        self.level_2_threshold_label = ttk.Label(self.quarantine_frame,
                                                 text='Threshold For Agents To Start Level 2 Social-distancing Policy:')
        self.level_2_threshold_label.grid(column=0, row=4, padx=8, pady=5, sticky='W')
        self.level_2_threshold = tk.StringVar(value=0.2)
        self.level_2_threshold_entry = ttk.Entry(self.quarantine_frame, width=10,
                                                 textvariable=self.level_2_threshold)
        self.level_2_threshold_entry.grid(column=1, row=4, padx=8, pady=5, sticky='W')

        self.update_btn = ttk.Button(self.win, text='Update Configuration', command=self.update_config)
        self.update_btn.grid(column=0, row=5, padx=10, pady=8)

        self.run_simulation_btn = ttk.Button(self.win, text='Run Simulation', command=self.run_simulation)
        self.run_simulation_btn.grid(column=1, row=5, padx=10, pady=8)

    def update_config(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            "; Toggle to activate hospital\n"
            "activate_hospital": str(self.hospital_toggle.get()),
            "; If auto mode is off, set the social-distancing level below (0-2) manually\n"
            "manual_social_distancing_lvl": str(self.manual_social_lvl.get()),
            "; Toggle to activate auto-social-distancing\n"
            "activate_automatic_mode": str(self.social_toggle.get())
        }
        config['covid_model'] = {
            "; Number of agents\n"
            "N": self.agent_number.get(),
            "; Number of initially infected agents\n"
            "M": self.initial_infected.get(),
            "; Number of healthy agents who wear face masks\n"
            "J": self.initial_healthy_mask.get(),
            "; Number of infected agents who wear face masks\n"
            "K": self.initial_infected_mask.get(),
            "; Width of the grid\n"
            "width": self.grid_width.get(),
            "; Height of the grid\n"
            "height": self.grid_height.get()
        }

        config['hospital_capacity'] = {
            "; Hospital Capacity\n"
            "L": self.hospital_capacity.get()
        }

        config['pass_probability'] = {
            "; Pass probability when both agents wear masks\n"
            "PASS_PR_BOTH_ON": self.pass_pr_both_on.get(),
            "; Pass probability when only the carrier wear masks\n"
            "PASS_PR_CARRIER_ON": self.pass_pr_carrier_on.get(),
            "; Pass probability when only the healthy contact wear masks\n"
            "PASS_PR_CONTACT_ON": self.pass_pr_contact_on.get(),
            "; Pass probability when both agents don't wear masks\n"
            "PASS_PR_BOTH_OFF": self.pass_pr_both_off.get()
        }

        config['incubation'] = {
            "; Minimum incubation period\n"
            "INCUBATION_MIN": self.incubation_min.get(),
            "; Maximum incubation period\n"
            "INCUBATION_MAX": self.incubation_max.get()
        }

        config['symptomatic'] = {
            "; Minimum symptomatic period\n"
            "SYMPTOMATIC_MIN": self.symptomatic_min.get(),
            "; Maximum symptomatic period\n"
            "SYMPTOMATIC_MAX": self.symptomatic_max.get()
        }

        config['fatality_rate'] = {
            "; Fatality rate for agents aged between 0~9 years old\n"
            '0': self.fatality_rate_0.get(),
            "; Fatality rate for agents aged between 10~19 years old\n"
            '1': self.fatality_rate_1.get(),
            "; Fatality rate for agents aged between 20~29 years old\n"
            '2': self.fatality_rate_2.get(),
            "; Fatality rate for agents aged between 30~39 years old\n"
            '3': self.fatality_rate_3.get(),
            "; Fatality rate for agents aged between 40~49 years old\n"
            '4': self.fatality_rate_4.get(),
            "; Fatality rate for agents aged between 50~59 years old\n"
            '5': self.fatality_rate_5.get(),
            "; Fatality rate for agents aged between 60~69 years old\n"
            '6': self.fatality_rate_6.get(),
            "; Fatality rate for agents aged between 70~79 years old\n"
            '7': self.fatality_rate_7.get(),
            "; Fatality rate for agents aged between 80~89 years old\n"
            '8': self.fatality_rate_8.get()
        }

        config['immunity_loss'] = {
            "; Probability of people losing immunity after a while\n"
            'IMMUNITY_LOSS_PR': self.immunity_loss_pr.get(),
            "; Minimum time people lose immunity after recovery\n"
            'IMMUNITY_LOSS_MIN': self.immunity_loss_min.get(),
            "; Maximum time people lose immunity after recovery\n"
            'IMMUNITY_LOSS_MAX': self.immunity_loss_max.get(),
        }

        config['quarantine_rate'] = {
            "; The ratio of people who need to self-isolate\n"
            '0': self.quarantine_ratio_0.get(),
            '1': self.quarantine_ratio_1.get(),
            '2': self.quarantine_ratio_2.get(),
        }

        config['quarantine_threshold'] = {
            "; The threshold of the ratio of agents to start social-distancing policy\n"
            'level_1_threshold': self.level_1_threshold.get(),
            'level_2_threshold': self.level_2_threshold.get(),
        }

        with open('../visualization/config.ini', 'w') as config_file:
            config.write(config_file)

        msg.showinfo('Success', 'Configuration updated successfully!')

    def run_simulation(self):
        config = configparser.ConfigParser()
        config.read('../visualization/config.ini')
        covid_model = config['covid_model']
        hospital_capacity = config['hospital_capacity']

        def agent_portrayal(agent):
            portrayal = {
                "Filled": "true",
                "Layer": 0,
            }
            if agent.has_immunity:
                portrayal["Shape"] = "immune.png"
            elif agent.is_infected and not agent.has_symptom and not agent.wear_mask:
                portrayal["Shape"] = "incubation_without_mask.png"
            elif agent.is_infected and not agent.has_symptom and agent.wear_mask:
                portrayal["Shape"] = "incubation_mask.png"
            elif agent.is_infected and agent.has_symptom and not agent.wear_mask:
                portrayal["Shape"] = "symptomatic_without_mask.png"
            elif agent.is_infected and agent.has_symptom and agent.wear_mask:
                portrayal["Shape"] = "symptomatic_mask.png"

            elif not agent.is_infected and agent.wear_mask:
                portrayal["Shape"] = "healthy_mask.png"
            else:
                portrayal["Shape"] = "healthy_without_mask.png"
            return portrayal

        grid = CanvasGrid(agent_portrayal, int(covid_model['width']), int(covid_model['height']), 800, 800)

        chart1 = ChartModule([{"Label": "Fatalities", "Color": "Black"},
                              {"Label": "Immune", "Color": "Blue"},
                              {"Label": "Healthy", "Color": "Green"},
                              {"Label": "Infected", "Color": "Orange"},
                              {"Label": "Hospital Occupation", "Color": "Yellow"}],
                             data_collector_name='data_collector')
        chart2 = ChartModule([{"Label": "Fatality Rate", "Color": "Black"},
                              {"Label": "Morbidity Rate", "Color": "Orange"}],
                             data_collector_name='data_collector')
        server = ModularServer(CovidModel,
                               [grid, chart1, chart2],
                               "COVID Model Simulation",
                               {"N": int(covid_model['N']), "M": int(covid_model['M']),
                                "J": int(covid_model['J']), "K": int(covid_model['K']),
                                "L": int(hospital_capacity["L"]),
                                "width": int(covid_model['width']),
                                "height": int(covid_model['height'])})
        server.port = 8521  # The default
        server.launch()


if __name__ == "__main__":
    gui = GUI()
    gui.win.mainloop()
