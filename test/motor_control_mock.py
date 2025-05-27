class motor_control_mock:
    
    def __init__(self):
        pass

    def motors_release(self):
        print("Motors released")

    def step(self, axis, reverse=False):
        if axis == axis.THETA:
            self.theta_step(reverse)
        elif axis == axis.RHO:
            self.rho_step(reverse)
        else:
            raise ValueError("Invalid axis. Use 'axis.THETA' or 'axis.RHO'.")

    def theta_step(self, reverse=False):
        print("t", "-" if reverse else "+")

    def rho_step(self, reverse=False):
        print("r", "-" if reverse else "+")
