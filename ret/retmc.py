import numpy as np
import random


class MonteCarlo:

    def __init__(self, cost):

        self.cost = cost
        self.G_IN_now = np.zeros(shape=(2, 2), dtype=np.complex128)
        self.cost_now = 0.0
        self.G_IN_new = np.zeros(shape=(2, 2), dtype=np.complex128)
        self.cost_new = 0.0
        self.G_IN_min = np.zeros(shape=(2, 2), dtype=np.complex128)
        self.cost_min = 1000
        self.nAcc = 0.0
        self.nAtt = 0.0
        self.fAcc = 0.0
        self.fAccIdeal = 0.5
        self.standDev = 0.1
        self.standDev_min = 1e-14
        self.standDev_max = 0.001
        self.accProb = 0.0
        self.temp = 0.0
        self.temp_min = 1.0
        self.temp_max = 2 * pow(10, 5)
        self.step = 1
        self.step_max = 5 * pow(10, 5)

    def do(self):

        self.initialise()
        while self.step < self.step_max:
            self.getTemp()
            self.nAtt += 1
            self.getStandDev()
            self.getNew()
            self.getProb()
            # self.cout()
            draw = np.log(random.random())
            if draw <= self.accProb:
                self.G_IN_now = self.G_IN_new
                self.cost_now = self.cost_new
                self.nAcc += 1
            self.fAcc = self.nAcc / self.nAtt
            self.trackMin()
            self.step += 1
        print self.G_IN_now
        print self.cost.g_RET_FUNC( self.G_IN_now )
        print self.cost_now
        return self.G_IN_now

    def cout( self ):

        print self.G_IN_now
        print self.cost_now
        print self.G_IN_new
        print self.cost_new
        print self.accProb
        print self.step
        print '###############################'

    def initialise( self ):

        self.G_IN_now += np.random.rand( 2, 2 )
        self.G_IN_now += 1j * np.random.rand( 2, 2 )
        self.cost_now = self.flattenCost( self.cost.g_RET_FUNC( self.G_IN_now ) )
    
    def trackMin( self ):

        if self.cost_now < self.cost_min:
            self.cost_min = self.cost_now
            self.G_IN_min = self.G_IN_now
            #print self.cost_min
        else:
            pass

    def flattenCost( self, IN ):

        return sum( np.abs( IN ).flatten() )

    def getNew( self ):
        
        self.G_IN_new = np.zeros( shape=(2,2), dtype=np.complex128 )
        
        if False:
            for i, col in enumerate( self.G_IN_now ):
                for j, row in enumerate( col ):
                    if self.cost.environment[ 'HAM_R' ][ 0, 1 ] == 0.0+0.0*1j:
                        if i + j != 1:
                            self.G_IN_new[ i, j ] += 0.0
                            self.G_IN_new[ i, j ] += 1j * 0.0
                        else:    
                            self.G_IN_new[ i, j ] += random.gauss( np.real( row ), self.standDev )
                            self.G_IN_new[ i, j ] += 1j * random.gauss( np.imag( row ), self.standDev )
                    else:
                        self.G_IN_new[ i, j ] += random.gauss( np.real( row ), self.standDev )
                        self.G_IN_new[ i, j ] += 1j * random.gauss( np.imag( row ), self.standDev )
        
        if False:
            for i, col in enumerate( self.G_IN_now ):
                for j, row in enumerate( col ):
                    self.G_IN_new[ i, j ] += random.gauss( np.real( row ), self.standDev )
                    self.G_IN_new[ i, j ] += 1j * random.gauss( np.imag( row ), self.standDev )
        
        if True:
            self.G_IN_new[ 0, 1 ] += random.gauss( np.real( self.G_IN_now[ 0, 1 ] ), self.standDev )
            self.G_IN_new[ 0, 1 ] += 1j * random.gauss( np.imag( self.G_IN_now[ 0, 1 ] ), self.standDev )
            self.G_IN_new[ 0, 0 ] += random.gauss( np.real( self.G_IN_now[ 0, 0 ] ), self.standDev )
            self.G_IN_new[ 1, 1 ] += random.gauss( np.real( self.G_IN_now[ 1, 1 ] ), self.standDev )
            self.G_IN_new[ 1, 0 ] = -np.conj( self.G_IN_new[ 0, 1 ] )

        self.cost_new = self.flattenCost( self.cost.g_RET_FUNC( self.G_IN_new ) )
    
    def getProb( self ):
       
        self.accProb = -self.temp * ( self.cost_new - self.cost_now )

    def getStandDev( self ):

        sf = np.absolute( self.fAcc - self.fAccIdeal )
        if self.fAcc > self.fAccIdeal:
            self.standDev /= sf
        elif self.fAcc < self.fAccIdeal:
            self.standDev *= sf

        if self.standDev < self.standDev_min:
            self.standDev = self.standDev_min
        elif self.standDev > self.standDev_max:
            self.standDev = self.standDev_max

    def getTemp( self ):

        self.temp = self.temp_min * pow( self.temp_max / self.temp_min, ( float( self.step ) - 1 ) / ( float( self.step_max ) - 1 ) )



        

