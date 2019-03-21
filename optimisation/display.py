'''
Class used to visualize the optimisation problems.
'''

import os, sys
import numpy as np
import matplotlib.figure as fig
import matplotlib.pyplot as plt
import fillplots as fill

class display:
    def __init__(self,problem,
        obj_levels=20,
        x_lim=[-10,10]  , y_lim=[-10,10],
        Nx = 100        , Ny = 100,
        display=False):

        if problem.dim != 2 and problem.type != 'NLP': 
            print('File "display.py", input error\n'+
                '  Only 2D problem supported.',file=sys.stderr)
            exit()

        x_size = x_lim[1]-x_lim[0]
        y_size = y_lim[1]-y_lim[0]

        self.obj_levels = obj_levels
        self.x_lim = [ x_lim[0] - x_size*0.05, x_lim[1] + x_size*0.05]
        self.y_lim = [ y_lim[0] - y_size*0.05, y_lim[1] + y_size*0.05]
        self.Nx = Nx
        self.Ny = Ny

        self.F,_ = plt.subplots()

        # Draw the objective function
        self.contour(problem)

        # Draw constraints
        self.draw_constraints(problem)


        ax = self.F.axes[0] 
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.set_xlabel('$x_0$')
        ax.set_ylabel('$x_1$')
        ax.set_title('Feasible region and Objective height')


        if display:
            plt.show()


    # =========================================================================
    # Contour plots
    def contour(self,problem):

        levels  = self.obj_levels
        x_lim   = self.x_lim
        y_lim   = self.y_lim
        Nx      = self.Nx
        Ny      = self.Ny

        x_step = (x_lim[1]-x_lim[0]) / Nx
        y_step = (y_lim[1]-y_lim[0]) / Ny

        
        x = np.matrix(np.arange(x_lim[0],x_lim[1],x_step)).T
        y = np.matrix(np.arange(y_lim[0],y_lim[1],y_step)).T

        X1,X2 = np.meshgrid(x,y)
        F = np.zeros( (X1.shape[0],X2.shape[0]) )

        
        for i in range(x.shape[0]):
            for j in range(y.shape[0]):
                X = [X1[i,j],X2[i,j]]
                F[i,j]=problem.f(X)
        
        ax = self.F.axes[0]
        con = ax.contour(X1,X2,F,levels, cmap='jet',zorder=0)
        plt.colorbar(con,ax=ax,label='Objective Value')
    
    
    # =========================================================================
    # Constraint functions
    def draw_constraints(self,problem):

        x_lim   = self.x_lim
        y_lim   = self.y_lim
        Nx      = self.Nx
        Ny      = self.Ny

        x_step = (x_lim[1]-x_lim[0]) / Nx
        y_step = (y_lim[1]-y_lim[0]) / Ny

        x = np.matrix(np.arange(x_lim[0],x_lim[1],x_step)).T
        y = np.matrix(np.arange(y_lim[0],y_lim[1],y_step)).T

        ax = self.F.axes[0]
        # _____________________________________________________________________
        # Linear constraints

        # Inequality constraints
        if problem.In_A.size != 0:
            N_in = len(problem.In_b)
            for id in range(N_in):
                a = problem.In_A[:,id]
                b = problem.In_b[id]

                if a[1] == 0:
                    xx = (b[0] / a[0])[0,0]
                    yy = np.array(y.T)[0,:]

                    # Orientation marking feasible to left (0) or right (1)
                    if a[0] < 0: orientation = 1 
                    else: orientation = 0
                
                    ax.fill_betweenx(yy,xx,x_lim[orientation],
                        color='gray',alpha=0.4,zorder=1)

                else:
                    xx = np.array(x.T)[0,:]
                    yy = np.array( ((b - x*a[0])/a[1]).T )[0,:]

                    # Orientation marking feasible bellow (1) or above (0)
                    if a[1] < 0: orientation = 1
                    else: orientation = 0

                    ax.fill_between(xx,yy,y_lim[orientation],
                        color='gray',alpha=0.4,zorder=0)

        # Equality constraints
        if problem.Eq_A.size != 0:
            N_eq = len(problem.Eq_b)
            for id in range(N_eq):
                a = problem.Eq_A[:,id]
                b = problem.Eq_b[id]

                if a[1] == 0:
                    xx = np.matrix(np.ones((len(x),1))) * b / a[0]
                    yy = y
                else:
                    xx = x
                    yy = (b - x*a[0])/a[1]
                
                ax.plot(xx,yy, 
                    color = 'black',
                    linewidth = 2,zorder=2)

    # =========================================================================
    # Export and other utilities
    
    def export(self, filename='fig', location='figures',ext='pdf', **kwargs):

        if not os.path.isdir(location):
            os.mkdir(location)
        
        self.F.savefig(location + '/' + filename + '.' + ext, **kwargs)