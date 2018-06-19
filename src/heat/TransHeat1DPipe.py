"""
  Copyright (c) 2016- by Dietmar W Weiss

  This is free software; you can redistribute it and/or modify it
  under the terms of the GNU Lesser General Public License as
  published by the Free Software Foundation; either version 3.0 of
  the License, or (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this software; if not, write to the Free
  Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
  02110-1301 USA, or see the FSF site: http://www.fsf.org.

  Version:
      2018-06-19 DWW
"""

from tempfile import gettempdir
from numba import autojit
import numpy as np
import matplotlib.pyplot as plt

from grayboxes.Base import Base

"""
    Demonstrates discretisation of a 1D transient heat conduction problem
    with Robin boundary conditions without heat source.

    Modelling:
        A liquid with initial temperature T_in,0 = T_out flows trough a pipe
        with initial wall temperature T_wal,0 = T_out. The liquid temperature
        jumps from T(x=x_in,t=0)=T_out to T(x=x_in,t>0)=T_in.

        The transient response of the wall temperature is measured with a
        thermocpuple on the outer wall surface. Wanted is an estimate of the
        time when the difference between outer surface temperature T_wal_out
        and liquid temperature T_in is less a given limit.

        The heat transfer from the flowing liquid to the inner surface is
        considered by a Robin boundary condition. The inner heat transfer
        cofficient is estimated from the Nusselt number formula by
        Dittus-Boelter. The outer heat transfer by natural convection is also
        considered by a Robin boundary condition. The outer heat transfer
        coefficient is assumed to be constant.

        From the conservation of energy follows:
            q_dot_in = q_dot_wal = q_dot_out

            At inner surface:
                q_dot_in = alpha_in * (T_in - T_wal_in)
                q_dot_in = -lambda_wal * dT/dx_in
                dT/dx_in ~ (T[1] - T[0]) / (X[1] - X[0])

            At outer surface:
                q_dot_out = alpha_out * (T_out - T_wal_out)
                q_dot_out = lambda_wal * dT/dx_out
                dT/dx_out ~ (T[-1] - T[-2]) / (X[-1] - X[-2])
                ([-1] is index of last element and [-2] of second last one)


           flowing
        <--liquid---> <-----------wall----------> <----gas---->

                     |///////////////////////////|
                     |///////////////////////////|
              forced |///  heat conduction  /////| natural
          convection |///////////////////////////| convection
                     |///////////////////////////|
            q_dot_in | q_dot_wal=-lambda*dT/dx   | q_dot_out
            -------> | ------>                   | -------->
                T_in | T_wal_in                  | T_out
            alpha_in | dT/dx_in=(T1-T0)/(X1-X0)  | alpha_out
                     |///////////////////////////|
                     |///////////////////////////|

               X[0]     X[1]              X[-2]     X[-1]
        +---------+--|--+---------------------+--|--+---------> x
                     |                           |
                   x_in                        x_out


    Discretisation:
        Explicit time discretisation in 1D space by means of finite
        differences. Discretisation for both cylindrical and Cartesian
        coordinates.

    Note:
        Function temperatureInWallForActualTimeStep() is compiled just-in-time
        with the @autojit decorator.
"""


@autojit
def temperatureInWallForActualTimeStep(X, T, T_old, Fo, alpha_in, alpha_out,
                                       T_in, T_out, lambda_wal, isCylinder):
    """
    Computes the temperature in the wall for the actual time step
    This function is called from TransHeat1DPipe.task()

    Args:
        X (1D array of float):
            coordinates [m]

        T (1D array of float):
            actual temperature [K]
            -- will be modified

        T_old (1D array of float):
            temperature of previous time step [K]
            -- will be modified

        alpha_in (float):
            inner heat transfer coefficient [W/(m2 K)]

        alpha_out (float):
            outer heat transfer coefficient [W/(m2 K)]

        T_in (float):
            temperature of inner liquid [K]

        T_out (float):
            temperature of outer gas [K]

        lambda_wal (float):
            thermal conductivity of wall [W/(m K)]

        isCylinder (bool):
            if True then space discretisation for cylinder geometry


    Note:
        The implementation as a pre-compiled external function increases the
        execution speed. Example:
            foo(nx=200, v=10, T_in=10000, T_out=0, alpha_out=5)
        --> speed up of 84 in comparison to speed without decorator '@autojit'
    """
    # space step size
    dx = X[1] - X[0]

    # surface temperatures are mean of the values close to the surface,
    # [-1] is index of last array element and [-2] of second last element
    T_wal_in = (T_old[1] + T_old[0]) * 0.5
    T_wal_out = (T_old[-1] + T_old[-2]) * 0.5

    # heat flux density by convection from liquid or gas to inner or outer face
    q_dot_in = alpha_in * (T_in - T_wal_in)
    q_dot_out = alpha_out * (T_out - T_wal_out)

    # updates the old temperatures in the nodes outside the wall
    #   -heat flux by convective heat transfer equals heat flux by conduction
    #   -in wall: q_dot_in = alpha * (T - T_wal) = lambda_wal * dT/dx_wal
    T_old[0] = T_old[1] + q_dot_in * dx / lambda_wal
    T_old[-1] = T_old[-2] + q_dot_out * dx / lambda_wal
    for i in range(1, X.size-1):
        if not isCylinder:
            dT = Fo * ((T_old[i+1] - T_old[i]) - (T_old[i] - T_old[i-1]))
        else:
            x_e = 0.5 * (X[i+1] + X[i])
            x_w = 0.5 * (X[i] + X[i-1])
            dT = Fo * (x_e * (T_old[i+1] - T_old[i]) -
                       x_w * (T_old[i] - T_old[i-1])
                       ) / X[i]
        T[i] = T_old[i] + dT

    # updates actual temperatures in the nodes outside wall
    T[0] = T[1] + q_dot_in * dx / lambda_wal
    T[-1] = T[-2] + q_dot_out * dx / lambda_wal


class TransHeat1DPipe(Base):
    def __init__(self, identifier='TransHeat1DPipe'):
        super().__init__(identifier=identifier)
        self.version = '250118_dww'

    def plotSingleTimeStep(self, lineStyle='--'):
        """
        Plots wall temperature distribution

        Args:
            lineStyle (string, optional):
                line style of temperature curves, '-': solid, '--': dashed,
                'r-o': red+points, ...
        """
        if self.show and self.i_t % self.show == 0:
            self.show *= 2
            xw, xe, Tw, Te = self.X[0], self.X[-1], self.T[0], self.T[-1]
            self.X[0] = (self.X[0] + self.X[1]) * 0.5
            self.X[-1] = (self.X[-1] + self.X[-2]) * 0.5
            self.T[0] = (self.T[0] + self.T[1]) * 0.5
            self.T[-1] = (self.T[-1] + self.T[-2]) * 0.5
            plt.plot(self.X*1e3, self.T, '--')
            self.X[0], self.X[-1], self.T[0], self.T[-1] = xw, xe, Tw, Te

    def pre(self, **kwargs):
        """
        Performs pre-processing, this method is called from __call__()

        Args:
            kwargs (dict, optional):
                keyword arguments
        """
        # common
        self.show         = kwargs.get('show',         1)
        figsize           = kwargs.get('figsize',      (10, 8))
        self.save         = kwargs.get('save',         False)
        self.path         = kwargs.get('path',         gettempdir().replace(
                                                              '\\', '/') + '/')
        # flowing liquid
        self.v            = kwargs.get('v',            3.)
        self.T_in         = kwargs.get('T_in',         10.)
        nu_in             = kwargs.get('nu_in',        1.307e-6)
        c_p_in            = kwargs.get('c_p_in',       4.192e3)
        rho_in            = kwargs.get('rho_in',       999.7)
        lambda_in         = kwargs.get('lambda_in',    0.582)

        # gas
        self.T_out        = kwargs.get('T_out',        20.)

        # wall
        self.isCylinder   = kwargs.get('isCylinder',   True)
        self.T0           = kwargs.get('T0',           self.T_out)
        D                 = kwargs.get('D',            15e-3)
        thickness         = kwargs.get('thickness',    1e-3)
        Ra_roughness      = kwargs.get('Ra_roughness', 1.6e-6)
        rho_wal           = kwargs.get('rho_wal',      8000.)
        cp_wal            = kwargs.get('cp_wal',       500.)
        self.lambda_wal   = kwargs.get('lambda_wal',   15.)

        # heat transfer in aurrounding gas
        self.alpha_out    = kwargs.get('alpha_out',    5.)

        # numeric
        self.delta_T_wal  = kwargs.get('delta_T_wal',  abs(self.T_out-
                                       self.T_in) * 3e-2)   # 3% difference
        self.nx           = kwargs.get('nx',           100)
        self.t_max        = kwargs.get('t_max',        1000.)
        self.i_t_max      = kwargs.get('i_t_max',      round(1e12))
                                                            # stop criterion
        a_wal = self.lambda_wal / (rho_wal * cp_wal)        # thermal diffusity
        self.x_in = D * 0.5                                 # inner radius
        self.x_out = self.x_in + thickness                  # outer radius

        # heat transfer inside flowing liquid
        a_in = lambda_in / (c_p_in * rho_in)                # thermal diffusity
        Re_in = self.v * D / nu_in
        Pr_in = nu_in / a_in
        Nu_in = 0.023 * Re_in**0.8 * Pr_in**0.3  # Dittus-Boelter (n=0.3:cool.)
        self.alpha_in = Nu_in * lambda_in / D       # inner heat transfer coeff

        self.dx = (self.x_out - self.x_in) / self.nx        # space step size
        self.dt = self.dx**2 / (2 * a_wal)
        self.Fo = self.dt * a_wal / self.dx**2

        # print local parameters
        self.write('+++ Parameters:')
        lst = dict(locals(), **self.__dict__)
        for key in sorted(lst, key=lambda s: s.lower()):
            if not key.startswith('_') and key not in \
                ('program', 'save', 'fig', 'show', 'figsize', 'self', 'kwargs',
                 'version', 'X', 'T', 'T_old'):
                self.write('{:>15}: {}'.format(key, lst[key]))
        self.write()

        self.X = np.linspace(self.x_in - 0.5 * self.dx,
                             self.x_out + 0.5 * self.dx, self.nx+2)
        self.T = np.full(self.X.size, float(self.T0))
        self.T_old = np.copy(self.T)

        # check that center of boundary cells are at wall positions
        assert np.isclose(2*self.x_in, self.X[0]+self.X[1]), \
            str(self.x_in)+' '+str(self.X[0])+' '+str(self.X[1])
        assert np.isclose(2*self.x_out, self.X[-1]+self.X[-2]), \
            str(self.x_out)+' '+str(self.X[0])+' ' + str(self.X[1])
        assert np.isclose(self.dx, self.X[1]-self.X[0]), \
            str(self.dx)+' '+str(self.X[1])+' '+str(self.X[0])
        assert np.isclose(self.dx, self.X[-1]-self.X[-2]), \
            str(self.dx)+' '+str(self.X[-1])+' '+str(self.X[-2])

        # plot empty diagram with settings for x and T
        self.fig = plt.figure(figsize=figsize)
        plt.xlim(self.x_in * 1e3, self.x_out * 1e3)
        plt.ylim(min(self.T_in, self.T_out)-.5, max(self.T_in, self.T_out)+.5)
        plt.xlabel('$r$ [mm]')
        plt.ylabel(r'$T$ [$\degree$C]')
        plt.grid()

    def task(self, **kwargs):
        """
        Performs task, this method is called from control()

        Args:
            kwargs (dict, optional):
                keyword arguments
        """
        self.t = 0.
        self.i_t = 0
        while True:

            # swap old and actual temperature array
            self.T, self.T_old = self.T_old, self.T

            self.plotSingleTimeStep('--')

            # computes actual wall temperature
            temperatureInWallForActualTimeStep(
                self.X, self.T, self.T_old, self.Fo, self.alpha_in,
                self.alpha_out, self.T_in, self.T_out, self.lambda_wal,
                self.isCylinder)
            if self.i_t > 0 and np.abs(self.T[-1] -
                                       self.T_in) < self.delta_T_wal:
                self.plotSingleTimeStep()
                # plota final wall temperature distribution
                self.write('+++ t_end: ', self.t, ' (', self.i_t, ' steps)')
                self.plotSingleTimeStep('r-o')
                return self.t

            if self.t > self.t_max:
                self.write('\n??? Break: physical time > limit: ', self.t_max)
                return -1.0

            if self.i_t_max and self.i_t > self.i_t_max:
                self.write('\n??? Break: steps > limit: ', self.i_t_max)
                return -1.0

            self.t += self.dt
            self.i_t += 1

    def post(self, **kwargs):
        """
        Performs post-processing, this method is called from __call__()

        Args:
            kwargs (dict, optional):
                keyword arguments
        """
        plt.title('v : ' + str(self.v) + ' m/s ' +
                  r' $\alpha_{out}$ : ' + str(self.alpha_out) +
                  r' Wm$^{-2}$K$^{-1}$' +
                  r'  $T_{in}$ : ' + str(self.T_in) + r' $\degree$C' +
                  r'  $T_{out}$ : ' + str(self.T_out) + r' $\degree$C' +
                  r'  $\vert T_{wall}^{out}-T_{in}\vert$ : ' +
                  str(self.delta_T_wal) +
                  ' K' +  # + r'  $N_x$ : ' + str(nx) +
                  r'  $t_{end}$ : ' + '{:5.3f}'.format(self.t) + ' s')
        plt.show()
        if self.save:
            self.fig.savefig(self.path + __name__ + '.png',
                             bbox_inches='tight')
        plt.close()


# Examples ####################################################################

if __name__ == "__main__":
    ALL = 0

    foo = TransHeat1DPipe()

    if 1 or ALL:
        #  Single call of response time computation
        t_response = foo(nx=128, isCylinder=True, v=10, T_in=100, T_out=20,
                         t_max=100, alpha_out=5, delta_T_wal=0.1)
    if 0 or ALL:
        # Demonstrates effect of space step size
        collect_t_nx = []
        for nx in [4, 8, 16, 32, 64, 128, 256, 512]:
            t_response = foo(nx=nx, v=10, T_in=100, T_out=20,
                             alpha_out=5, delta_T_wal=0.1)
            collect_t_nx.append((nx, t_response))

        plt.title('Effect of space step size on response time')
        plt.xlabel('$N_x$ [/]')
        # plt.xscale('log', nonposy='clip')
        plt.ylabel('$t_{response}$ [s]')
        t_nx = np.asfarray(collect_t_nx)
        plt.plot(t_nx.T[0], t_nx.T[1])
        plt.grid()
        plt.show()
