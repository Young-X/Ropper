# coding=utf-8
#
# Copyright 2014 Sascha Schirra
#
# This file is part of Ropper.
#
# Ropper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ropper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ropperapp.loaders.loader import *
from ropperapp.rop import Ropper
from ropperapp.arch import *

import unittest

class ELF_x86(unittest.TestCase):

    def setUp(self):
        self.file = Loader.open('test-binaries/scp-ppc')

    def test_general(self):
        self.assertEqual(self.file.arch, PPC)
        self.assertEqual(self.file.type, Type.ELF)
        

    def test_gadgets(self):
        ropper = Ropper(self.file)
        gadgets = ropper.searchRopGadgets()

        gadget = gadgets[0]
        self.assertEqual(len(gadgets), 552)
        self.assertEqual(gadget.lines[0][0], 0x4fb4)
        self.assertEqual(gadget.imageBase, 0x10000000)
        self.file.manualImagebase = 0x0
        self.assertEqual(gadget.imageBase, 0x0)
        self.file.manualImagebase = None
        self.assertEqual(gadget.imageBase, 0x10000000)


    def test_jmpreg(self):
        ropper = Ropper(self.file)
        regs=['esp']
        with self.assertRaises(RopperError):
            gadgets = ropper.searchJmpReg(regs)
        

    def test_ppr(self):
        ropper = Ropper(self.file)
        
        with self.assertRaises(RopperError):
            gadgets = ropper.searchPopPopRet()
        


if __name__ == '__main__':
    unittest.main()
