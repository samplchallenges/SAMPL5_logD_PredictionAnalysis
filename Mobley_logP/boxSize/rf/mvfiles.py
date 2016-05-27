import commands as c  
import os

numList = [100, 200, 300, 400, 500]

copyFrom = "/work/cluster/burleyk/RotationProject/BoxSize_ReactionField_Data/cyclohexane%i_rf/SAMPL5_024/calculation/%s"

for num in numList:
    #os.mkdir('cyc%i' % num)
    #mol = copyFrom % (num, 'mol.*')
    #c.getoutput('cp %s cyc%i/' % (mol, num))

    #res = copyFrom % (num, 'results.*')
    #c.getoutput('cp %s cyc%i/' % (res, num))
    prod = copyFrom % (num, 'prod.*.xvg')
    c.getoutput('cp %s cyc%i/' % (prod, num))
