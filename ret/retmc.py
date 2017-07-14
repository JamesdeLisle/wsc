import numpy as np
import random

class MonteCarlo:

    def __init__( self, cost ):
        
        self.cost = cost
        self.G_IN_now = np.zeros( shape=(2,2), dtype=np.complex128 )
        self.cost_now = np.zeros( shape=(2,2), dtype=np.complex128 )
        self.G_IN_new = np.zeros( shape=(2,2), dtype=np.complex128 )
        self.cost_new = np.zeros( shape=(2,2), dtype=np.complex128 )
        self.nAcc = 0.0
        self.nAtt = 0.0
        self.fAcc = 0.0
        self.fAccIdeal = 0.5
        self.standDev = 0.1
        self.standDev_min = 1e-14
        self.standDev_max = 0.1
        self.accProb = 0.0
        self.temp = 0.0
        self.temp_min = 1.0
        self.temp_max = 2 * pow( 10, 5 ) 
        self.step = 1
        self.step_max = 5 * pow( 10, 4 ) 
 
    def do( self ):

        self.initialise()
        while self.step < self.step_max:
            self.getTemp()
            self.nAtt += 1
            self.getStandDev()
            self.getNew()
            self.getProb()
            draw = np.log( random.random() )
            if draw <= self.accProb:
                self.G_IN_now = self.G_IN_new
                self.cost_now = self.cost_new
                self.nAcc += 1
            self.fAcc = self.nAcc / self.nAtt
            self.step += 1
        
        return self.G_IN_now

    def initialise( self ):

        self.G_IN_now += np.random.rand( 2, 2 )
        self.G_IN_now += 1j * np.random.rand( 2, 2 )
        self.cost_now = self.cost.g_RET_FUNC( self.G_IN_now ) 

    def getNew( self ):
        
        for i, col in enumerate( self.G_IN_now ):
            for j, row in enumerate( col ):
                self.G_IN_new[ i, j ] += random.gauss( np.real( row ), self.standDev )
                self.G_IN_new[ i, j ] += 1j * random.gauss( np.imag( row ), self.standDev )

        self.cost_new = self.cost.g_RET_FUNC( self.G_IN_new )
    
    def getProb( self ):
        
        self.accProb = -self.temp * sum( ( ( self.cost_new - self.cost_now ) ).flatten() ) 

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



        

