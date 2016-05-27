import commands as c  
import os

numList = [100, 120, 150, 180, 200, 300, 400]

copyFrom = "/work/cluster/burleyk/RotationProject/BoxSize_Data/cyclohexane%i_boxsize/SAMPL5_024/calculation/%s"

for num in numList:
    #os.mkdir('cyc%i' % num)
    #mol = copyFrom % (num, 'mol.*')
    #c.getoutput('cp %s cyc%i/' % (mol, num))

    #res = copyFrom % (num, 'results.*')
    #c.getoutput('cp %s cyc%i/' % (res, num))
    prod = copyFrom % (num, 'prod.*.xvg')
    c.getoutput('cp %s cyc%i/' % (prod, num))
