###########################################
#
# Main MasterMind
#
# Author : Antoine-Alexis Bourdon
# Link : https://github.com/antoinealexisb/masterMind
# Version : 0.1.0
# Dependency : mastermind, gui_mastermind
#
###########################################

import mastermind
import gui_mastermind

if __name__ == '__main__' :
    mm1 = mastermind.Mastermind(8)
    mm1.lancer()
    mm2 = mastermind.Mastermind(8)
    mm2.lancer()
    vue = gui_mastermind.VueMM(mm1,mm2)
    vue.lancer()

