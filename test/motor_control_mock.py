class MotorControlMock:
    
    theta_count = 0
    rho_count = 0

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
        if not reverse:
            self.theta_count += 1
        else:
            self.theta_count -= 1

    def rho_step(self, reverse=False):
        if not reverse:
            self.rho_count += 1
        else:
            self.rho_count -= 1
