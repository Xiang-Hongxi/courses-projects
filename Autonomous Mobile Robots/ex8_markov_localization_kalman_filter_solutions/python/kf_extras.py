import matplotlib.pyplot as plt
import numpy as np


class KFPlot:

    def __init__(self, time_duration=50, h0=150, R=2):

        self.fig, self.axs = plt.subplots(4)
        self.fig.set_size_inches(6, 8)
        self.fig.canvas.set_window_title('Ex8 - Kalman Filter (press Esc to quit)')
        self.fig.suptitle("Height Above Ground")
        self.h_true, = self.axs[0].plot(0, 0, "-b")
        self.h_dr,   = self.axs[0].plot(0, 0, "-k")
        self.h_est,  = self.axs[0].plot(0, 0, "-r")

        self.h_vt,   = self.axs[1].plot(0, 0, "-b")
        self.h_vdr,  = self.axs[1].plot(0, 0, "-k")
        self.h_vest, = self.axs[1].plot(0, 0, "-r")

        self.h_z,    = self.axs[2].plot(0, 0, ".g")

        self.h_vx, = self.axs[3].plot(0, 0, "-m")

        self.axs[0].legend([self.h_true, self.h_dr, self.h_est], ["Ground truth", "Dead reckoning", "Kalman Filter"])
        self.axs[2].legend([self.h_z], ["Height measurements"])
        self.axs[3].legend([self.h_vx], ["Height standard deviation"])

        self.axs[-1].set_xlabel("time")
        self.axs[0].set_xlim([0, time_duration])
        self.axs[0].set_ylim([0, h0*1.2])
        self.axs[0].set_ylabel('$h$ (m)')
        self.axs[1].set_xlim([0, time_duration])
        self.axs[1].set_ylim([-10, 2])
        self.axs[1].set_ylabel('$\dot{h}$ (m/s)')
        self.axs[2].set_xlim([0, time_duration])
        self.axs[2].set_ylim([0, 1.2*h0*np.sqrt(2)])
        self.axs[2].set_ylabel('$z$ (m)')
        self.axs[3].set_xlim([0, time_duration])
        self.axs[3].set_ylim([0, 1.2 * np.sqrt(R)*np.sqrt(2)])
        self.axs[3].set_ylabel('$\sigma_h$ (m)')
        for ax in self.axs:
            ax.grid(True)
        self.fig.canvas.mpl_connect(
            "key_release_event",
            lambda event: [exit(0) if event.key == "escape" else None],
        )


    def update(self, t, x_true, x_deadreckoning, x_estimated, z, P, pause=0.01):
        # Animation
        self.h_true.set_data(t, x_true[:, 0, 0])
        self.h_dr.set_data(t, x_deadreckoning[:, 0, 0])
        self.h_est.set_data(t, x_estimated[:, 0, 0])

        self.h_vt.set_data(t, x_true[:, 1, 0])
        self.h_vdr.set_data(t, x_deadreckoning[:, 1, 0])
        self.h_vest.set_data(t, x_estimated[:, 1, 0])

        self.h_z.set_data(t, z)
        self.h_vx.set_data(t, np.sqrt(P[:, 0, 0]))

        plt.pause(pause)
